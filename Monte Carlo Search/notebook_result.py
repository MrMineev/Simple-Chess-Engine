# importing libraries
from display import print_board
import random
import chess
from evaluate import golden_evaluation as eval
import rich
from pprint import pprint
import math
import numpy as np
from opening import Polyglot


CHECKMATE_SCORE = 2
DEPTH = 4
LOSS_VALUE = 1000
TOP_TIMES = 200
EXPLORATION = 50

book = Polyglot(f'/Users/danila/Documents/Chess_C++/polyglot-collection/Book.bin')

class Node:
    def __init__(self, board):
        self.board = board
        self.status = 0
        self.wins = 0
        self.visited = 0
        self.ucb = 0
        self.children = {}

    def expand(self):
        legal = self.board.legal_moves
        for move in legal:
            new_board = self.board.copy()
            new_board.push(move)
            self.children[str(move)] = Node(new_board)
    
    def simulate(self, depth):
        self.status += 1
        if self.board.is_stalemate():
            return 0
        if self.board.is_checkmate():
            return - (1 / depth) * CHECKMATE_SCORE
        if depth == DEPTH:
            evaluation = eval(self.board)
            if evaluation < 0:
                return evaluation / 24000 * LOSS_VALUE
            return (eval(self.board)) / 24000
        
        random_move = random.choice(list(self.board.legal_moves))
        new_board = self.board.copy()
        new_board.push(random_move)

        if str(random_move) in self.children:
            new_node = self.children[str(random_move)]
        else:
            new_node = Node(new_board)
            self.children[str(random_move)] = new_node

        new_node.visited += 1
        
        score = -new_node.simulate(depth + 1)

        new_node.wins += score

        return score
    
    def explore(self, number):
        for i in range(number):
            self.simulate(1)
    
    def UCB(self, C=1.4):
        for move in self.children:
            try:
                self.children[move].ucb = self.children[move].wins + \
                                C * math.sqrt(math.log(self.status) / self.children[move].status)
            except:
                self.children[move].ucb = 0
        
    def selection(self):
        if len(self.children) == 0:
            # expantion section
            self.expand()
            self.explore(EXPLORATION)
            self.UCB()
            return

        max_ucb = -1e9
        move = None
        for child_key in self.children:
            child = self.children[child_key]
            ucb = child.ucb
            if ucb > max_ucb:
                max_ucb = ucb
                move = child_key
        self.children[move].selection()
        self.UCB()
        return
    
    def get_best(self, opening=True):
        if opening == True:
            opening_move = book.get(self.board)
            if opening_move is not None:
                return opening_move

        for i in range(TOP_TIMES):
            self.selection()
        
        max_ucb = -1e9
        move = None
        for child_key in self.children:
            child = self.children[child_key]
            ucb = child.ucb
            if ucb > max_ucb:
                max_ucb = ucb
                move = child_key
        return chess.Move.from_uci(move)

    def output(self):
        for move in self.children:
            print(f'move = {move}, wins = {self.children[move].wins}, visited = {self.children[move].visited}, ucb = {self.children[move].ucb}')


board = chess.Board()

while True:
    node = Node(board)

    board.push(node.get_best())

    print_board(board)

    move = input("Enter move: ")
    board.push_san(move)
