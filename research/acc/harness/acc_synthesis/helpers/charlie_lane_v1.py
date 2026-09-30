#!/usr/bin/env python3
"""Charlie-inspired exact total-length-cap ladder, offline and resource bounded.

The archival disk engine and B36 ball are preserved separately. This small-memory
replacement uses the frozen official move kernel, exact ordered states, and complete
layers; partial layers are never promoted to negative certificates.
"""
from __future__ import annotations

import argparse
from collections import deque
import hashlib
import json
import math
from pathlib import Path
import resource
import shutil
import sqlite3
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from vendor.verifier import core
import official_checker

RULESET = "e13f57d82b5db1a79c1bd9d5ee1f6665ac4d96a634a3656ea20c0ada82e07643"
GOAL_RADIUS = 5


def save(path, obj):
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def rss_mib():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024


def address_limit(mib):
    ceiling = mib * 1024 * 1024
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS,
                       (min(soft, ceiling) if soft >= 0 else ceiling, hard))


def controller_stopped():
    db = ROOT / 'state/ledger.sqlite3'
    if not db.exists(): return False
    with sqlite3.connect('file:' + str(db) + '?mode=ro', uri=True) as conn:
        row = conn.execute('SELECT stopped FROM control WHERE singleton=1').fetchone()
    return bool(row and row[0])


def state_json(s):
    return [list(s[0]), list(s[1])]


def trace(records, state):
    out = []
    while records[state][0] is not None:
        parent, move, _ = records[state]
        out.append(move)
        state = parent
    return list(reversed(out))


def exact_cap(start, goal, cap, radius, quota, deadline, memory_mib, target_length,
              stop_check=lambda: False):
    """Start BFS against a complete goal radius; quota counts admitted records.

    A smaller cap is subsumed by any completed larger-cap search. We retain all
    visited exact states, rather than invoking Charlie's undirected two-layer
    subtraction, to make partial-budget accounting transparent.
    """
    began = time.monotonic()
    records = [{goal: (None, None, 0)}, {start: (None, None, 0)}]
    queues = [deque([goal]), deque([start])]
    depth_done = [-1, -1]
    expanded = [[], []]
    generated = 0
    excluded_by_cap = 0
    duplicates = 0
    admitted = 2
    phase = 0
    partial = None
    reason = None
    hit = None
    reserve = bytearray(4 * 1024 * 1024)
    try:
        if start == goal:
            hit = (start, 0)
        while hit is None:
            if phase == 0 and (not queues[0] or records[0][queues[0][0]][2] >= radius):
                depth_done[0] = radius if queues[0] else max((v[2] for v in records[0].values()), default=0)
                phase = 1
                if start in records[0] and records[0][start][2] < target_length:
                    hit = (start, records[0][start][2]); break
            if not queues[phase]:
                reason = "component_closed" if phase == 1 else "goal_component_closed"
                break
            level = records[phase][queues[phase][0]][2]
            count = 0
            while queues[phase] and records[phase][queues[phase][0]][2] == level:
                partial = {"side": "goal" if phase == 0 else "start", "depth": level,
                           "expanded_in_layer": count}
                if stop_check():
                    reason = "controller_stopped"; break
                if time.monotonic() >= deadline:
                    reason = "wall_time_cap"; break
                if rss_mib() >= memory_mib - 32:
                    reason = "memory_headroom_cap"; break
                s = queues[phase].popleft()
                count += 1
                for m in range(core.NUM_MOVES):
                    generated += 1
                    nxt = core.apply_move(s, m)
                    if len(nxt[0]) + len(nxt[1]) > cap:
                        excluded_by_cap += 1; continue
                    if nxt in records[phase]:
                        duplicates += 1; continue
                    if admitted >= quota:
                        reason = "node_cap"; break
                    records[phase][nxt] = (s, m, level + 1)
                    admitted += 1
                    queues[phase].append(nxt)
                    if phase == 1 and nxt in records[0]:
                        distance = level + 1 + records[0][nxt][2]
                        if distance < target_length:
                            hit = (nxt, distance)
                            break
                if reason or hit: break
            expanded[phase].append({"depth": level, "expanded": count,
                                    "complete": not reason and not hit})
            if reason or hit: break
            depth_done[phase] = level
        if hit:
            mid, length = hit
            left = trace(records[1], mid)
            right = trace(records[0], mid)
            route = left + [core.INVERSE_MOVE[m] for m in reversed(right)]
            assert len(route) == length
        else:
            route = None
    except MemoryError:
        del reserve
        reason = "memory_error"
        route = None
    return route, {
        "cap": cap, "goal_radius": radius, "termination_reason": reason or "candidate_found",
        "complete_under_cap": reason in ("component_closed", "goal_component_closed"),
        "admitted_records": admitted, "unique_states": {"goal": len(records[0]), "start": len(records[1])},
        "generated_moves": generated, "excluded_by_cap": excluded_by_cap, "duplicates": duplicates,
        "completed_expansion_depth": {"goal": depth_done[0], "start": depth_done[1]},
        "expanded_layers": {"goal": expanded[0], "start": expanded[1]},
        "partial_layer": partial if reason in ("node_cap", "wall_time_cap", "memory_headroom_cap", "controller_stopped", "memory_error") else None,
        "elapsed_seconds": time.monotonic() - began, "peak_rss_mib": rss_mib(),
        "bounded_negative_through": (depth_done[0] + depth_done[1]
             if depth_done[0] >= 0 and depth_done[1] >= 0 else None),
    }


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--row', required=True)
    p.add_argument('--output-dir', required=True)
    p.add_argument('--wall-seconds', type=float, default=180)
    p.add_argument('--node-cap', type=int, default=600000)
    p.add_argument('--target-length', type=int, default=44)
    p.add_argument('--memory-mib', type=int, default=1024)
    p.add_argument('--caps', default=None, help='ascending total-length caps, default start+8,+10,+12')
    p.add_argument('--goal-radius', type=int, default=GOAL_RADIUS)
    a = p.parse_args(argv)
    if not math.isfinite(a.wall_seconds) or not 0 < a.wall_seconds <= 180 or not 1 <= a.node_cap <= 600000 or not 64 <= a.memory_mib <= 1024 or a.target_length < 0 or not 0 <= a.goal_radius <= 5:
        p.error('bounds: wall (0,180], nodes [1,600000], memory [64,1024], goal radius [0,5]')
    out = Path(a.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    if any(out.iterdir()): raise SystemExit('output directory must be empty')
    address_limit(a.memory_mib)
    _, _, data, challenges = official_checker.load_kernel()
    challenge = challenges[a.row]
    assert challenge['move_spec_version'] == core.MOVE_SPEC_VERSION
    start = tuple(tuple(r) for r in challenge['initial_relators'])
    goal = tuple(tuple(r) for r in challenge['target_relators'])
    route_path = ROOT / 'continuation/routes.json'
    if not route_path.exists(): route_path = ROOT / 'integration/recovered_routes.json'
    routes = json.loads(route_path.read_text())['routes']
    saved = [r for r in routes if r['row_id'] == a.row]
    baseline = min(saved, key=lambda r: len(r['moves'])) if saved else None
    baseline_length = len(baseline['moves']) if baseline else None
    baseline_receipt = core.verify(challenge, baseline['moves'], 'ac-r2-v1', data['limits']) if baseline else None
    if baseline_receipt and not baseline_receipt['ok']: raise RuntimeError('baseline failed official replay')
    save(out / 'baseline.json', {"row_id": a.row, "moves": baseline['moves'] if baseline else None,
          "length": baseline_length, "sources": baseline.get('sources', []) if baseline else [],
          "official_receipt": baseline_receipt})
    shutil.copy2(__file__, out / 'executed_charlie_lane_v1.py')
    tests = ROOT / 'tests/test_charlie_lane.py'
    if tests.exists(): shutil.copy2(tests, out / 'executed_test_charlie_lane.py')
    deadline = time.monotonic() + a.wall_seconds
    remaining = a.node_cap
    caps = ([int(x) for x in a.caps.split(',')] if a.caps else
            [sum(map(len, start)) + d for d in (8, 10, 12)])
    if caps != sorted(set(caps)) or caps[0] < sum(map(len, start)):
        raise ValueError('caps must increase from at least start total length')
    coverage = []
    winner = None
    for cap in caps:
        if remaining <= 1 or time.monotonic() >= deadline: break
        route, report = exact_cap(start, goal, cap, a.goal_radius, remaining, deadline,
                                  a.memory_mib, min(a.target_length + 1, baseline_length) if baseline else a.target_length + 1,
                                  stop_check=controller_stopped)
        coverage.append(report)
        remaining -= report['admitted_records']
        if route:
            receipt = core.verify(challenge, route, 'ac-r2-v1', data['limits'])
            if not receipt['ok']: raise RuntimeError('search route failed official replay')
            if baseline_length is None or len(route) < baseline_length:
                winner = route
                save(out / 'candidate.json', {"row_id": a.row, "track": "AC",
                     "start": [''.join({1:'x',-1:'X',2:'y',-2:'Y'}[l] for l in w) for w in start],
                     "moves": route, "ruleset_sha256": RULESET, "evidence_grade": "V",
                     "family": "charlie-exact-total-length-cap"})
                save(out / 'receipt.json', receipt)
            break
        if not report['complete_under_cap']: break
    save(out / 'coverage.json', {"row_id": a.row, "caps_requested": caps,
         "caps_executed": coverage, "limits": {"wall_seconds": a.wall_seconds,
             "node_cap": a.node_cap, "memory_mib": a.memory_mib, "target_length": a.target_length},
         "saved_baseline_length": baseline_length, "baseline_source": str(route_path.relative_to(ROOT)),
         "winner_length": len(winner) if winner else None,
         "scope": "exact ordered freely reduced AC states; no cyclic or permutation quotient; incomplete cap is not exhaustive"})
    result = {"kind": "candidate" if winner else "bounded_miss", "summary":
              (f'Officially replayed {len(winner)}-move route' if winner else 'No saved-baseline improvement in bounded cap probe'),
              "limits": {"wall_seconds": a.wall_seconds, "node_cap": a.node_cap, "memory_mib": a.memory_mib},
              "actual_coverage": coverage, "termination_reason": coverage[-1]['termination_reason'] if coverage else 'unstarted',
              "reopen_when": {"event": "higher_exact_cap_capacity", "row_id": a.row}, "evidence": []}
    if winner: result['candidate'] = json.loads((out / 'candidate.json').read_text())
    save(out / 'worker_result.json', result)
    for name in ('baseline.json', 'coverage.json', 'executed_charlie_lane_v1.py',
                 'executed_test_charlie_lane.py', 'candidate.json', 'receipt.json'):
        path = out / name
        if path.exists(): result['evidence'].append({"path": str(path.relative_to(ROOT)),
                        "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    save(out / 'worker_result.json', result)
    print(json.dumps({"kind": result['kind'], "row_id": a.row,
                      "result_path": str((out / 'worker_result.json').relative_to(ROOT)),
                      "coverage_path": str((out / 'coverage.json').relative_to(ROOT)),
                      "termination_reason": result['termination_reason'],
                      "admitted_records": sum(x['admitted_records'] for x in coverage),
                      "winner_length": len(winner) if winner else None}))


if __name__ == '__main__':
    main()
