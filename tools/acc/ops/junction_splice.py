"""Junction splice over every route the team holds, toward both targets.
For each row, pool all verified routes from the start: AC paths (end (x,y)) and Stable routes (end (y,x), i.e. Stable lines
minus a trailing [15,15]). For target T in {(x,y), (y,x)}: index every state s on a T-route with its remaining length to T;
then from every state on ANY route (either target) search an exact radius-R neighbourhood for an indexed state and splice
prefix + connector + suffix. Reports splices shorter than our best route to T (AC length, or Stable = route + 2).
The sac-02257 case (Codex, 22:27Z): switching between two roads cut a 26-move stretch to 25 where windows <= 14 found nothing.
usage: python3 tools/acc/ops/junction_splice.py [R] [ROWS...]    (env ACC_S = scratch with work/*_cap.jsonl and sair/)
Output: one JSON line per improvement (id, target, old, new, record, k, ok, path); official core replay."""
import glob, gzip, json, os, re, sys
S = os.environ.get('ACC_S', '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad')
sys.path.insert(0, S + '/sair/competition/tools'); from verifier import core
R = int(sys.argv[1]) if len(sys.argv) > 1 else 2
ONLY = set(sys.argv[2:])
man = json.load(open(S + '/sair/competition/tools/verifier/data/manifest.json')); CH = {c['challenge_id']: c for c in man['challenges']}
def board(p):
    d = json.load(gzip.open(sorted(glob.glob(f'research/acc/live/boards/{p}_2026*.json.gz'))[-1]))['data']
    return {r['challengeId'].replace('sac-', 'ac-'): (r['currentBestLength'], r['kTeams']) for r in d['items']}
A, B = board('ac'), board('stable_ac')
XY, YX = ((1,), (2,)), ((2,), (1,))
P = {}
def add(cid, p, stable=False):
    if not isinstance(p, list) or not p or cid not in CH: return
    if stable:
        if p[-2:] != [15, 15]: return
        p = p[:-2]
    if all(isinstance(m, int) and 0 <= m < 14 for m in p): P.setdefault(cid, set()).add(tuple(p))
for f in glob.glob(S + '/work/*_cap.jsonl') + glob.glob('research/acc/live/sweeps/*.jsonl') + glob.glob('research/acc/live/ledger/*.jsonl') + glob.glob(S + '/yxm_ac-*.log') + glob.glob(S + '/yxmid_*.jsonl'):
    for l in open(f, errors='ignore'):
        try: d = json.loads(l)
        except Exception: continue
        if not isinstance(d, dict): continue
        cid = str(d.get('id') or d.get('row') or '').replace('sac-', 'ac-')
        add(cid, d.get('ac')); add(cid, d.get('path')); add(cid, d.get('sac'), stable=True)
for f in glob.glob('research/acc/live/**/*.txt', recursive=True) + glob.glob('ACC_*.txt'):
    for l in open(f, errors='ignore'):
        m = re.match(r'^\s*(s?ac-\d{5}):\s*(\[[\d,\s]*\])', l)
        if not m: continue
        try: p = json.loads(m.group(2))
        except Exception: continue
        if m.group(1).startswith('sac'): add('ac-' + m.group(1)[4:], p, stable=True)
        else: add(m.group(1), p)
def states(cid, p):
    s = tuple(tuple(w) for w in CH[cid]['initial_relators']); out = [s]
    for m in p: s = core.apply_move(s, m); out.append(s)
    return out
rows = [c for c in P if (not ONLY or c in ONLY)]
print(len(P), 'rows with routes;', sum(1 for c in P if len(P[c]) >= 2), 'with >= 2 routes', file=sys.stderr)
nfound = 0
for cid in sorted(rows):
    if len(P[cid]) < 2: continue
    R_ = [(list(p), states(cid, list(p))) for p in P[cid]]
    for T, off, rec in ((XY, 0, A.get(cid, (None, 0))), (YX, 2, B.get(cid, (None, 0)))):
        idx = {}
        for p, st in R_:
            if st[-1] != T: continue
            for j, s in enumerate(st):
                rem = len(p) - j
                if s not in idx or rem < idx[s][0]: idx[s] = (rem, p, j)
        if not idx: continue
        best = min(len(p) for p, st in R_ if st[-1] == T)
        if T == XY: best_line = best
        else:
            best_xy = min((len(p) for p, st in R_ if st[-1] == XY), default=10**9)
            best_line = min(best + 2, best_xy + 2)       # Stable line from either target
        bs = None
        for p, st in R_:
            for i, s in enumerate(st):
                if i >= best: break
                frontier = {s: []}; seen = {s}
                for d in range(R + 1):
                    for u, con in frontier.items():
                        if u in idx:
                            rem, q, j = idx[u]; L = i + len(con) + rem
                            if L < best and (bs is None or L < len(bs)): bs = p[:i] + con + q[j:]
                    if d == R: break
                    nf = {}
                    for u, con in frontier.items():
                        for m in range(14):
                            v = core.apply_move(u, m)
                            if v not in seen: seen.add(v); nf[v] = con + [m]
                    frontier = nf
        if bs:
            ok = states(cid, bs)[-1] == T; nfound += 1
            line = len(bs) + off
            print(json.dumps({'id': cid, 'target': 'x,y' if T == XY else 'y,x', 'old_route': best, 'new_route': len(bs),
                              'line_len': line, 'old_line': best_line, 'record': rec[0], 'k': rec[1], 'ok': ok,
                              'ties_or_beats': rec[0] is not None and line <= rec[0], 'path': bs}), flush=True)
print(nfound, 'improvements', file=sys.stderr)
