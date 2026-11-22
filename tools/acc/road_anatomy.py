#!/usr/bin/env python3
"""Anatomy of AC roads: what each move class does, and the abelian (2x2 matrix) lower bound.

Moves 0-1 invert a relator, 2-5 multiply one relator by the other (row operations on the 2x2 exponent-sum
matrix), 6-13 conjugate (the exponent-sum matrix does not change). For every finishing road we hold:
  - share of each class, and how the total length changes on each class
  - how often a conjugation is a pure rotation (length unchanged), growth (+2) or shrink (-2)
  - minimum number of row operations any road needs (BFS in GL(2,Z) from the start matrix to the finish
    matrix), compared with the number the road actually uses
"""
import sys, json, gzip, re, glob, collections
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as SR
from verifier import core
NO = {"09839", "02257", "09311", "06403", "04718", "05378"}
XY, YX = ((1,), (2,)), ((2,), (1,))
roads = {}
def add(cid, p):
    if not isinstance(p, list) or not p: return
    num = cid.split("-")[-1].split("#")[0]
    if num in NO or ("ac-" + num) not in SR.CH: return
    q = []
    for m in p:
        if not isinstance(m, int) or m < 0 or m > 13: break
        q.append(m)
    if q: roads.setdefault(num, set()).add(tuple(q))
for l in gzip.open("/home/user/operator-first/ACC_ROUNDUP_20261020/moves/ALL_VERIFIED_ROADS.txt.gz", "rt"):
    m = re.match(r"\s*(s?ac-\d+):\s*(\[.*\])", l)
    if m: add(m.group(1), json.loads(m.group(2)))
for f in sys.argv[1:]:
    for l in open(f):
        m = re.match(r"\s*(s?ac-\d+):\s*(\[.*\])", l)
        if m: add(m.group(1), json.loads(m.group(2)))

def ab(w): return (sum(1 if c == 1 else -1 if c == -1 else 0 for c in w), sum(1 if c == 2 else -1 if c == -2 else 0 for c in w))
def rowops(M):
    (a, b), (c, d) = M
    return [((-a, -b), (c, d)), ((a, b), (-c, -d)), ((a + c, b + d), (c, d)), ((a - c, b - d), (c, d)),
            ((a, b), (c + a, d + b)), ((a, b), (c - a, d - b))]
def gl2dist(M, goal, cap=40, lim=14):
    if M == goal: return 0
    seen = {M}; fr = [M]
    for d in range(1, lim + 1):
        nf = []
        for u in fr:
            for v in rowops(u):
                if v in seen or max(abs(x) for r in v for x in r) > cap: continue
                if v == goal: return d
                seen.add(v); nf.append(v)
        fr = nf
    return None

cls = lambda m: "invert" if m < 2 else ("multiply" if m < 6 else "conjugate")
cnt = collections.Counter(); dl = collections.defaultdict(collections.Counter)
gap = collections.Counter(); share = []; nroads = 0; best = {}
for num, ps in roads.items():
    s0 = tuple(tuple(w) for w in SR.CH["ac-" + num]["initial_relators"])
    for p in ps:
        s = s0; st = [s]
        for j, m in enumerate(p):
            s = core.apply_move(s, m); st.append(s)
            if s in (XY, YX): p = p[:j + 1]; break
        else: continue
        nroads += 1
        for m, a, b in zip(p, st, st[1:]):
            c = cls(m); cnt[c] += 1
            dl[c][(len(b[0]) + len(b[1])) - (len(a[0]) + len(a[1]))] += 1
        if num not in best or len(p) < len(best[num][0]): best[num] = (p, st[len(p)])
print("finishing roads", nroads, "rows", len(best))
tot = sum(cnt.values())
for c in ("invert", "multiply", "conjugate"):
    d = dl[c]; n = sum(d.values())
    top = ", ".join("%+d: %.0f%%" % (k, 100 * v / n) for k, v in sorted(d.items(), key=lambda kv: -kv[1])[:5])
    print("%-9s %5.1f%% of moves | length change %s" % (c, 100 * cnt[c] / tot, top))
# abelian bound on each row's best road
rows = []
for num, (p, end) in best.items():
    s0 = tuple(tuple(w) for w in SR.CH["ac-" + num]["initial_relators"])
    M = (ab(s0[0]), ab(s0[1])); goal = ((1, 0), (0, 1)) if end == XY else ((0, 1), (1, 0))
    d = gl2dist(M, goal); used = sum(1 for m in p if m < 6)
    rows.append((num, len(p), used, d))
ok = [r for r in rows if r[3] is not None]
print("rows with abelian distance found", len(ok), "of", len(rows))
print("best roads: mean length %.1f, row-op moves used %.1f, abelian minimum %.1f, conjugations %.1f" % (
    sum(r[1] for r in ok) / len(ok), sum(r[2] for r in ok) / len(ok), sum(r[3] for r in ok) / len(ok),
    sum(r[1] - r[2] for r in ok) / len(ok)))
h = collections.Counter(r[3] for r in ok); print("abelian minimum histogram", dict(sorted(h.items())))
h2 = collections.Counter(r[2] - r[3] for r in ok); print("extra row-ops beyond abelian minimum", dict(sorted(h2.items())))
