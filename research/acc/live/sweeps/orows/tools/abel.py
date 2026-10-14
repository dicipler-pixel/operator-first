"""Song idea 2a (count the throb): exponent-sum matrix E of a state; exact row-op distance to I ((x,y)) and J ((y,x)) by BFS over
|entries| <= M. Compare with the number of non-conjugation moves in our roads."""
import json, sys
S = '/tmp/claude-0/-home-user-operator-first/644f7765-aca6-5d39-980a-3e4ddc6288c0/scratchpad/orows'
from collections import deque
sys.path.insert(0, '/root/.cache/upgh/sair/competition/tools'); from verifier import core
man = json.load(open('/root/.cache/upgh/sair/competition/tools/verifier/data/manifest.json')); CH = {c['challenge_id']: c for c in man['challenges']}
M = 24
def E(s): return tuple((sum(1 for t in w if t == 1) - sum(1 for t in w if t == -1), sum(1 for t in w if t == 2) - sum(1 for t in w if t == -2)) for w in s)
def mv(e, m):
    (a, b), (c, d) = e
    if m == 0: return ((-a, -b), (c, d))
    if m == 1: return ((a, b), (-c, -d))
    if m == 2: return ((a + c, b + d), (c, d))
    if m == 3: return ((a - c, b - d), (c, d))
    if m == 4: return ((a, b), (c + a, d + b))
    if m == 5: return ((a, b), (c - a, d - b))
def ball(goal):
    D = {goal: 0}; q = deque([goal])
    while q:
        e = q.popleft()
        for m in range(6):
            f = mv(e, m)
            if max(abs(v) for r in f for v in r) <= M and f not in D: D[f] = D[e] + 1; q.append(f)
    return D
DI = ball(((1, 0), (0, 1))); DJ = ball(((0, 1), (1, 0)))
if __name__ == '__main__':

    import glob
    roads = {}
    for f in [S + '/all_ac_roads.json', S + '/all_ac_roads_r3.json']:
        roads.update(json.load(open(f)))
    sl = {}
    for f in [S + '/all_sac_lines.json', S + '/all_sac_lines_r3.json']:
        sl.update(json.load(open(f)))
    for n in sys.argv[1:]:
        s0 = tuple(tuple(w) for w in CH['ac-' + n]['initial_relators']); e0 = E(s0)
        ac = roads.get('ac-' + n, [None])[0]; yx = [l[:-2] for l in sl.get('sac-' + n, []) if l[-2:] == [15, 15] and all(m <= 13 for m in l[:-2])]
        nc = lambda p: sum(1 for m in p if m <= 5) if p else None
        print(n, 'E0', e0, 'dist I', DI.get(e0), 'dist J', DJ.get(e0), '| best AC road', len(ac) if ac else None, 'non-conj', nc(ac),
              '| best (y,x) road', len(yx[0]) if yx else None, 'non-conj', nc(yx[0]) if yx else None)
