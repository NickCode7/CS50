from tictactoe import winner, initial_state, X, O, EMPTY

# Test 1: empty board -> no winner
board = initial_state()
print("Empty board:", winner(board))
assert winner(board) is None

# Test 2: X fills the top row
board = [[X,     X,     X    ],
         [O,     O,     EMPTY],
         [EMPTY, EMPTY, EMPTY]]
print("X top row:", winner(board))
assert winner(board) == X

# Test 3: O fills the middle column
board = [[X,     O,     X    ],
         [EMPTY, O,     EMPTY],
         [X,     O,     EMPTY]]
print("O middle column:", winner(board))
assert winner(board) == O

# Test 4: X fills the diagonal from top-left to bottom-right
board = [[X,     O,     EMPTY],
         [EMPTY, X,     O    ],
         [EMPTY, EMPTY, X    ]]
print("X diagonal:", winner(board))
assert winner(board) == X

# Test 5: O fills the other diagonal, top-right to bottom-left
board = [[X,     X,     O    ],
         [EMPTY, O,     EMPTY],
         [O,     EMPTY, X    ]]
print("O other diagonal:", winner(board))
assert winner(board) == O

# Test 6: full board, nobody won (a tie)
board = [[X, O, X],
         [X, O, O],
         [O, X, X]]
print("Tie:", winner(board))
assert winner(board) is None

print("All tests passed!")
