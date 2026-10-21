from tictactoe import player, initial_state, X, O, EMPTY

# Test 1: empty board -> X goes first
board = initial_state()
result = player(board)
print("Empty board:", result)
assert result == X

# Test 2: X has played once -> O's turn
board = [[X,     EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
result = player(board)
print("After X's first move:", result)
assert result == O

# Test 3: X and O have each played once -> X's turn
board = [[X,     EMPTY, EMPTY],
         [EMPTY, O,     EMPTY],
         [EMPTY, EMPTY, EMPTY]]
result = player(board)
print("After one move each:", result)
assert result == X

# Test 4: X has played 3 times, O 2 times -> O's turn
board = [[X,     O,     X    ],
         [EMPTY, X,     EMPTY],
         [EMPTY, EMPTY, O    ]]
result = player(board)
print("X 3 moves, O 2 moves:", result)
assert result == O

print("All tests passed!")
