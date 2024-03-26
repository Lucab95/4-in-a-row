class Move():
    # maps keys to values for connect4 game
    # key : value
    # rank : row
    # file : col
    filesToCols = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6}
    colsToFiles = {v: k for k, v in filesToCols.items()}
    

    def __init__(self, col, board):
        # The column where the piece is played.
        self.col = col
        self.row = self.getFirstEmptyRow(board, col)
        self.piecePlayed = 'o' if board.count('o') <= board.count('x') else 'x' # Assume R starts
        self.moveID = self.row * 10 + self.col  # Simple unique ID for the move
    """
    Override equals method"""

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def __hash__(self):
        return self.moveID

    def getFirstEmptyRow(self, board, col):
        for row in range(len(board)):
            if board[row][col] == '-':  # Assuming '-' is the symbol for an empty cell
                return row
        return -1  # If the column is full, return -1
    
    def getNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + "->" + self.getRankFile(self.endRow, self.endCol)
