"""Replay a sibling (n=4) route on the n=3 start and print the state trace side by side.
usage: replay.py ROW_N3 ROW_N4 '[moves]'"""
import json, sys
SAIR = '/root/.cache/upgh/sair'
sys.path.insert(0, SAIR + '/competition/tools'); from verifier import core
man = json.load(open(SAIR + '/competition/tools/verifier/data/manifest.json')); CH = {c['challenge_id']: c for c in man['challenges']}
L = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}
def w(t): return ''.join(L[a] for a in t) or '1'
r3, r4, route = sys.argv[1], sys.argv[2], json.loads(sys.argv[3])
s3 = tuple(tuple(r) for r in CH[r3]['initial_relators']); s4 = tuple(tuple(r) for r in CH[r4]['initial_relators'])
print(f"{r3} start {w(s3[0])} | {w(s3[1])}\n{r4} start {w(s4[0])} | {w(s4[1])}")
print(f"{'i':>3} {'m':>2}  {'n=4 state':<34} {'n=3 state':<34} tot4 tot3")
for i, m in enumerate([None] + route):
    if m is not None: s3 = core.apply_move(s3, m); s4 = core.apply_move(s4, m)
    print(f"{i:>3} {'' if m is None else m:>2}  {w(s4[0]) + ' | ' + w(s4[1]):<34} {w(s3[0]) + ' | ' + w(s3[1]):<34} {len(s4[0])+len(s4[1]):>4} {len(s3[0])+len(s3[1]):>4}")
print("n=4 final", s4, "n=3 final", s3)
