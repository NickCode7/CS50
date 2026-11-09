from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")


def exactly_one(knight, knave):
    """Each character is either a knight or a knave, but not both."""
    return And(
        Or(knight, knave),
        Not(And(knight, knave))
    )


def says(knight, knave, statement):
    """Knights tell the truth; knaves lie."""
    return And(
        Implication(knight, statement),
        Implication(knave, Not(statement))
    )


# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    exactly_one(AKnight, AKnave),
    says(AKnight, AKnave, And(AKnight, AKnave))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    exactly_one(AKnight, AKnave),
    exactly_one(BKnight, BKnave),
    says(AKnight, AKnave, And(AKnave, BKnave))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    exactly_one(AKnight, AKnave),
    exactly_one(BKnight, BKnave),
    says(AKnight, AKnave, Or(
        And(AKnight, BKnight),
        And(AKnave, BKnave)
    )),
    says(BKnight, BKnave, Or(
        And(AKnight, BKnave),
        And(AKnave, BKnight)
    ))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    exactly_one(AKnight, AKnave),
    exactly_one(BKnight, BKnave),
    exactly_one(CKnight, CKnave),

    # A said exactly one of the two sentences; whichever it was,
    # it is true if A is a knight and false if A is a knave.
    Or(
        says(AKnight, AKnave, AKnight),
        says(AKnight, AKnave, AKnave)
    ),

    # B: "A said 'I am a knave'."
    says(BKnight, BKnave, says(AKnight, AKnave, AKnave)),

    # B: "C is a knave."
    says(BKnight, BKnave, CKnave),

    # C: "A is a knight."
    says(CKnight, CKnave, AKnight)
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
