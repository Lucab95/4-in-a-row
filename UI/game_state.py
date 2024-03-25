import random
from move import Move
class GameState:
    """Class representing the state of a Connect Four game.
    
    The game is played on a 6x7 board reprensented by a 2D list, initially filled with '-'.
    Players can place their pieces in any column, and the piece will fall to the lowest possible row.
    The game is won by placing four pieces in a row, column, or diagonal.
    When the game starts it will ask for the number of players: 
    - if the number is 1 the game will be played against the computer.
        The computer takes his moves randomly - possible improvement would be to implement a simple ai with a minimax algorithm.
    - if the number is 2 the game will be played by two players, and they will choose the moves alternatively.

    The design of the class is simple, it has a constructor that initializes the game state, a method to get the valid moves,
    a method to perform a move, a method to check if the current player won the game and a method to check if the board is full,
    in this case the outcome will be a draw. 
    The game loop is started by the start_game method, that will print the current board, ask for the next move,
    if the move is valid it will be performed and board will be updated. At this point, the gameState will check if 
    the current player won or if the board is full. If one of the endgame conditions is met the game will end printing the result.
    If the game is not over the current player will be updated and the loop will continue until one of the two endgame conditions is met.

    """

    def __init__(self, rows: int, columns: int, num_players: int) -> None:
        """Initialize the game state.
        
        Args:
            rows (int): The number of rows in the game board.
            columns (int): The number of columns in the game board.
            num_players (int): The number of players in the game.
        """
        self.rows = rows
        self.columns = columns
        self.num_players = num_players
        self.board = [["-"] * columns for _ in range(rows)]
        self.current_player = random.randint(0, 1)
        self.blue_to_move = True
        self.player_simbol = ["o", "x"]
        self.running = True
        self.letters = (["0", "1", "2", "3", "4", "5", "6"])
        self.numbers = (["6","5", "4", "3", "2", "1"])
        self.history = []
        self.turn_counter = 0
        self.control_blue = random.randint(0, 1)
    
    def get_valid_moves(self) -> list:
        """Get a list of valid moves.
        
        Returns:
            list: A list with the possilbe moves."""
        
        return [Move(col, self.board) for col in range(self.columns) if self.board[0][col] == "-"]
    
    def perform_move(self, move: Move, player: str) -> None:
        """perform a move in the game board.
        
        Args:
            move (int): The column where the player wants to place the piece.
            player (str): The player that is performing the move.
        """
        col = move.col
        for row in range(self.rows -1, -1, -1):
            print(row, col, self.board[row][col])
            if self.board[row][col] == "-":
                self.board[row][col] = self.player_simbol[player]
                self.blue_to_move = not self.blue_to_move
                break

        if self.is_winner(player):
            self.running = False
            self.win = self.player_simbol[player]
        if self.is_board_full():
            self.running = False
            self.win = "draw"

    def is_winner(self, player) -> bool:
        """Check if the current player won the game
        
        Args: player (int): The player number to check if it has reached a winning position.
        
        Returns:
            bool: True if the player won, False otherwise.
        """

        player = self.player_simbol[player]
        for row in range(self.rows):
            for col in range(self.columns):
                if self.board[row][col] == player:
                    # Check horizontal
                    if col + 3 < self.columns and all(self.board[row][col+i] == player for i in range(4)):
                        return True
                    # Check vertical
                    if row + 3 < self.rows and all(self.board[row+i][col] == player for i in range(4)):
                        return True
                    # Check diagonal (top-left to bottom-right)
                    if row + 3 < self.rows and col + 3 < self.columns and all(self.board[row+i][col+i] == player for i in range(4)):
                        return True
                    # Check diagonal (bottom-left to top-right)
                    if row - 3 >= 0 and col + 3 < self.columns and all(self.board[row-i][col+i] == player for i in range(4)):
                        return True
        return False
    
    def is_board_full(self) -> bool:
        """Check if the board is full.

        Returns:
            bool: True if the board is full, False otherwise.
        """

        return all(self.board[0][col] != "-" for col in range(self.columns))

    def print_state(self) -> None:
        """Print the current state of the game."""

        cols_index = "" + ' '.join(map(str, range(game.columns)))
        for i, row in enumerate(self.board[::-1]):
            print(' '.join(row))
        print(cols_index)