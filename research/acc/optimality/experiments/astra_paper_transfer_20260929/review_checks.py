"""Reproduce offline paper-transfer checks; no search lane, network, or submission.

Run from repository root. Prints JSON; --output writes a new result file.
This is a finite implementation audit, not a Lean proof or search-speed benchmark.
"""
from collections import deque
from functools import lru_cache
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
PIN = 'a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e'
assert subprocess.check_output(['git', '-C', str(ROOT/'SAIR'), 'rev-parse', 'HEAD'], text=True).strip() == PIN
assert not subprocess.check_output(['git', '-C', str(ROOT/'SAIR'), 'status', '--porcelain', '--untracked-files=no'], text=True).strip()
sys.path.insert(0, str(ROOT/'SAIR/competition/tools'))
from verifier import core

GOAL = ((1,), (2,))
HURWITZ = (2, 5, 2, 1)
UNHURWITZ = (1, 3, 4, 3)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay(state, moves):
    for move in moves:
        state = core.apply_move(state, move)
    return state


def ledger(state):
    return tuple(sum((a == g) - (a == -g) for a in w) for w in state for g in (1, 2))


class Affine:
    def __init__(self, prime):
        self.p = prime
        self.one = (1, 0, 0)
        self.gens = {1: (2, 1, 0), 2: (3, 0, 1)}
        self.gens.update({-g: self.inv(self.gens[g]) for g in (1, 2)})

    def mul(self, x, y):
        t, a, b = x
        u, c, d = y
        p = self.p
        return (t*u % p, (a+t*c) % p, (b+t*d) % p)

    def inv(self, x):
        t, a, b = x
        v = pow(t, -1, self.p)
        return (v, -v*a % self.p, -v*b % self.p)

    @lru_cache(maxsize=None)
    def word(self, w):
        out = self.one
        for a in w:
            out = self.mul(out, self.gens[a])
        return out

    def project(self, state):
        return tuple(self.word(w) for w in state)

    def move(self, state, m):
        a, b = state
        if m == 0:
            return (self.inv(a), b)
        if m == 1:
            return (a, self.inv(b))
        if m == 2:
            return (self.mul(a, b), b)
        if m == 3:
            return (self.mul(a, self.inv(b)), b)
        if m == 4:
            return (a, self.mul(b, a))
        if m == 5:
            return (a, self.mul(b, self.inv(a)))
        slot = 0 if m < 10 else 1
        g = self.gens[core.GENS[m - (6 if slot == 0 else 10)]]
        out = list(state)
        out[slot] = self.mul(self.mul(g, out[slot]), self.inv(g))
        return tuple(out)

    def distances(self):
        goal = self.project(GOAL)
        dist = {goal: 0}
        queue = deque([goal])
        while queue:
            s = queue.popleft()
            for m in range(14):
                child = self.move(s, m)
                if child not in dist:
                    dist[child] = dist[s] + 1
                    queue.append(child)
        # Independent distance-label certificate checks on EVERY quotient edge.
        for s, h in dist.items():
            children = [self.move(s, m) for m in range(14)]
            assert all(c in dist and abs(dist[c]-h) <= 1 for c in children)
            assert h == 0 if s == goal else any(dist[c] == h-1 for c in children)
            for m, child in enumerate(children):
                assert self.move(child, core.INVERSE_MOVE[m]) == s
        return dist


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    old = ROOT/'research/acc/optimality/experiments/astra_snell_smith_chain'
    manifest_path = ROOT/'SAIR/competition/tools/verifier/data/manifest.json'
    manifest = json.loads(manifest_path.read_text())
    challenges = {c['challenge_id']: c for c in manifest['challenges']}
    inputs = [old/'routes.json', old/'heldout_routes.json']
    routes = sum((json.loads(p.read_text()) for p in inputs), [])
    states = set()
    trajectories = []
    route_checks = []
    for r in routes:
        check = core.verify(challenges[r['id']], r['ac'], core.MOVE_SPEC_VERSION, manifest['limits'])
        assert check['ok'], (r['id'], check)
        route_checks.append({'id': r['id'], **check})
        s = tuple(map(tuple, challenges[r['id']]['initial_relators']))
        trajectory = [s]
        for m in r['ac']:
            states.add(s)
            s = core.apply_move(s, m)
            trajectory.append(s)
        assert s == GOAL
        trajectories.append(trajectory)
    identity_nonterminal = sorted(s for s in states if s != GOAL and ledger(s) == (1, 0, 0, 1))
    for s in states:
        u, v = s
        h = replay(s, HURWITZ)
        assert h == (core.free_reduce(u+v+core.invert(u)), u)
        assert core.free_reduce(h[0]+h[1]) == core.free_reduce(u+v)
        assert replay(h, UNHURWITZ) == s
        assert replay(replay(s, UNHURWITZ), HURWITZ) == s
    tables = []
    result = {'scope': 'finite offline AC-only diagnostic; not a production A/B or a Lean proof',
              'sair_commit': PIN, 'move_spec': core.MOVE_SPEC_VERSION,
              'routes': len(routes), 'nonterminal_visits': sum(len(t)-1 for t in trajectories),
              'distinct_nonterminal_states': len(states),
              'identity_ledger_nonterminal_states': identity_nonterminal,
              'hurwitz': {'forward': HURWITZ, 'inverse': UNHURWITZ, 'official_cost': 4,
                          'states_checked': len(states), 'product_preserved': True},
              'quotients': [], 'route_verification': route_checks}
    for p in (5, 7, 11):
        q = Affine(p)
        dist = q.distances()
        for s in states:
            for m in range(14):
                assert q.project(core.apply_move(s, m)) == q.move(q.project(s), m)
        blind = [dist[q.project(s)] for s in identity_nonterminal]
        assert all(h > 0 for h in blind)
        labels = sorted((s, h) for s, h in dist.items())
        result['quotients'].append({'p': p, 'component_states': len(dist),
          'goal_eccentricity_not_diameter': max(dist.values()),
          'official_word_move_checks': 14*len(states),
          'quotient_edges_certificate_checked': 14*len(dist),
          'identity_ledger_example_bounds': blind,
          'labels_sha256': hashlib.sha256(json.dumps(labels, separators=(',', ':')).encode()).hexdigest()})
        tables.append((q, dist))
    wide_path = ROOT/'research/acc/live/targets_astra_wide_20260929T0720Z.json'
    result['wide_start_bounds'] = []
    for r in json.loads(wide_path.read_text()):
        s = tuple(map(tuple, challenges[r['id']]['initial_relators']))
        hs = [d[q.project(s)] for q, d in tables]
        result['wide_start_bounds'].append({'id': r['id'], 'bounds_p5_p7_p11': hs, 'maximum': max(hs)})
    # Cheap goal-landmark endpoint lower bound. Descriptive sample only: these
    # windows overlap, routes are not random, and this is NOT a speed benchmark.
    bins = {k: {'windows': 0, 'shortening_ruled_out': 0} for k in range(2, 15)}
    for trajectory in trajectories:
        hs = [[d[q.project(s)] for q, d in tables] for s in trajectory]
        for span, counts in bins.items():
            for i in range(len(trajectory)-span):
                lb = max(abs(a-b) for a, b in zip(hs[i], hs[i+span]))
                assert lb <= span
                counts['windows'] += 1
                counts['shortening_ruled_out'] += lb > span-1
    result['goal_landmark_window_diagnostic'] = bins
    result['source_sha256'] = {str(p.relative_to(ROOT)): digest(p) for p in
                              [Path(__file__), *inputs, manifest_path, wide_path,
                               ROOT/'SAIR/competition/tools/verifier/core.py']}
    text = json.dumps(result, indent=2) + '\n'
    if args.output:
        with args.output.open('x') as f:
            f.write(text)
    print(text)


if __name__ == '__main__':
    main()
