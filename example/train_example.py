from smargo.loader import go_board_init, go_info_init
from smargo.model import MCTS
from smargo.visualize import plot_go_board, print_go_tree

# prepare go board data
file_path = "smargo_30/json/tsumego_000000.json"
state = go_board_init(file_path)
ground_truth, size = go_info_init(file_path)
num_moves = len(ground_truth)

# train monte carlo search tree
mcts = MCTS(c_puct=5)
mcts.train(state, init_playout=200, num_moves=num_moves)

# print total tree
print_go_tree(mcts.root, max_depth=2)

# print possibility
print([{x[0]: x[1].n_visits} for x in mcts.root.children.items()])
print([{x[0]: x[1].Q} for x in mcts.root.children.items()])

# visualize all moves
moves = mcts.result_moves(num_moves=num_moves)
print(moves)
plot_go_board(state, moves)
