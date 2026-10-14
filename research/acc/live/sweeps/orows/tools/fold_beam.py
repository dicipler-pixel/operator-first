"""Song idea 1 (FOLD): rotation-folded multiplication beam. One step = rotate r0 by a and r1 by b with real conjugation moves
(|a|,|b| <= R, each rotation step = 1 move), then one multiplication (moves 2-5); or a single inversion (0/1).
Only the post-step states compete, in buckets by REAL move cost; each bucket keeps the W best by total length (seeded tie-break).
Every child is looked up in exact balls around (x,y) and (y,x) (radius RB, length cap). Lines are replayed on the official cores.
usage: fold_beam.py ROW W R MAXCOST [SEED]"""
import json, sys, time, random
from collections import deque
sys.path.insert(0, '/root/.cache/upgh/sair/competition/tools'); from verifier import core, stable_core
man = json.load(open('/root/.cache/upgh/sair/competition/tools/verifier/data/manifest.json')); CH = {c['challenge_id']: c for c in man['challenges']}; LIM = man['limits']
n, W, R, MAXC = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); seed = int(sys.argv[5]) if len(sys.argv) > 5 else 0
rng = random.Random(seed)
XY = ((1,), (2,)); YX = ((2,), (1,)); INV = (0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12)
CONJ = {(0, 1): 6, (0, -1): 7, (0, 2): 8, (0, -2): 9, (1, 1): 10, (1, -1): 11, (1, 2): 12, (1, -2): 13}
def ball(goal, rad, cap):
    D = {goal: []}; fr = [goal]
    for d in range(rad):
        nf = []
        for s in fr:
            for m in range(14):
                t = core.apply_move(s, m)
                if t not in D and len(t[0]) + len(t[1]) <= cap: D[t] = [INV[m]] + D[s]; nf.append(t)
        fr = nf
    return D
t0 = time.time()
RB = 6; BX = ball(XY, RB, 14); BY = ball(YX, RB, 14)
print('balls', len(BX), len(BY), round(time.time() - t0), 's', flush=True)
def rots(s, i):
    """variants of relator i by rotation-only conjugations: list of (state, moves)"""
    out = [(s, [])]
    for side in (0, 1):
        cur, mv = s, []
        for k in range(R):
            w = cur[i]
            if len(w) < 2: break
            c = -w[0] if side == 0 else w[-1]
            m = CONJ[(i, c)]; cur = core.apply_move(cur, m); mv = mv + [m]
            out.append((cur, mv))
    return out
start = tuple(tuple(w) for w in CH['ac-' + n]['initial_relators'])
nodes = [(None, [], start)]  # parent idx, macro moves, state
best = {start: 0}
buckets = {0: [(0, start)]}
bestAC = (10 ** 9, None); bestS = (10 ** 9, None)
def path_of(idx):
    out = []
    while idx is not None:
        p, mv, _ = nodes[idx]; out = mv + out; idx = p
    return out
def check(idx, s, c):
    global bestAC, bestS
    if s in BX and c + len(BX[s]) < bestAC[0]:
        line = path_of(idx) + BX[s]
        if core.verify(CH['ac-' + n], line, 'ac-r2-v1', LIM)['ok']: bestAC = (len(line), line)
    if s in BY and c + len(BY[s]) + 2 < bestS[0]:
        line = path_of(idx) + BY[s] + [15, 15]
        if stable_core.verify(CH['sac-' + n], line, 'sac-r8-v1', LIM)['ok']: bestS = (len(line), line)
check(0, start, 0)
for c in range(0, MAXC + 1):
    B = buckets.pop(c, [])
    if not B: continue
    B = [(i, s) for i, s in B if best.get(s, 1 << 30) == c]
    B.sort(key=lambda x: (len(x[1][0]) + len(x[1][1]), rng.random()))
    B = B[:W]
    for idx, s in B:
        r0 = rots(s, 0)
        for s0, m0 in r0:
            for s1, m1 in rots(s0, 1):
                pre = m0 + m1
                for m in (2, 3, 4, 5):
                    t = core.apply_move(s1, m); cc = c + len(pre) + 1
                    if cc > MAXC or best.get(t, 1 << 30) <= cc: continue
                    best[t] = cc; nodes.append((idx, pre + [m], t)); j = len(nodes) - 1
                    buckets.setdefault(cc, []).append((j, t)); check(j, t, cc)
        for m in (0, 1):
            t = core.apply_move(s, m); cc = c + 1
            if cc <= MAXC and best.get(t, 1 << 30) > cc:
                best[t] = cc; nodes.append((idx, [m], t)); j = len(nodes) - 1; buckets.setdefault(cc, []).append((j, t)); check(j, t, cc)
    print('cost %d kept %d nodes %d bestAC %s bestSAC %s %.0fs' % (c, len(B), len(nodes), bestAC[0] if bestAC[1] else None, bestS[0] if bestS[1] else None, time.time() - t0), flush=True)
    if c + 1 >= min(bestAC[0], bestS[0] - 2): break
print(json.dumps({'row': n, 'W': W, 'R': R, 'seed': seed, 'AC': bestAC[0] if bestAC[1] else None, 'SAC': bestS[0] if bestS[1] else None,
                  'ac_line': bestAC[1], 'sac_line': bestS[1], 'secs': round(time.time() - t0)}), flush=True)
