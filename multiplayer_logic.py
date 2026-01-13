import random

games = {}

def create_new_game():
    code = str(random.randint(1000, 9999))
    games[code] = {
        "board": [["" for _ in range(3)] for _ in range(3)],
        "turn": "X",
        "winner": None,
        "players": []
    }
    return code


def join_game(code, player):
    game = games.get(code)
    if not game:
        return False

    if player not in game["players"] and len(game["players"]) < 2:
        game["players"].append(player)
        return True
    return False



def make_move(code, row, col):
    game = games.get(code)
    if not game or game["winner"]:
        return False

    if game["board"][row][col] == "":
        game["board"][row][col] = game["turn"]

        if check_winner(game["board"]):
            game["winner"] = game["turn"]
        elif all(cell for row in game["board"] for cell in row):
            game["winner"] = "Draw"
        else:
            game["turn"] = "O" if game["turn"] == "X" else "X"
        return True
    return False


def check_winner(b):
    for i in range(3):
        if b[i][0] == b[i][1] == b[i][2] != "":
            return True
        if b[0][i] == b[1][i] == b[2][i] != "":
            return True
    if b[0][0] == b[1][1] == b[2][2] != "":
        return True
    if b[0][2] == b[1][1] == b[2][0] != "":
        return True
    return False
