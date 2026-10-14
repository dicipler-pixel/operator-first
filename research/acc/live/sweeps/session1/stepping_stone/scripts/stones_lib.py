#!/usr/bin/env python3
"""Stepping-stone library (self-contained; only needs the official SAIR verifier checkout for final replay).

State = (r0, r1), tuples of ints (x=1, X=-1, y=2, Y=-2). Moves 0..13 = ac-r2-v1 (MOVES_MANUAL.md 1.2).
Store = every state on every held road (and, idea B, on every backward walk from the goal), keyed by its
normal form under the 16 symmetries (letter perm x<->y, invert x, invert y, swap relators), with its best
known tail (moves from that state to an end E in {(x,y), (y,x)}).  A searched state t whose normal form is
in the store gives a road: t --mmap(g, tail)--> g(E) --finish--> goal (or (y,x) for a Stable line)."""
import json
import os
import random
import sys
from collections import deque

GOAL = ((1,), (2,))
YX = ((2,), (1,))
INV = (0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12)
SYMS = [(p, sx, sy, rs) for p in (0, 1) for sx in (1, -1) for sy in (1, -1) for rs in (0, 1)]
CONJ = {6: (0, 1), 7: (0, -1), 8: (0, 2), 9: (0, -2), 10: (1, 1), 11: (1, -1), 12: (1, 2), 13: (1, -2)}
CONJ_INV = {v: k for k, v in CONJ.items()}
BASIC = {0: ("inv", 0), 1: ("inv", 1), 2: ("mul", 0, 1), 3: ("mulinv", 0, 1), 4: ("mul", 1, 0), 5: ("mulinv", 1, 0)}
BASIC_INV = {v: k for k, v in BASIC.items()}


def load_core(sair):
    sys.path.insert(0, os.path.join(sair, "competition/tools"))
    from verifier import core
    man = json.load(open(os.path.join(sair, "competition/tools/verifier/data/manifest.json")))
    return core, man


def rel_of(man):
    return {c["challenge_id"]: tuple(tuple(r) for r in c["initial_relators"]) for c in man["challenges"]}


# ---------------------------------------------------------------- fast moves (cross-checked vs core in selftest)
def inv(w):
    return tuple([-t for t in reversed(w)])


def cat(a, b):
    i, la, n = 0, len(a), min(len(a), len(b))
    while i < n and a[la - 1 - i] == -b[i]:
        i += 1
    return a[:la - i] + b[i:]


def conj(g, r):
    return cat(cat((g,), r), (-g,))


_G = (1, -1, 2, -2)


def apply(s, m):
    r0, r1 = s
    if m == 0:
        return (inv(r0), r1)
    if m == 1:
        return (r0, inv(r1))
    if m == 2:
        return (cat(r0, r1), r1)
    if m == 3:
        return (cat(r0, inv(r1)), r1)
    if m == 4:
        return (r0, cat(r1, r0))
    if m == 5:
        return (r0, cat(r1, inv(r0)))
    if m < 10:
        return (conj(_G[m - 6], r0), r1)
    return (r0, conj(_G[m - 10], r1))


def run(s, path):
    for m in path:
        s = apply(s, m)
    return s


def L(s):
    return len(s[0]) + len(s[1])


# ---------------------------------------------------------------- symmetries
def lmap(g, t):
    p, sx, sy, _ = g
    gen, sgn = abs(t), (1 if t > 0 else -1)
    sgn *= sx if gen == 1 else sy
    return sgn * ((3 - gen) if p else gen)


_LM = [{t: lmap(g, t) for t in (1, -1, 2, -2)} for g in SYMS]


def apply_g(gi, s):
    m = _LM[gi]
    a = tuple([m[t] for t in s[0]])
    b = tuple([m[t] for t in s[1]])
    return (b, a) if SYMS[gi][3] else (a, b)


def mmap(gi, mv):
    g = SYMS[gi]
    rs = g[3]
    if mv in CONJ:
        rel, c = CONJ[mv]
        return CONJ_INV[((1 - rel) if rs else rel, lmap(g, c))]
    b = BASIC[mv]
    if b[0] == "inv":
        return BASIC_INV[("inv", (1 - b[1]) if rs else b[1])]
    i, j = (1 - b[1], 1 - b[2]) if rs else (b[1], b[2])
    return BASIC_INV[(b[0], i, j)]


def enc(s):
    return bytes([a + 3 for a in s[0]]) + b"\x00" + bytes([a + 3 for a in s[1]])


_TR = []
for _gi in range(0, 16, 2):          # letter maps (rs=0 entries); relator swap handled by splitting
    _t = bytearray(range(256))
    for _a in (1, -1, 2, -2):
        _t[_a + 3] = lmap(SYMS[_gi], _a) + 3
    _TR.append(bytes(_t))


def norm(s):
    """symmetry normal form key (bytes): min over the 16 images (8 letter maps x relator swap)."""
    e = enc(s)
    best = None
    for tr in _TR:
        k = e.translate(tr)
        a, b = k.split(b"\x00")
        k2 = b + b"\x00" + a
        if k2 < k:
            k = k2
        if best is None or k < best:
            best = k
    return best


def norm_slow(s):
    return min(enc(apply_g(gi, s)) for gi in range(16))


_fin = {}


def finish(state, ends=(GOAL,), limit=8):
    """Shortest move list from a short state to one of `ends` (BFS, tiny states only)."""
    kk = (state, ends)
    if kk in _fin:
        return _fin[kk]
    seen, q = {state: []}, deque([state])
    res = None
    while q:
        s = q.popleft()
        if s in ends:
            res = seen[s]
            break
        if len(seen[s]) < limit:
            for m in range(14):
                t = apply(s, m)
                if t not in seen and L(t) <= 8:
                    seen[t] = seen[s] + [m]
                    q.append(t)
    _fin[kk] = res
    return res


# ---------------------------------------------------------------- road file
def read_roads(path):
    out = []
    for line in open(path):
        line = line.strip()
        if ":" not in line or line.startswith("#"):
            continue
        cid, rest = line.split(":", 1)
        try:
            mv = json.loads(rest)
        except Exception:
            continue
        out.append((cid.strip(), mv))
    return out


class Store:
    """norm key -> (tail_len, src_id, pos).  src: list of (start_state, moves, end_state).
    The tail of node at position pos of source i is moves[pos:], from state run(start, moves[:pos]) to end."""

    def __init__(self):
        self.d = {}
        self.src = []

    def add_path(self, start, moves, end, maxlen=10 ** 9):
        i = len(self.src)
        self.src.append((start, list(moves), end))
        s, n, added = start, len(moves), 0
        for pos in range(n + 1):
            if L(s) <= maxlen or pos == 0:
                k = norm(s)
                h = n - pos
                old = self.d.get(k)
                if old is None or old[0] > h:
                    if old is None:
                        added += 1
                    self.d[k] = (h, i, pos)
            if pos < n:
                s = apply(s, moves[pos])
        return added

    def add_halo(self, maxlen=40, src_hi=None):
        """Radius-1 halo: every 1-move neighbour c of a stored state b (from sources < src_hi) gets tail
        [INV[m]] + tail(b).  Entries use negative source ids into self.halo = [(i, pos, m)]."""
        if not hasattr(self, "halo"):
            self.halo = []
        src_hi = len(self.src) if src_hi is None else src_hi
        added = 0
        for i in range(src_hi):
            start, moves, end = self.src[i]
            s = start
            for pos in range(len(moves) + 1):
                if L(s) <= maxlen:
                    h0 = self.d.get(norm(s))
                    if h0 is not None and h0[1] == i and h0[2] == pos:       # only the best entry per class
                        for m in range(14):
                            c = apply(s, m)
                            if L(c) > maxlen + 2:
                                continue
                            k = norm(c)
                            if k not in self.d:
                                self.halo.append((i, pos, m))
                                self.d[k] = (len(moves) - pos + 1, -len(self.halo), 0)
                                added += 1
                if pos < len(moves):
                    s = apply(s, moves[pos])
        return added

    def get(self, t):
        return self.d.get(norm(t))

    def road_from(self, t, ends=(GOAL,)):
        """Reconstruct the shortest road from state t (whose norm is in the store) to one of ends."""
        h, i, pos = self.d[norm(t)]
        if i < 0:
            i, pos, m0 = self.halo[-i - 1]
            start, moves, end = self.src[i]
            b = apply(run(start, moves[:pos]), m0)
            tail = [INV[m0]] + moves[pos:]
        else:
            start, moves, end = self.src[i]
            b = run(start, moves[:pos])
            tail = moves[pos:]
        best = None
        for gi in range(16):
            if apply_g(gi, b) != t:
                continue
            p = [mmap(gi, m) for m in tail]
            e = apply_g(gi, end)
            f = finish(e, ends)
            if f is None:
                continue
            if best is None or len(p) + len(f) < len(best):
                best = p + f
        return best


def selftest(core, n=20000, seed=1):
    rng = random.Random(seed)
    s = ((1, 2, -1, -2, -2), (1, 1, 2, -1, -1, -1, -2))
    for _ in range(n):
        m = rng.randrange(14)
        a, b = apply(s, m), core.apply_move(s, m)
        assert a == b, (s, m, a, b)
        s = a if L(a) < 40 else s
    # symmetry move map: image of a path is the path of the image
    for _ in range(300):
        st = ((1, 2, 2, -1), (2, 1, -2, 1, 1))
        p = [rng.randrange(14) for _ in range(12)]
        for gi in range(16):
            assert apply_g(gi, run(st, p)) == run(apply_g(gi, st), [mmap(gi, m) for m in p])
    for _ in range(2000):
        st = run(((1, 2, 2, -1), (2, 1, -2, 1, 1)), [rng.randrange(14) for _ in range(15)])
        assert norm(st) == norm_slow(st)
    return True
