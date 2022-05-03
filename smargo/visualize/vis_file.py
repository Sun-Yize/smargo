import matplotlib.pyplot as plt
import numpy as np
import json
from typing import List
import os


def _plot_board(
    state: List,
    moves: List, 
    turn: int, 
    board_size: int,
    save_path: str):
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
    state = np.array(state)
    moves = np.array(moves)

    for init_point in zip(*np.where(state == 0)):
        ax.plot(init_point[1], board_size-init_point[0]-1,'o',markersize=50, markeredgecolor=(.5,.5,.5), markerfacecolor='k', markeredgewidth=2)
    
    for init_point in zip(*np.where(state == 1)):
        ax.plot(init_point[1], board_size-init_point[0]-1,'o',markersize=50, markeredgecolor=(0,0,0), markerfacecolor='w', markeredgewidth=2)
    
    plt.savefig(save_path+'original.png')

    for idx, move in enumerate(moves):
        policy = {
            (0, 0): [(.5,.5,.5), 'k'],
            (0, 1): [(0,0,0), 'w'],
            (1, 0): [(0,0,0), 'w'],
            (1, 1): [(.5,.5,.5), 'k'],
        }
        colorset = policy[(turn, idx%2)]
        ax.plot(move[1], board_size-move[0]-1,'o',markersize=50, markeredgecolor=colorset[0], markerfacecolor=colorset[1], markeredgewidth=2)
        plt.savefig(save_path+'step'+str(idx+1)+'.png')

def plot_go_file(file_path: str):
    board_info = json.load(open(file_path))
    dir_name = 'data/'+file_path.strip('.json').split('/')[-1]+'/'
    if os.path.exists(dir_name):
        raise FileExistsError('Already has a folder!')
    else:
        os.mkdir(dir_name)
    _plot_board(board_info['state'], board_info['ground_truth'], board_info['turn'], board_info['board_size'][0], dir_name)
