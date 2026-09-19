"""Suffix dictionary and splice compiler.

A suffix dictionary maps an exact state to a known exact move list reaching the
ordered target (x, y).  Two sources, both exact:

1. every state lying on a verified certificate path (its remaining tail is a
   suffix by construction);
2. a backward ball from the target, built with the official inverse column.

A forward state that collides with the dictionary yields prefix + stored suffix.
That candidate is still only a candidate: it goes through the official verifier
and an independent replay before it is called anything (W13).
"""

from __future__ import annotations

from collections import deque
from typing import Dict, Iterable, Optional, Sequence, Tuple

from .moves import INVERSE, N_MOVES, TARGET, apply_move
from .words import encode_state, total_length


class SuffixDictionary:
    def __init__(self):
        self.tail: Dict[bytes, tuple] = {}
        self.sources: Dict[str, int] = {}

    def __len__(self) -> int:
        return len(self.tail)

    def add(self, state, suffix: Sequence[int], source: str) -> bool:
        """Keep the shortest known suffix for each exact state."""
        key = encode_state(state)
        cur = self.tail.get(key)
        if cur is None or len(suffix) < len(cur):
            self.tail[key] = tuple(suffix)
            if cur is None:
                self.sources[source] = self.sources.get(source, 0) + 1
            return True
        return False

    def get(self, state) -> Optional[tuple]:
        return self.tail.get(encode_state(state))

    def add_certificate_path(self, start, moves: Sequence[int], source: str) -> int:
        """Every state on a verified path carries its own remaining tail."""
        state = start
        added = 0
        for i, m in enumerate(moves):
            added += bool(self.add(state, moves[i:], source))
            state = apply_move(state, m)
        added += bool(self.add(state, (), source))
        return added

    def add_backward_ball(self, depth: int, length_cap: int,
                          max_states: int = 3_000_000, source: str = "backward-ball") -> int:
        """Exact backward BFS from the target using the official inverse column."""
        self.add(TARGET, (), source)
        frontier = [(TARGET, ())]
        added = 0
        for _ in range(depth):
            nxt = []
            for state, suffix in frontier:
                for m in range(N_MOVES):
                    parent = apply_move(state, INVERSE[m])
                    if total_length(parent) > length_cap or parent == state:
                        continue
                    tail = (m,) + suffix
                    if self.add(parent, tail, source):
                        added += 1
                        nxt.append((parent, tail))
                if len(self.tail) > max_states:
                    return added
            frontier = nxt
            if not frontier:
                break
        return added


def forward_splice(start, sd: SuffixDictionary, depth: int, length_cap: int,
                   max_states: int = 2_000_000):
    """Forward BFS from `start`, testing every state against the dictionary.

    Returns (moves, stats).  `moves` is a complete candidate path, or None.
    """
    hit = sd.get(start)
    if hit is not None:
        return list(hit), {"result": "SPLICE", "met_at_depth": 0, "expanded": 0}
    seen = {encode_state(start): ()}
    frontier = [(start, ())]
    expanded = 0
    for d in range(1, depth + 1):
        nxt = []
        for state, prefix in frontier:
            for m in range(N_MOVES):
                child = apply_move(state, m)
                if total_length(child) > length_cap or child == state:
                    continue
                key = encode_state(child)
                if key in seen:
                    continue
                path = prefix + (m,)
                expanded += 1
                tail = sd.tail.get(key)
                if tail is not None:
                    return list(path + tail), {"result": "SPLICE", "met_at_depth": d,
                                               "prefix_len": len(path), "suffix_len": len(tail),
                                               "expanded": expanded}
                seen[key] = path
                nxt.append((child, path))
            if len(seen) > max_states:
                return None, {"result": "NO_SPLICE", "stop_reason": "STATE_BUDGET_REACHED",
                              "depth_reached": d, "expanded": expanded, "seen": len(seen)}
        frontier = nxt
        if not frontier:
            return None, {"result": "NO_SPLICE", "stop_reason": "FORWARD_BALL_EXHAUSTED_UNDER_CAP",
                          "depth_reached": d, "expanded": expanded, "seen": len(seen)}
    return None, {"result": "NO_SPLICE", "stop_reason": "DEPTH_LIMIT",
                  "depth_reached": depth, "expanded": expanded, "seen": len(seen)}
