############################################################
# CIS 521: Homework 5
############################################################

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
from collections import deque
import copy
import itertools
import random
import math

############################################################

student_name = "Ashwin Verma"

############################################################
# Sudoku Solver
############################################################


def sudoku_cells():
    cells= []
    for i in range(9):
        for j in range(9):
            cells.append((i,j))
    return cells


def sudoku_arcs():
    cells= sudoku_cells()
    arcs= []
    for cell in cells:
        for cell2 in cells:
            row, col = cell
            row2, col2 = cell2
            if row == row2 and col ==col2:
                continue
            if row == row2 or col == col2 or (row//3 == row2//3 and col//3 == col2//3):
                arcs.append(((row, col), (row2, col2)))
    return arcs


def read_board(path):
    board = {}
    with open (path, 'r') as f:
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
        if ((cell1),(cell2)) not in Sudoku.ARCS:
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
        pass

    def infer_with_guessing(self):
        pass
    
if __name__ == "__main__":
    sudoku = Sudoku(read_board("easy.txt")) # See below for a picture.
    sudoku.infer_ac3()
    for r in range(9):
        print(" ".join(str(next(iter(sudoku.get_values((r, c))))) for c in range(9)))

############################################################
# Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_2 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""

feedback_question_3 = """
Type your response here.
Your response may span multiple lines.
Do not include these instructions in your response.
"""
