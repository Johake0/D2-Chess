import json
import os
import matplotlib.pyplot as plt
import numpy as np

# === CONFIG ===
json_dir = "all_boards_json"
layout_file = "board_layout_matrix.json"
output_image = "puzzle_render_full.png"

# === SETTINGS ===
grid_size = 64
board_size = 8
square_size = 1
canvas_size = grid_size * board_size

color_map = {
    "black": "#1e1e1e",
    "white": "#f0f0f0",
    "light": "#b0b0b0",
    "dark": "#555555",
    "darkred": "#8b0000",
    "lightred": "#e06666",
}
text_color_map = {
    "black": "black",
    "white": "white"
}

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

# === PLOT SETUP ===
fig, ax = plt.subplots(figsize=(40, 40))
ax.set_xlim(0, canvas_size)
ax.set_ylim(0, canvas_size)
ax.set_aspect("equal")
ax.invert_yaxis()
ax.set_xticks([])
ax.set_yticks([])

# === DRAW ===
for board_r in range(grid_size):
    for board_c in range(grid_size):
        board_id = layout[board_r][board_c]
        if board_id == -1 or board_id not in board_jsons:
            continue

        board = board_jsons[board_id]
        for square in board:
            local_r = square["row"]
            local_c = square["col"]
            piece = square["piece"]
            color = square["color"]

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
                    fontsize=6,
                    color=font_color
                )

# === SAVE ===
plt.tight_layout()
plt.savefig(output_image, dpi=300)
plt.close()
print(f"Rendered puzzle saved to {output_image}")
