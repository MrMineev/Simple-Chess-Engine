import chess
import chess.polyglot

class Polyglot:
    def __init__(self, book_path):
        self.book = book_path
    
    def get(self, board):
        try:
            with chess.polyglot.open_reader(self.book) as reader:
                # get the best move from the opening book
                move = reader.find(board).move
            
            return move
        except:
            return None
