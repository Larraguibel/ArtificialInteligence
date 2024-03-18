#import necessary libraries
from tkinter import Frame, Label, CENTER, messagebox, Toplevel, Button

import numpy as np
import math


####################### INITIALIZATION ##################################
# Constants for the display and game parameters
#For the display
EDGE_LENGTH = 400
CELL_PAD = 10

#For the game 
POSSIBLE_MOVES_COUNT = 4 #Up, down, left and right
NUMBER_OF_MOVES = 4 

#For control
UP_KEY = "'w'"
DOWN_KEY = "'s'"
LEFT_KEY = "'a'"
RIGHT_KEY= "'d'"
AI_PLAY_KEY = "'p'"
AI_MULTI_PLAY = "'m'"

#For AI control 
NUMBER_TO_WIN = 2048
CELL_COUNT = 4 #Numbers of cells on the diagonal
NUMBER_OF_SQUARES = CELL_COUNT * CELL_COUNT
NEW_TILE_DISTRIBUTION = np.array([2, 2, 2, 2, 2, 2, 2, 2 ,2, 4])




######################## GAME FUNCTION ###################################
'''The code below will initialize the game and place a 2 tile at a random place'''
def initialize_game():
    board = np.zeros((NUMBER_OF_SQUARES), dtype="int")
    initial_twos = np.random.default_rng().choice(NUMBER_OF_SQUARES, 2, replace=False)
    board[initial_twos] = 2
    board = board.reshape((CELL_COUNT, CELL_COUNT))
    return board

'''The function below will remove all the tiles to the right of the board and check if any move has been done. Else it will return false for move_done'''
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

'''Merge the tiles and return a board that is not compressed'''
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
    # Rotate the board 90 degrees counterclockwise to make the "up" movement
    rotated_board = np.rot90(board, -1)
    # Move tiles to the right, checking if any tiles were pushed
    pushed_board, has_pushed = push_board_right(rotated_board)
    # Merge tiles together, calculate the score obtained from merging
    merged_board, has_merged, score = merge_elements(pushed_board)
    # Push the tiles to the right again after merging
    second_pushed_board, _ = push_board_right(merged_board)
    # Rotate the board back to its original orientation
    rotated_back_board = np.rot90(second_pushed_board)
    # Check if any move (push or merge) was made
    move_made = has_pushed or has_merged
    # Return the updated board, a flag indicating if a move was made, and the score obtained
    return rotated_back_board, move_made, score


    
def move_down(board):
    # Rotate the board 90 degrees clockwise to make the "down" movement
    board = np.rot90(board)
    # Move tiles to the right, checking if any tiles were pushed
    board, has_pushed = push_board_right(board)
    # Merge tiles together, calculate the score obtained from merging
    board, has_merged, score = merge_elements(board)
    # Push the tiles to the right again after merging
    board, _ = push_board_right(board)
     # Rotate the board back to its original orientation
    board = np.rot90(board, -1)
    # Check if any move (push or merge) was made
    move_made = has_pushed or has_merged
    # Return the updated board, a flag indicating if a move was made, and the score obtained
    return board, move_made, score


def move_left(board):
   # Rotate the board 180 degrees to make the "left" movement
    board = np.rot90(board, 2)
    # Move tiles to the right, checking if any tiles were pushed
    board, has_pushed = push_board_right(board)
    # Merge tiles together, calculate the score obtained from merging
    board, has_merged, score = merge_elements(board)
    # Push the tiles to the right again after merging
    board, _ = push_board_right(board)
    # Rotate the board back to its original orientation
    board = np.rot90(board, -2)
    # Check if any move (push or merge) was made
    move_made = has_pushed or has_merged
    # Return the updated board, a flag indicating if a move was made, and the score obtained
    return board, move_made, score


def move_right(board):
    # Move tiles to the right, checking if any tiles were pushed
    board, has_pushed = push_board_right(board)
    # Merge tiles together, calculate the score obtained from merging
    board, has_merged, score = merge_elements(board)
    # Push the tiles to the right again after merging
    board, _ = push_board_right(board)
    # Check if any move (push or merge) was made
    move_made = has_pushed or has_merged
    # Return the updated board, a flag indicating if a move was made, and the score obtained
    return board, move_made, score
    

'''The function checks for valid moves if it returns false then the game is over'''
def fixed_move(board):
   # Define the order of moves to be checked
    move_order = [move_left, move_up, move_down, move_right]
    # Iterate through the moves and check if any of them are valid
    for func in move_order:
        new_board, move_made, _ = func(board)
        if move_made:
            return new_board, True  # Return the updated board and a flag indicating a valid move
    return board, False  # If no valid move is found, return the original board and a flag indicating game over


def random_move(board):
    # Initialize flag to track if a move was made
    move_made = False
    # Define the order of moves to be tried randomly
    move_order = [move_right, move_up, move_down, move_left]
    # Continue trying random moves until a valid move is made or all moves are exhausted
    while not move_made and len(move_order) > 0:
        # Select a random move from the remaining ones
        move_index = np.random.randint(0, len(move_order))
        move = move_order[move_index]
        # Apply the selected move and check if it was valid
        board, move_made, score = move(board)
        # If a valid move is found, return the updated board and a flag indicating a valid move
        if move_made:
            return board, True, score
        # Remove the used move from the list
        move_order.pop(move_index)
    # If no valid move is found, return the original board and a flag indicating no move made
    return board, False, score


def add_new_tile(board):
    # Randomly choose a tile value from the distribution
    tile_value = NEW_TILE_DISTRIBUTION[np.random.randint(0, len(NEW_TILE_DISTRIBUTION))]
    # Get the positions of empty cells on the board
    tile_row_options, tile_col_options = np.nonzero(np.logical_not(board))
    # Randomly choose an empty cell to place the new tile
    tile_loc = np.random.randint(0, len(tile_row_options))
    # Place the new tile in the selected empty cell
    board[tile_row_options[tile_loc], tile_col_options[tile_loc]] = tile_value
    # Return the updated board
    return board


def check_for_win(board):
    # Check if the winning tile value is present on the board
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
    2048: "#fad74d",
    4096: "#fad74d",
    8192: "#fad74d"
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
    2048: "#ffffff",
    4096: "#ffffff",
    8192: "#ffffff"
}

######################## AI GAME #########################################

# Define weight matrices for different heuristics
WEIGHT_SNAKE = np.array([[2**15, 2**14, 2**13, 2**12], 
                         [2**8, 2**9, 2**10, 2**11], 
                         [2**7, 2**6, 2**5, 2**4], 
                         [2**0, 2**1, 2**2, 2**3]])

WEIGHT_DIAG = np.array([[2**7, 2**6, 2**5, 2**4], 
                        [2**6, 2**5, 2**4, 2**3], 
                        [2**5, 2**4, 2**3, 2**2], 
                        [2**4, 2**3, 2**2, 2**1]])



def heuristic(board, type_hes = 'WEIGHT_SNAKE'):
    '''
    Calculate the heuristic value for a given game board.

    Parameters:
    - board: 2D array representing the game board
    - type_hes: String, either 'WEIGHT_SNAKE' or 'WEIGHT_DIAG', specifying the heuristic type

    Returns:
    - h: Heuristic value calculated based on the specified heuristic type
    '''
    # Select the appropriate weight matrix based on the heuristic type
    if type_hes == 'WEIGHT_SNAKE':
        WEIGHT = WEIGHT_SNAKE
    else:
        WEIGHT = WEIGHT_DIAG

    h = 0
    # Iterate through each cell on the board and calculate the heuristic value
    for i in range(CELL_COUNT):
        for j in range(CELL_COUNT):
            h += board[i, j] * WEIGHT[i, j]
    # Return the final heuristic value
    return h

def expectimax(board, depth, move, type_hes):
    '''
    Perform the Expectimax algorithm to evaluate possible moves and choose the best move.

    Parameters:
    - board: 2D array representing the game board
    - depth: Integer, the current depth in the search tree
    - move: Function, the move function (e.g., move_left, move_up) to be considered
    - type_hes: String, either 'WEIGHT_SNAKE' or 'WEIGHT_DIAG', specifying the heuristic type

    Returns:
    - score: The calculated score representing the desirability of the current move
    - selected_move: The selected move function for the current depth
    '''
    # Base case: if depth reaches 0 or less, return the heuristic value of the current board
    if depth < 0:
        return heuristic(board, type_hes), move
    # If it's the AI's turn to move
    if depth % 2 == 0:
        # If no empty cells are left, return the heuristic value of the current board
        if np.sum((board == 0).astype('int')) == 0:
            total_score = heuristic(board, type_hes)
        else:
            empty_cells = np.argwhere(board == 0)
            total_score = 0
            # Consider possible new tiles with their respective weights
            for tile_value, weight in [(2, 0.9), (4, 0.1)]:
                for empty_cell in empty_cells:
                    row, col = empty_cell
                    new_board = np.copy(board)
                    new_board[row, col] = tile_value
                    new_score, _ = expectimax(new_board, depth - 1, move, type_hes)
                    total_score += 1. * weight * new_score / len(empty_cells)
        return total_score, move
    # If it's the chance node's turn (opponent's turn)
    elif depth % 2 == 1:
        max_score = -math.inf
        # Iterate through all possible player moves and choose the one with the maximum score
        for move_player in [move_left, move_up, move_down, move_right]:
            new_board, move_made, _ = move_player(np.copy(board))
            if move_made:
                new_score, _ = expectimax(np.copy(new_board), depth - 1, move_player, type_hes)
                if new_score > max_score:
                    max_score = new_score
                    selected_move = move_player
        return max_score, selected_move


def find_move(board, depth, type_hes):
    '''
    Find the best move using the Expectimax algorithm.
    Parameters:
    - board: 2D array representing the game board
    - depth: Integer, the depth of the search tree for the Expectimax algorithm
    - type_hes: String, either 'WEIGHT_SNAKE' or 'WEIGHT_DIAG', specifying the heuristic type
    Returns:
    - next_move: The best move function determined by the Expectimax algorithm
    '''
    # Initialize variables to track the maximum value and the next move
    max_value = -float('inf')
    next_move = None
    # Iterate through all possible moves
    for move in [move_left, move_up, move_down, move_right]:
        # Create a copy of the board to simulate the move
        board_copy = np.copy(board)
        board_new, move_made, _ = move(board_copy)

        # If the move is valid, evaluate its value using the Expectimax algorithm
        if move_made == True:
            value, _ = expectimax(np.copy(board_new), depth, move, type_hes)
            # Update the maximum value and next move if a better move is found
            if value > max_value:
                max_value = value
                next_move = move 
    # If no valid move is found in the Expectimax algorithm, choose the move with the highest heuristic value
    if max_value == -float('inf'):
        for move in [move_left, move_up, move_down, move_right]:
            board_copy = np.copy(board)
            board_new, move_made, _ = move(board_copy)
            h = heuristic(board_new, type_hes)
            # Update the maximum value and next move if a better move is found
            if h > max_value:
                max_value = h
                next_move = move
    # Return the best move determined by the Expectimax algorithm or the heuristic-based move
    return next_move




######################### GAME DISPLAY #############################################################


class Display(Frame):
    def __init__(self):
        '''
        Initialize the Display class, representing the graphical user interface for the 2048 game.
        Attributes:
        - grid_cells: List of Label widgets representing the cells of the game grid
        - commands: Dictionary mapping key presses to corresponding move functions
        '''
        # Initialize the parent class (Frame)
        Frame.__init__(self)
        # Set up the grid layout and other components
        self.grid()
        self.build_buttons()
        self.master.title('2048')
        self.master.bind("<Key>", self.key_press)
        # Define commands for key presses (mapping keys to move functions)
        self.commands = {
            UP_KEY: move_up,
            DOWN_KEY: move_down,
            LEFT_KEY: move_left,
            RIGHT_KEY: move_right,
        }
        # Initialize the list to store grid cells
        self.grid_cells = []
        # Build the game grid and initialize the game matrix
        self.build_grid()
        self.init_matrix()
        # Draw the initial state of the game grid
        self.draw_grid_cells()
        # Start the main event loop for the graphical interface
        self.mainloop()

    def build_grid(self):
       '''
        Build the game grid by creating Frame and Label widgets for each cell.
        The cells are organized in rows and columns, and each cell has a corresponding Label widget.
        Attributes:
        - background: Frame widget serving as the background for the entire grid
        - grid_cells: 2D list storing Label widgets representing the cells of the game grid
        '''
        # Create a background Frame for the entire grid with specified color and dimensions
        background = Frame(self, bg=GAME_COLOR, width=EDGE_LENGTH, height=EDGE_LENGTH)
        background.grid()
        # Iterate through each row and column to create cells and corresponding Label widgets
        for row in range(CELL_COUNT):
            grid_row = []  # List to store Label widgets for a single row
            for col in range(CELL_COUNT):
                # Create a cell Frame with specified color and dimensions
                cell = Frame(background, bg=EMPTY_COLOR, width=EDGE_LENGTH / CELL_COUNT, height=EDGE_LENGTH / CELL_COUNT)
                cell.grid(row=row, column=col, padx=CELL_PAD, pady=CELL_PAD)
                # Create a Label widget inside the cell with initial text and formatting
                t = Label(master=cell, text="", bg=EMPTY_COLOR, justify=CENTER, font=LABEL_FONT, width=5, height=2)
                t.grid()
                # Append the Label widget to the row list
                grid_row.append(t)
            # Append the row list to the grid_cells 2D list
            self.grid_cells.append(grid_row)

    def init_matrix(self):
        '''
        Initialize the game matrix by calling the initialize_game function.
        The resulting matrix is stored in the 'matrix' attribute of the Display class.
        '''
        self.matrix = initialize_game()

    def draw_grid_cells(self):
        '''
        Update the graphical representation of the game grid based on the current state of the matrix.
    
        The method iterates through each cell in the matrix and configures the corresponding Label widget
        in the graphical grid with the appropriate text, background color, and foreground color.
        '''
        for row in range(CELL_COUNT):
            for col in range(CELL_COUNT):
                tile_value = self.matrix[row][col]
                if not tile_value:
                    # Configure the Label widget for an empty cell
                    self.grid_cells[row][col].configure(text="", bg=EMPTY_COLOR)
                else:
                    # Configure the Label widget for a non-empty cell with appropriate text and colors
                    self.grid_cells[row][col].configure(
                        text=str(tile_value), bg=TILE_COLORS[tile_value], fg=LABEL_COLORS[tile_value])
    
        # Update the graphical display to reflect the changes
        self.update_idletasks()
    
    def build_buttons(self):
        '''
        Build the buttons for starting a new game and stopping the application.
    
        - new_game_button: Button widget for starting a new game, with text "New Game" and linked to the start_new_game method
        - stop_button: Button widget for stopping the application, with text "Stop" and linked to the master.destroy method
        '''
        # Button for starting a new game
        new_game_button = Button(self, text="New Game", command=self.start_new_game)
        new_game_button.grid(row=CELL_COUNT, column=0, columnspan=2, pady=10)
    
        # Button for stopping the application
        stop_button = Button(self, text="Stop", command=self.master.destroy)
        stop_button.grid(row=CELL_COUNT, column=2, columnspan=2, pady=10)

    def start_new_game(self):
        '''
        Start a new game by initializing the game matrix and updating the graphical representation of the grid.
        '''
        # Initialize the game matrix
        self.init_matrix()
    
        # Update the graphical representation of the grid
        self.draw_grid_cells()
     
    def key_press(self, event):
        '''
        Handle key press events.
    
        - key: Extracted key from the event.
        - AI_PLAY_KEY: Key used to trigger automatic gameplay with a fixed depth and heuristic.
        - AI_MULTI_PLAY: Key used to trigger multiple games with different depths and heuristics.
    
        For AI_PLAY_KEY:
        - move_count: Counter for the number of moves.
        - score_tot: Total score accumulated during gameplay.
        - won_the_game: Flag indicating whether the game was won.
        - Execute fixed_move until no valid moves left.
        - Update statistics and display the results.
    
        For AI_MULTI_PLAY:
        - num_games: Number of games to play.
        - move_count, score_tot, won_the_game: Counters and flags for each game.
        - results_weight: Matrix to store results for different depths and heuristics.
        - Loop over specified depths, heuristics, and games, playing and recording results.
        - Print the results for each depth.
    
        For general key commands:
        - Execute the corresponding move command if the key is in the predefined commands.
        - Update the game matrix, check for a valid move, add a new tile, and update the graphical representation.
    
        Note: Some commented code for handling win/loss popups is provided at the end but is currently disabled.
        '''
        key = repr(event.char)
        
        if key == AI_PLAY_KEY:
            move_count = 0
            score_tot = 0
            won_the_game = 0
            while fixed_move(self.matrix)[1]:
                if not check_for_win(self.matrix):
                    won_the_game = 1
                move = find_move(self.matrix, depth=2, type_hes='WEIGHT_DIAG')
                self.matrix, _, score_new = move(self.matrix) 
                score_tot += score_new            
                self.matrix = add_new_tile(self.matrix)
                self.draw_grid_cells()
                move_count += 1
        elif key == AI_MULTI_PLAY:
            num_games = 90
            move_count = 0
            score_tot = 0
            won_the_game = 0
            # Opret tomme matricer til at gemme resultaterne
            results_weight = np.zeros((6, num_games))

            # Loop for at spille spillet og gemme resultaterne
            for DEPTH in [2]:
                for j, types in enumerate(['WEIGHT_DIAG', 'WEIGHT_SNAKE']):
                    for i in range(num_games):
                        while fixed_move(self.matrix)[1]:
                            if check_for_win(self.matrix):
                                won_the_game = 1
                            move = find_move(self.matrix, DEPTH, type_hes=types)
                            self.matrix, _, score_new = move(self.matrix) 
                            score_tot += score_new            
                            self.matrix = add_new_tile(self.matrix)
                            self.draw_grid_cells()
                            move_count += 1
                        results_weight[0 + 3*j, i] = move_count
                        results_weight[1 + 3*j, i] = won_the_game
                        results_weight[2 + 3*j, i] = score_tot
                        move_count = 0
                        score_tot = 0
                        won_the_game = 0
                        score_new = 0
                        self.start_new_game()
                print(f'Results for depth: {DEPTH}:')
                print(f'{results_weight}\n')


            """ for i in range(num_games):
                while fixed_move(self.matrix)[1]:
                    if check_for_win(self.matrix):
                        won_the_game = 1
                    move = find_move(self.matrix, depth=2, type_hes='WEIGHT_SNAKE')
                    self.matrix, _, score_new = move(self.matrix) 
                    score_tot += score_new            
                    self.matrix = add_new_tile(self.matrix)
                    self.draw_grid_cells()
                    move_count += 1
                results_weight_snake[0, i] = move_count
                results_weight_snake[1, i] = won_the_game
                results_weight_snake[2, i] = score_tot
                move_count = 0
                score_tot = 0
                won_the_game = 0 
                self.start_new_game() """


            


        if key in self.commands:
            self.matrix, move_made, _ = self.commands[repr(event.char)](self.matrix)
            if move_made:
                self.matrix = add_new_tile(self.matrix)
                self.draw_grid_cells()
                move_made = False
        
        """if check_for_win(self.matrix):
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
            stop_button.pack(pady=10) """




gamegrid = Display()
