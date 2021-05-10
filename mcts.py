import datetime
import math
import random
import node
import numpy as np

class MCTS:
    def __init__(self, exploration_paramter):
        self.exploration_parameter = exploration_paramter
        self.totaltimes = 0

    def select(self, curr):
        # curr: curret (head) node
        q = curr
        path = []

        # chosen_node = q

        while not q.is_leaf():

            # determine largest UCT among children
            self.totaltimes += 1
            arr_uct = [
                c.utc(self.exploration_parameter)
                for c in q.children
            ]

            q = q.children[np.argmax(arr_uct)]
        return q

    # Append all possible successors to the current state and return a successor at random
    def expansion(self, leaf):
        return self.get_random_successor(leaf, True)

    # Appends and returns a random succesor to the node
    # my_node: The node of interest
    # appendAll: Option to append all possible successors to the node
    def get_random_successor(self, my_node, appendAll):
        row_status = my_node.row_status
        col_status = my_node.col_status
        successors = []

        #todo: update board/row/col_status, update move_count, maybe update scores
        for i in range(4):
            for j in range(3):
                if row_status[i][j] == 0:
                    successors.append(node.Node('row',                   # type
                                            [j,i],                  # logicalposition
                                            my_node.board_status,
                                            my_node.col_status,
                                            my_node.row_status,
                                            my_node,                # parent
                                            my_node.move_count + 1,
                                            my_node.player1_score,
                                            my_node.player2_score,
                                            my_node.is_player2_next()))    # player 2 next turn

        for i in range(3):
            for j in range(4):
                if col_status[i][j] == 0:
                    successors.append(node.Node('col',
                                            [j,i],
                                            my_node.board_status,
                                            my_node.col_status,
                                            my_node.row_status,
                                            my_node,
                                            my_node.move_count + 1,
                                            my_node.player1_score,
                                            my_node.player2_score,
                                            my_node.is_player2_next()))

        if (len(successors) == 0):
            return my_node
        chosen = successors[random.randint(0, len(successors) - 1)]

        if appendAll:
            for scsr in successors:
                my_node.children.append(scsr)

        return chosen


    # runs simulation until it reaches a terminal state, invokes backpropogate accordingly
    # node: node from selection/expansion to run simulation on
    def run_simulation(self, node):
        curr = node
        while(True):
            if curr.is_terminal() and curr.winner() == 1: # at terminal state, player 1 (opponent) won
                self.backpropogate(False, node)
                break
            elif curr.is_terminal() and curr.winner() == 2: # at terminal state, player 2 (AI) won
                self.backpropogate(True, node)
                break
            else:
                # keep running simulation
                curr = self.get_random_successor(curr,False) # get_random_successor determines next move
            # self.nodes.append(next_nodes) # dont need to keep track of encountered nodes


    # upon reaching end of game, all positions visited are incremented, and maybe win-count incremented
    # won: if the AI won or not
    # end_game_node: node from reaching terminal state in simulation
    def backpropogate(self, won, end_game_node):
        bp = end_game_node # backpropogate working node: bp
        if (won):

            while bp is not None:
                bp.visits += 1
                if(bp.is_player2):
                    bp.wins += 1
                bp = bp.parent # root_node.parent = None
        else:

            while bp is not None:
                bp.visits += 1
                if(not bp.is_player2):
                    bp.wins += 1
                bp = bp.parent

    #choose the move

    def choose_move(self,node):
        arr_uct = [
            c.utc(self.exploration_parameter)
            for c in node.children
        ]
        cur_node = node.children[np.argmax(arr_uct)]
        return (cur_node.type, cur_node.logical_position)
