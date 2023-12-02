from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    print('This is game_id', game_id)
    game = BoggleGame()
    games[game_id] = game

    print('This is game.board', game.board)
    return jsonify({"game_id": game_id, "board": game.board})


@app.post('/api/score-word')
def handle_score_word():
    """Handles scoring word from AJAX POST request
    Expect to receive as a POST request a JSON string of
    {"game_id": "valid_game_id", "word": "word"}

    Returns one of three responses as JSON string:
    If not valid word - {"result": "not-word"}
    If not on board - {"result": "not-on-board"}
    If valid word and on board - {"result": "ok"}
    """

    word = request.json["word"]
    print('This is word', word)

    game_id = request.json["game_id"]
    print('This is game_id', game_id)

    print('This is games', games)

    game = games[game_id]

    print('This is single game', game)

    word_in_list = game.is_word_in_word_list(word)
    # returns True if in word list and false if not

    print('This is word_in_list', word_in_list)
    if not word_in_list:
        print('If statement not word_in_list went thru')
        return jsonify({"result": "not-word"})

    word_on_board = game.check_word_on_board(word)

    if not word_on_board:
        return jsonify({"result": "not-on-board"})

    return jsonify({"result": "ok"})

    # when do we check for is_word_not_a_dup ?