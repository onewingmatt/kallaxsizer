#!/usr/bin/env python3
"""
Benchmark double-deep packing algorithms on real game data extracted from index.html.
Runs three variants and reports cube counts so we can pick the best one.
"""
import re
import itertools

# ── Extract game dims from index.html ─────────────────────────────────────────
dims_re = re.compile(r'(\d+):\s*\[([0-9., ]+)\].*?//\s*(.+)')
games = []
seen = set()
with open('/home/onewing/bgsize/index.html') as f:
    in_block = False
    for line in f:
        if 'const KNOWN_GAME_DIMS' in line:
            in_block = True
        if in_block:
            m = dims_re.search(line)
            if m:
                gid = int(m.group(1))
                if gid in seen:
                    continue
                seen.add(gid)
                raw = [float(x.strip()) for x in m.group(2).split(',')]
                name = m.group(3).strip()
                games.append({'id': gid, 'name': name, 'dims': raw})
            if '};' in line and in_block and len(games) > 10:
                break

print(f"Loaded {len(games)} games from KNOWN_GAME_DIMS")

# ── Constants ─────────────────────────────────────────────────────────────────
KALLAX_W = 33.0
KALLAX_H = 33.0
KALLAX_D = 39.0
W_TOL = 2.0
D_TOL = 4.5   # slightly more generous than current 4.0 to match physical reality
TOTAL_DEPTH = KALLAX_D + D_TOL   # 43.5 cm

# ── Filter games that physically fit ─────────────────────────────────────────
def can_fit(dims):
    s = sorted(dims)
    return s[0] <= KALLAX_W + W_TOL and s[1] <= KALLAX_H + W_TOL and s[2] <= TOTAL_DEPTH

fitting = [g for g in games if can_fit(g['dims'])]
print(f"Games that fit: {len(fitting)} / {len(games)}")

# ── Orientation enumerator ────────────────────────────────────────────────────
def get_orientations(dims):
    d = sorted(dims, reverse=True)  # [largest, middle, smallest]
    perms = set()
    result = []
    for p in itertools.permutations(d):
        key = p
        if key in perms:
            continue
        perms.add(key)
        spine, depth, height = p[2], p[1], p[0]
        if (spine <= KALLAX_W + W_TOL and
            depth <= TOTAL_DEPTH and
            height <= KALLAX_H + W_TOL):
            result.append({'spine': spine, 'depth': depth, 'height': height})
    result.sort(key=lambda o: o['depth'])  # shallowest first
    return result

# ─────────────────────────────────────────────────────────────────────────────
# ALGORITHM A: OLD column model (column width locked to first game's spine,
# back games must have spine ≤ column width)
# This is what we had several iterations ago.
# ─────────────────────────────────────────────────────────────────────────────
def algo_a(games_list):
    """Old column model."""
    gs = sorted(games_list, key=lambda g: -sorted(g['dims'])[1] * sorted(g['dims'])[2])
    cubes = []
    for g in gs:
        orients = get_orientations(g['dims'])
        if not orients:
            continue
        best = None
        best_waste = float('inf')
        for c_idx, cube in enumerate(cubes):
            for o in orients:
                for col_idx, col in enumerate(cube['cols']):
                    if o['spine'] <= col['width'] and col['depth_left'] >= o['depth']:
                        waste = col['depth_left'] - o['depth']
                        if waste < best_waste:
                            best = ('col', c_idx, col_idx, o)
                            best_waste = waste
                if cube['width_left'] >= o['spine']:
                    waste = (TOTAL_DEPTH - o['depth']) + 1000
                    if waste < best_waste:
                        best = ('new_col', c_idx, -1, o)
                        best_waste = waste
        if best:
            kind, c_idx, col_idx, o = best
            if kind == 'col':
                cubes[c_idx]['cols'][col_idx]['depth_left'] -= o['depth']
            else:
                cubes[c_idx]['width_left'] -= o['spine']
                cubes[c_idx]['cols'].append({'width': o['spine'], 'depth_left': TOTAL_DEPTH - o['depth']})
        else:
            o = orients[0]
            cubes.append({'width_left': KALLAX_W - o['spine'],
                          'cols': [{'width': o['spine'], 'depth_left': TOTAL_DEPTH - o['depth']}]})
    return len(cubes)

# ─────────────────────────────────────────────────────────────────────────────
# ALGORITHM B: Current two-strip model
# front.maxDepth + back.maxDepth ≤ TOTAL_DEPTH (too conservative)
# ─────────────────────────────────────────────────────────────────────────────
def algo_b(games_list):
    """Current two-strip model with global maxDepth per strip."""
    gs = sorted(games_list, key=lambda g: -min(sorted(g['dims'])[:2]))
    cubes = []
    for g in gs:
        orients = get_orientations(g['dims'])
        if not orients:
            continue
        best = None
        best_score = float('inf')
        for c_idx, cube in enumerate(cubes):
            for o in orients:
                # Front strip
                if (cube['front']['w_left'] >= o['spine'] and
                        o['depth'] + cube['back']['max_d'] <= TOTAL_DEPTH):
                    w_waste = cube['front']['w_left'] - o['spine']
                    d_waste = TOTAL_DEPTH - o['depth'] - cube['back']['max_d']
                    score = w_waste + d_waste * 0.3
                    if score < best_score:
                        best = ('front', c_idx, o)
                        best_score = score
                # Back strip
                if (cube['back']['w_left'] >= o['spine'] and
                        cube['front']['max_d'] + o['depth'] <= TOTAL_DEPTH):
                    w_waste = cube['back']['w_left'] - o['spine']
                    d_waste = TOTAL_DEPTH - cube['front']['max_d'] - o['depth']
                    score = w_waste + d_waste * 0.3
                    if score < best_score:
                        best = ('back', c_idx, o)
                        best_score = score
        if best:
            strip, c_idx, o = best
            cubes[c_idx][strip]['w_left'] -= o['spine']
            cubes[c_idx][strip]['max_d'] = max(cubes[c_idx][strip]['max_d'], o['depth'])
        else:
            o = orients[0]
            cubes.append({
                'front': {'w_left': KALLAX_W - o['spine'], 'max_d': o['depth']},
                'back':  {'w_left': KALLAX_W,              'max_d': 0}
            })
    return len(cubes)

# ─────────────────────────────────────────────────────────────────────────────
# ALGORITHM C: Per-column depth tracking
# Each cube has paired columns. Depth constraint is per-column:
#   col.front_depth + col.back_depth ≤ TOTAL_DEPTH
# Front and back widths are tracked independently.
# This is a much more accurate physical model.
# ─────────────────────────────────────────────────────────────────────────────
def algo_c(games_list):
    """Per-column depth tracking — accurate physical model."""
    # Sort: hardest to pair first (deepest minimum depth)
    gs = sorted(games_list, key=lambda g: -min(sorted(g['dims'])[:2]))
    cubes = []

    for g in gs:
        orients = get_orientations(g['dims'])
        if not orients:
            continue
        best = None
        best_score = float('inf')

        for c_idx, cube in enumerate(cubes):
            for o in orients:
                # ── Try placing in back of an existing column ──────────────
                for col_idx, col in enumerate(cube['cols']):
                    # Each column tracks: front_spine, back_spine, front_depth, back_depth
                    # A game can go into the BACK of a column if:
                    #   - there's depth room: col.front_depth + o.depth ≤ TOTAL_DEPTH
                    #   - back hasn't been filled yet in that column
                    if col['back_depth'] == 0 and col['front_depth'] + o['depth'] <= TOTAL_DEPTH:
                        if cube['back_w_left'] >= o['spine']:
                            w_waste = cube['back_w_left'] - o['spine']
                            d_waste = TOTAL_DEPTH - col['front_depth'] - o['depth']
                            score = w_waste + d_waste * 0.3
                            if score < best_score:
                                best = ('back_of_col', c_idx, col_idx, o)
                                best_score = score
                    # Try placing in FRONT of an existing back-only column
                    if col['front_depth'] == 0 and col['back_depth'] + o['depth'] <= TOTAL_DEPTH:
                        if cube['front_w_left'] >= o['spine']:
                            w_waste = cube['front_w_left'] - o['spine']
                            d_waste = TOTAL_DEPTH - col['back_depth'] - o['depth']
                            score = w_waste + d_waste * 0.3
                            if score < best_score:
                                best = ('front_of_col', c_idx, col_idx, o)
                                best_score = score

                # ── Try opening a new front-only column ───────────────────
                if cube['front_w_left'] >= o['spine']:
                    d_waste = (TOTAL_DEPTH - o['depth']) + 500  # penalty for new column
                    w_waste = cube['front_w_left'] - o['spine']
                    score = w_waste + d_waste * 0.3
                    if score < best_score:
                        best = ('new_front_col', c_idx, -1, o)
                        best_score = score

                # ── Try opening a new back-only column ────────────────────
                if cube['back_w_left'] >= o['spine']:
                    d_waste = (TOTAL_DEPTH - o['depth']) + 500
                    w_waste = cube['back_w_left'] - o['spine']
                    score = w_waste + d_waste * 0.3
                    if score < best_score:
                        best = ('new_back_col', c_idx, -1, o)
                        best_score = score

        if best:
            action = best[0]
            c_idx = best[1]
            col_idx = best[2]
            o = best[3]
            cube = cubes[c_idx]
            if action == 'back_of_col':
                cube['back_w_left'] -= o['spine']
                cube['cols'][col_idx]['back_depth'] = o['depth']
            elif action == 'front_of_col':
                cube['front_w_left'] -= o['spine']
                cube['cols'][col_idx]['front_depth'] = o['depth']
            elif action == 'new_front_col':
                cube['front_w_left'] -= o['spine']
                cube['cols'].append({'front_depth': o['depth'], 'back_depth': 0})
            elif action == 'new_back_col':
                cube['back_w_left'] -= o['spine']
                cube['cols'].append({'front_depth': 0, 'back_depth': o['depth']})
        else:
            # New cube — open a shallowest front column
            o = orients[0]
            cubes.append({
                'front_w_left': KALLAX_W - o['spine'],
                'back_w_left':  KALLAX_W,
                'cols': [{'front_depth': o['depth'], 'back_depth': 0}]
            })

    return len(cubes)

# ─────────────────────────────────────────────────────────────────────────────
# Verify Macao example: 6× Macao in one cube?
# Macao: 30.96 × 21.91 × 6.83
# Physical: 4 in back (6.83 spine, 21.91 depth) + 2 in front (same orientation)
# Total depth at those 2 positions: 21.91 + 21.91 = 43.82 (just within 43.5 w/ D_TOL=4.5)
# ─────────────────────────────────────────────────────────────────────────────
macao_dims = [30.96, 21.91, 6.83]
macao_orients = get_orientations(macao_dims)
print(f"\nMacao orientations: {macao_orients}")

macao_6 = [{'id': 55670 + i, 'name': f'Macao {i}', 'dims': macao_dims} for i in range(6)]
print(f"Algo A — 6× Macao: {algo_a(macao_6)} cubes (expect 1 or at most 2)")
print(f"Algo B — 6× Macao: {algo_b(macao_6)} cubes (expect 1 or at most 2)")
print(f"Algo C — 6× Macao: {algo_c(macao_6)} cubes (expect 1 or at most 2)")

# ── Run all three on the full collection ─────────────────────────────────────
print(f"\n{'='*55}")
print(f"Full collection benchmark ({len(fitting)} games)")
print(f"{'='*55}")

# ─────────────────────────────────────────────────────────────────────────────
# ALGORITHM D: Per-column depth tracking with MINIMUM-DEPTH scoring
# Key insight: in a column, we want to use MINIMUM depth per game so that
# more games can stack behind each other. Wrong: "tightest fit" (min waste).
# Correct: minimize the depth used by each game (maximizes future capacity).
# ─────────────────────────────────────────────────────────────────────────────
def algo_d(games_list):
    """Per-column model, scoring by minimum depth used (not minimum remaining waste)."""
    gs = sorted(games_list, key=lambda g: -min(sorted(g['dims'])[:2]))
    cubes = []

    for g in gs:
        orients = get_orientations(g['dims'])
        if not orients:
            continue
        best = None
        best_score = float('inf')  # score = (open_new_cube_penalty) + depth_used

        for c_idx, cube in enumerate(cubes):
            for o in orients:
                # Back of an existing column
                for col_idx, col in enumerate(cube['cols']):
                    if col['back_depth'] == 0 and col['front_depth'] + o['depth'] <= TOTAL_DEPTH:
                        if cube['back_w_left'] >= o['spine']:
                            # Score: prefer min depth used, break ties by tighter width fit
                            score = o['depth'] + (cube['back_w_left'] - o['spine']) * 0.01
                            if score < best_score:
                                best = ('back_of_col', c_idx, col_idx, o)
                                best_score = score
                    # Front of a back-only column
                    if col['front_depth'] == 0 and col['back_depth'] + o['depth'] <= TOTAL_DEPTH:
                        if cube['front_w_left'] >= o['spine']:
                            score = o['depth'] + (cube['front_w_left'] - o['spine']) * 0.01
                            if score < best_score:
                                best = ('front_of_col', c_idx, col_idx, o)
                                best_score = score
                # New front column in existing cube (penalise with large constant)
                if cube['front_w_left'] >= o['spine']:
                    score = 500 + o['depth'] + (cube['front_w_left'] - o['spine']) * 0.01
                    if score < best_score:
                        best = ('new_front_col', c_idx, -1, o)
                        best_score = score
                if cube['back_w_left'] >= o['spine']:
                    score = 500 + o['depth'] + (cube['back_w_left'] - o['spine']) * 0.01
                    if score < best_score:
                        best = ('new_back_col', c_idx, -1, o)
                        best_score = score

        if best:
            action, c_idx, col_idx, o = best
            cube = cubes[c_idx]
            if action == 'back_of_col':
                cube['back_w_left'] -= o['spine']
                cube['cols'][col_idx]['back_depth'] = o['depth']
            elif action == 'front_of_col':
                cube['front_w_left'] -= o['spine']
                cube['cols'][col_idx]['front_depth'] = o['depth']
            elif action == 'new_front_col':
                cube['front_w_left'] -= o['spine']
                cube['cols'].append({'front_depth': o['depth'], 'back_depth': 0})
            elif action == 'new_back_col':
                cube['back_w_left'] -= o['spine']
                cube['cols'].append({'front_depth': 0, 'back_depth': o['depth']})
        else:
            o = orients[0]
            cubes.append({
                'front_w_left': KALLAX_W - o['spine'],
                'back_w_left':  KALLAX_W,
                'cols': [{'front_depth': o['depth'], 'back_depth': 0}]
            })

    return len(cubes)

# ─────────────────────────────────────────────────────────────────────────────
# ALGORITHM E: Per-column, min-depth scoring + per-column stacking
# Extension of D but columns can have MORE than 2 games (front + multiple back)
# by tracking depth_used per column as a running total.
# This accurately models the user's real scenario:
#   4 games in back of a single column + 2 in front of some positions
# ─────────────────────────────────────────────────────────────────────────────
def algo_e(games_list):
    """Columns track total depth used; games stack as deep as needed."""
    gs = sorted(games_list, key=lambda g: -min(sorted(g['dims'])[:2]))
    cubes = []

    for g in gs:
        orients = get_orientations(g['dims'])
        if not orients:
            continue
        best = None
        best_score = float('inf')

        for c_idx, cube in enumerate(cubes):
            for o in orients:
                for col_idx, col in enumerate(cube['cols']):
                    if col['depth_used'] + o['depth'] <= TOTAL_DEPTH:
                        if cube['w_left'] >= o['spine'] or o['spine'] <= col['width']:
                            effective_spine_cost = max(0, o['spine'] - col['width'])
                            if cube['w_left'] >= effective_spine_cost:
                                score = o['depth'] + effective_spine_cost * 0.5
                                if score < best_score:
                                    best = ('in_col', c_idx, col_idx, o, effective_spine_cost)
                                    best_score = score
                # New column
                if cube['w_left'] >= o['spine']:
                    score = 500 + o['depth'] + (cube['w_left'] - o['spine']) * 0.01
                    if score < best_score:
                        best = ('new_col', c_idx, -1, o, o['spine'])
                        best_score = score

        if best:
            action, c_idx, col_idx, o, spine_cost = best
            cube = cubes[c_idx]
            if action == 'in_col':
                cube['w_left'] -= spine_cost
                cube['cols'][col_idx]['depth_used'] += o['depth']
                cube['cols'][col_idx]['width'] = max(cube['cols'][col_idx]['width'], o['spine'])
            else:
                cube['w_left'] -= spine_cost
                cube['cols'].append({'depth_used': o['depth'], 'width': o['spine']})
        else:
            o = orients[0]
            cubes.append({
                'w_left': KALLAX_W - o['spine'],
                'cols': [{'depth_used': o['depth'], 'width': o['spine']}]
            })

    return len(cubes)


print(f"Algo D — 6× Macao: {algo_d(macao_6)} cubes (expect 1)")
print(f"Algo E — 6× Macao: {algo_e(macao_6)} cubes (expect 1)")

a = algo_a(fitting)
b = algo_b(fitting)
c = algo_c(fitting)
d = algo_d(fitting)
e = algo_e(fitting)

print(f"\n{'='*55}")
print(f"Full collection benchmark ({len(fitting)} games)")
print(f"{'='*55}")
print(f"Algorithm A (old  column, footprint sort):        {a} cubes")
print(f"Algorithm B (two-strip maxDepth, current code):   {b} cubes")
print(f"Algorithm C (per-col depth, min-width-waste):     {c} cubes")
print(f"Algorithm D (per-col depth, min-depth scoring):   {d} cubes")
print(f"Algorithm E (per-col stacking, min-depth):        {e} cubes")
results = {'A': a, 'B': b, 'C': c, 'D': d, 'E': e}
winner = min(results, key=results.get)
print(f"\nWinner: {winner} = {results[winner]} cubes")
