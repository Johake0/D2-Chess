import json

# === CONFIG ===
adjacency_file = "board_adjacency.json"
output_file = "layout_16x16_by_seed.json"
GRID_SIZE = 16
SEED_ID = "2942"  # Starting board

# === LOAD DATA ===
with open(adjacency_file, "r", encoding="utf-8") as f:
    adjacency = json.load(f)

# === INIT ===
layout = [[-1 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
used = set()

# Place seed in top-left
layout[0][0] = SEED_ID
used.add(SEED_ID)

print(f"Seed {SEED_ID}")
print(f"  Right options: {adjacency.get(SEED_ID, {}).get('right', [])}")
print(f"  Bottom options: {adjacency.get(SEED_ID, {}).get('bottom', [])}")


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
        break  # Stop row if no match

# === BUILD EACH COLUMN BASED ON ABOVE ROW ===
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
            continue  # Leave -1 if nothing fits

# === SAVE OUTPUT ===
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(layout, f, indent=2)

placed = sum(1 for row in layout for val in row if val != -1)
print(f"✅ Boards placed: {placed} / {GRID_SIZE * GRID_SIZE}")
print(f"✅ Layout saved to {output_file}")
