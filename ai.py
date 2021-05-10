# ai.py
# A.I. that plays Dots and Boxes
import random
import mcts
import time
import node
import numpy as np
class AI:
# Decides on a move, given the current game state.
    def __init__(self):
        self.mcts = mcts.MCTS(np.sqrt(2))

    def move(self,board_status, row_status, col_status,move_counter,player1_score,player2_score, is_player2):
    # Placeholder algorithm that just chooses some empty edge. Replace with MCTS.
        move = self.heuristic(board_status,row_status,col_status,move_counter)
        if (not move[0] == "none"):
            return move

        #3 second timer
        timeout = time.time() + 10
        # parameters for node: self,type,logical_position,board_status,col_position,row_status,parent,move,player1_score,player2_score,is_player2
        root_node = node.Node("none",[-1,-1],board_status,col_status,row_status,None,move_counter,player1_score,player2_score,is_player2)
        i = 0
        while(True):
            if time.time() > timeout:
                break
            i += 1
            chosen_node = self.mcts.select(root_node)
            simulation_node = self.mcts.expansion(chosen_node)
            self.mcts.run_simulation(simulation_node)

        #time to choose node
        return self.mcts.choose_move(root_node)


    # A.I. that makes random moves, for testing purposes
    def dummy_ai(self,board_status, row_status, col_status):
        moves = []
        for i in range(4):
            for j in range(3):
                if row_status[i][j] == 0:
                    moves.append(('row', [j,i]))
        for i in range(3):
            for j in range(4):
                if col_status[i][j] == 0:
                    moves.append(('col', [j,i]))
                return moves[random.randint(0, len(moves) - 1)]

    # return either (type, logical position) ("col",[0,1]) or "("none",[-1,-1])"
    def heuristic(self,board_status, row_status, col_status, move):
        inital_move_set = [("col",[1,1]),("col",[0,1]),("col",[2,1]),("col",[3,1]),("row",[1,1]),("row",[1,0]),("row",[1,2]),("row",[1,3])]
        if (move >= 2 ):
            return ("none",[-1,-1])

        if(move == 0):
            return random.choice(inital_move_set)

        if(move == 1):
            if (col_status[1][1] == 1 or col_status[1][0] == 1):
                return ("row",[0,1])
            if (col_status[1][2] == 1 or col_status[1][3] == 1):
                return ("row",[2,2])
            if (row_status[1][1] == 1 or row_status[0][1] == 1):
                return ("col",[2,0])
            if (row_status[2][1] == 1 or row_status[3][1] == 1):
                return ("col",[1,2])

            return ("none",[-1,-1])
