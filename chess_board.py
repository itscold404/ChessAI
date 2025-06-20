import chess
from chessAI import *
import chess.svg
import chess.pgn
import chess.engine
import traceback
from flask import Flask, Response, request
import webbrowser
import time

SEARCH_DEPTH = 2      # depth at which the AI will perform minimax search
stockfish_move_count = 0
stockfish_total_time = 0
ai_move_count = 0
ai_total_time = 0
    
#------------------------------------------
# Searching Ai's Move
#------------------------------------------
def aimove():
    global ai_move_count, ai_total_time
    start = time.time()
    move = c_ai.select_move()
    end = time.time()
    
    ai_total_time += end - start
    ai_move_count += 1
    print("AI average time taken per move:", ai_total_time/ai_move_count, "seconds")
    
    c_ai.push(move)

#------------------------------------------
# Searching Stockfish's Move
#------------------------------------------
def stockfish():
    try:
        engine = chess.engine.SimpleEngine.popen_uci("stockfish/stockfish-windows-x86-64-avx2.exe")
        
        board = c_ai.get_board()
        move = engine.play(board, chess.engine.Limit(time=0.5))
        c_ai.push(move.move)
        engine.quit()
        
    except Exception as e:
        print("Error with stockfish interaction", e)
        traceback.print_exc()
        
app = Flask(__name__)

#------------------------------------------
# Front Page of the Flask Web Page
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
    ret += '<form action="/engine/" method="post"><button name="Stockfish Move" type="submit">Make Stockfish Move</button></form>'
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
# Make UCI Compatible engine's move
#------------------------------------------
@app.route("/engine/", methods=['POST'])
def engine():
    global stockfish_move_count, stockfish_total_time
    try:
        start = time.time()
        stockfish()
        end = time.time()
        
        stockfish_total_time += (end - start)
        stockfish_move_count += 1
        
        print("stock fish takes", stockfish_total_time/stockfish_move_count, "seconds on average per move")
        print("stock fish made", stockfish_move_count, "moves")
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