############################################################
# CIS 521: Homework 3
############################################################

############################################################
# Imports
import random
from queue import PriorityQueue
############################################################

# Include your imports here, if any are used.

############################################################

student_name = "Ashwin Verma"

############################################################
# Section 1: Tile Puzzle
############################################################


def create_tile_puzzle(rows, cols):
    board = [
        [
            0 if (r == rows - 1 and c == cols - 1) else (r * cols + c + 1)
            for c in range(cols)
        ]
        for r in range(rows)
    ]
    return TilePuzzle(board)


class TilePuzzle(object):

    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0]) if self.rows > 0 else 0

        self.empty_row = 0
        self.empty_col = 0
        for r in range(self.rows):
            for c in range(self.cols):
                if board[r][c] == 0:
                    self.empty_row = r
                    self.empty_col = c
                    break

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        direction_offsets = {
            'up': (-1, 0),
            'down': (1, 0),
            'left': (0, -1),
            'right': (0, 1)
        }

        if direction not in direction_offsets:
            return False

        empty_r = self.empty_row
        empty_c = self.empty_col

        offset_r, offset_c = direction_offsets[direction]
        new_r = empty_r + offset_r
        new_c = empty_c + offset_c

        if 0 <= new_r < self.rows and 0 <= new_c < self.cols:
            temp = self.board[empty_r][empty_c]
            self.board[empty_r][empty_c] = self.board[new_r][new_c]
            self.board[new_r][new_c] = temp

            self.empty_row = new_r
            self.empty_col = new_c
            return True

        return False

    def scramble(self, num_moves):
        for i in range(num_moves):
            direction = random.choice(["up", "down", "left", "right"])
            self.perform_move(direction)

    def is_solved(self):
        expected = 1
        for r in range(self.rows):
            for c in range(self.cols):
                if r == self.rows - 1 and c == self.cols - 1:
                    if self.board[r][c] != 0:
                        return False
                else:
                    if self.board[r][c] != expected:
                        return False
                    expected += 1
        return True

    def copy(self):
        new_board = [row[:] for row in self.board]
        return TilePuzzle(new_board)

    def successors(self):
        directions = ["up", "down", "left", "right"]
        for direction in directions:
            new_puzzle = self.copy()
            moved = new_puzzle.perform_move(direction)
            if moved:
                yield (direction, new_puzzle)

    def find_solutions_iddfs(self):
        def iddfs_helper(puzzle, limit, moves):
            if puzzle.is_solved():
                yield moves[:]
                return

            if len(moves) >= limit:
                return

            for direction, new_puzzle in puzzle.successors():
                moves.append(direction)
                yield from iddfs_helper(new_puzzle, limit, moves)
                moves.pop()

        limit = 0
        while True:
            solutions = list(iddfs_helper(self, limit, []))
            if solutions:
                yield from solutions
                return
            limit += 1

    # Required A* implementation
    def find_solution_a_star(self):
        def manhattan_distance(board, rows, cols):
            # Calculate total Manhattan distance for all tiles
            distance = 0
            for r in range(rows):
                for c in range(cols):
                    tile = board[r][c]
                    if tile != 0:
                        goal_r = (tile - 1) // cols
                        goal_c = (tile - 1) % cols
                        distance += abs(r - goal_r) + abs(c - goal_c)
            return distance

        def board_to_tuple(board):
            return tuple(tuple(row) for row in board)

        pq = PriorityQueue()
        counter = 0
        initial_h = manhattan_distance(self.board, self.rows, self.cols)
        pq.put((initial_h, counter, self, []))
        counter += 1

        visited = {board_to_tuple(self.board)}

        while not pq.empty():
            f_score, _, current_puzzle, path = pq.get()

            if current_puzzle.is_solved():
                return path

            # Explore neighbors
            for direction, new_puzzle in current_puzzle.successors():
                board_tuple = board_to_tuple(new_puzzle.board)

                if board_tuple not in visited:
                    visited.add(board_tuple)
                    new_path = path + [direction]
                    g_score = len(new_path)
                    h_score = manhattan_distance(
                        new_puzzle.board,
                        new_puzzle.rows,
                        new_puzzle.cols)
                    f_score = g_score + h_score
                    pq.put((f_score, counter, new_puzzle, new_path))
                    counter += 1

        # No solution found
        return None


############################################################
# Section 2: Grid Navigation
############################################################


def find_path(start, goal, scene):
    rows = len(scene)
    cols = len(scene[0]) if rows > 0 else 0

    if scene[start[0]][start[1]] or scene[goal[0]][goal[1]]:
        return None

    def euclidean_distance(p1, p2):
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return (dx*dx + dy*dy)**0.5

    def get_neighbors(point):
        r, c = point
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (-1, -1), (-1, 1), (1, -1), (1, 1)
        ]
        neighbors = []
        for dr, dc in directions:
            new_r = r + dr
            new_c = c + dc
            if (0 <= new_r < rows and 0 <= new_c < cols and
                    not scene[new_r][new_c]):
                neighbors.append((new_r, new_c))
        return neighbors

    # A* pathfinding
    pq = PriorityQueue()
    pq.put((0, start))

    came_from = {}
    g_score = {start: 0}

    while not pq.empty():
        _, current = pq.get()

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        for neighbor in get_neighbors(current):
            tentative_g = (g_score[current] +
                           euclidean_distance(current, neighbor))

            if (neighbor not in g_score or
                    tentative_g < g_score[neighbor]):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + euclidean_distance(neighbor, goal)
                pq.put((f_score, neighbor))

    # No path exists
    return None


############################################################
# Section 3: Linear Disk Movement
############################################################


def solve_distinct_disks(length, n):
    from collections import deque

    start = tuple(range(n))
    goal = tuple(range(length - 1, length - 1 - n, -1))

    def heuristic(state):
        total_distance = 0
        for disk_id in range(n):
            current_pos = state[disk_id]
            goal_pos = goal[disk_id]
            distance = abs(current_pos - goal_pos)
            total_distance += distance
        return total_distance // 2

    pq = PriorityQueue()
    initial_f = heuristic(start)
    pq.put((initial_f, 0, start, []))

    best_cost = {start: 0}

    while not pq.empty():
        f_score, g_score, current_state, path = pq.get()

        if current_state == goal:
            return path

        if g_score > best_cost.get(current_state, float('inf')):
            continue

        occupied = set(current_state)

        for disk_id in range(n):
            disk_pos = current_state[disk_id]

            possible_moves = []

            next_pos = disk_pos - 1
            if next_pos >= 0 and next_pos not in occupied:
                possible_moves.append(next_pos)

            next_pos = disk_pos + 1
            if next_pos < length and next_pos not in occupied:
                possible_moves.append(next_pos)

            next_pos = disk_pos - 2
            between = disk_pos - 1
            if next_pos >= 0:
                if between in occupied and next_pos not in occupied:
                    possible_moves.append(next_pos)

            next_pos = disk_pos + 2
            between = disk_pos + 1
            if next_pos < length:
                if between in occupied and next_pos not in occupied:
                    possible_moves.append(next_pos)

            for next_pos in possible_moves:
                new_state = list(current_state)
                new_state[disk_id] = next_pos
                new_state = tuple(new_state)

                new_g = g_score + 1

                if new_g < best_cost.get(new_state, float('inf')):
                    best_cost[new_state] = new_g
                    new_h = heuristic(new_state)
                    new_f = new_g + new_h
                    new_path = path + [(disk_pos, next_pos)]
                    pq.put((new_f, new_g, new_state, new_path))

    # No solution found
    return None


############################################################
# Section 4: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
I spent 13 hours on this assigment
"""


feedback_question_2 = """
I found it challenging coming up with the heuristics for the A* implementations
"""


feedback_question_3 = """
I liked the tile puzzle section because it was the easiest
"""
