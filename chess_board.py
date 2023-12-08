import chess
from chessAI import *
import chess.svg
import chess.pgn
import chess.engine
import traceback
from flask import Flask, Response, request
import webbrowser
import time

SEARCH_DEPTH = 5      # depth at which the AI will perform minimax search
    
#------------------------------------------
# Searching Ai's Move
#------------------------------------------
def aimove():
    move = c_ai.select_move()
    c_ai.push(move)

app = Flask(__name__)

#------------------------------------------
# Front Page of the Flask Web Page\
#------------------------------------------
@app.route("/")
def main():
    global count, c_ai
    ret = '<html><head>'
    ret += '<style>input {font-size: 20px; } button { font-size: 20px; }</style>'
    ret += '</head><body>'
    ret += '<img width=510 height=510 src="/board.svg?%f"></img></br></br>' % time.time()
    ret += '<form action="/game/" method="post"><button name="New Game" type="submit">New Game</button></form>'
    ret += '<form action="/undo/" method="post"><button name="Undo" type="submit">Undo Last Move</button></form>'
    ret += '<form action="/move/"><input type="submit" value="Make Human Move:"><input name="move" type="text"></input></form>'
    ret += '<form action="/dev/" method="post"><button name="Comp Move" type="submit">Make Ai Move</button></form>'
    return ret

#------------------------------------------
# Display Board
#------------------------------------------
@app.route("/board.svg/")
def board():
    board = c_ai.get_board()
    return Response(chess.svg.board(board=board, size=700), mimetype='image/svg+xml')

#------------------------------------------
# Human Move
#------------------------------------------
@app.route("/move/")
def move():
    try:
        move = request.args.get('move', default="")
        c_ai.push_san(move)
    except Exception:
        traceback.print_exc()
    return main()

#------------------------------------------
# Make Ai’s Move
#------------------------------------------
@app.route("/dev/", methods=['POST'])
def dev():
    try:
        aimove()
    except Exception:
        traceback.print_exc()
    return main()

#------------------------------------------
# New Game
#------------------------------------------
@app.route("/game/", methods=['POST'])
def game():
    c_ai.reset()
    return main()

#------------------------------------------
# Undo
#------------------------------------------
@app.route("/undo/", methods=['POST'])
def undo():
    try:
        c_ai.pop()
    except Exception:
        traceback.print_exc()
    return main()


#------------------------------------------
# start the program
#------------------------------------------
c_ai = chessAI(chess.Board(), SEARCH_DEPTH)
webbrowser.open("http://127.0.0.1:5000/")
app.run()