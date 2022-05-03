from smargo.loader import go_board_init
from smargo.model import MCTS
from smargo.visualize import plot_go_state, print_go_tree

# train monte carlo search tree
state = go_board_init("data/tsumego_000002.json")
mcts = MCTS(c_puct=20, n_playout=3000)
move = mcts.get_move(state)
print("move is: ", move)

# # print total tree
# print_go_tree(mcts.root, max_depth=2)

# # print possibility
# print([{x[0]: x[1].n_visits} for x in mcts.root.children.items()])
# print([{x[0]: x[1].Q} for x in mcts.root.children.items()])

# visualize all moves
moves = mcts.result_moves()
plot_go_state(state, moves)
