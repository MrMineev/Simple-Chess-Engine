import random
import chess

class ZobristHash:
    def __init__(self):
        self.zobrist = []
        for _ in range(64):
            row = []
            for _ in range(12):
                row.append(random.randrange(2**64))
            self.zobrist.append(row)

    def zobrist_hash(self, board):
        """
        Generate a unique hash for a board position
        Hashing algorithm from Zobrist (1970)
        """
        pieces = board.piece_map()

        hash = 0
        for square in chess.SQUARES:
            if square in pieces:
                piece = pieces[square]
                piece_type = piece.piece_type + piece.color * 6 - 1
                hash ^= self.zobrist[square][piece_type]

        return hash