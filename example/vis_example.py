from smargo.visualize import plot_go_board, plot_go_file, print_go_tree
from smargo.loader import dump_json, go_board_init, go_info_init


file_path = 'smargo_30/json/tsumego_000008.json'
file_path = 'output/temp.json'
print(file_path)
state = go_board_init(file_path)
plot_go_file(file_path, export_path="output/temp_truth", bgc=False)
