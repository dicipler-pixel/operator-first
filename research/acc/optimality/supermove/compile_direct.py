"""Compile an smbeam supermove road into official ac-r2-v1 moves directly: for each step, cyclically reduce both relators
by conjugation, find the substitution (x <- rot(x)*rot(y^s)) that reaches the next class, realize the rotations with
single-letter conjugations (cheaper direction) plus an inversion when needed, apply one multiplication (2-5), and finish
with a small BFS to exactly (x,y). Verified with the official core, then window-shortened (acc_window).
usage: compile_direct.py ROW ROADFILE"""
import json, re, subprocess, sys
from collections import deque
import os; S = os.environ.get('ACC_S', '/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); import skel_dp_local as k
from compile_road import parse, window
CONJ = [{1: 6, -1: 7, 2: 8, -2: 9}, {1: 10, -1: 11, 2: 12, -2: 13}]
def ap(state, m, out): out.append(m); return k.core.apply_move(state, m)
def free(w):
    t = []
    for a in w:
        if t and t[-1] == -a: t.pop()
        else: t.append(a)
    return t
def conj_to(state, i, want, out):
    for m in CONJ[i].values():
        t = k.core.apply_move(state, m)
        if t[i] == want: out.append(m); return t
    raise ValueError(('conj', state[i], want))
def cyc_reduce(state, i, out):
    while len(state[i]) > 1 and state[i][0] == -state[i][-1]: state = conj_to(state, i, state[i][1:-1], out)
    return state
def rot(w, r): r %= len(w); return w[r:] + w[:r]
def inv(w): return tuple(-a for a in reversed(w))
def rotate_to(state, i, target, out):
    w = state[i]; n = len(w)
    if w == target: return state
    for flip in (False, True):
        src = inv(w) if flip else w
        for r in range(n):
            if rot(src, r) == target:
                if flip: state = ap(state, i, out)                    # invert relator i (moves 0/1)
                left = r; right = n - r
                for _ in range(left if left <= right else right):
                    state = conj_to(state, i, rot(state[i], 1 if left <= right else -1), out)
                assert state[i] == target, (state[i], target)
                return state
    raise ValueError('target is not a rotation')
def step(state, nxt_cls, out):
    for i in (0, 1): state = cyc_reduce(state, i, out)
    x0, x1 = state
    best = None
    for xi in (0, 1):
        x, y = state[xi], state[1 - xi]
        for sg in (1, -1):
            ys = y if sg == 1 else inv(y)
            for i in range(len(x)):
                rx = rot(x, i)
                for j in range(len(ys)):
                    if ys[j] != -rx[-1]: continue
                    ry = rot(ys, j)
                    w = k.cyc(free(rx + ry))
                    cl = k.cls((tuple(w), y) if xi == 0 else (y, tuple(w)))
                    if cl != nxt_cls: continue
                    cost = min(i, len(x) - i) + min(j, len(ys) - j)
                    if best is None or cost < best[0]: best = (cost, xi, sg, rx, ry)
    if best is None: raise ValueError('no substitution reaches the next class')
    _, xi, sg, rx, ry = best; yi = 1 - xi
    state = rotate_to(state, xi, rx, out)
    ytarget = ry if sg == 1 else inv(ry)
    state = rotate_to(state, yi, ytarget, out)
    m = (2 if sg == 1 else 3) if xi == 0 else (4 if sg == 1 else 5)
    return ap(state, m, out)
def finish(state, target=((1,), (2,)), depth=10):
    q = deque([(state, [])]); seen = {state}
    while q:
        s, p = q.popleft()
        if s == target: return p
        if len(p) >= depth: continue
        for m in range(14):
            t = k.core.apply_move(s, m)
            if sum(len(w) for w in t) > 6 or t in seen: continue
            seen.add(t); q.append((t, p + [m]))
    return None
def compile_row(cid, roadfile):
    c = k.T[cid]; st = tuple(tuple(r) for r in c['initial_relators'])
    road = parse(roadfile); R = []
    for s in road:
        cl = k.cls(s)
        if not R or R[-1] != cl: R.append(cl)
    out = []; state = st
    for cl in R[1:]:
        state = step(state, cl, out)
    for i in (0, 1): state = cyc_reduce(state, i, out)
    f = finish(state)
    if f is None: return {'id': cid, 'err': 'finish'}, None
    out += f
    v = k.core.verify(c, out, 'ac-r2-v1', k.rl.LIMITS)
    if not (v.get('ok', v.get('valid', False)) or v.get('status') == 'ok'): return {'id': cid, 'err': 'verify'}, None
    raw = len(out); w = window(*c['initial_relators'], out)
    v2 = k.core.verify(c, w, 'ac-r2-v1', k.rl.LIMITS)
    if (v2.get('ok', v2.get('valid', False)) or v2.get('status') == 'ok') and len(w) < len(out): out = w
    return {'id': cid, 'road': len(R), 'raw_len': raw, 'ac_len': len(out)}, out
if __name__ == '__main__':
    rec, out = compile_row(sys.argv[1], sys.argv[2]); print(json.dumps(rec)); print(json.dumps(out) if out else 'NOPATH')
