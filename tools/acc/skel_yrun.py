"""Skeleton transfer restricted to Fable's 128 unsolved y-run MS rows (UPG-H assignment 19:03Z, UPDATE_upgh_to_all_20260930T1903Z.md).
Targets: research/acc/live/sweeps/fable/zoom_20260930T1858Z.json 'soft_unsolved_yrun_rows', in that order (nearest solved sibling first).
Donors: every held AC road (session 1 verified pool + UPG-H ledger) on a row with the same syllable skeleton, nearest by L1
distance of aligned exponents first (up to DONORS per target). For each donor: replay its path on the target, keep the SEEDS
shortest prefix states, run the substitution solver, then two acc_beam settings (H/DIV and P2) with a free depth limit.
Every path is replayed with the official core and must end at the target relators. Out: work/skel_yrun.jsonl, lines to
work/skel_yrun_lines.txt. Usage: python3 tools/acc/skel_yrun.py"""
import sys, json, os, re, subprocess, collections
S = '/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad'
REPO = '/home/user/operator-first'
sys.path.insert(0, S + '/sair/competition/tools'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verifier import core
import subst_solver as ss
m = json.load(open(S + '/sair/competition/tools/verifier/data/manifest.json')); C = {c['challenge_id']: c for c in m['challenges']}
DONORS = int(os.environ.get('DONORS', '4')); SEEDS = int(os.environ.get('SEEDS', '3')); BEAMT = int(os.environ.get('BEAMT', '90'))

roads = {}
def add(i, p):
    if isinstance(p, list) and i and i.startswith('ac-') and (i not in roads or len(p) < len(roads[i])): roads[i] = p
for l in open(S + '/known_roads_ok.txt'):
    mm = re.match(r'^(ac-\d{5}):\s*(\[.*\])', l.strip())
    if mm: add(mm.group(1), json.loads(mm.group(2)))
for l in open(REPO + '/research/acc/upgh/ledger.jsonl'):
    try: d = json.loads(l)['data']
    except Exception: continue
    if d.get('cid', '').startswith('ac-') and d.get('agree'): add(d['cid'], d.get('moves'))

def syl(w):
    s = []
    for g in w:
        if s and s[-1][0] == g: s[-1][1] += 1
        else: s.append([g, 1])
    if len(s) > 1 and s[0][0] == s[-1][0]: s[0][1] += s.pop()[1]
    return s
def canon(w):
    s = syl(w); best = None
    for v in (s, [[-g, c] for g, c in reversed(s)]):
        for k in range(len(v)):
            r = v[k:] + v[:k]; key = (tuple(g for g, _ in r), tuple(c for _, c in r))
            if best is None or key < best: best = key
    return best
def sig(rel):
    a, b = sorted((canon(rel[0]), canon(rel[1])))
    return (a[0], b[0]), a[1] + b[1]

fam = collections.defaultdict(list)
for cid, c in C.items():
    if cid.startswith('ac-'):
        sk, ex = sig(c['initial_relators']); fam[sk].append((cid, ex))
Y = json.load(open(REPO + '/research/acc/live/sweeps/fable/zoom_20260930T1858Z.json'))['soft_unsolved_yrun_rows']
if os.environ.get('REVERSE'): Y = Y[::-1]   # second worker: other end of the list
E = {1: 0, -1: 1, 2: 2, -2: 3}
def beam(s, env, W_='20000', depth=250):
    enc = [str(len(s[0]))] + [str(E[g]) for g in s[0]] + [str(len(s[1]))] + [str(E[g]) for g in s[1]]
    try: o = subprocess.run([S + '/dualbin/acc_beam', S + '/work/T9.tab', W_, str(depth)] + enc, capture_output=True, text=True, timeout=BEAMT, env={**os.environ, **env}).stdout
    except subprocess.TimeoutExpired: return None
    for line in o.splitlines():
        if line.startswith('AC ') and 'PATH' in line: return [int(v) for v in line.split('PATH')[1].split()]
out = S + '/work/skel_yrun.jsonl'
done = {json.loads(l)['id'] for l in open(out)} if os.path.exists(out) else set()
nodonor = 0
for row in Y:
    tid = row[0]
    if os.path.exists(out): done |= {json.loads(l)['id'] for l in open(out)}
    if tid in done or os.path.exists(S + '/work/skel_yrun_claim_' + tid): continue
    open(S + '/work/skel_yrun_claim_' + tid, 'w').close()   # a row is taken by the first worker to reach it
    sk, ex = sig(C[tid]['initial_relators'])
    donors = sorted((sum(abs(p - q) for p, q in zip(ex, e2)), sid) for sid, e2 in fam[sk] if sid in roads and sid != tid)[:DONORS]
    rec = {'id': tid, 'n': row[1], 'w': row[2], 'donors': [(d, s, len(roads[s])) for d, s in donors], 'ok': False}
    if not donors: nodonor += 1
    st = tuple(tuple(r) for r in C[tid]['initial_relators']); target = tuple(tuple(r) for r in C[tid]['target_relators'])
    for d, sid in donors:
        s = st; pre = []; cand = []
        for mv in roads[sid]:
            s = core.apply_move(s, mv); pre = pre + [mv]; cand.append((ss.clen(s), len(pre), list(pre), s))
        cand.sort(key=lambda c: (c[0], -c[1]))
        for c in cand[:SEEDS]:
            pre, s = c[2], c[3]; path = None
            nd, info = ss.solve(s, 150, 100, 8, int(os.environ.get('SUBT', '30')))
            if nd is not None:
                fin = ss.finish(ss.Node(nd.s, []))
                if fin is not None: path = pre + nd.mv + fin
            for env in ({'BEAM_H': '1', 'BEAM_DIV': '1.0'}, {'BEAM_P2': '2', 'BEAM_H': '1', 'BEAM_DIV': '0.8'}):
                if path: break
                b = beam(s, env)
                if b: path = pre + b
            if path:
                z = st
                for mv in path: z = core.apply_move(z, mv)
                if z == target:
                    rec.update(ok=True, len=len(path), moves=path, via=sid)
                    with open(S + '/work/skel_yrun_lines.txt', 'a') as f: f.write('%s: %s\n' % (tid, json.dumps(path).replace(' ', '')))
                    break
        if rec['ok']: break
    print(json.dumps({k: v for k, v in rec.items() if k != 'moves'}), flush=True)
    with open(out, 'a') as f: f.write(json.dumps(rec) + '\n')
print('DONE no-donor rows', nodonor, flush=True)
