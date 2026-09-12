#!/usr/bin/env python3
"""Exact finite length-well eye for rank-2 Andrews--Curtis states.

Uses the official SAIR ac-r2-v1 move semantics:
  0,1     invert one relator
  2..5    right-multiply one relator by the other or its inverse
  6..13   conjugate one relator by x^{±1}, y^{±1}
Words are freely reduced after every move.

This script does NOT decide Andrews--Curtis reachability. It measures a finite
bottleneck obstruction: for a start state P of total length L0, the cap-B well
is the exact component of P using only states of total length <= B. If that
component is closed and contains no state shorter than L0, then every path from
P to a shorter state must visit length >= B+1.
"""
from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
from typing import Iterable

Word = tuple[int, ...]
State = tuple[Word, Word]


def reduce_word(w: Iterable[int]) -> Word:
    out: list[int] = []
    for a in w:
        if out and out[-1] == -a:
            out.pop()
        else:
            out.append(a)
    return tuple(out)


def inverse(w: Word) -> Word:
    return tuple(-a for a in reversed(w))


def move(s: State, m: int) -> State:
    r0, r1 = s
    if m == 0:
        return inverse(r0), r1
    if m == 1:
        return r0, inverse(r1)
    if m == 2:
        return reduce_word(r0 + r1), r1
    if m == 3:
        return reduce_word(r0 + inverse(r1)), r1
    if m == 4:
        return r0, reduce_word(r1 + r0)
    if m == 5:
        return r0, reduce_word(r1 + inverse(r0))
    table = {
        6: (1, 0), 7: (-1, 0), 8: (2, 0), 9: (-2, 0),
        10: (1, 1), 11: (-1, 1), 12: (2, 1), 13: (-2, 1),
    }
    if m not in table:
        raise ValueError(f"move id must be 0..13, got {m}")
    a, i = table[m]
    w = (r0, r1)[i]
    nw = reduce_word((a,) + w + (-a,))
    return (nw, r1) if i == 0 else (r0, nw)


def total_length(s: State) -> int:
    return len(s[0]) + len(s[1])


@dataclass(frozen=True)
class WellResult:
    cap: int
    start_length: int
    component_size: int
    min_length: int
    escaped: bool
    closed: bool


def component_under_cap(start: State, cap: int, *, stop_on_escape: bool = False) -> WellResult:
    """Exhaust the exact cap-bounded component, optionally stopping at first descent."""
    L0 = total_length(start)
    if cap < L0:
        raise ValueError("cap must be at least the start length")
    seen = {start}
    q = deque([start])
    min_len = L0
    escaped = False
    while q:
        s = q.popleft()
        for m in range(14):
            t = move(s, m)
            lt = total_length(t)
            if lt > cap or t in seen:
                continue
            seen.add(t)
            if lt < min_len:
                min_len = lt
            if lt < L0:
                escaped = True
                if stop_on_escape:
                    return WellResult(cap, L0, len(seen), min_len, True, False)
            q.append(t)
    return WellResult(cap, L0, len(seen), min_len, escaped, True)


def replay(start: State, path: Iterable[int]) -> tuple[State, list[int]]:
    s = start
    lengths = [total_length(s)]
    for m in path:
        s = move(s, m)
        lengths.append(total_length(s))
    return s, lengths


# Official pool states, encoded x=1, x^-1=-1, y=2, y^-1=-2.
AC00015: State = (
    (-2, -1, 2, -1, -2, 1, 2, -1, 2, 1),
    (-2, -2, 1, -2, 1, -2, 1, -2, 1, 2, 1),
)
AC00002: State = (
    (-2, -2, -2, 1, 2, 1, -2, -1, -1, -1),
    (-2, -2, -2, -2, -2, -2, -2, -1, 2, 2, 2, 2, 2, 2, 1),
)

# Found by exact minimax search, then reduced to a cheap explicit certificate.
AC00015_ESCAPE_PATH = [8, 12, 3, 8, 7, 2, 0, 9, 13, 10, 3, 7, 8, 8, 8, 12, 2, 10, 13, 3]

# Ten verifier-accepted controls from the user's 2026-09-11 backup.
# The integer shown is the accepted path length (an upper bound, not a minimality claim).
CALIBRATION: dict[str, tuple[State, int]] = {
    "ac-00076": (((-2,-1,2,1,1), (-2,-2,-1,2,2,1,1,-2,-1,2,2,-1,2,-1,2,1,-2,-2,1)), 123),
    "ac-00145": (((-2,-2,-1,2,1), (-2,-2,-2,1,1,-2,1,-2,-1,-1)), 116),
    "ac-00219": (((-2,-1,-1,2,1), (-2,-2,-2,-1,2,1,2,2,-1,-2,1,1,2,2,1,2,-1,-2,-1)), 140),
    "ac-00576": (((-2,-2,-1,2,1), (-2,-2,-2,1,1,1,-2,-1,-2,-1)), 121),
    "ac-00742": (((-2,-2,-1,2,-1,-2,1), (-2,-1,2,-1,-2,1,-2,-1,2,1)), 15),
    "ac-00862": (((-2,-2,-1,2,1), (-2,-2,-1,-2,1,1,1,1,2,-1,-1)), 132),
    "ac-00977": (((-2,-2,-2,-2,1,-2,-2,-1,-1), (-2,-2,-2,-2,-2,-1,2,2,2,2,1)), 30),
    "ac-01198": (((-2,-2,-1,2,1), (-2,-2,1,-2,1,1,-2,-1,-2,-1)), 103),
    "ac-01217": (((-2,-2,-1,2,1), (-2,-2,-1,-1,-1,-1,-2,-2,1,1,1)), 61),
    "ac-01411": (((-2,-2,-1,-2,-2,1,2,-1), (-2,-2,-2,1,2,-1,-2,-2,-1)), 12),
}


def verify_ac00015() -> None:
    low = component_under_cap(AC00015, 26)
    assert low.closed and not low.escaped
    assert low.start_length == 21 and low.min_length == 21
    assert low.component_size == 105_912

    end, lengths = replay(AC00015, AC00015_ESCAPE_PATH)
    assert max(lengths) == 27
    assert total_length(end) == 20 < 21
    print("ac-00015 exact well certificate: PASS")
    print(f"  cap 26 closed component = {low.component_size:,} states, min length = {low.min_length}")
    print(f"  explicit escape path length = {len(AC00015_ESCAPE_PATH)}, max length = {max(lengths)}, end length = {total_length(end)}")
    print("  therefore minimum escape ceiling = 27 and exact well depth = +6")


def deep_check_ac00002() -> None:
    # Expensive (~1.3 million states in the final closure); not run by default.
    r31 = component_under_cap(AC00002, 31)
    assert r31.closed and not r31.escaped and r31.min_length == 25
    assert r31.component_size == 1_021_696
    r32 = component_under_cap(AC00002, 32)
    assert r32.closed and not r32.escaped and r32.min_length == 25
    assert r32.component_size == 1_303_928
    print("ac-00002 deep lower-bound certificate: PASS")
    print(f"  cap 31: {r31.component_size:,} states; cap 32: {r32.component_size:,} states")
    print("  no state of length <25 occurs; every descent must visit length >=33 (well depth >= +8)")


def calibration() -> None:
    print("id accepted_path_len start_len well_depth status")
    for cid, (s, path_len) in CALIBRATION.items():
        L0 = total_length(s)
        depth = None
        for extra in (0, 1):
            r = component_under_cap(s, L0 + extra, stop_on_escape=True)
            if r.escaped:
                depth = extra
                break
        print(cid, path_len, L0, depth if depth is not None else ">1", "accepted-path upper bound")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verify-ac00015", action="store_true")
    ap.add_argument("--deep-check-ac00002", action="store_true")
    ap.add_argument("--calibration", action="store_true")
    args = ap.parse_args()
    if not (args.verify_ac00015 or args.deep_check_ac00002 or args.calibration):
        args.verify_ac00015 = True
    if args.verify_ac00015:
        verify_ac00015()
    if args.calibration:
        calibration()
    if args.deep_check_ac00002:
        deep_check_ac00002()


if __name__ == "__main__":
    main()
