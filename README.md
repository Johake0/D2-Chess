# D2-Chess

Simple chess app reflecting the mechanics of the live event going on in Destiny 2 as of April 30th 2025

Forked from https://github.com/Alvii-1/D2-Chess to add mapping, adjacency relation, and plotting scripts. 


To run this:
1) Create a data folder in the root of the project then put the data.tsv file that you can get from https://tjl.co/queens-gambit-arg/ into said data folder.

2) Create a folder named json_outputs in the root of the project.

3) Go to the terminal and cd into the scripts folder.

4) run `python convert_tsv_to_json.py` in the terminal. This will generate json files that will be put into the >all_boards_json_final folder of all of the chess boards that have been verified.

5) run `python extract_edge_profiles.py` in the terminal. This will generate an edge profiles json file that will generate the edges for each of the boards.

6) run `python generate_adjacency_map.py` in the terminal. This will generate an adjacency map which shows which boards share a border based on border and color.

7) run `python make_layout_64x64_multi_seed_color_grouped.py` in the terminal. This will generate a json file that will be read by the board renderer which will plot down the boards and their adjacent boards.

8) run `python render_full_64x64.py` in the terminal. This will render the board as a png image using matplotlib, and will output the picture of the board in /pictures.

You can use the original app by loading the index.html file in your browser or by visiting the Web App: https://alvii-1.github.io/D2-Chess/
