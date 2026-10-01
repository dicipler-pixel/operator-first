"""Differential check of the independent C++ move implementation on synthetic states."""
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'official' / 'competition' / 'tools'))
from verifier import core

ENC = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}
DEC = {v: k for k, v in ENC.items()}
def show(w):
    return ''.join(ENC[c] for c in w) or '-'
def parse(w):
    return () if w == '-' else tuple(DEC[c] for c in w)

rng = random.Random(61012026)
states = []
for _ in range(300):
    s = ((1,), (2,))
    for _ in range(rng.randrange(1, 60)):
        nxt = core.apply_move(s, rng.randrange(14))
        if sum(map(len, nxt)) <= 60:
            s = nxt
    states.append(s)
with tempfile.TemporaryDirectory() as d:
    p = Path(d) / 'words.txt'
    count = 0
    for s in states:
        p.write_text(show(s[0]) + ' ' + show(s[1]) + '\n')
        proc = subprocess.run([str(ROOT / 'sol61' / 'sol61_ida'), '--dump-neighbors', str(p)],
                              check=True, text=True, capture_output=True)
        rows = proc.stdout.splitlines()
        assert len(rows) == 14
        for m, line in enumerate(rows):
            mid, a, b = line.split()
            assert int(mid) == m
            actual = (parse(a), parse(b))
            assert actual == core.apply_move(s, m), (s, m, actual)
            assert core.apply_move(actual, core.INVERSE_MOVE[m]) == s
            count += 1
print(json.dumps({'status': 'complete', 'seed': 61012026, 'synthetic_states': len(states),
                  'atomic_move_comparisons': count, 'inverse_checks': count,
                  'mismatches': 0, 'official_rows_searched': 0}))
