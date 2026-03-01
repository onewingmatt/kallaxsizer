#!/usr/bin/env python3
"""
Local proxy server for the Kallax Collection Calculator.
Serves index.html and proxies BGG API requests to bypass CORS.
Uses Playwright to fetch collections (since the XML API is now blocked).
"""

import http.server
import http.cookiejar
import urllib.request
import urllib.parse
import urllib.error
import json
import os
import time
import requests as req_lib
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright

PORT = 8042
BGG_BASE = "https://boardgamegeek.com"
GEEKDO_BASE = "https://api.geekdo.com"
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bgg_config.json")
DIMS_CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dims_cache.json")

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))
BROWSER_UA = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"

def load_dims_cache():
    if os.path.exists(DIMS_CACHE_FILE):
        with open(DIMS_CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_dims_cache(cache):
    with open(DIMS_CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

dims_cache = load_dims_cache()

def bgg_request(url, method="GET", data=None, content_type=None, extra_headers=None):
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("User-Agent", BROWSER_UA)
    req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
    req.add_header("Accept-Language", "en-US,en;q=0.5")
    req.add_header("Referer", "https://boardgamegeek.com/")
    if content_type:
        req.add_header("Content-Type", content_type)
    if extra_headers:
        for k, v in extra_headers.items():
            req.add_header(k, v)
    return opener.open(req, timeout=30)

# Shared requests session for geekdo API calls
geekdo_session = req_lib.Session()
geekdo_session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
})

def fetch_dims_for_game(gid):
    """Fetch physical dimensions for a single game ID."""
    key = str(gid)
    try:
        # Step 1: get version IDs
        r1 = geekdo_session.get(
            f"{GEEKDO_BASE}/api/geekitems",
            params={'objectid': str(gid), 'objecttype': 'thing', 'nosession': '1'},
            timeout=10
        )
        if r1.status_code != 200:
            return gid, None

        versions = r1.json().get('item', {}).get('links', {}).get('boardgameversion', [])
        if not versions:
            return gid, None

        # Step 2: try versions until we find one with dimensions
        for ver in versions:
            vid = ver.get('objectid')
            if not vid:
                continue
            time.sleep(0.1)  # polite rate limiting
            r2 = geekdo_session.get(
                f"{GEEKDO_BASE}/api/geekitems",
                params={'objectid': vid, 'objecttype': 'version', 'subtype': 'boardgameversion'},
                timeout=10
            )
            if r2.status_code != 200:
                continue
            item = r2.json().get('item', {})
            l = float(item.get('length', 0) or 0)
            w = float(item.get('width', 0) or 0)
            d = float(item.get('depth', 0) or 0)
            if l > 0 and w > 0 and d > 0:
                dims = sorted([l * 2.54, w * 2.54, d * 2.54], reverse=True)
                return gid, {'l': round(dims[0], 1), 'w': round(dims[1], 1), 'h': round(dims[2], 1)}
        return gid, None
    except Exception as e:
        print(f"  [{gid}] error: {e}")
        return gid, None

def fetch_dims_for_ids(game_ids, force=False):
    results = {}
    
    if force:
        uncached = game_ids
    else:
        uncached = [gid for gid in game_ids if str(gid) not in dims_cache or dims_cache[str(gid)] is None]

        # Return from cache for already-fetched games
        for gid in game_ids:
            key = str(gid)
            if key in dims_cache and dims_cache[key] is not None:
                results[key] = dims_cache[key]

    if not uncached:
        return results

    print(f"  Fetching dims for {len(uncached)} games via api.geekdo.com (Parallel)...")
    
    # Using ThreadPoolExecutor for faster fetching
    with ThreadPoolExecutor(max_workers=5) as executor:
        batch_results = list(executor.map(fetch_dims_for_game, uncached))
        
    for gid, dims in batch_results:
        key = str(gid)
        dims_cache[key] = dims
        if dims:
            results[key] = dims

    save_dims_cache(dims_cache)
    return results

def scrape_bgg_collection(username):
    """Use Playwright to scrape the collection page for games (bypasses XML API blockage)."""
    print(f"Scraping collection for {username} via Playwright...")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                ]
            )
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = context.new_page()
            all_games = []
            page_num = 1
            
            while True:
                url = f"https://boardgamegeek.com/collection/user/{username}?own=1&objecttype=thing&subtype=boardgame&page={page_num}"
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                
                # Wait for the table to load
                try:
                    page.wait_for_selector(".collection_table", timeout=10000)
                except:
                    # If it's page 1, might just be empty. If it's page > 1, we might have hit the end unexpectedly
                    if page_num == 1:
                        print("  Table selector not found, collection might be empty.")
                    break
                    
                # Extract games from the table
                games = page.evaluate("""
                    () => {
                        const items = [];
                        const rows = document.querySelectorAll('tr[id^="row_"]');
                        rows.forEach(row => {
                            const link = row.querySelector('td.collection_objectname a');
                            if (!link) return;
                            const idMatch = link.href.match(/boardgame\\/(\\d+)/);
                            if (!idMatch) return;
                            items.push({
                                id: parseInt(idMatch[1], 10),
                                name: link.textContent.trim()
                            });
                        });
                        return items;
                    }
                """)
                
                if not games:
                    break
                    
                all_games.extend(games)
                
                # Check if there's a next page link (BGG uses '»' text or title containing 'next')
                has_next = page.evaluate("""
                    () => {
                        const links = Array.from(document.querySelectorAll('a'));
                        return links.some(l =>
                            l.title.toLowerCase().includes('next') ||
                            l.textContent.includes('\u00bb')
                        );
                    }
                """)
                
                if not has_next:
                    break
                    
                page_num += 1

            browser.close()
            print(f"  ✓ Found {len(all_games)} games in collection (across {page_num} pages)")
            return all_games
    except Exception as e:
        print(f"  ✗ Playwright scrape error: {e}")
        return None

def fetch_collection_xml(username):
    """Fetch collection via BGG XML API2 (works from datacenter IPs unlike the HTML pages)."""
    import xml.etree.ElementTree as ET
    print(f"Fetching collection for {username} via XML API...")
    url = f"https://boardgamegeek.com/xmlapi2/collection?username={urllib.parse.quote(username)}&own=1&subtype=boardgame&excludesubtype=boardgameexpansion&stats=0"
    
    max_retries = 8
    for attempt in range(max_retries):
        try:
            resp = opener.open(urllib.request.Request(url, headers={
                'User-Agent': BROWSER_UA,
                'Accept': 'application/xml',
            }), timeout=30)
            status = resp.getcode()
            if status == 200:
                data = resp.read().decode('utf-8')
                root = ET.fromstring(data)
                games = []
                for item in root.findall('.//item'):
                    obj_id = item.get('objectid')
                    name_el = item.find('name')
                    if obj_id and name_el is not None:
                        games.append({
                            'id': int(obj_id),
                            'name': name_el.text or ''
                        })
                print(f"  ✓ XML API returned {len(games)} games")
                return games
            elif status == 202:
                # BGG queues collection requests — retry after a delay
                print(f"  ⏳ XML API returned 202 (queued), retry {attempt+1}/{max_retries}...")
                time.sleep(3)
                continue
            else:
                print(f"  ✗ XML API returned status {status}")
                return None
        except urllib.error.HTTPError as e:
            if e.code == 202:
                print(f"  ⏳ XML API returned 202 (queued), retry {attempt+1}/{max_retries}...")
                time.sleep(3)
                continue
            print(f"  ✗ XML API HTTP error: {e.code}")
            return None
        except Exception as e:
            print(f"  ✗ XML API error: {e}")
            return None
    
    print(f"  ✗ XML API: gave up after {max_retries} retries (still 202)")
    return None

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/bggproxy/"):
            self._proxy_get()
        elif self.path.startswith("/api/collection"):
            self._handle_collection()
        elif self.path.startswith("/api/dims"):
            self._handle_dims()
        elif self.path == "/api/status":
            self._handle_status()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith("/bggproxy/"):
            self._proxy_post()
        elif self.path == "/api/bgg-login":
            self._handle_bgg_login()
        else:
            self.send_error(404)

    def _handle_collection(self):
        """Handle /api/collection?username=... requests"""
        parsed_url = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed_url.query)
        username = qs.get("username", [""])[0]
        if not username:
            self._json_response(400, {"error": "Missing username parameter"})
            return
        
        # Try XML API first (works from datacenter IPs)
        games = fetch_collection_xml(username)
        
        # Fallback to Playwright scraping if XML fails
        if games is None:
            print("  XML API failed, trying Playwright scraper...")
            games = scrape_bgg_collection(username)
            
        if games is not None:
            self._json_response(200, {"games": games, "count": len(games)})
        else:
            self._json_response(500, {
                "error": "Failed to fetch BGG collection via both XML API and scraping.",
                "workaround": "Use CSV import instead: BGG Collection → ⋯ → Export as CSV → Upload to app"
            })

    def _handle_dims(self):
        parsed_url = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed_url.query)
        raw_ids = qs.get("ids", [""])[0]
        force = qs.get("force", ["0"])[0] == "1"
        if not raw_ids:
            self._json_response(400, {"error": "Missing ?ids= parameter"})
            return
        try:
            game_ids = [int(x.strip()) for x in raw_ids.split(",") if x.strip()]
        except ValueError:
            self._json_response(400, {"error": "Invalid IDs"})
            return
        if len(game_ids) > 500:
            self._json_response(400, {"error": "Too many IDs (max 500)"})
            return
        results = fetch_dims_for_ids(game_ids, force)
        self._json_response(200, {"dims": results, "count": len(results), "requested": len(game_ids)})

    def _handle_status(self):
        self._json_response(200, {
            "logged_in": True,
            "cached_games": len([v for v in dims_cache.values() if v is not None]),
            "config_file": os.path.exists(CONFIG_FILE),
            "playwright_enabled": True
        })

    def _handle_bgg_login(self):
        self._json_response(200, {"ok": True, "message": "Login no longer required — using Playwright scraper"})

    def _json_response(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _proxy_get(self):
        target = self.path[len("/bggproxy/"):]
        url = f"{BGG_BASE}/{target}"
        try:
            resp = bgg_request(url)
            body = resp.read()
            self.send_response(resp.status)
            self.send_header("Content-Type", resp.headers.get("Content-Type", "text/xml"))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
        except urllib.error.HTTPError as e:
            body = e.read()
            print(f"  BGG {e.code} for {target}")
            self.send_response(e.code)
            self.send_header("Content-Type", e.headers.get("Content-Type", "text/plain"))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            print(f"  Proxy error for {target}: {e}")
            self.send_response(502)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(f"Proxy error: {e}".encode())

    def _proxy_post(self):
        target = self.path[len("/bggproxy/"):]
        url = f"{BGG_BASE}/{target}"
        content_len = int(self.headers.get("Content-Length", 0))
        post_body = self.rfile.read(content_len) if content_len > 0 else b""
        ct = self.headers.get("Content-Type", "application/json")
        try:
            resp = bgg_request(url, method="POST", data=post_body, content_type=ct)
            body = resp.read()
            self.send_response(resp.status)
            self.send_header("Content-Type", resp.headers.get("Content-Type", "application/json"))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
        except urllib.error.HTTPError as e:
            body = e.read()
            print(f"  POST error {e.code}")
            self.send_response(e.code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(body)
        except Exception as e:
            self.send_response(502)
            self.send_header("Content-Type", "text/plain")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(f"Proxy error: {e}".encode())

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        # Silence logs for better CLI visibility
        pass


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"Starting Kallax Calculator Server on port {PORT}...")
    print(f"Dimension cache: {len([v for v in dims_cache.values() if v is not None])} games")
    print(f"Playwright: Collection scraping enabled")

    server = http.server.HTTPServer(("", PORT), ProxyHandler)
    print(f"Server active at http://localhost:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
