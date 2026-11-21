#!/usr/bin/env python3
"""8-10 move window pass with a random control.

For each target row, take our shortest road (Stable rows: shortest road to either finish). Every window
[i, j] with j - i in {8, 9, 10} is a candidate. Two arms of equal size, disjoint:
  picked  - windows ranked by climb-and-fall of the length profile, V - |T| with l_k = ln(len_{k+1}/len_k),
            V = sum |l_k|, T = sum l_k (direction kept; a pure downhill window scores 0 but is not excluded)
  control - windows drawn uniformly at random (fixed seed) from the rest.
Each window gets an exact meet-in-the-middle search for the shortest legal route between the two states,
forward radius ceil((w-1)/2) and backward radius floor((w-1)/2). Only strict shortenings count.
Every shortened full road is replayed with the official verifier before it is counted or reported.

usage: windows.py TARGETS.json OUT.json N_PER_ARM [SEED]
TARGETS.json: list of {"cid","ours","rec","k","path"} (path = our current best full road for that row)
"""
import sys, os, json, math, random, time
from multiprocessing import Pool
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as SR
from verifier import core, stable_core

TG = json.load(open(sys.argv[1])); OUTF = sys.argv[2]; N = int(sys.argv[3])
SEED = int(sys.argv[4]) if len(sys.argv) > 4 else 20261121
NPROC = int(os.environ.get("NPROC", "1"))
INV = (0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12)
WL = (8, 9, 10)

def start(cid): return tuple(tuple(w) for w in SR.CH["ac-" + cid.split("-")[1]]["initial_relators"])
def states(cid, p):
    s = start(cid); out = [s]
    for m in p: s = core.apply_move(s, m); out.append(s)
    return out
def ball(s, r):
    out = {s: ()}; fr = [s]
    for d in range(r):
        nf = []
        for u in fr:
            for m in range(14):
                v = core.apply_move(u, m)
                if v not in out: out[v] = out[u] + (m,); nf.append(v)
        fr = nf
    return out
def verify(cid, p):
    if cid.startswith("sac-"): return bool(stable_core.verify(SR.CH[cid], p, "sac-r8-v1", SR.LIM).get("ok"))
    return core.verify(SR.CH[cid], p, "ac-r2-v1", SR.LIM)["ok"]

# ---------- window selection ----------
jobs = []; rng = random.Random(SEED)
for t in TG:
    cid = t["cid"]; full = t["path"]
    body = [m for m in full if m <= 13]
    if cid.startswith("sac-"):
        # keep the AC part; the Stable finish (moves > 13) is re-appended unchanged
        cut = next((k for k, m in enumerate(full) if m > 13), len(full)); body = full[:cut]; tail = full[cut:]
    else: tail = []
    st = states(cid, body); ln = [len(s[0]) + len(s[1]) for s in st]
    lg = [math.log(ln[k + 1] / ln[k]) if ln[k] and ln[k + 1] else 0.0 for k in range(len(ln) - 1)]
    cands = []
    for w in WL:
        for i in range(0, len(body) - w + 1):
            seg = lg[i:i + w]; V = sum(abs(x) for x in seg); T = sum(seg)
            cands.append((V - abs(T), i, i + w))
    cands.sort(key=lambda c: -c[0])
    t["_body"], t["_tail"] = body, tail
    jobs.append((t, cands))
# equal budget across arms, spread across rows: round-robin over rows
picked, control = [], []
per_row = max(1, N // max(1, len(jobs)))
for t, cands in jobs:
    top = cands[:per_row]; chosen = {(i, j) for _, i, j in top}
    rest = [c for c in cands if (c[1], c[2]) not in chosen]
    rnd = rng.sample(rest, min(per_row, len(rest)))
    picked += [("picked", t, s, i, j) for s, i, j in top]
    control += [("control", t, s, i, j) for s, i, j in rnd]
picked, control = picked[:N], control[:N]

def work(job):
    arm, t, score, i, j = job
    cid = t["cid"]; body = t["_body"]; w = j - i
    st = states(cid, body); a = (w - 1 + 1) // 2; b = (w - 1) // 2
    F = ball(st[i], a); B = ball(st[j], b)
    best = None
    small, big = (B, F) if len(B) < len(F) else (F, B)
    for u in small:
        if u in big:
            fp, bp = F[u], B[u]
            d = len(fp) + len(bp)
            if d < w and (best is None or d < len(best)):
                best = list(fp) + [INV[m] for m in reversed(bp)]
    res = dict(arm=arm, cid=cid, i=i, j=j, w=w, score=round(score, 4), short=None)
    if best is not None:
        newbody = body[:i] + best + body[j:]
        full = newbody + t["_tail"]
        ok = verify(cid, full)
        res.update(short=w - len(best), newlen=len(full), ok=ok, path=full if ok else None)
    return res

if __name__ == "__main__":
    allj = picked + control
    print("rows", len(jobs), "windows per arm", len(picked), len(control), flush=True)
    t0 = time.time(); out = []
    with Pool(NPROC) as P:
        for r in P.imap_unordered(work, allj, chunksize=1):
            out.append(r)
            if r["short"] and r["ok"]:
                t = next(x for x in TG if x["cid"] == r["cid"])
                tag = "BEAT" if r["newlen"] < t["rec"] else ("TIE" if r["newlen"] == t["rec"] else "shorter")
                print(tag, r["arm"], r["cid"], "window", r["i"], r["j"], "saves", r["short"], "->", r["newlen"],
                      "record", t["rec"], "k", t["k"], flush=True)
            json.dump(out, open(OUTF, "w"))
    for arm in ("picked", "control"):
        rs = [r for r in out if r["arm"] == arm]
        sh = [r for r in rs if r["short"] and r["ok"]]
        print(arm, "windows", len(rs), "strict shortenings (replayed ok)", len(sh),
              "rows shortened", len({r["cid"] for r in sh}), flush=True)
    bad = [r for r in out if r["short"] and not r["ok"]]
    print("replay failures", len(bad), "time %ds" % (time.time() - t0), flush=True)
