"""Opposite-orientation beam: run the beam on the exact mirror twin of a row (swap letters x<->y AND swap the two
relators; this symmetry fixes the target (x,y)), then map the path back move by move and replay it on the original.
usage: python3 tools/acc/ops/twin_beam.py ROW [W] [DMAX]   (env: BEAM_* as for acc_beam; BIN dir via TWIN_BIN)
TWIN_MODE=yx: swap letters only (keep relator order): the twin's path to (x,y) is a path from the row to (y,x), so the
Stable AC line is that path + [15,15] (reported as "sac"); the AC fields are then not set."""
import json, os, re, subprocess, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scratch_utils')); from acmoves import run
S = os.environ.get('ACC_S', '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad')
row = sys.argv[1]; W = sys.argv[2] if len(sys.argv) > 2 else '20000'; D = sys.argv[3] if len(sys.argv) > 3 else '60'
man = json.load(open(S + '/sair/competition/tools/verifier/data/manifest.json'))
C = {c['challenge_id']: c for c in man['challenges']}
L = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}; SW = str.maketrans('xXyY', 'yYxX')
r0, r1 = [''.join(L[i] for i in r) for r in C[row]['initial_relators']]
YX = os.environ.get('TWIN_MODE') == 'yx'
if YX:
    t0, t1 = r0.translate(SW), r1.translate(SW)        # twin = (sigma(r0), sigma(r1)); its (x,y) is our (y,x)
    BACK = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 8, 7: 9, 8: 6, 9: 7, 10: 12, 11: 13, 12: 10, 13: 11}
else:
    t0, t1 = r1.translate(SW), r0.translate(SW)        # twin = (sigma(r1), sigma(r0))
    BACK = {0: 1, 1: 0, 2: 4, 3: 5, 4: 2, 5: 3, 6: 12, 7: 13, 8: 10, 9: 11, 10: 8, 11: 9, 12: 6, 13: 7}
E = {'x': '0', 'X': '1', 'y': '2', 'Y': '3'}
enc = lambda a, b: [str(len(a)), *[E[c] for c in a], str(len(b)), *[E[c] for c in b]]
BIN = os.environ.get('TWIN_BIN', S + '/p2ybin')
t = time.time()
p = subprocess.run([BIN + '/acc_beam', S + '/p2beam/T8.tab', W, D, *enc(t0, t1)], capture_output=True, text=True)
m = re.search(r'^AC \d+ PATH ([\d ]+)', p.stdout, re.M)
if not m: print(json.dumps({'id': row, 'twin': True, 'verdict': 'nopath', 'wall_s': round(time.time() - t)})); sys.exit()
tp = list(map(int, m.group(1).split())); op = [BACK[x] for x in tp]
if YX:
    ok = run((r0, r1), op) == ('y', 'x')
    print(json.dumps({'id': row, 'twin': 'yx', 'sac_len': len(op) + 2, 'ok': ok, 'sac': op + [15, 15], 'wall_s': round(time.time() - t)})); sys.exit()
ok = run((r0, r1), op) == ('x', 'y')
print(json.dumps({'id': row, 'twin': True, 'ac_len': len(op), 'ok': ok, 'ac': op, 'wall_s': round(time.time() - t)}))
