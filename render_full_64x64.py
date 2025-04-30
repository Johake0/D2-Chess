import json
import os
import matplotlib.pyplot as plt

# === CONFIG ===
json_dir = "all_boards_json_final"
layout_file = "layout_64x64_multi_seed_color_validated.json"
output_image = "puzzle_render_64x64_combined_color.png"

# === SETTINGS ===
grid_size = 64
board_size = 8
canvas_size = grid_size * board_size

color_map = {
    "black": "#1e1e1e",
    "white": "#f0f0f0",
    "light": "#b0b0b0",
    "dark": "#555555",
    "lightred": "#e06666",
    "darkred": "#8b0000",
    "lightgray": "#d3d3d3",  # ← Add this
    "darkgray": "#555555",   # ← And this
    "orange": "#ffa500",     # ← Also include fallback
}

text_color_map = {"white": "white", "black": "black"}

# === LOAD LAYOUT ===
with open(layout_file, "r") as f:
    layout = json.load(f)

# === LOAD BOARDS ===
board_jsons = {}
for fname in os.listdir(json_dir):
    if fname.startswith("board_") and fname.endswith(".json"):
        try:
            board_id = int(fname.split("_")[1].split(".")[0])
            with open(os.path.join(json_dir, fname), "r") as f:
                board_jsons[board_id] = json.load(f)
        except Exception as e:
            print(f"Error loading {fname}: {e}")

# === RENDER ===
fig, ax = plt.subplots(figsize=(40, 40))
ax.set_xlim(0, canvas_size)
ax.set_ylim(0, canvas_size)
ax.set_aspect("equal")
ax.invert_yaxis()
ax.set_xticks([])
ax.set_yticks([])

for board_r in range(grid_size):
    for board_c in range(grid_size):
        board_id = layout[board_r][board_c]
        if board_id == -1 or board_id not in board_jsons:
            continue
        for sq in board_jsons[board_id]:
            local_r, local_c = sq["row"], sq["col"]
            piece = sq["piece"]
            color = sq["color"]
            global_r = board_r * board_size + local_r
            global_c = board_c * board_size + local_c
            fill = color_map.get(color, "#ff00ff")
            ax.add_patch(
                plt.Rectangle((global_c, global_r), 1, 1, facecolor=fill, edgecolor=fill)
            )
            if piece:
                is_black = piece in "♜♞♝♛♚♟"
                font_color = text_color_map["white"] if is_black else text_color_map["black"]
                ax.text(
                    global_c + 0.5,
                    global_r + 0.65,
                    piece,
                    ha="center",
                    va="center",
                    fontsize=5.5,
                    color=font_color
                )

plt.tight_layout()
plt.savefig(output_image, dpi=300)
plt.close()
print(f"Rendered image saved to {output_image}")
