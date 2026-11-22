#!/usr/bin/env python3
"""Rotate-then-multiply search: an AC-specific beam whose steps are products, with the lining-up priced exactly.

What our roads showed: ~45% of moves only re-align words (every length-neutral conjugation is a one-letter rotation),
a product can only cancel where the two words meet, and our one-move ties kept the products and dropped a rotation.
So one step here is a whole macro:
    rotate/shrink/wrap r0 and r1 by conjugations (cheapest sequence found exactly by a small per-word BFS,
    both directions: one letter left = "sub one", one letter right = "add one"; up to G wraps that add a letter pair)
    optionally invert the relator being changed (move 0/1)
    multiply it by the other relator with either sign ("opposite e": r0*r1 or r0*r1^-1, r1*r0 or r1*r0^-1)
Only products that cancel at the junction are generated. Cost = every official move in the macro.
Beam layers are products, not moves, so states that spent moves rotating no longer crowd out states that spent
them multiplying. Rank: cost + LAM * total length. States are kept once at their cheapest cost.
Every finish is replayed on the official core (Stable: + [16,15] or [15,15]); only roads shorter than ours count.

usage: rtm.py TARGETS.json OUT.json CIDS(comma, or 'all') [W] [G] [CUTSTEP] [LAMS e.g. 0.7,1,1.4]
TARGETS.json: list of {"cid","ours","rec","k","path"} (path = our best full road for that row)
"""
import sys, os, json, time
from multiprocessing import Pool
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as SR
from verifier import core, stable_core

TG = json.load(open(sys.argv[1])); OUTF = sys.argv[2]; CIDS = sys.argv[3]
W = int(sys.argv[4]) if len(sys.argv) > 4 else 2000
G = int(sys.argv[5]) if len(sys.argv) > 5 else 0
CUTSTEP = int(sys.argv[6]) if len(sys.argv) > 6 else 4
LAMS = [float(x) for x in (sys.argv[7] if len(sys.argv) > 7 else "0.7,1,1.4").split(",")]
NPROC = int(os.environ.get("NPROC", "4")); KMIN0 = os.environ.get("KMIN0") == "1"
ZMAX = int(os.environ.get("ZMAX", "2"))   # products with no cancellation allowed when the multiplier has <= ZMAX letters
NO = {"09839", "02257", "09311", "06403", "04718", "05378"}
LETI = {1: 0, -1: 1, 2: 2, -2: 3}          # move 6+4k+LETI[g] does r_k <- g r_k g^-1 (checked on the official core)
XY, YX = ((1,), (2,)), ((2,), (1,))

def mul(a, b):
    k = 0; la, lb = len(a), len(b)
    while k < la and k < lb and a[la - 1 - k] == -b[k]: k += 1
    return a[:la - k] + b[k:]
def inv(w): return tuple(-c for c in reversed(w))
def conj(w, g): return mul(mul((g,), w), (-g,))

NB = {}
def nbhd(w, k):
    """All words reachable from w by conjugations alone, length <= len(w)+2G, with the cheapest move sequence."""
    key = (w, k)
    r = NB.get(key)
    if r is not None: return r
    lim = len(w) + 2 * G; R = min(16, len(w) // 2 + G + 2)
    out = {w: ()}; fr = [w]
    for _ in range(R):
        nf = []
        for u in fr:
            for g in (1, -1, 2, -2):
                v = conj(u, g)
                if len(v) > lim or v in out: continue
                out[v] = out[u] + (6 + 4 * k + LETI[g],); nf.append(v)
        fr = nf
        if not fr: break
    r = list(out.items())
    if len(NB) > 60000: NB.clear()
    NB[key] = r; return r

def prep(s):
    """Per state: for each changed relator t, its conjugates (and inverses) indexed by last letter, and the other
    relator's conjugates with both signs."""
    N = (nbhd(s[0], 0), nbhd(s[1], 1)); P = []
    for t in (0, 1):
        idx = {}
        for a, pa in N[t]:
            if a: idx.setdefault(a[-1], []).append((a, pa))
            ai = inv(a)
            if ai: idx.setdefault(ai[-1], []).append((ai, pa + (t,)))      # invert the relator being changed
        mult = []
        for b, pb in N[1 - t]:
            for sgn in (1, -1):
                bb = b if sgn == 1 else inv(b)
                if bb: mult.append((b, pb, bb, (2 if sgn == 1 else 3) if t == 0 else (4 if sgn == 1 else 5)))
        P.append((idx, mult))
    return P

def finish(s, g, stable):
    """Cheapest finish from s by conjugations/inversions only."""
    best = None
    for a, pa in nbhd(s[0], 0):
        if len(a) != 1: continue
        for b, pb in nbhd(s[1], 1):
            if len(b) != 1 or abs(a[0]) == abs(b[0]): continue
            if not stable and abs(a[0]) != 1: continue
            mv = pa + pb + ((0,) if a[0] < 0 else ()) + ((1,) if b[0] < 0 else ())
            if best is None or len(mv) < len(best): best = mv
    return None if best is None else (g + len(best), best)

def search(s0, prefix, budget, lam, stable):
    nodes = [(-1, tuple(prefix))]; cur = [(s0, len(prefix), 0)]; seen = {s0: len(prefix)}; best = None; nexp = 0
    while cur:
        for s, g, nid in cur:
            f = finish(s, g, stable)
            if f and f[0] <= budget and (best is None or f[0] < best[0]): best = (f[0], nid, f[1])
        bound = best[0] - 1 if best else budget
        nxt = {}; thr = float("inf")
        for s, g, nid in cur:
            if g >= bound: continue
            P = prep(s)
            for t in (0, 1):
                idx, mult = P[t]
                for b, pb, bb, pm in mult:
                    lb = len(bb); g1 = g + len(pb) + 1
                    if g1 > bound: continue
                    allc = [x for l in idx.values() for x in l] if (KMIN0 or lb <= ZMAX) else idx.get(-bb[0], ())
                    for a, pa in allc:
                        ng = g1 + len(pa)
                        if ng > bound: continue
                        la = len(a); k = 0
                        while k < la and k < lb and a[la - 1 - k] == -bb[k]: k += 1
                        fv = ng + lam * (la + lb - 2 * k + len(b))
                        if fv > thr: continue
                        nexp += 1
                        na = a[:la - k] + bb[k:]
                        ns = (na, b) if t == 0 else (b, na)
                        o = seen.get(ns)
                        if o is not None and o <= ng: continue
                        x = nxt.get(ns)
                        if x is None or ng < x[0]:
                            nxt[ns] = (ng, nid, pa + pb + (pm,), fv)
                            if len(nxt) > 4 * W:
                                keep = sorted(nxt.items(), key=lambda kv: kv[1][3])[:2 * W]
                                nxt = dict(keep); thr = keep[-1][1][3]
        items = sorted(nxt.items(), key=lambda kv: kv[1][3])[:W]
        cur = []
        for ns, (ng, pid, mv, fv) in items:
            seen[ns] = ng; nodes.append((pid, mv)); cur.append((ns, ng, len(nodes) - 1))
    if not best: return None, nexp
    L, nid, tail = best; parts = [tail]
    while nid >= 0: pid, mv = nodes[nid]; parts.append(mv); nid = pid
    road = [m for p in reversed(parts) for m in p]
    return road, nexp

def start(num): return tuple(tuple(w) for w in SR.CH["ac-" + num]["initial_relators"])
def verify(cid, road):
    num = cid.split("-")[1]
    if cid.startswith("sac-"):
        for fin in ([16, 15], [15, 15]):
            if stable_core.verify(SR.CH[cid], road + fin, "sac-r8-v1", SR.LIM).get("ok"): return road + fin
        return None
    return road if core.verify(SR.CH[cid], road, "ac-r2-v1", SR.LIM)["ok"] else None

def job(j):
    t, cut, lam = j; t0 = time.time(); cid = t["cid"]; num = cid.split("-")[1]; stable = cid.startswith("sac-")
    body = []
    for m in t["path"]:
        if m > 13: break
        body.append(m)
    s = start(num)
    for m in body[:cut]: s = core.apply_move(s, m)
    budget = t["ours"] - 1 - (2 if stable else 0) + int(os.environ.get("BUDGETPLUS", "0"))   # strictly shorter than ours (self-test: +1)
    road, nexp = search(s, body[:cut], budget, lam, stable)
    out = dict(cid=cid, cut=cut, lam=lam, ours=t["ours"], rec=t["rec"], k=t["k"], sec=round(time.time() - t0, 1), nexp=nexp)
    if road:
        ok = verify(cid, road)
        out.update(len=len(ok) if ok else None, ok=bool(ok), path=ok)
    return out

if __name__ == "__main__":
    tg = [t for t in TG if t["cid"].split("-")[1] not in NO and (CIDS == "all" or t["cid"] in CIDS.split(","))]
    jobs = []
    for t in tg:
        n = sum(1 for m in t["path"] if m <= 13)
        L0 = sum(len(w) for w in start(t["cid"].split("-")[1]))
        cuts = range(0, max(1, n - 6), CUTSTEP)
        if os.environ.get("FROMEND"): cuts = sorted({n - int(x) for x in os.environ["FROMEND"].split(",") if n - int(x) >= 0})
        for cut in cuts:
            for lam in LAMS: jobs.append((t, cut, lam))
    if os.environ.get("CUTS"): jobs = [j for j in jobs if j[1] in {int(x) for x in os.environ["CUTS"].split(",")}]
    if os.environ.get("DONEF"):                          # skip jobs already finished in an earlier output file
        dn = {(r["cid"], r["cut"], r["lam"]) for r in json.load(open(os.environ["DONEF"]))}
        jobs = [j for j in jobs if (j[0]["cid"], j[1], j[2]) not in dn]
    jobs.sort(key=lambda j: -j[1])                       # late cuts first: small, near-exhaustive
    print("targets", len(tg), "jobs", len(jobs), "W", W, "G", G, "cutstep", CUTSTEP, "lams", LAMS, flush=True)
    res = []; t0 = time.time()
    with Pool(NPROC) as P:
        for r in P.imap_unordered(job, jobs, chunksize=1):
            res.append(r)
            if r.get("ok"):
                tag = "BEAT" if r["len"] < r["rec"] else ("TIE" if r["len"] == r["rec"] else "shorter")
                print(tag, r["cid"], r["len"], "record", r["rec"], "k", r["k"], "ours", r["ours"], "cut", r["cut"],
                      "lam", r["lam"], "%.0fs" % r["sec"], flush=True)
            elif r.get("path") is None and r.get("ok") is False:
                print("REPLAY-FAIL", r["cid"], r["cut"], flush=True)
            json.dump(res, open(OUTF, "w"))
    print("done", len(res), "jobs; improved rows", len({r["cid"] for r in res if r.get("ok")}),
          "time %ds" % (time.time() - t0), flush=True)
