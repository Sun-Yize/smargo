from smargo.loader import go_board_init
from smargo.structure.board import compute_valid_moves, next_state
from smargo.visualize import plot_go_state

# train monte carlo search tree
state = go_board_init("data/tsumego_000002.json")
plot_go_state(state, save_path="img1.png")
next_state(state, 6)
plot_go_state(state, save_path="img1.png")
next_state(state, 5)
plot_go_state(state, save_path="img1.png")
next_state(state, 10)
plot_go_state(state, save_path="img1.png")
next_state(state, 11)
plot_go_state(state, save_path="img1.png")
