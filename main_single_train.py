import json
import os

from smargo.loader import dump_json, go_board_init, go_info_init
from smargo.model import MCTS
from smargo.visualize import plot_go_board, plot_go_file, print_go_tree

root_path = "smargo_50/json/"
file_list = ["tsumego_000000.json"]

total_num = 0
total_correct_num = 0

for file in file_list:
    file_path = os.path.join(root_path, file)
    print(file_path)
    state = go_board_init(file_path)
    ground_truth, size = go_info_init(file_path)
    if size > 9:
        continue
    elif size == 7:
        init_playout = 800
    elif size == 9:
        init_playout = 300

    num_moves = len(ground_truth)

    mcts = MCTS(c_puct=5)
    mcts.train(state, init_playout=init_playout, num_moves=8)

    # print_go_tree(mcts.root, max_depth=4)

    print([{x[0]: x[1].n_visits} for x in mcts.root.children.items()])
    print([{x[0]: x[1].Q} for x in mcts.root.children.items()])

    # visualize all moves
    moves = mcts.result_moves()
    print(file, "moves:", moves)
    print(file, "ground truth:", ground_truth)

    plot_go_board(state, moves, export_path=file_path.rstrip(".json") + "_pred")
    plot_go_file(file_path, export_path=file_path.rstrip(".json") + "_truth")

    total_num += len(moves)
    correct_num = 0
    for move in moves:
        if move in ground_truth:
            total_correct_num += 1
            correct_num += 1
    board_info = json.load(open(file_path))
    board_size = board_info["board_size"][0]
    board_info["predict"] = [[int(move // board_size), int(move % board_size)] for move in moves]
    dump_json(board_info, file_path)
