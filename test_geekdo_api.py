#!/usr/bin/env python3
"""
Test api.geekdo.com endpoints directly without parsing main game pages.
"""

import requests
import json
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

base_url = "https://api.geekdo.com/api/geekitems"

print("Testing api.geekdo.com endpoints")
print("=" * 70)

# Test 1: Search for a game
print("\nTest 1: Search for Catan")
print("-" * 70)
try:
    resp = requests.get(
        base_url,
        params={
            'nosession': '1',
            'objecttype': 'thing',
            'subtype': 'boardgame',
            'search': 'Catan'
        },
        headers=headers,
        timeout=10
    )
    print(f"Status: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"Hits: {len(data.get('hits', []))}")
        
        if data.get('hits'):
            game = data['hits'][0]
            print(f"Name: {game['name']}")
            print(f"ID: {game['id']}")
            
            # Check if dimension data is in search results
            if 'length' in game:
                print(f"Dimensions directly in search: {game['length']} × {game['width']} × {game['depth']}")
            else:
                print("No dimensions in search result")
    else:
        print(f"Error: {resp.text[:200]}")
        
except Exception as e:
    print(f"Exception: {e}")

# Test 2: Try to access a game thing directly
print("\n\nTest 2: Get game 'thing' by ID (13 = Catan)")
print("-" * 70)
try:
    resp = requests.get(
        base_url,
        params={
            'objectid': '13',
            'objecttype': 'thing'
        },
        headers=headers,
        timeout=10
    )
    print(f"Status: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        print(f"Response: {json.dumps(data, indent=2)[:500]}")
    else:
        print(f"Error: {resp.text[:200]}")
        
except Exception as e:
    print(f"Exception: {e}")

# Test 3: Try accessing all versions for a game
print("\n\nTest 3: Get all versions for game 13")
print("-" * 70)
try:
    resp = requests.get(
        base_url,
        params={
            'objectid': '13',
            'objecttype': 'thing',
            'subtype': 'boardgameversion'
        },
        headers=headers,
        timeout=10
    )
    print(f"Status: {resp.status_code}")
    
    if resp.status_code == 200:
        data = resp.json()
        hits = data.get('hits', [])
        print(f"Found {len(hits)} versions")
        
        if hits:
            # Show first version
            v = hits[0]
            print(f"\nFirst version:")
            print(f"  Name: {v.get('name')}")
            print(f"  ID: {v.get('id')}")
            print(f"  Length: {v.get('length')}")
            print(f"  Width: {v.get('width')}")
            print(f"  Depth: {v.get('depth')}")
            print(f"  Weight: {v.get('weight')}")
    else:
        print(f"Error: {resp.text[:200]}")
        
except Exception as e:
    print(f"Exception: {e}")
