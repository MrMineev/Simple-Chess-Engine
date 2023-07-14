import chess

# Piece values for material score
PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

# Pawn structure values
PAWN_STRUCTURE_VALUES = {
    "isolated": -10,
    "doubled": -10,
    "backward": -8,
    "passed": 20
}

# Piece mobility values
PIECE_MOBILITY_VALUES = {
    chess.PAWN: 0,
    chess.KNIGHT: 10,
    chess.BISHOP: 10,
    chess.ROOK: 5,
    chess.QUEEN: 2
}

# Bonus score for pieces being on their optimal squares
OPTIMAL_SQUARES_BONUS = {
    chess.KNIGHT: 20,
    chess.BISHOP: 15,
    chess.ROOK: 10,
    chess.QUEEN: 5
}

CENTER_VALUE = 1

def center_score(board, turn):
    if turn == 'white':
        center_square = chess.E4
        total_distance = 0
        
        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]:
            for square in board.pieces(piece_type, chess.WHITE):
                total_distance += chess.square_distance(square, center_square)
            for square in board.pieces(piece_type, chess.BLACK):
                total_distance -= chess.square_distance(square, center_square)
                
        return total_distance * CENTER_VALUE
    else:
        center_square = chess.E4
        total_distance = 0
        
        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]:
            for square in board.pieces(piece_type, chess.WHITE):
                total_distance -= chess.square_distance(square, center_square)
            for square in board.pieces(piece_type, chess.BLACK):
                total_distance += chess.square_distance(square, center_square)
                
        return total_distance * CENTER_VALUE

def fast_evaluate(board, CENTER=0.01):
    if board.turn == chess.WHITE:
        center_square = chess.E4
        total_distance = 0
        
        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]:
            for square in board.pieces(piece_type, chess.WHITE):
                total_distance += chess.square_distance(square, center_square) * PIECE_VALUES[piece_type]
            for square in board.pieces(piece_type, chess.BLACK):
                total_distance -= chess.square_distance(square, center_square) * PIECE_VALUES[piece_type]
                
        return total_distance * CENTER
    else:
        center_square = chess.E4
        total_distance = 0
        
        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]:
            for square in board.pieces(piece_type, chess.WHITE):
                total_distance -= chess.square_distance(square, center_square) * PIECE_VALUES[piece_type]
            for square in board.pieces(piece_type, chess.BLACK):
                total_distance += chess.square_distance(square, center_square) * PIECE_VALUES[piece_type]
                
        return total_distance * CENTER

def simple_evaluate(board):
    if board.turn == chess.WHITE:
        material_score = compute_material_score(board, 'white')

        evaluation_score = material_score

        return evaluation_score
    elif board.turn == chess.BLACK:
        material_score = compute_material_score(board, 'black')

        evaluation_score = material_score

        return evaluation_score 

def golden_evaluation(board):
    if board.is_stalemate():
        return 0

    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -1e9
        else:
            return 1e9

    if board.turn == chess.WHITE:
        material_score = compute_material_score(board, 'white')
        center_points = center_score(board, 'white')

        evaluation_score = material_score + center_points

        return evaluation_score
    elif board.turn == chess.BLACK:
        material_score = compute_material_score(board, 'black')
        center_points = center_score(board, 'black')

        evaluation_score = material_score + center_points

        return evaluation_score  

def evaluate(board):
    if board.turn == chess.WHITE:
        material_score = compute_material_score(board, 'white')
        mobility_score = compute_mobility_score(board, 'white')

        evaluation_score = material_score + mobility_score

        return evaluation_score
    elif board.turn == chess.BLACK:
        material_score = compute_material_score(board, 'black')
        mobility_score = compute_mobility_score(board, 'black')

        evaluation_score = material_score + mobility_score

        return evaluation_score

def compute_material_score(board, turn):
    if turn == 'white':
        material_score = 0
        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            material_score += len(board.pieces(piece_type, chess.WHITE)) * PIECE_VALUES[piece_type]
            material_score -= len(board.pieces(piece_type, chess.BLACK)) * PIECE_VALUES[piece_type]

        return material_score
    else:
        material_score = 0
        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            material_score -= len(board.pieces(piece_type, chess.WHITE)) * PIECE_VALUES[piece_type]
            material_score += len(board.pieces(piece_type, chess.BLACK)) * PIECE_VALUES[piece_type]

        return material_score 


def compute_mobility_score(board, turn):
    if turn == 'white':
        mobility_score = 0
        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            for square in board.pieces(piece_type, chess.WHITE):
                mobility_score += len(board.attacks(square)) * PIECE_MOBILITY_VALUES[piece_type]
                mobility_score += OPTIMAL_SQUARES_BONUS.get(piece_type, 0) if is_on_optimal_square(square, piece_type) else 0

            for square in board.pieces(piece_type, chess.BLACK):
                mobility_score -= len(board.attacks(square)) * PIECE_MOBILITY_VALUES[piece_type]
                mobility_score -= OPTIMAL_SQUARES_BONUS.get(piece_type, 0) if is_on_optimal_square(square, piece_type) else 0

        return mobility_score
    else:
        mobility_score = 0
        for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            for square in board.pieces(piece_type, chess.WHITE):
                mobility_score -= len(board.attacks(square)) * PIECE_MOBILITY_VALUES[piece_type]
                mobility_score -= OPTIMAL_SQUARES_BONUS.get(piece_type, 0) if is_on_optimal_square(square, piece_type) else 0

            for square in board.pieces(piece_type, chess.BLACK):
                mobility_score += len(board.attacks(square)) * PIECE_MOBILITY_VALUES[piece_type]
                mobility_score += OPTIMAL_SQUARES_BONUS.get(piece_type, 0) if is_on_optimal_square(square, piece_type) else 0

        return mobility_score 


def is_on_optimal_square(square, piece_type):
    """
    Returns True if the piece on the given square is on its optimal square,
    False otherwise.
    """
    if piece_type == chess.KNIGHT:
        return square in [chess.C3, chess.C6, chess.F3, chess.F6]
    elif piece_type == chess.BISHOP:
        return square in [chess.C1, chess.F1, chess.C8, chess.F8]
    elif piece_type == chess.ROOK:
        return square in [chess.A1, chess.H1, chess.A8, chess.H8]
    elif piece_type == chess.QUEEN:
        return square in [chess.D1, chess.D8]
