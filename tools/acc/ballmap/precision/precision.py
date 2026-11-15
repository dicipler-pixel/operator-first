# Precision of the grid ball field: closed forms at high precision, exact integer arithmetic at odd z, float64 error on real roads.
import sys, re, gzip, math, random, collections
from fractions import Fraction
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as SR
from verifier import core
try:
    import mpmath as mp; mp.mp.dps = 50; HAVE_MP = True
except ImportError:
    HAVE_MP = False
print("mpmath:", HAVE_MP)
# 1. closed forms (50 digits): tr W = 2 - 4 sinh^4(r/2) = 2 - 4 (R/T)^2, R = G^2, T = 1 - R, G = (z-1)/(z+1); wall G^2 = 1/2
def mat(z):
    a = mp.log(z) / 2
    X = mp.matrix([[mp.e ** a, 0], [0, mp.e ** -a]]); Y = mp.matrix([[mp.cosh(a), mp.sinh(a)], [mp.sinh(a), mp.cosh(a)]])
    return X, Y
for name, z in (("3", mp.mpf(3)), ("5", mp.mpf(5)), ("wall", 3 + 2 * mp.sqrt(2)), ("8", mp.mpf(8))):
    X, Y = mat(z); W = X * Y * X ** -1 * Y ** -1; t = W[0, 0] + W[1, 1]
    G = (z - 1) / (z + 1); R = G ** 2; T = 1 - R; g = mp.sinh(mp.log(z) / 2) ** 2
    e1 = abs(t - (2 - 4 * g ** 2)); e2 = abs(t - (2 - 4 * (R / T) ** 2))
    line = "z=%-5s tr W=%s |trW-(2-4g^2)|=%s |trW-(2-4(R/T)^2)|=%s P=2G^2=%s" % (name, mp.nstr(t, 12), mp.nstr(e1, 3), mp.nstr(e2, 3), mp.nstr(2 * R, 12))
    if 2 * R < 1:   # inside the wall: centre of turn radius rho^2 = (1-s)/(1+s), s = sqrt(1-2G^2); turn = 2 acos(|t|/2)
        s = mp.sqrt(1 - 2 * R); rho2 = (1 - s) / (1 + s)
        a_, b_, c_, d_ = W[0, 0], W[0, 1], W[1, 0], W[1, 1]          # fixed point of z -> (a z + b)/(c z + d) in the upper half plane
        disc = mp.sqrt((d_ - a_) ** 2 + 4 * b_ * c_ + 0j); fp = ((a_ - d_) + disc) / (2 * c_)
        if fp.imag < 0: fp = ((a_ - d_) - disc) / (2 * c_)
        w = (fp - 1j) / (fp + 1j)                                     # Cayley map to the unit disk, i -> 0
        turn = 2 * mp.acos(abs(t) / 2); line += " | rho^2 formula=%s measured=%s | turn %s deg (= %s of a full turn the other way)" % (mp.nstr(rho2, 12), mp.nstr(abs(w) ** 2, 12), mp.nstr(mp.degrees(turn), 10), mp.nstr(1 - turn / (2 * mp.pi), 6))
    elif abs(2 * R - 1) < mp.mpf(10) ** -40:
        N = W + mp.eye(2); line += " | wall: |W+I|=%s |(W+I)^2|=%s (Jordan block)" % (mp.nstr(mp.mnorm(N, 1), 6), mp.nstr(mp.mnorm(N * N, 1), 3))
    else:
        line += " | past the wall: run length 4 acosh g = %s" % mp.nstr(4 * mp.acosh(g), 10)
    print(line)
X, Y = mat(mp.mpf(5)); M = mp.matrix([[1, 1], [1, -1]]) / mp.sqrt(2)
print("swap symmetry |M X M - Y| at z=5:", mp.nstr(mp.mnorm(M * X * M - Y, 1), 3))
# 2. exact integer form at odd z: rho(w) = z^(-|w|/2) * M(w), M integer, det M = z^|w|
def gens_int(z):
    c, s = (z + 1) // 2, (z - 1) // 2
    return {1: (z, 0, 0, 1), -1: (1, 0, 0, z), 2: (c, s, s, c), -2: (c, -s, -s, c)}
def mul(A, B): return (A[0]*B[0]+A[1]*B[2], A[0]*B[1]+A[1]*B[3], A[2]*B[0]+A[3]*B[2], A[2]*B[1]+A[3]*B[3])
def word(w, G):
    M = (1, 0, 0, 1)
    for t in w: M = mul(M, G[t])
    return M
adj = lambda M: (M[3], -M[1], -M[2], M[0])
def k_exact(st, z, G):                       # k = 2 - tr[rho r0, rho r1], exact rational
    A, B = word(st[0], G), word(st[1], G)
    C = mul(mul(A, B), mul(adj(A), adj(B))); return 2 - Fraction(C[0] + C[3], z ** (len(st[0]) + len(st[1])))
def logabs(q):
    if q == 0: return float("-inf")
    return math.log(abs(q.numerator)) - math.log(q.denominator)
GF = {}
def kf(st, z):                               # float64, as the C engine computes it
    a = math.log(z) / 2; ea, ch, sh = math.exp(a), math.cosh(a), math.sinh(a)
    g = {1: (ea, 0, 0, 1 / ea), -1: (1 / ea, 0, 0, ea), 2: (ch, sh, sh, ch), -2: (ch, -sh, -sh, ch)}
    def wf(w):
        M = (1.0, 0.0, 0.0, 1.0)
        for t in w: M = mul(M, g[t])
        return M
    A, B = wf(st[0]), wf(st[1]); C = mul(mul(A, B), mul(adj(A), adj(B))); return 2 - (C[0] + C[3])
G5 = gens_int(5)
fin = ((1,), (2,)); print("exact k at the finish (x,y), z=5:", k_exact(fin, 5, G5), "= 4 g^2 = 4*(4/5)^2 =", Fraction(64, 25))
# 3. real roads: invariance under moves 0-5 (exact) and float64 error vs exact
best = {}
for line in gzip.open("/home/user/operator-first/ACC_ROUNDUP_20261020/moves/ALL_VERIFIED_ROADS.txt.gz", "rt"):
    m = re.match(r"(ac-\d+): \[([\d, ]*)\]", line)
    if m:
        p = list(map(int, m.group(2).split(",")))
        if m.group(1) not in best or len(p) < len(best[m.group(1)]): best[m.group(1)] = p
rows = sorted(best); random.seed(1); random.shuffle(rows); rows = [r for r in rows if len(best[r]) <= 120][:300]
inv_ok = inv_n = 0; chg = collections.Counter(); tot = collections.Counter(); errs = collections.defaultdict(list); nst = 0
for cid in rows:
    st = tuple(tuple(x) for x in SR.CH[cid]["initial_relators"]); kprev = k_exact(st, 5, G5)
    for mv in best[cid]:
        nxt = core.apply_move(st, mv); kn = k_exact(nxt, 5, G5); tot[mv] += 1
        if kn != kprev: chg[mv] += 1
        if mv <= 5: inv_n += 1; inv_ok += (kn == kprev)
        L = len(nxt[0]) + len(nxt[1]); nst += 1
        if L <= 400:
            le = logabs(kn); kfl = kf(nxt, 5)
            lf = math.log(max(1e-9, abs(kfl))) if math.isfinite(kfl) else float("inf")
            errs[min(L // 20 * 20, 200)].append(abs(lf - le) if math.isfinite(lf) and math.isfinite(le) else float("inf"))
        st, kprev = nxt, kn
print("states checked:", nst)
print("exact invariance of k under moves 0-5 (inversions and multiplications): %d of %d moves" % (inv_ok, inv_n))
print("share of moves that change k, by move:", {m: "%.2f" % (chg[m] / tot[m]) for m in sorted(tot)})
print("float64 error in L = ln|k| at z=5 vs exact, by total letters (median / 90th pct / max, inf = overflow):")
for b in sorted(errs):
    v = sorted(errs[b]); n = len(v)
    print("  letters %3d-%3d: n=%5d  median %.2e  p90 %.2e  max %.2e" % (b, b + 19, n, v[n // 2], v[int(n * .9)], v[-1]))
