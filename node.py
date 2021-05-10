import math
import copy
import random
import numpy as np

class Node:
    def __init__(self,type,logical_position,board_status,col_position,row_status,parent,move,player1_score,player2_score,is_player2):
        #the move that lead to the this node
        self.type = type
        self.logical_position = copy.deepcopy(logical_position)
        #the the current board position of the parent
        self.col_status = copy.deepcopy(col_position)
        self.row_status = copy.deepcopy(row_status)
        self.board_status = copy.deepcopy(board_status)
        #this node win and visits
        self.wins = 0
        self.visits = 0
        # all the children for this node
        self.children = []
        self.parent = parent
        # the total move count after making the move that lead to this state
        self.move_count = move
        # player1 and player2 of the parents board state
        self.player1_score = copy.copy(player1_score)
        self.player2_score = copy.copy(player2_score)
        # the player that made the move that lead to this node
        self.is_player2 = copy.copy(is_player2)
        self.won_turn = False
        if(not self.type == "none"):
            self.update_board_score()

        # IN PROGRESS
        # self.untried_actions = set_untried_actions()


    #internal update
    def update_board_score(self):
        r = self.logical_position[0]
        c = self.logical_position[1]
        if c < 3 and r < 3:
            self.board_status[c][r] += 1
            if(self.board_status[c][r] == 4):
                self.won_turn = True
                if (self.is_player2):
                    self.player2_score += 1
                else:
                    self.player1_score += 1
        if self.type == 'row':
            self.row_status[c][r] = 1
            if c >= 1:
                self.board_status[c-1][r] += 1
                # if the four edges are filed in
                if(self.board_status[c-1][r] == 4):
                    self.won_turn = True
                    if (self.is_player2):
                        self.player2_score += 1
                    else:
                        self.player1_score += 1

        elif self.type == 'col':
            self.col_status[c][r] = 1
            if r >= 1:
                self.board_status[c][r-1] += 1
                if(self.board_status[c][r-1] == 4):
                    self.won_turn = True
                    if (self.is_player2):
                        self.player2_score += 1
                    else:
                        self.player1_score += 1

    #return if it is player2 turn next
    def is_player2_next(self):
        if self.won_turn:
            return self.is_player2
        else:
            return not self.is_player2

    #check if the current is a is_leaf(true for leaf and false for non leaf)
    def is_leaf(self):
        if(len(self.children) == 0 ):
            return True
        else:
            return False
    #is the node terminal(true for terminal and false for non terminal)
    def is_terminal(self):
        if(self.move_count == 24):
            return True
        else:
            return False
    #return 1 if player 1 won the state or 2 if player 2 won the state or 0 (if 24 moves has not been reached)
    def winner(self):
        if (not self.is_terminal()):
            return 0

        if (self.player1_score > self.player2_score):

            return 1
        else:
            return 2
    #return utc:
    def utc(self,exploration_paramter):
        if (self.visits == 0):
            return 1000 + random.randint(0,1000) #1000 being our undefined value
        return (self.wins/self.visits) + exploration_paramter*(np.sqrt(np.log(self.parent.visits)/self.visits))

    # IN PROGRESS:
    # determines if a node is fully expanded, meaning all its successors are in tree policy
    # returns true if fully expanded, false otherwise
    # def can_expand(self):
    #     return len(self.possible_children ) == 0

    # def set_untried_actions(self):
    #     if self.untried_actions is None:
    #         self.untried_actions = self.get_random_successor(self, True)
    #     return self.untried_actions
