import unittest
from isba_logic import is_valid_move, check_win, check_draw

class TestGameLogic(unittest.TestCase):
    def test_valid_move(self):
        board = [["X", "O", " "], [" ", "X", "O"], ["O", "X", " "]]
        self.assertTrue(is_valid_move(board, 0, 2))
        self.assertFalse(is_valid_move(board, 0, 0))

    def test_check_win(self):
        board = [["X", "X", "X"], ["O", "O", " "], [" ", " ", " "]]
        win, pos = check_win(board, "X")
        self.assertTrue(win)
        self.assertEqual(pos, [0, 1, 2])

    def test_check_draw(self):
        board = [["X", "O", "X"], ["X", "O", "O"], ["O", "X", "X"]]
        self.assertTrue(check_draw(board))

if __name__ == '__main__':
    unittest.main()