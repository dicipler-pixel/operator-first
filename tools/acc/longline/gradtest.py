# Which reading slopes toward the finish? Features on every state of our best road per row; truth = moves left.
import sys, re, gzip, math, random
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
ZS = [1.5, 2, 3, 5, 8, 13]
def gens(z):
    a = math.log(z) / 2; e = math.exp(a); ch, sh = math.cosh(a), math.sinh(a)
    return {1: (e, 0, 0, 1 / e), -1: (1 / e, 0, 0, e), 2: (ch, sh, sh, ch), -2: (ch, -sh, -sh, ch)}
G = {z: gens(z) for z in ZS}
def word(w, g):
    p, q, u, v = 1.0, 0.0, 0.0, 1.0
    for t in w:
        e, f, gg, h = g[t]; p, q, u, v = p * e + q * gg, p * f + q * h, u * e + v * gg, u * f + v * h
    return p, q, u, v
def comm_tr(A, B):
    a, b, c, d = A; e, f, g, h = B
    P = (a * e + b * g, a * f + b * h, c * e + d * g, c * f + d * h); Q = (d * h - b * g * 0 + 0, 0, 0, 0)
    Ai = (d, -b, -c, a); Bi = (h, -f, -g, e)
    Q = (Ai[0] * Bi[0] + Ai[1] * Bi[2], Ai[0] * Bi[1] + Ai[1] * Bi[3], Ai[2] * Bi[0] + Ai[3] * Bi[2], Ai[2] * Bi[1] + Ai[3] * Bi[3])
    return P[0] * Q[0] + P[1] * Q[2] + P[2] * Q[1] + P[3] * Q[3]
def feats(st):
    f = {"letters": len(st[0]) + len(st[1])}
    for z in ZS:
        A, B = word(st[0], G[z]), word(st[1], G[z]); tA, tB = A[0] + A[3], B[0] + B[3]; tc = comm_tr(A, B)
        if not all(map(math.isfinite, (tA, tB, tc))): return None
        f["loop%g" % z] = math.log(max(1e-9, abs(2 - tc)))
        den = (tA * tA - 4) * (tB * tB - 4) / 4
        q = (2 - tc) / den if abs(den) > 1e-9 else 1.0          # = sin^2(angle) if axes cross, -sinh^2(dist) if apart
        f["axis%g" % z] = abs(math.log(max(1e-9, abs(q))))       # 0 at the finish (perpendicular crossing, q=1)
        f["size%g" % z] = math.acosh(max(1, abs(tA) / 2)) + math.acosh(max(1, abs(tB) / 2))
    f["loopmulti"] = sum(f["loop%g" % z] for z in ZS) / len(ZS)
    f["axismulti"] = sum(f["axis%g" % z] for z in ZS) / len(ZS)
    return f
data = []; roads = []
for cid in rows:
    st = [tuple(tuple(x) for x in SR.CH[cid]["initial_relators"])]
    for mv in best[cid]: st.append(core.apply_move(st[-1], mv))
    L = len(best[cid]); seq = []
    for i, s in enumerate(st):
        if len(s[0]) + len(s[1]) > 400: seq = None; break
        f = feats(s)
        if f is None: seq = None; break
        f["left"] = L - i; seq.append(f)
    if seq: roads.append(seq); data += seq
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
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry)); den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return num / den
def slope(key):  # share of road steps where the reading moves the right way (down as the finish nears), ties count half
    good = tot = 0
    for seq in roads:
        for a, b in zip(seq, seq[1:]):
            tot += 1; good += 1 if b[key] < a[key] else 0.5 if b[key] == a[key] else 0
    return good / tot
left = [d["left"] for d in data]
print("roads", len(roads), "states", len(data))
keys = [k for k in data[0] if k != "left"]
res = [(spear([d[k] for d in data], left), slope(k), k) for k in keys]
for s, sl, k in sorted(res, reverse=True): print("%-10s spearman %.3f  downhill-steps %.3f" % (k, s, sl))
print("-- letters + w * reading")
for k in ("loop5", "loopmulti", "axis5", "axismulti", "axis3", "axis2"):
    bestc = max(((spear([d["letters"] + w * d[k] for d in data], left), w) for w in (0.5, 1, 2, 4, 8, 16)))
    sl = None
    print("%-10s best spearman %.3f at w=%g" % (k, bestc[0], bestc[1]))
