import matplotlib.pyplot as plt
import numpy as np
from ..structure.constant import *
from ..structure.board import if_win, next_state
from typing import List
import os
import shutil


def _plot_board_state(
    state: List,
    moves: List, 
    save_path: str
) -> None:
    board_size = state.shape[1]

    black_list, white_list = [], []
    for init_point in zip(*np.where(state[BLACK_CHAN] == 1)):
        black_list.append([init_point[1], board_size-init_point[0]-1])
    for init_point in zip(*np.where(state[WHITE_CHAN] == 1)):
        white_list.append([init_point[1], board_size-init_point[0]-1])
    _plot_go_figure(board_size, black_list, white_list, save_path+'original.png')


    for idx, move in enumerate(moves):
        next_state(state, move)
        black_list, white_list = [], []
        for init_point in zip(*np.where(state[BLACK_CHAN] == 1)):
            black_list.append([init_point[1], board_size-init_point[0]-1])
        for init_point in zip(*np.where(state[WHITE_CHAN] == 1)):
            white_list.append([init_point[1], board_size-init_point[0]-1])
        _plot_go_figure(board_size, black_list, white_list, save_path+'step'+str(idx+1)+'.png')


def _plot_go_figure(board_size, black_list, white_list, save_path):
    fig = plt.figure(figsize=[8,8])
    fig.patch.set_facecolor((1,1,.8))
    ax = fig.add_subplot(111)
    for x in range(board_size):
        ax.plot([x, x], [0,board_size-1], 'k')
    for y in range(7):
        ax.plot([0, board_size-1], [y,y], 'k')
    ax.set_position([0,0,1,1])
    ax.set_axis_off()
    ax.set_xlim(-1,board_size)
    ax.set_ylim(-1,board_size)

    for point in black_list:
        ax.plot(*point,'o',markersize=50, markeredgecolor=(.5,.5,.5), markerfacecolor='k', markeredgewidth=2)
    for point in white_list:
        ax.plot(*point,'o',markersize=50, markeredgecolor=(0,0,0), markerfacecolor='w', markeredgewidth=2)
    plt.savefig(save_path)


def plot_go_state(state: np.array, moves: List) -> None:
    dir_name = 'data/current_state/'
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)
    else:
        shutil.rmtree(dir_name)
        os.mkdir(dir_name)
    _plot_board_state(state, moves, dir_name)
