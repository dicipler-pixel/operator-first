#!/usr/bin/env python3
"""Independently replay the 53 h_i transformations from Shehper et al.

This checks only ordinary Andrews-Curtis equivalence P ~ AK(3).  The h_i
notation permits multiplying a relator by the inverse of the other relator;
that operation expands into ordinary AC inversion and multiplication moves.
It does not certify that P is stably AC-trivial.

Source: Ali Shehper et al., arXiv:2408.15332v1, Section 3.5;
        A. Lisitsa, arXiv:2501.18601v1, Section 3.
"""

import argparse
import json


MOVES = [
    9, 7, 4, 8, 11, 5, 11, 9, 3, 10, 12, 7, 7, 9, 11, 5, 3, 5,
    4, 3, 12, 5, 7, 7, 1, 9, 11, 8, 3, 5, 10, 2, 6, 12, 9, 7,
    5, 11, 10, 3, 8, 11, 9, 2, 10, 12, 5, 7, 9, 11, 1, 9, 8,
]
P = ("ABaBAbaBBabAb", "BAbbABabaBBa")
AK3 = ("aaaBBBB", "abaBAB")
INVERT = str.maketrans("abAB", "ABab")


def inverse(word):
    return word[::-1].translate(INVERT)


def reduce_word(word):
    stack = []
    for letter in word:
        assert letter in "abAB"
        if stack and inverse(letter) == stack[-1]:
            stack.pop()
        else:
            stack.append(letter)
    return "".join(stack)


def apply_h(state, move):
    left, right = state
    # h1-h4: right multiplication by the other relator or its inverse.
    if move == 1:
        right = reduce_word(right + left)
    elif move == 2:
        left = reduce_word(left + inverse(right))
    elif move == 3:
        right = reduce_word(right + inverse(left))
    elif move == 4:
        left = reduce_word(left + right)
    else:
        # h5-h12: conjugation by one letter.
        conjugations = {
            5: (1, "A"), 6: (0, "B"), 7: (1, "B"), 8: (0, "a"),
            9: (1, "a"), 10: (0, "b"), 11: (1, "b"), 12: (0, "A"),
        }
        index, letter = conjugations[move]
        if index == 0:
            left = reduce_word(letter + left + inverse(letter))
        else:
            right = reduce_word(letter + right + inverse(letter))
    return left, right


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="print every state for formalization")
    args = parser.parse_args()

    assert len(MOVES) == 53
    assert len(P[0]) == 13 and len(P[1]) == 12
    states = [{"step": 0, "move": None, "relators": P}]
    state = P
    for step, move in enumerate(MOVES, 1):
        state = apply_h(state, move)
        assert state == tuple(map(reduce_word, state))
        states.append({"step": step, "move": move, "relators": state})
    assert state == AK3, f"certificate does not reach AK(3): {state}"
    if args.json:
        print(json.dumps(states, indent=2))
    else:
        print("PASS: 53 h_i transformations take P to AK(3).")
        print(f"P = {P}; AK(3) = {state}")
        print("This certificate contains no stabilization or P-to-standard path.")


if __name__ == "__main__":
    main()
