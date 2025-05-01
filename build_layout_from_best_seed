import json

# === CONFIG ===
adjacency_file = "board_adjacency.json"
output_file = "layout_16x16_best_seed.json"
GRID_SIZE = 16

# === LOAD DATA ===
with open(adjacency_file, "r", encoding="utf-8") as f:
    adjacency = json.load(f)

# === FIND BEST-CONNECTED SEED TILE ===
def get_connection_score(adj):
    return len(adj["top"]) + len(adj["bottom"]) + len(adj["left"]) + len(adj["right"])

best_seed = max(adjacency.items(), key=lambda x: get_connection_score(x[1]))[0]
print(f"🌱 Using best seed: {best_seed}")
print(f"  Right: {len(adjacency[best_seed]['right'])}, Bottom: {len(adjacency[best_seed]['bottom'])}")

# === INIT ===
layout = [[-1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
used = set()

layout[0][0] = best_seed
used.add(best_seed)

# === BUILD FIRST ROW ===
for col in range(1, GRID_SIZE):
    left_id = layout[0][col - 1]
    options = adjacency[left_id]["right"]
    found = False
    for option in options:
        if option not in used:
            layout[0][col] = option
            used.add(option)
            found = True
            break
    if not found:
        break

# === BUILD COLUMNS BASED ON FIRST ROW ===
for row in range(1, GRID_SIZE):
    for col in range(GRID_SIZE):
        above_id = layout[row - 1][col]
        if above_id == -1:
            continue
        options = adjacency[above_id]["bottom"]
        found = False
        for option in options:
            if option not in used:
                layout[row][col] = option
                used.add(option)
                found = True
                break
        if not found:
            continue

# === SAVE LAYOUT ===
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(layout, f, indent=2)

placed = sum(1 for row in layout for val in row if val != -1)
print(f"✅ Boards placed: {placed} / {GRID_SIZE * GRID_SIZE}")
print(f"✅ Layout saved to {output_file}")
