"""Window-14 shortening (acc_window, exact for windows <= 14) of a (y,x) route, run in the letter-swapped twin space
where the route ends at (x,y). usage: python3 tools/acc/ops/yx_window.py ROW '[route to (y,x), AC moves]'
Prints the (possibly shorter) route and the Stable AC line (route + [15,15]); replays both ends on the original row."""
import json, os, re, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scratch_utils')); from acmoves import run
S = os.environ.get('ACC_S', '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad')
row, route = sys.argv[1], json.loads(sys.argv[2])
C = {c['challenge_id']: c for c in json.load(open(S + '/sair/competition/tools/verifier/data/manifest.json'))['challenges']}
L = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}; SW = str.maketrans('xXyY', 'yYxX'); E = {'x': '0', 'X': '1', 'y': '2', 'Y': '3'}
r0, r1 = [''.join(L[i] for i in r) for r in C[row]['initial_relators']]
assert run((r0, r1), route) == ('y', 'x'), 'route does not end at (y,x)'
MAP = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 8, 7: 9, 8: 6, 9: 7, 10: 12, 11: 13, 12: 10, 13: 11}   # involution
t0, t1 = r0.translate(SW), r1.translate(SW); tp = [MAP[m] for m in route]
wd = S + '/yxwin_' + row; os.makedirs(wd, exist_ok=True)
p = subprocess.run([S + '/acc_window', wd, str(len(t0)), *[E[c] for c in t0], str(len(t1)), *[E[c] for c in t1], str(len(tp)), *map(str, tp)],
                   capture_output=True, text=True)
m = re.search(r'FINALPATH ?([\d ]*)', p.stdout)
new = [MAP[x] for x in map(int, m.group(1).split())] if m else route
ok = run((r0, r1), new) == ('y', 'x')
print(json.dumps({'row': row, 'before': len(route), 'after': len(new), 'ends_yx': ok, 'sac_len': len(new) + 2}))
print('sac-%s: %s' % (row[3:], json.dumps(new + [15, 15])))
