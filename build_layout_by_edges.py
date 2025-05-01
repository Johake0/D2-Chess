import json
from collections import deque

# Re-import files after reset
adjacency_path = "board_adjacency.json"
output_path = "layout_16x16_fixed.json"
GRID_SIZE = 16

# === LOAD ADJACENCY MAP ===
with open(adjacency_path, "r", encoding="utf-8") as f:
    adjacency = json.load(f)

# === INITIALIZE EMPTY LAYOUT ===
layout = [[-1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
used = set()

# === BFS EXPANSION FUNCTION ===
def fill_layout_from_seed(seed_id):
    queue = deque()
    layout[0][0] = seed_id
    used.add(seed_id)
    queue.append((0, 0, seed_id))

    while queue:
        r, c, board_id = queue.popleft()

        # Try all directions
        directions = {
            "right": (0, 1),
            "bottom": (1, 0),
            "left": (0, -1),
            "top": (-1, 0)
        }

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
                break  # Only place one tile per direction

# === PICK BEST-CONNECTED STARTING BOARD ===
def get_connection_score(adj):
    return len(adj["top"]) + len(adj["bottom"]) + len(adj["left"]) + len(adj["right"])

best_seed = max(adjacency.items(), key=lambda x: get_connection_score(x[1]))[0]
fill_layout_from_seed(best_seed)

# === SAVE LAYOUT ===
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(layout, f, indent=2)

placed = sum(1 for row in layout for val in row if val != -1)
output_path, placed
