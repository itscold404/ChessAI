import chess
# from chessboard import display
# from time import sleep
from chessAI import *
# # https://python-chess.readthedocs.io/en/latest/

# # board.fen() -- get fen() representation of current board
# # board.set_fen("fen") -- set the board to the fen representation

# # while True:
# #     display.check_for_quit()
# #     display.update(valid_fen, game_board)




SEARCH_DEPTH = 5      # depth at which the AI will perform minimax search
# board = chess.Board()

# c_ai = chessAI(board, SEARCH_DEPTH)

# board.push(c_ai.select_move())
# print(board)
# Remaining imports
import chess.svg
import chess.pgn
import chess.engine
# from IPython.display import SVG
import traceback
from flask import Flask, Response, request
import webbrowser
import time

board = chess.Board()

c_ai = chessAI(board, SEARCH_DEPTH)

#Searching Ai's Move
def aimove():
    move = c_ai.select_move()
    board.push(move)
# Searching Stockfish's Move
def stockfish():
    engine = chess.engine.SimpleEngine.popen_uci(
        "your_path/stockfish.exe")
    move = engine.play(board, chess.engine.Limit(time=0.1))
    board.push(move.move)
app = Flask(__name__)
# Front Page of the Flask Web Page
@app.route("/")
def main():
    global count, board
    ret = '<html><head>'
    ret += '<style>input {font-size: 20px; } button { font-size: 20px; }</style>'
    ret += '</head><body>'
    ret += '<img width=510 height=510 src="/board.svg?%f"></img></br></br>' % time.time()
    ret += '<form action="/game/" method="post"><button name="New Game" type="submit">New Game</button></form>'
    ret += '<form action="/undo/" method="post"><button name="Undo" type="submit">Undo Last Move</button></form>'
    ret += '<form action="/move/"><input type="submit" value="Make Human Move:"><input name="move" type="text"></input></form>'
    ret += '<form action="/dev/" method="post"><button name="Comp Move" type="submit">Make Ai Move</button></form>'
    ret += '<form action="/engine/" method="post"><button name="Stockfish Move" type="submit">Make Stockfish Move</button></form>'
    return ret
# Display Board
@app.route("/board.svg/")
def board():
    return Response(chess.svg.board(board=board, size=700), mimetype='image/svg+xml')
# Human Move
@app.route("/move/")
def move():
    try:
        move = request.args.get('move', default="")
        board.push_san(move)
    except Exception:
        traceback.print_exc()
    return main()
# Make Ai’s Move
@app.route("/dev/", methods=['POST'])
def dev():
    try:
        aimove()
    except Exception:
        traceback.print_exc()
    return main()
# Make UCI Compatible engine's move
@app.route("/engine/", methods=['POST'])
def engine():
    try:
        stockfish()
    except Exception:
        traceback.print_exc()
    return main()
# New Game
@app.route("/game/", methods=['POST'])
def game():
    board.reset()
    return main()
# Undo
@app.route("/undo/", methods=['POST'])
def undo():
    try:
        board.pop()
    except Exception:
        traceback.print_exc()
    return main()

board = chess.Board()
webbrowser.open("http://127.0.0.1:5000/")
app.run()