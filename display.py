import chess

def print_board(board):
    """
    Prints a text representation of a chess board to the console.
    """
    board_str = "\n".join([
        "  +------------------------+",
        *[f"{8 - i} {'|' + '  '.join(board.piece_at(chess.square(j, 7 - i)).unicode_symbol() if board.piece_at(chess.square(j, 7 - i)) else '.' for j in range(8)) + ' |'}" for i in range(8)],
        "  +------------------------+",
        "    a  b  c  d  e  f  g  h"
    ])
    print(board_str)