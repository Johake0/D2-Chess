
import json
from collections import deque

# === CONFIG ===
adjacency_file = "board_adjacency.json"
output_file = "layout_64x64_multi_seed_final.json"
GRID_SIZE = 64

# Confirmed corner seeds
SEEDS = {
    (0, 0): "2692",               # top-left
    (0, GRID_SIZE - 1): "3986",   # top-right
    (GRID_SIZE - 1, 0): "1996",   # bottom-left
    (GRID_SIZE - 1, GRID_SIZE - 1): "311"  # bottom-right
}

# === LOAD ADJACENCY MAP ===
with open(adjacency_file, "r", encoding="utf-8") as f:
    adjacency = json.load(f)

layout = [[-1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
used = set()

def bfs_expand(seed_row, seed_col, seed_id):
    queue = deque()
    layout[seed_row][seed_col] = seed_id
    used.add(seed_id)
    queue.append((seed_row, seed_col, seed_id))

    directions = {
        "right": (0, 1),
        "bottom": (1, 0),
        "left": (0, -1),
        "top": (-1, 0)
    }

    while queue:
        r, c, board_id = queue.popleft()
        for dir_name, (dr, dc) in directions.items():
            nr, nc = r + dr, c + dc
            if not (0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE):
                continue
            if layout[nr][nc] != -1:
                continue
            candidates = adjacency.get(board_id, {}).get(dir_name, [])
            for candidate_id in candidates:
                if candidate_id in used:
                    continue
                layout[nr][nc] = candidate_id
                used.add(candidate_id)
                queue.append((nr, nc, candidate_id))
                break

# Expand from each seed
for (row, col), seed_id in SEEDS.items():
    if seed_id not in used:
        bfs_expand(row, col, seed_id)

# Convert all placed IDs to int
layout_fixed = [
    [int(cell) if isinstance(cell, str) else cell for cell in row]
    for row in layout
]

# Save layout
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(layout_fixed, f, indent=2)

print(f"✅ Layout saved to {output_file} with {sum(cell != -1 for row in layout_fixed for cell in row)} boards.")
