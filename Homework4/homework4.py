############################################################
# CIS 521: Homework 4
############################################################

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import math

############################################################

student_name = "Ashwin Verma"

############################################################
# Section 1: Dominoes Game
############################################################


def create_dominoes_game(rows, cols):
    game = []
    for r in range(rows):
        row = []
        for c in range(cols):
            row.append(False)
        game.append(row)
    return DominoesGame(game)


class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board

    def get_board(self):
        return self.board

    def reset(self):
        # set all positions to False
        self.board = [
            [False for _ in range(len(self.board[0]))]
            for _ in range(len(self.board))
        ]

    def is_legal_move(self, row, col, vertical):
        # edge cases
        if (row < 0 or row >= len(self.board) or
                col < 0 or col >= len(self.board[0])):
            return False
        if self.board[row][col]:
            return False
        if vertical:
            if row + 1 >= len(self.board) or self.board[row + 1][col]:
                return False
        else:
            if col + 1 >= len(self.board[0]) or self.board[row][col + 1]:
                return False
        return True

    def legal_moves(self, vertical):
        moves = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.is_legal_move(i, j, vertical):
                    moves.append((i, j))

        return moves

    def perform_move(self, row, col, vertical):
        self.board[row][col] = True
        if vertical:
            self.board[row + 1][col] = True
        else:
            self.board[row][col + 1] = True

    def game_over(self, vertical):
        if len(self.legal_moves(vertical)) == 0:
            return True
        return False

    def copy(self):
        copied = []
        for r in range(len(self.board)):
            row = []
            for c in range(len(self.board[0])):
                row.append(self.board[r][c])
            copied.append(row)
        return DominoesGame(copied)

    def successors(self, vertical):
        moves = self.legal_moves(vertical)
        for move in moves:
            new_game = self.copy()
            new_game.perform_move(move[0], move[1], vertical)
            yield (move, new_game)

    def get_random_move(self, vertical):
        pass

        # recursively find the min_score for beta player
    def get_min_score(self, vertical, limit, alpha, beta, max_player):
        score = math.inf
        if self.game_over(vertical) or limit == 0:
            beta_moves = len(self.legal_moves(max_player))
            alpha_moves = len(self.legal_moves(not max_player))
            return beta_moves - alpha_moves, 1

        nodes = 0
        for move, new_board in self.successors(vertical):
            eval, child_nodes = new_board.get_max_score(
                not vertical, limit - 1, alpha, beta, max_player
            )
            nodes += child_nodes
            score = min(score, eval)
            beta = min(beta, score)
            if beta <= alpha:
                break
        return score, nodes

    # recursively find the max_score for alpha player
    def get_max_score(self, vertical, limit, alpha, beta, max_player):
        score = -math.inf
        if self.game_over(vertical) or limit == 0:
            alpha_moves = len(self.legal_moves(max_player))
            beta_moves = len(self.legal_moves(not max_player))
            return alpha_moves - beta_moves, 1

        nodes = 0
        for move, new_board in self.successors(vertical):
            eval, child_nodes = new_board.get_min_score(
                not vertical, limit - 1, alpha, beta, max_player
            )
            nodes += child_nodes
            score = max(score, eval)
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return score, nodes

    # Required
    def get_best_move(self, vertical, limit):
        alpha = -math.inf
        beta = math.inf
        best_score = -math.inf
        best_move = None
        nodes_visited = 0

        for move, new_board in self.successors(vertical):
            score, nodes = new_board.get_min_score(
                not vertical, limit - 1, alpha, beta, vertical
            )
            nodes_visited += nodes
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)

        return (best_move, best_score, nodes_visited)

############################################################
# Section 2: Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
This assignment took me 10 hours
"""

feedback_question_2 = """
Figuring out the recursive alpha-beta implementation was the
most challenging. While on paper I understood what needed to
be done, implementing it in code and making sure the logic was correct
was difficult.
"""

feedback_question_3 = """
I liked the overall aspect of having 2 players and them
fighting to minimize/maximize the score.
"""
