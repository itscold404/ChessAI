import chess
import chess.polyglot

# establish the positioning and material value of each piece
pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]
knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]
bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]
rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]
queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]
kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]
piece_weight = {"p": 100, 
                "n": 320,
                "b": 330,
                "r": 500,
                "q": 900}


class chessAI():
    def __init__(self, board, depth) -> None:
        self.board = board
        self.search_depth = depth
    #--------------------------------------------------------------------------------------------
    # produce evaluation score based ONLY on checkmate and stalemate
    #--------------------------------------------------------------------------------------------
    def evalueate_board_state(self):
        if self.board.is_checkmate():
            if self.board.turn:
                return -999999
            else:
                return 999999
            
        if self.board.is_stalemate():
                return 0
            
        if self.board.is_insufficient_material():
                return 0

    #--------------------------------------------------------------------------------------------
    # find the evaluation score based on board state (checkmate/stalemate)
    # else find the score based on each piece's material value and position 
    # value
    #--------------------------------------------------------------------------------------------
    def evaluate_board(self):
        board_state_score = self.evalueate_board_state()
        
        # find number of each piece type for both black and white
        wp = len(self.board.pieces(chess.PAWN, chess.WHITE))
        bp = len(self.board.pieces(chess.PAWN, chess.BLACK))
        wn = len(self.board.pieces(chess.KNIGHT, chess.WHITE))
        bn = len(self.board.pieces(chess.KNIGHT, chess.BLACK))
        wb = len(self.board.pieces(chess.BISHOP, chess.WHITE))
        bb = len(self.board.pieces(chess.BISHOP, chess.BLACK))
        wr = len(self.board.pieces(chess.ROOK, chess.WHITE))
        br = len(self.board.pieces(chess.ROOK, chess.BLACK))
        wq = len(self.board.pieces(chess.QUEEN, chess.WHITE))
        bq = len(self.board.pieces(chess.QUEEN, chess.BLACK))
        
        # find weighed difference between black and white
        material = (piece_weight["p"] * (wp - bp) + piece_weight["n"] * (wn - bn) + 
                    piece_weight["b"] * (wb - bb) + piece_weight["r"] * (wr - br) + 
                    piece_weight["q"] * (wq - bq))
        
        # index for board.pieces(): top row starts at index 0 and increments by 
        # 1 going to the right. next row starts at index 8 and increments by one going 
        # to the right and so on.
        pawnsq = sum([pawntable[i] for i in self.board.pieces(chess.PAWN, chess.WHITE)])
        pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)]
                            for i in self.board.pieces(chess.PAWN, chess.BLACK)])
        
        knightsq = sum([knightstable[i] for i in self.board.pieces(chess.KNIGHT, chess.WHITE)])
        knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                                for i in self.board.pieces(chess.KNIGHT, chess.BLACK)])
        
        bishopsq = sum([bishopstable[i] for i in self.board.pieces(chess.BISHOP, chess.WHITE)])
        bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)]
                                for i in self.board.pieces(chess.BISHOP, chess.BLACK)])
        
        rooksq = sum([rookstable[i] for i in self.board.pieces(chess.ROOK, chess.WHITE)])
        rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
                            for i in self.board.pieces(chess.ROOK, chess.BLACK)])
        
        queensq = sum([queenstable[i] for i in self.board.pieces(chess.QUEEN, chess.WHITE)])
        queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
                                for i in self.board.pieces(chess.QUEEN, chess.BLACK)])
        
        kingsq = sum([kingstable[i] for i in self.board.pieces(chess.KING, chess.WHITE)])
        kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
                            for i in self.board.pieces(chess.KING, chess.BLACK)])
        
        eval = (board_state_score + material + pawnsq + knightsq + bishopsq + 
                rooksq + queensq + kingsq)
        
        return eval if self.board.turn else -eval

    #--------------------------------------------------------------------------------------------
    # quienscence search to avoid horixontal effect from depth limitation
    #--------------------------------------------------------------------------------------------
    def quiesce(self, alpha, beta):
        stand_pat = self.evaluate_board()
        if stand_pat >= beta:
            return beta
        if alpha < stand_pat:
            alpha = stand_pat

        for move in self.board.legal_moves:
            if self.board.is_capture(move):
                self.board.push(move)
                score = -1 * self.quiesce(-beta, -alpha)
                self.board.pop()

                if score >= beta:
                    return beta
                if score > alpha:
                    alpha = score

        return alpha

    #--------------------------------------------------------------------------------------------
    # alpha-beta pruning to cut search cost
    #--------------------------------------------------------------------------------------------
    def alphabeta(self, alpha, beta, depthleft):
        bestscore = -9999
        if (depthleft == 0):
            return self.quiesce(alpha, beta)
        
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -1 * self.alphabeta(-beta, -alpha, depthleft - 1)
            self.board.pop()
            
            if (score >= beta):
                return score
            if (score > bestscore):
                bestscore = score
            if (score > alpha):
                alpha = score
                
        return bestscore

    #--------------------------------------------------------------------------------------------
    # chess ai finds move from grandmaster opening moves or use minimax search
    # with alpha-beta pruning
    #--------------------------------------------------------------------------------------------
    def select_move(self):
        try:
            move = chess.polyglot.MemoryMappedReader("human.bin").weighted_choice(self.board).move
            return move
        except:
            bestMove = chess.Move.null()
            bestValue = -99999
            alpha = -100000
            beta = 100000
            for move in self.board.legal_moves:
                self.board.push(move)
                boardValue = -1 * self.alphabeta(-beta, -alpha, self.search_depth - 1)
                if boardValue > bestValue:
                    bestValue = boardValue
                    bestMove = move
                if (boardValue > alpha):
                    alpha = boardValue
                self.board.pop()
            return bestMove


# chessAI = chessAI(chess.Board())
# print(chessAI.select_move(5))