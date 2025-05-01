import csv
import json
import os

piece_map = {
    "K": {"white": "♔", "black": "♚"},
    "Q": {"white": "♕", "black": "♛"},
    "R": {"white": "♖", "black": "♜"},
    "B": {"white": "♗", "black": "♝"},
    "N": {"white": "♘", "black": "♞"},
    "P": {"white": "♙", "black": "♟"},
}

COLOR_PALETTE = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "lightgray": (211, 211, 211),
    "darkgray": (85, 85, 85),
    "lightred": (255, 102, 102),
    "darkred": (139, 0, 0),
    "orange": (255, 165, 0),  # fallback for unknown colors
}

DEFAULT_COLOR = "orange"

def normalize_color_name(raw):
    return raw.strip().lower().replace(" ", "")

with open("data-verified.tsv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        board_id = row["frequency"]
        piece_string = row["board"]
        interior_color_raw = row["fill"]
        has_qr = row["hasQR"]

        # Skip if QR value is 1
        if has_qr == "1":
            continue

        interior_color = normalize_color_name(interior_color_raw)
        if interior_color not in COLOR_PALETTE:
            print(f"Warning: Unknown interior color '{interior_color_raw}'. Defaulting to {DEFAULT_COLOR}.")
            interior_color = DEFAULT_COLOR

        squares = piece_string.split(',')
        board = []

        for i, sq in enumerate(squares):
            row_idx, col_idx = divmod(i, 8)
            is_edge = row_idx == 0 or row_idx == 7 or col_idx == 0 or col_idx == 7

            if sq:
                piece_letter = sq[0].upper()
                color = "white" if sq[1].lower() == "w" else "black"
                piece = piece_map.get(piece_letter, {}).get(color)
            else:
                piece = None

            square_color = "black" if is_edge else interior_color

            board.append({
                "row": row_idx,
                "col": col_idx,
                "piece": piece,
                "color": square_color
            })

        out_dir = "all_boards_json"
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, f"board_{board_id}.json")
        with open(path, "w", encoding="utf-8") as f_out:
            json.dump(board, f_out, indent=2)
