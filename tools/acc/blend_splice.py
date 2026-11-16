#!/usr/bin/env python3
"""Blend / splice / cross-path search over every verified road we hold.

Index: every state on every road (any row) that ends at (x,y) or (y,x) -> fewest moves left along that road.
Query: for each target row, every state on every road we hold for it, its radius-R move ball, and all 16
mirrors (8 signed letter permutations x optional word swap). A hit means: our prefix + ball path + the other
road's tail mapped back through the mirror + a short fix to the finish. AC needs (x,y); Stable takes (x,y) or
(y,x) and adds the 2-move finish. Every candidate shorter than our best is replayed on the official core.

usage: blend_splice.py TARGETS.json OUT.json R [extra road files...]
"""
import sys, os, json, gzip, re, glob, itertools
from multiprocessing import Pool
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as SR
from verifier import core, stable_core

TG = json.load(open(sys.argv[1])); OUTF = sys.argv[2]; R = int(sys.argv[3]); EXTRA = sys.argv[4:]
NO = {"09839", "02257", "09311", "06403", "04718", "05378"}
XY, YX = ((1,), (2,)), ((2,), (1,))
LET = [1, -1, 2, -2]
MAXREM = max(t["ours"] for t in TG) + 2

def start(num): return tuple(tuple(w) for w in SR.CH["ac-" + num]["initial_relators"])

# ---------- load roads ----------
roads = {}   # num -> set of AC-move tuples (prefix before any Stable-only move)
def add(cid, p):
    if not isinstance(p, list) or not p: return
    num = cid.split("-")[-1].split("#")[0]
    if num in NO or ("ac-" + num) not in SR.CH: return
    q = []
    for m in p:
        if not isinstance(m, int) or m < 0 or m > 13: break
        q.append(m)
    if q: roads.setdefault(num, set()).add(tuple(q))
M = "/home/user/operator-first/ACC_ROUNDUP_20261020/moves/"
for l in gzip.open(M + "ALL_VERIFIED_ROADS.txt.gz", "rt"):
    m = re.match(r"\s*(s?ac-\d+):\s*(\[.*\])", l)
    if m: add(m.group(1), json.loads(m.group(2)))
for l in open("/home/user/operator-first/research/acc/upgh/ledger.jsonl"):
    try: d = json.loads(l).get("data", {})
    except Exception: continue
    if isinstance(d, dict) and d.get("cid") and isinstance(d.get("moves"), list): add(d["cid"], d["moves"])
for f in EXTRA:
    for l in open(f):
        m = re.match(r"\s*(s?ac-\d+):\s*(\[.*\])", l)
        if m: add(m.group(1), json.loads(m.group(2)))
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for f in glob.glob(S + "/mine*/*.best.json"):
    cid = os.path.basename(f).split(".")[0]; d = json.load(open(f))
    for k in ("ac", "stable"): add(cid, d.get(k))
for f in glob.glob(S + "/mine*/*.road"):
    add(os.path.basename(f).split(".")[0], json.load(open(f)))

def states(num, p):
    s = start(num); out = [s]
    for m in p: s = core.apply_move(s, m); out.append(s)
    return out

# ---------- index ----------
IDX = {}   # hash(state) -> (rem, endpoint 0=xy 1=yx, num, road tuple, pos)
nroads = 0
for num, ps in roads.items():
    for p in ps:
        st = states(num, p)
        # trim to the first time the road reaches a finish
        end = None
        for j, s in enumerate(st):
            if s == XY or s == YX: end = j; break
        if end is None: continue
        e = 0 if st[end] == XY else 1; nroads += 1
        for j in range(max(0, end - MAXREM), end + 1):
            h = hash(st[j]); rem = end - j
            if h not in IDX or rem < IDX[h][0]: IDX[h] = (rem, e, num, p, j)
print("roads", sum(len(v) for v in roads.values()), "finishing", nroads, "index states", len(IDX), flush=True)

# ---------- mirrors ----------
MIR = []
for a in LET:
    for b in LET:
        if abs(a) == abs(b): continue
        for w in (0, 1): MIR.append(({1: a, -1: -a, 2: b, -2: -b}, w))
def tstate(s, T):
    mp, w = T; r = (tuple(mp[c] for c in s[0]), tuple(mp[c] for c in s[1]))
    return (r[1], r[0]) if w else r
def tinv(T):
    mp, w = T; inv = {v: k for k, v in mp.items()}; return (inv, w)
SW = {0: 1, 1: 0, 2: 4, 3: 5, 4: 2, 5: 3}
def tmove(m, T):
    mp, w = T
    if m < 6: return SW[m] if w else m
    word, li = divmod(m - 6, 4); nl = mp[LET[li]]
    return 6 + 4 * (word ^ w) + LET.index(nl)

def bfs_fix(src, goals, depth=6):
    if src in goals: return {src: []}
    seen = {src: []}; fr = [src]; got = {}
    for d in range(depth):
        nf = []
        for u in fr:
            for m in range(14):
                v = core.apply_move(u, m)
                if v in seen: continue
                seen[v] = seen[u] + [m]; nf.append(v)
                if v in goals and v not in got: got[v] = seen[v]
        if got: return got
        fr = nf
    return got
FIX = {}  # (endpoint state) -> (fix to XY, fix to XY-or-YX)
for T in MIR:
    Ti = tinv(T)
    for E in (XY, YX):
        q = tstate(E, Ti)
        if q in FIX: continue
        a = bfs_fix(q, {XY}); b = bfs_fix(q, {XY, YX})
        FIX[q] = (a.get(XY), min(b.values(), key=len) if b else None)

# ---------- query ----------
def ball(s):
    out = {s: []}; fr = [s]
    for d in range(R):
        nf = []
        for u in fr:
            for m in range(14):
                v = core.apply_move(u, m)
                if v not in out: out[v] = out[u] + [m]; nf.append(v)
        fr = nf
    return out

def work(job):
    t, num, p = job
    st = states(num, p); best = {}
    stable = t["cid"].startswith("sac-")
    for i, s in enumerate(st):
        if i >= t["ours"]: break
        for u, path in ball(s).items():
            base = i + len(path)
            if base >= t["ours"]: continue
            for T in MIR:
                hit = IDX.get(hash(tstate(u, T)))
                if not hit: continue
                rem, e, n2, p2, j = hit
                Ti = tinv(T); endst = tstate(XY if e == 0 else YX, Ti)
                fx, fa = FIX[endst]
                fix = fa if stable else fx
                if fix is None: continue
                L = base + rem + len(fix) + (2 if stable else 0)
                if L < t["ours"] and (L not in best):
                    tail = [tmove(m, Ti) for m in p2[j:j + rem]]
                    best[L] = (list(p[:i]) + path + tail + fix, n2)
    return t["cid"], best

if __name__ == "__main__":
    jobs = []
    for t in TG:
        num = t["cid"].split("-")[1]
        if num in NO: continue
        for p in roads.get(num, ()):
            if len(p) <= t["ours"] + 6: jobs.append((t, num, p))
    print("targets", len(TG), "jobs", len(jobs), "radius", R, flush=True)
    found = {}
    with Pool(4) as P:
        for cid, best in P.imap_unordered(work, jobs):
            for L, (path, src) in best.items(): found.setdefault(cid, []).append((L, path, src))
    out = []
    for t in TG:
        cid = t["cid"]; num = cid.split("-")[1]
        for L, path, src in sorted(found.get(cid, []), key=lambda x: x[0]):
            if cid.startswith("sac-"):
                ok = None
                for fin in ([16, 15], [15, 15]):
                    q = path + fin
                    if stable_core.verify(SR.CH["sac-" + num], q, "sac-r8-v1", SR.LIM).get("ok"): ok = q; break
                if ok:
                    out.append(dict(cid=cid, len=len(ok), rec=t["rec"], k=t["k"], ours=t["ours"], src=src, path=ok)); break
            else:
                if core.verify(SR.CH[cid], path, "ac-r2-v1", SR.LIM)["ok"]:
                    out.append(dict(cid=cid, len=len(path), rec=t["rec"], k=t["k"], ours=t["ours"], src=src, path=path)); break
    json.dump(out, open(OUTF, "w"))
    for o in out:
        tag = "BEAT" if o["len"] < o["rec"] else ("TIE" if o["len"] == o["rec"] else "improves ours")
        print(tag, o["cid"], o["len"], "record", o["rec"], "k", o["k"], "ours", o["ours"], "via", o["src"])
    print("done; verified improvements:", len(out))
