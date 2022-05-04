import json
from smargo.loader import go_board_init, dump_json
from smargo.model import MCTS
from smargo.visualize import plot_go_board, print_go_tree, plot_go_file

root_path = "data/test/"
# file_list = ["tsumego_000002.json"]
file_list = ["tsumego_000001.json"]

for file in file_list:
    file_path = root_path+file
    state = go_board_init(file_path)
    mcts = MCTS(c_puct=30)
    mcts.train(state, init_playout=5000, iter_playout=500)

    print([{x[0]: x[1].n_visits} for x in mcts.root.children.items()])
    print([{x[0]: x[1].Q} for x in mcts.root.children.items()])

    # visualize all moves
    moves = mcts.result_moves()
    print(file, "moves:", moves)
    plot_go_board(state, moves, export_path=file_path.strip('.json')+"_pred")
    plot_go_file(file_path, export_path=file_path.strip('.json')+"_truth")

    board_info = json.load(open(file_path))
    board_size = board_info['board_size'][0]
    board_info["predict"] = [[int(move//board_size), int(move%board_size)] for move in moves]
    dump_json(board_info, file_path)
