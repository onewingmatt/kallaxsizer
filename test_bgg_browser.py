#!/usr/bin/env python3
"""
Try to access BGG with proper browser headers and cookies.
"""

import requests
from urllib.parse import urlencode

# Headers that look like a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://boardgamegeek.com/',
}

game_id = 13
game_name = "Catan"

print(f"Testing BGG with browser-like headers for {game_name} (ID: {game_id})\n")

# Test 1: Game page with proper headers
print("=" * 60)
print("Test 1: Getting game page HTML with browser headers")
print("=" * 60)
try:
    session = requests.Session()
    resp = session.get(
        f"https://boardgamegeek.com/boardgame/{game_id}/{game_name.replace(' ', '-')}",
        headers=headers,
        timeout=10,
        allow_redirects=True
    )
    print(f"Status: {resp.status_code}")
    
    if resp.status_code == 200:
        # Check if dimensions are in the HTML
        html = resp.text
        
        # Look for common dimension patterns
        if 'dimension' in html.lower() or 'cm' in html.lower():
            print("✓ Found dimension-related content in HTML")
            
            # Try to find the actual values
            import re
            
            # Pattern 1: Look for numeric dimensions
            dim_patterns = [
                r'(\d+\.?\d*)\s*×\s*(\d+\.?\d*)\s*×\s*(\d+\.?\d*)\s*cm',
                r'width["\']?\s*[:=]\s*["\']?(\d+\.?\d*)',
                r'height["\']?\s*[:=]\s*["\']?(\d+\.?\d*)',
                r'depth["\']?\s*[:=]\s*["\']?(\d+\.?\d*)',
            ]
            
            for pattern in dim_patterns:
                matches = re.findall(pattern, html, re.IGNORECASE)
                if matches:
                    print(f"Found matches for pattern '{pattern}':")
                    print(f"  {matches[:5]}")  # Show first 5 matches
            
            # Look for the data structure (usually in <script> tags)
            script_blocks = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
            print(f"\nFound {len(script_blocks)} script blocks")
            
            # Search for JSON data in scripts
            for i, script in enumerate(script_blocks[:5]):  # Check first 5 scripts
                if 'width' in script.lower() or 'dimension' in script.lower():
                    print(f"\nScript block {i} contains dimension-related content:")
                    # Print first 300 chars
                    print(script[:300])
                    print("...")
        else:
            print("✗ No dimension-related content found in HTML")
            print(f"Page length: {len(html)} characters")
    else:
        print(f"Failed: Status {resp.status_code}")
        print(f"Response: {resp.text[:200]}")
        
except Exception as e:
    print(f"Exception: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Try JSON API with headers
print("\n" + "=" * 60)
print("Test 2: /api/boardgame endpoint with proper headers")
print("=" * 60)
try:
    resp = requests.get(
        f"https://boardgamegeek.com/api/boardgame/{game_id}",
        headers=headers,
        timeout=10
    )
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        print("Success!")
        print(resp.json())
except Exception as e:
    print(f"Error: {e}")

# Test 3: Check /xml/boardgame (not xmlapi2)
print("\n" + "=" * 60)
print("Test 3: /xml/boardgame endpoint (old XML API)")
print("=" * 60)
try:
    resp = requests.get(
        f"https://boardgamegeek.com/xml/boardgame/{game_id}",
        headers=headers,
        timeout=10
    )
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        print("Success! Got XML response")
        print(resp.text[:500])
except Exception as e:
    print(f"Error: {e}")
