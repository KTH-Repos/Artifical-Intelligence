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
        score_A, score_B = state.get_player_scores()
        return score_A - score_B  
            
    def minimax(self, node, player, depth, alpha, beta):
        children = node.compute_and_get_children()
        if len(children) == 0 or depth == 0:
            return self.heuristic_function(node.state)
        else:
            if player == 0:
                bestPossible = math.inf*(-1)
                for child in children:
                    bestPossible = max(bestPossible, self.minimax(child, 1, depth-1, alpha, beta))
                    alpha = max(alpha, bestPossible)
                    if beta <= alpha:
                        break
                #print('bestpossible for max is '+ str(bestPossible))
                return bestPossible
            
            else:
                bestPossible = math.inf
                for child in children:
                    bestPossible = min(bestPossible, self.minimax(child, 0, depth-1, alpha, beta))
                    beta = min(beta, bestPossible)
                    if beta <= alpha:
                        break
                #print('bestpossible for min is '+ str(bestPossible))
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

        # EDIT THIS METHOD TO RETURN BEST NEXT POSSIBLE MODE USING MINIMAX ###

        # NOTE: Don't forget to initialize the children of the current node
        #       with its compute_and_get_children() method!
        #children_of_node = initial_tree_node.compute_and_get_children()
        first_level = initial_tree_node.compute_and_get_children()
        alpha = math.inf*(-1)
        beta = math.inf
        bestChild = None
        bestResult = alpha
        for child in first_level:
            #print("hej!!!!!")
            result = self.minimax(child, 0, 2, alpha, beta)
            #print("hejjjj2!!!!!") #TODO Fastnar ppå första barnet. Minimax måste fixas
            if result > bestResult:
                bestResult = result
                bestChild = child
        print(ACTION_TO_STR[bestChild.move])
        return ACTION_TO_STR[bestChild.move] 