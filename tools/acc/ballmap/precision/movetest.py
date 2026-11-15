# Does accounting for the grid's movement help? Exact readings at z=5 on the same 700 roads.
# loop  : ln|2 - tr[A,B]|                     (trace only; blind to where the grid sits)
# reach : d(i, A i) + d(i, B i)                (how far each relator moves the base point: the grid's movement vs free space)
# fricke: |u-u*| + |v-v*| + |w-w*|, u = acosh(|trA|/2), v = acosh(|trB|/2), w = acosh(|trAB|/2): the pair's relative position, 3 numbers
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
L5 = math.log(5)
def lg(n): return math.log(abs(n)) if n else -50.0
def half_len(t_int, n):       # acosh(|tr|/2) with tr = t_int / 5^(n/2), via logs to stay exact-ish for huge ints
    x = lg(t_int) - n * L5 / 2 - math.log(2)          # ln(|tr|/2)
    return x + math.log(1 + math.sqrt(max(0.0, 1 - math.exp(-2 * x)))) if x > 0 else 0.0
def reach(M, n):              # d(i, M i) = acosh(|M|_F^2 / 2), |M|_F^2 = sum M^2 / 5^n
    x = lg(sum(e * e for e in M)) - n * L5 - math.log(2)
    return x + math.log(1 + math.sqrt(max(0.0, 1 - math.exp(-2 * x)))) if x > 0 else 0.0
def feats(st):
    A, B = word(st[0]), word(st[1]); a, b = len(st[0]), len(st[1]); n = a + b; AB = mul(A, B)
    tA, tB, tAB = A[0] + A[3], B[0] + B[3], AB[0] + AB[3]
    K = 4 * 5 ** n - tA * tA * 5 ** b - tB * tB * 5 ** a - tAB * tAB + tA * tB * tAB
    u, v, w = half_len(tA, a), half_len(tB, b), half_len(tAB, n)
    return {"letters": n, "loop": (lg(K) - n * L5) if K else -20.7, "reach": reach(A, a) + reach(B, b), "fricke": (u, v, w)}
FIN = feats(((1,), (2,)))["fricke"]
data, roads = [], []
for cid in rows:
    st = [tuple(tuple(x) for x in SR.CH[cid]["initial_relators"])]
    for mv in best[cid]: st.append(core.apply_move(st[-1], mv))
    if max(len(s[0]) + len(s[1]) for s in st) > 400: continue
    Lr = len(best[cid]); seq = []
    for i, s in enumerate(st):
        f = feats(s); f["left"] = Lr - i; u, v, w = f["fricke"]
        f["fdist"] = abs(u - FIN[0]) + abs(v - FIN[1]) + abs(w - FIN[2]); f["mv"] = best[cid][i - 1] if i else None
        seq.append(f)
    roads.append(seq); data += seq
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
def slope(f, tol=1e-9):
    d = s = u = 0
    for seq in roads:
        for a, b in zip(seq, seq[1:]):
            fa, fb = f(a), f(b)
            if abs(fb - fa) <= tol * max(1.0, abs(fa)): s += 1
            elif fb < fa: d += 1
            else: u += 1
    t = d + s + u; return d / t, s / t, u / t
left = [x["left"] for x in data]
print("roads", len(roads), "states", len(data))
R_ = {"letters": lambda x: x["letters"], "loop (trace only)": lambda x: x["loop"], "reach (grid movement)": lambda x: x["reach"],
      "fricke distance (a,b,trAB)": lambda x: x["fdist"], "letters + 2*loop": lambda x: x["letters"] + 2 * x["loop"],
      "letters + 1*reach": lambda x: x["letters"] + x["reach"], "letters + 2*fricke": lambda x: x["letters"] + 2 * x["fdist"],
      "letters + 2*loop + 1*fricke": lambda x: x["letters"] + 2 * x["loop"] + x["fdist"]}
print("%-30s %8s | per move: %6s %6s %6s" % ("reading", "Spearman", "down", "same", "up"))
for name, f in R_.items():
    dn, sm, up = slope(f); print("%-30s %8.3f | %16.3f %6.3f %6.3f" % (name, spear([f(x) for x in data], left), dn, sm, up))
for wt in (0.5, 1, 2, 4):
    print("  letters + %g*reach: %.3f   letters + %g*fricke: %.3f" % (wt, spear([x["letters"] + wt * x["reach"] for x in data], left), wt, spear([x["letters"] + wt * x["fdist"] for x in data], left)))
# Compass test: at each road state, rank all 14 next states by the reading; where does the road's actual next move land?
print("\nCompass test (300 roads): rank of the road's own next move among the 14 neighbours (0 = best, ties averaged)")
sub = [r for r in rows if r in best][:300]
res = {k: [] for k in R_}
for cid in sub:
    st = tuple(tuple(x) for x in SR.CH[cid]["initial_relators"])
    for mv in best[cid]:
        nb = [core.apply_move(st, m) for m in range(14)]
        if max(len(s[0]) + len(s[1]) for s in nb) > 400: st = nb[mv]; continue
        fs = []
        for s in nb:
            f = feats(s); u, v, w = f["fricke"]; f["fdist"] = abs(u - FIN[0]) + abs(v - FIN[1]) + abs(w - FIN[2]); fs.append(f)
        for name, fn in R_.items():
            vals = [fn(f) for f in fs]; me = vals[mv]
            better = sum(1 for x in vals if x < me - 1e-9); tie = sum(1 for x in vals if abs(x - me) <= 1e-9) - 1
            res[name].append((better + tie / 2) / 13)
        st = nb[mv]
print("%-30s %10s %10s" % ("reading", "mean rank", "in top 3"))
for name, v in res.items():
    print("%-30s %9.1f%% %9.1f%%" % (name, 100 * sum(v) / len(v), 100 * sum(1 for x in v if x <= 2 / 13 + 1e-9) / len(v)))
print("random guess: 50.0% mean rank, 21.4% in top 3 (3 of 14)")
