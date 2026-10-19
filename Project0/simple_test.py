import degrees

# A tiny made-up movie world, small enough to follow by hand:
#
#   Alice --(Movie 1)-- Bob --(Movie 2)-- Carol
#
#   Dave is in no movies, so he is not connected to anyone.

degrees.people["1"] = {"name": "Alice", "birth": "", "movies": {"m1"}}
degrees.people["2"] = {"name": "Bob",   "birth": "", "movies": {"m1", "m2"}}
degrees.people["3"] = {"name": "Carol", "birth": "", "movies": {"m2"}}
degrees.people["4"] = {"name": "Dave",  "birth": "", "movies": set()}

degrees.movies["m1"] = {"title": "Movie 1", "year": "", "stars": {"1", "2"}}
degrees.movies["m2"] = {"title": "Movie 2", "year": "", "stars": {"2", "3"}}


# Test 1: Alice and Bob were in Movie 1 together -> 1 step
path = degrees.shortest_path("1", "2")
print("Alice -> Bob:", path)
assert path == [("m1", "2")]

# Test 2: Alice -> Bob -> Carol -> 2 steps
path = degrees.shortest_path("1", "3")
print("Alice -> Carol:", path)
assert path == [("m1", "2"), ("m2", "3")]

# Test 3: same person -> 0 steps
path = degrees.shortest_path("1", "1")
print("Alice -> Alice:", path)
assert path == []

# Test 4: Dave is in no movies -> not connected
path = degrees.shortest_path("1", "4")
print("Alice -> Dave:", path)
assert path is None

print("All tests passed!")
