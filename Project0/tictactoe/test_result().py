from tictactoe import result, initial_state, X, O, EMPTY

# Test 1: X plays in the centre of an empty board
board = initial_state()
new_board = result(board, (1, 1))
print("New board:     ", new_board)
print("Original board:", board)
assert new_board == [[EMPTY, EMPTY, EMPTY],
                     [EMPTY, X,     EMPTY],
                     [EMPTY, EMPTY, EMPTY]]

# Test 2: the original board must NOT change
assert board == initial_state()

# Test 3: after X has played, the next move is O
board = [[X,     EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
new_board = result(board, (2, 2))
print("O's move:      ", new_board)
assert new_board[2][2] == O

# Test 4: playing on a square that is already taken is an error
try:
    result(board, (0, 0))
    print("No error - this is wrong!")
    assert False
except ValueError as e:
    print("Error as expected:", e)

print("All tests passed!")