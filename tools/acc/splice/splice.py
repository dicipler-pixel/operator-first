"""Path pool + splicing + waypoint restarts for one AC row.

Every known path for the row goes into a pool. All states on all pool paths become graph nodes.
Edges: consecutive path steps, plus shortcut edges found by an exact radius-R expansion from every
node (any node reachable in d <= R official moves gets an edge of weight d). Dijkstra from the
start to (x,y) gives the best spliced path. Waypoint restarts run acc_beam (no depth cap) from
states along the current best path to add new, different routes to the pool, then splice again.

usage: splice.py SAIR BIN TFILE ROW POOL.jsonl [--radius 2] [--rounds 3] [--width 20000]
                 [--fracs 0.2,0.35,0.5,0.65,0.8] [--jobs 3] [--div 0.3,0.6,0.9]
POOL.jsonl: one {"path":[...]} per line (moves 0..13). New paths are appended to it.
Prints BEST <len> <json> after each round; every printed path passes the official verifier."""
import argparse, heapq, json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor

ap = argparse.ArgumentParser()
for a in ('sair', 'bin', 'tfile', 'row', 'pool'): ap.add_argument(a)
ap.add_argument('--radius', type=int, default=2); ap.add_argument('--rounds', type=int, default=3)
ap.add_argument('--width', default='20000'); ap.add_argument('--fracs', default='0.2,0.35,0.5,0.65,0.8')
ap.add_argument('--jobs', type=int, default=3); ap.add_argument('--div', default='0.3,0.6,0.9')
ap.add_argument('--dmax', default='600')
A = ap.parse_args()
sys.path.insert(0, A.sair + '/competition/tools'); from verifier import core
man = json.load(open(A.sair + '/competition/tools/verifier/data/manifest.json'))
CH = {c['challenge_id']: c for c in man['challenges']}; ch = CH[A.row]
S0 = tuple(tuple(r) for r in ch['initial_relators']); GOAL = ((1,), (2,))
E = {1: 0, -1: 1, 2: 2, -2: 3}
def ok(p): return core.verify(ch, p, 'ac-r2-v1', man['limits'])['ok']
def enc(s): return [str(len(s[0])), *[str(E[t]) for t in s[0]], str(len(s[1])), *[str(E[t]) for t in s[1]]]
def states(p):
    s = [S0]
    for m in p: s.append(core.apply_move(s[-1], m))
    return s

def load_pool():
    pool = []
    if os.path.exists(A.pool):
        for l in open(A.pool):
            l = l.strip()
            if l:
                p = json.loads(l)['path']
                if ok(p): pool.append(p)
    return pool

def splice(pool):
    node = {}; adj = {}
    def nid(s):
        if s not in node: node[s] = len(node); adj[node[s]] = []
        return node[s]
    for p in pool:
        st = states(p)
        for i, m in enumerate(p): adj[nid(st[i])].append((1, nid(st[i + 1]), (m,)))
    nid(S0); nid(GOAL)
    rev = {v: k for k, v in node.items()}
    for u in list(rev):  # exact radius-R shortcuts
        front = {rev[u]: ()}; seen = {rev[u]}
        for d in range(1, A.radius + 1):
            nf = {}
            for s, w in front.items():
                for m in range(14):
                    t = core.apply_move(s, m)
                    if t in seen: continue
                    seen.add(t); nf[t] = w + (m,)
                    if t in node and d > 0: adj[u].append((d, node[t], nf[t]))
            front = nf
    src, dst = node[S0], node[GOAL]; dist = {src: 0}; prev = {}; pq = [(0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if u == dst: break
        if d > dist[u]: continue
        for w, v, mv in adj[u]:
            if d + w < dist.get(v, 1 << 30): dist[v] = d + w; prev[v] = (u, mv); heapq.heappush(pq, (d + w, v))
    if dst not in dist: return None, len(node)
    out = []; v = dst
    while v != src: u, mv = prev[v]; out[:0] = list(mv); v = u
    return out, len(node)

def beam_from(prefix, div='0.6'):
    s = states(prefix)[-1]
    env = dict(os.environ, BEAM_DIV=div)
    p = subprocess.run([A.bin + '/acc_beam', A.tfile, A.width, A.dmax, *enc(s)], capture_output=True, text=True, env=env, timeout=2600)
    m = re.search(r'^AC \d+ PATH ([\d ]+)', p.stdout, re.M)
    if not m: return None
    full = prefix + list(map(int, m.group(1).split()))
    return full if ok(full) else None

def add(pool, p):
    if p and p not in pool:
        pool.append(p)
        with open(A.pool, 'a') as f: f.write(json.dumps({'path': p}) + '\n')

pool = load_pool()
if not pool:
    print('pool empty: seeding with a beam from the start', flush=True); add(pool, beam_from([]))
if not pool: print('NO PATH', A.row, flush=True); sys.exit(1)
for rnd in range(A.rounds + 1):
    t0 = time.time(); best, nn = splice(pool)
    assert best is not None and ok(best)
    add(pool, best)
    print(f'ROUND {rnd} pool={len(pool)} nodes={nn} min_pool={min(map(len, pool))} spliced={len(best)} ({time.time() - t0:.0f}s)', flush=True)
    print('BEST', len(best), json.dumps(best).replace(' ', ''), flush=True)
    if rnd == A.rounds: break
    fr = [float(x) for x in A.fracs.split(',')]
    with ThreadPoolExecutor(A.jobs) as ex:
        jobs = [(f, d) for f in fr for d in A.div.split(',')]
        for p in ex.map(lambda fd: beam_from(best[:int(fd[0] * len(best))], fd[1]), jobs):
            if p: print(f'  waypoint path {len(p)}', flush=True)
            add(pool, p)
