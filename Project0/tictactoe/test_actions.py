from tictactoe import actions, initial_state, X, O, EMPTY

# Test 1: empty board -> all 9 squares are possible
board = initial_state()
result = actions(board)
print("Empty board:", result)
assert len(result) == 9

# Test 2: X in the top-left corner -> 8 squares left, (0, 0) is not one
board = [[X,     EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY],
         [EMPTY, EMPTY, EMPTY]]
result = actions(board)
print("X in corner:", result)
assert len(result) == 8
assert (0, 0) not in result

# Test 3: only two empty squares left
board = [[X, O,     X],
         [X, O,     O],
         [O, EMPTY, EMPTY]]
result = actions(board)
print("Two squares left:", result)
assert result == {(2, 1), (2, 2)}

# Test 4: full board -> no moves
board = [[X, O, X],
         [X, O, O],
         [O, X, X]]
result = actions(board)
print("Full board:", result)
assert result == set()

print("All tests passed!")
