"""Restart the beam from every state along our best path of a row; report prefix + new finish when it beats the path.
usage: python3 tools/acc/ops/mid_restart.py ROW TARGET_LEN [W] [CUTS]   (env BEAM_* passed to the beam; BIN via MR_BIN)
MR_ITER=1: iterate — every strict improvement is saved to $ACC_S/work/mr_cap.jsonl and the restarts begin again from it,
until a full pass finds nothing shorter or TARGET_LEN is reached.
TARGET_LEN = the length to reach (e.g. the record); each cut i beams from s_i with DMAX = TARGET_LEN - i."""
import glob, json, os, re, subprocess, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scratch_utils')); from acmoves import move, run
S = os.environ.get('ACC_S', '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad')
row = sys.argv[1]; T = int(sys.argv[2]); W = sys.argv[3] if len(sys.argv) > 3 else '20000'
man = json.load(open(S + '/sair/competition/tools/verifier/data/manifest.json')); C = {c['challenge_id']: c for c in man['challenges']}
L = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}; E = {'x': '0', 'X': '1', 'y': '2', 'Y': '3'}
R0 = tuple(''.join(L[i] for i in r) for r in C[row]['initial_relators'])
paths = set()
for f in glob.glob(S + '/work/*_cap.jsonl'):
    for l in open(f):
        try: d = json.loads(l)
        except Exception: continue
        if d.get('id') == row and isinstance(d.get('ac'), list) and run(R0, d['ac']) == ('x', 'y'): paths.add(tuple(d['ac']))
best = min(paths, key=len); BIN = os.environ.get('MR_BIN', S + '/p2ybin')
ITER = os.environ.get('MR_ITER') == '1'
while True:
  cuts = [int(x) for x in sys.argv[4].split(',')] if len(sys.argv) > 4 else range(1, len(best) - 8)
  st = [R0]
  for mv in best: st.append(move(st[-1], mv))
  print(json.dumps({'id': row, 'paths': len(paths), 'best': len(best), 'target': T}), flush=True)
  improved = None
  for i in cuts:
    a, b = st[i]; dmax = T - i
    if dmax < 1: break
    t0 = time.time()
    p = subprocess.run([BIN + '/acc_beam', S + '/p2beam/T8.tab', W, str(dmax), str(len(a)), *[E[c] for c in a], str(len(b)), *[E[c] for c in b]],
                       capture_output=True, text=True)
    m = re.search(r'^AC (\d+) PATH ([\d ]*)', p.stdout, re.M)
    tail = list(map(int, m.group(2).split())) if m else None
    full = list(best[:i]) + tail if tail is not None else None
    ok = full is not None and run(R0, full) == ('x', 'y')
    better = ok and len(full) < len(best) and (improved is None or len(full) < len(improved))
    print(json.dumps({'cut': i, 'len_at_cut': len(a) + len(b), 'tail': len(tail) if tail is not None else None,
                      'total': len(full) if full else None, 'ok': ok, 'path': full if better or (ok and len(full) <= T) else None,
                      'wall_s': round(time.time() - t0)}), flush=True)
    if better:
        improved = full
        with open(S + '/work/mr_cap.jsonl', 'a') as o: o.write(json.dumps({'id': row, 'ac': full, 'ac_len': len(full), 'record': T}) + '\n')
        if ITER: break
  if not (ITER and improved) or len(improved) <= T: break
  best = improved
