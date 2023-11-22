from game2dboard import Board
import time
import random

# Key commands
MSG = "U: Undo Last Moves    F2: Restart    ESC: Exit Game"

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
        
        # (ADLT) Use a dictionary to store the number of disks for each player
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

        self.board.print(MSG)

        # Player 1 is Human-user
        # Player 2 is Computer-AI
        # Player 1 starts the game
        self.current_player = 2 # Save initial state move as player 2 (Computer-AI)
        self.save_moves() # Save state before making a move
        self.current_player = 1 # The turn is for player 1 (Human-user)

    def run(self):
        self.board.show()

    def keyboard_command(self, key):
        if key == "Escape":
            self.board.close()
        elif key == "F2":
            self.starting_game_initialization()
        elif key == "u" or key == "U":
            self.undo_last_two_moves()

    # (ADLT) Triggered when the user clicks on the board with the mouse.
    # It shouldnt directly get through here if the computer is thinking/moving, though.
    def play_as_human_player(self, btn, r, c):
        ''' 
            Arguments: 
                        btn: Mouse button clicked
                        r, c are the row/column coordinates where the user clicked on the board.
        '''
        # TEST
        print("Mouse Button: ",btn)
        print("Clicked on Board Coordinates: ",r," ", c)
        
        # 1. Play the human-user's turn
        if self.current_player_can_move():
            print("Current player has possible move(s)")
            # Update the current move with tuple of coordinates (column, row)
            self.current_move = (r,c)
            
            if self.move_has_disk_to_flip(self.current_move, self.current_player):
                print("Current move HAS disk(s) to flip: ",r," ", c)
                # (ADLT)
                # Disable user's click 
                self.board.cursor = None   # "watch"
                # ?? A way to disable mouse-click temporarely with Game2DBoard library...

                # Make the move, actually. Board update, disk paint, disks fliped, etc.

                self.make_current_move()

            else:
                print("Current move is NOT legal: ",r," ", c)
                return
        self.board.cursor = "arrow"

         # Check if the game is over if no moves are possible by AI-computer 
        # or if the board is full of disks
        
        if self.is_game_over():
            return
        else:
            #self.play_as_ai_computer_player() (COMMENTED BECAUSE IT IS COUPLED)
            # 2. Play the computer-AI turn
            # Start a Timer (for just one trigger ONLY) for AI-Computer to move
            # This is the way to decouple the computer-AI move
            # from the human-user's click, so user's move is painted first
            # Otherwise user's move and AI-computer move would be painted at the same time.
            # GitHub issue related: https://github.com/ADRIANDLT/Othello-IE-Proyect/issues/2
            self.board.start_timer(2000)



    def evaluate_move(self, move):
        score = 0

        # Disk flipping score
        flipping_score = sum(self.direction_has_disk_to_flip(move, direction, self.current_player)
                             for direction in POSSIBLE_MOVE_DIRECTIONS)
        score += flipping_score

        # Board position score
        if move in [(0, 0), (0, self.board_size_n - 1), (self.board_size_n - 1, 0),
                    (self.board_size_n - 1, self.board_size_n - 1)]:
            score += 100  # High score for corners
        elif move[0] in [0, self.board_size_n - 1] or move[1] in [0, self.board_size_n - 1]:
            score += 50  # High score for edges

        # Mobility and future opportunities
        # Temporarily make the move and evaluate the opponent's response
        original_value = self.board[move[0]][move[1]]
        self.board[move[0]][move[1]] = self.current_player
        opponent_moves = self.get_possible_moves_by_player(3 - self.current_player)
        self.board[move[0]][move[1]] = original_value  # Revert the temporary move

        mobility_score = -len(opponent_moves)  # Less opponent moves is better
        score += mobility_score

        # Stability (more complex to evaluate, can be added later)

        return score
    
    def make_best_move_by_current_player(self):
        possible_moves = self.get_possible_moves_by_current_player()
        if possible_moves:
            # Evaluate each move and choose the one with the highest score
            best_move = max(possible_moves, key=lambda move: self.evaluate_move(move))
            self.current_move = best_move
            self.make_current_move()

    def play_as_ai_computer_player(self):
        # First of all, disable the Timer so it doesn't get triggered again, automatically.
        self.board.stop_timer()

        self.board.cursor = None

        self.current_player = 2
        # 1. Play the AI-computer´s turn
        if self.current_player_can_move():
            print("Current player(AI-Computer) has possible move(s). Player ID: ", self.current_player)
            time.sleep(2)
            self.make_best_move_by_current_player()
    

    # (ADLT) Returns a list of possible moves that can be made by the current player
    # (ADLT) This is an example of usage of a Linked List, adding moves with .append()
    # (TO DO) Evaluate if instead of linked list, a tree is better to store the possible moves
        # depending on the real AI algorithm to be used.
    def get_possible_moves_by_current_player(self, player_number=None):
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

    def is_game_over(self):
        if not self.player_can_move(1) and not self.player_can_move(2):
            if self.num_disks_dictionary[1] > self.num_disks_dictionary[2]:
                print('*****************')
                print('Wooohooo! You won!! Congrats!!')
                self.board.print(MSG + ' -- Wooohooo! You won!! Congrats!!')
            elif self.num_disks_dictionary[1] < self.num_disks_dictionary[2]:
                print('*****************')
                print('Too bad, you lost!! The computer won!! ;)')
                self.board.print(MSG + ' -- Too bad, you lost!! The computer won!! ;)')

            return True
        
        else:
            return False # Game is not over yet

        # (ADLT) TO DO CLEAN UP BELOW IF NOT NEEDED

        # total_disks_on_board = self.num_disks_dict[1] + self.num_disks_dict[2]
        
        # (ADLT) Conditions for who won probably needs to improve...
        # If a player cannot move, then the one who has more disks wins? Or the other moves?
        
       # message_for_human_winner = " ****** Wooohooo! You won!! Congrats!!****** "
       # message_for_computer_ai_winner = " ****** Too bad!! The computer won!! ;) ****** "


        # if total_disks_on_board == self.n ** 2:
            # if self.num_disks_dict[1] > self.num_disks_dict[2]:
                    # print('*****************')
                    # print(message_for_human_winner)
                    # self.board.print(MSG + message_for_human_winner)
            # else:
                    # print('*****************')
                    # print(message_for_computer_ai_winner)
                    # self.board.print(MSG + message_for_computer_ai_winner)

    def move_has_disk_to_flip(self, move, player_number):
        ''' 
            Checks whether the player's move is possible.
            move parameter is a tuple of coordinates (row, col)
            Returns: boolean (True if move is possible, False if not)
        '''

        content_of_move_cell = self.board[move[0]][move[1]]

        # print(self.board)

        if move != () and self.coord_is_valid(move[0], move[1]) \
           and content_of_move_cell == None:
            for direction in POSSIBLE_MOVE_DIRECTIONS:
                # print("Direction: ",direction)
                has_disk_to_flip = self.direction_has_disk_to_flip(move, direction, player_number)
                if has_disk_to_flip:
                    return True
                     
        return False


    def current_player_can_move(self):
        ''' 
            Returns: True if the current player has possible moves, False if not.
        ''' 
        return self.player_can_move(self.current_player)
    
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

    def coord_is_valid(self, row, col):
        '''
            Returns: True if row and col are valid, False if not.
            A valid coordinate must be in the range of the board.
        '''
        if 0 <= row < self.board_size_n and 0 <= col < self.board_size_n:
            return True
        return False
    
    #(ADLT) 
    # This is a very interesting function, since it checks 
    # if there is any disk to flip and it calculates also how many disks to flip.
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
    
    def save_moves(self):
        state = {
            # "board": [[self.board[r][c] for c in range(self.board.ncols)] for r in range(self.board.nrows)],
            "board": self.copy_board_cell_states(),
            "current_player": self.current_player,
            "num_disks_dictionary": self.num_disks_dictionary.copy()
        }
        self.algo_stack.append(state)
        print("Saved state: ", state)
    
    def copy_board_cell_states(self):
        board_cell_states = [[None for _ in range(8)] for _ in range(8)]
        rows_array = range(0, self.board.nrows, 1)
        cols_array = range(0, self.board.ncols, 1)
        for row in rows_array:
            for col in cols_array:
                board_cell_states[row][col] = self.board[row][col]

        return board_cell_states


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
            False

    def make_current_move(self):
        ''' 
            Puts a disk for the player's current move on the board 
            and then flips the contrary's disks in between. 
            The update of the disks is made by changing the board's states 
            (1 for black disks and 2 for white disks), 
            and increasing the number of disks of the current player by 1.
            (flip_disks_for_current_move() function should also increase 
            the number of disks of the current player by 1)
        '''
        

        if self.move_has_disk_to_flip(self.current_move, self.current_player): # (ADLT) This is redundant, since we already checked this in play()
            # Put current player color on the current move cell
            self.board[self.current_move[0]][self.current_move[1]] = self.current_player
            # Adds 1 disk to the current players disk count
            self.num_disks_dictionary[self.current_player] += 1
            
            self.flip_disks_for_current_move()
            self.save_moves()  # Save state after making a move

    def flip_disks_for_current_move(self):
        '''
            Flips the contrary's disks for the current move being applied by 
            updating the board's states:
            "1" state for black disks and "2" state for white disks.
            Also, per each flip, increases the number of disks for the current player by 1, 
            and decreases for the contrary.
        '''
        current_disk_type = self.current_player 
        for direction in POSSIBLE_MOVE_DIRECTIONS:
            if self.direction_has_disk_to_flip(self.current_move, direction, self.current_player):
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
                    row = self.current_move[0] + direction[0] * distance
                    col = self.current_move[1] + direction[1] * distance
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