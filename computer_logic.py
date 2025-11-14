import random
from isba_logic import check_win

def computer_move(board, computer_symbol="O", player_symbol="X"):
    """Smart computer move: tries to win, block, or pick best spot."""
    empty_positions = [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

    # Try to win
    for r, c in empty_positions:
        board[r][c] = computer_symbol
        win, _ = check_win(board, computer_symbol)
        board[r][c] = " "
        if win:
            return (r, c)

    # Try to block player
    for r, c in empty_positions:
        board[r][c] = player_symbol
        win, _ = check_win(board, player_symbol)
        board[r][c] = " "
        if win:
            return (r, c)

    # Pick center
    if (1, 1) in empty_positions:
        return (1, 1)

    # Pick a corner
    for pos in [(0, 0), (0, 2), (2, 0), (2, 2)]:
        if pos in empty_positions:
            return pos

    # Pick any remaining spot
    return random.choice(empty_positions) if empty_positions else None