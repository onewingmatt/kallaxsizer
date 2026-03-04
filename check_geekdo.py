#!/usr/bin/env python3
import requests
import json

games = {
    "Tidal Blades Heroes of the Reef": 233262,
    "Forbidden Island": 65244,
    "Millions of Dollars": 193213,
}

print("Searching geekdo API by name...\n")

for name, bgg_id in games.items():
    print(f"\n{'='*70}")
    print(f"Searching: {name} (BGG ID: {bgg_id})")
    print('='*70)
    
    try:
        # Search by name
        url = f"https://api.geekdo.com/api/search?type=boardgame&query={name}"
        resp = requests.get(url, timeout=5)
        print(f"Search Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            if 'games' in data and len(data['games']) > 0:
                print(f"Found {len(data['games'])} results:\n")
                for i, game in enumerate(data['games'][:3]):
                    print(f"{i+1}. {game.get('name', 'N/A')} (ID: {game.get('id')})")
                    print(f"   Year: {game.get('yearPublished', 'N/A')}")
                    dims = []
                    if game.get('width'):
                        dims.append(f"W: {game.get('width')}")
                    if game.get('depth'):
                        dims.append(f"D: {game.get('depth')}")
                    if game.get('height'):
                        dims.append(f"H: {game.get('height')}")
                    if dims:
                        print(f"   Dims: {' | '.join(dims)}")
                    print()
            else:
                print(f"No results. Response: {json.dumps(data, indent=2)[:300]}")
    except Exception as e:
        print(f"Error: {e}")

print("\n" + "="*70)
print("Summary: If geekdo doesn't have dimensions, we need to:")
print("  1. Check your actual boxes for measurements")
print("  2. Look up standard retail versions on BGG directly")
print("  3. Manually enter corrected dimensions in the app")
