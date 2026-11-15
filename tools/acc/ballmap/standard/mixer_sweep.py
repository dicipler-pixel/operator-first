# Mixer sweep: record many ball readings on the same road states; map (Spearman, 700 roads) + compass (300 roads).
import sys, re, gzip, math, random, json, itertools, time
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as SR
from verifier import core
Z = float(sys.argv[1]) if len(sys.argv) > 1 else 5.0
OUT = sys.argv[2] if len(sys.argv) > 2 else "/tmp/claude-0/-home-user-operator-first/644f7765-aca6-5d39-980a-3e4ddc6288c0/scratchpad/grad/mixer_z%g.json" % Z
R = "/home/user/operator-first/ACC_ROUNDUP_20261020/moves/"
best = {}
for line in gzip.open(R + "ALL_VERIFIED_ROADS.txt.gz", "rt"):
    m = re.match(r"(ac-\d+): \[([\d, ]*)\]", line)
    if m:
        p = list(map(int, m.group(2).split(",")))
        if m.group(1) not in best or len(p) < len(best[m.group(1)]): best[m.group(1)] = p
rows = sorted(best); random.seed(1); random.shuffle(rows); rows = [r for r in rows if len(best[r]) <= 120][:700]
a = math.log(Z) / 2; ea, ch, sh = math.exp(a), math.cosh(a), math.sinh(a)
GEN = {1: (ea, 0.0, 0.0, 1 / ea), -1: (1 / ea, 0.0, 0.0, ea), 2: (ch, sh, sh, ch), -2: (ch, -sh, -sh, ch)}
def mul(A, B): return (A[0]*B[0]+A[1]*B[2], A[0]*B[1]+A[1]*B[3], A[2]*B[0]+A[3]*B[2], A[2]*B[1]+A[3]*B[3])
def inv(A): return (A[3], -A[1], -A[2], A[0])
def word(w, pre=None):           # (normalised matrix, log scale)
    M, ls = (pre if pre else (1.0, 0.0, 0.0, 1.0)), 0.0
    for t in w:
        M = mul(M, GEN[t]); mx = max(abs(M[0]), abs(M[1]), abs(M[2]), abs(M[3]))
        if mx > 1e60: M = (M[0] / 1e60, M[1] / 1e60, M[2] / 1e60, M[3] / 1e60); ls += math.log(1e60)
    return M, ls
def dist(Mn, ls, g=None):        # d(p, M p) with p = g(i): cosh d = |g^-1 M g|_F^2 / 2
    if g is not None: Mn = mul(inv(g), mul(Mn, g))
    lf = math.log(max(1e-300, Mn[0]**2 + Mn[1]**2 + Mn[2]**2 + Mn[3]**2)) + 2 * ls - math.log(2)
    if lf > 20: return lf + math.log(2)
    x = math.exp(lf); return math.acosh(x) if x > 1 else 0.0
def rot(th): return (math.cos(th / 2), math.sin(th / 2), -math.sin(th / 2), math.cos(th / 2))
def along(th, s): return mul(rot(th), (math.exp(s / 2), 0.0, 0.0, math.exp(-s / 2)))   # point at distance s from i, direction th
L = math.log(Z)
BASES = {"O": None, "I.5": along(0, .5 * L), "I1": along(0, L), "J.5": along(math.pi / 2, .5 * L), "J1": along(math.pi / 2, L),
         "D.5": along(math.pi / 4, .5 * L), "D1": along(math.pi / 4, L)}
NEIGH = [along(0, L), along(0, -L), along(math.pi / 2, L), along(math.pi / 2, -L)]
HEIGHTS = (0.5, 1.0, 2.0)
def lift(d, h): return math.acosh(max(1.0, math.cosh(h) ** 2 * math.cosh(min(d, 700)) - math.sinh(h) ** 2)) if d < 700 else d + 2 * math.log(math.cosh(h))
Xi, Yi = GEN[-1], GEN[-2]
def feats(st):
    f = {"letters": len(st[0]) + len(st[1])}
    A = word(st[0]); B = word(st[1])
    for name, g in BASES.items():
        f["reach_" + name] = dist(*A, g) + dist(*B, g)
    dA, dB = dist(*A), dist(*B)
    for h in HEIGHTS: f["reach_h%g" % h] = lift(dA, h) + lift(dB, h)
    f["reach_grid4"] = sum(dist(*A, g) + dist(*B, g) for g in NEIGH) / 4
    f["reach_max"] = max(dA, dB); f["reach_sq"] = math.sqrt(dA * dA + dB * dB)
    XA, YB = word(st[0], Xi), word(st[1], Yi); YA, XB = word(st[0], Yi), word(st[1], Xi)
    for name, g in (("O", None), ("I.5", BASES["I.5"]), ("D.5", BASES["D.5"]), ("J.5", BASES["J.5"])):
        xy = dist(*XA, g) + dist(*YB, g); yx = dist(*YA, g) + dist(*XB, g)
        f["rel_" + name] = xy; f["relmin_" + name] = min(xy, yx)
    return f
def rank(v):
    o = sorted(range(len(v)), key=lambda i: v[i]); r = [0.0] * len(v); i = 0
    while i < len(o):
        j = i
        while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
        for k in range(i, j + 1): r[o[k]] = (i + j) / 2
        i = j + 1
    return r
def spear(x, y):
    rx, ry = rank(x), rank(y); n = len(x); mx, my = sum(rx) / n, sum(ry) / n
    return sum((p - mx) * (q - my) for p, q in zip(rx, ry)) / math.sqrt(sum((p - mx) ** 2 for p in rx) * sum((q - my) ** 2 for q in ry))
t0 = time.time()
data = []
for cid in rows:
    st = [tuple(tuple(x) for x in SR.CH[cid]["initial_relators"])]
    for mv in best[cid]: st.append(core.apply_move(st[-1], mv))
    if max(len(s[0]) + len(s[1]) for s in st) > 400: continue
    Lr = len(best[cid])
    for i, s in enumerate(st):
        f = feats(s); f["left"] = Lr - i; data.append(f)
keys = [k for k in data[0] if k != "left"]
combos = {k: (lambda d, k=k: d[k]) for k in keys}
for k in keys:
    if k == "letters": continue
    for w in (0.5, 1, 2, 4): combos["letters+%g*%s" % (w, k)] = (lambda d, k=k, w=w: d["letters"] + w * d[k])
left = [d["left"] for d in data]
mp = {name: spear([fn(d) for d in data], left) for name, fn in combos.items()}
print("map done: %d states, %d readings, %.0fs" % (len(data), len(combos), time.time() - t0), flush=True)
comp = {name: [0.0, 0, 0] for name in combos}   # sum rank, top3 hits, n
sub = rows[:300]
for cid in sub:
    st = tuple(tuple(x) for x in SR.CH[cid]["initial_relators"])
    for mv in best[cid]:
        nb = [core.apply_move(st, m) for m in range(14)]
        if max(len(s[0]) + len(s[1]) for s in nb) > 400: st = nb[mv]; continue
        fs = [feats(s) for s in nb]
        for name, fn in combos.items():
            vals = [fn(f) for f in fs]; me = vals[mv]
            better = sum(1 for x in vals if x < me - 1e-9); tie = sum(1 for x in vals if abs(x - me) <= 1e-9) - 1
            r_ = (better + tie / 2) / 13; c = comp[name]; c[0] += r_; c[1] += (r_ <= 2 / 13 + 1e-9); c[2] += 1
        st = nb[mv]
res = sorted(((comp[n][1] / comp[n][2], comp[n][0] / comp[n][2], mp[n], n) for n in combos), reverse=True)
json.dump([{"reading": n, "top3": t, "mean_rank": r, "spearman": s} for t, r, s, n in res], open(OUT, "w"), indent=0)
print("z=%g  %d decisions; best 25 by compass (top-3 share):" % (Z, comp["letters"][2]))
print("%-34s %7s %9s %9s" % ("reading", "top3", "meanrank", "spearman"))
for t, r, s, n in res[:25]: print("%-34s %6.1f%% %8.1f%% %9.3f" % (n, 100 * t, 100 * r, s))
for n in ("letters", "reach_O", "letters+1*reach_O"):
    t, r, s = comp[n][1] / comp[n][2], comp[n][0] / comp[n][2], mp[n]; print("ref %-30s %6.1f%% %8.1f%% %9.3f" % (n, 100 * t, 100 * r, s))
print("best by map:", sorted(((v, k) for k, v in mp.items()), reverse=True)[:6])
print("time %.0fs" % (time.time() - t0))
