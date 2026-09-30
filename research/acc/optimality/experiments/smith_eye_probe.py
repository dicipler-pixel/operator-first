"""Offline Smith-chart eye on saved AC paths, with 14-sibling ranks.

Usage: python smith_eye_probe.py MANIFEST MIRROR_JSONL [ID:PATH_JSON ...]
For det(M)<0, reflect M.i into the upper half-plane before Cayley mapping;
this deliberately treats orientation reversal as an equally valid eye.
"""
import json
import math
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).parents[2]))
from verifier import core

rows = {r['challenge_id']: r for r in json.load(open(sys.argv[1]))['challenges']}
paths = []
for line in open(sys.argv[2]):
    x = json.loads(line)
    if x.get('ac') and x.get('ok'):
        paths.append((x['id'], x['ac']))
for spec in sys.argv[3:]:
    row_id, pathfile = spec.split(':', 1)
    paths.append((row_id, json.load(open(pathfile))))

def score(st):
    a, b = sum(x == 1 for x in st[0])-sum(x == -1 for x in st[0]), sum(x == 2 for x in st[0])-sum(x == -2 for x in st[0])
    c, d = sum(x == 1 for x in st[1])-sum(x == -1 for x in st[1]), sum(x == 2 for x in st[1])-sum(x == -2 for x in st[1])
    det = a*d-b*c
    assert abs(det) == 1
    z = c*c+d*d
    re = (a*c+b*d)/z
    im = 1/z  # reflected when det<0
    return math.sqrt((re*re+(im-1)**2)/(re*re+(im+1)**2))

records = []
for row_id, path in paths:
    st = tuple(map(tuple, rows[row_id]['initial_relators']))
    for k, move in enumerate(path):
        child = [core.apply_move(st, m) for m in range(14)]
        vals = [score(s) for s in child]
        lens = [sum(map(len, s)) for s in child]
        # Midranks handle ties; top 3 is the same convention as SCORE_ZOO.
        rank_s = sum(v < vals[move]-1e-12 for v in vals) + .5*(1+sum(abs(v-vals[move])<1e-12 for v in vals))
        rank_l = sum(v < lens[move] for v in lens) + .5*(1+sum(v == lens[move] for v in lens))
        climbing = lens[move] > sum(map(len, st))
        records.append({'row': row_id, 'step': k, 'move': move, 'climb': climbing,
                        'smith_midrank': rank_s, 'length_midrank': rank_l,
                        'smith_top3': rank_s <= 3, 'length_top3': rank_l <= 3})
        st = child[move]
    assert st == ((1,), (2,)), row_id
for name, x in [('all', records), ('climb', [r for r in records if r['climb']]),
                ('conjugation_climb', [r for r in records if r['climb'] and r['move'] >= 6])]:
    print(name, 'n', len(x), 'smith_top3', round(sum(r['smith_top3'] for r in x)/len(x), 3) if x else None,
          'length_top3', round(sum(r['length_top3'] for r in x)/len(x), 3) if x else None)
json.dump({'paths': len(paths), 'steps': len(records), 'records': records},
          open(os.environ.get('SMITH_OUT', 'smith_eye_probe.json'), 'w'))
