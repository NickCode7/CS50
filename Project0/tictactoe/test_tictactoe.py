from tictactoe import player, initial_state, X, O, EMPTY
from tictactoe import actions
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
print(f"After X's first, it's  {result} turn to move:")
assert result == O

# Test 3: X and O have each played once -> X's turn
board = [[X,     EMPTY, EMPTY],
         [EMPTY, O,     EMPTY],
         [EMPTY, EMPTY, EMPTY]]
result = player(board)
print(f"After one move each,it's  {result} turn to move")
assert result == X

# Test 4: X has played 3 times, O 2 times -> O's turn
board = [[X,     O,     X    ],
         [EMPTY, X,     EMPTY],
         [EMPTY, EMPTY, O    ]]
result = player(board)
print(f"X 3 moves, O 2 moves, it's  {result} turn to move")
assert result == O

print("All tests passed!")



""""Action()Test"""

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


