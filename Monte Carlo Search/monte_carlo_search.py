import chess
import random
from evaluate import golden_evaluation as evaluate_position
from opening import Polyglot

book = Polyglot(f'/Users/danila/Documents/Chess_C++/polyglot-collection/Book.bin')

# Define the Monte Carlo Search function
def monte_carlo_search(board, num_simulations, opening=True):
    if opening == True:
        opening_move = book.get(board)
        if opening_move is not None:
            return opening_move

    # Initialize the scores and visit counts for each move
    scores = {move: 0 for move in board.legal_moves}
    visits = {move: 0 for move in board.legal_moves}

    # Perform the specified number of simulations
    for i in range(num_simulations):
        # Select a move to explore
        move = None
        best_score = float('-inf')
        for move, score in scores.items():
            if score > best_score:
                move = move
                best_score = score

        # Simulate a game from the selected move to the end of the game or to a certain depth
        sim_board = board.copy()
        sim_board.push(move)
        for j in range(50):
            # Choose a random legal move
            random_move = random.choice(list(sim_board.legal_moves))
            sim_board.push(random_move)

            # Check if the game is over or if the maximum depth has been reached
            if sim_board.is_game_over() or j == 49:
                break

        # Evaluate the outcome of the simulated game
        if sim_board.is_game_over():
            outcome = sim_board.result()
            if outcome == "1-0":
                score = 1
            elif outcome == "0-1":
                score = -1
            else:
                score = 0
        else:
            # Evaluate the resulting position using a static evaluation function
            score = evaluate_position(sim_board)

        # Backpropagate the result of the simulation
        scores[move] += score
        visits[move] += 1

    # Choose the move with the highest expected score
    best_move = None
    best_score = float('-inf')
    for move, score in scores.items():
        if score > best_score:
            best_move = move
            best_score = score
    return best_move

