# Mixer v2 recordings: unequal step ratios (zx for arm I = x, zy for arm J = y) and light readings ln(t'/t) = ln|M u_phi|^2.
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
NB = {}
for cid in rows[:300]:
    if cid not in ROADS: continue
    NB[cid] = [[core.apply_move(s, m) for m in range(14)] for s in ROADS[cid][:-1]]
def mul(A, B): return (A[0]*B[0]+A[1]*B[2], A[0]*B[1]+A[1]*B[3], A[2]*B[0]+A[3]*B[2], A[2]*B[1]+A[3]*B[3])
def inv(A): return (A[3], -A[1], -A[2], A[0])
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
PHI = [k * math.pi / 4 for k in range(8)]
U = [(math.cos(f / 2), math.sin(f / 2)) for f in PHI]
def run(zx, zy):
    ax, ay = math.log(zx) / 2, math.log(zy) / 2
    GEN = {1: (math.exp(ax), 0.0, 0.0, math.exp(-ax)), -1: (math.exp(-ax), 0.0, 0.0, math.exp(ax)),
           2: (math.cosh(ay), math.sinh(ay), math.sinh(ay), math.cosh(ay)), -2: (math.cosh(ay), -math.sinh(ay), -math.sinh(ay), math.cosh(ay))}
    half = (math.exp(ax / 2), 0.0, 0.0, math.exp(-ax / 2))         # base point half a step along arm I
    def word(w, pre=None):
        M, ls = (pre if pre else (1.0, 0.0, 0.0, 1.0)), 0.0
        for t in w:
            M = mul(M, GEN[t]); mx = max(abs(M[0]), abs(M[1]), abs(M[2]), abs(M[3]))
            if mx > 1e60: M = (M[0] / 1e60, M[1] / 1e60, M[2] / 1e60, M[3] / 1e60); ls += math.log(1e60)
        return M, ls
    def dist(Mn, ls, g=None):
        if g is not None: Mn = mul(inv(g), mul(Mn, g))
        lf = math.log(max(1e-300, Mn[0]**2 + Mn[1]**2 + Mn[2]**2 + Mn[3]**2)) + 2 * ls - math.log(2)
        if lf > 20: return lf + math.log(2)
        x = math.exp(lf); return math.acosh(x) if x > 1 else 0.0
    def light(Mn, ls):           # ln(t'/t) for the 8 prepared directions: ln |M u|^2
        return [math.log(max(1e-300, (Mn[0]*u[0] + Mn[1]*u[1])**2 + (Mn[2]*u[0] + Mn[3]*u[1])**2)) + 2 * ls for u in U]
    LX, LY = light(*word((1,))), light(*word((2,)))
    Xi, Yi = GEN[-1], GEN[-2]
    def feats(st):
        A, B = word(st[0]), word(st[1]); la, lb = light(*A), light(*B)
        f = {"letters": len(st[0]) + len(st[1]), "reach_O": dist(*A) + dist(*B)}
        XA, YB, YA, XB = word(st[0], Xi), word(st[1], Yi), word(st[0], Yi), word(st[1], Xi)
        f["rel_O"] = dist(*XA) + dist(*YB); f["relmin_O"] = min(f["rel_O"], dist(*YA) + dist(*XB))
        f["rel_I.5"] = dist(*XA, half) + dist(*YB, half)
        f["light_abs"] = sum(abs(v) for v in la) / 8 + sum(abs(v) for v in lb) / 8
        lxy = sum(abs(p - q) for p, q in zip(la, LX)) / 8 + sum(abs(p - q) for p, q in zip(lb, LY)) / 8
        lyx = sum(abs(p - q) for p, q in zip(la, LY)) / 8 + sum(abs(p - q) for p, q in zip(lb, LX)) / 8
        f["light_rel"] = lxy; f["light_relmin"] = min(lxy, lyx)
        return f
    t0 = time.time(); data = []
    for cid, st in ROADS.items():
        Lr = len(st) - 1
        for i, s in enumerate(st): f = feats(s); f["left"] = Lr - i; data.append(f)
    keys = [k for k in data[0] if k not in ("left",)]
    combos = {k: (lambda d, k=k: d[k]) for k in keys}
    for k in keys:
        if k != "letters":
            for w in (0.25, 0.5, 1, 2): combos["letters+%g*%s" % (w, k)] = (lambda d, k=k, w=w: d["letters"] + w * d[k])
    combos["letters+0.5*rel_I.5+0.25*light_rel"] = lambda d: d["letters"] + 0.5 * d["rel_I.5"] + 0.25 * d["light_rel"]
    left = [d["left"] for d in data]; mp = {n: spear([fn(d) for d in data], left) for n, fn in combos.items()}
    comp = {n: [0.0, 0, 0] for n in combos}
    for cid, layers in NB.items():
        moves = best[cid]
        for mv, nb in zip(moves, layers):
            if max(len(s[0]) + len(s[1]) for s in nb) > 400: continue
            fs = [feats(s) for s in nb]
            for n, fn in combos.items():
                vals = [fn(f) for f in fs]; me = vals[mv]
                better = sum(1 for x in vals if x < me - 1e-9); tie = sum(1 for x in vals if abs(x - me) <= 1e-9) - 1
                r_ = (better + tie / 2) / 13; c = comp[n]; c[0] += r_; c[1] += (r_ <= 2 / 13 + 1e-9); c[2] += 1
    return {n: {"top3": comp[n][1] / comp[n][2], "mean_rank": comp[n][0] / comp[n][2], "spearman": mp[n]} for n in combos}, time.time() - t0
PAIRS = [(5, 5), (3, 5), (5, 3), (3, 7), (7, 3), (5, 7), (7, 5), (7, 7), (3, 3), (2, 5)]
allres = {}
for zx, zy in PAIRS:
    res, dt = run(zx, zy); allres["%g,%g" % (zx, zy)] = res
    top = sorted(res.items(), key=lambda kv: -kv[1]["top3"])[:4]
    g = math.sinh(math.log(zx) / 2) * math.sinh(math.log(zy) / 2)
    print("zx=%g zy=%g (g=%.3f, %s the wall) %.0fs | best: %s" % (zx, zy, g, "inside" if g < 1 else "past", dt,
          " ; ".join("%s %.1f%%/%.3f" % (n, 100 * v["top3"], v["spearman"]) for n, v in top)), flush=True)
json.dump(allres, open("/tmp/claude-0/-home-user-operator-first/644f7765-aca6-5d39-980a-3e4ddc6288c0/scratchpad/grad/mixer2_recordings.json", "w"))
print("\nreference rows at each ratio pair (top3 / mean rank / spearman):")
for key in ("letters", "letters+0.5*rel_I.5", "letters+0.5*light_rel", "letters+0.5*light_relmin", "letters+1*light_abs", "light_rel", "letters+0.5*rel_I.5+0.25*light_rel"):
    print("%-38s" % key + " ".join("%s:%.1f%%" % (p, 100 * allres[p][key]["top3"]) for p in allres))
