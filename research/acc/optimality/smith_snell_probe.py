#!/usr/bin/env python3
"""Exploratory Smith-coordinate and Snell-style routing tests on AC paths.

These are empirical search features, not group invariants or a physical law.
The Smith map projects the two relator lengths to a bounded disk. Rigidity is
the fraction of legal one-step moves that fail to lower total relator length.
The Snell-style test asks whether R*sin(theta)^2 predicts the next chart step
better than angle persistence with R fixed, with the true next move withheld.
"""
import argparse
import cmath
import json
import math
import statistics
import sys
from collections import Counter
from pathlib import Path


def reflect(state, z0):
    z = complex(len(state[0]), len(state[1]))
    return (z - z0) / (z + z0)


def band(gamma):
    return min(3, int(abs(gamma) * 4)), min(7, int(((cmath.phase(gamma) + math.pi) / (2 * math.pi)) * 8))


def sin2_radial(a, b):
    delta = b - a
    if abs(delta) < 1e-12 or abs(a) < 1e-12:
        return None
    tangent = complex(-a.imag, a.real) / abs(a)
    return max(0.0, min(1.0, (delta.real * tangent.real + delta.imag * tangent.imag) ** 2 / (abs(delta) ** 2)))


def rigidity(core, state):
    length = sum(map(len, state))
    return 1.0 + sum(sum(map(len, core.apply_move(state, m))) >= length for m in range(14)) / 14.0


def load_routes(args):
    rows = json.loads(Path(args.paths).read_text())
    for filename in args.extra:
        for line in Path(filename).read_text().splitlines():
            rec = json.loads(line)
            if rec.get('ac'):
                rows.append({'id': rec['id'], 'ac': rec['ac'], 'len': len(rec['ac']), 'src': 'new_beam'})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--paths', required=True)
    ap.add_argument('--extra', nargs='*', default=[])
    ap.add_argument('--verifier-root', required=True)
    ap.add_argument('--max-routes', type=int, default=80)
    args = ap.parse_args()
    sys.path.insert(0, str(Path(args.verifier_root) / 'competition' / 'tools'))
    from verifier import core
    manifest = json.loads(Path(args.manifest).read_text())
    challenges = {c['challenge_id']: c for c in manifest['challenges']}
    rows = load_routes(args)
    # Deterministic spread across all supplied paths, with a few new beam paths.
    old = [r for r in rows if r.get('src') != 'new_beam']
    step = max(1, len(old) // args.max_routes)
    chosen = old[::step][:args.max_routes] + [r for r in rows if r.get('src') == 'new_beam']
    valid = 0
    sectors = Counter()
    crossings = 0
    path_steps = 0
    high_hump_crossings = 0
    junctions = 0
    rank_const = []
    rank_rigid = []
    actual_changes = []
    ambiguous = 0
    route_deltas = []
    for row in chosen:
        challenge = challenges.get(row['id'])
        if challenge is None:
            continue
        moves = row['ac']
        if not core.verify(challenge, moves, 'ac-r2-v1', manifest['limits'])['ok']:
            raise ValueError('invalid route ' + row['id'])
        valid += 1
        state = tuple(tuple(w) for w in challenge['initial_relators'])
        states = [state]
        for move in moves:
            state = core.apply_move(state, move)
            states.append(state)
        start_len = sum(map(len, states[0]))
        z0 = max(1.0, start_len / 2.0)
        chart = [reflect(s, z0) for s in states]
        bs = [band(g) for g in chart]
        route_rank_start = len(rank_const)
        sectors.update(bs)
        for i in range(1, len(states) - 1):
            path_steps += 1
            if bs[i] != bs[i + 1]:
                crossings += 1
                if sum(map(len, states[i])) >= start_len + 5:
                    high_hump_crossings += 1
            incoming = sin2_radial(chart[i - 1], chart[i])
            if incoming is None or bs[i - 1][0] == bs[i][0]:
                continue
            rin = rigidity(core, states[i - 1])
            target = rin * incoming
            rnow = rigidity(core, states[i])
            cand = []
            actual = None
            for m in range(14):
                nxt = core.apply_move(states[i], m)
                gout = reflect(nxt, z0)
                outgoing = sin2_radial(chart[i], gout)
                if outgoing is None:
                    continue
                rnext = rigidity(core, nxt)
                # Constant-R comparator and proposed varying-rigidity Snell channel.
                base = abs(incoming - outgoing)
                snell = abs(target - rnext * outgoing)
                cand.append((m, base, snell))
                if m == moves[i]:
                    actual = (base, snell, abs(rnext - rin))
            if actual is None or len(cand) < 2:
                continue
            if sum(abs(x[2] - actual[1]) < 1e-9 for x in cand) > 1:
                ambiguous += 1
            rank_const.append((sum(x[1] < actual[0] - 1e-9 for x in cand) + .5 * sum(abs(x[1] - actual[0]) < 1e-9 for x in cand)) / len(cand))
            rank_rigid.append((sum(x[2] < actual[1] - 1e-9 for x in cand) + .5 * sum(abs(x[2] - actual[1]) < 1e-9 for x in cand)) / len(cand))
            actual_changes.append(actual[2])
            junctions += 1
        if len(rank_const) > route_rank_start:
            route_deltas.append(sum(rank_rigid[j] - rank_const[j] for j in range(route_rank_start, len(rank_const)))
                                / (len(rank_const) - route_rank_start))
    mean = lambda a: round(sum(a) / len(a), 4) if a else None
    result = {
        'routes_verified': valid,
        'chart': {'sector_count': len(sectors), 'sector_visits': {str(k): v for k, v in sectors.items()},
                  'path_steps': path_steps, 'sector_crossings': crossings,
                  'crossings_at_least_5_above_start': high_hump_crossings},
        'snell': {'eligible_radial_interfaces': junctions,
                  'ambiguous_actual_angle_matches': ambiguous,
                  'mean_rank_fraction_constant_R': mean(rank_const),
                  'mean_rank_fraction_varying_R': mean(rank_rigid),
                  'route_mean_rank_delta_varying_minus_constant': mean(route_deltas),
                  'route_delta_standard_error': round(statistics.stdev(route_deltas) / math.sqrt(len(route_deltas)), 4)
                  if len(route_deltas) > 1 else None,
                  'routes_with_eligible_interfaces': len(route_deltas),
                  'mean_absolute_rigidity_change': mean(actual_changes),
                  'interpretation': '0.5 is tie-aware chance rank; smaller ranks are better. The test does not prove a law.'},
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
