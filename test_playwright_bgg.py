#!/usr/bin/env python3
"""
Use Playwright to scrape BGG game dimensions with better error handling.
"""

import asyncio
from playwright.async_api import async_playwright
import re

async def get_game_dimensions(game_id, game_name, timeout_ms=20000):
    """Scrape dimensions for a single game using Playwright."""
    
    async with async_playwright() as p:
        # Launch with stealth measures
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            # Simulate a real browser
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1280, 'height': 720}
        )
        page = await context.new_page()
        
        # Navigate to the game page
        url = f"https://boardgamegeek.com/boardgame/{game_id}"
        print(f"Fetching: {game_name} ({game_id})...", end=" ", flush=True)
        
        try:
            # Try with load state instead of networkidle
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
            except:
                # If that fails, try with just load
                await page.goto(url, wait_until="load", timeout=timeout_ms)
            
            # Wait a bit for JS rendering
            await page.wait_for_timeout(1500)
            
            # Get page title to confirm we loaded
            title = await page.title()
            print(f"[Loaded: {title[:40]}...]")
            
            # Extract all text content
            all_text = await page.content()
            
            # Search for cm dimensions in multiple formats
            patterns = [
                r'(\d+(?:\.\d+)?)\s*×\s*(\d+(?:\.\d+)?)\s*×\s*(\d+(?:\.\d+)?)\s*cm',
                r'(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)\s*cm',
            ]
            
            for pattern in patterns:
                matches = re.findall(pattern, all_text, re.IGNORECASE)
                if matches:
                    # Take the first match
                    length, width, height = matches[0]
                    result = {
                        'game_id': game_id,
                        'game_name': game_name,
                        'length': float(length),
                        'width': float(width),
                        'height': float(height),
                        'status': 'success'
                    }
                    print(f"  ✓ {length} × {width} × {height} cm")
                    await browser.close()
                    return result
            
            # If we got here, no dimensions found
            print(f"  ✗ No dimensions found")
            await browser.close()
            return {
                'game_id': game_id,
                'game_name': game_name,
                'status': 'not_found'
            }
            
        except asyncio.TimeoutError:
            print(f"  ✗ Page load timeout")
            await browser.close()
            return {
                'game_id': game_id,
                'game_name': game_name,
                'status': 'timeout'
            }
        except Exception as e:
            print(f"  ✗ Error: {str(e)[:50]}")
            await browser.close()
            return {
                'game_id': game_id,
                'game_name': game_name,
                'status': 'error',
                'error': str(e)
            }

async def test_scraper():
    """Test the scraper with a few known games."""
    
    test_games = [
        (13, "Catan"),
        (822, "Carcassonne"),
        (3110, "Puerto Rico"),
    ]
    
    print("Testing Playwright BGG scraper (with improved settings)\n")
    print("=" * 70)
    
    results = []
    for game_id, game_name in test_games:
        result = await get_game_dimensions(game_id, game_name)
        results.append(result)
    
    print("=" * 70)
    print("\nSummary:")
    successful = [r for r in results if r['status'] == 'success']
    print(f"✓ Successfully scraped: {len(successful)}/{len(results)}")
    
    if successful:
        print("\nScraped dimensions:")
        for r in successful:
            print(f"  {r['game_name']}: {r['length']} × {r['width']} × {r['height']} cm")
    
    # Show errors
    errors = [r for r in results if r['status'] != 'success']
    if errors:
        print(f"\nFailed ({len(errors)}):")
        for r in errors:
            print(f"  {r['game_name']}: {r['status']}")
    
    return results

if __name__ == "__main__":
    results = asyncio.run(test_scraper())
