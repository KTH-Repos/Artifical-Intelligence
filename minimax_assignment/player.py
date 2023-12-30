#!/usr/bin/env python3
import math
import time
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
        total_score = state.player_scores[0] - state.player_scores[1]
    
        likelihood = 0
        for i in state.fish_positions:
            fish_positions = state.fish_positions[i]
            hook_positions = state.hook_positions[0]

            #calculate manhattan distance between hook and every uncaught fish
            y = abs(fish_positions[1] - hook_positions[1])
            delta_x = abs(fish_positions[0] - hook_positions[0])
            x = min(delta_x, 20 - delta_x)
            distance = x + y

            fish_score = state.fish_scores[i]
            
            if fish_score > 0:
                if distance == 0:
                    return float('inf')
            
                likelihood = max(likelihood, fish_score * 1/distance)

        return 3 * total_score + likelihood

    
    def hash_state(self, state):
        fish_positions = state.get_fish_positions()
        fish_scores = state.get_fish_scores()

        pos_dic = {str(pos[0]) + str(pos[1]): score for pos, score in zip(fish_positions.items(), fish_scores.items())}

        return str(state.get_hook_positions()) + str(pos_dic)


    def alpha_beta(self, node, player, depth, alpha, beta, transposition_table, initial_time):
        if time.time() - initial_time > 0.05:
            raise TimeoutError
        
        else:
            key = self.hash_state(node.state)
            if key in transposition_table and transposition_table[key][0] >= depth:
                return transposition_table[key][1]  #return heuristic value for that node
            children = node.compute_and_get_children()
            children.sort(key=lambda child: self.heuristic_function(child.state), reverse=True)
            if len(children) == 0 or depth == 0:
                bestPossible = self.heuristic_function(node.state)
                  
            elif player == 0:
                bestPossible = float('-inf')
                for child in children:
                    bestPossible = max(bestPossible, self.alpha_beta(child, 1, depth-1, alpha, beta, transposition_table, initial_time))
                    alpha = max(alpha, bestPossible)
                    if beta <= alpha:
                        break
            else:
                bestPossible = float('inf')
                for child in children:
                    bestPossible = min(bestPossible, self.alpha_beta(child, 0, depth-1, alpha, beta, transposition_table, initial_time))
                    beta = min(beta, bestPossible)
                    if beta <= alpha:
                        break
            key = self.hash_state(node.state)
            transposition_table.update({key:[depth, bestPossible]})
        return bestPossible   
    
    def search_best_move(self, node, depth, start_time, transposition_table):
        alpha = float('-inf')
        beta = float('inf')
        
        children = node.compute_and_get_children()
        children_scores = []
        
        for child in children:
            score = self.alpha_beta(child, 1, depth, alpha, beta, transposition_table, start_time)
            children_scores.append(score)
            
        best_score_index = children_scores.index(max(children_scores))
        return children[best_score_index].move
        
    def search_best_next_move(self, initial_tree_node):
        """
        Use minimax (and extensions) to find best possible next move for player 0 (green boat)
        :param initial_tree_node: Initial game tree node
        :type initial_tree_node: game_tree.Node
            (see the Node class in game_tree.py for more information!)
        :return: either "stay", "left", "right", "up" or "down"
        :rtype: str
        """       
        start_time = time.time()
        transposition_table = dict()
        timeout = False
        depth = 0
        best_move = 0
        
        while not timeout:
            try:
                result = self.search_best_move(initial_tree_node, depth, start_time, transposition_table)
                depth += 1
                best_move = result
            except:
                timeout = True
        return ACTION_TO_STR[best_move] 