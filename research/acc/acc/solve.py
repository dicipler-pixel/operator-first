"""IDA* search for an ordinary-AC certificate.

g = moves used.  h = exact finite-image distance (admissible: rho is a
homomorphism, so a word path projects to an image path of the same length).
h never prunes on its own and never ranks greedily; it only bounds.

`length_cap` is a DIAL, not a constant.  On the 424 training certificates the
correlation between path length and peak total relator length is only 0.29, and
the recovered finisher records a 25-move path peaking at 20 against a 40-move
path peaking at 15 -- the shorter path climbs higher.  A tight cap forbids the
climb by construction and can only ever find the long low road.
"""

from __future__ import annotations

import time
from typing import Optional, Sequence

from .image_distance import lower_bound, table
from .moves import N_MOVES, TARGET, apply_move
from .words import encode_state, total_length


def solve(start, length_cap: int, primes=(5, 7), max_nodes: int = 2_000_000,
          time_budget: float = 120.0, max_depth: int = 60):
    """Returns (moves, stats).  moves is None when the budget is spent."""
    for p in primes:
        table(p)
    t0 = time.time()
    nodes = 0
    h0 = lower_bound(start, primes)["lower_bound_moves"]
    if h0 is None:
        return None, {"result": "NO_CERTIFICATE", "stop_reason": "IMAGE_UNREACHABLE",
                      "nodes": 0, "h0": None}

    def h(state):
        v = lower_bound(state, primes)["lower_bound_moves"]
        return 10 ** 6 if v is None else v

    bound = h0
    path: list = []
    stop = None

    def dfs(state, g, bound, prev_undo):
        nonlocal nodes, stop
        nodes += 1
        if nodes > max_nodes:
            stop = "STATE_BUDGET_REACHED"
            return None
        if time.time() - t0 > time_budget:
            stop = "TIME_BUDGET_REACHED"
            return None
        f = g + h(state)
        if f > bound:
            return f
        if state == TARGET:
            return "FOUND"
        best = None
        for m in range(N_MOVES):
            if m == prev_undo:
                continue
            child = apply_move(state, m)
            if child == state or total_length(child) > length_cap:
                continue
            path.append(m)
            r = dfs(child, g + 1, bound, _INV[m])
            if r == "FOUND":
                return "FOUND"
            path.pop()
            if stop:
                return None
            if r is not None and (best is None or r < best):
                best = r
        return best

    from .moves import INVERSE as _INV
    while bound <= max_depth:
        path.clear()
        r = dfs(start, 0, bound, None)
        if r == "FOUND":
            return list(path), {"result": "CERTIFICATE_CANDIDATE", "stop_reason": None,
                                "nodes": nodes, "h0": h0, "bound": bound,
                                "seconds": round(time.time() - t0, 2)}
        if stop:
            break
        if r is None:
            stop = "SEARCH_EXHAUSTED_UNDER_LENGTH_CAP"
            break
        bound = r
    return None, {"result": "NO_CERTIFICATE",
                  "stop_reason": stop or "DEPTH_LIMIT",
                  "nodes": nodes, "h0": h0, "final_bound": bound,
                  "length_cap": length_cap,
                  "seconds": round(time.time() - t0, 2)}
