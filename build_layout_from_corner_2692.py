import json

# === CONFIG ===
adjacency_file = "board_adjacency.json"
output_file = "layout_16x16_from_2692.json"
GRID_SIZE = 16
SEED = "2692"

# === LOAD ADJACENCY DATA ===
with open(adjacency_file, "r", encoding="utf-8") as f:
    adjacency = json.load(f)

layout = [[-1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
used = set()

# === PLACE SEED ===
layout[0][0] = SEED
used.add(SEED)

# === BUILD FIRST ROW ===
for col in range(1, GRID_SIZE):
    left_id = layout[0][col - 1]
    right_neighbors = adjacency.get(left_id, {}).get("right", [])
    placed = False
    for neighbor in right_neighbors:
        if neighbor not in used:
            layout[0][col] = neighbor
            used.add(neighbor)
            placed = True
            break
    if not placed:
        break  # stop row if no more matches

# === BUILD FIRST COLUMN ===
for row in range(1, GRID_SIZE):
    top_id = layout[row - 1][0]
    bottom_neighbors = adjacency.get(top_id, {}).get("bottom", [])
    placed = False
    for neighbor in bottom_neighbors:
        if neighbor not in used:
            layout[row][0] = neighbor
            used.add(neighbor)
            placed = True
            break
    if not placed:
        break  # stop column if no more matches

# === SAVE OUTPUT ===
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(layout, f, indent=2)

placed_count = sum(1 for row in layout for val in row if val != -1)
print(f"✅ Placed {placed_count} boards from corner seed {SEED}")
print(f"✅ Layout saved to {output_file}")
