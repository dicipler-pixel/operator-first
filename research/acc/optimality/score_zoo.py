#!/usr/bin/env python3
"""Score zoo: a fast screen of cheap state scores against record-length AC paths, 2026-09-28.

Discovery, not proof.  Each candidate score f (lower = better unless the a-priori direction says "high") is judged by
where it ranks the move that a record-length path actually took among the 14 children of each path state.

Data: the paths that `p2_hump_test.py` collects and replays with the official verifier core (one shortest verified
path per row); "at record" = the path length equals the live board record (board snapshot in p2_hump_test.BOARD);
"hump" = at-record paths whose raw total climbs >= 6 above the start (the P2 test's set).

Per step: f on each of the 14 children; mid-rank of the record child (ties -> average rank).  Reported:
  top3        fraction of steps with mid-rank <= 3 (as in p2_hump_test; comparable to its 0.407 for (P2c8, P1m, raw))
  top3_exp    expected top-3 rate under a random tie-break (what a fingerprint tie-break does in the beam)
  mean_rank   mean mid-rank
on four step sets: hump paths all steps / climbing steps (raw total of the record child > current total), and
all at-record paths all steps / climbing steps.  Spearman rho of f(state) with moves remaining: pooled over every
state of every at-record path, and the mean within-path rho over hump paths.

Modes: 'prim' ranks by f alone; 'tb' ranks by (P2c8, f), i.e. f as the tie-break under P2 cut 8 (BEAM_P2=2 puts the
beam's existing key there); 'tb2' ranks by (P2c8, P1m, f, raw) (f after BEAM_P2=1's key); 'tb3' ranks by
(P2c8, f, P1m, raw) (f inserted between P2 and P1m); 'combo' = hand-built lexicographic keys, including the ledger's
K0 = (P2c8, P1m, raw) and the beam's current keys (P2, H) [BEAM_P2=2 BEAM_H=1] and (P2, P1m, H) [BEAM_P2=1 BEAM_H=1].
Step sets also split climbing steps into conjugation moves (6-13) and multiplication moves (2-5).  Every score is also run with
the opposite sign ('flip'; post hoc, flagged).  Paired path bootstrap (1000 resamples of hump paths) gives a 95% CI
for the climbing top-3 difference against the baselines.  Survival rule (the atlas ledger's rule, fixed there before
its run): tie-break climbing top3 >= (P2c8, P1m) + 0.05 and all-steps top3 >= (P2c8, P1m) - 0.02 on hump paths.

Class-level scores (functions of the unordered pair of cyclic classes up to rotation and inversion: P0cyc, P1, P2,
P3, WH, ...) give the same value to the parent class, so the 8 conjugation and 2 inversion children always tie; only
word-level scores (raw, P1m, H, L1, real2, ...) can separate them.

usage: nice -n 10 python3 score_zoo.py [--out JSON] [--quick N] [--no-expensive]
"""
import argparse, cmath, gzip, json, math, os, random, statistics, sys, time
from collections import Counter, defaultdict, deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import p2_hump_test as P  # noqa: E402  (path collection, replay, P1/P1m/P2 definitions)

REPO = P.REPO
OUT_DEFAULT = os.path.join(REPO, 'research/acc/live/ledger/score_zoo_20260928.json')
cycred_s, inv_s, free_reduce_s, canon, enc, tot = P.cycred_s, P.inv_s, P.free_reduce_s, P.canon, P.enc, P.tot


# ----------------------------------------------------------------------------- per-state context (lazy)
class Ctx:
    __slots__ = ('s', '_e', '_c', '_k', '_M')

    def __init__(self, s):
        self.s = s
        self._e = self._c = self._k = self._M = None

    def e(self):
        if self._e is None:
            self._e = (enc(self.s[0]), enc(self.s[1]))
        return self._e

    def c(self):
        if self._c is None:
            a, b = self.e()
            self._c = (cycred_s(a), cycred_s(b))
        return self._c

    def key(self):
        if self._k is None:
            a, b = self.c()
            ca, cb = canon(a), canon(b)
            self._k = (ca, cb) if ca <= cb else (cb, ca)
        return self._k

    def M(self):
        if self._M is None:
            self._M = P.exp_matrix(self.s)
        return self._M


_CTX = {}


def ctx_of(s):
    c = _CTX.get(s)
    if c is None:
        if len(_CTX) > 400000:
            _CTX.clear()
        c = _CTX[s] = Ctx(s)
    return c


# ----------------------------------------------------------------------------- helpers
def p2s(A, B, cut):
    """P2 (cyc variant) of cyclically reduced string cores, sharing p2_hump_test's memo."""
    ca, cb = canon(A), canon(B)
    key = ((ca, cb) if ca <= cb else (cb, ca), cut)
    r = P._P2.get(key)
    if r is None:
        cl, fl = P.level1(A, B, cut)
        r = (min(P.p1_cores(x, y)[0] for (_, _, x, y) in cl), min(P.p1_cores(x, y)[1] for (_, _, x, y) in fl))
        P._P2[key] = r
    return r[0]


def p3s(A, B, cut=8):
    cl, _ = P.level1(A, B, cut)
    return min(p2s(x, y, cut) for (_, _, x, y) in cl)


SHEARS = []
for _im in ({'a': 'ab', 'b': 'b'}, {'a': 'aB', 'b': 'b'}, {'a': 'ba', 'b': 'b'}, {'a': 'Ba', 'b': 'b'},
            {'a': 'a', 'b': 'ba'}, {'a': 'a', 'b': 'bA'}, {'a': 'a', 'b': 'ab'}, {'a': 'a', 'b': 'Ab'}):
    _im = dict(_im)
    _im['A'], _im['B'] = inv_s(_im['a']), inv_s(_im['b'])
    SHEARS.append(_im)


def shear(w, im):
    return cycred_s(free_reduce_s(''.join(im[ch] for ch in w)))


def wh_min(words):
    """Greedy steepest Whitehead descent of a tuple of cyclic words over the 8 rank-2 shears (Whitehead's peak
    reduction makes this reach the orbit minimum). Returns the reduced tuple."""
    cur = tuple(words)
    cl = sum(len(w) for w in cur)
    while True:
        best = None
        for im in SHEARS:
            nw = tuple(shear(w, im) for w in cur)
            L = sum(len(w) for w in nw)
            if L < cl:
                cl, best = L, nw
        if best is None:
            return cur
        cur = best


def xtype(ch):
    return ch in 'aA'


def cyc_runs(c):
    """(number of cyclic runs of equal letters, longest run)."""
    n = len(c)
    if n == 0:
        return 0, 0
    ch = sum(1 for i in range(n) if c[i] != c[i - 1])
    if ch == 0:
        return 1, n
    start = next(i for i in range(n) if c[i] != c[i - 1])
    best = run = 0
    for j in range(n):
        i = (start + j) % n
        run = run + 1 if j and c[i] == c[i - 1] else 1
        best = max(best, run)
    return ch, best


def syllables(c):
    n = len(c)
    return sum(1 for i in range(n) if xtype(c[i]) != xtype(c[i - 1])) if n else 0


def comm4(c):
    n = len(c)
    if n < 4:
        return 0
    k = 0
    for i in range(n):
        a, b, cc, d = c[i], c[(i + 1) % n], c[(i + 2) % n], c[(i + 3) % n]
        if xtype(a) != xtype(b) and cc == a.swapcase() and d == b.swapcase():
            k += 1
    return k


_TRIG = {}


def fourier_low(c):
    """(power of the x- and y-sign sequences at frequencies 1 and 2, total non-DC power)."""
    n = len(c)
    if n < 3:
        return 0.0, 0.0
    tb = _TRIG.get(n)
    if tb is None:
        tb = _TRIG[n] = [[cmath.exp(-2j * math.pi * k * i / n) for i in range(n)] for k in (1, 2)]
    low = tot_p = 0.0
    for pos, neg in (('a', 'A'), ('b', 'B')):
        seq = [1 if ch == pos else -1 if ch == neg else 0 for ch in c]
        for row in tb:
            z = sum(v * w for v, w in zip(seq, row) if v)
            low += (z.real * z.real + z.imag * z.imag) / n
        sm = sum(seq)
        tot_p += sum(1 for v in seq if v) - sm * sm / n
    return low, tot_p


def sym_order(c):
    n = len(c)
    if n == 0:
        return 0.0
    d, t = c + c, inv_s(c)
    dt = t + t
    distinct = {d[i:i + n] for i in range(n)} | {dt[i:i + n] for i in range(n)}
    return 2.0 * n / len(distinct)


def onesign(c):
    k = 0
    for pos, neg in (('a', 'A'), ('b', 'B')):
        if not (pos in c and neg in c):
            k += 1
    return k


def euclid(M):
    """Greedy count of row operations r_i <- r_i +- r_j that bring the exponent matrix to a signed permutation."""
    (a, b), (c, d) = M
    steps = 0
    while abs(a) + abs(b) + abs(c) + abs(d) > 2 and steps < 400:
        cur = abs(a) + abs(b) + abs(c) + abs(d)
        best = None
        for (na, nb, nc, nd) in ((a + c, b + d, c, d), (a - c, b - d, c, d), (a, b, c + a, d + b), (a, b, c - a, d - b)):
            v = abs(na) + abs(nb) + abs(nc) + abs(nd)
            if best is None or v < best[0]:
                best = (v, na, nb, nc, nd)
        if best[0] >= cur:
            break
        _, a, b, c, d = best
        steps += 1
    return steps


def hprio(s):
    """acc_beam.c hprio (BEAM_H=1, BAL=0): ACSolverX priority x16 on the stored words."""
    L = len(s[0]) + len(s[1])
    if not L:
        return 0
    K = MK = 0
    cnt, blk = [0, 0], [0, 0]
    for w in s:
        n = len(w)
        if not n:
            continue
        k = 0
        prev = 0 if abs(w[-1]) == 1 else 1
        for a in w:
            g = 0 if abs(a) == 1 else 1
            cnt[g] += 1
            if g != prev:
                k += 1
                blk[g] += 1
            prev = g
        if k == 0:
            blk[0 if abs(w[0]) == 1 else 1] += 1
        kr = k // 2
        K += kr
        MK = max(MK, kr)
    th = 0 if cnt[0] <= cnt[1] else 1
    S = cnt[th] / blk[th] if blk[th] else 0
    im = abs(cnt[0] - cnt[1]) / L
    return int((L + 2.53 * K + 6.418 * MK + 8.458 * S + 3.292 * im) * 16.0)


# ----------------------------------------------------------------------------- finite shadows
class SL2Probe:
    """SL(2,p) probe x->A, y->B with a fixed random generating pair; exact shadow BFS distance to (A, B)."""

    def __init__(self, p, rng):
        els = [(a, b, c, d) for a in range(p) for b in range(p) for c in range(p) for d in range(p)
               if (a * d - b * c) % p == 1]
        ix = {e: i for i, e in enumerate(els)}
        n = len(els)
        mm = lambda u, v: ((u[0] * v[0] + u[1] * v[2]) % p, (u[0] * v[1] + u[1] * v[3]) % p,
                           (u[2] * v[0] + u[3] * v[2]) % p, (u[2] * v[1] + u[3] * v[3]) % p)
        inv = [ix[(e[3], -e[1] % p, -e[2] % p, e[0])] for e in els]
        mul = [[ix[mm(els[i], els[j])] for j in range(n)] for i in range(n)]
        one = ix[(1, 0, 0, 1)]
        while True:
            A, B = rng.randrange(n), rng.randrange(n)
            seen, q = {one}, [one]
            while q:
                g = q.pop()
                for h in (A, B, inv[A], inv[B]):
                    u = mul[g][h]
                    if u not in seen:
                        seen.add(u)
                        q.append(u)
            if len(seen) == n:
                break
        self.p, self.n, self.A, self.B = p, n, els[A], els[B]
        self.img = {1: A, -1: inv[A], 2: B, -2: inv[B]}
        self.nxt = {a: [mul[g][self.img[a]] for g in range(n)] for a in (1, -1, 2, -2)}
        self.one = one
        cen = lambda v: v if v <= p // 2 else v - p
        self.frob = [math.sqrt((cen(e[0]) - 1) ** 2 + cen(e[1]) ** 2 + cen(e[2]) ** 2 + (cen(e[3]) - 1) ** 2) for e in els]
        order = []
        for i in range(n):
            g, k = i, 1
            while g != one:
                g, k = mul[g][i], k + 1
            order.append(k)
        self.order = order
        cons = [A, inv[A], B, inv[B]]
        conj = [[mul[mul[c][i]][inv[c]] for i in range(n)] for c in cons]
        dist = bytearray([255]) * (n * n)
        t = A * n + B
        dist[t] = 0
        dq = deque([t])
        while dq:
            s = dq.popleft()
            a, b = divmod(s, n)
            d = dist[s] + 1
            ia, ib = inv[a], inv[b]
            for u in (ia * n + b, a * n + ib, mul[a][b] * n + b, mul[a][ib] * n + b, a * n + mul[b][a],
                      a * n + mul[b][ia], conj[0][a] * n + b, conj[1][a] * n + b, conj[2][a] * n + b,
                      conj[3][a] * n + b, a * n + conj[0][b], a * n + conj[1][b], a * n + conj[2][b], a * n + conj[3][b]):
                if dist[u] == 255:
                    dist[u] = d
                    dq.append(u)
        self.dist = dist
        self.diameter = max(v for v in dist if v != 255)

    def word(self, w):
        g = self.one
        nx = self.nxt
        for a in w:
            g = nx[a][g]
        return g


class SnProbe:
    """Random permutation representation into S_7 (B95 cycle types); table-walk images."""

    def __init__(self, k, rng):
        while True:
            X = list(range(k))
            Y = list(range(k))
            rng.shuffle(X)
            rng.shuffle(Y)
            # transitive?
            seen, q = {0}, [0]
            while q:
                i = q.pop()
                for j in (X[i], Y[i]):
                    if j not in seen:
                        seen.add(j)
                        q.append(j)
            if len(seen) == k:
                break
        inv = lambda p: tuple(sorted(range(k), key=lambda i: p[i]))
        gens = {1: tuple(X), -1: inv(tuple(X)), 2: tuple(Y), -2: inv(tuple(Y))}
        ident = tuple(range(k))
        idx, els, q = {ident: 0}, [ident], [ident]
        nxt = {a: [] for a in gens}
        i = 0
        while i < len(els):
            g = els[i]
            for a, h in gens.items():
                u = tuple(h[g[t]] for t in range(k))   # apply g then h (right action on the word)
                if u not in idx:
                    idx[u] = len(els)
                    els.append(u)
                nxt[a].append(idx[u])
            i += 1
        self.nxt = nxt
        self.ct = [self.cycle_type(g) for g in els]
        self.target = sorted([self.ct[nxt[1][0]], self.ct[nxt[2][0]]])

    @staticmethod
    def cycle_type(g):
        seen, out = set(), []
        for i in range(len(g)):
            if i in seen:
                continue
            L, j = 0, i
            while j not in seen:
                seen.add(j)
                j = g[j]
                L += 1
            out.append(L)
        return tuple(sorted(out))

    def word(self, w):
        g = 0
        nx = self.nxt
        for a in w:
            g = nx[a][g]
        return g

    def mismatch(self, s):
        got = [self.ct[self.word(s[0])], self.ct[self.word(s[1])]]
        t = list(self.target)
        m = 0
        for x in got:
            if x in t:
                t.remove(x)
            else:
                m += 1
        return m


PROBES_SL2, PROBES_SN = [], []


def init_probes(seed=20260928):
    rng = random.Random(seed)
    for p in (5, 5, 5, 7, 7, 7):
        PROBES_SL2.append(SL2Probe(p, rng))
    for _ in range(3):
        PROBES_SN.append(SnProbe(7, rng))


# ----------------------------------------------------------------------------- scores
# (name, fn(ctx, start_ctx), level, a-priori direction, atlas source, expensive)
def _lens(c):
    return len(c.s[0]), len(c.s[1])



# realization distance: how many non-multiplication moves (inversions 0-1, conjugations 6-13) before one literal
# multiplication lands in a level-1 class that P2 (resp. P1) promises.  Word-level; breaks the P2 plateau among
# conjugation children by "which rotation walks toward the promised product".
_MK = {}
NONMULT = (0, 1, 6, 7, 8, 9, 10, 11, 12, 13)


def mult_keys(s):
    v = _MK.get(s)
    if v is None:
        v = _MK[s] = frozenset(ctx_of(P.apply_move(s, m)).key() for m in (2, 3, 4, 5))
    return v


_TG = {}


def targets(c, which):
    k = (c.key(), which)
    v = _TG.get(k)
    if v is None:
        A, B = c.c()
        cl, _ = P.level1(A, B, 8)
        if which == 2:
            vals = [(P.p1_cores(x, y)[0], key) for (_, key, x, y) in cl]
        else:
            vals = [(t, key) for (t, key, _, _) in cl]
        best = min(t for t, _ in vals)
        v = _TG[k] = frozenset(key for t, key in vals if t == best)
    return v


def realize(c, which, depth):
    T = targets(c, which)
    frontier, seen = [c.s], {c.s}
    for d in range(depth + 1):
        for s in frontier:
            if mult_keys(s) & T:
                return d
        if d == depth:
            break
        nf = []
        for s in frontier:
            for m in NONMULT:
                u = P.apply_move(s, m)
                if u not in seen:
                    seen.add(u)
                    nf.append(u)
        frontier = nf
    return depth + 1


_L1, _L2 = {}, {}


def l1_memo(s):
    v = _L1.get(s)
    if v is None:
        v = _L1[s] = min(tot(P.apply_move(s, j)) for j in range(14))
    return v


def l2_memo(s):
    v = _L2.get(s)
    if v is None:
        v = _L2[s] = min(l1_memo(P.apply_move(s, j)) for j in range(14))
    return v


def f_L1(c, st):
    """true one-move lookahead: min total over the 14 children (actual moves, no free rotations)"""
    return l1_memo(c.s)


def f_L2(c, st):
    """true two-move lookahead: min total over all 14 x 14 continuations"""
    return l2_memo(c.s)


def f_L3(c, st):
    """true three-move lookahead: min total over all 14^3 continuations (memoised L2 of the children)"""
    return min(l2_memo(P.apply_move(c.s, j)) for j in range(14))


# symmetry / "cage" scores: the 8 signed letter permutations of {x, y}
LETTER_PERMS = []
for _sw in (False, True):
    for _sx in (1, -1):
        for _sy in (1, -1):
            _ix = ('b' if _sw else 'a') if _sx == 1 else ('B' if _sw else 'A')
            _iy = ('a' if _sw else 'b') if _sy == 1 else ('A' if _sw else 'B')
            LETTER_PERMS.append(str.maketrans({'a': _ix, 'A': _ix.swapcase(), 'b': _iy, 'B': _iy.swapcase()}))


def cage_n(c, st):
    """number of signed letter permutations sigma with sigma(r0) ~ r1^{+-1} up to rotation"""
    A, B = c.c()
    cb = canon(B)
    return sum(1 for t in LETTER_PERMS if canon(A.translate(t)) == cb)


def stab(c, st):
    """number of signed letter permutations that map the unordered pair of classes to itself (>= 1)"""
    A, B = c.c()
    k = c.key()
    n = 0
    for t in LETTER_PERMS:
        a, b = canon(A.translate(t)), canon(B.translate(t))
        if ((a, b) if a <= b else (b, a)) == k:
            n += 1
    return n


def selfsym(c, st):
    """sum over relators of the number of non-identity sigma with sigma(r) ~ r^{+-1} up to rotation"""
    n = 0
    for w in c.c():
        cw = canon(w)
        n += sum(1 for t in LETTER_PERMS if canon(w.translate(t)) == cw) - 1
    return n


def self_inv(c, st):
    """relators equal to their own inverse up to rotation (a free-group theorem says never, unless empty)"""
    n = 0
    for w in c.c():
        if w:
            d = w + w
            if inv_s(w) in d:
                n += 1
    return n


def f_branch(c, st):
    s = c.s
    L = tot(s)
    return sum(1 for j in range(14) if tot(P.apply_move(s, j)) <= L)


def f_litcancel(c, st):
    s = c.s
    L = tot(s)
    return max((L - tot(P.apply_move(s, j))) / 2.0 for j in (2, 3, 4, 5))


def f_ovl(c, st):
    A, B = c.c()
    return max(P.lcs_cyc(A, inv_s(B)), P.lcs_cyc(A, B))


def f_ovl_ratio(c, st):
    A, B = c.c()
    m = min(len(A), len(B))
    return f_ovl(c, st) / m if m else 0.0


def f_self_ovl(c, st):
    return max(P.lcs_cyc(w, inv_s(w)) for w in c.c())


def f_comm_len(c, st):
    a, b = c.e()
    return len(cycred_s(free_reduce_s(a + b + inv_s(a) + inv_s(b))))


def f_wh(c, st):
    return sum(len(w) for w in wh_min(c.c()))


def f_p2wh(c, st):
    A, B = wh_min(c.c())
    return p2s(A, B, 8)


def f_wh1(c, st):
    return min(len(wh_min((w,))[0]) for w in c.c())


def f_prim(c, st):
    return sum(1 for w in c.c() if len(wh_min((w,))[0]) == 1)


def f_fourier(c, st):
    return sum(fourier_low(w)[0] for w in c.c())


def f_fourier_frac(c, st):
    lo = tp = 0.0
    for w in c.c():
        a, b = fourier_low(w)
        lo += a
        tp += b
    return lo / tp if tp > 1e-9 else 1.0


def f_entropy(c, st):
    cnt = Counter(''.join(c.c()))
    n = sum(cnt.values())
    return -sum(v / n * math.log2(v / n) for v in cnt.values()) if n else 0.0


def f_bigrams(c, st):
    out = set()
    for w in c.c():
        n = len(w)
        for i in range(n):
            out.add(w[i - 1] + w[i])
    return len(out)


def f_tclass(c, st):
    cls = P.classify_T(st.M(), c.M())
    return {'pmI': 0, 'finite': 1, 'parabolic': 2, 'hyperbolic': 3}[cls]


def f_sh_dist(c, st):
    s = c.s
    return sum(pr.dist[pr.word(s[0]) * pr.n + pr.word(s[1])] for pr in PROBES_SL2)


def f_sh_frob(c, st):
    s = c.s
    return sum(pr.frob[pr.word(s[0])] + pr.frob[pr.word(s[1])] for pr in PROBES_SL2) / len(PROBES_SL2)


def f_sh_order(c, st):
    s = c.s
    return sum(pr.order[pr.word(s[0])] + pr.order[pr.word(s[1])] for pr in PROBES_SL2)


def f_sn_ct(c, st):
    return sum(pr.mismatch(c.s) for pr in PROBES_SN)


SWAPXY = str.maketrans({'a': 'b', 'A': 'B', 'b': 'a', 'B': 'A'})


def f_p2mir(c, st):
    """two-sided P2 (item 14): min of P2c8 of the state and of its x<->y mirror.  P2 without a cut is mirror
    invariant; P2c8 is not quite, because the level-1 cut breaks total-length ties by canonical string."""
    A, B = c.c()
    return min(p2s(A, B, 8), p2s(A.translate(SWAPXY), B.translate(SWAPXY), 8))


def f_p1m_2side(c, st):
    s = c.s
    return min(P.p1m(*s), P.p1m(P.invert(s[0]), P.invert(s[1])))


SCORES = [
    # baselines / references
    ('raw', lambda c, st: tot(c.s), 'word', 'low', 'baseline', False),
    ('P0cyc', lambda c, st: sum(len(w) for w in c.c()), 'class', 'low', 'Plate XII rung 1', False),
    ('P1', lambda c, st: P.p1_cores(*c.c())[0], 'class', 'low', 'Plate XII rung 2', False),
    ('P1m', lambda c, st: P.p1m(*c.s), 'word', 'low', 'baseline', False),
    ('P2c8', lambda c, st: p2s(*c.c(), 8), 'class', 'low', 'B31 baseline', False),
    ('H', lambda c, st: hprio(c.s), 'word', 'low', 'beam BEAM_H=1 key (P2=2 second key)', False),
    # 1 lengths [E1, B6]
    ('len_min', lambda c, st: min(_lens(c)), 'word', 'low', 'E1', False),
    ('len_max', lambda c, st: max(_lens(c)), 'word', 'low', 'E1', False),
    ('len_bal', lambda c, st: abs(len(c.s[0]) - len(c.s[1])), 'word', 'low', 'B6', False),
    ('len_ratio', lambda c, st: min(_lens(c)) / max(1, max(_lens(c))), 'word', 'high', 'B20 ratio', False),
    ('cyc_min', lambda c, st: min(len(w) for w in c.c()), 'class', 'low', 'E1', False),
    ('cyc_max', lambda c, st: max(len(w) for w in c.c()), 'class', 'low', 'E1', False),
    ('cyc_bal', lambda c, st: abs(len(c.c()[0]) - len(c.c()[1])), 'class', 'low', 'B6', False),
    # 2 Whitehead frame [B83]
    ('WH', f_wh, 'class', 'low', 'B83 matched frame', False),
    # 3/17 overlap [GEO-OVERLAP, B20]
    ('ovl', f_ovl, 'class', 'high', 'GEO-OVERLAP', False),
    ('ovl_ratio', f_ovl_ratio, 'class', 'high', 'B20/B19 ratio', False),
    ('self_ovl', f_self_ovl, 'class', 'high', 'transport/overlap', False),
    # 4 syllables [B95]
    ('syll', lambda c, st: sum(syllables(w) for w in c.c()), 'class', 'low', 'B95 cycle type', False),
    # 5/19 exponent matrix [B13, C1, UPG-GAP-RANK, B66]
    ('tr_abs', lambda c, st: abs(c.M()[0][0] + c.M()[1][1]), 'class', 'low', 'B13/B51 trace', False),
    ('offdiag', lambda c, st: abs(c.M()[0][1]) + abs(c.M()[1][0]), 'class', 'low', 'UPG-GAP-RANK', False),
    ('abel_mass', lambda c, st: sum(abs(v) for r in c.M() for v in r) - 2, 'class', 'low', 'UPG-GAP-RANK', False),
    ('abel_euclid', lambda c, st: euclid(c.M()), 'class', 'low', 'UPG-GAP-RANK', False),
    ('T_class', f_tclass, 'class', 'low', 'B13/C1 transfer class vs start', False),
    ('det_neg', lambda c, st: 1 if (c.M()[0][0] * c.M()[1][1] - c.M()[0][1] * c.M()[1][0]) < 0 else 0, 'class', 'low',
     'B66 orientation sheet', False),
    # 6 runs [periodicity eye]
    ('maxrun', lambda c, st: max(cyc_runs(w)[1] for w in c.c()), 'class', 'high', 'periodicity eye', False),
    ('nruns', lambda c, st: sum(cyc_runs(w)[0] for w in c.c()), 'class', 'low', 'periodicity eye', False),
    # 7 commutator load [hump_features, B2]
    ('comm4', lambda c, st: sum(comm4(w) for w in c.c()), 'class', 'low', 'hump_features / B2', False),
    ('comm_len', f_comm_len, 'word', 'low', 'B2 [r0,r1]', False),
    # 8 Fourier [OPT-TWO-FREQUENCY]
    ('fourier_low', f_fourier, 'class', 'low', 'OPT-TWO-FREQUENCY', False),
    ('fourier_frac', f_fourier_frac, 'class', 'high', 'OPT-TWO-FREQUENCY', False),
    # 9 symmetry [B6, B87]
    ('sym_order', lambda c, st: sum(sym_order(w) for w in c.c()), 'class', 'high', 'B6/B87 protected degeneracy', False),
    # 10 primitive-likeness [Plate XVIII]
    ('onesign', lambda c, st: sum(onesign(w) for w in c.c()), 'class', 'high', 'Plate XVIII prefilter', False),
    ('n_prim', f_prim, 'class', 'high', 'Plate XVIII primitive finish', False),
    ('wh1_min', f_wh1, 'class', 'low', 'Plate XVIII / B83', False),
    # 11 finite shadows [OBS-PROBE-SPAN, B95]
    ('sh_dist', f_sh_dist, 'word', 'low', 'OBS-PROBE-SPAN (exact shadow distance)', False),
    ('sh_frob', f_sh_frob, 'word', 'low', 'OBS-PROBE-SPAN (|img - I|_F)', False),
    ('sh_order', f_sh_order, 'word', 'low', 'OBS-PROBE-SPAN (element orders)', False),
    ('sn_ct', f_sn_ct, 'class', 'low', 'B95 S7 cycle types', False),
    # 12/13/14 ladder and frames
    ('P3c8', lambda c, st: p3s(*c.c()), 'class', 'low', 'Plate XII P3', True),
    ('P2wh', f_p2wh, 'class', 'low', 'B83 + B31', False),
    ('P2mir', f_p2mir, 'class', 'low', 'B81 mirror transport (two-sided P2)', False),
    ('P1m_2side', f_p1m_2side, 'word', 'low', 'B81 mirror (reversal)', False),
    # 15/16/18 rails, branching, growth
    ('gap', lambda c, st: tot(c.s) - p2s(*c.c(), 8), 'word', 'high', 'B96 gap between rails', False),
    ('p12gain', lambda c, st: P.p1_cores(*c.c())[0] - p2s(*c.c(), 8), 'class', 'high', 'Plate XII rung gain', False),
    ('branch', f_branch, 'word', 'high', 'B17 overflow', False),
    ('growth', lambda c, st: tot(c.s) / tot(st.s), 'word', 'low', 'B19', False),
    # 20 extras from METHOD/DIAGNOSTIC lines
    ('conj_debt', lambda c, st: tot(c.s) - sum(len(w) for w in c.c()), 'word', 'low', 'Plate XIV / B57 zero-length moves', False),
    ('nonred', lambda c, st: sum(1 for w, cw in zip(c.e(), c.c()) if len(w) != len(cw)), 'word', 'low', 'Plate XIV', False),
    ('L1', f_L1, 'word', 'low', 'true 1-move lookahead (BEAM_LOOK)', False),
    ('L2', f_L2, 'word', 'low', 'true 2-move lookahead (14^2)', False),
    ('L3', f_L3, 'word', 'low', 'true 3-move lookahead (14^3)', True),
    ('real2_d0', lambda c, st: realize(c, 2, 0), 'word', 'low', 'a literal product lands in a P2-promised class now', False),
    ('real2_d1', lambda c, st: realize(c, 2, 1), 'word', 'low', 'moves to realise the P2 promise (depth 1)', False),
    ('cage', lambda c, st: 1 if cage_n(c, st) else 0, 'class', 'low', 'lead: symmetric "cage" states (r1 ~ sigma(r0))', False),
    ('cage_n', cage_n, 'class', 'low', 'lead: cage symmetry count', False),
    ('stab', stab, 'class', 'low', 'lead: stabiliser of the class pair under the 8 letter mirrors', False),
    ('selfsym', selfsym, 'class', 'low', 'lead: self-symmetries of each relator', False),
    ('self_inv', self_inv, 'class', 'low', 'lead: relator ~ own inverse', False),
    ('real2_d2', lambda c, st: realize(c, 2, 2), 'word', 'low', 'B31 + Plate XIV: moves to realise the P2 promise', False),
    ('real2_d3', lambda c, st: realize(c, 2, 3), 'word', 'low', 'B31 + Plate XIV: moves to realise the P2 promise', True),
    ('real1_d2', lambda c, st: realize(c, 1, 2), 'word', 'low', 'moves to realise the P1 (best single product)', False),
    ('lit_cancel', f_litcancel, 'word', 'high', 'B20 cancellation available now', False),
    ('xy_imb', lambda c, st: abs(sum(len([a for a in w if abs(a) == 1]) for w in c.s) -
                                 sum(len([a for a in w if abs(a) == 2]) for w in c.s)) / max(1, tot(c.s)),
     'word', 'low', 'B69 x-mass', False),
    ('entropy', f_entropy, 'class', 'low', 'B6 entropy', False),
    ('bigrams', f_bigrams, 'class', 'low', 'B95 / periodicity', False),
]
SC_NAMES = [x[0] for x in SCORES]
SC = {x[0]: x for x in SCORES}
MEMO = {x[0]: {} for x in SCORES}


def value(name, c, st):
    _, fn, level, _, _, _ = SC[name]
    if name in ('T_class', 'growth'):
        return fn(c, st)
    m = MEMO[name]
    k = c.key() if level == 'class' else c.s
    v = m.get(k)
    if v is None:
        v = m[k] = fn(c, st)
    return v


# ----------------------------------------------------------------------------- statistics
def mid(keys, i):
    v = keys[i]
    b = sum(1 for x in keys if x < v)
    t = sum(1 for x in keys if x == v)
    return 1 + b + (t - 1) / 2.0, min(1.0, max(0.0, (3 - b) / t))


def rankdata(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    r = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        for k in range(i, j + 1):
            r[order[k]] = (i + j) / 2.0 + 1
        i = j + 1
    return r


def spearman(xs, ys):
    if len(xs) < 3:
        return None
    rx, ry = rankdata(xs), rankdata(ys)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    sxy = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    sxx = sum((a - mx) ** 2 for a in rx)
    syy = sum((b - my) ** 2 for b in ry)
    if sxx <= 0 or syy <= 0:
        return None
    return sxy / math.sqrt(sxx * syy)


def rnd(x, d=3):
    return None if x is None else round(x, d)


# ----------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sair', default=P.SAIR_DEFAULT)
    ap.add_argument('--out', default=OUT_DEFAULT)
    ap.add_argument('--quick', type=int, default=0, help='use only the first N at-record paths (testing)')
    ap.add_argument('--no-expensive', action='store_true')
    ap.add_argument('--boot', type=int, default=1000)
    args = ap.parse_args()
    T0 = time.time()
    official = P.load_official(args.sair)
    man = {c['challenge_id']: c['initial_relators']
           for c in json.load(open(os.path.join(args.sair, 'competition/tools/verifier/data/manifest.json')))['challenges']}
    board = {c['challengeId']: c['currentBestLength'] for c in json.load(gzip.open(P.BOARD))['data']['items']}
    rows_all, collection, bad = P.collect_rows(official, man, board)
    at_rec = [p for p in rows_all if p['at_record']]
    if args.quick:
        at_rec = at_rec[:args.quick]
    for p in at_rec:
        p['hump'] = max(p['raw']) - p['raw'][0] >= 6
    humps = [p for p in at_rec if p['hump']]
    print('collected', collection, 'at record', len(at_rec), 'hump', len(humps), round(time.time() - T0, 1), flush=True)
    init_probes()
    print('probes', [(pr.p, pr.n, pr.diameter) for pr in PROBES_SL2], round(time.time() - T0, 1), flush=True)

    expensive = {n for n in SC_NAMES if SC[n][5]}
    # ---- per-score timing on 150 random child states (fresh memo, fresh ctx)
    rng = random.Random(5)
    pool = []
    for p in at_rec:
        for s in p['states'][:-1]:
            pool.append((s, p['states'][0]))
    rng.shuffle(pool)
    timing = {}
    samp = pool[:150]
    for nm in SC_NAMES:
        if nm in expensive and args.no_expensive:
            continue
        fn = SC[nm][1]
        ts = []
        for s, s0 in samp:
            kid = P.apply_move(s, rng.randrange(14))
            P._P2.clear()
            P._P1.clear()
            _L1.clear()
            _L2.clear()
            _MK.clear()
            _TG.clear()
            c, st = Ctx(kid), Ctx(s0)
            t = time.perf_counter()
            fn(c, st)
            ts.append(time.perf_counter() - t)
        timing[nm] = {'ms_median': rnd(1000 * statistics.median(ts), 3), 'ms_mean': rnd(1000 * sum(ts) / len(ts), 3),
                      'ms_p90': rnd(1000 * sorted(ts)[int(0.9 * len(ts))], 3)}
    P._P2.clear()
    P._P1.clear()
    _L1.clear()
    _L2.clear()
    print('timing', {k: v['ms_median'] for k, v in timing.items()}, round(time.time() - T0, 1), flush=True)

    # ---- mirror check (item 14): P2 of the x<->y swapped state
    mir_bad = 0
    for s, _ in pool[:200]:
        sw = (tuple(2 * (a // abs(a)) if abs(a) == 1 else a // abs(a) for a in s[0]),
              tuple(2 * (a // abs(a)) if abs(a) == 1 else a // abs(a) for a in s[1]))
        if p2s(*ctx_of(s).c(), 8) != p2s(*Ctx(sw).c(), 8):
            mir_bad += 1
    mirror = {'states': min(200, len(pool)), 'P2c8_differs_under_xy_swap': mir_bad,
              'note': 'P2 without a cut is invariant under the 16 letter mirrors (length and cyclic overlap are); P2c8 '
                      'differs only through the cut tie-break by canonical string. Item 14 is scored as P2mir = '
                      'min(P2c8(s), P2c8(swap s)); the reversal mirror is scored on the word-level P1m (P1m_2side).'}
    print('mirror', mirror, flush=True)

    # ---- values on every child of every at-record path step, and on the path states
    steps = []
    path_vals = []
    active = [n for n in SC_NAMES if not (n in expensive and args.no_expensive)]
    for pi, p in enumerate(at_rec):
        _L1.clear()          # path-local lookahead / realisation memos (bounded memory)
        _L2.clear()
        _MK.clear()
        st = ctx_of(p['states'][0])
        names_here = active if p['hump'] else [n for n in active if n not in expensive]
        pv = {n: [] for n in names_here}
        for s in p['states']:
            c = ctx_of(s)
            for n in names_here:
                pv[n].append(value(n, c, st))
        path_vals.append({'row': p['row'], 'hump': p['hump'], 'N': len(p['moves']), 'record': p['record'],
                          'states': p['states'] if p['hump'] else None, 'vals': pv})
        for t, m in enumerate(p['moves']):
            s = p['states'][t]
            kids = [ctx_of(P.apply_move(s, j)) for j in range(14)]
            vals = {n: [value(n, k, st) for k in kids] for n in names_here}
            steps.append({'row': p['row'], 'pi': pi, 't': t, 'N': len(p['moves']), 'move': m, 'hump': p['hump'],
                          'climb': vals['raw'][m] > tot(s), 'vals': vals})
        for n in ('L3', 'L2', 'L1', 'real2_d0', 'real2_d1', 'real2_d2', 'real2_d3', 'real1_d2', 'R1', 'R2'):
            if n in MEMO:
                MEMO[n].clear()  # word-level memos keyed by state; not reused across paths
        if pi % 20 == 0:
            print('  path', pi, p['row'], 'hump' if p['hump'] else '', len(steps), round(time.time() - T0, 1), flush=True)
    print('values done', len(steps), round(time.time() - T0, 1), flush=True)

    # ---- ranks.  A config is a lexicographic key: a list of (score, sign) components.
    def keyvec(r, comps):
        v = r['vals']
        if any(n not in v for n, _ in comps):
            return None
        cols = [[sg * x for x in v[n]] for n, sg in comps]
        return list(zip(*cols))

    configs = {}   # cid -> (comps, meta)
    for n in active:
        for sg, tag in ((1, 'low'), (-1, 'high')):
            flip = tag != SC[n][3]
            meta = {'score': n, 'direction': tag, 'flipped_post_hoc': flip}
            configs['%s|%s|prim' % (n, tag)] = ([(n, sg)], dict(meta, mode='prim', key='f'))
            configs['%s|%s|tb' % (n, tag)] = ([('P2c8', 1), (n, sg)], dict(meta, mode='tb', key='(P2c8, f)'))
            configs['%s|%s|tb2' % (n, tag)] = ([('P2c8', 1), ('P1m', 1), (n, sg), ('raw', 1)],
                                               dict(meta, mode='tb2', key='(P2c8, P1m, f, raw)'))
            configs['%s|%s|tb3' % (n, tag)] = ([('P2c8', 1), (n, sg), ('P1m', 1), ('raw', 1)],
                                               dict(meta, mode='tb3', key='(P2c8, f, P1m, raw)'))
    COMBOS = {
        'K0 (P2,P1m,raw)': [('P2c8', 1), ('P1m', 1), ('raw', 1)],
        '(P2,P1m)': [('P2c8', 1), ('P1m', 1)],
        'beam P2=2 H: (P2,H)': [('P2c8', 1), ('H', 1)],
        'beam P2=1 H: (P2,P1m,H)': [('P2c8', 1), ('P1m', 1), ('H', 1)],
        '(P2,real2_d2,P1m,H)': [('P2c8', 1), ('real2_d2', 1), ('P1m', 1), ('H', 1)],
        '(P2,real2_d1,P1m,H)': [('P2c8', 1), ('real2_d1', 1), ('P1m', 1), ('H', 1)],
        '(P2,comm_len,P1m,H)': [('P2c8', 1), ('comm_len', 1), ('P1m', 1), ('H', 1)],
        '(P2,real2_d2,comm_len,P1m,raw)': [('P2c8', 1), ('real2_d2', 1), ('comm_len', 1), ('P1m', 1), ('raw', 1)],
        '(P2,real2_d1,comm_len,P1m,raw)': [('P2c8', 1), ('real2_d1', 1), ('comm_len', 1), ('P1m', 1), ('raw', 1)],
        '(P2,real2_d2,L2,P1m,raw)': [('P2c8', 1), ('real2_d2', 1), ('L2', 1), ('P1m', 1), ('raw', 1)],
        '(P2,real2_d3,comm_len,P1m,raw)': [('P2c8', 1), ('real2_d3', 1), ('comm_len', 1), ('P1m', 1), ('raw', 1)],
        '(P2,L2,comm_len,P1m,raw)': [('P2c8', 1), ('L2', 1), ('comm_len', 1), ('P1m', 1), ('raw', 1)],
        '(P2,L3,P1m,raw)': [('P2c8', 1), ('L3', 1), ('P1m', 1), ('raw', 1)],
        '(L2,P2,P1m,raw)': [('L2', 1), ('P2c8', 1), ('P1m', 1), ('raw', 1)],
        '(L3,P2,P1m,raw)': [('L3', 1), ('P2c8', 1), ('P1m', 1), ('raw', 1)],
        '(P2,cage,P1m,raw)': [('P2c8', 1), ('cage', 1), ('P1m', 1), ('raw', 1)],
    }
    for nm, comps in COMBOS.items():
        if all(n in active for n, _ in comps):
            configs['combo|' + nm] = (comps, {'score': nm, 'direction': 'as listed', 'flipped_post_hoc': False,
                                              'mode': 'combo', 'key': nm})
    is_conj = lambda r: r['move'] >= 6
    is_mult = lambda r: 2 <= r['move'] <= 5
    sets = {'hump_all': lambda r: r['hump'], 'hump_climb': lambda r: r['hump'] and r['climb'],
            'hump_climb_conj': lambda r: r['hump'] and r['climb'] and is_conj(r),
            'hump_climb_mult': lambda r: r['hump'] and r['climb'] and is_mult(r),
            'rec_all': lambda r: True, 'rec_climb': lambda r: r['climb'],
            'rec_climb_conj': lambda r: r['climb'] and is_conj(r), 'rec_climb_mult': lambda r: r['climb'] and is_mult(r)}
    step_sets = [[k for k, sel in sets.items() if sel(r)] for r in steps]
    res = {}
    perpath = {}   # config -> {pi: [hits_climb, n_climb, hits_all, n_all]} on hump steps
    for cid, (comps, meta) in configs.items():
        acc = {k: [0, 0.0, 0.0, 0.0] for k in sets}
        pp = defaultdict(lambda: [0.0, 0, 0.0, 0])
        for r, ks in zip(steps, step_sets):
            kv = keyvec(r, comps)
            if kv is None:
                continue
            mr, te = mid(kv, r['move'])
            hit = 1.0 if mr <= 3 else 0.0
            for k in ks:
                a = acc[k]
                a[0] += 1
                a[1] += hit
                a[2] += te
                a[3] += mr
            if r['hump']:
                e = pp[r['pi']]
                e[2] += hit
                e[3] += 1
                if r['climb']:
                    e[0] += hit
                    e[1] += 1
        res[cid] = dict(meta, **{k: ({'steps': a[0], 'top3': rnd(a[1] / a[0]), 'top3_exp': rnd(a[2] / a[0]),
                                      'mean_rank': rnd(a[3] / a[0])} if a[0] else None) for k, a in acc.items()})
        perpath[cid] = dict(pp)
    print('ranks done', len(configs), round(time.time() - T0, 1), flush=True)

    # ---- paired path bootstrap vs baselines on hump steps
    hump_pis = sorted({r['pi'] for r in steps if r['hump']})
    brng = random.Random(99)
    boots = [[brng.choice(hump_pis) for _ in hump_pis] for _ in range(args.boot)]
    base_ids = {'raw': 'raw|low|prim', 'P1m': 'P1m|low|prim', 'P2c8': 'P2c8|low|prim',
                'P2c8>P1m': 'combo|(P2,P1m)', 'K0 P2c8>P1m>raw': 'combo|K0 (P2,P1m,raw)',
                'beam P2=2 H': 'combo|beam P2=2 H: (P2,H)', 'beam P2=1 H': 'combo|beam P2=1 H: (P2,P1m,H)'}

    def agg(cid, sample, which):
        pp = perpath[cid]
        h = nn = 0.0
        for pi in sample:
            e = pp.get(pi)
            if e:
                if which == 'climb':
                    h += e[0]
                    nn += e[1]
                else:
                    h += e[2]
                    nn += e[3]
        return h / nn if nn else 0.0

    def boot_delta(cid, bid, which):
        ds = sorted(agg(cid, b, which) - agg(bid, b, which) for b in boots)
        return [rnd(ds[int(0.025 * len(ds))]), rnd(ds[int(0.975 * len(ds)) - 1])]

    K0 = res[base_ids['K0 P2c8>P1m>raw']]
    for cid, e in res.items():
        if e['hump_climb'] is None:
            continue
        e['vs'] = {bn: {'d_top3_climb': rnd(e['hump_climb']['top3'] - res[bid]['hump_climb']['top3']),
                        'd_top3_all': rnd(e['hump_all']['top3'] - res[bid]['hump_all']['top3'])}
                   for bn, bid in base_ids.items()}
        e['survives_ledger_rule'] = (e['mode'] != 'prim' and
                                     e['hump_climb']['top3'] >= K0['hump_climb']['top3'] + 0.05 and
                                     e['hump_all']['top3'] >= K0['hump_all']['top3'] - 0.02)
    # bootstrap where it matters: anything within reach of the best baseline on climbing steps, and every combo
    thr = min(res[base_ids['P1m']]['hump_climb']['top3'], K0['hump_climb']['top3']) - 0.03
    nboot = 0
    for cid, e in res.items():
        if e['hump_climb'] is None or (e['hump_climb']['top3'] < thr and e['mode'] != 'combo'):
            continue
        e['boot95_d_top3_climb'] = {bn: boot_delta(cid, base_ids[bn], 'climb') for bn in ('P1m', 'K0 P2c8>P1m>raw')}
        e['boot95_d_top3_all'] = {bn: boot_delta(cid, base_ids[bn], 'all') for bn in ('P1m', 'K0 P2c8>P1m>raw')}
        nboot += 1
    print('bootstrap done', nboot, round(time.time() - T0, 1), flush=True)

    # ---- Spearman with moves remaining
    spear = {}
    for n in active:
        xs, ys, within = [], [], []
        for pv in path_vals:
            v = pv['vals'].get(n)
            if v is None:
                continue
            N = pv['N']
            rem = [N - t for t in range(len(v))]
            xs += v
            ys += rem
            if pv['hump']:
                rho = spearman(v, rem)
                if rho is not None:
                    within.append(rho)
        spear[n] = {'pooled_rec_states': rnd(spearman(xs, ys)), 'n_states': len(xs),
                    'within_hump_path_mean': rnd(sum(within) / len(within)) if within else None,
                    'within_hump_paths': len(within)}
    print('spearman done', round(time.time() - T0, 1), flush=True)

    # ---- symmetric ("cage") states: do record paths pass through them less often than their siblings?
    passthrough = {}
    for nm in ('cage', 'stab>1', 'selfsym>0'):
        src_name = {'cage': 'cage', 'stab>1': 'stab', 'selfsym>0': 'selfsym'}[nm]
        thr_v = 1 if nm == 'stab>1' else 0
        if src_name not in active:
            continue
        out_s = {}
        for setname, sel in (('rec_all', lambda r: True), ('hump_all', lambda r: r['hump']),
                             ('rec_climb', lambda r: r['climb']),
                             ('rec_far_from_finish', lambda r: r['N'] - r['t'] > 6),
                             ('hump_far_from_finish', lambda r: r['hump'] and r['N'] - r['t'] > 6)):
            n_any = rec_sym = 0
            sib = 0.0
            n_steps = 0
            n_states_sym = 0
            for r in steps:
                if not sel(r):
                    continue
                n_steps += 1
                flags = [x > thr_v for x in r['vals'][src_name]]
                if not any(flags):
                    continue
                n_any += 1
                m = r['move']
                rec_sym += flags[m]
                sib += sum(f for j, f in enumerate(flags) if j != m) / 13.0
            out_s[setname] = {'steps': n_steps, 'steps_with_a_symmetric_child': n_any,
                              'record_child_symmetric_rate': rnd(rec_sym / n_any) if n_any else None,
                              'sibling_symmetric_rate': rnd(sib / n_any) if n_any else None}
        sym_states = sum(1 for pv in path_vals for x in pv['vals'][src_name] if x > thr_v)
        all_states = sum(len(pv['vals'][src_name]) for pv in path_vals)
        out_s['path_states_symmetric'] = [sym_states, all_states]
        out_s['note'] = 'rate = share of steps (with >= 1 symmetric child) whose record child is symmetric, vs the mean ' \
                        'share of symmetric children among the 13 siblings; far = more than 6 moves remain after the step'
        passthrough[nm] = out_s
    print('passthrough', json.dumps(passthrough), flush=True)

    # ---- P2 climb along hump paths: slack c such that a P2 <= P2(start) + c capped search contains the path
    p2climb = {}
    for label, cut in (('P2c8', 8), ('P2c40', 40)):
        per = []
        for pv in path_vals:
            if not pv['hump']:
                continue
            if cut == 8:
                seq = pv['vals']['P2c8']
            else:
                seq = [p2s(*ctx_of(s).c(), cut) for s in pv['states']]
            per.append({'row': pv['row'], 'len': pv['N'], 'record': pv['record'], 'P2_start': seq[0],
                        'P2_max': max(seq), 'climb': max(seq) - seq[0],
                        'raw_climb': max(tot(s) for s in pv['states']) - tot(pv['states'][0]),
                        'first_argmax_t': seq.index(max(seq))})
        cs = [e['climb'] for e in per]
        hist = Counter(cs)
        p2climb[label] = {'hump_paths': len(per), 'hist': {str(k): hist[k] for k in sorted(hist)},
                          'median': statistics.median(cs), 'mean': rnd(sum(cs) / len(cs)), 'max': max(cs),
                          'contained_frac_by_slack_c': {str(c): rnd(sum(1 for x in cs if x <= c) / len(cs))
                                                        for c in range(0, max(cs) + 1)},
                          'per_path': per}
    rec_cl = [max(pv['vals']['P2c8']) - pv['vals']['P2c8'][0] for pv in path_vals]
    hc = Counter(rec_cl)
    p2climb['P2c8_all_at_record_paths'] = {'paths': len(rec_cl), 'hist': {str(k): hc[k] for k in sorted(hc)},
                                           'contained_frac_by_slack_c': {str(c): rnd(sum(1 for x in rec_cl if x <= c) / len(rec_cl))
                                                                         for c in range(0, max(rec_cl) + 1)}}
    print('P2 climb', {k: (v['hist'], v.get('contained_frac_by_slack_c')) for k, v in p2climb.items()}, flush=True)

    counts = {'at_record_paths': len(at_rec), 'hump_paths': len(humps),
              **{k + '_steps': sum(1 for r, ks in zip(steps, step_sets) if k in ks) for k in sets}}
    scores_meta = {n: {'level': SC[n][2], 'a_priori_direction': SC[n][3], 'source': SC[n][4],
                       'expensive_hump_only': SC[n][5], 'timing': timing.get(n), 'spearman_moves_remaining': spear.get(n)}
                   for n in active}
    out = {'generated': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'script': os.path.relpath(__file__, REPO),
           'doc': __doc__, 'board_snapshot': os.path.relpath(P.BOARD, REPO), 'collection': collection,
           'counts': counts, 'probes': {'SL2': [{'p': pr.p, 'A': pr.A, 'B': pr.B, 'order': pr.n, 'diameter': pr.diameter}
                                                for pr in PROBES_SL2],
                                        'S7_target_cycle_types': [pr.target for pr in PROBES_SN]},
           'mirror_check': mirror, 'baseline_ids': base_ids, 'combos': {k: v for k, v in COMBOS.items()},
           'symmetric_passthrough': passthrough, 'P2_climb': p2climb,
           'scores': scores_meta, 'results': res, 'wall_s': round(time.time() - T0, 1)}
    with open(args.out, 'w') as f:
        json.dump(out, f, indent=1)

    # ---- console table
    print('counts', counts)
    for bn, bid in base_ids.items():
        e = res[bid]
        print('BASE %-18s hC %.3f hA %.3f hCconj %.3f hCmult %.3f rC %.3f rA %.3f' % (
            bn, e['hump_climb']['top3'], e['hump_all']['top3'], e['hump_climb_conj']['top3'],
            e['hump_climb_mult']['top3'], e['rec_climb']['top3'], e['rec_all']['top3']))
    rows = sorted((e for e in res.values() if e['hump_climb']), key=lambda e: -e['hump_climb']['top3'])
    print('%-40s %6s %6s %6s %6s %6s %6s' % ('config', 'hClim', 'hAll', 'hCconj', 'hCmult', 'rClim', 'rAll'))
    for e in rows[:70]:
        print('%-40s %6.3f %6.3f %6.3f %6.3f %6.3f %6.3f%s%s' % (
            e['score'] + '|' + e['direction'] + '|' + e['mode'], e['hump_climb']['top3'], e['hump_all']['top3'],
            e['hump_climb_conj']['top3'], e['hump_climb_mult']['top3'],
            e['rec_climb']['top3'] if e['rec_climb'] else -1, e['rec_all']['top3'],
            ' SURV' if e.get('survives_ledger_rule') else '', ' *flip' if e['flipped_post_hoc'] else ''))
    print('wrote', args.out, 'wall', out['wall_s'])


if __name__ == '__main__':
    main()
