#!/usr/bin/env python3
"""Offline exact saved-route union and deterministic bounded bridge search.

Only ordered freely reduced states are keyed. No cyclic, relator-permutation,
or generator normalization occurs. Move semantics come from the pinned kernel.
The fresh phase is layered bidirectional multi-source BFS: each seed has its
shortest saved-union prefix/suffix cost. For each (state, fresh-depth, side),
only the least cumulative cost label is retained. A collision joins two exact
paths when the sum of fresh depths is at most --depth. All caps bound this run,
not the AC problem. Search scheduling may stop in a partial layer.
"""
from __future__ import annotations
import argparse
from collections import deque
import hashlib
import json
import math
from pathlib import Path
import resource
import sqlite3
import sys
import time

import official_checker

ROOT = Path(__file__).resolve().parent


def dump(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def state_json(state):
    return [list(w) for w in state]


def replay_states(core, start, moves):
    states = [start]
    for move in moves:
        if type(move) is not int or not 0 <= move < core.NUM_MOVES:
            raise ValueError('saved route has invalid move id')
        states.append(core.apply_move(states[-1], move))
    return states


def shortest_paths(graph, origin):
    """BFS on explicit exact directed edges; return reproducible move paths."""
    paths = {origin: []}
    queue = deque([origin])
    while queue:
        current = queue.popleft()
        for neighbor, move in sorted(graph[current], key=lambda e: (e[1], e[0])):
            if neighbor not in paths:
                paths[neighbor] = paths[current] + [move]
                queue.append(neighbor)
    return paths


def saved_union(core, start, target, routes):
    graph = {start: set(), target: set()}
    traces = []
    for route in routes:
        states = replay_states(core, start, route['moves'])
        if states[-1] != target:
            raise ValueError('saved route fails exact endpoint')
        traces.append(states)
        for source, move, dest in zip(states, route['moves'], states[1:]):
            graph.setdefault(source, set()).add((dest, move))
            graph.setdefault(dest, set()).add((source, core.INVERSE_MOVE[move]))
    prefix = shortest_paths(graph, start)
    backwards = shortest_paths(graph, target)
    suffix = {s: [core.INVERSE_MOVE[m] for m in reversed(p)]
              for s, p in backwards.items()}
    return graph, traces, prefix, suffix


def stopped():
    database = ROOT / 'state/ledger.sqlite3'
    if not database.exists():
        return False
    with sqlite3.connect('file:' + str(database) + '?mode=ro', uri=True) as conn:
        row = conn.execute('SELECT stopped FROM control WHERE singleton=1').fetchone()
    return bool(row and row[0])


def peak_rss_mib():
    # This runner is Linux; ru_maxrss is KiB.
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024


def bounded_bridge(core, prefix, suffix, baseline, *, wall_seconds=180,
                   node_cap=600000, depth=8, target_length=31,
                   max_total_length=10000, memory_mib=1024, stop_check=stopped):
    """Return best complete moves and measured coverage of one fresh run.

    Records are immutable, even when a lower-cost label replaces a key, so
    reconstructing descendants cannot silently change a path or its cost.
    Node cap counts ALL admitted records, including replaced labels and seeds.
    Depth is total fresh bridge length; each side explores at most ceil(depth/2).
    Odd depth therefore tests balanced splits up to this bound, not every split.
    """
    started = time.monotonic()
    deadline = started + wall_seconds
    side_depth = (depth + 1) // 2
    best = list(baseline) if baseline is not None else None
    # record = (state, fresh_depth, cumulative_cost, parent_id, move, seed)
    records = [[], []]
    tables = [{}, {}]  # exact state -> fresh-depth -> latest record id
    layers = [[deque() for _ in range(side_depth + 1)] for _ in range(2)]
    counts = {'admitted_records': 0, 'generated_moves': 0, 'collision_pairs': 0,
              'duplicate_or_dominated': 0, 'replaced_labels': 0,
              'length_pruned': 0, 'cost_pruned': 0, 'stale_queue_labels': 0,
              'expanded_by_side_depth': [[0]*(side_depth+1) for _ in range(2)],
              'admitted_by_side_depth': [[0]*(side_depth+1) for _ in range(2)],
              'improvements': []}
    reason = 'depth_exhausted'
    partial = None
    # Reserve enough headroom to emit a result on MemoryError.
    reserve = bytearray(8 * 1024 * 1024)

    def route(side, rid):
        moves = []
        record = records[side][rid]
        while record[3] is not None:
            moves.append(record[4])
            record = records[side][record[3]]
        if side == 0:
            return prefix[record[5]] + list(reversed(moves))
        return [core.INVERSE_MOVE[m] for m in moves] + suffix[record[5]]

    def add(side, state, fresh, cost, parent, move, seed):
        nonlocal best
        previous = tables[side].get(state, {}).get(fresh)
        if previous is not None and records[side][previous][2] <= cost:
            counts['duplicate_or_dominated'] += 1
            return
        if counts['admitted_records'] >= node_cap:
            raise OverflowError('node_cap')
        if previous is not None:
            counts['replaced_labels'] += 1
        rid = len(records[side])
        records[side].append((state, fresh, cost, parent, move, seed))
        tables[side].setdefault(state, {})[fresh] = rid
        layers[side][fresh].append(rid)
        counts['admitted_records'] += 1
        counts['admitted_by_side_depth'][side][fresh] += 1
        for other_depth, other_id in tables[1-side].get(state, {}).items():
            if fresh + other_depth > depth:
                continue
            counts['collision_pairs'] += 1
            total = cost + records[1-side][other_id][2]
            if best is None or total < len(best):
                ids = (rid, other_id) if side == 0 else (other_id, rid)
                candidate = route(0, ids[0]) + route(1, ids[1])
                if len(candidate) != total:
                    raise AssertionError('label cost does not match reconstruction')
                best = candidate
                counts['improvements'].append({'length': total,
                    'fresh_depths': [records[0][ids[0]][1], records[1][ids[1]][1]],
                    'meeting_state': state_json(state),
                    'elapsed_seconds': time.monotonic()-started})

    try:
        for side, seeds in enumerate((prefix, suffix)):
            for seed in sorted(seeds, key=lambda s: (len(seeds[s]), s)):
                add(side, seed, 0, len(seeds[seed]), None, None, seed)
        for fresh in range(side_depth):
            # Fixed deterministic side order and FIFO layer expansion.
            for side in (0, 1):
                queue = layers[side][fresh]
                while queue:
                    partial = {'side': side, 'depth': fresh}
                    if stop_check():
                        reason = 'controller_stopped'
                        raise InterruptedError(reason)
                    if time.monotonic() >= deadline:
                        reason = 'wall_time_cap'
                        raise InterruptedError(reason)
                    if peak_rss_mib() >= memory_mib - 32:
                        reason = 'memory_headroom_cap'
                        raise InterruptedError(reason)
                    rid = queue.popleft()
                    state, d, cost, _, last, _ = records[side][rid]
                    if tables[side][state][d] != rid:
                        counts['stale_queue_labels'] += 1
                        continue
                    if best is not None and cost >= len(best):
                        counts['cost_pruned'] += 1
                        continue
                    counts['expanded_by_side_depth'][side][d] += 1
                    for move in range(core.NUM_MOVES):
                        counts['generated_moves'] += 1
                        dest = core.apply_move(state, move)
                        if len(dest[0]) + len(dest[1]) > max_total_length:
                            counts['length_pruned'] += 1
                            continue
                        add(side, dest, d+1, cost+1, rid, move, None)
                    if best is not None and len(best) <= target_length:
                        reason = 'target_found'
                        raise InterruptedError(reason)
        partial = None
    except OverflowError:
        reason = 'node_cap'
    except InterruptedError:
        pass
    except MemoryError:
        reserve = None
        reason = 'address_space_cap'
    reserve = None
    counts.update({'termination_reason': reason,
        'elapsed_seconds': time.monotonic()-started,
        'peak_rss_mib': peak_rss_mib(),
        'unique_states_by_side': [len(t) for t in tables],
        'latest_labels_by_side': [sum(len(v) for v in t.values()) for t in tables],
        'pending_by_side_depth': [[len(q) for q in side] for side in layers],
        'partial_layer': partial, 'target_length': target_length,
        'best_length': len(best) if best is not None else None,
        'total_bridge_depth_cap': depth, 'per_side_depth_cap': side_depth,
        'coverage_scope': 'Only admitted exact labels and generated moves under caps; no impossibility claim.'})
    return best, counts


def candidate_for(row, start, moves, ruleset):
    return {'row_id': row, 'track': 'AC', 'start': official_checker.render(start),
            'moves': moves, 'ruleset_sha256': ruleset,
            'evidence_grade': 'V', 'family': 'exact-multipath-bridge'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--row', required=True)
    parser.add_argument('--output-dir', required=True)
    parser.add_argument('--routes', default='integration/recovered_routes.json')
    parser.add_argument('--wall-seconds', type=float, default=180)
    parser.add_argument('--node-cap', type=int, default=600000)
    parser.add_argument('--profile', choices=['route-local'], default='route-local')
    parser.add_argument('--depth', type=int, default=8)
    parser.add_argument('--target-length', type=int, default=31)
    parser.add_argument('--memory-mib', type=int, default=1024)
    args = parser.parse_args(argv)
    if not math.isfinite(args.wall_seconds) or not 0 < args.wall_seconds <= 180:
        parser.error('wall-seconds must be finite, positive and at most 180')
    if args.node_cap < 2 or not 1 <= args.depth <= 20 or args.target_length < 0:
        parser.error('positive depth <=20, node-cap>=2, target-length>=0 required')
    if not 64 <= args.memory_mib <= 1024:
        parser.error('memory-mib must be between 64 and 1024')
    out = Path(args.output_dir).resolve()
    if not out.is_relative_to(ROOT):
        parser.error('output-dir must be within the workspace')
    out.mkdir(parents=True, exist_ok=True)
    # Hard limit applies to the whole process, not just estimated search storage.
    cap = args.memory_mib * 1024 * 1024
    old_soft, old_hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (min(cap, old_hard) if old_hard != -1 else cap, old_hard))
    phase_start = time.monotonic()
    core, specs, doc, challenges = official_checker.load_kernel()
    challenge = challenges[args.row]
    start = tuple(tuple(w) for w in challenge['initial_relators'])
    target = tuple(tuple(w) for w in challenge['target_relators'])
    rule = specs.get(challenge['move_spec_version']).move_spec_hash.removeprefix('sha256:')
    routes_path = (ROOT / args.routes).resolve()
    routes = [r for r in json.loads(routes_path.read_text())['routes'] if r['row_id'] == args.row]
    graph, traces, prefix, suffix = saved_union(core, start, target, routes)
    baseline = prefix.get(target)
    best_saved = min((len(r['moves']) for r in routes), default=None)
    states = sorted(graph)
    ids = {s: i for i, s in enumerate(states)}
    union_artifact = {'row_id': args.row, 'representation': 'ordered-freely-reduced-words',
        'generator_map': {'1':'x', '-1':'X', '2':'y', '-2':'Y'},
        'direction': 'start-to-exact-target; explicit inverse edges included',
        'cost_convention': 'one frozen official atomic move per edge',
        'start': state_json(start), 'target': state_json(target),
        'routes': [{'moves': r['moves'], 'sources': r.get('sources', []),
                    'state_ids': [ids[s] for s in trace]} for r, trace in zip(routes, traces)],
        'states': [state_json(s) for s in states],
        'edges': sorted([[ids[s], move, ids[t]] for s in states for t, move in graph[s]]),
        'union_shortest_moves': baseline, 'union_shortest_length': len(baseline) if baseline is not None else None,
        'best_saved_length': best_saved}
    dump(out/'saved_union.json', union_artifact)
    if baseline is not None:
        base = candidate_for(args.row, start, baseline, rule)
        receipt = official_checker.check(base)
        if not receipt['valid']:
            raise ValueError('union composition failed official replay')
        dump(out/'baseline.json', base)
        dump(out/'baseline_receipt.json', receipt)
    union_seconds = time.monotonic()-phase_start
    best, coverage = bounded_bridge(core, prefix, suffix, baseline,
        wall_seconds=args.wall_seconds, node_cap=args.node_cap, depth=args.depth,
        target_length=args.target_length, max_total_length=doc['limits']['max_total_relator_length'],
        memory_mib=args.memory_mib)
    coverage.update({'row_id': args.row, 'profile': args.profile,
        'best_saved_length': best_saved, 'union_shortest_length': len(baseline) if baseline is not None else None,
        'union_states': len(graph), 'union_directed_edges': sum(map(len, graph.values())),
        'saved_route_lengths': [len(r['moves']) for r in routes],
        'phase_seconds': {'saved_union_and_replay': union_seconds, 'fresh_search': coverage['elapsed_seconds']},
        'limits': {'wall_seconds': args.wall_seconds, 'node_cap': args.node_cap,
                   'memory_mib': args.memory_mib, 'total_bridge_depth': args.depth},
        'command': [sys.executable, 'bridge_search.py'] + (sys.argv[1:] if argv is None else list(argv)),
        'python_version': sys.version, 'ruleset_sha256': rule,
        'route_source_sha256': official_checker.sha(routes_path),
        'method_sha256': official_checker.sha(__file__),
        'checker_sha256': official_checker.sha(ROOT/'official_checker.py'),
        'live_score_claim': False})
    improvement = best is not None and (best_saved is None or len(best) < best_saved)
    artifact_paths = [out/'saved_union.json', out/'coverage.json', Path(__file__), ROOT/'tests/test_bridge_search.py']
    if baseline is not None:
        artifact_paths += [out/'baseline.json', out/'baseline_receipt.json']
    if improvement:
        candidate = candidate_for(args.row, start, best, rule)
        receipt = official_checker.check(candidate)
        if not receipt['valid']:
            raise ValueError('fresh bridge candidate failed official replay')
        dump(out/'candidate.json', candidate)
        dump(out/'receipt.json', receipt)
        artifact_paths += [out/'candidate.json', out/'receipt.json']
        result = {'kind':'candidate', 'summary': f'Officially replayed local route length {len(best)}, saved baseline {best_saved}; target {args.target_length}. No live score or submission.', 'candidate':candidate}
    else:
        result = {'kind':'bounded_miss', 'summary': f'No saved-baseline improvement found; best {coverage["best_length"]}, target {args.target_length}; bounded run ended {coverage["termination_reason"]}. No impossibility or live score claim.',
            'limits':coverage['limits'], 'actual_coverage': {k:coverage[k] for k in ['admitted_records','generated_moves','expanded_by_side_depth','collision_pairs','unique_states_by_side','partial_layer']},
            'termination_reason':coverage['termination_reason'],
            'reopen_when': {'event':'bridge_budget_increased','row_id':args.row,'total_bridge_depth':args.depth+1,'node_cap':args.node_cap+1}}
    official_checker.load_kernel()
    dump(out/'coverage.json', coverage)
    result['evidence'] = [{'path':str(p.relative_to(ROOT)), 'sha256':official_checker.sha(p)} for p in artifact_paths]
    dump(out/'worker_result.json', result)
    print(json.dumps({'result_path':str((out/'worker_result.json').relative_to(ROOT)),
                      'kind':result['kind'], 'best_length':coverage['best_length'],
                      'termination_reason':coverage['termination_reason']}))


if __name__ == '__main__':
    main()
