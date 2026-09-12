#!/usr/bin/env python3
"""Word-order / cancellation eye for the rank-2 Andrews–Curtis search.

This is deliberately *not* an admissible move-count lower bound.  It is a
move-ordering / barrier diagnostic designed after the quotient and exponent-
matrix eyes failed their hard negative control.

For cyclically reduced relators r,s, define k(r,s) as the largest free
cancellation available in a product after allowing cyclic rotations and
inversion of either relator.  The cancellation surplus is

    surplus(r,s) = 2*k(r,s) - min(|r|,|s|).

If the shorter relator is multiplied into the longer one in the appropriate
oriented representatives, positive surplus means the product can shorten total
word length by that amount after the setup conjugations/inversions are paid.

The important point is that this eye retains word order.  On the opposed
controls it separates the 8-move and 622-move instances, unlike the integral
exponent matrix.

The second half exactly exhausts the ac-00002 sublevel components for total
length caps 25, 27 and 29.  It records how temporary length growth unlocks
larger cyclic overlaps/cancellation surplus.  The larger cap-31 certificate is
kept in the backup ledger (1,021,696 states); this regression intentionally
stays small enough for routine CI.
"""

from __future__ import annotations

from collections import Counter, deque
from dataclasses import dataclass
from typing import Iterable

Word = tuple[int, ...]
State = tuple[Word, Word]


def reduce_word(word: Iterable[int]) -> Word:
    out: list[int] = []
    for letter in word:
        if out and out[-1] == -letter:
            out.pop()
        else:
            out.append(letter)
    return tuple(out)


def inverse(word: Word) -> Word:
    return tuple(-letter for letter in reversed(word))


def cyclic_reduce(word: Word) -> Word:
    work = list(word)
    while len(work) > 1 and work[0] == -work[-1]:
        work = work[1:-1]
    return tuple(work)


def rotations(word: Word) -> list[Word]:
    if not word:
        return [()]
    return [word[i:] + word[:i] for i in range(len(word))]


def oriented_rotations(word: Word) -> list[Word]:
    word = cyclic_reduce(word)
    return rotations(word) + rotations(inverse(word))


def cancellation_length(left: Word, right: Word) -> int:
    k = 0
    limit = min(len(left), len(right))
    while k < limit and left[-1-k] == -right[k]:
        k += 1
    return k


def max_cyclic_cancellation(r: Word, s: Word) -> int:
    return max(
        cancellation_length(a, b)
        for a in oriented_rotations(r)
        for b in oriented_rotations(s)
    )


def cancellation_surplus(r: Word, s: Word) -> int:
    r = cyclic_reduce(r)
    s = cyclic_reduce(s)
    k = max_cyclic_cancellation(r, s)
    return 2 * k - min(len(r), len(s))


def ac_move(state: State, move: int) -> State:
    r0, r1 = state
    if move == 0:
        return inverse(r0), r1
    if move == 1:
        return r0, inverse(r1)
    if move == 2:
        return reduce_word(r0 + r1), r1
    if move == 3:
        return reduce_word(r0 + inverse(r1)), r1
    if move == 4:
        return r0, reduce_word(r1 + r0)
    if move == 5:
        return r0, reduce_word(r1 + inverse(r0))

    conjugations = {
        6: (1, 0),
        7: (-1, 0),
        8: (2, 0),
        9: (-2, 0),
        10: (1, 1),
        11: (-1, 1),
        12: (2, 1),
        13: (-2, 1),
    }
    letter, which = conjugations[move]
    word = (r0, r1)[which]
    conjugated = reduce_word((letter,) + word + (-letter,))
    return (conjugated, r1) if which == 0 else (r0, conjugated)


def total_length(state: State) -> int:
    return len(state[0]) + len(state[1])


def sublevel_component(start: State, cap: int) -> set[State]:
    seen = {start}
    queue = deque([start])
    while queue:
        state = queue.popleft()
        for move in range(14):
            nxt = ac_move(state, move)
            if total_length(nxt) > cap or nxt in seen:
                continue
            seen.add(nxt)
            queue.append(nxt)
    return seen


@dataclass(frozen=True)
class EyeControl:
    challenge_id: str
    state: State
    reference: str


CONTROLS = [
    EyeControl(
        "ac-01635",
        (
            (-2, -2, -1),
            (-2, -2, -2, -1, -2, -2, -2, -1, -2, -1),
        ),
        "8-move positive control",
    ),
    EyeControl(
        "ac-00015",
        (
            (-2, -1, 2, -1, -2, 1, 2, -1, 2, 1),
            (-2, -2, 1, -2, 1, -2, 1, -2, 1, 2, 1),
        ),
        "622-move negative control",
    ),
    EyeControl(
        "ac-00002",
        (
            (-2, -2, -2, 1, 2, 1, -2, -1, -1, -1),
            (-2, -2, -2, -2, -2, -2, -2, -1, 2, 2, 2, 2, 2, 2, 1),
        ),
        "length-well control",
    ),
]

EXPECTED_INITIAL = {
    "ac-01635": (3, 3),   # k=3, surplus=+3
    "ac-00015": (4, -2),  # k=4, surplus=-2
    "ac-00002": (5, 0),   # k=5, surplus=0
}

EXPECTED_COMPONENTS = {
    25: 3000,
    27: 17720,
    29: 91040,
}

EXPECTED_LAYER_SURPLUS = {
    25: {0: 3000},
    27: {0: 12000, 2: 2720},
    29: {0: 48000, 2: 10880, 4: 14440},
}


def main() -> None:
    print("initial opposed controls")
    print("challenge\tlengths\tmax_cyclic_cancel\tsurplus\treference")
    for control in CONTROLS:
        r0, r1 = control.state
        k = max_cyclic_cancellation(r0, r1)
        surplus = cancellation_surplus(r0, r1)
        if (k, surplus) != EXPECTED_INITIAL[control.challenge_id]:
            raise AssertionError(
                f"{control.challenge_id}: expected {EXPECTED_INITIAL[control.challenge_id]}, "
                f"got {(k, surplus)}"
            )
        print(
            f"{control.challenge_id}\t{(len(r0), len(r1))}\t{k}\t"
            f"{surplus:+d}\t{control.reference}"
        )

    start = CONTROLS[2].state
    previous: set[State] | None = None
    for cap in (25, 27, 29):
        component = sublevel_component(start, cap)
        if len(component) != EXPECTED_COMPONENTS[cap]:
            raise AssertionError(
                f"cap {cap}: expected {EXPECTED_COMPONENTS[cap]} states, got {len(component)}"
            )
        if previous is not None and not previous.issubset(component):
            raise AssertionError("sublevel components are not nested")

        layer = [state for state in component if total_length(state) == cap]
        distribution = Counter(cancellation_surplus(*state) for state in layer)
        expected_distribution = Counter(EXPECTED_LAYER_SURPLUS[cap])
        if distribution != expected_distribution:
            raise AssertionError(
                f"cap {cap}: expected surplus distribution {expected_distribution}, "
                f"got {distribution}"
            )

        print(
            f"cap={cap} states={len(component)} layer={len(layer)} "
            f"surplus={dict(sorted(distribution.items()))}"
        )
        previous = component

    print("\nVERDICT: KEEP as a discovery / move-ordering eye, not as a proof bound.")
    print("The hard 622-move control begins with negative cancellation surplus, while")
    print("the 8-move control begins positive.  On ac-00002, increasing the allowed")
    print("length from 25 to 27 to 29 creates exact layers with surplus 0, +2, +4.")
    print("This directly measures the cancellation capacity purchased by climbing the")
    print("word-length well that defeats monotone length-greedy search.")


if __name__ == "__main__":
    main()
