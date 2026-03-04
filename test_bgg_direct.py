#!/usr/bin/env python3
"""
Test direct BGG API access to diagnose 401 errors.
"""
import urllib.request
import urllib.error

BROWSER_UA = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"

def test_endpoint(url_path, description):
    """Test a BGG endpoint."""
    url = f"https://boardgamegeek.com{url_path}"
    print(f"\nTesting: {description}")
    print(f"URL: {url}")
    
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", BROWSER_UA)
        req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
        req.add_header("Referer", "https://boardgamegeek.com/")
        
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.status
            content_len = len(resp.read())
            print(f"✅ Status {status}, {content_len} bytes")
            return True
    except urllib.error.HTTPError as e:
        print(f"❌ Status {e.code}: {e.reason}")
        print(f"   Response: {e.read().decode('utf-8', errors='ignore')[:200]}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Test various endpoints
print("═" * 60)
print("BGG API Endpoint Tests")
print("═" * 60)

test_endpoint("/xmlapi2/thing?id=13", "xmlapi2/thing (single game)")
test_endpoint("/xmlapi2/thing?id=13&versions=1", "xmlapi2/thing with versions (single)")
test_endpoint("/xmlapi/thing?id=13", "xmlapi/thing (old API, single)")
test_endpoint("/xmlapi2/collection/unknown_user123456", "xmlapi2/collection (public)")

# Try the actual batch URL that's failing
test_endpoint(
    "/xmlapi2/thing?id=298619,250621,371947&versions=1",
    "xmlapi2/thing (batch of 3 as tested)"
)

print("\n" + "═" * 60)
