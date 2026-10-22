from tictactoe import minimax, initial_state, X, O, EMPTY

# Test 1: X can win right now by playing the top-right corner
board = [[X,     X,     EMPTY],
         [O,     O,     EMPTY],
         [EMPTY, EMPTY, EMPTY]]
move = minimax(board)
print("X should win at (0, 2):", move)
assert move == (0, 2)

# Test 2: O must block X, who is about to win across the top row
board = [[X,     X,     EMPTY],
         [EMPTY, O,     EMPTY],
         [EMPTY, EMPTY, EMPTY]]
move = minimax(board)
print("O should block at (0, 2):", move)
assert move == (0, 2)

# Test 3: O can win right now, and that beats blocking X
board = [[X,     X,     EMPTY],
         [O,     O,     EMPTY],
         [X,     EMPTY, EMPTY]]
move = minimax(board)
print("O should win at (1, 2):", move)
assert move == (1, 2)

# Test 4: game already over -> no move
board = [[X,     X,     X    ],
         [O,     O,     EMPTY],
         [EMPTY, EMPTY, EMPTY]]
move = minimax(board)
print("Game over:", move)
assert move is None

print("All tests passed!")