from game2dboard import Board
import time
import random
from tkinter import messagebox, Tk

# Key commands
MSG = "U: Undo Last Moves    F2: Restart    ESC: Exit Game    "

# Defines sizes of the square and tile, colors of the board, line, 
# and tile as constants
GAME_WINDOW_TITLE = "Othello"
CELL_SIZE = 80
CELL_COLOR = "green"
CELL_SPACING = 2
LINE_COLOR = "black"

# All the possible move directions a player's move can flip disks 
# from the other player, as constant (0 –> the current row/column, 
# +1 –> the next row/column, -1 –> the previous row/column)
POSSIBLE_MOVE_DIRECTIONS = [(-1, -1), (-1, 0), (-1, +1),
                            (0, -1),           (0, +1),
                            (+1, -1), (+1, 0), (+1, +1)]

# ARRAY of tuples (row, col): 
# POSSIBLE_MOVE_DIRECTIONS = [(-1, -1), (-1, 0), (-1, +1), (0, -1), (0, +1),(+1, -1), (+1, 0), (+1, +1)]



# The constructor method for the OthelloGame class in the othello_game.py file.

# initializes the game board, sets the board size, creates the output bar for messages and instructions,
    # and initializes event handlers for keyboard commands, starting the game, mouse clicks, and timer for the computer AI move.

class Game:
    def __init__(self, board_width=8, board_height=8):

        # Board initialization
        self.board = Board(board_width, board_height)

         # (IL) Set the default cursor state to 'arrow'
        self.board.cursor = "arrow"

        # If you want computer AI White disks to start, uncomment the line below: 
            #self.board.start_timer(2000)
        self.board.cell_size = CELL_SIZE
        self.board.margin_color = self.board.grid_color = LINE_COLOR
        self.board.cell_color = CELL_COLOR
        self.board.cell_spacing = CELL_SPACING
        self.board.title = GAME_WINDOW_TITLE
        # Bottom bar for messages and short instructions
        self.board.create_output(background_color="grey", color="white")

        # Global settings initialization
        self.board_size_n = min(self.board.nrows, self.board.ncols)

        # Event-Handlers initialization
        '''
        Assign the keyboard_command and initialize_game_settings methods as event handlers, 
        so we just specify the relationship/mapping the functions dont run now 
        only when the events happen.
        By omitting the parentheses, we are assigning the methods themselves as event handlers
        '''
        self.board.on_key_press = self.keyboard_command
        self.board.on_start = self.starting_game_initialization
        self.board.on_mouse_click = self.play_as_human_player
        # Eevent handler for timer to decouple the computer-AI move from the human-user's click
        self.board.on_timer = self.play_as_ai_computer_player
        # Stack feature for saving movements feature
        self.algo_stack = []


    # Initializes/resets the game board, placing the initial disks for both players in the center of the board.
    def starting_game_initialization(self):
        self.algo_stack.clear()
        # Game settings initialization
        
        # Use a dictionary to store the number of disks for each player
        # so, index 0 (if it was an array) is not used and this way with dictionary 
        # the index coincides with the Player's number (1 or 2). 

        self.num_disks_dictionary = {1: 2, 2: 2}

        if self.board_size_n < 2:
            return
        
        # Clean the board, in case we're re-starting from a previous game
        self.board.clear()
        self.board.cursor = "arrow"

        # Disks initialization (Draw the first 4 disks in the middle of the board)
        '''
        If the board cols and rows are both 2 or greater, 
        the method calculates the coordinates of the four initial disks and 
        stores them in the initial_cells list. 
        The coord1 and coord2 variables are calculated as the floor division 
        of self.board_size_n / 2 - 1 and self.board_size_n / 2, respectively, 
        where self.board_size_n is the size of the board.
        '''
        coord1 = int(self.board_size_n / 2 - 1)
        coord2 = int(self.board_size_n / 2)
        initial_cells = [(coord1, coord2), (coord1, coord1),
                         (coord2, coord1), (coord2, coord2)]
        
        '''
        The method then iterates over the initial_cells list and sets the color and position of each disk on the board. 
        The color variable is set to i % 2, which alternates between 0 and 1 for each iteration of the loop. 
        The row and col variables are set to the row and column coordinates of the current disk, respectively.
        '''
        for i in range(len(initial_cells)):
            color = i % 2
            row = initial_cells[i][0]
            col = initial_cells[i][1]

            self.board[row][col] = color + 1
        
        print(self.board)

        self.difficulty = "M" # Default difficulty is Medium
        self.board.print(MSG + "DIFFICULTY: (E: Easy, M: *Medium*, H: Hard)")

        # Player 1 is Human-user
        # Player 2 is Computer-AI
        # Player 1 starts the game
        self.current_player = 2 # Save initial state move as player 2 (Computer-AI)
        self.save_moves() # Save state before making a move
        self.current_player = 1 # The turn is for player 1 (Human-user)

        # Time Complexity:
        # Worst and Average case = O(1), as it performs a constant number of operations
        # Best case = O(1), same as above

    # This function verifies if a set of coordinates, given as row and column, are within the bounds of a board.
    def coord_is_valid(self, row, col):
        '''
            Returns: True if row and col are valid, False if not.
            A valid coordinate must be in the range of the board.
        '''
        if 0 <= row < self.board_size_n and 0 <= col < self.board_size_n:
            return True
        return False

    # Time Complexity:
    # Worst, Average, and Best case = O(1)

    # This funcgtions creates and returns an independent copy of the current state of all
    # cells in a board, which can be usefull when trying to undo moves or use the copied board
    def copy_board_cell_states(self):
        board_cell_states = [[None for _ in range(8)] for _ in range(8)]
        rows_array = range(0, self.board.nrows, 1)
        cols_array = range(0, self.board.ncols, 1)
        for row in rows_array:
            for col in cols_array:
                board_cell_states[row][col] = self.board[row][col]

        return board_cell_states

    # Time Complexity:
    # Worst, Average, Best = O(N^2), as it iterates over each cell in the board

    # This function evaluates whether the last two moves in a game were made by the same player.
    def check_last_two_moves_from_same_player(self):
        if len(self.algo_stack) < 2:
            print("Not enough moves to check.")
            return False
        
        for i in range(len(self.algo_stack)):
            print("Player: ", i, " ", self.algo_stack[i]["current_player"])

        last_move = self.algo_stack[-1]
        second_last_move = self.algo_stack[-2]
        print("Last move: ", last_move)
        print("Second last move: ", second_last_move)

        last_player = self.algo_stack[-1]["current_player"]
        second_last_player = self.algo_stack[-2]["current_player"]
        if last_player == second_last_player:
            return True
        else:
            return False

    # Time Complexity:
    # Worst, Average, and Best case = O(1)

    def direction_has_disk_to_flip(self, move, direction, player_number):

        #    Parameters: move (tuple), direction (tuple)
        #    Returns: True if there is any disk to flip, False if not.
        #    Checks if the player has any adversary's disk to flip with the move to make.
        #    move is the (row, col) coordinate of where the player makes a move; 
        #    direction is the direction in which the adversary's disk/s are to be flipped 

        #calculate disk type to flip
        disk_type_current_player = player_number
        disk_type_to_flip = 3 - player_number

        # Since we initialize i to 1, 1 means we didnt find any disk to flip.
        distance = 1
        disks_to_flip_counter = 0
        while True:
            row = move[0] + direction[0] * distance
            col = move[1] + direction[1] * distance

            if not self.coord_is_valid(row, col) or \
                    self.board[row][col] == None:  # Empty cell
                    return False
            elif self.board[row][col] == disk_type_current_player:  
                # Current player color disk found, so stop direction and exit
                break
            else:
                # Disk color is the one to flip, so continue looking in the same direction
                if self.board[row][col] == disk_type_to_flip:
                    # print("Found disk to flip: ", row, ",", col, "content:", self.board[row][col])
                    distance += 1
                    disks_to_flip_counter += 1
        
        return (disks_to_flip_counter > 0) # Return True if there is any disk to flip, False if not.

    # Time Complexity:
    # Worst case = O(N), entire borad
    # Average and Best case = O(1), only few cells checks or only one

    # This function for determining the validity and impact of a player's move,
    # specifically whether it can capture any of the opponent's pieces, if the player fliped.
    def move_has_disk_to_flip(self, move, player_number):
        ''' 
            Checks whether the player's move is possible.
            move parameter is a tuple of coordinates (row, col)
            Returns: boolean (True if move is possible, False if not)
        '''

        content_of_move_cell = self.board[move[0]][move[1]]

        if move != () and self.coord_is_valid(move[0], move[1]) \
           and content_of_move_cell == None:
            for direction in POSSIBLE_MOVE_DIRECTIONS:
                # print("Direction: ",direction)
                has_disk_to_flip = self.direction_has_disk_to_flip(move, direction, player_number)
                if has_disk_to_flip:
                    return True
                     
        return False

    # Time Complexity:
    # Worst case = O(N), much check all
    # Average case = O(1), early return
    # Best case = O(1),  initial conditions fail

    # This function is critical espcially in our game where capturing the
    # opponent's pieces is a core mechanic. It updates the counts of discs for
    # each player in accordance with the opponent's discs being flipped to the
    # player's colour along all valid directions emanating from the move.
    def flip_disks_for_move(self, move):
            '''
                Flips the contrary's disks for the current move being applied by 
                updating the board's states:
                "1" state for black disks and "2" state for white disks.
                Also, per each flip, increases the number of disks for the current player by 1, 
                and decreases for the contrary.
            '''
            current_disk_type = self.current_player 
            for direction in POSSIBLE_MOVE_DIRECTIONS:
                if self.direction_has_disk_to_flip(move, direction, self.current_player):
                    counter_of_disks_flipped = 0
                    distance = 1
                    while True:
                        # Calculate the coordinates of the current cell 
                        # based on the direction. For example, if the current move is (3, 4) and the direction is (-1, 0), 
                        # then the code calculates the row and column coordinates of the cell 
                        # to check as follows:
                        # row = 3 + (-1) * distance = 3 - distance
                        # col = 4 + 0 * distance = 4
                        # So, cell as (3 - distance, 4) is checked.
                        row = move[0] + direction[0] * distance
                        col = move[1] + direction[1] * distance
                        # If the current cell has a disk of the current player, stop and exit.
                        if self.board[row][col] == current_disk_type:
                            break
                        else:
                            # Flip the disk on the current cell being analyzed
                            self.board[row][col] = current_disk_type

                            # Update the number of disks for the current player and the contrary
                            self.num_disks_dictionary[self.current_player] += 1
                        # print("New current player total disks:",self.num_disks_dictionary[self.current_player])
                            
                            # print("Contrary's total disks BEFORE:",self.num_disks_dictionary[3 - self.current_player])
                            self.num_disks_dictionary[3 - self.current_player] -= 1
                            # print("Contrary's total disks AFTER:",self.num_disks_dictionary[3 - self.current_player])
                            counter_of_disks_flipped += 1
                            distance += 1
                
                    # print("Total disks flipped: ",counter_of_disks_flipped, "for direction: ",direction)

    # Time Complexity:
    # Worst case = O(N), if it needs to flip disks across the board
    # Average case = O(1), few flipped
    # Best case = O(1), no flip

    # This function places a disk on the board for the current player's move,
    # flips the opponent's disks, it updates the board states, increasing
    # player's disk count.
    def make_current_move(self):
        self.make_move(self.current_move)

    # Time Complexity:
    # Worst and Average case = O(N), flipping disks across the board
    # Best case = O(1), if no disks to flip

    def make_move(self, move):
            ''' 
                Puts a disk for the player's current move on the board 
                and then flips the contrary's disks in between. 
                The update of the disks is made by changing the board's states 
                (1 for black disks and 2 for white disks), 
                and increasing the number of disks of the current player by 1.
                (flip_disks_for_current_move() function should also increase 
                the number of disks of the current player by 1)
            '''
            if self.move_has_disk_to_flip(move, self.current_player):
                # Put current player color on the current move cell
                self.board[move[0]][move[1]] = self.current_player
                # Adds 1 disk to the current players disk count
                self.num_disks_dictionary[self.current_player] += 1
                
                self.flip_disks_for_move(move)
                self.save_moves()  # Save state after making a move

    # Time Complexity:
    # Worst and Average case = O(N), flipping disks across the board
    # Best case = O(1), if no disks to flip

    # This function checks if the player has any possible moves left on the board
    # If yes, the player can make a move that would flip at least one of the
    # opponent's disks, and if not it the game would be over.
    def player_can_move(self, player_number):
        ''' 
            Returns: True if the current player has possible moves, False if not.
        '''
        # print("Current player is: ", player_number)

        rows_array = range(0, self.board.nrows, 1)
        cols_array = range(0, self.board.ncols, 1)

        # Go through all the cells of the board matrix to check if there is any possible move
        player_has_possible_move = False

        for row in rows_array:
            # print("Range of rows: ", rows_array)
            for col in cols_array:
                # print("Range of cols: ", cols_array)
                test_move = (row, col)
                if self.move_has_disk_to_flip(test_move, player_number):
                    player_has_possible_move = True
                    # If found possible move, return True and exit the function
                    return player_has_possible_move
               
        return player_has_possible_move

    # Time Complexity:
    # Worst and Average case = O(N^2), scanning all cells for a valid move
    # Best case = O(1), if an early valid move is found

    # Function determines if current player has any moves available
    def current_player_can_move(self):
        ''' 
            Returns: True if the current player has possible moves, False if not.
        ''' 
        return self.player_can_move(self.current_player)

    # Time Complexity: Inherits from player_can_move
    # Worst and Average case = O(N^2)
    # Best case = O(1)

    # This function generates and gives a touple list of all valid move coordinates
    # that the player can make.
    def get_possible_moves_by_current_player(self):
            ''' 
                Returns a list of possible moves that can be made by the current player
                Every move is a tuple of coordinates (row, col).
            '''
            rows_array = range(0, self.board.nrows, 1)
            cols_array = range(0, self.board.ncols, 1)
            allowed_moves_list = []
            for row in rows_array:
                for col in cols_array:
                    # Move to check and append if valid
                    move_to_check = (row, col)
                    if self.move_has_disk_to_flip(move=move_to_check, player_number=self.current_player):
                        allowed_moves_list.append(move_to_check)

            return allowed_moves_list
            # Returns a list of possible moves that can be made by the current player
            # This is an example of usage of a Linked List, adding moves with .append()

    # Time Complexity:
    # Worst and Average case = O(N^2), scanning all cells for valid moves
    # Best case = O(1), if no valid moves are found early

    #  Calculates and returns a score representing the current state of the board
    #  This takes into account the number of pieces, corners and edges and mobility.
    def evaluate_board_state(self, original_number_of_disks_AI_player, original_board, after_move_board):
            score = 0
            
            # 1. Count the number of pieces for AI and opponent
            ai_pieces = 0
            opponent_pieces = 0
            for row in range(self.board_size_n):
                for col in range(self.board_size_n):
                    if self.board[row][col] == 2:  # Assuming AI is player 2
                        ai_pieces += 1
                    elif self.board[row][col] == 1:
                        opponent_pieces += 1

            number_of_new_disks_for_AI = ai_pieces - original_number_of_disks_AI_player

            score += number_of_new_disks_for_AI

            # 2. Control of corners (corners are more valuable)
            if self.ai_has_new_disk_in_corner(original_board, after_move_board):
                score += 25

            # 3. Control of edges
            if self.ai_has_new_disk_on_edge(original_board, after_move_board):
                score += 10

            return score

    # Time Complexity:
    # Worst and Average case = O(N^2), scanning the entire board
    # Best case = O(N^2), as it always scans the entire board

    # This function checks if the AI has a new disk in a corner
    def ai_has_new_disk_in_corner(self, original_board, after_move_board):
        new_ai_disks = []
        for i in range(len(original_board)):
            for j in range(len(original_board[i])):
                if original_board[i][j] != 2 and after_move_board[i][j] == 2:
                    new_ai_disks.append((i, j))

        corners = [(0, 0), (0, len(original_board[0])-1), (len(original_board)-1, 0), (len(original_board)-1, len(original_board[0])-1)]
        for disk in new_ai_disks:
            if disk in corners:
                return True
        return False

    # Time Complexity:
    # Worst and Average case_ O(N^2)
    # Best case= O(N^2), as it always scans the entire board

    # This function checks if the AI has a new disk in an edge
    def ai_has_new_disk_on_edge(self, original_board, after_move_board):
        new_ai_disks = []
        for i in range(len(original_board)):
            for j in range(len(original_board[i])):
                if original_board[i][j] != 2 and after_move_board[i][j] == 2:
                    new_ai_disks.append((i, j))

        edges = []
        edges.extend([(i, 0) for i in range(len(original_board))])  # left edge
        edges.extend([(i, len(original_board[0])-1) for i in range(len(original_board))])  # right edge
        edges.extend([(0, j) for j in range(len(original_board[0]))])  # top edge
        edges.extend([(len(original_board)-1, j) for j in range(len(original_board[0]))])  # bottom edge

        for disk in new_ai_disks:
            if disk in edges:
                return True
        return False

    # Time Complexity:
    # Worst, Best and Average case= O(N^2), scanning the entire board

    # This function is used to make a random move on the board for the player.
    def make_random_move_by_current_player(self):
        # Makes a random possible move on the board.
        possible_moves = self.get_possible_moves_by_current_player()
        print("Possible moves for AI-Computer: ", possible_moves)
        if possible_moves:
            self.current_move = random.choice(possible_moves)
            self.make_current_move()

    # Time Complexity is constant at a O(N), creating a list of moves depends on the size of the board

    # This method simulates a move, analyses its effect, and then returns the board to its initial
    # configuration in order to determine how effective a particular move is in a board game.
    # It returns back a score that represents how effective the move was.
    def evaluate_move_greedy(self, move):
        original_number_of_disks_AI_player = self.num_disks_dictionary[2]

        original_board = self.copy_board_cell_states()

        # Make the move in the board (including flips) temporarily to simulate the move
        self.make_move(move)

        after_move_board = self.copy_board_cell_states()

        # Evaluate the board after making the move
        score = self.evaluate_board_state(original_number_of_disks_AI_player, original_board, after_move_board)

        # Revert the move and flips
        self.undo_last_move()

        return score

    # Time Complexity is constant at a O(N^2)

    # This function can predict the outcome of a move several turns in advance
    # helping the AI and the computer to determine its next move
    def evaluate_move_minimax(self, move, current_depth=0, max_depth=3):
        original_number_of_disks_AI_player = self.num_disks_dictionary[2]

        original_board = self.copy_board_cell_states()

        # Make the move in the board (including flips) temporarily to simulate the move
        self.make_move(move)

        after_move_board = self.copy_board_cell_states()
        
        if current_depth == max_depth:
            # Base case: Evaluate the board at the current depth
            score = self.evaluate_board_state(original_number_of_disks_AI_player, original_board, after_move_board)
        else:
            # Evaluate the board after making the move
            score = self.evaluate_board_state(original_number_of_disks_AI_player, original_board, after_move_board)

            # Depending on the depth, switch between AI and opponent moves
            next_player = self.current_player if current_depth % 2 == 0 else 3 - self.current_player

            # Generate potential moves for the next player
            next_moves = self.get_possible_moves_by_current_player()
            if next_moves:
                for next_move in next_moves:
                    if next_player == self.current_player:
                        # Maximize AI score
                        score += self.evaluate_move_minimax(next_move, current_depth + 1, max_depth)
                    else:
                        # Minimize opponent score
                        score -= self.evaluate_move_minimax(next_move, current_depth + 1, max_depth)

        self.undo_last_move()
        return score

    # Time Complexity:
        # Best Case O(1). Happens when there are no more moves available, so no calls to the recursive function.
        # Average Case and Worst Case O(n). Depends on how big the averagely branched explored game tree is.


    # The function finds and executes the best possible move for the current player in a board game.
    def make_best_move_by_current_player(self):
            best_score = float('-inf')
            best_move = None

            # Get all possible moves for the AI player
            possible_moves = self.get_possible_moves_by_current_player()

            # Evaluate each move using the random, greedy or minimax function/method
            for move in possible_moves:
                if self.difficulty == "M":
                    score = self.evaluate_move_greedy(move)
                elif self.difficulty == "H":
                    score = self.evaluate_move_minimax(move)

                # Select the move with the highest score
                if score > best_score:
                    best_score = score
                    best_move = move

            # Make the best move if one is found
            if best_move:
                self.current_move = best_move
                self.make_current_move()

    # TimeComplexity:
    # Worst case = O(N * M), maximum number of possible moves to consider.
    # Average case =  O(N_avg * M), depends on the average number of possible moves the AI can make
    # Best case = O(N), evaluating a single move

    # This function determines if the game has ended, if both player 1 and 2 have no where else to move
    # if no one can move it checks the player with most disk and return the winner
    def is_game_over(self):
            if not self.player_can_move(1) and not self.player_can_move(2):
                if self.num_disks_dictionary[1] > self.num_disks_dictionary[2]:
                    print('*****************')
                    print('Wooohooo! You won!! Congrats!!')
                    # self.board.print(MSG + ' -- Wooohooo! You won!! Congrats!!')
                    messagebox.showinfo("Game Over", "Wooohooo! You won!! Congrats!!")
                elif self.num_disks_dictionary[1] < self.num_disks_dictionary[2]:
                    print('*****************')
                    print('Too bad, you lost!! The computer won!! ;)')
                    # self.board.print(MSG + ' -- Too bad, you lost!! The computer won!! ;)')
                    messagebox.showinfo("Game Over", "Too bad, you lost!! The computer won!! ;)")
                return True
            
            else:
                return False # Game is not over yet

    # TimeComplexity:
    # Worst case = After confirming that neither player can move, it performs the constant time
    # operation of comparing disk counts, but this does not affect the overall complexity.
    # Average case =  2 * O(N), both players before determining if the game is over
    # Best case = O(N), when player 1 wins, thus does not need to check player 2

    # Triggered when the user clicks on the board with the mouse.
    # It shouldnt directly get through here if the computer is thinking/moving, though.
    def play_as_human_player(self, btn, r, c):
        ''' 
            Arguments: 
                        btn: Mouse button clicked
                        r, c are the row/column coordinates where the user clicked on the board.
        '''
        # Indicate that the game is processing the user's input
        self.board.cursor = "wait"
        
        # Check if it's the human user's turn and if they can make a move
        if self.current_player_can_move():
            print("Current player has possible move(s)")

            # Update the current move with tuple of coordinates (column, row)
            self.current_move = (r,c)
            
            if self.move_has_disk_to_flip(self.current_move, self.current_player):
                print("Current move HAS disk(s) to flip: ",r," ", c)

                # Make the move, actually. Board update, disk paint, disks flipped, etc.
                self.make_current_move()

                # After move, check if game is over
                if self.is_game_over():
                    self.board.cursor = "arrow"
                    return

                self.current_player = 2
                # Start the timer for the AI move after the human player's turn
                self.board.start_timer(2000)

            else:
                print("Current move is NOT legal: ",r," ", c)

        # Reset the cursor to the default state (arrow) after processing user's input
        self.board.cursor = "arrow"

    # TimeComplexity:
    # Worst, average case = O(M + F + U + G), checking for moves, flipping disks, doing the move, checking if game is over.
    # Best case = O(N), returns False immediately

    # This function create the AI's game plan, making sure that it makes a move
    # when it is its turn or until human player can move once more.
    def play_as_ai_computer_player(self):
        
        # Disable the Timer to prevent re-triggering
        self.board.stop_timer()

        # Set the cursor to indicate AI is processing
        self.board.cursor = "wait"

        # AI's turn to play
        # if human player cannot move and is not game over the computer keeps playing with this loop
        while True:    
            self.current_player = 2
            if self.current_player_can_move():
                print("AI (Player 2) is making a move...")
                time.sleep(1) # Simulate AI thinking time

            if self.difficulty == "E":
                self.make_random_move_by_current_player()
            else: # Medium or Hard
                # AI makes the best move selected by the algorithm
                # self.make_random_move_by_current_player()
                self.make_best_move_by_current_player()

            # Check if the game is over after the AI move
            if self.is_game_over():
                self.board.cursor = "arrow"
                return
            
            self.current_player = 1
            if self.current_player_can_move():
                self.board.cursor = "arrow"
                # if human player can move after computer´s turn, then exit the loop
                break

    # TimeComplexity:
    # Worst case = O(W * (M + B + G)), maximum number of iterations as W that AI will make
    # Average case = O(A * (M + B + G)), a few moves between the AI and the human player
    # Best case =  O(M + B + G), if the game ends after the computer first move.


    def count_disks(self, board):
        num_disks_dictionary = {1: 0, 2: 0}
        for row in board:
            for cell in row:
                if cell in num_disks_dictionary:
                    num_disks_dictionary[cell] += 1
        return num_disks_dictionary
    # TimeComplexity:
    #Time Complexity: O(N^2): The function cycles through every board cell.
    # The board has a quadratic time complexity if it is N x N in size and needs to check N^2 cells.

    # This function does, to undo the last two moves. Depending on the game's current
    # and past states. If the human player make mistakes or reconsider different stratgies
    def undo_last_move(self):
        print("Current player before undoing: ", self.current_player)
        print("Number of disks in element 1 of the stack: ", self.algo_stack[1]["num_disks_dictionary"][2])
        print("Number of disks for AI player before undoing: ", self.num_disks_dictionary[2])
        self.board.cursor = "arrow"
        print("Current player before undoing: ", self.current_player)
        if len(self.algo_stack) < 2:
           print("Not possible to undo move since there are no moves to undo.")
           return
        
        # remove the last move from the stack
        self.algo_stack.remove(self.algo_stack[-1])

        # get last value of the stack without removing it
        previous_state = self.algo_stack[-1]
        print("Number of elements in undoing: ", len(self.algo_stack))
        print("Previous state: ", previous_state)
        print("Board before undoing:")
        print(self.board)
        print("**********")
        rows_array = range(0, self.board.nrows, 1)
        cols_array = range(0, self.board.ncols, 1)
        matrix = previous_state["board"]
        for row in rows_array:
            for col in cols_array:
                self.board[row][col] = matrix[row][col]
        print("Board after undoing:")
        print(self.board)
        print("**********")

        # possible issue with reference to the board, since it is not being updated
        # self.num_disks_dictionary = previous_state["num_disks_dictionary"]
        
        self.num_disks_dictionary = self.count_disks(self.board)

        print("Number of disks for AI player after undoing: ", self.num_disks_dictionary[2])

        print("Current player after undoing: ", self.current_player)
        # refresh of the board is done when the function is finished
    # TimeComplexity:
    # Worst case and Average case = O(n^2), performs the whole code given back two moves
    # Best case =   O(1), if there are less the two moves in the stack, returning immediatly

    def undo_last_two_moves(self):
        self.board.cursor = "arrow"
        print("Current player before undoing: ", self.current_player)
        if len(self.algo_stack) < 2:
           print("Not possible to undo move since there are no moves to undo.")
           return
        # check if the last 2 moves are the same player
        if self.check_last_two_moves_from_same_player() or self.algo_stack[-1]["current_player"] == 1:
            self.algo_stack.pop()
        else:
            self.algo_stack.pop()
            self.algo_stack.pop()

        previous_state = self.algo_stack.pop()
        print("Board before undoing:")
        print(self.board)
        print("**********")
        rows_array = range(0, self.board.nrows, 1)
        cols_array = range(0, self.board.ncols, 1)
        matrix = previous_state["board"]
        for row in rows_array:
            for col in cols_array:
                self.board[row][col] = matrix[row][col]
        print("Board after undoing:")
        print(self.board)
        print("**********")
        
        print("Elements in stack: ",self.algo_stack.count)
        if len(self.algo_stack) == 0:
            # if we only have the initial move/postition, then the current player´s turn is 1
            self.current_player = 2
            self.save_moves()
            self.current_player = 1
        else:
            self.current_player = previous_state["current_player"]
            self.save_moves()
            # The current players turn is the contrary of the previous state
            self.current_player = 3 - previous_state["current_player"]
        
        self.num_disks_dictionary = previous_state["num_disks_dictionary"]
        
        print("Current player after undoing: ", self.current_player)
        # refresh of the board is done when the function is finished
    # TimeComplexity:
    # Worst case and Average case = O(n^2), performs the whole code given back two moves

    # This function starts the display of the board, starting the game
    def run(self):
        self.board.show()
    # Time Complexity is constant time of O(1)

    # This function is used to handle keyboard inputs and outputs, and what the user can click.
    def  keyboard_command(self, key):
        if key == "Escape":
            self.board.close()
        elif key == "F2":
            self.starting_game_initialization()
        elif key == "u" or key == "U":
            self.undo_last_two_moves()
        elif key == "e" or key == "E":
            self.difficulty = "E"
            self.board.print(MSG + "DIFFICULTY: (E: *Easy*, M: Medium, H: Hard)")
        elif key == "m" or key == "M":
            self.difficulty = "M"
            self.board.print(MSG + "DIFFICULTY: (E: Easy, M: *Medium*, H: Hard)")
        elif key == "h" or key == "H":
            self.difficulty = "H"
            self.board.print(MSG + "DIFFICULTY: (E: Easy, M: Medium, H: *Hard*)")
    # TimeComplexity:
    # Worst case = O(n), if all the cells have a disk that needs to be copied
    # Average case and Best case =  O(1), copy and appending into stack

    def save_moves(self):
        state = {
            "board": self.copy_board_cell_states(),
            "current_player": self.current_player,
            "num_disks_dictionary": self.copy_num_disks_dictionary(self.num_disks_dictionary)
        }
        self.algo_stack.append(state)
        print("Saved state: ", state)
    # TimeComplexity:
    # Worst case = O(n), if all the cells have a disk that needs to be copied

    def copy_num_disks_dictionary(self, original_dict):
        new_dict = {}
        for key, value in original_dict.items():
            new_dict[key] = value
        return new_dict

    # TimeComplexity:
    # Worst case = O(n), if all the cells have a disk that needs to be copied
