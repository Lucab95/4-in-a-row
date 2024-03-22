from main import GameState
import unittest

class Test(unittest.TestCase):

    def setUp(self):
        self.game = GameState(6, 7)

    def test_is_valid_move(self):
        self.assertTrue(0 in self.game.get_valid_moves() )
        self.assertTrue(6 in self.game.get_valid_moves())
        self.assertFalse(-1 in self.game.get_valid_moves())
        self.assertFalse(7 in self.game.get_valid_moves())
        self.assertFalse("j" in self.game.get_valid_moves())
        
    
    def test_horizontal_winner(self):
        for i in range(4):
            self.game.perform_move(i, 0)
        self.assertTrue(self.game.is_winner(0))
    
    def test_vertical_winner(self):
        for i in range(4):
            self.game.perform_move(2, 0)
        self.assertTrue(self.game.is_winner(0))
    
    def test_diagonal_winner(self):
        self.game.board[0][0] = "o"
        self.game.board[1][1] = "o"
        self.game.board[2][2] = "o"
        self.game.board[3][3] = "o"
        self.assertTrue(self.game.is_winner(1))
    
    def test_full_column(self):
        for i in range(6):
            self.game.perform_move(0, 0)
        self.assertTrue(0 not in self.game.get_valid_moves())
    
    def test_full_board(self):
        for i in range(6):
            for j in range(7):
                self.game.perform_move(j, j%2)
        self.assertTrue(self.game.is_board_full())