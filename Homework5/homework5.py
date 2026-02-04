############################################################
# CIS 521: Homework 5
############################################################

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import collections
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
    pass


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
        pass

    def infer_ac3(self):
        pass

    def infer_improved(self):
        pass

    def infer_with_guessing(self):
        pass

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
