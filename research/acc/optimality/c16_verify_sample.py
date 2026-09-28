"""Replay the C16 sample descents (acc_c16 sample output) with the official SAIR verifier.

Each input line is "d l0 w.. l1 w.. | m1 .. md" (letters 0=x 1=x^-1 2=y 3=y^-1). For every line the state is
converted to official ints (1,-1,2,-2), the moves are replayed with verifier.core.verify (target (x,y), spec
ac-r2-v1, generous limits) and the result must be ok with length exactly d; the peak total relator length along
the path must also stay <= CEIL (the descent lives inside the ceiling graph).
usage: c16_verify_sample.py VERIFIER_TOOLS_DIR SAMPLE_FILE CEIL [OUT_JSON]"""
import json, sys
sys.path.insert(0, sys.argv[1])
from verifier import core  # official kernel

E = {0: 1, 1: -1, 2: 2, 3: -2}
CEIL = int(sys.argv[3])
LIM = {'max_path_length': 10 ** 6, 'max_total_relator_length': 10 ** 6, 'max_work': 10 ** 12}
n = ok = bad_len = bad_peak = 0; fails = []; by_d = {}
for line in open(sys.argv[2]):
    head, _, tail = line.partition('|')
    a = list(map(int, head.split())); mv = list(map(int, tail.split()))
    d = a[0]; l0 = a[1]; r0 = [E[t] for t in a[2:2 + l0]]; l1 = a[2 + l0]; r1 = [E[t] for t in a[3 + l0:3 + l0 + l1]]
    assert len(a) == 3 + l0 + l1 and len(mv) == d
    ch = {'challenge_id': 'c16-sample', 'move_spec_version': core.MOVE_SPEC_VERSION,
          'initial_relators': [r0, r1], 'target_relators': [[1], [2]]}
    v = core.verify(ch, mv, core.MOVE_SPEC_VERSION, LIM)
    # independent step-by-step replay with apply_move, for the peak inside the ceiling
    st = (tuple(r0), tuple(r1)); peak = len(r0) + len(r1)
    for m in mv:
        st = core.apply_move(st, m); peak = max(peak, len(st[0]) + len(st[1]))
    n += 1; by_d[d] = by_d.get(d, 0) + 1
    good = v.get('ok') and v['length'] == d and st == ((1,), (2,))
    if good: ok += 1
    else:
        bad_len += 1; fails.append({'d': d, 'r0': r0, 'r1': r1, 'moves': mv, 'verifier': v})
    if peak > CEIL: bad_peak += 1
res = {'sample': n, 'verified_exact_length': ok, 'failed': bad_len, 'peak_above_ceiling': bad_peak,
       'max_d': max(by_d), 'by_distance': {str(k): by_d[k] for k in sorted(by_d)}, 'fails': fails[:10]}
print(json.dumps({k: v for k, v in res.items() if k != 'fails'}))
if len(sys.argv) > 4: json.dump(res, open(sys.argv[4], 'w'), indent=1)
sys.exit(0 if ok == n and not bad_peak else 1)
