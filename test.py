from search import get_best_move
import chess
import time

board = chess.Board("r2q1rk1/2p2ppp/p3b3/1p1pP3/1b1Pn3/1B6/PP3PPP/RNBQR1K1 w - - 1 13")

start_time = time.time()
print(get_best_move(board, 4, opening=False))
end_time = time.time()

print(f'duration = {end_time - start_time}')
