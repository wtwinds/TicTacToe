# --- Isba's Part: Validation + Win/Draw Detection ---

def is_valid_move(board, row, col):
    """Return True if the move is allowed (cell empty)."""
    return board[row][col] == " "


def check_win(board, player):
    """Return (True, winning_positions) if player wins, else (False, [])"""
    win_conditions = [
        [(0, 0), (0, 1), (0, 2)],  # rows
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],  # columns
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],  # diagonals
        [(0, 2), (1, 1), (2, 0)]
    ]
    for combo in win_conditions:
        if all(board[r][c] == player for r, c in combo):
            return True, combo
    return False, []

def check_draw(board):
    """Check if the board is full and there is no winner."""
    return all(cell != " " for row in board for cell in row)


# --- Testing Section (only for manual check) ---
if __name__ == "__main__":
    # Example 3x3 board
    board = [
        ["X", "O", "X"],
        ["X", "O", "O"],
        ["O", "X", " "]
    ]

    print("Valid move check (row 2, col 2):", is_valid_move(board, 2, 2))  # True (empty)
    print("Valid move check (row 0, col 0):", is_valid_move(board, 0, 0))  # False (already X)
    print("X wins?", check_win(board, "X"))  # False
    print("O wins?", check_win(board, "O"))  # False
    print("Draw?", check_draw(board))        # False (still one empty)
