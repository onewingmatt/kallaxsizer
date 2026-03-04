#!/usr/bin/env python3
"""
Try to fetch dimension data from BGG's Versions section.
Dimensions are usually listed in game versions/editions details.
"""

import requests
from bs4 import BeautifulSoup
import re

# Headers that look like a browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

# Test game: Catan (ID 13)
game_id = 13
game_name = "Catan"

print(f"Fetching dimension data from BGG Versions section")
print(f"Game: {game_name} (ID: {game_id})")
print("=" * 70)

# Try different version page URLs
urls = [
    f"https://boardgamegeek.com/boardgame/{game_id}/versions",
    f"https://boardgamegeek.com/boardgame/{game_id}/versions/",
    f"https://boardgamegeek.com/boardgame/{game_id}#versions",
]

for url in urls:
    print(f"\nTrying: {url}")
    print("-" * 70)
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        print(f"Status: {resp.status_code}")
        
        if resp.status_code == 200:
            # Parse HTML
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # Look for dimension patterns
            text = soup.get_text()
            
            # Search for cm dimensions
            pattern = r'(\d+(?:\.\d+)?)\s*×\s*(\d+(?:\.\d+)?)\s*×\s*(\d+(?:\.\d+)?)\s*cm'
            matches = re.findall(pattern, text, re.IGNORECASE)
            
            if matches:
                print(f"✓ Found {len(matches)} dimension matches!")
                for i, match in enumerate(matches[:5], 1):
                    print(f"  {i}. {match[0]} × {match[1]} × {match[2]} cm")
            else:
                print("✗ No dimensions found in page text")
            
            # Look for common dimension-related text
            sections = []
            for section in soup.find_all(['div', 'table', 'tr']):
                section_text = section.get_text().strip()
                if 'dimension' in section_text.lower() or 'size' in section_text.lower():
                    sections.append(section_text)
            
            if sections:
                print(f"\nFound {len(sections)} sections mentioning dimensions:")
                for i, section in enumerate(sections[:3], 1):
                    print(f"  {i}. {section[:100]}...")
        
        elif resp.status_code == 403:
            print("✗ Blocked by Cloudflare (403)")
        elif resp.status_code == 404:
            print("✗ Page not found (404)")
        else:
            print(f"✗ Error: {resp.status_code}")
            
    except Exception as e:
        print(f"✗ Exception: {e}")

print("\n" + "=" * 70)
print("\nTrying alternate approach: Raw /xmlapi2/boardgame endpoint")
print(f"URL: https://boardgamegeek.com/xmlapi2/boardgame/{game_id}")

try:
    resp = requests.get(
        f"https://boardgamegeek.com/xmlapi2/boardgame/{game_id}",
        headers=headers,
        timeout=10
    )
    print(f"Status: {resp.status_code}")
    
    if resp.status_code == 200:
        # Try to find dimensions in XML
        if 'dimension' in resp.text.lower():
            print("✓ Found 'dimension' in response!")
            # Print relevant XML sections
            lines = resp.text.split('\n')
            for i, line in enumerate(lines):
                if 'dimension' in line.lower():
                    start = max(0, i-2)
                    end = min(len(lines), i+3)
                    print("\n".join(lines[start:end]))
        else:
            print("✗ No dimensions in XML response")
            print(f"Response (first 500 chars): {resp.text[:500]}")
    else:
        print(f"✗ Status {resp.status_code}")
        
except Exception as e:
    print(f"✗ Exception: {e}")
