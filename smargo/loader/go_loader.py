import json

import numpy as np

from ..structure.board import compute_valid_moves
from ..structure.constant import *


def go_board_init(board_path):
    board_info = json.load(open(board_path))
    board = np.array(board_info["state"])
    state = np.zeros(
        (
            CHAN,
            board_info["board_size"][0],
            board_info["board_size"][1],
        )
    )
    state[BLACK_CHAN][np.where(board == 0)] = 1
    state[WHITE_CHAN][np.where(board == 1)] = 1
    state[ORIGIN_WHITE_CHAN] = state[WHITE_CHAN]
    state[TURN_CHAN] = board_info["turn"]
    state[VALID_CHAN] = compute_valid_moves(state, board_info["turn"])
    return state
