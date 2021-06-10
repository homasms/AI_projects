import chess
import sys
import random
from time import sleep


class MinimaxAI():
    temp_depth = [0]
    our_turn = [0]
    result = " "
    final_move = {

    }
    visited = []

    def __init__(self, depth):
        self.depth = depth

    def choose_move(self, board):
        sleep(1)
        self.best_move(board)
        self.result = max(self.final_move, key=self.final_move.get)
        self.final_move = {

        }
        self.visited.append(self.result)
        print("MiniMax recommended:", self.result)
        sleep(1)
        return self.result

    # ------------------- *
    # ---------------- *
    # ------------- *
    # choose move *
    # ------------- *
    # ---------------- *
    # ------------------- *
    def best_move(self, board):

        # no more move
        # if len(list(board.legal_moves)) == 0:
        #    print(board.turn)
        #    an = list(board.legal_moves)
        #    print(board.turn )
        #    board.pop()
        #    self.temp_depth[0] -= 1
        #    return self.score(board)

        # enough depth
        if self.temp_depth[0] == self.depth or board.is_game_over():
            leeve_score = self.evaluate_piece_type(board) + self.evvaluate_table(board)
            if self.depth == 1:
                self.final_move[board.peek()] = leeve_score
            return leeve_score

        # --------
        # main part
        # --------
        # max line
        if self.temp_depth[0] % 2 == 0:
            return self.max_value(board)
        # min line
        else:
            return self.min_value(board)

    # compute max lines scores
    def max_value(self, board):
        # print("max line")
        moves = list(board.legal_moves)
        # print(moves)

        v = -1 * sys.maxsize
        for move in moves:
            board.push(move)
            self.temp_depth[0] += 1
            x = self.best_move(board)
            v = max(v, x)
            if self.temp_depth[0] == 1:
                self.final_move[move] = x
            board.pop()
            board.pop()
            self.temp_depth[0] -= 1
        return v

    # compute min lines scores
    def min_value(self, board):
        board.push(chess.Move.null())
        moves = list(board.legal_moves)
        v = sys.maxsize
        for move in moves:
            board.push(move)
            self.temp_depth[0] += 1
            v = min(v, self.best_move(board))
            if self.temp_depth[0] == 1:
                self.final_move[move] = v
            board.pop()
            self.temp_depth[0] -= 1
        return v

    def evaluate_piece_type(self, board):
        num = 0
        # all squares
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            # all pieces (ignore none squares)
            if piece is None:
                continue
            if piece.color: # white
                num -= self.score_piece_type(piece)
            if piece.color == chess.BLACK: # black
                num += self.score_piece_type(piece)
                #num -= 10 * float(chess.square_name(square)[1])
        return num

    def score_piece_type(self, piece):
        if piece.piece_type == 1:
            return 10
        if piece.piece_type == 2:
            return 50
        if piece.piece_type == 3:
            return 30
        if piece.piece_type == 4:
            return 30
        if piece.piece_type == 5:
            return 90
        if piece.piece_type == 6:
            return 900
        return

    def  evvaluate_table(self, board):
        p = self.score_table(board, PAWN_TABLE, chess.PAWN)
        n = self.score_table(board, KNIGHT_TABLE, chess.KNIGHT)
        b = self.score_table(board, BISHOP_TABLE, chess.BISHOP)
        r = self.score_table(board, ROOK_TABLE, chess.ROOK)
        q = self.score_table(board, QUEEN_TABLE, chess.QUEEN)
        k = self.score_table(board, KING_TABLE, chess.KING)
        #print(p + n + b + r + q + k)
        return p + n + b + r + q + k

    def score_table(self, board, pTable, pType):
        pieces = list(board.pieces(pType, False))
        if chess.BLACK:
            pTable.reverse()
            s = sum([pTable[x] for x in pieces])
            pTable.reverse()
        else:
            s = sum([pTable[x] for x in pieces])
        return s


PAWN_TABLE = [0,  0,  0,  0,  0,  0,  0,  0,
50, 50, 50, 50, 50, 50, 50, 50,
10, 10, 20, 30, 30, 20, 10, 10,
 5,  5, 10, 25, 25, 10,  5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5, -5,-10,  0,  0,-10, -5,  5,
 5, 10, 10,-20,-20, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]


KNIGHT_TABLE = [-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  0,  0,  0,-20,-40,
-30,  0, 10, 15, 15, 10,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 10, 15, 15, 10,  5,-30,
-40,-20,  0,  5,  5,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50]

BISHOP_TABLE = [-20,-10,-10,-10,-10,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  5,  0,  0,  0,  0,  5,-10,
-20,-10,-10,-10,-10,-10,-10,-20]

ROOK_TABLE = [0,  0,  0,  0,  0,  0,  -100,  0,
  5, 10, 10, 10, 10, 10, 10,  5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  0,  0,  0,  5,  5,  0,  0,  0]

QUEEN_TABLE = [-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  0,  5,  5,  5,  5,  0,-10,
 -5,  0,  5,  5,  5,  5,  0, -5,
  0,  0,  5,  5,  5,  5,  0, -5,
-10,  5,  5,  5,  5,  5,  0,-10,
-10,  0,  5,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20]

KING_TABLE = [-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-20,-30,-30,-40,-40,-30,-30,-20,
-10,-20,-20,-20,-20,-20,-20,-10,
 20, 20,  0,  0,  0,  0, 20, 20,
 20, 30, 10,  0,  0, 10, 30, 20]

