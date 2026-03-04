#!/usr/bin/env python3
"""
Try different parameter combinations for api.geekdo.com to get version dimensions.
"""

import requests
import json

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

base_url = "https://api.geekdo.com/api/geekitems"

test_params = [
    # Original attempt
    {
        'name': 'objectid=13, objecttype=thing, subtype=boardgameversion',
        'params': {'objectid': '13', 'objecttype': 'thing', 'subtype': 'boardgameversion'}
    },
    # Try with includes
    {
        'name': 'objectid=13, objecttype=thing, includes=stats,links',
        'params': {'objectid': '13', 'objecttype': 'thing', 'includes': 'stats,links'}
    },
    # Try geekitemlinks  
    {
        'name': 'objectid=13, objecttype=thing, linktype=boardgameversion',
        'params': {'objectid': '13', 'objecttype': 'thing', 'linktype': 'boardgameversion'}
    },
    # Try verison directly with thing type
    {
        'name': 'objecttype=version, parentobjectid=13',
        'params': {'objecttype': 'version', 'parentobjectid': '13'}
    },
    # Try with parent thing
    {
        'name': 'objectid=13, parentobjecttype=thing',
        'params': {'objectid': '13', 'parentobjecttype': 'thing', 'objecttype': 'version'}
    },
]

print("Testing different api.geekdo.com parameter combinations")
print("=" * 70)

for test in test_params:
    print(f"\nTest: {test['name']}")
    print("-" * 70)
    try:
        resp = requests.get(
            base_url,
            params=test['params'],
            headers=headers,
            timeout=10
        )
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            
            # Check for hits
            if 'hits' in data:
                print(f"Hits: {len(data.get('hits', []))}")
                if data.get('hits'):
                    hit = data['hits'][0]
                    print(f"First result keys: {list(hit.keys())[:15]}")
                    if 'dimensions' in hit:
                        print(f"Has dimensions: {hit['dimensions']}")
                    if 'length' in hit:
                        print(f"Has length: {hit['length']}")
            
            # Check for item
            if 'item' in data:
                item = data['item']
                print(f"Item type: {item.get('objecttype')}")
                print(f"Item keys: {list(item.keys())[:15]}")
                if 'versions' in item:
                    print(f"Has versions: {len(item['versions'])}")
                    if item['versions']:
                        print(f"  First version keys: {list(item['versions'][0].keys())}")
        else:
            print(f"Error: {resp.text[:200]}")
            
    except Exception as e:
        print(f"Exception: {e}")
