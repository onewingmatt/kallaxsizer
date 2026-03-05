#!/usr/bin/env python3
"""
Local proxy server for the Kallax Collection Calculator.
Serves index.html and proxies BGG API requests to bypass CORS.

Optional: to enable automatic dimension fetching, create bgg_config.json:
  {"username": "your_bgg_username", "password": "your_bgg_password"}

Usage: python3 server.py
Then open http://localhost:8042
"""

import http.server
import http.cookiejar
import urllib.request
import urllib.parse
import urllib.error
import json
import os
import time
import xml.etree.ElementTree as ET
import requests as req_lib
from playwright.sync_api import sync_playwright

PORT = 8042
BGG_BASE = "https://boardgamegeek.com"
GEEKDO_BASE = "https://api.geekdo.com"
CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bgg_config.json")
DIMS_CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dims_cache.json")
COMMUNITY_DIMS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "community_dims.json")

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

def load_community_dims():
    if os.path.exists(COMMUNITY_DIMS_FILE):
        with open(COMMUNITY_DIMS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_community_dims(store):
    with open(COMMUNITY_DIMS_FILE, "w") as f:
        json.dump(store, f, indent=2)

def submit_community_dims(game_id, l, w, h):
    """Record a user-submitted dimension. Finds matching entry (within 0.5cm) and
    increments its vote, or adds a new entry with 1 vote. Returns the winning entry."""
    store = load_community_dims()
    key = str(game_id)
    entries = store.get(key, [])
    l, w, h = round(l, 1), round(w, 1), round(h, 1)
    for entry in entries:
        if abs(entry['l'] - l) <= 0.5 and abs(entry['w'] - w) <= 0.5 and abs(entry['h'] - h) <= 0.5:
            entry['votes'] += 1
            print(f"[community] game {key}: vote for {l}x{w}x{h} now {entry['votes']}")
            break
    else:
        entries.append({'l': l, 'w': w, 'h': h, 'votes': 1})
        print(f"[community] game {key}: new submission {l}x{w}x{h}")
    store[key] = entries
    save_community_dims(store)
    best = max(entries, key=lambda e: e['votes'])
    return best

community_dims = load_community_dims()

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

bgg_access_token = None  # kept for backwards compat (not used for dims anymore)

def fetch_dims_for_ids(game_ids):
    """
    Fetch physical dimensions for BGG game IDs using api.geekdo.com.
    Two-step process (no authentication required):
      1. GET /api/geekitems?objectid={game_id}&objecttype=thing  → version list
      2. GET /api/geekitems?objectid={version_id}&objecttype=version → dimensions
    """
    results = {}
    uncached = [gid for gid in game_ids if str(gid) not in dims_cache]

    # Return from cache for already-fetched games
    for gid in game_ids:
        key = str(gid)
        if key in dims_cache and dims_cache[key] is not None:
            results[key] = dims_cache[key]

    if not uncached:
        return results

    print(f"  Fetching dims for {len(uncached)} games via api.geekdo.com...")
    fetched = 0

    for gid in uncached:
        key = str(gid)
        try:
            # Step 1: get version IDs from the game's item record
            r1 = geekdo_session.get(
                f"{GEEKDO_BASE}/api/geekitems",
                params={'objectid': str(gid), 'objecttype': 'thing', 'nosession': '1'},
                timeout=10
            )
            if r1.status_code != 200:
                print(f"  [{gid}] geekitems status {r1.status_code}")
                dims_cache[key] = None
                continue

            versions = r1.json().get('item', {}).get('links', {}).get('boardgameversion', [])
            if not versions:
                dims_cache[key] = None
                continue

            # Step 2: try each version until we find one with dimensions
            found = False
            for ver in versions:
                vid = ver.get('objectid')
                if not vid:
                    continue
                time.sleep(0.2)  # polite rate limiting
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
                    dims_cache[key] = {'l': round(dims[0], 1), 'w': round(dims[1], 1), 'h': round(dims[2], 1)}
                    results[key] = dims_cache[key]
                    fetched += 1
                    found = True
                    break

            if not found:
                dims_cache[key] = None

        except Exception as e:
            print(f"  [{gid}] error: {e}")
            dims_cache[key] = None

    print(f"  Done: {fetched}/{len(uncached)} games got dimensions")
    save_dims_cache(dims_cache)
    return results

def scrape_bgg_collection(username):
    """Use Playwright to scrape the collection page for games (bypasses XML API blockage)."""
    print(f"Scraping collection for {username} via Playwright...")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                ]
            )
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            )
            page = context.new_page()
            
            all_games = []
            page_num = 1
            
            while True:
                url = f"https://boardgamegeek.com/collection/user/{urllib.parse.quote(username)}?own=1&subtype=boardgame&excludesubtype=boardgameexpansion&page={page_num}"
                print(f"  Loading page {page_num}: {url}")
                
                try:
                    page.goto(url, wait_until="load", timeout=60000)
                    page.wait_for_selector('tr[id^="row_"]', timeout=20000)
                    page.wait_for_timeout(2000)
                except Exception as e:
                    print(f"  [Page {page_num}] Warning/Error waiting for rows: {e}")
                    if all_games: break
                    else: return None

                # Extract games from the table
                games = page.evaluate("""
                    () => {
                        const items = [];
                        const rows = Array.from(document.querySelectorAll('tr[id^="row_"]'));
                        rows.forEach(row => {
                            const link = row.querySelector('a.primary') || row.querySelector('td.collection_objectname a');
                            if (!link) return;
                            const href = link.href || "";
                            const idMatch = href.match(/boardgame\\/(\\d+)/);
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
                print(f"  [Page {page_num}] Extracted {len(games)} games")
                
                # Check for next page
                has_next = page.evaluate("""
                    () => {
                        const nextLink = document.querySelector('a[title="next page"]') || 
                                       Array.from(document.querySelectorAll('a')).find(l => l.textContent.includes('\\u00bb'));
                        return !!nextLink;
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

def fetch_game_versions(game_id):
    """
    Fetch all versions (editions) for a single game with their dimensions.
    Returns a list of versions with name, year, and dimensions.
    """
    versions = []
    try:
        # Step 1: Get all version IDs for this game
        r1 = geekdo_session.get(
            f"{GEEKDO_BASE}/api/geekitems",
            params={'objectid': str(game_id), 'objecttype': 'thing', 'nosession': '1'},
            timeout=10
        )
        if r1.status_code != 200:
            print(f"  [Game {game_id}] geekitems status {r1.status_code}")
            return versions

        item = r1.json().get('item', {})
        version_list = item.get('links', {}).get('boardgameversion', [])
        if not version_list:
            print(f"  [Game {game_id}] no versions found")
            return versions

        print(f"  [Game {game_id}] found {len(version_list)} versions, fetching dimensions...")

        # Step 2: Fetch each version's dimensions
        for idx, ver_link in enumerate(version_list[:10]):  # Limit to 10 versions
            vid = ver_link.get('objectid')
            if not vid:
                continue
            
            try:
                time.sleep(0.15)  # polite rate limiting
                r2 = geekdo_session.get(
                    f"{GEEKDO_BASE}/api/geekitems",
                    params={'objectid': vid, 'objecttype': 'version', 'subtype': 'boardgameversion'},
                    timeout=10
                )
                if r2.status_code != 200:
                    continue
                
                item_data = r2.json().get('item', {})
                l = float(item_data.get('length', 0) or 0)
                w = float(item_data.get('width', 0) or 0)
                d = float(item_data.get('depth', 0) or 0)
                
                # Only include if we have valid dimensions
                if l > 0 and w > 0 and d > 0:
                    dims = sorted([l * 2.54, w * 2.54, d * 2.54], reverse=True)
                    
                    # Get version name and year
                    name = item_data.get('name', f'Version {idx + 1}')
                    year = item_data.get('yearpublished')
                    publisher = item_data.get('publisher', {}).get(0, {}).get('name', '')
                    
                    versions.append({
                        'id': vid,
                        'name': f"{name}" if not publisher else f"{name} ({publisher})",
                        'year': year,
                        'l': round(dims[0], 1),
                        'w': round(dims[1], 1),
                        'h': round(dims[2], 1)
                    })
            except Exception as e:
                print(f"    [Version {vid}] error: {e}")
                continue

    except Exception as e:
        print(f"  [Game {game_id}] error: {e}")

    print(f"  [Game {game_id}] returned {len(versions)} versions with dimensions")
    return versions

class ProxyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/bggproxy/"):
            self._proxy_get()
        elif self.path.startswith("/api/collection"):
            self._handle_collection()
        elif self.path.startswith("/api/dims"):
            self._handle_dims()
        elif self.path.startswith("/api/versions"):
            self._handle_versions()
        elif self.path.startswith("/api/community-dims"):
            self._handle_community_dims_get()
        elif self.path == "/api/status":
            self._handle_status()
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith("/bggproxy/"):
            self._proxy_post()
        elif self.path == "/api/bgg-login":
            self._handle_bgg_login()
        elif self.path == "/api/community-dims":
            self._handle_community_dims_post()
        else:
            self.send_error(404)

    def _handle_collection(self):
        """Handle /api/collection?username=... requests"""
        parsed_url = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed_url.query)
        username = qs.get("username", [""])[0]
        
        if not username:
            self._json_response(400, {"error": "Missing ?username= parameter"})
            return
        
        try:
            games = scrape_bgg_collection(username)
            if games is not None:
                self._json_response(200, {"username": username, "games": games, "count": len(games)})
            else:
                self._json_response(500, {
                    "error": "Failed to scrape BGG collection. Please use CSV import instead.",
                    "username": username,
                    "workaround": "1. Go to your BGG collection\n2. Click ⋯ menu → 'Download board games as CSV'\n3. Upload the CSV file using the 📁 button"
                })
        except Exception as e:
            print(f"Error scraping collection for {username}: {e}")
            self._json_response(500, {
                "error": f"Collection scraping failed: {str(e)}",
                "username": username,
                "workaround": "Use CSV import instead"
            })

    def _handle_dims(self):
        parsed_url = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed_url.query)
        raw_ids = qs.get("ids", [""])[0]
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
        results = fetch_dims_for_ids(game_ids)
        self._json_response(200, {"dims": results, "count": len(results), "requested": len(game_ids)})

    def _handle_versions(self):
        """Fetch all available versions (editions) for a single game ID with their dimensions"""
        parsed_url = urllib.parse.urlparse(self.path)
        qs = urllib.parse.parse_qs(parsed_url.query)
        game_id = qs.get("id", [""])[0]
        if not game_id:
            self._json_response(400, {"error": "Missing ?id= parameter"})
            return
        try:
            game_id = int(game_id)
        except ValueError:
            self._json_response(400, {"error": "Invalid game ID"})
            return
        
        versions = fetch_game_versions(game_id)
        self._json_response(200, {"id": game_id, "versions": versions})

    def _handle_community_dims_get(self):
        """Return the highest-voted dims for every game that has community submissions."""
        store = load_community_dims()
        best = {}
        for gid, entries in store.items():
            if entries:
                winner = max(entries, key=lambda e: e['votes'])
                best[gid] = winner
        self._json_response(200, {"dims": best, "count": len(best)})

    def _handle_community_dims_post(self):
        """Accept a new dimension submission from the frontend."""
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len) if content_len > 0 else b"{}"
        try:
            data = json.loads(body)
            gid = int(data["id"])
            l = float(data["l"])
            w = float(data["w"])
            h = float(data["h"])
        except (KeyError, ValueError, TypeError) as e:
            self._json_response(400, {"error": f"Invalid body: {e}"})
            return
        best = submit_community_dims(gid, l, w, h)
        self._json_response(200, {"ok": True, "best": best})

    def _handle_status(self):
        self._json_response(200, {
            "logged_in": True,  # no login needed; geekdo API is public
            "cached_games": len([v for v in dims_cache.values() if v is not None]),
            "config_file": os.path.exists(CONFIG_FILE),
        })

    def _handle_bgg_login(self):
        # Login no longer required — api.geekdo.com works without auth
        self._json_response(200, {"ok": True, "message": "No login required — dimensions fetched from api.geekdo.com"})

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
            print(f"  POST {target}: {resp.status}, cookies: {len(cookie_jar)}")
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
        print(f"[{self.log_date_time_string()}] {format % args}")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("Getting BGG session cookies...")
    try:
        bgg_request(BGG_BASE)
        print(f"Got {len(cookie_jar)} cookies from BGG")
    except Exception as e:
        print(f"Could not pre-warm cookies: {e}")

    print(f"Dimension source: api.geekdo.com (no login required)")
    print(f"Cached dims: {len([v for v in dims_cache.values() if v is not None])} games")

    server = http.server.HTTPServer(("", PORT), ProxyHandler)
    print(f"Kallax Calculator running at http://localhost:{PORT}")
    print(f"Open http://localhost:{PORT}/index.html")
    print(f"Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.server_close()
