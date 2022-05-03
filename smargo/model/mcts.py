import numpy as np
import copy
from operator import itemgetter
from ..structure.board import *


class TreeNode:
    def __init__(self, parent, prior_p):
        self.parent = parent
        self.children = {}
        self.n_visits = 0
        self.Q = 0
        self.U = 0
        self.P = prior_p

    def select(self, c_puct):
        return max(
            self.children.items(), key=lambda act_node: act_node[1].get_value(c_puct)
        )

    def expand(self, action_priors):
        for action, prob in action_priors:
            if action not in self.children:
                self.children[action] = TreeNode(self, prob)

    def update(self, leaf_value):
        self.n_visits += 1
        self.Q += 1.0 * (leaf_value - self.Q) / self.n_visits

    def update_recursive(self, leaf_value):
        if self.parent:
            self.parent.update_recursive(-leaf_value)
        self.update(leaf_value)

    def get_value(self, c_puct):
        self.U = c_puct * self.P * np.sqrt(self.parent.n_visits) / (1 + self.n_visits)
        return self.Q + self.U

    def is_leaf(self):
        return self.children == {}

    def is_root(self):
        return self.parent is None


class MCTS:
    def __init__(self, c_puct=5, n_playout=10000, total_play=20):
        self.root = TreeNode(None, 1.0)
        self.c_puct = c_puct
        self.n_playout = n_playout
        self.total_play = total_play

    def policy_value_fn(self, game_state_simulator):
        availables = valid_moves(game_state_simulator)
        action_probs = np.random.rand(len(availables))
        return zip(availables, action_probs)

    def playout(self, simulate_game_state):
        node = self.root
        depth = 0
        while True:
            if node.is_leaf():
                break
            depth += 1
            action, node = node.select(self.c_puct)
            next_state(simulate_game_state, action)
        if depth < self.total_play and not if_end(simulate_game_state):
            availables = valid_moves(simulate_game_state)
            action_probs = np.ones(len(availables)) / len(availables)
            node.expand(zip(availables, action_probs))
            leaf_value = self.evaluate_rollout(simulate_game_state, depth=depth)
        else:
            leaf_value = 1.0 if turn(simulate_game_state) == 0 else -1.0
        node.update_recursive(leaf_value)

    def get_move(self, game):
        for i in range(self.n_playout):
            game_state = copy.deepcopy(game)
            self.playout(game_state)
        print(
            max(self.root.children.items(), key=lambda act_node: act_node[1].n_visits)
        )
        return max(
            self.root.children.items(), key=lambda act_node: act_node[1].n_visits
        )[0]

    def update_with_move(self, last_move):
        if last_move in self.root.children:
            self.root = self.root.children[last_move]
            self.root.parent = None
        else:
            self.root = TreeNode(None, 1.0)

    def evaluate_rollout(self, simulate_game_state, depth):
        game_state_copy = copy.deepcopy(simulate_game_state)
        player = turn(game_state_copy)
        for _ in range(self.total_play - depth):
            winner = if_win(game_state_copy)
            if winner:
                return 1.0 if player == 1 else -1.0
            if if_end(game_state_copy):
                return 1.0 if player == 0 else -1.0
            depth += 1
            action_probs = self.policy_value_fn(game_state_copy)
            max_action = max(action_probs, key=itemgetter(1))[0]
            next_state(game_state_copy, max_action)
        else:
            return 1.0 if player == 0 else -1.0

    def update_with_move(self, state, num):
        move_list = []
        for _ in range(num):
            if self.root.children != {}:
                move = max(
                    self.root.children.items(),
                    key=lambda act_node: act_node[1].n_visits,
                )[0]
                move_list.append(move)
                self.root = self.root.children[move]
                self.root.parent = None
            else:
                break
        return move_list
