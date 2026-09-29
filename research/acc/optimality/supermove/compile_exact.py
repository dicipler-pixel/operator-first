"""Replay an smbeam2 actual-state road as official ac-r2-v1 moves (rotations by single conjugations, one multiplication,
cyclic reduction), finish to (x,y) by BFS, verify with the official core. usage: compile_exact.py ROW ROADFILE"""
import json, sys
import os; S = os.environ.get('ACC_S', '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compile_direct as cd, skel_dp_local as k
def parse(f):
    road = []; on = False
    for l in open(f):
        if l.startswith('ROAD'): on = True; continue
        if on and '|' in l:
            a, b = l.split('|'); road.append((tuple(int(t) for t in a.split()), tuple(int(t) for t in b.split())))
    return road
def step(state, nxt, out):
    best = None
    for xi in (0, 1):
        x, y = state[xi], state[1 - xi]; nx, ny = len(x), len(y)
        if y != tuple(nxt[1 - xi]) and not any(cd.rot(y, r) == tuple(nxt[1 - xi]) for r in range(ny)): continue
        for sg in (1, -1):
            ys = y if sg == 1 else cd.inv(y)
            for i in range(nx):
                rx = cd.rot(x, i)
                for j in range(ny):
                    if ys[j] != -rx[-1]: continue
                    ry = cd.rot(ys, j); yr = ry if sg == 1 else cd.inv(ry)
                    if yr != tuple(nxt[1 - xi]): continue
                    if tuple(k.cyc(cd.free(rx + ry))) != tuple(nxt[xi]): continue
                    cost = min(i, nx - i) + min(j, ny - j)
                    if best is None or cost < best[0]: best = (cost, xi, sg, rx, yr)
    if best is None: raise ValueError('no exact supermove')
    _, xi, sg, rx, yr = best
    state = cd.rotate_to(state, xi, rx, out); state = cd.rotate_to(state, 1 - xi, yr, out)
    state = cd.ap(state, (2 if sg == 1 else 3) if xi == 0 else (4 if sg == 1 else 5), out)
    state = cd.cyc_reduce(state, xi, out)
    assert state == tuple(tuple(w) for w in nxt), (state, nxt)
    return state
def compile_row(cid, roadfile):
    c = k.T[cid]; state = tuple(tuple(r) for r in c['initial_relators']); out = []
    for i in (0, 1): state = cd.cyc_reduce(state, i, out)
    road = parse(roadfile)
    assert state == road[0], (state, road[0])
    for nxt in road[1:]: state = step(state, nxt, out)
    f = cd.finish(state)
    if f is None: raise ValueError('finish')
    out += f
    v = k.core.verify(c, out, 'ac-r2-v1', k.rl.LIMITS)
    if not v.get('ok'): raise ValueError('verify')
    return out
if __name__ == '__main__':
    out = compile_row(sys.argv[1], sys.argv[2]); print(len(out)); print(json.dumps(out))
