"""Control for song idea 1: plain Python beam, layers by move count, all 14 moves, W best by total length (seeded tie-break),
same exact finish balls as fold_beam.py. usage: plain_beam.py ROW W MAXD [SEED]"""
import json, sys, time, random
sys.path.insert(0, '/root/.cache/upgh/sair/competition/tools'); from verifier import core, stable_core
man = json.load(open('/root/.cache/upgh/sair/competition/tools/verifier/data/manifest.json')); CH = {c['challenge_id']: c for c in man['challenges']}; LIM = man['limits']
n, W, MAXD = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); rng = random.Random(int(sys.argv[4]) if len(sys.argv) > 4 else 0)
XY = ((1,), (2,)); YX = ((2,), (1,)); INV = (0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12)
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
t0 = time.time(); BX = ball(XY, 6, 14); BY = ball(YX, 6, 14)
start = tuple(tuple(w) for w in CH['ac-' + n]['initial_relators'])
layer = [(start, [])]; seen = {start}; bestAC = (10 ** 9, None); bestS = (10 ** 9, None)
for d in range(MAXD + 1):
    for s, p in layer:
        if s in BX and d + len(BX[s]) < bestAC[0]:
            l = p + BX[s]
            if core.verify(CH['ac-' + n], l, 'ac-r2-v1', LIM)['ok']: bestAC = (len(l), l)
        if s in BY and d + len(BY[s]) + 2 < bestS[0]:
            l = p + BY[s] + [15, 15]
            if stable_core.verify(CH['sac-' + n], l, 'sac-r8-v1', LIM)['ok']: bestS = (len(l), l)
    if d == MAXD or d + 1 >= min(bestAC[0], bestS[0] - 2): break
    kids = []
    for s, p in layer:
        for m in range(14):
            t = core.apply_move(s, m)
            if t in seen: continue
            seen.add(t); kids.append((len(t[0]) + len(t[1]), rng.random(), t, p + [m]))
    kids.sort(key=lambda x: (x[0], x[1])); layer = [(k[2], k[3]) for k in kids[:W]]
print(json.dumps({'row': n, 'W': W, 'AC': bestAC[0] if bestAC[1] else None, 'SAC': bestS[0] if bestS[1] else None, 'ac_line': bestAC[1], 'sac_line': bestS[1], 'secs': round(time.time() - t0)}), flush=True)
