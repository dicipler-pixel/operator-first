# Atlas candidates on the compass/map harness (z = 5): matched reach MR (min over inversion signs, + swap),
# relative translation length T, matched loop ML (exact), loop (exact), Schur peel, along/off axis, one-step lookahead.
import sys, re, gzip, math, random, json, time
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as SR
from verifier import core
R = "/home/user/operator-first/ACC_ROUNDUP_20261020/moves/"
best = {}
for line in gzip.open(R + "ALL_VERIFIED_ROADS.txt.gz", "rt"):
    m = re.match(r"(ac-\d+): \[([\d, ]*)\]", line)
    if m:
        p = list(map(int, m.group(2).split(",")))
        if m.group(1) not in best or len(p) < len(best[m.group(1)]): best[m.group(1)] = p
rows = sorted(best); random.seed(1); random.shuffle(rows); rows = [r for r in rows if len(best[r]) <= 120][:700]
ROADS = {}
for cid in rows:
    st = [tuple(tuple(x) for x in SR.CH[cid]["initial_relators"])]
    for mv in best[cid]: st.append(core.apply_move(st[-1], mv))
    if max(len(s[0]) + len(s[1]) for s in st) <= 400: ROADS[cid] = st
IG = {1: (5, 0, 0, 1), -1: (1, 0, 0, 5), 2: (3, 2, 2, 3), -2: (3, -2, -2, 3)}      # integer form: rho(w) = M(w) / 5^(|w|/2)
def mul(A, B): return (A[0]*B[0]+A[1]*B[2], A[0]*B[1]+A[1]*B[3], A[2]*B[0]+A[3]*B[2], A[2]*B[1]+A[3]*B[3])
def iw(w):
    M = (1, 0, 0, 1)
    for t in w: M = mul(M, IG[t])
    return M
L5 = math.log(5)
def lg(n): return math.log(abs(n)) if n else -60.0
def acosh_l(lx):   # acosh(e^lx) for lx = ln x, x >= 1
    if lx <= 0: return 0.0
    return lx + math.log(1 + math.sqrt(max(0.0, 1 - math.exp(-2 * lx))))
def d_of(M, n):    # d(i, rho i), rho = M / 5^(n/2): cosh d = sum(M^2) / (2 * 5^n)
    return acosh_l(lg(M[0]**2 + M[1]**2 + M[2]**2 + M[3]**2) - n * L5 - math.log(2))
def ell(M, n):     # translation length 2 acosh(|tr|/2)
    return 2 * acosh_l(lg(M[0] + M[3]) - n * L5 / 2 - math.log(2))
def inv_word(w): return tuple(-t for t in reversed(w))
def feats(st, look=False):
    r0, r1 = st; A, B = iw(r0), iw(r1); a, b = len(r0), len(r1)
    f = {"letters": a + b, "reach": d_of(A, a) + d_of(B, b)}
    XiA, XA, YiB, YB = mul(IG[-1], A), mul(IG[1], A), mul(IG[-2], B), mul(IG[2], B)
    YiA, YA, XiB, XB = mul(IG[-2], A), mul(IG[2], A), mul(IG[-1], B), mul(IG[1], B)
    m0 = min(d_of(XiA, a + 1), d_of(XA, a + 1)); m1 = min(d_of(YiB, b + 1), d_of(YB, b + 1))
    s0 = min(d_of(YiA, a + 1), d_of(YA, a + 1)); s1 = min(d_of(XiB, b + 1), d_of(XB, b + 1))
    f["rel"] = d_of(XiA, a + 1) + d_of(YiB, b + 1); f["MR"] = m0 + m1; f["MRswap"] = min(m0 + m1, s0 + s1)
    f["T"] = ell(XiA, a + 1) + ell(YiB, b + 1)
    # matched loop: 2 - tr[A,X] = A12 A21 (l - 1/l)^2, 2 - tr[B,Y] = 1/4[(B11-B22)^2 - (B12-B21)^2](l - 1/l)^2, l = sqrt 5 -> (l-1/l)^2 = 16/5
    c = math.log(16 / 5)
    f["ML"] = max(-20.0, lg(A[1] * A[2]) - a * L5 + c) + max(-20.0, lg((B[0] - B[3])**2 - (B[1] - B[2])**2) - math.log(4) - b * L5 + c)
    n = a + b; tA, tB = A[0] + A[3], B[0] + B[3]; AB = mul(A, B); tAB = AB[0] + AB[3]
    K = 4 * 5 ** n - tA * tA * 5 ** b - tB * tB * 5 ** a - tAB * tAB + tA * tB * tAB
    f["loop"] = (lg(K) - n * L5) if K else -20.7
    # Schur peel: min over |k| <= 3 of |k| ln5 + d(Xp, Ap) + d(Yp, B A^k p), and the mirror A B^k
    best_p = f["rel"]; Ak, Ai, Bk, Bi = A, iw(inv_word(r0)), B, iw(inv_word(r1))
    PA, PB, NA, NB_ = A, A, B, B
    cur_pos_B, cur_neg_B, cur_pos_A, cur_neg_A = B, B, A, A
    for k in range(1, 4):
        cur_pos_B = mul(cur_pos_B, A); cur_neg_B = mul(cur_neg_B, Ai); cur_pos_A = mul(cur_pos_A, B); cur_neg_A = mul(cur_neg_A, Bi)
        for MB in (cur_pos_B, cur_neg_B):
            best_p = min(best_p, k * L5 + d_of(XiA, a + 1) + d_of(mul(IG[-2], MB), b + k * a + 1))
        for MA in (cur_pos_A, cur_neg_A):
            best_p = min(best_p, k * L5 + d_of(mul(IG[-1], MA), a + k * b + 1) + d_of(YiB, b + 1))
    f["peel"] = best_p
    # along / off the finish axis for r0: w = X^-1 A i ; along = ln|w|, off = asinh(|Re w| / Im w)   (float from the integer matrix)
    def aoff(M, n):
        p, q, u, v = (x / 5 ** (n / 2) for x in M) if n < 300 else (1.0, 0.0, 0.0, 1.0)
        w = complex(p * 1j + q) / complex(u * 1j + v) if (u or v) else 1j
        return abs(math.log(abs(w))) if abs(w) > 0 else 50.0, math.asinh(abs(w.real) / max(1e-300, w.imag)) if w.imag > 0 else 50.0
    al0, of0 = aoff(XiA, a + 1); al1, of1 = aoff(mul(IG[1], mul(IG[2], mul(IG[-2], mul(IG[-1], YiB)))), b + 1)  # second: same as Y^-1 B (identity padding)
    f["along"], f["off"] = al0 + al1, of0 + of1
    return f
def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); rr = [0.0] * len(v); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
        for k in range(i, j + 1): rr[o[k]] = (i + j) / 2
        i = j + 1
    return rr
def spear(x, y):
    rx, ry = rank(x), rank(y); n = len(x); mx, my = sum(rx) / n, sum(ry) / n
    return sum((p - mx) * (q - my) for p, q in zip(rx, ry)) / math.sqrt(sum((p - mx) ** 2 for p in rx) * sum((q - my) ** 2 for q in ry))
base = ["reach", "rel", "MR", "MRswap", "T", "ML", "loop", "peel", "along", "off"]
combos = {k: (lambda d, k=k: d[k]) for k in ["letters"] + base}
for k in base:
    for w in (0.25, 0.5, 1, 2): combos["letters+%g*%s" % (w, k)] = (lambda d, k=k, w=w: d["letters"] + w * d[k])
for w in (0.5, 1, 2):
    combos["letters+reach+%g*loop" % w] = (lambda d, w=w: d["letters"] + d["reach"] + w * d["loop"])
    combos["letters+0.5*MR+%g*loop" % w] = (lambda d, w=w: d["letters"] + 0.5 * d["MR"] + w * d["loop"])
    combos["letters+0.5*MR+%g*ML" % w] = (lambda d, w=w: d["letters"] + 0.5 * d["MR"] + w * d["ML"])
    combos["letters+0.5*MR+%g*off" % w] = (lambda d, w=w: d["letters"] + 0.5 * d["MR"] + w * d["off"])
combos["letters+0.25*peel+1*loop"] = lambda d: d["letters"] + 0.25 * d["peel"] + d["loop"]
t0 = time.time(); data = []
for cid, st in ROADS.items():
    for i, s in enumerate(st): f = feats(s); f["left"] = len(st) - 1 - i; data.append(f)
left = [d["left"] for d in data]; mp = {n: spear([fn(d) for d in data], left) for n, fn in combos.items()}
print("map: %d states %.0fs" % (len(data), time.time() - t0), flush=True)
comp = {n: [0.0, 0, 0] for n in combos}
for cid in rows[:300]:
    if cid not in ROADS: continue
    for mv, s in zip(best[cid], ROADS[cid]):
        nb = [core.apply_move(s, m) for m in range(14)]
        if max(len(x[0]) + len(x[1]) for x in nb) > 400: continue
        fs = [feats(x) for x in nb]
        for n, fn in combos.items():
            vals = [fn(f) for f in fs]; me = vals[mv]
            better = sum(1 for x in vals if x < me - 1e-9); tie = sum(1 for x in vals if abs(x - me) <= 1e-9) - 1
            r_ = (better + tie / 2) / 13; c = comp[n]; c[0] += r_; c[1] += (r_ <= 2 / 13 + 1e-9); c[2] += 1
print("compass %.0fs" % (time.time() - t0), flush=True)
# one-step lookahead on 100 roads: child value = min over its 14 children of the reading
look = {"letters+reach": [0.0, 0, 0], "lookahead letters+reach": [0.0, 0, 0], "letters+0.5*MR": [0.0, 0, 0], "lookahead letters+0.5*MR": [0.0, 0, 0]}
def fr(f, which): return f["letters"] + (f["reach"] if which == "reach" else 0.5 * f["MR"])
for cid in rows[:100]:
    if cid not in ROADS: continue
    for mv, s in zip(best[cid], ROADS[cid]):
        nb = [core.apply_move(s, m) for m in range(14)]
        if max(len(x[0]) + len(x[1]) for x in nb) > 300: continue
        f1 = [feats(x) for x in nb]
        la = {"reach": [], "MR": []}
        for x in nb:
            ch = [feats(core.apply_move(x, m)) for m in range(14)]
            for wch in la: la[wch].append(min(fr(c, wch) for c in ch))
        for name, vals in (("letters+reach", [fr(f, "reach") for f in f1]), ("lookahead letters+reach", la["reach"]), ("letters+0.5*MR", [fr(f, "MR") for f in f1]), ("lookahead letters+0.5*MR", la["MR"])):
            me = vals[mv]; better = sum(1 for x in vals if x < me - 1e-9); tie = sum(1 for x in vals if abs(x - me) <= 1e-9) - 1
            r_ = (better + tie / 2) / 13; c = look[name]; c[0] += r_; c[1] += (r_ <= 2 / 13 + 1e-9); c[2] += 1
res = sorted(((comp[n][1] / comp[n][2], comp[n][0] / comp[n][2], mp[n], n) for n in combos), reverse=True)
out = [{"reading": n, "top3": t, "mean_rank": r, "spearman": s} for t, r, s, n in res]
json.dump({"main": out, "lookahead_100roads": {k: {"top3": v[1] / v[2], "mean_rank": v[0] / v[2], "n": v[2]} for k, v in look.items()}}, open(sys.argv[1], "w"), indent=0)
print("%-30s %7s %9s %8s" % ("reading", "top3", "meanrank", "map"))
for t, r, s, n in res[:22]: print("%-30s %6.1f%% %8.1f%% %8.3f" % (n, 100 * t, 100 * r, s))
for n in ("letters", "reach", "MR", "T", "ML", "loop", "peel", "off", "along"):
    t, r, s = comp[n][1] / comp[n][2], comp[n][0] / comp[n][2], mp[n]; print("alone %-24s %6.1f%% %8.1f%% %8.3f" % (n, 100 * t, 100 * r, s))
print("best map:", [(n, round(mp[n], 3)) for n in sorted(mp, key=lambda k: -mp[k])[:5]])
for k, v in look.items(): print("lookahead test (100 roads, %d decisions): %-26s top3 %.1f%% mean rank %.1f%%" % (v[2], k, 100 * v[1] / v[2], 100 * v[0] / v[2]))
print("total %.0fs" % (time.time() - t0))
