# 3D recordings: x, y as SL(2,C) motions of the full ball (Light at the Hypersurface: S2.boost), planar vs non-planar maps.
import sys, re, gzip, math, random, json, time, cmath
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
NB = {cid: [[core.apply_move(s, m) for m in range(14)] for s in ROADS[cid][:-1]] for cid in rows[:300] if cid in ROADS}
def mul(A, B): return (A[0]*B[0]+A[1]*B[2], A[0]*B[1]+A[1]*B[3], A[2]*B[0]+A[3]*B[2], A[2]*B[1]+A[3]*B[3])
def inv(A): return (A[3], -A[1], -A[2], A[0])
def boost(u, r):   # S2.boost from the page: [[c + s uz, s(ux - i uy)], [s(ux + i uy), c - s uz]], c = cosh(r/2), s = sinh(r/2)
    c, s = math.cosh(r / 2), math.sinh(r / 2); ux, uy, uz = u
    return (complex(c + s * uz), complex(s * ux, -s * uy), complex(s * ux, s * uy), complex(c - s * uz))
def rot(n, th):    # exp(-i th/2 n.sigma)
    c, s = math.cos(th / 2), math.sin(th / 2); nx, ny, nz = n
    return (complex(c, -s * nz), complex(-s * ny, -s * nx), complex(s * ny, -s * nx), complex(c, s * nz))
r = math.log(5)
A1, A2, A3 = boost((0, 0, 1), r), boost((1, 0, 0), r), boost((0, 1, 0), r)      # A1 = our X, A2 = our Y, A3 = the third arm
VARIANTS = {"V0 planar (x=I, y=J)": (A1, A2), "V1 y=J then K": (A1, mul(A2, A3)), "V2 x=I then K, y=J then K": (mul(A1, A3), mul(A2, A3)),
            "V3 y=J with a 90deg twist": (A1, mul(A2, rot((1, 0, 0), math.pi / 2))), "V4 both twisted 90deg": (mul(A1, rot((0, 0, 1), math.pi / 2)), mul(A2, rot((1, 0, 0), math.pi / 2))),
            "V5 y=J with a 30deg twist": (A1, mul(A2, rot((1, 0, 0), math.pi / 6)))}
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
out = {}
for name, (GX, GY) in VARIANTS.items():
    GEN = {1: GX, -1: inv(GX), 2: GY, -2: inv(GY)}
    def word(w, pre=None):
        M, ls = (pre if pre else (1+0j, 0j, 0j, 1+0j)), 0.0
        for t in w:
            M = mul(M, GEN[t]); mx = max(abs(M[0]), abs(M[1]), abs(M[2]), abs(M[3]))
            if mx > 1e60: M = tuple(e / 1e60 for e in M); ls += math.log(1e60)
        return M, ls
    def dist(Mn, ls):   # cosh d(O, M O) = ||M||_F^2 / 2 in SL(2,C)
        lf = math.log(max(1e-300, sum(abs(e) ** 2 for e in Mn))) + 2 * ls - math.log(2)
        if lf > 20: return lf + math.log(2)
        x = math.exp(lf); return math.acosh(x) if x > 1 else 0.0
    Xi, Yi = inv(GX), inv(GY)
    def feats(st):
        A, B = word(st[0]), word(st[1])
        return {"letters": len(st[0]) + len(st[1]), "reach": dist(*A) + dist(*B), "rel": dist(*word(st[0], Xi)) + dist(*word(st[1], Yi))}
    combos = {"reach": lambda d: d["reach"], "rel": lambda d: d["rel"]}
    for w in (0.25, 0.5, 1, 2):
        combos["letters+%g*reach" % w] = (lambda d, w=w: d["letters"] + w * d["reach"]); combos["letters+%g*rel" % w] = (lambda d, w=w: d["letters"] + w * d["rel"])
    t0 = time.time(); data = []
    for cid, st in ROADS.items():
        for i, s in enumerate(st): f = feats(s); f["left"] = len(st) - 1 - i; data.append(f)
    left = [d["left"] for d in data]; mp = {n: spear([fn(d) for d in data], left) for n, fn in combos.items()}
    comp = {n: [0.0, 0, 0] for n in combos}
    for cid, layers in NB.items():
        for mv, nb in zip(best[cid], layers):
            if max(len(s[0]) + len(s[1]) for s in nb) > 400: continue
            fs = [feats(s) for s in nb]
            for n, fn in combos.items():
                vals = [fn(f) for f in fs]; me = vals[mv]
                better = sum(1 for x in vals if x < me - 1e-9); tie = sum(1 for x in vals if abs(x - me) <= 1e-9) - 1
                r_ = (better + tie / 2) / 13; c = comp[n]; c[0] += r_; c[1] += (r_ <= 2 / 13 + 1e-9); c[2] += 1
    out[name] = {n: {"top3": comp[n][1] / comp[n][2], "mean_rank": comp[n][0] / comp[n][2], "spearman": mp[n]} for n in combos}
    b = max(out[name].items(), key=lambda kv: kv[1]["top3"]); m_ = max(out[name].items(), key=lambda kv: kv[1]["spearman"])
    print("%-28s best compass %-20s %.1f%% | best map %-20s %.3f | reach alone %.1f%% rel alone %.1f%% | %.0fs" % (name, b[0], 100 * b[1]["top3"], m_[0], m_[1]["spearman"], 100 * out[name]["reach"]["top3"], 100 * out[name]["rel"]["top3"], time.time() - t0), flush=True)
json.dump(out, open("/tmp/claude-0/-home-user-operator-first/644f7765-aca6-5d39-980a-3e4ddc6288c0/scratchpad/grad/mixer3d_recordings.json", "w"))
