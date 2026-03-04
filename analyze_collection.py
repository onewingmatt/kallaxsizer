#!/usr/bin/env python3
"""
Analyze the exported collection CSV and update our database with real dimensions.
"""

import csv
import os

csv_path = '/home/onewing/Downloads/collection_with_dimensions.csv'

print("=" * 70)
print("ANALYZING EXPORTED COLLECTION DATA")
print("=" * 70)

games_with_dims = 0
games_without_dims = 0
total_games = 0
real_dims = {}

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        total_games += 1
        
        game_id = row.get('objectid', '')
        game_name = row.get('objectname', '')
        
        # Get dimensions (in inches from the CSV)
        length_in = row.get('length_in', '')
        width_in = row.get('width_in', '')
        depth_in = row.get('depth_in', '')
        
        # Check if we have dimensions
        if length_in and width_in and depth_in:
            try:
                l = float(length_in)
                w = float(width_in)
                d = float(depth_in)
                
                # Skip zero dimensions
                if l > 0 and w > 0 and d > 0:
                    # Convert inches to cm (inches * 2.54)
                    l_cm = round(l * 2.54, 2)
                    w_cm = round(w * 2.54, 2)
                    d_cm = round(d * 2.54, 2)
                    
                    real_dims[int(game_id)] = {
                        'name': game_name,
                        'length': l_cm,
                        'width': w_cm,
                        'depth': d_cm,
                        'length_in': round(l, 2),
                        'width_in': round(w, 2),
                        'depth_in': round(d, 2)
                    }
                    games_with_dims += 1
                else:
                    games_without_dims += 1
            except (ValueError, TypeError):
                games_without_dims += 1
        else:
            games_without_dims += 1

print(f"\n📊 SUMMARY")
print(f"Total games in collection: {total_games}")
print(f"✅ Games WITH dimensions: {games_with_dims}")
print(f"❌ Games WITHOUT dimensions: {games_without_dims}")
print(f"Coverage: {100*games_with_dims/total_games:.1f}%")

print(f"\n🎲 SAMPLE OF REAL DIMENSIONS (first 10 games):")
print("-" * 70)

for i, (game_id, data) in enumerate(list(real_dims.items())[:10], 1):
    print(f"{i}. {data['name']} (ID: {game_id})")
    print(f"   {data['length']} × {data['width']} × {data['depth']} cm")
    print(f"   ({data['length_in']} × {data['width_in']} × {data['depth_in']} inches)")

# Save formatted for JavaScript insertion
print(f"\n💾 SAVING FORMATTED DATA...")
with open('/home/onewing/bgsize/real_collection_dims.txt', 'w') as f:
    f.write("// Real dimensions from user's BGG collection export\n")
    f.write("// Converted from inches (×2.54) to centimeters\n")
    f.write("// Format: ID: [length, width, depth], // Name\n\n")
    
    for game_id in sorted(real_dims.keys()):
        data = real_dims[game_id]
        f.write(f"      {game_id}: [{data['length']}, {data['width']}, {data['depth']}], // {data['name']}\n")

print(f"✓ Saved {len(real_dims)} games to real_collection_dims.txt")

print("\n" + "=" * 70)
print(f"NEXT STEP: Update KNOWN_GAME_DIMS in index.html with real data!")
print("=" * 70)
