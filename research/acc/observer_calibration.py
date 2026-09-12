#!/usr/bin/env python3
"""Exact calibration of the integral exponent-sum matrix eye for AC rank 2.

The state of a two-relator presentation is projected to the 2x2 integer matrix
whose rows are the exponent sums of x and y in each relator.  Under the
ac-r2-v1 move table:

  0,1 : negate one row
  2,3 : row0 <- row0 +/- row1
  4,5 : row1 <- row1 +/- row0
  6..13: conjugations, hence no matrix change

Therefore the exact word distance from the projected matrix to I under moves
0..5 is an admissible lower bound on the real AC move count.  The projected
graph is infinite, so unlike a fixed finite quotient it has no finite-diameter
ceiling in principle.

This script calibrates that lower bound against deliberately opposed controls.
The result is negative: the full integral matrix still collapses a 622-move
hard case to the same distance as an 8-move case.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Iterable

Matrix = tuple[int, int, int, int]
Word = tuple[int, ...]
Presentation = tuple[Word, Word]
TARGET: Matrix = (1, 0, 0, 1)


@dataclass(frozen=True)
class Control:
    challenge_id: str
    presentation: Presentation
    reference_move_count: int | None
    note: str


def exponent_row(word: Word) -> tuple[int, int]:
    sx = 0
    sy = 0
    for letter in word:
        if letter == 1:
            sx += 1
        elif letter == -1:
            sx -= 1
        elif letter == 2:
            sy += 1
        elif letter == -2:
            sy -= 1
        else:
            raise ValueError(f"unexpected rank-2 letter {letter}")
    return sx, sy


def exponent_matrix(presentation: Presentation) -> Matrix:
    (a, b), (c, d) = map(exponent_row, presentation)
    return a, b, c, d


def projected_moves(M: Matrix) -> Iterable[tuple[int, Matrix]]:
    a, b, c, d = M
    yield 0, (-a, -b, c, d)
    yield 1, (a, b, -c, -d)
    yield 2, (a + c, b + d, c, d)
    yield 3, (a - c, b - d, c, d)
    yield 4, (a, b, c + a, d + b)
    yield 5, (a, b, c - a, d - b)


def exact_matrix_distance(start: Matrix) -> tuple[int, list[int], int]:
    """Exact BFS distance in the projected row-operation graph.

    The six generators are symmetric: 0 and 1 are involutions; 2/3 and 4/5
    are inverse pairs.  Hence first hit of TARGET is the exact word distance.
    """
    if start == TARGET:
        return 0, [], 1

    queue = deque([start])
    previous: dict[Matrix, tuple[Matrix | None, int | None]] = {start: (None, None)}

    while queue:
        state = queue.popleft()
        for move, nxt in projected_moves(state):
            if nxt in previous:
                continue
            previous[nxt] = (state, move)
            if nxt == TARGET:
                path: list[int] = []
                cursor = nxt
                while previous[cursor][0] is not None:
                    parent, used = previous[cursor]
                    assert parent is not None and used is not None
                    path.append(used)
                    cursor = parent
                path.reverse()
                return len(path), path, len(previous)
            queue.append(nxt)

    raise RuntimeError("unreachable target in GL(2,Z) component")


CONTROLS = [
    Control(
        "ac-01635",
        (
            (-2, -2, -1),
            (-2, -2, -2, -1, -2, -2, -2, -1, -2, -1),
        ),
        8,
        "positive control: current short solution",
    ),
    Control(
        "ac-00015",
        (
            (-2, -1, 2, -1, -2, 1, 2, -1, 2, 1),
            (-2, -2, 1, -2, 1, -2, 1, -2, 1, 2, 1),
        ),
        622,
        "negative control: hard case that killed fixed finite quotients",
    ),
    Control(
        "ac-00002",
        (
            (-2, -2, -2, 1, 2, 1, -2, -1, -1, -1),
            (-2, -2, -2, -2, -2, -2, -2, -1, 2, 2, 2, 2, 2, 2, 1),
        ),
        None,
        "length-well control: exact search requires escape to total length >= 32",
    ),
]


def main() -> None:
    expected = {
        "ac-01635": 7,
        "ac-00015": 7,
        "ac-00002": 5,
    }

    print("challenge\tmatrix\tmatrix_lb\treference\tpath\tstates_seen\tnote")
    for control in CONTROLS:
        M = exponent_matrix(control.presentation)
        det = M[0] * M[3] - M[1] * M[2]
        if abs(det) != 1:
            raise AssertionError(f"{control.challenge_id}: matrix is not unimodular: {M}")
        distance, path, states = exact_matrix_distance(M)
        if distance != expected[control.challenge_id]:
            raise AssertionError(
                f"{control.challenge_id}: expected projected distance "
                f"{expected[control.challenge_id]}, got {distance}"
            )
        reference = "open" if control.reference_move_count is None else str(control.reference_move_count)
        print(
            f"{control.challenge_id}\t{M}\t{distance}\t{reference}\t"
            f"{path}\t{states}\t{control.note}"
        )

    print("\nVERDICT: REJECT integral exponent-sum matrix as a hard-case pruning eye.")
    print("Reason: ac-00015 and ac-01635 both project to exact distance 7, while")
    print("their real move counts are separated by 614 moves (622 versus 8).")
    print("The observer is not finite-diameter, but it still discards the word-order")
    print("information carrying the difficult part of these competition instances.")


if __name__ == "__main__":
    main()
