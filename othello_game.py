from game2dboard import Board

import time

# Key commands
MSG = "ESC: Close    F2: Restart"

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

class Game:
    def __init__(self, board_width=8, board_height=8):

        # Board initialization
        self.board = Board(board_width, board_height)
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
        so we just specify not execute their code.
        By omitting the parentheses, we are assigning the methods themselves as event handlers
        '''
        self.board.on_key_press = self.keyboard_command
        self.board.on_start = self.initialize_game_settings
        self.board.on_mouse_click = self.play

    def keyboard_command(self, key):
        if key == "Escape":
            self.board.close()
        elif key == "F2":
            self.initialize_game_settings()

    def initialize_game_settings(self):
            
        # Game settings initialization
        self.current_player = 1
        self.num_disks = [2, 2]

        if self.board_size_n < 2:
            return
        
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
            # self.draw_tile(initial_squares[i], color)
        
        print(self.board)

        self.board.print(MSG)

    def run(self):
        self.board.show()
    
    # (ADLT) Triggered when the user clicks on the board
    # It won't directly get thru here if the computer is thinking/moving, though.
    def play(self, btn, r, c):
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
            
            if self.move_has_disk_to_flip(self.current_move):
                print("Current move HAS disks around to flip: ",r," ", c)
                # (ADLT)
                # Disable user's click 
                self.board.cursor = "None"   # "watch"
                # ?? A way to disable mouse-click temporarely with Game2DBoard library...

                # Make the move, actually. Board update, disk paint, disks fliped, etc.

                # ADLT Current point

               # TO DO self.make_current_move()
            else:
                print("Current move is NOT legal: ",r," ", c)
                return
        self.board.cursor = "arrow"

    def move_has_disk_to_flip(self, move):
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
                print("Direction: ",direction)
                if self.direction_has_disk_to_flip(move, direction):
                    return True     
        return False

    def current_player_can_move(self):
        return True #TBD Will implement the logic for this
    
    def coord_is_valid(self, row, col):
        '''
            Returns: True if row and col are valid, False if not.
            A valid coordinate must be in the range of the board.
        '''
        if 0 <= row < self.board_size_n and 0 <= col < self.board_size_n:
            return True
        return False
    
    #(CDLTLL) 
    # This is a very interesting function, since it checks 
    # if there is any disk to flip and it calculates also how many disks to flip.
    def direction_has_disk_to_flip(self, move, direction):

        #    Parameters: move (tuple), direction (tuple)
        #    Returns: True if there is any disk to flip, False if not.
        #    Checks if the player has any adversary's disk to flip with the move to make.
        #    move is the (row, col) coordinate of where the player makes a move; 
        #    direction is the direction in which the adversary's disk/s are to be flipped 

        #claculate disk type to flip
        disk_type_to_flip = 3 - self.current_player
        disk_type_current_player = self.current_player

        i = 1
        while True:
            row = move[0] + direction[0] * i
            col = move[1] + direction[1] * i

            if not self.coord_is_valid(row, col) or \
                    self.board[row][col] == None:  # Empty cell
                    return False
            elif self.board[row][col] == disk_type_current_player:  
                # Current player color disk found, so stop direction and exit
                break
            else:
                # Disk color is the one to flip, so continue looking in the same direction
                if self.board[row][col] == disk_type_to_flip:
                    print("Found disk to flip: ", row, ",", col, "content:", self.board[row][col])
                    i += 1
        
        return i > 1  # At least it should be 2, since 1 started on 1 plus one found = 2