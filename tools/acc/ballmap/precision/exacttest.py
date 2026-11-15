# Loop reading L = ln|2 - tr[rho r0, rho r1]| at z=5 computed EXACTLY (integer matrices), vs float64; same 700 roads as gradtest.
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
G = {1: (5, 0, 0, 1), -1: (1, 0, 0, 5), 2: (3, 2, 2, 3), -2: (3, -2, -2, 3)}
def mul(A, B): return (A[0]*B[0]+A[1]*B[2], A[0]*B[1]+A[1]*B[3], A[2]*B[0]+A[3]*B[2], A[2]*B[1]+A[3]*B[3])
def word(w):
    M = (1, 0, 0, 1)
    for t in w: M = mul(M, G[t])
    return M
def L_exact(st):          # k*5^n = 4*5^n - tA^2 5^|B| - tB^2 5^|A| - tAB^2 + tA tB tAB  (trace identity, all integers)
    A, B = word(st[0]), word(st[1]); a, b = len(st[0]), len(st[1]); n = a + b
    tA, tB, tAB = A[0] + A[3], B[0] + B[3], (lambda C: C[0] + C[3])(mul(A, B))
    K = 4 * 5 ** n - tA * tA * 5 ** b - tB * tB * 5 ** a - tAB * tAB + tA * tB * tAB
    return (math.log(abs(K)) - n * math.log(5)) if K else -20.7
data, roads = [], []
for cid in rows:
    st = [tuple(tuple(x) for x in SR.CH[cid]["initial_relators"])]
    for mv in best[cid]: st.append(core.apply_move(st[-1], mv))
    Lr = len(best[cid]); seq = []
    for i, s in enumerate(st):
        if len(s[0]) + len(s[1]) > 400: seq = None; break
        seq.append({"left": Lr - i, "letters": len(s[0]) + len(s[1]), "loopx": L_exact(s)})
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
    return sum((a - mx) * (b - my) for a, b in zip(rx, ry)) / math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
def slope(f):
    g = t = e = 0
    for seq in roads:
        for a, b in zip(seq, seq[1:]):
            t += 1; fa, fb = f(a), f(b)
            if fb < fa: g += 1
            elif abs(fb - fa) < 1e-9: e += 1
    return g / t, e / t, (g + 0.5 * e) / t
left = [d["left"] for d in data]
print("roads", len(roads), "states", len(data))
print("Spearman with moves left: letters %.3f | exact loop %.3f" % (spear([d["letters"] for d in data], left), spear([d["loopx"] for d in data], left)))
for w in (0.5, 1, 2, 4, 8):
    print("  letters + %g * exact loop: %.3f" % (w, spear([d["letters"] + w * d["loopx"] for d in data], left)))
for name, f in (("letters", lambda d: d["letters"]), ("exact loop", lambda d: d["loopx"]), ("letters + 2*exact loop", lambda d: d["letters"] + 2 * d["loopx"])):
    g, e, h = slope(f); print("per move, %-24s strictly down %.3f | unchanged %.3f | down with ties as half %.3f" % (name, g, e, h))
# consistency: share of moves 0-5 among road steps used above, and whether the exact reading is unchanged on them
import collections
c = collections.Counter(); kept = []
for cid in rows:
    st = [tuple(tuple(x) for x in SR.CH[cid]["initial_relators"])]
    ok = True
    for mv in best[cid]:
        st.append(core.apply_move(st[-1], mv))
        if len(st[-1][0]) + len(st[-1][1]) > 400: ok = False
    if not ok or len(st[0][0]) + len(st[0][1]) > 400: continue
    for mv, a, b in zip(best[cid], st, st[1:]):
        same = abs(L_exact(a) - L_exact(b)) < 1e-9
        c[("mult/inv" if mv <= 5 else "conj", same)] += 1
print(dict(c))
