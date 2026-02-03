############################################################
# CIS 521: Homework 2
############################################################

############################################################
# Imports
import math
import random
from collections import deque
############################################################

# Include your imports here, if any are used.

############################################################

student_name = "Ashwin Verma"

############################################################
# Section 1: N-Queens
############################################################


def num_placements_all(n):
    total_squares = n * n
    return math.comb(total_squares, n)


def num_placements_one_per_row(n):
    return n ** n


def n_queens_valid(board):
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j]:
                return False
            if abs(i - j) == abs(board[i] - board[j]):
                return False
    return True


def n_queens_helper(n, board):  # Added helper function
    if len(board) == n:
        yield board
        return

    for col in range(n):
        new_board = board + [col]

        if n_queens_valid(new_board):
            yield from n_queens_helper(n, new_board)  # Fixed function name


def n_queens_solutions(n):
    return list(n_queens_helper(n, []))

############################################################
# Section 2: Lights Out
############################################################


class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0]) if board else 0

    def get_board(self):
        return self.board

    def perform_move(self, row, col):
        self.board[row][col] = not self.board[row][col]
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for d_row, d_col in directions:
            new_row, new_col = row + d_row, col + d_col
            if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                self.board[new_row][new_col] = not self.board[new_row][new_col]

    def scramble(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if random.random() < 0.5:
                    self.perform_move(row, col)

    def is_solved(self):
        for row in self.board:
            for light in row:
                if light:
                    return False
        return True

    def copy(self):
        new_board = [row[:] for row in self.board]
        return LightsOutPuzzle(new_board)

    def successors(self):
        for row in range(self.rows):
            for col in range(self.cols):
                new_puzzle = self.copy()
                new_puzzle.perform_move(row, col)
                yield ((row, col), new_puzzle)

    def find_solution(self):
        if self.is_solved():
            return []

        def to_tuple(b):
            return tuple(tuple(r) for r in b)
        start = to_tuple(self.board)
        q = deque()
        q.append((start, []))
        seen = set()
        seen.add(start)
        while len(q) > 0:
            curr_state, moves = q.popleft()
            temp_board = [list(row) for row in curr_state]
            temp_puzzle = LightsOutPuzzle(temp_board)
            for m, next_p in temp_puzzle.successors():
                next_state = to_tuple(next_p.get_board())
                if next_p.is_solved():
                    return moves + [m]
                if next_state not in seen:
                    seen.add(next_state)
                    q.append((next_state, moves + [m]))
        return None


def create_puzzle(rows, cols):
    board = [[False for i in range(cols)] for i in range(rows)]
    return LightsOutPuzzle(board)


############################################################
# Section 3: Linear Disk Movement
############################################################


def solve_identical_disks(length, n):
    # start with disks at beginning
    start = frozenset(range(n))
    goal = frozenset(range(length - n, length))

    q = deque()
    q.append((start, []))
    visited = set()
    visited.add(start)

    while q:
        state, moves = q.popleft()

        if state == goal:
            return moves

        # try all the disks
        disks = sorted(state)
        for pos in disks:
            # can we move left
            if pos - 1 >= 0 and pos - 1 not in state:
                next_state = (state - {pos}) | {pos - 1}
                if next_state not in visited:
                    visited.add(next_state)
                    new_moves = moves[:]
                    new_moves.append((pos, pos - 1))
                    q.append((next_state, new_moves))

            # what about right
            if pos + 1 < length and pos + 1 not in state:
                next_state = (state - {pos}) | {pos + 1}
                if next_state not in visited:
                    visited.add(next_state)
                    q.append((next_state, moves + [(pos, pos + 1)]))

            # jump left
            new_pos = pos - 2
            middle = pos - 1
            if new_pos >= 0 and new_pos < length:
                if middle in state and new_pos not in state:
                    next_state = (state - {pos}) | {new_pos}
                    if next_state not in visited:
                        visited.add(next_state)
                        q.append((next_state, moves + [(pos, new_pos)]))

            # or jump right
            new_pos = pos + 2
            middle = pos + 1
            if new_pos >= 0 and new_pos < length:
                if middle in state:
                    if new_pos not in state:
                        next_state = (state - {pos}) | {new_pos}
                        if next_state not in visited:
                            visited.add(next_state)
                            q.append((next_state, moves + [(pos, new_pos)]))

    return None


def solve_distinct_disks(length, n):
    # each disk needs to end up reversed
    start = tuple(range(n))
    end = tuple(range(length - 1, length - 1 - n, -1))

    q = deque()
    q.append((start, []))
    seen = set()
    seen.add(start)

    while len(q) > 0:
        curr, path = q.popleft()

        if curr == end:
            return path

        occupied = set(curr)

        # check each disk
        for i in range(n):
            disk_pos = curr[i]

            # move left by 1
            next_pos = disk_pos - 1
            if next_pos >= 0:
                if next_pos not in occupied:
                    new_state = list(curr)
                    new_state[i] = next_pos
                    new_state = tuple(new_state)
                    if new_state not in seen:
                        seen.add(new_state)
                        new_path = path + [(disk_pos, next_pos)]
                        q.append((new_state, new_path))

            # move right by 1
            next_pos = disk_pos + 1
            if next_pos < length and next_pos not in occupied:
                new_state = list(curr)
                new_state[i] = next_pos
                new_state = tuple(new_state)
                if new_state not in seen:
                    seen.add(new_state)
                    q.append((new_state, path + [(disk_pos, next_pos)]))

            # try jump left
            next_pos = disk_pos - 2
            between = disk_pos - 1
            if next_pos >= 0:
                if between in occupied:
                    if next_pos not in occupied:
                        new_state = list(curr)
                        new_state[i] = next_pos
                        new_state = tuple(new_state)
                        if new_state not in seen:
                            seen.add(new_state)
                            q.append(
                                (new_state, path + [(disk_pos, next_pos)])
                            )

            # jump right
            next_pos = disk_pos + 2
            between = disk_pos + 1
            if 0 <= next_pos < length:
                if between in occupied and next_pos not in occupied:
                    new_state = list(curr)
                    new_state[i] = next_pos
                    new_state = tuple(new_state)
                    if new_state not in seen:
                        seen.add(new_state)
                        new_path = path[:]
                        new_path.append((disk_pos, next_pos))
                        q.append((new_state, new_path))


############################################################
# Section 4: Feedback
############################################################

# Just an approximation is fine.
feedback_question_1 = """
I spent 12 hours on this assignment
"""

feedback_question_2 = """
I personally felt that the hardest part was simply understanding
what the problems were asking for. Took a while to read carefully
and draw out examples, but once understood, the implementation
was straightforward.
"""

feedback_question_3 = """
Not really a fan of puzzle type assignments :)
"""
