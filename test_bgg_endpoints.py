#!/usr/bin/env python3
"""
Test different BGG endpoints to find which ones provide dimension data.
"""

import requests
import json

# Test game: Catan (ID 13)
game_id = 13
game_name = "Catan"

print(f"Testing different BGG endpoints for {game_name} (ID: {game_id})\n")

# Test 1: Original XML API
print("=" * 60)
print("Test 1: /xmlapi2/thing (original - we know this is 401)")
print("=" * 60)
try:
    resp = requests.get(f"https://boardgamegeek.com/xmlapi2/thing?id={game_id}&type=boardgame", timeout=5)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        print("Response (first 500 chars):", resp.text[:500])
    else:
        print(f"Error: {resp.text[:200]}")
except Exception as e:
    print(f"Exception: {e}")

# Test 2: JSON API endpoint (if it exists)
print("\n" + "=" * 60)
print("Test 2: /api/boardgame/{id} (possible JSON endpoint)")
print("=" * 60)
try:
    resp = requests.get(f"https://boardgamegeek.com/api/boardgame/{game_id}", timeout=5)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        data = resp.json()
        print("Success! Response keys:", list(data.keys())[:10])
        if 'stats' in data:
            print("Has stats:", list(data['stats'].keys()))
        print("Full response (first 1000 chars):", json.dumps(data, indent=2)[:1000])
    else:
        print(f"Error: {resp.status_code}")
except Exception as e:
    print(f"Exception: {e}")

# Test 3: GraphQL endpoint (modern sites often use this)
print("\n" + "=" * 60)
print("Test 3: GraphQL endpoint (if available)")
print("=" * 60)
try:
    query = """
    query {
      game(id: %d) {
        id
        name
        width
        height
        depth
      }
    }
    """ % game_id
    
    resp = requests.post(
        "https://boardgamegeek.com/graphql",
        json={"query": query},
        timeout=5
    )
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        print("Response:", resp.text[:500])
    else:
        print(f"Error: {resp.status_code}")
except Exception as e:
    print(f"Exception: {e}")

# Test 4: Direct game page with Accept headers
print("\n" + "=" * 60)
print("Test 4: Game page with JSON Accept header")
print("=" * 60)
try:
    resp = requests.get(
        f"https://boardgamegeek.com/boardgame/{game_id}",
        headers={"Accept": "application/json"},
        timeout=5
    )
    print(f"Status: {resp.status_code}")
    print(f"Content-Type: {resp.headers.get('content-type')}")
    if 'json' in resp.headers.get('content-type', ''):
        print("Success! Got JSON response")
        data = resp.json()
        print("Keys:", list(data.keys())[:10])
    else:
        print("Got HTML response (expected)")
except Exception as e:
    print(f"Exception: {e}")

# Test 5: Search API
print("\n" + "=" * 60)
print("Test 5: Search/Browse API")
print("=" * 60)
try:
    resp = requests.get(
        f"https://boardgamegeek.com/api/search",
        params={"q": game_name},
        timeout=5
    )
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        print("Response (first 500 chars):", resp.text[:500])
except Exception as e:
    print(f"Exception: {e}")

print("\n" + "=" * 60)
print("Analysis: If any endpoint returns dimension data, we found our solution!")
print("=" * 60)
