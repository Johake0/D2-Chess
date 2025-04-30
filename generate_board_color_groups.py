import os
import json

# Folder with your board JSONs
board_dir = "all_boards_json_final"
output_file = "board_color_groups.json"

# Define color groups
RED_COLORS = {"lightred", "darkred"}
GRAY_COLORS = {"lightgray", "darkgray"}

color_group_map = {}

for fname in os.listdir(board_dir):
    if not fname.startswith("board_") or not fname.endswith(".json"):
        continue
    try:
        board_id = int(fname.split("_")[1].split(".")[0])
    except (IndexError, ValueError):
        print(f"Skipping invalid file: {fname}")
        continue

    with open(os.path.join(board_dir, fname), "r", encoding="utf-8") as f:
        board = json.load(f)

    # Look for first non-edge square
    interior_color = None
    for square in board:
        r, c = square["row"], square["col"]
        if r != 0 and r != 7 and c != 0 and c != 7:
            interior_color = square["color"]
            break

    if interior_color in RED_COLORS:
        color_group = "red"
    elif interior_color in GRAY_COLORS:
        color_group = "gray"
    else:
        color_group = "unknown"

    color_group_map[board_id] = color_group

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(color_group_map, f, indent=2)

print(f"✅ Saved color groups to {output_file}")
