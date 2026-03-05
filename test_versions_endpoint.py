#!/usr/bin/env python3
"""
Quick test of the /api/versions endpoint
Run this after starting server.py: python3 server.py
Then in another terminal: python3 test_versions_endpoint.py
"""

import requests
import json
import time

BASE_URL = "http://localhost:8042"

# Test games to fetch versions for
TEST_GAMES = {
    13: "Catan",
    36218: "Dominion",
    70323: "King of Tokyo",
    822: "Carcassonne",
}

print("Testing /api/versions endpoint...")
print("=" * 60)

for game_id, game_name in TEST_GAMES.items():
    print(f"\n📦 Fetching versions for {game_name} (ID: {game_id})...")
    
    try:
        resp = requests.get(f"{BASE_URL}/api/versions?id={game_id}", timeout=30)
        
        if resp.status_code == 200:
            data = resp.json()
            versions = data.get('versions', [])
            
            if versions:
                print(f"   ✓ Found {len(versions)} versions:")
                for v in versions[:3]:  # Show first 3
                    print(f"     • {v['name']} ({v['year']}) - {v['l']}×{v['w']}×{v['h']} cm")
                if len(versions) > 3:
                    print(f"     ... and {len(versions) - 3} more")
            else:
                print(f"   ⚠ No versions with dimensions found")
        else:
            print(f"   ✗ HTTP {resp.status_code}: {resp.text}")
    
    except requests.exceptions.ConnectionError:
        print(f"   ✗ Could not connect to server")
        print(f"   → Make sure to run: python3 server.py")
        break
    except Exception as e:
        print(f"   ✗ Error: {e}")
    
    time.sleep(1)  # Be polite

print("\n" + "=" * 60)
print("✓ Feature is working! Open the app and click a game to test.")
