"""Skeleton-family transfer (after Viaclovsky 2609.33785 §6.3: vary a parameter, keep the combinatorial type).
Rows with the same syllable skeleton (letter pattern, exponents abstracted) form a family. For each unsolved row,
take the nearest sibling we hold a path for (L1 distance of aligned exponent vectors), replay that path on the
unsolved row, and search on from the shortest prefix states (relator-substitution solver, then acc_beam H/P2).
Every path is replayed with the official core. Nearest pairs first. Out: work/skel_transfer.jsonl"""
import sys, json, os, subprocess, collections
S = '/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad'
sys.path.insert(0, S + '/sair/competition/tools'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from verifier import core
import subst_solver as ss
m = json.load(open(S + '/sair/competition/tools/verifier/data/manifest.json')); C = {c['challenge_id']: c for c in m['challenges']}
rows = json.load(open(S + '/work/pattern_rows.json'))
roads = {}
for f in ('all_roads', 'kernel_paths'):
    for l in open(S + '/work/' + f + '.jsonl'):
        r = json.loads(l)
        if isinstance(r.get('ac'), list) and (r['id'] not in roads or len(r['ac']) < len(roads[r['id']])): roads[r['id']] = r['ac']
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
def sig(x):
    a, b = sorted((canon(x['rel'][0]), canon(x['rel'][1])))
    return (a[0], b[0]), a[1] + b[1]
fam = collections.defaultdict(list)
for x in rows:
    sk, ex = sig(x); fam[sk].append((x, ex))
pairs = []
for sk, v in fam.items():
    src = [(x, e) for x, e in v if x['id'] in roads]
    for x, e in v:
        if x['st'] != 'unsolved' or not src: continue
        d, sx = min((sum(abs(p - q) for p, q in zip(e, e2)), s['id']) for s, e2 in src)
        pairs.append((d, x['id'], sx))
pairs.sort()
E = {1: 0, -1: 1, 2: 2, -2: 3}
def beam(s, env, W_='20000', depth=250, T=int(os.environ.get('SKEL_BEAMT', '60'))):
    enc = [str(len(s[0]))] + [str(E[g]) for g in s[0]] + [str(len(s[1]))] + [str(E[g]) for g in s[1]]
    try: o = subprocess.run([S + '/dualbin/acc_beam', S + '/work/T9.tab', W_, str(depth)] + enc, capture_output=True, text=True, timeout=T, env={**os.environ, **env}).stdout
    except subprocess.TimeoutExpired: return None
    for line in o.splitlines():
        if line.startswith('AC ') and 'PATH' in line: return [int(v) for v in line.split('PATH')[1].split()]
out = S + '/work/skel_transfer.jsonl'
done = {json.loads(l)['id'] for l in open(out)} if os.path.exists(out) else set()
print('pairs', len(pairs), 'distance histogram', collections.Counter(min(d, 10) for d, _, _ in pairs), flush=True)
for d, tid, sid in pairs:
    if tid in done: continue
    st = tuple(tuple(r) for r in C[tid]['initial_relators']); target = tuple(tuple(r) for r in C[tid]['target_relators'])
    s = st; pre = []; cand = []
    for mv in roads[sid]:
        s = core.apply_move(s, mv); pre = pre + [mv]; cand.append((ss.clen(s), len(pre), list(pre), s))
    cand.sort(key=lambda c: (c[0], -c[1]))
    seeds = [(c[2], c[3]) for c in cand[:int(os.environ.get('SKEL_SEEDS', '1'))]]
    rec = {'id': tid, 'from': sid, 'd': d, 'seed_len': [ss.clen(z) for _, z in seeds], 'ok': False}
    for pre, s in seeds:
        path = None
        nd, info = ss.solve(s, 150, 100, 8, int(os.environ.get('SKEL_SUBT', '30')))
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
            if z == target: rec.update(ok=True, len=len(path), moves=path); break
    print(json.dumps({k: v for k, v in rec.items() if k != 'moves'}), flush=True)
    with open(out, 'a') as f: f.write(json.dumps(rec) + '\n')
