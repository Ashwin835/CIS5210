############################################################
# CIS 521: Homework 5
############################################################

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from collections import deque
import copy
############################################################

student_name = "Ashwin Verma"

############################################################
# Sudoku Solver
############################################################


def sudoku_cells():
    cells = []
    for i in range(9):
        for j in range(9):
            cells.append((i, j))
    return cells


def sudoku_arcs():
    cells = sudoku_cells()
    arcs = []
    for cell in cells:
        for cell2 in cells:
            row, col = cell
            row2, col2 = cell2
            if row == row2 and col == col2:
                continue
            if (row == row2 or col == col2 or
                    (row//3 == row2//3 and col//3 == col2//3)):
                arcs.append(((row, col), (row2, col2)))
    return arcs


def read_board(path):
    board = {}
    with open(path, 'r') as f:
        lines = f.readlines()
        for r, line in enumerate(lines):
            for c, char in enumerate(line.strip()):
                if char == '*':
                    board[(r, c)] = set(range(1, 10))
                else:
                    board[(r, c)] = {int(char)}
    return board


class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        if ((cell1), (cell2)) not in Sudoku.ARCS:
            return False
        if len(self.board[cell2]) == 1:
            number = next(iter(self.board[cell2]))
            if number in self.board[cell1]:
                self.board[cell1].remove(number)
                return True
        return False

    def infer_ac3(self):
        queue = deque(Sudoku.ARCS)
        while queue:
            cell1, cell2 = queue.popleft()
            isRemoved = self.remove_inconsistent_values(cell1, cell2)
            if isRemoved:
                for arc in Sudoku.ARCS:
                    if arc[1] == cell1 and arc[0] != cell2:
                        queue.append(arc)

    def infer_improved(self):
        made_additional_inference = True
        while made_additional_inference:
            self.infer_ac3()
            made_additional_inference = False
            for cell in Sudoku.CELLS:
                if len(self.board[cell]) > 1:
                    row, col = cell
                    neighbor_rows = [(r, col) for r in range(9)
                                     if r != row]
                    neighbor_cols = [(row, c) for c in range(9)
                                     if c != col]
                    neighbor_blocks = [
                        (r, c) for r in range((row//3)*3, (row//3)*3 + 3)
                        for c in range((col//3)*3, (col//3)*3 + 3)
                        if (r, c) != cell]
                    neighbor_cells = [neighbor_rows, neighbor_cols,
                                      neighbor_blocks]
                    for number in self.board[cell]:
                        for group in neighbor_cells:
                            unique = True
                            for neighbor in group:
                                if number in self.board[neighbor]:
                                    unique = False
                                    break
                            if unique:
                                made_additional_inference = True
                                self.board[cell] = {number}
                                break
                    if made_additional_inference:
                        break

    def isSolved(self):
        for cell in Sudoku.CELLS:
            if len(self.board[cell]) != 1:
                return False
        return True

    def infer_with_guessing(self):
        if self.isSolved():
            return True

        self.infer_improved()
        for cells in Sudoku.CELLS:
            if len(self.board[cells]) > 1:
                for number in self.board[cells]:
                    new_board = copy.deepcopy(self.board)
                    self.board[cells] = {number}
                    self.infer_with_guessing()
                    if self.isSolved():
                        break
                    else:
                        self.board = new_board
                return True


############################################################
# Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
This homework took me around 8 hours to complete.
"""

feedback_question_2 = """
Most challenging with infer_improved becuase my
original approach was incorrect and it took
some time to debug.
"""

feedback_question_3 = """
I liked the last method because it was fun to implement
the recursive function and understand logically the cases
for which backtracking is necessary.
"""
