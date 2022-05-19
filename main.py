import json
import os

from smargo.loader import dump_json, go_board_init, go_info_init
from smargo.model import MCTS
from smargo.visualize import plot_go_board, plot_go_file

root_path = "smargo_50/json/"
file_list = sorted([_ for _ in os.listdir(root_path) if _.endswith(".json")])[:]

total_num = 0
total_correct_num = 0
total_correct_num_top3 = 0

result_file_name = "output/result_top3.txt"

for file in file_list[:2]:
    file_path = os.path.join(root_path, file)
    print(file_path)
    state = go_board_init(file_path)
    ground_truth, size = go_info_init(file_path)
    if size > 9:
        continue
    elif size == 7:
        init_playout = 2000
    elif size == 9:
        init_playout = 3000

    num_moves = len(ground_truth)

    mcts = MCTS(c_puct=5)
    mcts.train(state, init_playout=init_playout, num_moves=num_moves)

    # print_go_tree(mcts.root, max_depth=4)

    print([{x[0]: x[1].n_visits} for x in mcts.root.children.items()])
    print([{x[0]: x[1].Q} for x in mcts.root.children.items()])

    # visualize all moves
    moves = mcts.result_moves(num_moves=num_moves)
    moves_top3 = mcts.result_moves_top3(num_moves=num_moves)
    print(file, "moves:", moves)
    print(file, "ground truth:", ground_truth)

    plot_go_board(state, moves, export_path=file_path.rstrip(".json") + "_pred")
    plot_go_file(file_path, export_path=file_path.rstrip(".json") + "_truth")

    total_num += len(moves)
    correct_num = 0
    correct_num_top3 = 0
    for idx, move in enumerate(moves):
        if move in ground_truth:
            total_correct_num += 1
            correct_num += 1
        if ground_truth[idx] in moves_top3[idx]:
            total_correct_num_top3 += 1
            correct_num_top3 += 1

    result_file = open(result_file_name, "a")
    result_str = "\n".join([str(x) for x in [file_path, ground_truth, moves, moves_top3]]) + "\n"
    result_str += (
        " ".join([str(x) for x in [correct_num, correct_num_top3, len(moves), len(ground_truth)]])
        + "\n"
    )
    result_file.writelines(result_str)
    result_file.close()

    board_info = json.load(open(file_path))
    board_size = board_info["board_size"][0]
    board_info["predict"] = [[int(move // board_size), int(move % board_size)] for move in moves]
    dump_json(board_info, file_path)

print(total_correct_num)
print(total_correct_num_top3)
print(total_num)

result_file = open(result_file_name, "a")
result_file.writelines(
    "\n" + str(total_correct_num) + "," + str(total_correct_num_top3) + "," + str(total_num) + "\n"
)
result_file.close()
print("accuracy is", total_correct_num / total_num)
