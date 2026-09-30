"""Print the state trace of a route on a row's start. usage: trace.py ROW '[moves]'"""
import json, sys
SAIR = '/root/.cache/upgh/sair'
sys.path.insert(0, SAIR + '/competition/tools'); from verifier import core
man = json.load(open(SAIR + '/competition/tools/verifier/data/manifest.json')); CH = {c['challenge_id']: c for c in man['challenges']}
L = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}
def w(t): return ''.join(L[a] for a in t) or '1'
row, route = sys.argv[1], json.loads(sys.argv[2])
s = tuple(tuple(r) for r in CH[row]['initial_relators'])
print(f"  0     {w(s[0])} | {w(s[1])}")
for i, m in enumerate(route):
    s = core.apply_move(s, m); print(f"{i+1:>3} {m:>2}  {w(s[0])} | {w(s[1])}   tot={len(s[0])+len(s[1])}")
print("FINAL", s == ((1,), (2,)), len(route))
