#!/usr/bin/env python3
"""
Fetch box dimensions for missing games from BoardGameGeek game pages.
Since the API is blocked, we'll parse the HTML pages instead.
"""

import urllib.request
import urllib.error
import csv
import re
import time
from html.parser import HTMLParser

BROWSER_UA = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"

class DimensionExtractor(HTMLParser):
    """Extract dimensions from BGG HTML."""
    def __init__(self):
        super().__init__()
        self.in_specs = False
        self.dimensions = None
        self.current_text = ""
        
    def handle_starttag(self, tag, attrs):
        if tag == 'dd':
            self.in_specs = True
            
    def handle_endtag(self, tag):
        if tag == 'dd':
            self.in_specs = False
            
    def handle_data(self, data):
        if self.in_specs:
            self.current_text += data
            # Look for dimension patterns like "10" × 8.5" × 3.5""
            match = re.search(r'([\d.]+)"\s*×\s*([\d.]+)"\s*×\s*([\d.]+)"', data)
            if match:
                # Convert inches to cm
                w, l, h = float(match.group(1)), float(match.group(2)), float(match.group(3))
                self.dimensions = (round(w * 2.54, 1), round(l * 2.54, 1), round(h * 2.54, 1))

def fetch_bgg_dimensions(game_id):
    """Fetch dimensions from BGG game page."""
    url = f"https://boardgamegeek.com/boardgame/{game_id}"
    
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", BROWSER_UA)
        
        with urllib.request.urlopen(req, timeout=5) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
            # Look for dimension patterns in the HTML
            # BGG typically shows: 10" × 8.5" × 3.5"
            match = re.search(r'([\d.]+)"\s*×\s*([\d.]+)"\s*×\s*([\d.]+)"', html)
            if match:
                w, l, h = float(match.group(1)), float(match.group(2)), float(match.group(3))
                # Return in cm (inches * 2.54)
                return [round(w * 2.54, 1), round(l * 2.54, 1), round(h * 2.54, 1)]
            
            return None
            
    except urllib.error.HTTPError as e:
        print(f"  ❌ HTTP {e.code}")
        return None
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return None

# Read the CSV file
missing_games = {}
with open('/home/onewing/bgsize/missing_games.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        game_id = int(row['Game ID'])
        game_name = row['Game Name']
        missing_games[game_id] = game_name

print(f"📥 Loaded {len(missing_games)} missing games from CSV")
print("\n🔍 Attempting to fetch dimensions from BGG...")
print("=" * 70)

found_dims = {}
failed = []
rate_limited = 0

for idx, (game_id, game_name) in enumerate(missing_games.items(), 1):
    print(f"[{idx:3d}/{len(missing_games)}] ID {game_id:6d}: {game_name[:40]:40s}", end=" ", flush=True)
    
    dims = fetch_bgg_dimensions(game_id)
    
    if dims:
        found_dims[game_id] = dims
        print(f"✓ {dims[0]:5.1f} × {dims[1]:5.1f} × {dims[2]:5.1f} cm")
    else:
        failed.append((game_id, game_name))
        print(f"✗ (no data)")
    
    # Rate limit to avoid BGG blocking us
    if idx % 10 == 0:
        time.sleep(1)

print("=" * 70)
print(f"\n📊 Results:")
print(f"  ✓ Found dimensions: {len(found_dims)}")
print(f"  ✗ No data found: {len(failed)}")

if found_dims:
    print(f"\n💾 Creating dimension list for code...")
    print("\nAdd this to KNOWN_GAME_DIMS object in index.html:\n")
    print("      // Auto-fetched from BGG (Feb 2026)")
    for game_id in sorted(found_dims.keys()):
        dims = found_dims[game_id]
        game_name = missing_games[game_id]
        print(f"      {game_id}: [{dims[0]}, {dims[1]}, {dims[2]}],       // {game_name}")

if failed:
    print(f"\n⚠️  {len(failed)} games could not be fetched (may need manual lookup):")
    for game_id, game_name in failed[:20]:  # Show first 20
        print(f"  {game_id}: {game_name}")
    if len(failed) > 20:
        print(f"  ... and {len(failed) - 20} more")
