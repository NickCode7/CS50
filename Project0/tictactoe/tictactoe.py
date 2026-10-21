"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Count how many X's and O's are on the board
    x_count = 0
    o_count = 0
    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1

    # X goes first, so if both have played the same number of moves,
    # it's X's turn. Otherwise X is one ahead, so it's O's turn.
    if x_count == o_count:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    # i is the row number, j is the column number (both 0, 1 or 2)
    for i in range(3):
        for j in range(3):
            # A move is possible anywhere the square is still empty
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    # The move must be on the board and on an empty square
    if action not in actions(board):
        raise ValueError(f"Invalid action: {action}")

    # Make a full copy so the original board is not changed
    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board
