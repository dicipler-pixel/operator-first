"""Use the official training trivializations (competition/examples/training_424.json) as known roads.
Every state on a training path has a known number of moves left to (x, y). A scored start within
R moves of any road state gets the path  bridge + rest of the road. The (relator swap o generator
swap) image of each road is also a road with the same length, since it fixes the target (x, y).
Paths use the official ac-r2-v1 kernel (same formulas as verifier/core.py); every emitted line must
still pass the official verifier before it is sent.
usage: road_bridges.py SAIR_DIR R OUT.jsonl"""
import json, sys

SAIR, R, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3]
GENS = (1, -1, 2, -2)


def red(w):
    out = []
    for a in w:
        if out and out[-1] == -a:
            out.pop()
        else:
            out.append(a)
    return tuple(out)


def inv(w):
    return tuple(-a for a in reversed(w))


def apply(s, m):
    r0, r1 = s
    if m == 0: return (inv(r0), r1)
    if m == 1: return (r0, inv(r1))
    if m == 2: return (red(r0 + r1), r1)
    if m == 3: return (red(r0 + inv(r1)), r1)
    if m == 4: return (r0, red(r1 + r0))
    if m == 5: return (r0, red(r1 + inv(r0)))
    if m <= 9: g = GENS[m - 6]; return (red((g,) + r0 + (-g,)), r1)
    g = GENS[m - 10]; return (r0, red((g,) + r1 + (-g,)))


# relator swap (rho) and generator swap (sigma) act on move ids; rho∘sigma fixes the target (x, y)
RHO = {0: 1, 1: 0, 2: 4, 4: 2, 3: 5, 5: 3, 6: 10, 10: 6, 7: 11, 11: 7, 8: 12, 12: 8, 9: 13, 13: 9}
SIG = {6: 8, 8: 6, 7: 9, 9: 7, 10: 12, 12: 10, 11: 13, 13: 11}
def rs_move(m): return RHO.get(SIG.get(m, m), SIG.get(m, m))
def rs_state(s):
    sw = lambda w: tuple((3 - abs(a)) * (1 if a > 0 else -1) for a in w)
    return (sw(s[1]), sw(s[0]))


train = json.load(open(SAIR + '/competition/examples/training_424.json'))['instances']
road = {}                      # state -> (moves left, list of remaining moves)
bad = 0
for t in train:
    s = tuple(map(tuple, t['initial_relators'])); mv = t['moves']
    states = [s]
    for m in mv:
        s = apply(s, m); states.append(s)
    if s != ((1,), (2,)):
        bad += 1; continue
    for i, st in enumerate(states):
        rest = mv[i:]
        for key, moves in ((st, rest), (rs_state(st), [rs_move(m) for m in rest])):
            if key not in road or len(moves) < len(road[key][1]):
                road[key] = (t['training_id'], moves)
print(f'training paths replayed: {len(train) - bad} ok, {bad} bad; road states: {len(road)}', flush=True)

man = json.load(open(SAIR + '/competition/tools/verifier/data/manifest.json'))
scored = [c for c in man['challenges'] if c['challenge_id'].startswith('ac-')]
hits = 0
with open(OUT, 'w') as f:
    for n, c in enumerate(scored):
        s0 = tuple(map(tuple, c['initial_relators']))
        seen = {s0: []}
        frontier = [s0]
        best = None
        for d in range(0, R + 1):
            if d:
                nxt = []
                for s in frontier:
                    for m in range(14):
                        t = apply(s, m)
                        if t not in seen:
                            seen[t] = seen[s] + [m]; nxt.append(t)
                frontier = nxt
            for s in frontier:
                if s in road:
                    tid, rest = road[s]
                    path = seen[s] + list(rest)
                    if best is None or len(path) < len(best[1]):
                        best = (tid, path, d)
        if best:
            f.write(json.dumps({'id': c['challenge_id'], 'via': best[0], 'bridge': best[2],
                                'len': len(best[1]), 'ac': best[1]}) + '\n')
            hits += 1
        if n % 1000 == 0:
            print(n, 'starts,', hits, 'with a road', flush=True)
print('done:', hits, 'scored starts within', R, 'moves of a training road')
