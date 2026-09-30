"""(y,x) mid-restart: from every state s_i of a given AC path of a row, beam the letter-swapped state (x<->y) toward (x,y)
with DMAX = TARGET - i, map the tail back (conjugations by x and y trade places), and keep prefix + tail when it is a route
from the row to (y,x) of length <= TARGET. The Stable AC line is that route + [15, 15], so TARGET = Stable record - 2 ties.
usage: python3 tools/acc/ops/yx_mid.py ROW TARGET 'PATH_JSON' [W] [STEP]   (env BEAM_* passed to the beam; BIN via MR_BIN)
env YX_START=i resumes at cut i; YX_CAP=file appends each new best route (JSON line) as soon as it is found.
Prints one JSON line per cut; the last line is the best route found (or none)."""
import json, os, re, subprocess, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scratch_utils')); from acmoves import move, run
S = os.environ.get('ACC_S', '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad')
row, T, path = sys.argv[1], int(sys.argv[2]), json.loads(sys.argv[3])
W = sys.argv[4] if len(sys.argv) > 4 else '20000'; STEP = int(sys.argv[5]) if len(sys.argv) > 5 else 1
man = json.load(open(S + '/sair/competition/tools/verifier/data/manifest.json')); C = {c['challenge_id']: c for c in man['challenges']}
L = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}; E = {'x': '0', 'X': '1', 'y': '2', 'Y': '3'}; SW = str.maketrans('xXyY', 'yYxX')
BACK = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 8, 7: 9, 8: 6, 9: 7, 10: 12, 11: 13, 12: 10, 13: 11}
R0 = tuple(''.join(L[i] for i in r) for r in C[row]['initial_relators'])
assert run(R0, path) == ('x', 'y'), 'given path does not reach (x,y)'
BIN = os.environ.get('MR_BIN', S + '/p2ybin')
st = [R0]
for mv in path: st.append(move(st[-1], mv))
best = None
START = int(os.environ.get('YX_START', '0'))  # resume: skip cuts a killed run already logged
CAP = os.environ.get('YX_CAP')  # append each new best route here at once, so a killed run keeps its hit
for i in range(START, min(len(path), T), STEP):
    if st[i] == ('y', 'x') and i <= T:
        best = list(path[:i]); print(json.dumps({'cut': i, 'route': i, 'note': 'path passes (y,x)'}), flush=True); break
    a, b = st[i][0].translate(SW), st[i][1].translate(SW); dmax = T - i
    if dmax < 1: break
    t0 = time.time()
    p = subprocess.run([BIN + '/acc_beam', S + '/p2beam/T8.tab', W, str(dmax), str(len(a)), *[E[c] for c in a], str(len(b)), *[E[c] for c in b]],
                       capture_output=True, text=True)
    m = re.search(r'^AC (\d+) PATH ([\d ]*)', p.stdout, re.M)
    tail = [BACK[x] for x in map(int, m.group(2).split())] if m else None
    full = list(path[:i]) + tail if tail is not None else None
    ok = full is not None and run(R0, full) == ('y', 'x')
    if ok and len(full) <= T and (best is None or len(full) < len(best)):
        best = full
        if CAP:
            with open(CAP, 'a') as o: o.write(json.dumps({'id': row, 'target': T, 'best_route': len(best), 'sac_len': len(best) + 2, 'sac': best + [15, 15]}) + '\n')
    print(json.dumps({'cut': i, 'len_at_cut': len(a) + len(b), 'tail': len(tail) if tail is not None else None,
                      'route': len(full) if full else None, 'ok': ok, 'wall_s': round(time.time() - t0)}), flush=True)
print(json.dumps({'id': row, 'target': T, 'best_route': len(best) if best else None,
                  'sac_len': len(best) + 2 if best else None, 'sac': best + [15, 15] if best else None}), flush=True)
