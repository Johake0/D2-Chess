import os
import json

project_root = os.path.dirname(os.path.dirname(__file__))

# === CONFIG ===
edge_profiles_file = os.path.join(project_root, "json_outputs/edge_profiles.json")
output_file = os.path.join(project_root, "json_outputs/board_adjacency.json")

# === LOAD EDGE PROFILES ===
with open(edge_profiles_file, "r", encoding="utf-8") as f:
    edge_profiles = json.load(f)

# === MATCHING FUNCTION ===
def edges_match(edge1, edge2):
    return edge1 == edge2

# === BUILD ADJACENCY MAP ===
adjacency_map = {}

for id_a, edges_a in edge_profiles.items():
    id_a = str(id_a)
    adjacency_map[id_a] = {"top": [], "bottom": [], "left": [], "right": []}
    for id_b, edges_b in edge_profiles.items():
        id_b = str(id_b)
        if id_a == id_b:
            continue
        if edges_match(edges_a["right"], edges_b["left"]):
            adjacency_map[id_a]["right"].append(id_b)
        if edges_match(edges_a["left"], edges_b["right"]):
            adjacency_map[id_a]["left"].append(id_b)
        if edges_match(edges_a["top"], edges_b["bottom"]):
            adjacency_map[id_a]["top"].append(id_b)
        if edges_match(edges_a["bottom"], edges_b["top"]):
            adjacency_map[id_a]["bottom"].append(id_b)

# === SAVE OUTPUT ===
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(adjacency_map, f, indent=2)

print(f"Board adjacency map written to {output_file}")
