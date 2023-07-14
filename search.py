import chess
from evaluate import golden_evaluation as evaluate
from zobrist import ZobristHash
import threading
from opening import Polyglot
import os

PIECE_VALUES = {
    chess.PAWN: 1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK: 5,
    chess.QUEEN: 9,
    chess.KING: 0 # The king's value is not used in the evaluation function
}

book = Polyglot(f'{os.getcwd()}/polyglot-collection/Book.bin')

hasher = ZobristHash()

class SearchThread(threading.Thread):
    def __init__(self, board, depth, alpha, beta, transposition_table, move_scores, move):
        threading.Thread.__init__(self)
        self.board = board
        self.depth = depth
        self.alpha = alpha
        self.beta = beta
        self.transposition_table = transposition_table
        self.move_scores = move_scores
        self.move = move

    def run(self):
        board = self.board.copy()
        board.push(self.move)
        score = alpha_beta(board, self.depth - 1, self.alpha, self.beta, False, self.transposition_table)
        self.move_scores[self.move] = score

def order_moves(board):
    moves = []
    
    # First consider captures
    for move in board.generate_captures():
        moves.append(move)
    
    # Then consider checks
    for move in board.generate_checks():
        if move not in moves:
            moves.append(move)
    
    # Finally, consider all other moves
    for move in board.generate_legal_moves():
        if move not in moves:
            moves.append(move)
    
    return moves

def alpha_beta(board, depth, alpha, beta, maximizing_player, transposition_table):
    fen = board.fen() #hasher.zobrist_hash(board)

    if fen in transposition_table:
        return transposition_table[fen]

    if depth == 0 or board.is_game_over():
        eval_score = evaluate(board)
        transposition_table[fen] = eval_score
        return eval_score
    
    moves = board.legal_moves
    #moves = order_moves(board)

    if maximizing_player:
        max_eval = float('-inf')
        for move in moves:
            board.push(move)
            eval = alpha_beta(board, depth-1, alpha, beta, False, transposition_table)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        transposition_table[fen] = max_eval
        return max_eval
    else:
        min_eval = float('inf')
        for move in moves:
            board.push(move)
            eval = alpha_beta(board, depth-1, alpha, beta, True, transposition_table)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        transposition_table[fen] = min_eval
        return min_eval

def get_best_move(board, depth, opening=True):
    """
    Searches the game tree to the given depth using alpha-beta pruning and returns the best move for the current player.
    """

    if opening:
        opening_move = book.get(board)
        if opening_move is not None:
            return opening_move, "Opening Stage no Eval"

    transposition_table = {}
    move_scores = {}

    # Spawn a thread for each legal move
    threads = []
    for move in board.legal_moves:
        thread = SearchThread(board, depth, float("-inf"), float("inf"), transposition_table, move_scores, move)
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    # Find the move with the highest score
    best_move = None
    best_score = float("-inf")
    for move, score in move_scores.items():
        if score > best_score:
            best_move = move
            best_score = score

    return best_move, best_score
