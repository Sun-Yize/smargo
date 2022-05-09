from smargo.visualize import plot_go_board, plot_go_file, print_go_tree

root_path = "data/test/"
file_list = ["tsumego_000002.json"]

for file in file_list:
    file_path = root_path + file
    plot_go_file(file_path, export_path=file_path.strip(".json") + "_truth")
