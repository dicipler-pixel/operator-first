# Sonar: replay every recorded road, mark collapse positions, and emit longline records (state, moves left, finish).
import sys, re, gzip, json, collections
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as SR
from verifier import core
R = "/home/user/operator-first/ACC_ROUNDUP_20261020/moves/"
OUT = sys.argv[1]; CAP = 255
E = {1: "0", -1: "1", 2: "2", -2: "3"}
best = {}; col = []; nroad = 0
def enc(w): return "".join(E[t] for t in w)
def roads():
    for line in gzip.open(R + "ALL_VERIFIED_ROADS.txt.gz", "rt"):
        m = re.match(r"(s?)(ac-\d+): \[([\d, ]*)\]", line)
        if m:
            p = list(map(int, m.group(3).split(",")))
            if m.group(1): p = p[:-2]
            if all(x < 14 for x in p): yield m.group(2), p, bool(m.group(1))
    for line in open(R + "BEST_ROADS_STABLE.txt"):
        m = re.match(r"s(ac-\d+): \[([\d, ]*)\]", line)
        if m: yield m.group(1), list(map(int, m.group(2).split(",")))[:-2], True
for cid, p, stab in roads():
    st = [tuple(tuple(x) for x in SR.CH[cid]["initial_relators"])]
    for mv in p: st.append(core.apply_move(st[-1], mv))
    fin = st[-1]
    if fin == ((1,), (2,)): ef = 0
    elif fin == ((2,), (1,)): ef = 1
    else: continue
    nroad += 1; L = len(p); lens = [len(a) + len(b) for a, b in st]
    run = lens[0]; peak = lens[0]
    for i, n in enumerate(lens):
        peak = max(peak, n)
        if n < run:
            if peak >= 1.5 * n and i < L: col.append((cid, i, L - i, n, peak))
            run = n; peak = n
    for i in range(max(0, L - CAP), L + 1):
        k = (st[i], ef); r = L - i
        if k not in best or r < best[k]: best[k] = r
with open(OUT + "/records.txt", "w") as f:
    for (s, ef), r in best.items(): f.write("%d %d %s %s\n" % (r, ef, enc(s[0]), enc(s[1])))
h = collections.Counter(min(c[2] // 10 * 10, 100) for c in col)
json.dump(col, open(OUT + "/collapses.json", "w"))
print("roads replayed", nroad, "| distinct hook states", len(best), "| collapse positions", len(col))
print("collapse moves-left histogram (by 10s):", sorted(h.items()))
