#!/usr/bin/env python3
"""Independent exact radius-3 balls on one frozen paid route; no solver import."""
import argparse
from collections import deque, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import official_checker

def dump(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--row', required=True)
    p.add_argument('--output-dir', required=True)
    p.add_argument('--wall-seconds', type=float, required=True)
    p.add_argument('--node-cap', type=int, required=True)
    p.add_argument('--memory-mib', type=int, required=True)
    p.add_argument('--target-length', type=int, required=True)
    a = p.parse_args()
    if not (0 < a.wall_seconds <= 180 and 0 < a.node_cap <= 600000 and 64 <= a.memory_mib <= 1024):
        p.error('unchanged harness bounds required')
    out = Path(a.output_dir).resolve()
    out.relative_to(ROOT / 'runs/route_ball6_revival')
    out.mkdir(parents=True, exist_ok=True)
    if any(out.iterdir()):
        p.error('fresh output directory required')
    hard = resource.getrlimit(resource.RLIMIT_AS)[1]
    resource.setrlimit(resource.RLIMIT_AS, (min(a.memory_mib*1048576, hard) if hard >= 0 else a.memory_mib*1048576, hard))
    started = time.monotonic()
    deadline = started + a.wall_seconds
    inp = ROOT / 'helpers/route_ball6_input.json'
    frozen = json.loads(inp.read_text())
    if a.row != frozen['row_id']:
        raise ValueError('row differs from frozen experiment')
    core, specs, doc, challenges = official_checker.load_kernel()
    ch = challenges[a.row]
    moves = frozen['moves']
    initial = tuple(tuple(w) for w in ch['initial_relators'])
    original = core.verify(ch, moves, ch['move_spec_version'], doc['limits'])
    if not original['ok']:
        raise ValueError('frozen route failed pinned official checker')
    states = [initial]
    for m in moves:
        states.append(core.apply_move(states[-1], m))
    for name, content in [('captured_input.json', frozen), ('input_receipt.json', original)]:
        dump(out / name, content)
    (out / 'executed_route_ball6_v1.py').write_bytes(Path(__file__).read_bytes())
    balls = []
    index = defaultdict(list)
    edges = {(i, i+1): [m] for i, m in enumerate(moves)}
    coverage = {'admitted_labels': 0, 'pair_comparisons': 0, 'generated_moves': 0,
                'completed_balls': 0, 'shortcut_edges': 0, 'radius': 3,
                'input_length': len(moves), 'source_sha256': official_checker.sha(inp)}
    limits = {'wall_seconds': a.wall_seconds, 'node_cap': a.node_cap, 'memory_mib': a.memory_mib,
              'radius': 3, 'max_replacement_length': 6, 'fixed_route_states': len(states)}
    last_control = 0
    reason = 'complete'
    def guard():
        nonlocal last_control
        now = time.monotonic()
        if now >= deadline:
            raise StopIteration('wall_seconds')
        if coverage['admitted_labels'] + coverage['pair_comparisons'] >= a.node_cap:
            raise StopIteration('record_cap')
        if now-last_control >= .1:
            last_control = now
            if json.loads((ROOT/'continuation/checkpoint.json').read_text()).get('stopped') is not False:
                raise StopIteration('controller_stop')
    try:
        for i, seed in enumerate(states):
            guard()
            ball = {seed: ()}
            balls.append(ball)
            coverage['admitted_labels'] += 1
            q = deque([seed])
            while q:
                guard()
                s = q.popleft()
                path = ball[s]
                if len(path) == 3:
                    continue
                for m in range(core.NUM_MOVES):
                    guard()
                    t = core.apply_move(s, m)
                    coverage['generated_moves'] += 1
                    if sum(map(len, t)) > doc['limits']['max_total_relator_length'] or t in ball:
                        continue
                    ball[t] = path + (m,)
                    coverage['admitted_labels'] += 1
                    q.append(t)
            coverage['completed_balls'] += 1
            # Every indexed earlier ball is complete. Exact ordered states only.
            for state, forward in ball.items():
                for j, left in index[state]:
                    guard()
                    coverage['pair_comparisons'] += 1
                    replacement = list(left) + [core.INVERSE_MOVE[m] for m in reversed(forward)]
                    if len(replacement) < i-j and len(replacement) < len(edges.get((j,i), moves)):
                        edges[j,i] = replacement
                index[state].append((i, forward))
    except StopIteration as exc:
        reason = str(exc)
    # Shortest composition of disjoint paid replacements on the frozen route.
    dist = [0] + [10**9] * len(moves)
    parent = {}
    outgoing = defaultdict(list)
    for (i,j), path in edges.items():
        outgoing[i].append((j,path))
    for i in range(len(moves)):
        for j, path in outgoing[i]:
            if dist[i]+len(path) < dist[j]:
                dist[j] = dist[i]+len(path)
                parent[j] = (i,path)
    chunks = []
    j = len(moves)
    while j:
        i, path = parent[j]
        chunks.append(path)
        j = i
    best = [m for part in reversed(chunks) for m in part]
    verdict = core.verify(ch, best, ch['move_spec_version'], doc['limits'])
    if not verdict['ok']:
        raise ValueError('composed shortcut failed independent pinned checker')
    coverage.update(termination_reason=reason, best_length=len(best),
                    shortcut_edges=sum(j > i+1 for i,j in edges),
                    elapsed_seconds=time.monotonic()-started,
                    peak_rss_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
    archive = [[[list(map(list,s)), list(path)] for s,path in b.items()] for b in balls]
    (out/'balls.json.gz').write_bytes(gzip.compress(json.dumps(archive,separators=(',',':')).encode(), mtime=0))
    dump(out/'coverage.json', coverage)
    dump(out/'shortcuts.json', [{'from_index':i,'to_index':j,'moves':v} for (i,j),v in sorted(edges.items()) if j>i+1])
    dump(out/'output_receipt.json', verdict)
    result = {'kind': 'bounded_miss' if reason == 'complete' else 'blocked',
              'summary': f'Fixed radius-3 pair shortcut audit: {len(moves)} -> {len(best)} moves; {reason}. No global lower bound.',
              'limits': limits, 'actual_coverage': coverage, 'termination_reason': reason,
              'reopen_when': {'event':'different_exact_input_route_or_distinct_justified_method','row_id':a.row}}
    if len(best) < len(moves):
        candidate = {'row_id':a.row,'track':'AC','start':official_checker.render(initial),'moves':best,
                     'ruleset_sha256':specs.get(ch['move_spec_version']).move_spec_hash.removeprefix('sha256:'),
                     'evidence_grade':'V','family':'fixed-route-radius3-pair-shortcut'}
        receipt = official_checker.check(candidate)
        if not receipt['valid']:
            raise ValueError('independent adapter rejected shortcut')
        dump(out/'candidate.json',candidate)
        dump(out/'receipt.json',receipt)
        result.update(kind='candidate',candidate=candidate)
    evidence = sorted(x for x in out.iterdir() if x.is_file())
    result['evidence'] = [{'path':str(x.relative_to(ROOT)),'sha256':official_checker.sha(x)} for x in evidence]
    dump(out/'worker_result.json',result)
    print(json.dumps({'kind':result['kind'],'coverage':coverage}))

if __name__ == '__main__':
    main()
