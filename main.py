# from visualize import plot_go_file

# plot_go_file('data/tsumego_000001.json')

from smargo.loader import go_board_init
from smargo.model import MCTS
from smargo.visualize import plot_go_state, print_go_tree

import time

state = go_board_init('data/tsumego_000002.json')
mcts = MCTS(c_puct=20, n_playout=300, total_play=10)
# start_time = time.process_time()
move = mcts.get_move(state)
# print_go_tree(mcts.root)
# print([{x[0]: x[1].n_visits} for x in mcts.root.children.items()])
# print([{x[0]: x[1].Q} for x in mcts.root.children.items()])
moves = mcts.result_moves(10)
# moves = [6, 10, 0, 11, 5, 15]
# print(moves)
plot_go_state(state, moves)
