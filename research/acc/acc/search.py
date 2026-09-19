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


def min_height(closure: Closure) -> int:
    """Smallest total relator length anywhere in the component."""
    from .words import decode_state
    return min(total_length(decode_state(k)) for k in closure.visited)


def complete_frontier(closure: Closure, cap: int) -> List[tuple]:
    """EVERY directed edge from the component to a state above the cap.

    This is the frontier required by `ACCFrontier.cap_closed_exit_forces_above_cap_edge`
    (see `proof/`).  The theorem deliberately does not assume a first exit has
    height cap+1 -- an ordinary AC move can jump several length levels -- so a
    frontier restricted to the cheapest exits is NOT a complete frontier and
    must never be used as one in a mandatory-hump argument.
    """
    out = []
    for state in closure.boundary:
        for move_id, child in children(state):
            if total_length(child) > cap:
                out.append((state, move_id, child, total_length(child)))
    return out


def mandatory_hump_certificate(closure: Closure, start: Presentation, cap: int) -> dict:
    """Check the hypotheses of `ACCWell.descent_forces_cap_exit` (see `proof/`).

    Hypotheses, in the theorem's order:
      hstart   -- start is in the component;
      hclosed  -- the component is closed under every move whose target stays at
                  height <= cap.  A BFS that emptied its frontier gives exactly
                  this; a BUDGET run does NOT, and the certificate is refused;
      hlower   -- no state of the component is lower than the start.

    On success the conclusion is: every finite move sequence from `start` that
    ends lower than `start` must visit a state of total length > cap.
    """
    h0 = total_length(start)
    lo = min_height(closure)
    frontier = complete_frontier(closure, cap)
    heights = sorted({h for _, _, _, h in frontier})
    hyp = {
        "hstart": encode_state(start) in closure.visited,
        "hclosed": closure.status == "CLOSED",
        "hlower": lo >= h0,
    }
    ok = all(hyp.values())
    return {
        "theorem": "ACCWell.descent_forces_cap_exit",
        "hypotheses": hyp,
        "holds": ok,
        "cap": cap,
        "start_height": h0,
        "component_min_height": lo,
        "component_size": closure.size,
        "complete_frontier_edges": len(frontier),
        "distinct_exit_heights": heights,
        "exit_jumps_more_than_one_level": bool(heights and max(heights) > cap + 1),
        "conclusion": (
            f"every finite move sequence from the start that ends below total length "
            f"{h0} must visit a state of total length > {cap}"
        ) if ok else None,
        "refused_because": None if ok else [k for k, v in hyp.items() if not v],
    }


def cheapest_exits(closure: Closure, cap: int) -> List[Presentation]:
    """Distinct over-cap children of MINIMUM total length.

    A reporting slice, not the complete frontier -- see `complete_frontier`.
    """
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
