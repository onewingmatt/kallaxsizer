#!/usr/bin/env python3
import csv

# Parse the real collection dimensions
games = {}
with open('/home/onewing/bgsize/real_collection_dims.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith('//'):
            continue
        # Parse: ID: [L, W, H], // Name
        parts = line.split('//')
        if len(parts) < 2:
            continue
        
        name = parts[-1].strip()
        dims_part = parts[0].strip()
        
        # Extract ID and dimensions
        if ':' not in dims_part:
            continue
        
        id_str, dims_str = dims_part.split(':', 1)
        game_id = int(id_str.strip())
        
        # Parse [L, W, H]
        dims_str = dims_str.strip()
        if not dims_str.startswith('[') or not dims_str.endswith('],'):
            if not dims_str.endswith(']'):
                continue
            dims_str = dims_str.rstrip('],')
        else:
            dims_str = dims_str.rstrip('],')
        
        try:
            dims = [float(x.strip()) for x in dims_str.strip('[]').split(',')]
            if len(dims) == 3:
                games[game_id] = {'name': name, 'dims': dims}
        except:
            continue

# Kallax dimensions with overhang tolerance
KALLAX_W = 33 + 2
KALLAX_H = 33 + 2
KALLAX_D = 39 + 2

# Check which games don't fit
too_big = []
for game_id, game in games.items():
    l, w, h = game['dims']
    sorted_dims = sorted([l, w, h])
    smallest, middle, largest = sorted_dims
    
    # A game fits if all these are true:
    if not (smallest <= KALLAX_W and middle <= KALLAX_H and largest <= KALLAX_D):
        # Calculate overhang
        excess = []
        if smallest > KALLAX_W:
            excess.append(f"smallest {smallest:.1f} > {KALLAX_W}")
        if middle > KALLAX_H:
            excess.append(f"middle {middle:.1f} > {KALLAX_H}")
        if largest > KALLAX_D:
            excess.append(f"largest {largest:.1f} > {KALLAX_D}")
        
        too_big.append({
            'id': game_id,
            'name': game['name'],
            'dims': [l, w, h],
            'sorted': sorted_dims,
            'excess': excess
        })

# Sort by largest dimension descending
too_big.sort(key=lambda g: g['sorted'][2], reverse=True)

print("\n🛑 GAMES THAT DON'T FIT (sorted by largest dimension):\n")
print(f"{'ID':<8} {'Largest':<10} {'Other dims':<20} {'Game Name':<40} {'Exceeds':<30}")
print("=" * 110)

for game in too_big:
    largest = game['sorted'][2]
    other_dims = f"{game['sorted'][0]:.1f} × {game['sorted'][1]:.1f}"
    excess_str = " | ".join(game['excess'])
    print(f"{game['id']:<8} {largest:>8.1f}cm {other_dims:<20} {game['name']:<40} {excess_str:<30}")

print(f"\n📊 Summary: {len(too_big)} games don't fit out of {len(games)} total")
print(f"   Coverage: {len(games) - len(too_big)}/{len(games)} games fit ({100*(len(games)-len(too_big))/len(games):.1f}%)")

# Show some options for too-big games
if too_big:
    print(f"\n💡 Options for the {len(too_big)} non-fitting games:")
    print("   • Store separately or on different shelf")
    print("   • Remove from this shelf's planning")
    print("   • Increase shelf dimensions (Kallax 2x4 or larger)")
