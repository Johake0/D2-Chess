import json
import os
import matplotlib.pyplot as plt
import numpy as np

# === CONFIG ===
layout_file = "layout_32x32_from_TR.json"
json_dir = "all_boards_json"
output_image = "render_32x32_quadrant.png"

# === SETTINGS ===
board_size = 8
text_color_map = {"white": "white", "black": "black"}
color_map = {
    "black": "#1e1e1e",
    "white": "#f0f0f0",
    "light": "#b0b0b0",
    "dark": "#555555",
    "darkred": "#8b0000",
    "lightred": "#e06666",
}

# === LOAD LAYOUT ===
with open(layout_file, "r") as f:
    layout = json.load(f)

grid_rows = len(layout)
grid_cols = len(layout[0])
canvas_size = board_size * max(grid_rows, grid_cols)

# === LOAD BOARDS ===
board_jsons = {}
for fname in os.listdir(json_dir):
    if fname.startswith("board_") and fname.endswith(".json"):
        try:
            board_id = int(fname.split("_")[1].split(".")[0])
            with open(os.path.join(json_dir, fname), "r") as f:
                board_jsons[board_id] = json.load(f)
        except:
            continue

# === RENDER SETUP ===
fig, ax = plt.subplots(figsize=(24, 24))
ax.set_xlim(0, board_size * grid_cols)
ax.set_ylim(0, board_size * grid_rows)
ax.set_aspect("equal")
ax.invert_yaxis()
ax.set_xticks([])
ax.set_yticks([])

# === DRAW EACH SQUARE ===
for board_r in range(grid_rows):
    for board_c in range(grid_cols):
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
                is_black_piece = piece in "♜♞♝♛♚♟"
                font_color = text_color_map["white"] if is_black_piece else text_color_map["black"]
                ax.text(
                    global_c + 0.5,
                    global_r + 0.65,
                    piece,
                    ha="center",
                    va="center",
                    fontsize=5.5,
                    color=font_color
                )

# === SAVE OUTPUT ===
plt.tight_layout()
plt.savefig(output_image, dpi=300)
plt.close()
print(f"Saved quadrant to {output_image}")
