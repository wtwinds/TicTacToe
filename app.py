from flask import Flask, render_template, request, redirect, url_for,jsonify
from isba_logic import is_valid_move, check_win, check_draw
from tic_tac_toe_part import create_empty_board
from computer_logic import computer_move
from multiplayer_logic import create_new_game, join_game, make_move, games

app = Flask(__name__)
app.secret_key = "super_secret_key"




# ------------------------------
# GLOBAL GAME STATE VARIABLES
# ------------------------------
board = create_empty_board()
players = {"X": "", "O": ""}
current_player = "X"
mode = "offline"
wins = {"X": 0, "O": 0}
losses = {"X": 0, "O": 0}
draws = {"X": 0, "O": 0}
winner = None
winning_positions = []
difficulty = "easy"

@app.route("/play_online")
def play_online():
    code = create_new_game()
    return render_template("multiplayer.html", code=code, player='X')

@app.route("/join_game", methods=["GET", "POST"])
def join_game_route():
    if request.method == "POST":
        code = request.form["code"]
        if join_game(code, "O"):
            return redirect(url_for("multiplayer_board", code=code, player='O'))
        else:
            return render_template("join_game.html", error="Invalid or full game code")
    return render_template("join_game.html")

@app.route("/multiplayer/<code>/<player>")
def multiplayer_board(code, player):
    game = games.get(code)
    if not game:
        return "Game not found", 404
    return render_template("multiplayer.html", code=code, player=player)

@app.route("/move_online", methods=["POST"])
def move_online():
    code = request.form["code"]
    row = int(request.form["row"])
    col = int(request.form["col"])
    make_move(code, row, col)
    return jsonify(games[code])

@app.route("/get_state/<code>")
def get_state(code):
    return jsonify(games.get(code, {}))






# ------------------------------
# ROUTES
# ------------------------------
@app.route('/')
def home():
    """Homepage route."""
    global board, current_player, winner, wins, losses, winning_positions, draws
    board = create_empty_board()
    current_player = "X"
    winner = None
    winning_positions = []
    wins = {"X": 0, "O": 0}
    losses = {"X": 0, "O": 0}
    draws = {"X": 0, "O": 0}
    return render_template('homepage.html')


@app.route('/offline_mode')
def offline_mode():
    """Offline mode player name input page."""
    return render_template('playernameinput.html')


@app.route('/start_offline', methods=['POST'])
def start_offline():
    """Start offline mode with two players."""
    global board, current_player, players, mode, winner, winning_positions
    players["X"] = request.form.get('player1', 'Player 1')
    players["O"] = request.form.get('player2', 'Player 2')
    board = create_empty_board()
    current_player = "X"
    winner = None
    winning_positions = []
    mode = "offline"
    return redirect(url_for('game'))


@app.route('/computer_mode')
def computer_mode():
    """Display computer difficulty selection page."""
    return render_template('vs_computer.html')


@app.route('/start_computer', methods=['POST'])
def start_computer():
    """Start game vs computer."""
    global board, current_player, players, mode, winner, winning_positions, difficulty
    players["X"] = request.form.get('player', 'You')
    players["O"] = "Computer"
    difficulty = request.form.get('difficulty', 'easy')
    board = create_empty_board()
    current_player = "X"
    winner = None
    winning_positions = []
    mode = "computer"
    return redirect(url_for('game'))


@app.route('/game')
def game():
    """Main game display."""
    return render_template(
        'game.html',
        player1=players.get("X", "Player 1"),
        player2=players.get("O", "Player 2"),
        wins=wins,
        losses=losses,
        draws=draws,
        board=board,
        current_player=current_player,
        winner=winner,
        winning_positions=winning_positions
    )


@app.route('/move', methods=['POST'])
def move():
    """Handle player moves and computer responses."""
    global board, current_player, wins, losses, mode, winner, winning_positions, draws

    try:
        row = int(request.form['row'])
        col = int(request.form['col'])
    except (KeyError, ValueError):
        return redirect(url_for('game'))

    if not is_valid_move(board, row, col) or winner is not None:
        return redirect(url_for('game'))

    # Make the move
    board[row][col] = current_player
    win, positions = check_win(board, current_player)
    if win:
        winner = players[current_player]
        winning_positions = positions
        wins[current_player] += 1
        losses["O" if current_player == "X" else "X"] += 1
        return redirect(url_for('game'))

    if check_draw(board):
        winner = "Draw"
        winning_positions = []
        draws["X"] += 1
        draws["O"] += 1
        return redirect(url_for('game'))

    # Switch player
    current_player = "O" if current_player == "X" else "X"

    # Computer's turn
    if mode == "computer" and current_player == "O":
        move = computer_move(board, "O", "X")
        if move:
            r, c = move
            board[r][c] = "O"
            win, positions = check_win(board, "O")
            if win:
                winner = players["O"]
                winning_positions = positions
                wins["O"] += 1
                losses["X"] += 1
                return redirect(url_for('game'))

            if check_draw(board):
                winner = "Draw"
                winning_positions = []
                draws["X"] += 1
                draws["O"] += 1
                return redirect(url_for('game'))

            current_player = "X"

    return redirect(url_for('game'))


@app.route('/restart')
def restart():
    """Restart the current game."""
    global board, current_player, winner, winning_positions
    board = create_empty_board()
    current_player = "X"
    winner = None
    winning_positions = []
    return redirect(url_for('game'))


@app.route('/reset_all')
def reset_all():
    """Reset scores and restart."""
    global board, current_player, winner, wins, losses, winning_positions, draws
    board = create_empty_board()
    current_player = "X"
    winner = None
    winning_positions = []
    wins = {"X": 0, "O": 0}
    losses = {"X": 0, "O": 0}
    draws = {"X": 0, "O": 0}
    return redirect(url_for('game'))


@app.route('/about_page')
def about_page():
    """About page."""
    return render_template('about.html')


@app.route('/result')
def result():
    """Result display page."""
    return render_template(
        'result.html',
        board=board,
        winner=winner,
        winning_positions=winning_positions
    )


if __name__ == '__main__':
    app.run(debug=True)
