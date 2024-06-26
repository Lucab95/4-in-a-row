import random
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
        self.player_simbol = ["o", "x"]
        self.running = True
    
    def get_valid_moves(self) -> list:
        """Get a list of valid moves.
        
        Returns:
            list: A list with the possilbe moves."""
        
        return [col for col in range(self.columns) if self.board[self.rows -1][col] == "-"]
    
    def perform_move(self, move: int, player: str) -> None:
        """perform a move in the game board.
        
        Args:
            move (int): The column where the player wants to place the piece.
            player (str): The player that is performing the move.
        """
        
        for row in range(self.rows):
            if self.board[row][move] == "-":
                self.board[row][move] = self.player_simbol[player]
                break

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

        return all(self.board[self.rows-1][col] != "-" for col in range(self.columns))

    def print_state(self) -> None:
        """Print the current state of the game."""

        cols_index = "" + ' '.join(map(str, range(game.columns)))
        for i, row in enumerate(self.board[::-1]):
            print(' '.join(row))
        print(cols_index)

    def start_game(self):
        """Start the game loop."""

        self.print_state()

        while self.running:
            print("-------------------")
            valid_moves = self.get_valid_moves()
            if self.num_players ==1 and self.current_player == 1:
                move = random.choice(valid_moves)
            else:
                move = input(f"Player '{self.player_simbol[self.current_player]}',  enter your move: ")
                # To only allow integers, if not a digit the move will be invalidated 
                if move.isdigit(): 
                    move = int(move)
            
            if move in valid_moves:
                self.perform_move(move, self.current_player)
                self.print_state()
                print(f"Player '{self.player_simbol[self.current_player]}' added a disc in column {move}")
                if self.is_winner(self.current_player):
                    print(f"Player {self.current_player} wins!")
                    self.running = False
                elif self.is_board_full():
                    print("It's a draw!")
                    self.running = False
                self.current_player = 1 - self.current_player
                
            else:
                print("Invalid move. Try again.")

if "__main__" == __name__:
    
    print("***Welcome to Connect Four!***")

    players_number = input("Enter number of players (1 or 2): ")
    if players_number.isdigit() and int(players_number) in [1, 2]:
        game = GameState(6, 7, int(players_number))
        game.start_game()
    else:
        raise ValueError("Invalid number of players. Please enter 1 or 2.")
    