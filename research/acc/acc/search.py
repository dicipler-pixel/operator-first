"""Exact capped search over official AC moves.

A run that hits its budget is BUDGET, never CLOSED.
"""

from __future__ import annotations

from collections import deque
from typing import Dict, List, Sequence

from .moves import Presentation, apply_move, children, parents, N_MOVES
from .words import encode_state, normalize_ordinary, total_length


class Closure:
    def __init__(self, status: str, visited: set, boundary: list, exits: int):
        self.status = status           # "CLOSED" | "BUDGET"
        self.visited = visited
        self.boundary = boundary
        self.exits = exits

    @property
    def size(self) -> int:
        return len(self.visited)


def capped_closure(start: Presentation, cap: int, max_states: int) -> Closure:
    """BFS over exact ordered presentations of total length <= cap."""
    if total_length(start) > cap:
        raise ValueError("start already exceeds the cap")
    seen = {encode_state(start)}
    queue = deque([start])
    boundary: list = []
    exits = 0
    status = "CLOSED"
    while queue:
        if len(seen) > max_states:
            status = "BUDGET"
            break
        state = queue.popleft()
        over = False
        for _, child in children(state):
            if total_length(child) > cap:
                over = True
                exits += 1
                continue
            key = encode_state(child)
            if key not in seen:
                seen.add(key)
                queue.append(child)
        if over:
            boundary.append(state)
    return Closure(status, seen, boundary, exits)


def cheapest_exits(closure: Closure, cap: int) -> List[Presentation]:
    """Distinct over-cap children of minimum total length."""
    best: Dict[int, list] = {}
    for state in closure.boundary:
        for _, child in children(state):
            t = total_length(child)
            if t > cap:
                best.setdefault(t, []).append(child)
    if not best:
        return []
    lo = min(best)
    out, seen = [], set()
    for child in best[lo]:
        k = encode_state(child)
        if k not in seen:
            seen.add(k)
            out.append(child)
    return out


def ball(start: Presentation, depth: int, backward: bool = False) -> dict:
    """Unrestricted exact ball: {state_key: distance}."""
    step = parents if backward else children
    seen = {encode_state(start): 0}
    frontier = [start]
    for d in range(1, depth + 1):
        nxt = []
        for state in frontier:
            for _, nb in step(state):
                key = encode_state(nb)
                if key not in seen:
                    seen[key] = d
                    nxt.append(nb)
        frontier = nxt
    return seen


def exact_distance(a: Presentation, b: Presentation, max_depth: int):
    """Bidirectional exact distance, or a disjointness certificate.

    Returns ``(distance, evidence)``.  When no path is found, ``distance`` is
    None and the evidence records the two ball sizes and the bound they prove:
    balls of radius d from both ends, disjoint, means no path of length <= 2d.
    """
    fwd = {encode_state(a): 0}
    bwd = {encode_state(b): 0}
    ff, bf = [a], [b]
    for d in range(1, max_depth + 1):
        nxt = []
        for s in ff:
            for _, c in children(s):
                k = encode_state(c)
                if k not in fwd:
                    fwd[k] = d
                    nxt.append(c)
        ff = nxt
        hit = set(fwd) & set(bwd)
        if hit:
            return min(fwd[k] + bwd[k] for k in hit), {"met_at_depth": d}
        nxt = []
        for s in bf:
            for _, c in parents(s):
                k = encode_state(c)
                if k not in bwd:
                    bwd[k] = d
                    nxt.append(c)
        bf = nxt
        hit = set(fwd) & set(bwd)
        if hit:
            return min(fwd[k] + bwd[k] for k in hit), {"met_at_depth": d}
    return None, {"forward_ball": len(fwd), "backward_ball": len(bwd),
                  "radius": max_depth, "disjoint": True,
                  "proves": f"no path of length <= {2 * max_depth}"}


def ordinary_reps(states) -> set:
    return {normalize_ordinary(s) for s in states}
