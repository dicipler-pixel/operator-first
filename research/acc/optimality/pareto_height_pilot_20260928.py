#!/usr/bin/env python3
"""Small exact pilot for Pareto labels (moves, maximum total relator length).

Run with the pinned SAIR verifier's ``competition/tools`` directory on
PYTHONPATH, for example:
  PYTHONPATH=/path/to/Andrews-Curtis/competition/tools python3 \
    pareto_height_pilot_20260928.py

The target is generated from the standard pair by SEED. This is an algorithm
control, not a scored ACC challenge or a shortest-path claim beyond depth 5.
"""

import json
import time

from verifier import core


START = ((1,), (2,))
SEED = [6, 4, 12, 4, 12]
DEPTH_LIMIT = 5


def height(state):
    return len(state[0]) + len(state[1])


def pareto_search(start, target, depth_limit):
    """Enumerate nondominated (depth, peak-height) labels per exact state."""
    labels = {start: {(0, height(start))}}
    frontier = [(start, 0, height(start))]
    expanded = generated = 0
    for _ in range(depth_limit):
        following = []
        for state, depth, peak in frontier:
            if (depth, peak) not in labels.get(state, set()):
                continue  # a later label dominated this queued item
            expanded += 1
            for move in range(core.NUM_MOVES):
                child = core.apply_move(state, move)
                child_depth = depth + 1
                child_peak = max(peak, height(child))
                generated += 1
                child_labels = labels.setdefault(child, set())
                if any(d <= child_depth and h <= child_peak
                       for d, h in child_labels):
                    continue
                dominated = [
                    (d, h) for d, h in child_labels
                    if child_depth <= d and child_peak <= h
                ]
                child_labels.difference_update(dominated)
                child_labels.add((child_depth, child_peak))
                following.append((child, child_depth, child_peak))
        frontier = following
    return labels, expanded, generated


def capped_bfs(start, target, cap, depth_limit):
    """Return first target distance and counts for one exact height cap."""
    if height(start) > cap:
        return None, 0, 0, 0
    seen = {start}
    layer = [start]
    expanded = generated = 0
    for depth in range(1, depth_limit + 1):
        following = []
        for state in layer:
            expanded += 1
            for move in range(core.NUM_MOVES):
                generated += 1
                child = core.apply_move(state, move)
                if height(child) > cap or child in seen:
                    continue
                if child == target:
                    return depth, len(seen), expanded, generated
                seen.add(child)
                following.append(child)
        layer = following
    return None, len(seen), expanded, generated


def main():
    target = START
    for move in SEED:
        target = core.apply_move(target, move)

    started = time.perf_counter()
    labels, pareto_expanded, pareto_generated = pareto_search(
        START, target, DEPTH_LIMIT
    )
    pareto_seconds = time.perf_counter() - started
    target_frontier = sorted(labels.get(target, set()))
    max_target_peak = max((h for _, h in target_frontier), default=height(START))

    cap_rows = []
    for cap in range(height(START), max_target_peak + 1):
        best_from_labels = min(
            (depth for depth, peak in target_frontier if peak <= cap),
            default=None,
        )
        distance, seen, expanded, generated = capped_bfs(
            START, target, cap, DEPTH_LIMIT
        )
        assert distance == best_from_labels
        cap_rows.append({
            "cap": cap,
            "pareto_distance": best_from_labels,
            "capped_bfs_distance": distance,
            "seen_states": seen,
            "expanded_states": expanded,
            "generated_transitions": generated,
        })

    print(json.dumps({
        "scope": "synthetic control from standard pair; depth <= 5",
        "seed_path": SEED,
        "target_relators": [list(w) for w in target],
        "target_pareto_labels_depth_peak": target_frontier,
        "pareto_state_count": len(labels),
        "pareto_label_count": sum(map(len, labels.values())),
        "pareto_expanded_labels": pareto_expanded,
        "pareto_generated_transitions": pareto_generated,
        "pareto_wall_seconds": round(pareto_seconds, 6),
        "cap_bfs": cap_rows,
        "cap_bfs_aggregate_expanded": sum(r["expanded_states"] for r in cap_rows),
        "cap_bfs_aggregate_transitions": sum(r["generated_transitions"] for r in cap_rows),
        "cap_bfs_aggregate_seen_state_counts": sum(r["seen_states"] for r in cap_rows),
        "result": "distance envelopes agree; Pareto used more transitions on this small control",
    }, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
