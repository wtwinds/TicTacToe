# tic_tac_toe_part.py
"""
Simple Tic-Tac-Toe UI (text) + two-player alternating input (row, col).
This file implements:
 - Displaying a 3x3 grid with symbols
 - Two-player mode (Player X and Player O)
 - Taking turns by entering row and column (1-3)
 - Input validation and "cell already taken" handling
 - 'q' to quit anytime
No win/draw logic included (since your task only asked for display + alternating input).
"""

def create_empty_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def print_board(board):
    # Nicely formatted grid using box-like separators
    print("\n   1   2   3")
    for r in range(3):
        row_cells = [f" {board[r][c]} " for c in range(3)]
        print(f"{r+1} " + "|".join(row_cells))
        if r < 2:
            print("  ---+---+---")
    print()

def get_move(player):
    """
    Prompt player to enter row and column.
    Accepts either:
      - two numbers separated by space or comma (e.g. "2 3" or "2,3")
      - or one by one prompting
    Returns tuple (row_index, col_index) 0-based, or None if player chose to quit.
    """
    prompt = f"Player {player} — enter row and column (1-3), or 'q' to quit: "
    while True:
        s = input(prompt).strip()
        if not s:
            continue
        if s.lower() == 'q':
            return None
        # try parse "r c" or "r,c"
        for sep in (" ", ","):
            if sep in s:
                parts = [p.strip() for p in s.split(sep) if p.strip() != ""]
                if len(parts) >= 2:
                    try:
                        r = int(parts[0])
                        c = int(parts[1])
                        if 1 <= r <= 3 and 1 <= c <= 3:
                            return (r-1, c-1)
                    except ValueError:
                        pass
        # if single number given, ask for second
        try:
            x = int(s)
            if 1 <= x <= 3:
                # ask for the other coordinate
                y = input("Enter the other coordinate (1-3), or 'q' to quit: ").strip()
                if y.lower() == 'q':
                    return None
                try:
                    y = int(y)
                    if 1 <= y <= 3:
                        # decide whether first was row or col — we'll treat first as row
                        return (x-1, y-1)
                except ValueError:
                    pass
        except ValueError:
            pass

        print("Invalid input. Use formats like '2 3' or '1,1' (rows and columns are 1–3).")

def main():
    board = create_empty_board()
    current = "X"  # X starts
    print("=== Tic-Tac-Toe (Display + 2-player alternating input) ===")
    print("Players take turns. Input row and column numbers (1 to 3). Type 'q' to quit.\n")
    while True:
        print_board(board)
        move = get_move(current)
        if move is None:
            print("Game exited. Bye!")
            break
        r, c = move
        if board[r][c] != " ":
            print(f"Cell ({r+1},{c+1}) already taken — choose another cell.")
            continue
        board[r][c] = current
        # Alternate player
        current = "O" if current == "X" else "X"

if __name__ == "__main__":
    main()