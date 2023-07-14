import chess
from display import print_board
from search import MTCS as monte_carlo 
import time

board = chess.Board()

while True:
    print_board(board)

    start = time.time()
    
    search = monte_carlo(board, number_simulation=10)
    best_move = search.get()
    print(f"best move = {best_move}")
    best_score = "NONE"
    end = time.time()
    board.push(best_move)

    print_board(board)

    print(f'EVAL = {best_score}, TIME = {end - start}')

    run = True
    while run:
        try:
            move = input('Enter your move: ')
            if move == 'quit':
                run = False
                
            board.push_san(move)
            break
        except:
            print('Invalid move')
    if run == False:
        break
