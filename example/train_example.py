from smargo.loader import go_board_init
from smargo.model import MCTS
from smargo.visualize import plot_go_board, print_go_tree

# train monte carlo search tree
state = go_board_init("data/test/tsumego_000001.json")
mcts = MCTS(c_puct=30)
mcts.train(state, init_playout=2000, iter_playout=200)

# # print total tree
# print_go_tree(mcts.root, max_depth=6)

# print possibility
print([{x[0]: x[1].n_visits} for x in mcts.root.children.items()])
print([{x[0]: x[1].Q} for x in mcts.root.children.items()])

# visualize all moves
moves = mcts.result_moves()
print(moves)
plot_go_board(state, moves)
