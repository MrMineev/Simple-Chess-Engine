import chess
from display import print_board
from search import get_best_move
import time

DEPTH = int(input('Enter depth: '))

print(f'DEPTH = {DEPTH}')

board = chess.Board("rnb3nr/p2k4/1p1p2Q1/2pNpp1p/2P5/3P1P2/4PK2/7q b ha - 0 1")

while True:
    print_board(board)

    start = time.time()
    best_move, best_score = get_best_move(board, DEPTH)
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
