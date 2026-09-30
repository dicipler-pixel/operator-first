#!/usr/bin/env python3
"""t00138 step 2/3: repeated blocks and exponent runs in our AC routes.
Lists (a) maximal runs of one conjugation move id (x^m / y^m applied to a
relator one letter at a time), (b) repeated move blocks of length >= 4,
(c) for each run, whether the all-pairs exact helper search covered a
window containing it (window length <= 9 at DF=DB=3, <= 11 at 4+4)."""
import json, sys, os
sys.path.insert(0, os.path.expanduser('~/.cache/upgh/sair/competition/tools'))
from verifier import stable_core
ct = json.load(open('/home/user/operator-first/research/acc/upgh/tasks/t00138.json'))
man = json.load(open(os.path.expanduser('~/.cache/upgh/sair/competition/tools/verifier/data/manifest.json')))
idx = {c['challenge_id']: c for c in man['challenges']}
for row in ct['rows']:
    P = ct['context'][row]['our_best_moves']
    n = len(P)
    while P[n - 1] >= 14:
        n -= 1
    AC = P[:n]
    print(f'== {row}: AC len {n}, tail {P[n:]}')
    # (a) runs of a single conjugation id
    runs = []
    i = 0
    while i < n:
        j = i
        while j < n and AC[j] == AC[i]:
            j += 1
        if j - i >= 2 and 6 <= AC[i] <= 13:
            runs.append((i, j, AC[i]))
        i = j
    print('  conjugation runs (start,end,move,len):', [(a, b, m, b - a) for a, b, m in runs])
    print('  longest run:', max((b - a for a, b, m in runs), default=0),
          '-> fully inside a window of length <= 9 (covered exactly at 3+3)' if max((b - a for a, b, m in runs), default=0) <= 9 else '-> longer than 9: only partially covered')
    # (b) repeated blocks of length >= 4
    seen = {}
    for L in range(4, 9):
        for s in range(n - L + 1):
            blk = tuple(AC[s:s + L])
            seen.setdefault(blk, []).append(s)
    rep = {b: p for b, p in seen.items() if len(p) >= 2 and len(b) >= 4}
    # keep only maximal-length repeats
    maxrep = sorted(rep.items(), key=lambda kv: -len(kv[0]))[:6]
    print('  repeated blocks (block, positions):', [(list(b), p) for b, p in maxrep])
    # (c) which subwords are rebuilt: relator words along the path, look for a subword of length >= 4 built twice
    st = tuple(tuple(w) for w in idx[row]['initial_relators'])
    words = set()
    rebuilt = {}
    for k, m in enumerate(AC):
        st, _ = stable_core.apply_move(st, m)
        for w in st:
            for L in (6, 8):
                for a in range(len(w) - L + 1):
                    sub = w[a:a + L]
                    rebuilt.setdefault(sub, set()).add(k)
    # a subword that appears at two well-separated times (gap >= 10 moves) with an absence in between
    cand = []
    for sub, ks in rebuilt.items():
        ks = sorted(ks)
        gaps = [(ks[t], ks[t + 1]) for t in range(len(ks) - 1) if ks[t + 1] - ks[t] >= 10]
        if gaps and len(sub) == 8:
            cand.append((sub, gaps[:2]))
    print('  length-8 subwords absent for >= 10 moves then rebuilt:', len(cand), cand[:4])
