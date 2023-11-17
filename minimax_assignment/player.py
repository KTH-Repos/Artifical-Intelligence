#!/usr/bin/env python3
import random
import math

from fishing_game_core.game_tree import Node
from fishing_game_core.player_utils import PlayerController
from fishing_game_core.shared import ACTION_TO_STR


class PlayerControllerHuman(PlayerController):
    def player_loop(self):
        """
        Function that generates the loop of the game. In each iteration
        the human plays through the keyboard and send
        this to the game through the sender. Then it receives an
        update of the game through receiver, with this it computes the
        next movement.
        :return:
        """

        while True:
            # send message to game that you are ready
            msg = self.receiver()
            if msg["game_over"]:
                return


class PlayerControllerMinimax(PlayerController):

    def __init__(self):
        super(PlayerControllerMinimax, self).__init__()

    def player_loop(self):
        """
        Main loop for the minimax next move search.
        :return:
        """

        # Generate first message (Do not remove this line!)
        first_msg = self.receiver()

        while True:
            msg = self.receiver()

            # Create the root node of the game tree
            node = Node(message=msg, player=0)

            # Possible next moves: "stay", "left", "right", "up", "down"
            best_move = self.search_best_next_move(initial_tree_node=node)

            # Execute next action
            self.sender({"action": best_move, "search_time": None})
        
    def heuristic_function(self, state):
        hook_pos = state.get_hook_positions()
        green_hook_pos = next(iter(hook_pos.values()))
        fish_pos = state.get_fish_positions()
        fish_values = state.get_fish_scores()
        score_A, score_B = state.get_player_scores()
        big_score = math.inf * (-1)
        for fish in fish_pos:
            fish_coordinates = fish_pos[fish]
            if abs(green_hook_pos[0] - fish_coordinates[0]) <= 3 and abs(green_hook_pos[1] - fish_coordinates[1]) <= 3:
                # Nu har vi avgränsat området till ett visst antal fiskar som är närliggande. Nästa steg är att kolla på deras scores:
                fish_score = fish_values[fish]

                if fish_score > big_score and fish_score > 0:
                    big_score = fish_score

        score_diff = score_A - score_B

        return max(score_diff, big_score)
    

    # def heuristic_function(self, state):
    #     #fish_pos = state.get_fish_positions()
    #     fish_values = state.get_fish_scores()

    #     big_score = math.inf * (-1)
    #     for fish in fish_values:
    #         fish_score = fish_values[fish]
    #         if fish_score > big_score and fish_score > 0:
    #             big_score = fish_score

    #     return big_score


    def minimax(self, node, player, depth, alpha, beta):
        children = node.compute_and_get_children()
        if len(children) == 0 or depth == 0:
            return self.heuristic_function(node.state)
        elif player == 0:
            bestPossible = math.inf*(-1)
            for child in children:
                bestPossible = max(bestPossible, self.minimax(child, 1, depth-1, alpha, beta))
                alpha = max(alpha, bestPossible)
                if beta <= alpha:
                    break
        else:
            bestPossible = math.inf
            for child in children:
                bestPossible = min(bestPossible, self.minimax(child, 0, depth-1, alpha, beta))
                beta = min(beta, bestPossible)
                if beta <= alpha:
                    break
        return bestPossible
        

    def search_best_next_move(self, initial_tree_node):
        """
        Use minimax (and extensions) to find best possible next move for player 0 (green boat)
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """

        first_level = initial_tree_node.compute_and_get_children()
        alpha = math.inf*(-1)
        beta = math.inf
        bestChild = None
        bestResult = alpha
        for child in first_level:
            result = self.minimax(child, 0, 2, alpha, beta)
            if result > bestResult:
                bestResult = result
                bestChild = child
        #print(ACTION_TO_STR[bestChild.move])
        return ACTION_TO_STR[bestChild.move] 