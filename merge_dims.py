
import json
import re
import os

def parse_txt(file_path):
    dims = {}
    # Pattern to match ID: [L, W, H], // Name
    pattern = re.compile(r'^\s*(\d+):\s*\[([\d\.,\s]+)\]')
    
    if not os.path.exists(file_path):
        return dims
        
    with open(file_path, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                game_id = match.group(1)
                raw_dims = match.group(2).split(',')
                if len(raw_dims) == 3:
                    try:
                        l = float(raw_dims[0].strip())
                        w = float(raw_dims[1].strip())
                        h = float(raw_dims[2].strip())
                        # Sort descending
                        sorted_dims = sorted([l, w, h], reverse=True)
                        dims[game_id] = {
                            'l': round(sorted_dims[0], 1),
                            'w': round(sorted_dims[1], 1),
                            'h': round(sorted_dims[2], 1)
                        }
                    except ValueError:
                        continue
    return dims

def main():
    cache_file = 'dims_cache.json'
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cache = json.load(f)
    else:
        cache = {}
        
    print(f"Current cache size: {len(cache)}")
    
    real_dims = parse_txt('real_collection_dims.txt')
    to_add_dims = parse_txt('dims_to_add.txt')
    
    print(f"Found {len(real_dims)} in real_collection_dims.txt")
    print(f"Found {len(to_add_dims)} in dims_to_add.txt")
    
    added = 0
    updated = 0
    
    for gid, d in real_dims.items():
        if gid not in cache or cache[gid] is None:
            cache[gid] = d
            added += 1
        else:
            # Only update if current is None or different
            if cache[gid] != d:
                cache[gid] = d
                updated += 1
                
    for gid, d in to_add_dims.items():
        if gid not in cache or cache[gid] is None:
            cache[gid] = d
            added += 1
        elif cache[gid] != d:
            # Prioritize real_dims over to_add_dims if already added? 
            # For now just update if different
            cache[gid] = d
            updated += 1
            
    with open(cache_file, 'w') as f:
        json.dump(cache, f, indent=2)
        
    print(f"Finished. Added: {added}, Updated: {updated}")
    print(f"New cache size: {len(cache)}")

if __name__ == "__main__":
    main()
