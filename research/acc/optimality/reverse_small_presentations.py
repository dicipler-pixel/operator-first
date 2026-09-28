#!/usr/bin/env python3
"""Exact small-endpoint AC distances under the SAIR ac-r2-v1 move table.

Enumerates all ordered, freely reduced relator pairs with total length <=6
and abelianization determinant +/-1. BFS uses the literal 14 AC moves, with
only the intermediate *total relator length* capped at 6. For each observed
maximum, an uncapped bidirectional-ball intersection proves that no shorter
route exists, even if it wanders through arbitrarily long relators.

This is a finite small-endpoint statement, not a uniform AC bound.
"""

import hashlib
import json
from collections import Counter, deque

LETTERS = (1, -1, 2, -2)
ROOT = ((1,), (2,))
CAP = 6
INVERSE_MOVE = (0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12)


def reduce_word(word):
    out = []
    for a in word:
        if out and out[-1] == -a:
            out.pop()
        else:
            out.append(a)
    return tuple(out)


def inverse(word):
    return tuple(-a for a in reversed(word))


def move(state, m):
    a, b = state
    if m == 0:
        return inverse(a), b
    if m == 1:
        return a, inverse(b)
    if m == 2:
        return reduce_word(a + b), b
    if m == 3:
        return reduce_word(a + inverse(b)), b
    if m == 4:
        return a, reduce_word(b + a)
    if m == 5:
        return a, reduce_word(b + inverse(a))
    if m < 10:
        g = LETTERS[m - 6]
        return reduce_word((g,) + a + (-g,)), b
    g = LETTERS[m - 10]
    return a, reduce_word((g,) + b + (-g,))


def length(state):
    return len(state[0]) + len(state[1])


def words(max_length):
    by_length = {1: [(a,) for a in LETTERS]}
    for n in range(2, max_length + 1):
        by_length[n] = [w + (a,) for w in by_length[n - 1]
                        for a in LETTERS if a != -w[-1]]
    return by_length


def abelianization(word):
    return (word.count(1) - word.count(-1),
            word.count(2) - word.count(-2))


def determinant_one_states(cap):
    by_length = words(cap - 1)
    states = set()
    for n in range(2, cap + 1):
        for i in range(1, n):
            for a in by_length[i]:
                ax, ay = abelianization(a)
                for b in by_length[n - i]:
                    bx, by = abelianization(b)
                    if abs(ax * by - ay * bx) == 1:
                        states.add((a, b))
    return states


def capped_bfs(cap):
    # Value: (distance, predecessor, move from predecessor); root is special.
    seen = {ROOT: (0, None, None)}
    queue = deque([ROOT])
    while queue:
        state = queue.popleft()
        d = seen[state][0]
        for m in range(14):
            nxt = move(state, m)
            if length(nxt) <= cap and nxt not in seen:
                seen[nxt] = (d + 1, state, m)
                queue.append(nxt)
    return seen


def uncapped_ball(start, depth):
    seen = {start}
    frontier = {start}
    for _ in range(depth):
        frontier = {move(state, m) for state in frontier for m in range(14)} - seen
        seen.update(frontier)
    return seen


def capped_route_to_root(state, bfs):
    route = []
    while state != ROOT:
        _, state, m = bfs[state]
        route.append(INVERSE_MOVE[m])
    return route


def digest(states):
    raw = json.dumps(sorted(states), separators=(",", ":"))
    return hashlib.sha256(raw.encode()).hexdigest()


def main():
    candidates = determinant_one_states(CAP)
    bfs = capped_bfs(CAP)
    assert set(bfs) == candidates, "candidate coverage failed"
    profiles = []
    for end_length in range(2, CAP + 1):
        subset = [s for s in candidates if length(s) <= end_length]
        top = max(bfs[s][0] for s in subset)
        witness = min(s for s in subset if bfs[s][0] == top)
        route = capped_route_to_root(witness, bfs)
        current = witness
        for m in route:
            current = move(current, m)
            assert length(current) <= CAP
        assert current == ROOT
        # If a shorter route of at most top-1 existed, the uncapped balls
        # around the root/witness would intersect after top-1 moves.
        left_depth = (top - 1) // 2
        right_depth = (top - 1) - left_depth
        left = uncapped_ball(ROOT, left_depth)
        right = uncapped_ball(witness, right_depth)
        assert left.isdisjoint(right), "uncapped shortcut to witness"
        profiles.append({
            "endpoint_max_total_length": end_length,
            "candidate_count": len(subset),
            "unrestricted_max_shortest_moves": top,
            "witness": witness,
            "witness_route_to_root": route,
            "uncapped_lower_bound_ball_depths": [left_depth, right_depth],
            "uncapped_ball_sizes": [len(left), len(right)],
        })
    result = {
        "move_spec": "SAIR ac-r2-v1 (ordered pair, 14 moves, no swap)",
        "intermediate_length_cap_for_upper_bounds": CAP,
        "candidate_count": len(candidates),
        "reachable_count": len(bfs),
        "max_capped_distance": max(v[0] for v in bfs.values()),
        "candidates_sha256": digest(candidates),
        "reachable_sha256": digest(bfs),
        "capped_distance_histogram": dict(sorted(Counter(v[0] for v in bfs.values()).items())),
        "profiles": profiles,
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
