import chess
from chessboard import display
from time import sleep
# https://python-chess.readthedocs.io/en/latest/

board = chess.Board()

move_list = [
    'e4', 'e5',
    'Qh5', 'Nc6',
    'Bc4', 'Nf6',
    'Qxf7'
]

# board.fen() -- get fen() representation of current board
# board.set_fen("fen") -- set the board to the fen representation

# while True:
#     display.check_for_quit()
#     display.update(valid_fen, game_board)