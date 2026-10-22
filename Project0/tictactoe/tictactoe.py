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


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # Check each row
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]

    # Check each column
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] != EMPTY:
            return board[0][j]

    # Check the diagonal from top-left to bottom-right
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]

    # Check the diagonal from top-right to bottom-left
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    # Nobody has three in a row
    return None
