import chess
import random
from evaluate import golden_evaluation as evaluate
import math

MOVE_LIMIT = 50

class Node:
    def __init__(self, position):
        self.position = position
        self.num_visits = 0
        self.total_reward = 0
        self.children = []

    def select_best_child(self):
        # Choose the child node with the highest UCB score
        # using the UCT formula
        C = 1.4
        best_child = None
        best_score = -1

        for child in self.children:
            score = (child.total_reward / child.num_visits) + C * math.sqrt(math.log(self.num_visits) / child.num_visits)
            if score > best_score:
                best_score = score
                best_child = child

        return best_child

    def simulate_game(self):
        # Play a random game from the current position
        board = self.position

        index = 0
        for index in range(0, MOVE_LIMIT):
            move = random.choice(list(board.legal_moves))
            board.push(move)

        result = evaluate(board)

        return result

    def update_stats(self, result):
        # Update the visit count and total reward of the node
        self.num_visits += 1
        self.total_reward += result

    def get_best_move(self):
        # Choose the move associated with the child node with the highest average reward
        best_child = max(self.children, key=lambda child: child.total_reward / child.num_visits)
        return best_child.position.move(best_child.move)

    def expand(self):
        # Add child nodes for all legal moves from the current position
        for move in self.position.legal_moves:
            new_position = self.position.copy()
            new_position.push(move)
            child = Node(new_position)
            child.move = move
            self.children.append(child)

class MTCS:
    def __init__(self, board, number_simulation=10):
        self.board = board
        self.number_simulation = number_simulation

    def get(self):
        search = Node(self.board)
        return search.get_best_move()
