from tkinter import Frame, Label, CENTER, messagebox, Toplevel, Button

import numpy as np
import math


####################### INITIALIZATION ##################################
#For the display
EDGE_LENGTH = 400
CELL_PAD = 10

#For the game 
POSSIBLE_MOVES_COUNT = 4 #Up, down, left and right
CELL_COUNT = 4 #Numbers of cells on the diagonal
NUMBER_OF_SQUARES = CELL_COUNT * CELL_COUNT
NEW_TILE_DISTRIBUTION = np.array([2, 2, 2, 2, 2, 2, 2, 2 ,2, 4])

#For control
UP_KEY = "'w'"
DOWN_KEY = "'s'"
LEFT_KEY = "'a'"
RIGHT_KEY= "'d'"
AI_PLAY_KEY = "'p'"

#For AI control 
NUMBER_TO_WIN = 2048
NUMBER_OF_MOVES = 4 


######################## GAME FUNCTION ###################################
'''The code below will initialize the game and place a 2 tile at a ramdom place'''
def initialize_game():
    board = np.zeros((NUMBER_OF_SQUARES), dtype="int")
    initial_twos = np.random.default_rng().choice(NUMBER_OF_SQUARES, 2, replace=False)
    board[initial_twos] = 2
    board = board.reshape((CELL_COUNT, CELL_COUNT))
    return board

'''The function below will remove all the tiles to the rigth of the board and check if any move has been done. Else it will return false for move_done'''
def push_board_right(board):
    new = np.zeros((CELL_COUNT, CELL_COUNT), dtype="int")
    move_done = False
    for row in range(CELL_COUNT):
        count = CELL_COUNT - 1
        for col in range(CELL_COUNT - 1, -1, -1):
            if board[row][col] != 0:
                new[row][count] = board[row][col]
                if col != count:
                    move_done = True
                count -= 1
    return (new, move_done)

'''Merge the tiles together and return a board that is not compressed'''
def merge_elements(board):
    score = 0
    merge_done = False
    for row in range(CELL_COUNT):
        for col in range(CELL_COUNT - 1, 0, -1):
            if board[row][col] == board[row][col-1] and board[row][col] != 0:
                board[row][col] *= 2
                score += board[row][col]
                board[row][col-1] = 0
                merge_done = True
    return (board, merge_done, score)

'''For all of the moves below the board will be rotated so the push_board_right can be applied. 
Afterwards the merge_element will be applied an a second push is need to compress the tiles. 
lastly mode_made is used to check if the mode is valid, either tiles should be merged or some tiles so change its location for the move to be valid'''
def move_up(board):
    rotated_board = np.rot90(board, -1)
    pushed_board, has_pushed = push_board_right(rotated_board)
    merged_board, has_merged, score = merge_elements(pushed_board)
    second_pushed_board, _ = push_board_right(merged_board)
    rotated_back_board = np.rot90(second_pushed_board)
    move_made = has_pushed or has_merged
    return rotated_back_board, move_made, score

    
def move_down(board):
    board = np.rot90(board)
    board, has_pushed = push_board_right(board)
    board, has_merged, score = merge_elements(board)
    board, _ = push_board_right(board)
    board = np.rot90(board, -1)
    move_made = has_pushed or has_merged
    return board, move_made, score


def move_left(board):
    board = np.rot90(board, 2)
    board, has_pushed = push_board_right(board)
    board, has_merged, score = merge_elements(board)
    board, _ = push_board_right(board)
    board = np.rot90(board, -2)
    move_made = has_pushed or has_merged
    return board, move_made, score


def move_right(board):
    board, has_pushed = push_board_right(board)
    board, has_merged, score = merge_elements(board)
    board, _ = push_board_right(board)
    move_made = has_pushed or has_merged
    return board, move_made, score

'''The function checks for valid moves if it returns false then the game is over'''
def fixed_move(board):
    move_order = [move_left, move_up, move_down, move_right]
    for func in move_order:
        new_board, move_made, _ = func(board)
        if move_made:
            return new_board, True
    return board, False


def random_move(board):
    move_made = False
    move_order = [move_right, move_up, move_down, move_left]
    while not move_made and len(move_order) > 0:
        move_index = np.random.randint(0, len(move_order))
        move = move_order[move_index]
        board, move_made, score  = move(board)
        if move_made:
            return board, True, score
        move_order.pop(move_index)
    return board, False, score


def add_new_tile(board):
    tile_value = NEW_TILE_DISTRIBUTION[np.random.randint(0, len(NEW_TILE_DISTRIBUTION))]
    tile_row_options, tile_col_options = np.nonzero(np.logical_not(board))
    tile_loc = np.random.randint(0, len(tile_row_options))
    board[tile_row_options[tile_loc], tile_col_options[tile_loc]] = tile_value
    return board


def check_for_win(board):
    return NUMBER_TO_WIN in board


######################### COLOR FOR GAME DISPLAY ############################################
LABEL_FONT = ("Verdana", 40, "bold")

GAME_COLOR = "#a39489"

EMPTY_COLOR = "#c2b3a9"

TILE_COLORS = {
    2: "#fcefe6",
    4: "#f2e8cb",
    8: "#f5b682",
    16: "#f29446",
    32: "#ff775c",
    64: "#e64c2e",
    128: "#ede291",
    256: "#fce130",
    512: "#ffdb4a",
    1024: "#f0b922",
    2048: "#fad74d"
}

LABEL_COLORS ={
    2: "#695c57",
    4: "#695c57",
    8: "#ffffff",
    16: "#ffffff",
    32: "#ffffff",
    64: "#ffffff",
    128: "#ffffff",
    256: "#ffffff",
    512: "#ffffff",
    1024: "#ffffff",
    2048: "#ffffff"
}

######################## AI GAME #########################################

""" WEIGHT = np.array([[2**15, 2**14, 2**13, 2**12], 
                    [2**8, 2**9, 2**10, 2**11], 
                    [2**7, 2**6, 2**5, 2**4], 
                    [2**0, 2**1, 2**2, 2**3]]) """

WEIGHT = np.array([[2**7, 2**6, 2**5, 2**4], 
                    [2**6, 2**5, 2**4, 2**3], 
                    [2**5, 2**4, 2**3, 2**2], 
                    [2**4, 2**3, 2**2, 2**1]])

""" WEIGHT = np.array([[4**1, 4**2, 4**3, 4**4], 
                    [4**2, 4**3, 4**4, 4**5], 
                    [4**3, 4**4, 4**5, 4**6], 
                    [4**4, 4**5, 4**6, 4**7]])
 """
def heuristic(board):
    h = 0
    for i in range(CELL_COUNT):
        for j in range(CELL_COUNT):
            h += board[i,j] * WEIGHT[i,j]
    return h   

def expectimax(board, depth, move):
    
    if depth < 0:
        print('\t in heuristic')
        return heuristic(board), move

    if depth % 2 == 0:
        if np.sum((board==0).astype('int')) == 0:
            print('in sum')
            total_score = expectimax(new_board, depth - 1, move)
        else:
            print('in tile')
            empty_cells = np.argwhere(board == 0)
            total_score = 0
            for tile_value, weight in [(2, 0.9), (4, 0.1)]:
                for empty_cell in empty_cells:
                    row, col = empty_cell
                    new_board = np.copy(board)
                    new_board[row, col] = tile_value
                    new_score, _ = expectimax(new_board, depth - 1, move)
                    total_score += 1.* weight * new_score /len(empty_cells)

        return total_score, move
    
    elif depth % 2 == 1:  
        print('in player')
        max_score = -math.inf
        for move_player in [move_left, move_up, move_down, move_right]:
            new_board, move_made, _ = move_player(np.copy(board))
            print(np.copy(board))
            print(move_made, move_player)
            print(new_board)
            if move_made:
                print(f'\move made: t{move}')
                new_score, _ = expectimax(np.copy(new_board), depth - 1, move_player)
                if new_score > max_score:
                    max_score = new_score
                    print(f'\t\t {max_score}')
                    move = move_player
        return max_score, move


def find_move(board, depth):
    max_value = -float('inf')  
    next_move = None

    for move in [move_left, move_up, move_down, move_right]:
        board_copy = np.copy(board)
        board_new, move_made, _ = move(board_copy)

        if move_made == True:
            print(f'Expectimax to check {move}')
            print(board_new)
            value, _ = expectimax(np.copy(board_new), depth, move)
            print(f'{move}, {value}')
            if value > max_value:
                max_value = value
                next_move = move 

    if max_value == -float('inf'):
        for move in [move_left, move_up, move_down, move_right]:
            board_copy = np.copy(board)
            board_new, move_made, _ = move(board_copy)
            h = heuristic(board_new)
            if h > max_value:
                max_value = h
                next_move = move

    print(f'The return move was {next_move}')

    return next_move




######################### GAME DISPLAY #############################################################


class Display(Frame):
    def __init__(self):
        Frame.__init__(self)

        self.grid()
        self.build_buttons()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_press)

        self.commands = {UP_KEY: move_up, 
                         DOWN_KEY: move_down,
                         LEFT_KEY: move_left, 
                         RIGHT_KEY: move_right,
                         }
        
        self.grid_cells = []
        self.build_grid()
        self.init_matrix()
        self.draw_grid_cells()

        self.mainloop()

    def build_grid(self):
        background = Frame(self, bg=GAME_COLOR,
                           width=EDGE_LENGTH, height=EDGE_LENGTH)
        background.grid()

        for row in range(CELL_COUNT):
            grid_row = []
            for col in range(CELL_COUNT):
                cell = Frame(background, bg=EMPTY_COLOR,
                             width=EDGE_LENGTH / CELL_COUNT,
                             height=EDGE_LENGTH / CELL_COUNT)
                cell.grid(row=row, column=col, padx=CELL_PAD,
                          pady=CELL_PAD)
                t = Label(master=cell, text="",
                          bg=EMPTY_COLOR,
                          justify=CENTER, font=LABEL_FONT, width=5, height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def init_matrix(self):
        self.matrix = initialize_game()

    def draw_grid_cells(self):
        for row in range(CELL_COUNT):
            for col in range(CELL_COUNT):
                tile_value = self.matrix[row][col]
                if not tile_value:
                    self.grid_cells[row][col].configure(
                        text="", bg=EMPTY_COLOR)
                else:
                    self.grid_cells[row][col].configure(text=str(
                        tile_value), bg=TILE_COLORS[tile_value],
                        fg=LABEL_COLORS[tile_value])
        self.update_idletasks()
    
    def build_buttons(self):
        new_game_button = Button(self, text="New Game", command=self.start_new_game)
        new_game_button.grid(row=CELL_COUNT, column=0, columnspan=2, pady=10)

        stop_button = Button(self, text="Stop", command=self.master.destroy)
        stop_button.grid(row=CELL_COUNT, column=2, columnspan=2, pady=10)
        
    def start_new_game(self):
        self.init_matrix()  
        self.draw_grid_cells()
     
    def key_press(self, event):
        key = repr(event.char)
        
        if key == AI_PLAY_KEY:
            move_count = 0
            while not check_for_win(self.matrix) and fixed_move(self.matrix)[1]:
                move = find_move(self.matrix, depth=2)
                self.matrix, _, _ = move(self.matrix)             
                self.matrix = add_new_tile(self.matrix)
                self.draw_grid_cells()
            move_count += 1

        if key in self.commands:
            self.matrix, move_made, _ = self.commands[repr(event.char)](self.matrix)
            if move_made:
                self.matrix = add_new_tile(self.matrix)
                self.draw_grid_cells()
                move_made = False
        
        if check_for_win(self.matrix):
            popup = Toplevel(self.master)
            popup.title("Game Over")
            popup.geometry("300x150")
            label = Label(popup, text=f'Congratulations! You\'ve reached {NUMBER_TO_WIN}. Game Over!')
            label.pack(pady=10)
            new_game_button = Button(popup, text="New Game", command=lambda: [self.start_new_game(), popup.destroy()])
            new_game_button.pack(pady=10)
            stop_button = Button(popup, text="Stop", command=self.master.destroy)
            stop_button.pack(pady=10)
        elif not fixed_move(self.matrix)[1]:
            popup = Toplevel(self.master)
            popup.title("Game Over")
            popup.geometry("300x150")
            label = Label(popup, text=f'Game Over! LOSSER!')
            label.pack(pady=10)
            new_game_button = Button(popup, text="New Game", command=lambda: [self.start_new_game(), popup.destroy()])
            new_game_button.pack(pady=10)
            stop_button = Button(popup, text="Stop", command=self.master.destroy)
            stop_button.pack(pady=10)


gamegrid = Display()
