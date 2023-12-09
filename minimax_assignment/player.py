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
        
    def heuristic_function_gar(self, state):
        # Fish Proximity
        fish_positions = state.get_fish_positions()
        hook_positions = state.get_hook_positions()
        current_player = state.get_player()
        fish_values = state.get_fish_scores()

        fish_proximity_score = 0
        for fish_number, pos in fish_positions.items():
            distance_to_hook = abs(pos[0] - hook_positions[current_player][0]) + abs(pos[1] - hook_positions[current_player][1])
            fish_proximity_score += (1 / (distance_to_hook + 1)) * fish_values[fish_number]

        # Score Differentials
        player_score, opponent_score = state.get_player_scores()
        score_differential = player_score - opponent_score

        # Relative Boat Positions
        relative_position_score = 0
        if current_player == 0:
            relative_position_score = hook_positions[0][0] - hook_positions[1][0]
        else:
            relative_position_score = hook_positions[1][0] - hook_positions[0][0]

        # Encourage boat movement towards areas with more fish
        movement_score = 0
        if not state.get_caught()[current_player]:
            for fish_number, pos in fish_positions.items():
                movement_score += (1 / (abs(pos[0] - hook_positions[current_player][0]) + 1)) * fish_values[fish_number]

        # Combine the components with appropriate weights
        heuristic_score = 0.3 * fish_proximity_score + 0.3 * score_differential + 0.2 * relative_position_score + 0.2 * movement_score

        return heuristic_score
        
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
   
    
    def hash_state(self, state):
        scorex, scorey = state.get_player_scores()
        caughtx, caughty = state.get_caught()
        hook_pos = state.get_hook_positions()
        pos_1 = hook_pos[0]
        pos_2 = hook_pos[1]
        
        return str(scorex)+str(scorey)+str(caughtx)+str(caughty)+str(pos_1)+str(pos_2)

    def minimax(self, node, player, depth, alpha, beta, transposition_table, initial_time):
        
        if time.time() - initial_time > 0.05:
            raise TimeoutError
        
        else:
            key = self.hash_state(node.state)
            if key in transposition_table and transposition_table[key][0] >= depth:
                return transposition_table[key][1]  #return heuristic value for that node
            children = node.compute_and_get_children()
            if len(children) == 0 or depth == 0:
                bestPossible = self.heuristic_function(node.state)
                  
            elif player == 0:
                bestPossible = float('inf')*(-1)
                for child in children:
                    bestPossible = max(bestPossible, self.minimax(child, 1, depth-1, alpha, beta, transposition_table, initial_time))
                    alpha = max(alpha, bestPossible)
                    if beta <= alpha:
                        break
            else:
                bestPossible = float('inf')
                for child in children:
                    bestPossible = min(bestPossible, self.minimax(child, 0, depth-1, alpha, beta, transposition_table, initial_time))
                    beta = min(beta, bestPossible)
                    if beta <= alpha:
                        break
            key = self.hash_state(node.state)
            transposition_table.update({key:[depth, bestPossible]})
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
        alpha = float('inf')*(-1)
        beta = float('inf')
        depth = 0
        start_time = time.time()
        transposition_table = {}
        bestChild = None
        bestResult = float('inf')*(-1)
        timeout = False
        move = None
        
        while not timeout:
            try:
                for child in first_level:
                    result = self.minimax(child, 0, depth, alpha, beta, transposition_table, start_time)
                    if result > bestResult:
                        bestResult = result
                        bestChild = child
                depth += 1
            except:
                timeout = True
        #print(ACTION_TO_STR[bestChild.move])
        if bestChild is not None:
            move = ACTION_TO_STR[bestChild.move] 
        return move