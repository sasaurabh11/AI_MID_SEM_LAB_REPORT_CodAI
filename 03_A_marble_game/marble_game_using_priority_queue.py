import numpy as np
from itertools import product
from time import time
from datetime import timedelta
import heapq

BOARD = np.array([
    (0, 0, 1, 1, 1, 0, 0),
    (0, 0, 1, 1, 1, 0, 0),
    (1, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 1),
    (0, 0, 1, 1, 1, 0, 0),
    (0, 0, 1, 1, 1, 0, 0)
], dtype=bool)

WINNING_BOARD = np.array([
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 1, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0),
    (0, 0, 0, 0, 0, 0, 0)
], dtype=bool)

left, right, up, down = 1, 2, 3, 4
directions = {left: (-1, 0), right: (1, 0), up: (0, 1), down: (0, -1)}
moves = {left: 'left', right: 'right', up: 'up', down: 'down'}

start_time = time()

winning_moves = [
    (5, 3, left), (4, 5, down), (6, 4, left), (6, 2, up), (4, 3, up),
    (4, 6, down), (4, 2, right), (4, 0, up), (3, 4, right), (6, 4, left),
    (3, 6, down), (3, 4, right), (3, 2, right), (6, 2, left), (3, 0, up),
    (3, 2, right), (1, 4, right), (2, 6, down), (2, 4, right), (5, 4, left),
    (3, 4, down), (2, 2, right), (5, 2, left), (2, 0, up), (2, 3, down),
    (0, 2, right), (3, 2, left), (0, 4, down), (0, 2, right), (2, 1, up),
    (1, 3, right)
]

class Move:
    def __init__(self, r, c, direction):
        self.r, self.c, self.direction = r, c, direction

    def apply(self, board_state):
        dr, dc = directions[self.direction]
        board_state[self.r + dr * 2, self.c + dc * 2] = board_state[self.r, self.c]
        board_state[self.r, self.c] = False
        board_state[self.r + dr, self.c + dc] = False

    def __str__(self):
        return f"Move ({self.r}, {self.c}) {moves[self.direction]}"

class Games_m:
    def __init__(self, initial_board=BOARD):
        self.board = np.copy(initial_board)

    def simulation(self, moveset):
        self.display_board()
        for move in moveset:
            input("Next move? Press Enter...")
            Move(*move).apply(self.board)
            self.display_board()

    def display_board(self):
        print("\nCurrent Board:")
        for row in self.board:
            print(' '.join('O' if cell else '.' for cell in row))
        print()

    def find_winning_moves(self):
        priority_queue = []
        heapq.heappush(priority_queue, (0, []))
        visited_states = set()

        for iteration in range(10000000):
            if not priority_queue:
                print("No more moves to process.")
                return None

            current_cost, current_moveset = heapq.heappop(priority_queue)
            board_copy = np.copy(self.board)
            self.apply_moves(board_copy, current_moveset)

            if np.array_equal(board_copy, WINNING_BOARD):
                print("-DONE-")
                print(f"Winning Moveset: {current_moveset}")
                return current_moveset

            legal_moves = []
            for r, c in product(range(board_copy.shape[0]), range(board_copy.shape[1])):
                if board_copy[r, c]:
                    if c >= 2 and board_copy[r, c - 1] and not board_copy[r, c - 2]:
                        legal_moves.append((r, c, down))
                    if c <= board_copy.shape[1] - 3 and board_copy[r, c + 1] and not board_copy[r, c + 2]:
                        legal_moves.append((r, c, up))
                    if r <= board_copy.shape[0] - 3 and board_copy[r + 1, c] and not board_copy[r + 2, c]:
                        legal_moves.append((r, c, right))
                    if r >= 2 and board_copy[r - 1, c] and not board_copy[r - 2, c]:
                        legal_moves.append((r, c, left))

            for move in legal_moves:
                new_moveset = current_moveset + [move]
                new_board_state = np.copy(board_copy)
                Move(*move).apply(new_board_state)
                state_tuple = tuple(new_board_state.flatten())
                if state_tuple not in visited_states:
                    visited_states.add(state_tuple)
                    heapq.heappush(priority_queue, (current_cost + 1, new_moveset))

            if iteration % 50000 == 0:
                self.report_progress(iteration, priority_queue)

    def report_progress(self, iteration, priority_queue):
        print(f"------\nIteration: {iteration}")
        print(f"Runtime: {timedelta(seconds=time() - start_time)}")
        print(f"Queue Length: {len(priority_queue)}\n")

    def apply_moves(self, board, moveset):
        for move in moveset:
            Move(*move).apply(board)

if __name__ == "__main__":
    game = Games_m()
    game.simulation(winning_moves)
