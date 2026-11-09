from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


# ---------------------------------------------------------------------------
# Puzzle 0
# A says "I am both a knight and a knave."
# ---------------------------------------------------------------------------

# Structure: A is a knight or a knave...
a_is_knight_or_knave = Or(AKnight, AKnave)
# ...but not both.
a_is_not_both = Not(And(AKnight, AKnave))

# What A said, translated into logic.
a_statement0 = And(AKnight, AKnave)

# If A is a knight, A's statement is true.
if_a_knight_statement_true0 = Implication(AKnight, a_statement0)
# If A is a knave, A's statement is false.
if_a_knave_statement_false0 = Implication(AKnave, Not(a_statement0))

knowledge0 = And(
    a_is_knight_or_knave,
    a_is_not_both,
    if_a_knight_statement_true0,
    if_a_knave_statement_false0
)


# ---------------------------------------------------------------------------
# Puzzle 1
# A says "We are both knaves."
# B says nothing.
# ---------------------------------------------------------------------------

# Structure for B (A's structure rules are defined above and reused).
b_is_knight_or_knave = Or(BKnight, BKnave)
b_is_not_both = Not(And(BKnight, BKnave))

# What A said.
a_statement1 = And(AKnave, BKnave)

# A's statement is true if A is a knight, false if A is a knave.
if_a_knight_statement_true1 = Implication(AKnight, a_statement1)
if_a_knave_statement_false1 = Implication(AKnave, Not(a_statement1))

# B said nothing, so there is nothing to add for B's statements.

knowledge1 = And(
    a_is_knight_or_knave,
    a_is_not_both,
    b_is_knight_or_knave,
    b_is_not_both,
    if_a_knight_statement_true1,
    if_a_knave_statement_false1
)


# ---------------------------------------------------------------------------
# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
# ---------------------------------------------------------------------------

# "Same kind" means both knights, or both knaves.
both_knights = And(AKnight, BKnight)
both_knaves = And(AKnave, BKnave)
a_statement2 = Or(both_knights, both_knaves)

# "Different kinds" means A knight and B knave, or A knave and B knight.
a_knight_b_knave = And(AKnight, BKnave)
a_knave_b_knight = And(AKnave, BKnight)
b_statement2 = Or(a_knight_b_knave, a_knave_b_knight)

# A's statement is true if A is a knight, false if A is a knave.
if_a_knight_statement_true2 = Implication(AKnight, a_statement2)
if_a_knave_statement_false2 = Implication(AKnave, Not(a_statement2))

# B's statement is true if B is a knight, false if B is a knave.
if_b_knight_statement_true2 = Implication(BKnight, b_statement2)
if_b_knave_statement_false2 = Implication(BKnave, Not(b_statement2))

knowledge2 = And(
    a_is_knight_or_knave,
    a_is_not_both,
    b_is_knight_or_knave,
    b_is_not_both,
    if_a_knight_statement_true2,
    if_a_knave_statement_false2,
    if_b_knight_statement_true2,
    if_b_knave_statement_false2
)


# ---------------------------------------------------------------------------
# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
# ---------------------------------------------------------------------------

# Structure for C.
c_is_knight_or_knave = Or(CKnight, CKnave)
c_is_not_both = Not(And(CKnight, CKnave))

# Option 1: A said "I am a knight."
#   true if A is a knight, false if A is a knave.
a_said_i_am_knight = And(
    Implication(AKnight, AKnight),
    Implication(AKnave, Not(AKnight))
)

# Option 2: A said "I am a knave."
#   true if A is a knight, false if A is a knave.
a_said_i_am_knave = And(
    Implication(AKnight, AKnave),
    Implication(AKnave, Not(AKnave))
)

# We don't know which one A said, so one of the two options holds.
a_said_one_of_them = Or(a_said_i_am_knight, a_said_i_am_knave)

# B's first statement: "A said 'I am a knave'."
#   This is exactly option 2 from above.
b_statement3_first = a_said_i_am_knave
if_b_knight_first_true = Implication(BKnight, b_statement3_first)
if_b_knave_first_false = Implication(BKnave, Not(b_statement3_first))

# B's second statement: "C is a knave."
b_statement3_second = CKnave
if_b_knight_second_true = Implication(BKnight, b_statement3_second)
if_b_knave_second_false = Implication(BKnave, Not(b_statement3_second))

# C's statement: "A is a knight."
c_statement3 = AKnight
if_c_knight_statement_true = Implication(CKnight, c_statement3)
if_c_knave_statement_false = Implication(CKnave, Not(c_statement3))

knowledge3 = And(
    a_is_knight_or_knave,
    a_is_not_both,
    b_is_knight_or_knave,
    b_is_not_both,
    c_is_knight_or_knave,
    c_is_not_both,
    a_said_one_of_them,
    if_b_knight_first_true,
    if_b_knave_first_false,
    if_b_knight_second_true,
    if_b_knave_second_false,
    if_c_knight_statement_true,
    if_c_knave_statement_false
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
