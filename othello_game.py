from game2dboard import Board

# Key commands
MSG = "ESC: Close    F2: Restart"

# Defines sizes of the square and tile, colors of the board, line, 
# and tile as constants
GAME_WINDOW_TITLE = "Othello"
CELL_SIZE = 80
CELL_COLOR = "green"
CELL_SPACING = 2
LINE_COLOR = "black"

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
        self.n = min(self.board.nrows, self.board.ncols)
        
        # Event-Handlers initialization
        '''
        Assign the keyboard_command and initialize_game_settings methods as event handlers, 
        so we just specify not execute their code.
        By omitting the parentheses, we are assigning the methods themselves as event handlers
        '''
        self.board.on_key_press = self.keyboard_command
        self.board.on_start = self.initialize_game_settings

    def keyboard_command(self, key):
        if key == "Escape":
            self.board.close()
        elif key == "F2":
            self.initialize_game_settings()

    def initialize_game_settings(self):
            
        # Game settings initialization
        self.current_player = 1
        self.num_disks = [2, 2]

        if self.n < 2:
            return
        
        # Disks initialization (Draw the first 4 disks in the middle of the board)
        '''
        If the board cols and rows are both 2 or greater, 
        the method calculates the coordinates of the four initial disks and 
        stores them in the initial_cells list. 
        The coord1 and coord2 variables are calculated as the floor division 
        of self.n / 2 - 1 and self.n / 2, respectively, where self.n is the size of the board.
        '''
        coord1 = int(self.n / 2 - 1)
        coord2 = int(self.n / 2)
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

    def start_game(self):
        self.board.show()
    

