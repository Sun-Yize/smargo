import numpy as np
from scipy import ndimage
from scipy.ndimage import measurements

from .constant import *


def next_state(state, action1d):
    board_shape = state.shape[1:]
    action2d = action1d // board_shape[0], action1d % board_shape[1]
    player = turn(state)
    ko_protect = None
    assert state[VALID_CHAN, action2d[0], action2d[1]] == 1, (
        "Invalid move",
        action2d,
        state[VALID_CHAN, :, :],
    )
    state[player, action2d[0], action2d[1]] = 1
    adj_locs, surrounded = adj_data(state, action2d, player)
    killed_groups = update_pieces(state, adj_locs, player)
    if len(killed_groups) == 1 and surrounded:
        killed_group = killed_groups[0]
        if len(killed_group) == 1:
            ko_protect = killed_group[0]
    state[VALID_CHAN] = compute_valid_moves(state, player, ko_protect)
    state[TURN_CHAN] = 1 - state[TURN_CHAN]


def update_pieces(state, adj_locs, player):
    opponent = 1 - player
    killed_groups = []
    all_pieces = np.sum(state[[BLACK_CHAN, WHITE_CHAN]], axis=0)
    empties = 1 - all_pieces
    all_opp_groups, _ = ndimage.measurements.label(state[opponent])
    all_adj_labels = all_opp_groups[adj_locs[:, 0], adj_locs[:, 1]]
    all_adj_labels = np.unique(all_adj_labels)
    for opp_group_idx in all_adj_labels[np.nonzero(all_adj_labels)]:
        opp_group = all_opp_groups == opp_group_idx
        liberties = empties * ndimage.binary_dilation(opp_group)
        if np.sum(liberties) <= 0:
            opp_group_locs = np.argwhere(opp_group)
            state[opponent, opp_group_locs[:, 0], opp_group_locs[:, 1]] = 0
            killed_groups.append(opp_group_locs)
    return killed_groups


def adj_data(state, action2d, player):
    neighbors = neighbor_deltas + action2d
    valid = (neighbors >= 0) & (neighbors < state.shape[1])
    valid = np.prod(valid, axis=1)
    neighbors = neighbors[np.nonzero(valid)]
    opp_pieces = state[1 - player]
    surrounded = (opp_pieces[neighbors[:, 0], neighbors[:, 1]] > 0).all()
    return neighbors, surrounded


# return: valid 1 invalid 0
def compute_valid_moves(state, player, ko_protect=None):
    all_pieces = np.sum(state[[BLACK_CHAN, WHITE_CHAN]], axis=0)
    empties = 1 - all_pieces
    possible_invalid_array = np.zeros(state.shape[1:])
    definite_valids_array = np.zeros(state.shape[1:])
    all_own_groups, num_own_groups = measurements.label(state[player])
    all_opp_groups, num_opp_groups = measurements.label(state[1 - player])
    expanded_own_groups = np.zeros((num_own_groups, *state.shape[1:]))
    expanded_opp_groups = np.zeros((num_opp_groups, *state.shape[1:]))
    for i in range(num_own_groups):
        expanded_own_groups[i] = all_own_groups == (i + 1)
    for i in range(num_opp_groups):
        expanded_opp_groups[i] = all_opp_groups == (i + 1)
    all_own_liberties = empties[np.newaxis] * ndimage.binary_dilation(
        expanded_own_groups, surround_struct[np.newaxis]
    )
    all_opp_liberties = empties[np.newaxis] * ndimage.binary_dilation(
        expanded_opp_groups, surround_struct[np.newaxis]
    )
    own_liberty_counts = np.sum(all_own_liberties, axis=(1, 2))
    opp_liberty_counts = np.sum(all_opp_liberties, axis=(1, 2))
    possible_invalid_array += np.sum(all_own_liberties[own_liberty_counts > 1], axis=0)
    possible_invalid_array += np.sum(all_opp_liberties[opp_liberty_counts == 1], axis=0)
    definite_valids_array += np.sum(all_own_liberties[own_liberty_counts == 1], axis=0)
    definite_valids_array += np.sum(all_opp_liberties[opp_liberty_counts > 1], axis=0)
    surrounded = (
        ndimage.convolve(all_pieces, surround_struct, mode="constant", cval=1) == 4
    )
    invalid_moves = (
        all_pieces + possible_invalid_array * (definite_valids_array == 0) * surrounded
    )

    example_board = ndimage.convolve(
        np.ones(state.shape[1:]), surround_struct, mode="constant"
    )
    black_surrounded = (
        ndimage.convolve(state[BLACK_CHAN], surround_struct, mode="constant")
        == example_board
    )
    white_surrounded = (
        ndimage.convolve(state[WHITE_CHAN], surround_struct, mode="constant")
        == example_board
    )

    if ko_protect is not None:
        invalid_moves[ko_protect[0], ko_protect[1]] = 1
    all_pieces = np.sum(state[[BLACK_CHAN, WHITE_CHAN]], axis=0)
    valid_points = ndimage.binary_dilation(all_pieces, structure=valid_surround).astype(
        all_pieces.dtype
    )
    invalid_moves += 1 - valid_points + all_pieces
    invalid_moves += black_surrounded
    invalid_moves += white_surrounded
    return 1 - (invalid_moves > 0)


def valid_moves(state):
    result = np.argwhere(state[VALID_CHAN].flatten() == 1)
    result = [x[0] for x in result]
    return result


def turn(state):
    return int(np.max(state[TURN_CHAN]))


def if_win(state):
    result = state[ORIGIN_WHITE_CHAN] * state[WHITE_CHAN]
    return True if np.sum(result) != np.sum(state[ORIGIN_WHITE_CHAN]) else False


def if_end(state):
    m, n = state.shape[1:]
    return True if np.count_nonzero(state[VALID_CHAN] == 0) == m * n else False
