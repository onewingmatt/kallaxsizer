#!/usr/bin/env python3
"""
Scrape board game box dimensions from BGG using api.geekdo.com internal API.
Based on geekdo API documentation - no authentication required.
"""

import requests
import json
import re
import csv
import time
from urllib.parse import quote

class BGGDimensionScraper:
    def __init__(self, delay=0.5):
        """Initialize scraper with rate limit delay."""
        self.base_url = "https://api.geekdo.com/api/geekitems"
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_game(self, game_name):
        """Search for a game by name to get BGG ID."""
        print(f"Searching for: {game_name}")
        
        try:
            resp = self.session.get(
                self.base_url,
                params={
                    'nosession': '1',
                    'objecttype': 'thing',
                    'subtype': 'boardgame',
                    'search': game_name,
                    'gallery': 'off'
                },
                timeout=10
            )
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get('hits') and len(data['hits']) > 0:
                    result = data['hits'][0]
                    game_id = result['id']
                    name = result['name']
                    print(f"  ✓ Found: {name} (ID: {game_id})")
                    return game_id
            
            print(f"  ✗ No results found")
            return None
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return None
    
    def get_game_versions(self, game_id):
        """Fetch version IDs for a game from its main page."""
        print(f"Fetching versions for game ID {game_id}...")
        
        try:
            resp = requests.get(
                f"https://boardgamegeek.com/boardgame/{game_id}",
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                timeout=10
            )
            
            if resp.status_code == 200:
                # Look for GEEK.geekitemPreload in the page
                match = re.search(r'GEEK\.geekitemPreload\s*=\s*({.*?});', resp.text, re.DOTALL)
                if match:
                    try:
                        data = json.loads(match.group(1))
                        versions = data.get('links', {}).get('boardgameversion', [])
                        if versions:
                            print(f"  ✓ Found {len(versions)} versions")
                            return versions
                    except json.JSONDecodeError:
                        pass
            
            print(f"  ✗ Could not extract version data")
            return []
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
            return []
    
    def get_version_dimensions(self, version_id):
        """Fetch dimensions for a specific version."""
        try:
            resp = self.session.get(
                self.base_url,
                params={
                    'objectid': version_id,
                    'objecttype': 'version',
                    'subtype': 'boardgameversion'
                },
                timeout=10
            )
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get('hits') and len(data['hits']) > 0:
                    item = data['hits'][0]
                    
                    # Convert inches to cm (inches * 2.54)
                    length = float(item.get('length', 0))
                    width = float(item.get('width', 0))
                    depth = float(item.get('depth', 0))
                    
                    if length > 0 and width > 0 and depth > 0:
                        return {
                            'length_cm': round(length * 2.54, 2),
                            'width_cm': round(width * 2.54, 2),
                            'depth_cm': round(depth * 2.54, 2),
                            'length_in': length,
                            'width_in': width,
                            'depth_in': depth,
                            'weight_lbs': float(item.get('weight', 0))
                        }
            
            return None
            
        except Exception as e:
            print(f"    Error fetching version {version_id}: {e}")
            return None
    
    def get_game_dimensions(self, game_id, game_name=None):
        """Get dimensions for a game by ID (uses most common version)."""
        print(f"\nFetching {game_name or f'Game {game_id}'}...")
        
        # Get versions
        versions = self.get_game_versions(game_id)
        if not versions:
            return None
        
        # Try each version until we find one with dimensions
        for version in versions:
            version_id = version.get('id')
            version_name = version.get('name', 'Unknown')
            
            time.sleep(self.delay)  # Rate limiting
            dims = self.get_version_dimensions(version_id)
            
            if dims:
                print(f"  ✓ {version_name}: {dims['length_cm']}×{dims['width_cm']}×{dims['depth_cm']} cm")
                return {
                    'game_id': game_id,
                    'game_name': game_name or 'Unknown',
                    'version_name': version_name,
                    'version_id': version_id,
                    **dims
                }
        
        print(f"  ✗ No version with dimensions found")
        return None

def test_scraper():
    """Test with a few known games."""
    scraper = BGGDimensionScraper(delay=0.5)
    
    test_games = [
        (13, "Catan"),
        (822, "Carcassonne"),
        (174430, "Gloomhaven"),
    ]
    
    print("=" * 70)
    print("Testing BGG Dimension Scraper (api.geekdo.com)")
    print("=" * 70)
    
    results = []
    for game_id, game_name in test_games:
        result = scraper.get_game_dimensions(game_id, game_name)
        if result:
            results.append(result)
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    successful = [r for r in results if r is not None]
    print(f"Successfully scraped: {len(successful)}/{len(test_games)}")
    
    if successful:
        print("\nDimensions (cm):")
        for r in successful:
            print(f"  {r['game_name']}: {r['length_cm']} × {r['width_cm']} × {r['depth_cm']}")
    
    return results

if __name__ == "__main__":
    results = test_scraper()
