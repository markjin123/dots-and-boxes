# Base GUI derived from https://github.com/aqeelanwar/Dots-and-Boxes

import ai
import sys

from tkinter import *
import numpy as np

size_of_board = 600
number_of_dots = 4
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
dot_color = '#7BC043'
line_color = '#7BC043'
player1_color = '#0492CF'
player1_color_light = '#67B0CF'
player2_color = '#EE4035'
player2_color_light = '#EE7E77'
Green_color = '#7BC043'
dot_width = 0.25*size_of_board/number_of_dots
edge_width = 0.1*size_of_board/number_of_dots
distance_between_dots = size_of_board / (number_of_dots)

class Dots_and_Boxes():
    # ------------------------------------------------------------------
    # Initialization functions
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title('Dots_and_Boxes')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        self.player1_starts = True
        self.ai = ai.AI()
        self.play_again()

    def play_again(self):
        self.refresh_board()
        # board_status is (3,3) matrix representing the boxes, domain:[0,4]
        #   4 => all sides of a box are drawn
        self.board_status = np.zeros(shape=(number_of_dots - 1, number_of_dots - 1))

        # row_status is (4,3) matrix: if there is a horizontal line on m-th row
        #                             array([0,0,0],
        #                                   [0,0,0],
        #                                   [0,0,0]
        #                                   [0,0,0])
        self.row_status = np.zeros(shape=(number_of_dots, number_of_dots - 1))
        # col_status is (3,4) matrix:: if there is a vertical line on n-th col
        self.col_status = np.zeros(shape=(number_of_dots - 1, number_of_dots))

        self.player1_score = 0
        self.player2_score = 0
        self.box_captured = False
        self.num_moves = 0

        # Input from user in form of clicks
        self.player1_turn = self.player1_starts
        self.player1_starts = not self.player1_starts
        self.reset_board = False
        self.turntext_handle = []

        self.already_marked_boxes = []
        self.display_turn_text()

        # If player 2 (AI) goes first
        while not self.player1_turn:
            self.initiate_ai_move()

    def mainloop(self):
        self.window.mainloop()

    # ------------------------------------------------------------------
    # Logical Functions:
    # The modules required to carry out game logic
    # ------------------------------------------------------------------

    def is_grid_occupied(self, logical_position, type):
        r = logical_position[0]
        c = logical_position[1]
        occupied = True

        if type == 'row' and self.row_status[c][r] == 0:
            occupied = False
        if type == 'col' and self.col_status[c][r] == 0:
            occupied = False

        return occupied

    # Check if a line exist in the grid_position and return the logical position of the click
    # Return:
    # logical_position: return the logical position, for example, [0,1] where 0 is the row in the matrix and 1 in the col in the matrix
    # type: either col or row or false to indicted if the line being checked is a col or row line or it is not a line at all.
    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        position = (grid_position-distance_between_dots/4)//(distance_between_dots/2)

        type = False
        logical_position = []
        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            r = int((position[0]-1)//2)
            c = int(position[1]//2)
            logical_position = [r, c]
            type = 'row'
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            c = int((position[1] - 1) // 2)
            r = int(position[0] // 2)
            logical_position = [r, c]
            type = 'col'

        return logical_position, type

    def mark_box(self):
        boxes = np.argwhere(self.board_status == 4)
        for box in boxes:
            if list(box) not in self.already_marked_boxes and list(box) !=[]:

                self.box_captured = True
                self.already_marked_boxes.append(list(box))

                if self.player1_turn:
                    self.player1_score += 1
                    color = player1_color_light
                else:
                    self.player2_score += 1
                    color = player2_color_light

                self.shade_box(box, color)

    def update_board(self, type, logical_position):
        r = logical_position[0]
        c = logical_position[1]
        val = 1

        if c < (number_of_dots-1) and r < (number_of_dots-1):
            self.board_status[c][r] += val

        if type == 'row':
            self.row_status[c][r] = 1
            if c >= 1:
                self.board_status[c-1][r] += val

        elif type == 'col':
            self.col_status[c][r] = 1
            if r >= 1:
                self.board_status[c][r-1] += val

    def is_gameover(self):
        return (self.row_status == 1).all() and (self.col_status == 1).all()

    # ------------------------------------------------------------------
    # Drawing Functions:
    # The modules required to draw required game based object on canvas
    # ------------------------------------------------------------------

    def make_edge(self, type, logical_position):
        if type == 'row':
            start_x = distance_between_dots/2 + logical_position[0]*distance_between_dots
            end_x = start_x+distance_between_dots
            start_y = distance_between_dots/2 + logical_position[1]*distance_between_dots
            end_y = start_y
        elif type == 'col':
            start_y = distance_between_dots / 2 + logical_position[1] * distance_between_dots
            end_y = start_y + distance_between_dots
            start_x = distance_between_dots / 2 + logical_position[0] * distance_between_dots
            end_x = start_x

        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=line_color, width=edge_width)

    def display_gameover(self):
        player1_score = self.player1_score
        player2_score = self.player2_score

        if player1_score > player2_score:
            # Player 1 wins
            text = 'Winner: Player 1'
            color = player1_color
            print('p1 wins\n')
        elif player2_score > player1_score:
            # Player 2 wins
            text = 'Winner: Player 2'
            color = player2_color
            print('p2 wins\n')
        else:
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(size_of_board / 2, size_of_board / 3, font="cmr 50 bold", fill=color, text=text)

        score_text = 'Scores\n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="cmr 40 bold", fill=Green_color,
                                text=score_text)

        score_text = 'Player 1 : ' + str(player1_score) + '\n'
        score_text += 'Player 2 : ' + str(player2_score) + '\n'
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="cmr 30 bold", fill=Green_color,
                                text=score_text)
        self.reset_board = True

        score_text = 'Click to play again\n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    def refresh_board(self):
        for i in range(number_of_dots):
            x = i*distance_between_dots+distance_between_dots/2
            self.canvas.create_line(x, distance_between_dots/2, x,
                                    size_of_board-distance_between_dots/2,
                                    fill='gray', dash = (2, 2))
            self.canvas.create_line(distance_between_dots/2, x,
                                    size_of_board-distance_between_dots/2, x,
                                    fill='gray', dash=(2, 2))

        for i in range(number_of_dots):
            for j in range(number_of_dots):
                start_x = i*distance_between_dots+distance_between_dots/2
                end_x = j*distance_between_dots+distance_between_dots/2
                self.canvas.create_oval(start_x-dot_width/2, end_x-dot_width/2, start_x+dot_width/2,
                                        end_x+dot_width/2, fill=dot_color,
                                        outline=dot_color)

    def display_turn_text(self):
        text = 'Next turn: '
        if self.player1_turn:
            text += 'Player1'
            color = player1_color
        else:
            text += 'Player2'
            color = player2_color

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(size_of_board - 5*len(text),
                                                       size_of_board-distance_between_dots/8,
                                                       font="cmr 15 bold", text=text, fill=color)


    def shade_box(self, box, color):
        start_x = distance_between_dots / 2 + box[1] * distance_between_dots + edge_width/2
        start_y = distance_between_dots / 2 + box[0] * distance_between_dots + edge_width/2
        end_x = start_x + distance_between_dots - edge_width
        end_y = start_y + distance_between_dots - edge_width
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline='')

    def display_turn_text(self):
        text = 'Next turn: '
        if self.player1_turn:
            text += 'Player1'
            color = player1_color
        else:
            text += 'Player2'
            color = player2_color

        self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(size_of_board - 5*len(text),
                                                       size_of_board-distance_between_dots/8,
                                                       font="cmr 15 bold",text=text, fill=color)

    def click(self, event):
        if not self.reset_board and self.player1_turn:
            grid_position = [event.x, event.y]
            logical_position, valid_input = self.convert_grid_to_logical_position(grid_position)
            if valid_input and not self.is_grid_occupied(logical_position, valid_input):
                self.initiate_move(valid_input, logical_position)

            while not self.player1_turn and not self.reset_board:
                self.initiate_ai_move()

        elif self.reset_board:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

    def initiate_ai_move(self):
        valid_input, logical_position = self.ai.move(self.board_status, self.row_status, self.col_status, self.num_moves,self.player1_score,self.player2_score, not self.player1_turn)
        if valid_input and not self.is_grid_occupied(logical_position, valid_input):
            self.initiate_move(valid_input, logical_position)
        else:
            sys.exit('ERROR: A.I. selected filled edge')

    def initiate_move(self, m_type, logical_position):
        self.update_board(m_type, logical_position)
        self.make_edge(m_type, logical_position)
        self.mark_box()
        self.refresh_board()
        self.num_moves += 1

        if self.player1_turn:
            player = 'p1'
        else:
            player = 'p2'

        if m_type == 'row':
            print(player+': row_status['+str(logical_position[0])+']['+str(logical_position[1])+'] (Move ' + str(self.num_moves) + ')')
        else:
            print(player+': col_status['+str(logical_position[1])+']['+str(logical_position[0])+'] (Move ' + str(self.num_moves) + ')')

        if self.box_captured:
            self.box_captured = not self.box_captured
        else:
            self.player1_turn = not self.player1_turn

        if self.is_gameover():
            self.display_gameover()
        else:
            self.display_turn_text()

        self.canvas.update()

game_instance = Dots_and_Boxes()
game_instance.mainloop()
