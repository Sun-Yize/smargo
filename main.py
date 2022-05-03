# from visualize import plot_go_file

# plot_go_file('data/tsumego_000001.json')

from smargo.loader import go_board_init
from smargo.model import MCTS

import time

state = go_board_init('data/tsumego_000002.json')
mcts = MCTS(c_puct=5, n_playout=3000, total_play=20)
start_time = time.clock()
move = mcts.get_move(state)
print([{x[0]: x[1].n_visits} for x in mcts.root.children.items()])
