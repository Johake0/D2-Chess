import os
import json

os.makedirs("json_outputs", exist_ok=True)

# Define input directory (adjust if needed)
json_dir = "all_boards_json"
output_file = "json_outputs/edge_profiles.json"

# Output structure: board_id -> { top: [...], bottom: [...], left: [...], right: [...] }
edge_profiles = {}

# Helper function to load a board and extract edges
def extract_edges(board_data):
    top = [None] * 8
    bottom = [None] * 8
    left = [None] * 8
    right = [None] * 8

    for square in board_data:
        row = square["row"]
        col = square["col"]
        piece = square.get("piece")

        if row == 0:
            top[col] = piece
        if row == 7:
            bottom[col] = piece
        if col == 0:
            left[row] = piece
        if col == 7:
            right[row] = piece

    return {
        "top": top,
        "bottom": bottom,
        "left": left,
        "right": right
    }

# Iterate through all board files
for fname in os.listdir(json_dir):
    if fname.startswith("board_") and fname.endswith(".json"):
        try:
            board_id = int(fname.split("_")[1].split(".")[0])
        except (IndexError, ValueError):
            print(f"Skipping file not matching board_### format: {fname}")
            continue

        with open(os.path.join(json_dir, fname), "r", encoding="utf-8") as f:
            board_data = json.load(f)
            edge_profiles[board_id] = extract_edges(board_data)

# Save to disk
with open(output_file, "w", encoding="utf-8") as out:
    json.dump(edge_profiles, out, indent=2)

print(f"Edge profiles written to {output_file}")
