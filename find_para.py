import json
import os
from distutils.file_util import write_file

from smargo.loader import dump_json, go_board_init, go_info_init
from smargo.model import MCTS
from smargo.visualize import plot_go_board, plot_go_file, print_go_tree

root_path = "smargo_dataset_30/json/"
file_list = sorted([_ for _ in os.listdir(root_path) if _.endswith(".json")])[:4]

init_playouts = [3000, 800, 1000, 2000]
etas = [10, 10, 5]

for init_playout in init_playouts:
    for eta in etas:
        total_num = 0
        total_correct_num = 0
        for file in file_list:
            file_path = os.path.join(root_path, file)
            print(file_path)
            state = go_board_init(file_path)
            ground_truth, size = go_info_init(file_path)
            num_moves = len(ground_truth)

            mcts = MCTS(c_puct=eta)
            mcts.train(state, init_playout=init_playout, num_moves=num_moves)

            # print_go_tree(mcts.root, max_depth=4)

            print([{x[0]: x[1].n_visits} for x in mcts.root.children.items()])
            print([{x[0]: x[1].Q} for x in mcts.root.children.items()])

            # visualize all moves
            moves = mcts.result_moves(num_moves=num_moves)

            total_num += len(moves)
            correct_num = 0
            for move in moves:
                if move in ground_truth:
                    total_correct_num += 1
                    correct_num += 1

            result_file = open("result.txt", "a")
            result_file.writelines(str(file_path) + "\n")
            result_file.writelines(str(moves) + "\n")
            result_file.writelines(str(ground_truth) + "\n")
            result_file.writelines(
                str(correct_num) + " " + str(len(moves)) + " " + str(len(ground_truth)) + "\n"
            )
            result_file.close()

            board_info = json.load(open(file_path))
            board_size = board_info["board_size"][0]
            board_info["predict"] = [
                [int(move // board_size), int(move % board_size)] for move in moves
            ]
            dump_json(board_info, file_path)

        print(total_correct_num)
        print(total_num)

        result_file = open("result.txt", "a")
        result_file.writelines("\n" + str(eta) + "," + str(init_playout) + "\n")
        result_file.writelines(str(total_correct_num) + "," + str(total_num) + "\n\n")
        result_file.close()
        print(eta, init_playout, "accuracy is", total_correct_num / total_num)
