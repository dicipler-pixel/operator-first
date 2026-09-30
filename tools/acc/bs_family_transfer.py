"""BS-family transfer (x^-1 y^n x = y^(n+1), n=2,3,4): the same second relator is solved at one n and unsolved at another.
Replay our path for the solved partner on the unsolved row, take the shortest prefix states, and search on from there
(relator-substitution solver, then acc_beam H and P2). Paths replayed with the official core. Out: work/bs_transfer.jsonl"""
import sys, json, os, subprocess, collections
S = '/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad'
sys.path.insert(0, S + '/sair/competition/tools'); sys.path.insert(0, os.path.dirname(__file__))
from verifier import core
import subst_solver as ss
m = json.load(open(S + '/sair/competition/tools/verifier/data/manifest.json')); C = {c['challenge_id']: c for c in m['challenges']}
rows = json.load(open(S + '/work/pattern_rows.json'))
W = lambda t: ''.join({1: 'x', -1: 'X', 2: 'y', -2: 'Y'}[g] for g in t)
cls = {'YYYXyyx': 2, 'YYYYXyyyx': 3, 'YYYYYXyyyyx': 4}
roads = {}
for f in ('all_roads', 'kernel_paths'):
    for l in open(S + '/work/' + f + '.jsonl'):
        r = json.loads(l)
        if isinstance(r.get('ac'), list) and (r['id'] not in roads or len(r['ac']) < len(roads[r['id']])): roads[r['id']] = r['ac']
by = collections.defaultdict(dict)
for x in rows:
    k = W(x['shortrel'])
    if k in cls:
        a, b = x['rel']; o = W(b) if tuple(a) == tuple(x['shortrel']) else W(a)
        by[o][cls[k]] = x
E = {1: 0, -1: 1, 2: 2, -2: 3}
def beam(s, env, W_='20000', depth=250, T=240):
    enc = [str(len(s[0]))] + [str(E[g]) for g in s[0]] + [str(len(s[1]))] + [str(E[g]) for g in s[1]]
    try: o = subprocess.run([S + '/dualbin/acc_beam', S + '/work/T9.tab', W_, str(depth)] + enc, capture_output=True, text=True, timeout=T, env={**os.environ, **env}).stdout
    except subprocess.TimeoutExpired: return None
    for line in o.splitlines():
        if line.startswith('AC ') and 'PATH' in line: return [int(v) for v in line.split('PATH')[1].split()]
out = S + '/work/bs_transfer.jsonl'
done = {json.loads(l)['id'] for l in open(out)} if os.path.exists(out) else set()
for o, v in by.items():
    src = [x for x in v.values() if x['id'] in roads]
    for tgt in [x for x in v.values() if x['st'] == 'unsolved' and x['id'] not in done]:
        st = tuple(tuple(r) for r in C[tgt['id']]['initial_relators']); target = tuple(tuple(r) for r in C[tgt['id']]['target_relators'])
        seeds = [([], st)]
        for sx in src:
            s = st; pre = []; cand = []
            for mv in roads[sx['id']]:
                s = core.apply_move(s, mv); pre = pre + [mv]; cand.append((ss.clen(s), len(pre), list(pre), s))
            cand.sort(key=lambda c: (c[0], -c[1])); seeds += [(c[2], c[3]) for c in cand[:2]]
        rec = {'id': tgt['id'], 'from': [x['id'] for x in src], 'seed_len': [ss.clen(s) for _, s in seeds], 'ok': False}
        for pre, s in seeds:
            nd, info = ss.solve(s, 150, 120, 8, 120)
            path = None
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
