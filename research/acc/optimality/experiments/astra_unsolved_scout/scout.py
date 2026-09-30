"""Read-only unsolved target triage. No beam, networking or submission calls.

Match saved Miller--Schupp hints to official starts, then locate solved adjacent-n
rows and verified source routes. Canonical equivalence here is a catalogue key,
not a constructed AC bridge or a bound on the cost of that bridge.
"""
import argparse
import collections
import datetime as dt
import functools
import gzip
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

PIN = 'a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e'
LETTERS = {'x': 1, 'X': -1, 'y': 2, 'Y': -2}


def read_json(path):
    raw = path.read_bytes()
    return json.loads(gzip.decompress(raw) if path.suffix == '.gz' else raw)


def cyclic_reduce(word):
    out = []
    for x in word:
        if out and out[-1] == -x:
            out.pop()
        else:
            out.append(x)
    while len(out) >= 2 and out[0] == -out[-1]:
        out = out[1:-1]
    return tuple(out)


@functools.lru_cache(maxsize=None)
def cyclic_key(word):
    word = cyclic_reduce(word)
    if not word:
        return ()
    inverse = tuple(-x for x in reversed(word))
    return min(w[i:] + w[:i] for w in (word, inverse) for i in range(len(w)))


def pair_key(pair):
    keys = []
    for swap in (False, True):
        for sx in (-1, 1):
            for sy in (-1, 1):
                mp = {1: sx * (2 if swap else 1), 2: sy * (1 if swap else 2)}
                words = [cyclic_key(tuple(mp[abs(x)] * (1 if x > 0 else -1) for x in w)) for w in pair]
                keys.append(tuple(sorted(words)))
    return min(keys)


def ms_pair(n, word):
    power = (-2,) * (n + 1) + (-1,) + (2,) * n + (1,)
    return (tuple(LETTERS[x] for x in word), power)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=Path.cwd())
    ap.add_argument('--board', type=Path, required=True)
    ap.add_argument('--unsolved', type=Path, required=True)
    ap.add_argument('--roads', type=Path, required=True)
    ap.add_argument('--exclusions', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    actual_pin = subprocess.check_output(['git', '-C', str(args.root / 'SAIR'), 'rev-parse', 'HEAD'], text=True).strip()
    if actual_pin != PIN:
        raise SystemExit(f'Official core pin mismatch: {actual_pin}')
    sys.path.insert(0, str(args.root / 'SAIR/competition/tools'))
    from verifier import core
    manifest_path = args.root / 'SAIR/competition/tools/verifier/data/manifest.json'
    manifest = read_json(manifest_path)
    challenge = {c['challenge_id']: c for c in manifest['challenges']}
    board = read_json(args.board)
    items = {r['challengeId']: r for r in board['data']['items']}
    unsolved = read_json(args.unsolved)
    blocked = set(read_json(args.exclusions)['rows'])
    input_roads = read_json(args.roads)['rows']
    verified = {}
    failed_roads = []
    for row in input_roads:
        cid = row['id']
        if row['start'] != challenge[cid]['initial_relators']:
            failed_roads.append({'id': cid, 'reason': 'start mismatch'})
            continue
        check = core.verify(challenge[cid], row['moves'], 'ac-r2-v1', manifest['limits'])
        if not check['ok']:
            failed_roads.append({'id': cid, 'reason': check})
        else:
            verified[cid] = {'length': len(row['moves']), 'certificate_hash': check['certificate_hash']}
    index = collections.defaultdict(list)
    for cid in items:
        index[pair_key(challenge[cid]['initial_relators'])].append(cid)
    candidates = []
    excluded = []
    for row in unsolved:
        ids = row['class']
        if set(ids) & blocked or any(items[c]['status'] != 'unsolved' for c in ids):
            excluded.append(row['id'])
            continue
        if row['kind'] != 'Miller-Schupp, solved neighbour':
            continue
        match = re.search(r'MS\((\d+),([^|]+)\|[01]\)', row['hint'])
        if not match:
            raise ValueError(row['hint'])
        n, word = int(match[1]), match[2]
        own_key = pair_key(challenge[row['id']]['initial_relators'])
        hint_matches_start = own_key == pair_key(ms_pair(n, word))
        sources = []
        if hint_matches_start:
            for nn in (n - 1, n + 1):
                if nn < 1:
                    continue
                for cid in index.get(pair_key(ms_pair(nn, word)), []):
                    if items[cid]['status'] == 'solved':
                        sources.append({'id': cid, 'n': nn, 'record': items[cid]['currentBestLength'],
                                        'held_route': verified.get(cid)})
        candidates.append({**row, 'n': n, 'w': word, 'hint_matches_start': hint_matches_start,
                           'solved_adjacent_sources': sources,
                           'has_verified_adjacent_source': any(s['held_route'] for s in sources),
                           'ownership': 'coordinate with session1 firstsolve; YYXXYx also with Git; Bob owns generator-change transfer',
                           'status': 'scouted only; no new search or AC bridge constructed'})
    candidates.sort(key=lambda r:(not r['has_verified_adjacent_source'], -r['class_size'],
                                   min([s['held_route']['length'] for s in r['solved_adjacent_sources'] if s['held_route']] or [10**9]),
                                   r['start_len'], r['id']))
    summary = {
        'saved_board_pulled_at': board['pulledAt'], 'saved_board_generated_at': board['data']['generatedAt'],
        'board_unsolved_rows': sum(x['status'] == 'unsolved' for x in items.values()),
        'catalog_classes': len(unsolved), 'catalog_rows': sum(r['class_size'] for r in unsolved),
        'catalog_kind_counts': dict(collections.Counter(r['kind'] for r in unsolved)),
        'catalog_rows_still_unsolved': sum(items[c]['status'] == 'unsolved' for r in unsolved for c in r['class']),
        'blocked_or_now_solved_classes': excluded,
        'source_routes_checked': len(input_roads), 'source_routes_valid': len(verified),
        'source_routes_failed': failed_roads, 'ms_classes': len(candidates),
        'ms_hint_matches': sum(r['hint_matches_start'] for r in candidates),
        'ms_with_solved_adjacent': sum(bool(r['solved_adjacent_sources']) for r in candidates),
        'ms_with_held_adjacent': sum(r['has_verified_adjacent_source'] for r in candidates),
        'ms_with_held_adjacent_rows': sum(r['class_size'] for r in candidates if r['has_verified_adjacent_source']),
        'new_solutions': 0, 'new_bridges': 0, 'searches_started': 0,
    }
    result = {'created_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'sair_pin': PIN,
              'scope': 'saved-board catalogue audit and verified-source availability; no current SAIR reads',
              'input_sha256': {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in (args.board, args.unsolved, args.roads, args.exclusions, manifest_path)},
              'summary': summary, 'ranked_candidates': candidates}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(summary, indent=2), flush=True)
    for row in candidates[:12]:
        print(json.dumps({k:row[k] for k in ('id','class_size','hint','solved_adjacent_sources','has_verified_adjacent_source')}), flush=True)


if __name__ == '__main__':
    main()
