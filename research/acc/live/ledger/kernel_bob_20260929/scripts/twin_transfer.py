# SCRIPT: KERNEL-TWIN-TRANSFER-01
# Turn a verified path for a pool twin T0 into a path for our row R0.
# Find phi = sigma o psi (sigma = one of 8 letter symmetries) and relator order s so that
# phi^-1(T0) relators are cyclic rotations / inverses of R0's relators. Then
#   bridge R0 -> R1 = phi^-1(T0) with conjugation + inversion moves (BFS per relator),
#   pull the twin path back through phi (relator indices relabelled if s swaps),
#   finish to ((1,),(2,)) by BFS. The whole line is replayed with the official core.
import sys, itertools
from collections import deque
sys.path.insert(0, '/home/claude/sair/competition/tools')
from verifier.core import apply_move, free_reduce
from ms_detect import red, inv, sub, cyc_forms
from ms_route import pull_back, inverse_auto, finish_bfs, run, T
SWAPMOVE = {0: 1, 1: 0, 2: 4, 3: 5, 4: 2, 5: 3, 6: 10, 7: 11, 8: 12, 9: 13, 10: 6, 11: 7, 12: 8, 13: 9}
def sym_imgs(s):
    sw, sx, sy = s
    ix = [(2 if sw else 1) * sx]; iy = [(1 if sw else 2) * sy]
    return ix, iy
SYMS = [(sw, sx, sy) for sw in (0, 1) for sx in (1, -1) for sy in (1, -1)]
def compose(img_outer, img_inner):
    # (outer o inner)(g) = outer(inner(g))
    return {1: red(sub(img_inner[1], img_outer)), 2: red(sub(img_inner[2], img_outer))}
def bridge_relator(start, goal, k):
    # BFS over conjugations/inversion of relator k only (other relator untouched)
    moves = [k] + ([6, 7, 8, 9] if k == 0 else [10, 11, 12, 13])
    other = (1,) if k == 0 else (1,)
    q = deque([(tuple(start), [])]); seen = {tuple(start)}
    while q:
        w, p = q.popleft()
        if w == tuple(goal): return p
        if len(p) > len(start) + len(goal) + 2: continue
        for m in moves:
            st = (w, other) if k == 0 else (other, w)
            v = apply_move(st, m)[k]
            if len(v) <= max(len(start), len(goal)) + 2 and v not in seen:
                seen.add(v); q.append((v, p + [m]))
    return None
def transfer(R0, psi, T0, twin_path):
    R0 = [red(list(R0[0])), red(list(R0[1]))]
    for s in SYMS:
        ix, iy = sym_imgs(s)
        phi = compose({1: ix, 2: iy}, {1: psi[0], 2: psi[1]})
        u, v = inverse_auto(phi[1], phi[2])
        pinv = {1: u, 2: v}
        for swap in (0, 1):
            Ts = [T0[1], T0[0]] if swap else [T0[0], T0[1]]
            R1 = [red(sub(list(Ts[0]), pinv)), red(sub(list(Ts[1]), pinv))]
            if not all(cyc_forms(R1[k]) == cyc_forms(R0[k]) for k in (0, 1)):
                continue
            b0 = bridge_relator(R0[0], R1[0], 0); b1 = bridge_relator(R0[1], R1[1], 1)
            if b0 is None or b1 is None: continue
            P = [SWAPMOVE[m] for m in twin_path] if swap else list(twin_path)
            line = b0 + b1 + pull_back(P, pinv)
            s0 = (tuple(R0[0]), tuple(R0[1]))
            e = run(s0, line)
            f = finish_bfs(e, maxd=12, cap=2 * (len(u) + len(v)) + 4)
            if f is None: continue
            line += f
            if run(s0, line) == T: return line
    return None
