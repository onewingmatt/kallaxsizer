#!/usr/bin/env python3
"""
refresh_cache.py — Force re-fetch dimensions for all games in dims_cache.json.

Usage:
    python3 refresh_cache.py           # re-fetch everything (clears old entries first)
    python3 refresh_cache.py --null    # only re-fetch games that currently have null dims
    python3 refresh_cache.py --dry-run # show what would be fetched, don't write anything
"""

import json
import os
import sys
import time
import requests

GEEKDO_BASE = "https://api.geekdo.com"
CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dims_cache.json")
SAVE_EVERY = 25   # save progress to disk every N games
RATE_DELAY = 0.25 # seconds between API calls (polite rate limiting)

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
})


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            return json.load(f)
    return {}


def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def fetch_best_dims(gid):
    """
    Fetch all versions for a game and return the best-fit dimensions.
    Strategy: prefer English editions; among those, pick the one with the
    largest volume (most likely the main retail box, not a mini/promo).
    Falls back to any edition with valid dims if no English found.
    Returns {'l', 'w', 'h'} in cm or None.
    """
    try:
        r1 = session.get(
            f"{GEEKDO_BASE}/api/geekitems",
            params={'objectid': str(gid), 'objecttype': 'thing', 'nosession': '1'},
            timeout=12,
        )
        if r1.status_code != 200:
            print(f"  [{gid}] HTTP {r1.status_code} on thing lookup")
            return None

        version_links = r1.json().get('item', {}).get('links', {}).get('boardgameversion', [])
        if not version_links:
            return None

        candidates = []  # (volume_cm3, is_english, dims_dict)

        for ver in version_links:
            vid = ver.get('objectid')
            if not vid:
                continue
            time.sleep(RATE_DELAY)
            r2 = session.get(
                f"{GEEKDO_BASE}/api/geekitems",
                params={'objectid': vid, 'objecttype': 'version', 'subtype': 'boardgameversion'},
                timeout=12,
            )
            if r2.status_code != 200:
                continue

            item = r2.json().get('item', {})
            l = float(item.get('length', 0) or 0)
            w = float(item.get('width', 0) or 0)
            d = float(item.get('depth', 0) or 0)
            if not (l > 0 and w > 0 and d > 0):
                continue

            # Convert inches → cm and sort largest-first
            dims = sorted([l * 2.54, w * 2.54, d * 2.54], reverse=True)
            volume = dims[0] * dims[1] * dims[2]

            # Check if this is an English edition
            lang_links = item.get('links', {}).get('language', [])
            is_english = any(
                str(lang.get('value', '')).lower() == 'english'
                for lang in (lang_links if isinstance(lang_links, list) else lang_links.values())
            )

            candidates.append((volume, is_english, {
                'l': round(dims[0], 1),
                'w': round(dims[1], 1),
                'h': round(dims[2], 1),
            }))

        if not candidates:
            return None

        # Prefer English editions, then pick largest volume
        english = [(vol, eng, d) for vol, eng, d in candidates if eng]
        pool = english if english else candidates
        pool.sort(key=lambda x: x[0], reverse=True)
        return pool[0][2]

    except Exception as e:
        print(f"  [{gid}] error: {e}")
        return None


def main():
    null_only = '--null' in sys.argv
    dry_run = '--dry-run' in sys.argv

    cache = load_cache()
    all_ids = list(cache.keys())

    if null_only:
        ids_to_refresh = [gid for gid in all_ids if not cache[gid]]
        print(f"Re-fetching {len(ids_to_refresh)} games with null dims (out of {len(all_ids)} total)...")
    else:
        ids_to_refresh = all_ids
        print(f"Re-fetching ALL {len(ids_to_refresh)} games in cache...")

    if dry_run:
        print(f"[DRY RUN] Would re-fetch: {ids_to_refresh[:10]}{'...' if len(ids_to_refresh) > 10 else ''}")
        return

    total = len(ids_to_refresh)
    success = 0
    failed = 0

    for i, gid in enumerate(ids_to_refresh, 1):
        dims = fetch_best_dims(gid)
        cache[gid] = dims
        if dims:
            success += 1
            print(f"  [{i}/{total}] {gid}: {dims['l']}×{dims['w']}×{dims['h']} cm ✓")
        else:
            failed += 1
            print(f"  [{i}/{total}] {gid}: no dims found")

        if i % SAVE_EVERY == 0:
            save_cache(cache)
            print(f"  💾 Progress saved ({i}/{total})")

    save_cache(cache)
    print(f"\nDone. {success}/{total} games got dimensions, {failed} had none.")


if __name__ == '__main__':
    main()
