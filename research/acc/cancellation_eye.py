#!/usr/bin/env python3
"""Word-order / cancellation eye for the rank-2 Andrews–Curtis search.

This is deliberately *not* an admissible move-count lower bound. It is a
move-ordering / barrier diagnostic designed after the quotient and exponent-
matrix eyes failed their hard negative control.

For cyclically reduced relators r,s, define k(r,s) as the largest free
cancellation available in a product after allowing cyclic rotations and
inversion of either relator. The cancellation surplus is

    surplus(r,s) = 2*k(r,s) - min(|r|,|s|).

If the shorter relator is multiplied into the longer one in the appropriate
oriented representatives, positive surplus is exactly the amount by which that
one multiplication can reduce total *cyclic* length once setup orientations
are available.

This gives an exact one-product collapse floor

    collapse_floor = cyclic_total_length - surplus.

The important point is that this eye retains word order. On the opposed
controls it separates the 8-move and 622-move instances, unlike the integral
exponent matrix.

The second half exactly exhausts the ac-00002 sublevel components for raw total
length caps 25, 27 and 29. It records how temporary length growth unlocks
larger cyclic overlaps/cancellation surplus. The larger cap-31 certificate is
kept in the backup ledger (1,021,696 states); this regression intentionally
stays small enough for routine CI.

A canonical cyclic/inversion signature is also recorded. It is used only to
share expensive eye evaluations, never to identify raw search states or erase
move cost. The measured compression is enormous: the 91,040 raw states in the
cap-29 component occupy only 28 such signatures.
"""

from __future__ import annotations

from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from typing import Iterable

Word = tuple[int, ...]
State = tuple[Word, Word]
Signature = tuple[Word, Word]


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


def canonical_relator(word: Word) -> Word:
    word = cyclic_reduce(word)
    return min(rotations(word) + rotations(inverse(word)))


def signature(state: State) -> Signature:
    # Relator order is preserved.  Inversion/conjugation are collapsed only for
    # diagnostic caching; the raw search still retains every state and move.
    return canonical_relator(state[0]), canonical_relator(state[1])


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


def signature_metrics(sig: Signature) -> tuple[int, int, int, int]:
    r, s = sig
    k = max_cyclic_cancellation(r, s)
    cyclic_total = len(r) + len(s)
    surplus = 2 * k - min(len(r), len(s))
    collapse_floor = cyclic_total - surplus
    return k, surplus, cyclic_total, collapse_floor


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
    "ac-01635": (3, 3, 10),   # k=3, surplus=+3, collapse floor 10
    "ac-00015": (4, -2, 23),  # k=4, surplus=-2, collapse floor 23
    "ac-00002": (5, 0, 25),   # k=5, surplus=0, collapse floor 25
}

EXPECTED_COMPONENTS = {
    25: 3000,
    27: 17720,
    29: 91040,
}

EXPECTED_SIGNATURES = {
    25: 5,
    27: 9,
    29: 28,
}

EXPECTED_LAYER_SURPLUS = {
    25: {0: 3000},
    27: {0: 12000, 2: 2720},
    29: {0: 48000, 2: 10880, 4: 14440},
}

EXPECTED_ALL_COMPONENT_JOINT_AT_29 = {
    (25, 0, 25): 63000,
    (27, 2, 25): 13600,
    (29, 4, 25): 14440,
}


def main() -> None:
    print("initial opposed controls")
    print("challenge\tlengths\tmax_cyclic_cancel\tsurplus\tcollapse_floor\treference")
    for control in CONTROLS:
        sig = signature(control.state)
        k, surplus, _, floor = signature_metrics(sig)
        if (k, surplus, floor) != EXPECTED_INITIAL[control.challenge_id]:
            raise AssertionError(
                f"{control.challenge_id}: expected {EXPECTED_INITIAL[control.challenge_id]}, "
                f"got {(k, surplus, floor)}"
            )
        r0, r1 = control.state
        print(
            f"{control.challenge_id}\t{(len(r0), len(r1))}\t{k}\t"
            f"{surplus:+d}\t{floor}\t{control.reference}"
        )

    start = CONTROLS[2].state
    previous: set[State] | None = None
    component_29: set[State] | None = None

    for cap in (25, 27, 29):
        component = sublevel_component(start, cap)
        if len(component) != EXPECTED_COMPONENTS[cap]:
            raise AssertionError(
                f"cap {cap}: expected {EXPECTED_COMPONENTS[cap]} states, got {len(component)}"
            )
        if previous is not None and not previous.issubset(component):
            raise AssertionError("sublevel components are not nested")

        sigs = {signature(state) for state in component}
        if len(sigs) != EXPECTED_SIGNATURES[cap]:
            raise AssertionError(
                f"cap {cap}: expected {EXPECTED_SIGNATURES[cap]} signatures, got {len(sigs)}"
            )

        metric_cache = {sig: signature_metrics(sig) for sig in sigs}
        layer = [state for state in component if total_length(state) == cap]
        distribution = Counter(metric_cache[signature(state)][1] for state in layer)
        expected_distribution = Counter(EXPECTED_LAYER_SURPLUS[cap])
        if distribution != expected_distribution:
            raise AssertionError(
                f"cap {cap}: expected surplus distribution {expected_distribution}, "
                f"got {distribution}"
            )

        print(
            f"cap={cap} states={len(component)} signatures={len(sigs)} "
            f"compression={len(component)/len(sigs):.1f}x "
            f"layer={len(layer)} surplus={dict(sorted(distribution.items()))}"
        )
        previous = component
        if cap == 29:
            component_29 = component

    assert component_29 is not None
    sig_cache = {sig: signature_metrics(sig) for sig in {signature(s) for s in component_29}}
    joint = Counter()
    for state in component_29:
        _, surplus, cyclic_total, floor = sig_cache[signature(state)]
        joint[(cyclic_total, surplus, floor)] += 1
    if joint != Counter(EXPECTED_ALL_COMPONENT_JOINT_AT_29):
        raise AssertionError(
            f"cap 29 joint collapse-floor distribution mismatch: {joint}"
        )

    # All 91,040 raw states in the measured cap-29 well live on the same
    # one-product collapse floor: climbing by 2 units of cyclic length buys
    # exactly 2 units of cancellation surplus, but no net descent below 25.
    if {floor for (_, _, floor) in joint} != {25}:
        raise AssertionError("cap-29 well is not a single collapse-floor plateau")

    # Measure the class-fiber graph inside the closed component.  Only
    # multiplication moves change the canonical cyclic/inversion signature.
    class_edges: dict[Signature, set[Signature]] = defaultdict(set)
    class_changing_by_family = Counter()
    for state in component_29:
        source = signature(state)
        for move in range(14):
            nxt = ac_move(state, move)
            if nxt not in component_29:
                continue
            target = signature(nxt)
            if target == source:
                continue
            class_edges[source].add(target)
            class_changing_by_family["multiply" if 2 <= move <= 5 else "other"] += 1

    unique_directed_edges = sum(len(v) for v in class_edges.values())
    if unique_directed_edges != 88:
        raise AssertionError(f"expected 88 directed signature edges, got {unique_directed_edges}")
    if class_changing_by_family["other"] != 0:
        raise AssertionError(
            f"non-multiplication moves changed signature: {class_changing_by_family}"
        )

    print(
        "cap29 joint(cyclic_total,surplus,floor)="
        f"{dict(sorted(joint.items()))}"
    )
    print(
        f"cap29 signature graph: nodes=28 directed_edges={unique_directed_edges} "
        f"raw_class_changing_multiplications={class_changing_by_family['multiply']}"
    )

    print("\nVERDICT: KEEP as a discovery / move-ordering eye, not as a proof bound.")
    print("The hard 622-move control begins with negative cancellation surplus, while")
    print("the 8-move control begins positive. On ac-00002, the cap-29 component is")
    print("a 91,040-state plateau at collapse floor 25: length growth is exactly paid")
    print("back as cancellation capacity. The expensive diagnostics can be shared")
    print("across only 28 cyclic/inversion signatures while raw states are retained")
    print("for exact path reconstruction and move costs.")


if __name__ == "__main__":
    main()
