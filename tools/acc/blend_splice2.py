#!/usr/bin/env python3
"""Ordered-route splice: two frontiers, every step kept, official replay.

Sources: every verified road we hold (roundup, ledger, scratch bests, extra files). The full ordered route of
each road is kept with the total reduced relator length at every step. Rises in that profile mark cuts.

Back frontier: every state on every road (any row) that reaches (x,y) or (y,x), with moves left along the road,
plus its BACK-move neighbourhood (the omitted states next to kept ones; the bridge move is stored).
Front frontier: from every state on our roads for a target row, the FWD-move ball, under all 16 mirrors
(signed letter permutations x word swap). A meeting gives prefix + forward bridge + back bridge + mapped tail
+ a short fix to the finish. Ranked by actual moves; AC needs (x,y); Stable takes either finish plus 2 moves.
Every candidate shorter than our best is replayed on the official core.

usage: blend_splice2.py BOARD_AC.gz BOARD_STABLE.gz MINE.txt OUT.json FWD BACK [MAXGAP] [extra road files...]
"""
import sys, os, json, gzip, re, glob
from multiprocessing import Pool
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as SR
from verifier import core, stable_core

BA, BS, MINEF, OUTF = sys.argv[1:5]; FWD = int(sys.argv[5]); BACK = int(sys.argv[6])
MAXGAP = int(sys.argv[7]) if len(sys.argv) > 7 else 3; EXTRA = sys.argv[8:]
NO = {"09839", "02257", "09311", "06403", "04718", "05378"}
XY, YX = ((1,), (2,)), ((2,), (1,))
LET = [1, -1, 2, -2]
INV = (0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12)
RISEONLY = os.environ.get('RISEONLY') == '1'   # full FWD radius only at cuts on a rise of the length profile
ONLYGAP = int(os.environ.get('ONLYGAP', '0'))      # if set, keep only targets with exactly this gap

def start(num): return tuple(tuple(w) for w in SR.CH["ac-" + num]["initial_relators"])
def board(f):
    d = json.load(gzip.open(f))["data"]; lst = next(v for v in d.values() if isinstance(v, list))
    return {r["challengeId"]: (r["currentBestLength"], r["kTeams"]) for r in lst}

# ---------- roads ----------
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
def addfile(f, opener=open):
    for l in opener(f, "rt") if opener is gzip.open else opener(f):
        m = re.match(r"\s*(s?ac-\d+):\s*(\[.*\])", l)
        if m: add(m.group(1), json.loads(m.group(2)))
addfile("/home/user/operator-first/ACC_ROUNDUP_20261020/moves/ALL_VERIFIED_ROADS.txt.gz", gzip.open)
for l in open("/home/user/operator-first/research/acc/upgh/ledger.jsonl"):
    try: d = json.loads(l).get("data", {})
    except Exception: continue
    if isinstance(d, dict) and d.get("cid") and isinstance(d.get("moves"), list): add(d["cid"], d["moves"])
for f in EXTRA: addfile(f)
S = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for f in glob.glob(S + "/mine*/*.best.json"):
    cid = os.path.basename(f).split(".")[0]; d = json.load(open(f))
    for k in ("ac", "stable"): add(cid, d.get(k))
for f in glob.glob(S + "/mine*/*.road"): add(os.path.basename(f).split(".")[0], json.load(open(f)))

def states(num, p):
    s = start(num); out = [s]
    for m in p: s = core.apply_move(s, m); out.append(s)
    return out
FIN = {}   # num -> list of (road, states, end index, endpoint)
for num, ps in roads.items():
    for p in ps:
        st = states(num, p)
        for j, s in enumerate(st):
            if s == XY or s == YX: FIN.setdefault(num, []).append((p[:j], st[:j + 1], j, 0 if s == XY else 1)); break

# ---------- targets: ours = min(submitted, held) ----------
A, B = board(BA), board(BS)
mine = {}
for l in open(MINEF):
    t = l.split()
    if len(t) == 2 and t[1].isdigit(): mine[t[0]] = int(t[1])
held = {}
for num, lst in FIN.items():
    a = min((j for _, _, j, e in lst if e == 0), default=None)
    s = min((j for _, _, j, e in lst), default=None)
    if a is not None: held["ac-" + num] = a
    if s is not None: held["sac-" + num] = s + 2
TG, unsent = [], []
for cid in set(mine) | set(held):
    num = cid.split("-")[1]
    if num in NO: continue
    rec, k = (A if cid.startswith("ac-") else B).get(cid, (None, 0))
    if not rec: continue
    ours = min(mine.get(cid, 10**9), held.get(cid, 10**9))
    if held.get(cid, 10**9) <= rec and mine.get(cid, 10**9) > held[cid]: unsent.append((cid, held[cid], rec, k, mine.get(cid)))
    if 1 <= ours - rec <= MAXGAP: TG.append(dict(cid=cid, ours=ours, rec=rec, k=k))
if ONLYGAP: TG = [t for t in TG if t["ours"] - t["rec"] == ONLYGAP]
TG.sort(key=lambda t: (t["ours"] - t["rec"], t["k"]))
MAXREM = max(t["ours"] for t in TG) + 2

# ---------- back frontier ----------
IDX = {}   # hash(state) -> (rem, endpoint, num, road, pos, bridge moves from this state onto the road)
for num, lst in FIN.items():
    for p, st, end, e in lst:
        for j in range(max(0, end - MAXREM), end + 1):
            h = hash(st[j]); rem = end - j
            if h not in IDX or rem < IDX[h][0]: IDX[h] = (rem, e, num, p, j, ())
if BACK >= 1:
    layer = []
    for num, lst in FIN.items():
        for p, st, end, e in lst:
            for j in range(max(0, end - MAXREM), end + 1): layer.append((st[j], end - j, e, num, p, j, ()))
    for d in range(BACK):
        nl = []
        for s, rem, e, num, p, j, br in layer:
            for m in range(14):
                v = core.apply_move(s, m); h = hash(v); nb = (INV[m],) + br
                cand = (rem + len(nb), e, num, p, j, nb)
                if h not in IDX or cand[0] < IDX[h][0]: IDX[h] = cand; nl.append((v, rem, e, num, p, j, nb))
        layer = nl
print("roads", sum(len(v) for v in roads.values()), "back frontier", len(IDX), "targets", len(TG), flush=True)
for u in sorted(unsent): print("HELD-NOT-SUBMITTED", *u, flush=True)

# ---------- mirrors and fixes ----------
MIR = []
for a in LET:
    for b in LET:
        if abs(a) != abs(b):
            for w in (0, 1): MIR.append(({1: a, -1: -a, 2: b, -2: -b}, w))
def tstate(s, T):
    mp, w = T; r = (tuple(mp[c] for c in s[0]), tuple(mp[c] for c in s[1]))
    return (r[1], r[0]) if w else r
def tinv(T):
    mp, w = T; return ({v: k for k, v in mp.items()}, w)
SW = {0: 1, 1: 0, 2: 4, 3: 5, 4: 2, 5: 3}
def tmove(m, T):
    mp, w = T
    if m < 6: return SW[m] if w else m
    word, li = divmod(m - 6, 4); return 6 + 4 * (word ^ w) + LET.index(mp[LET[li]])
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
FIX = {}
for T in MIR:
    Ti = tinv(T)
    for E in (XY, YX):
        q = tstate(E, Ti)
        if q not in FIX:
            a = bfs_fix(q, {XY}); b = bfs_fix(q, {XY, YX})
            FIX[q] = (a.get(XY), min(b.values(), key=len) if b else None)

# ---------- front frontier ----------
def ball(s, r):
    out = {s: []}; fr = [s]
    for d in range(r):
        nf = []
        for u in fr:
            for m in range(14):
                v = core.apply_move(u, m)
                if v not in out: out[v] = out[u] + [m]; nf.append(v)
        fr = nf
    return out
def size(s): return len(s[0]) + len(s[1])

def work(job):
    t, num, p = job
    st = states(num, p); stable = t["cid"].startswith("sac-"); best = {}
    prof = [size(s) for s in st]
    for i, s in enumerate(st):
        if i >= t["ours"] - 1: break
        rise = (i + 1 < len(prof) and prof[i + 1] > prof[i]) or (i > 0 and prof[i] > prof[i - 1])
        r = FWD if (rise or not RISEONLY) else max(1, FWD - 1)
        for u, path in ball(s, r).items():
            b0 = i + len(path)
            if b0 >= t["ours"]: continue
            for T in MIR:
                hit = IDX.get(hash(tstate(u, T)))
                if not hit: continue
                rem, e, n2, p2, j, br = hit
                Ti = tinv(T); fx, fa = FIX[tstate(XY if e == 0 else YX, Ti)]
                fix = fa if stable else fx
                if fix is None: continue
                L = b0 + rem + len(fix) + (2 if stable else 0)
                if L < t["ours"] and L not in best:
                    tail = [tmove(m, Ti) for m in list(br) + list(p2[j:])]
                    best[L] = (list(p[:i]) + path + tail + fix, n2, i, rise, len(path), len(br))
    return t["cid"], best

if __name__ == "__main__":
    jobs = []
    for t in TG:
        num = t["cid"].split("-")[1]
        for p, _, _, _ in sorted(FIN.get(num, []), key=lambda x: x[2])[:6]: jobs.append((t, num, p))
    print("jobs", len(jobs), "fwd", FWD, "back", BACK, flush=True)
    found = {}
    with Pool(4) as P:
        for cid, best in P.imap_unordered(work, jobs, chunksize=1):
            for L, v in best.items(): found.setdefault(cid, []).append((L,) + v)
    out = []
    for t in TG:
        cid = t["cid"]; num = cid.split("-")[1]
        for L, path, src, cut, rise, fl, bl in sorted(found.get(cid, []), key=lambda x: x[0]):
            ok = None
            if cid.startswith("sac-"):
                for fin in ([16, 15], [15, 15]):
                    if stable_core.verify(SR.CH["sac-" + num], path + fin, "sac-r8-v1", SR.LIM).get("ok"): ok = path + fin; break
            elif core.verify(SR.CH[cid], path, "ac-r2-v1", SR.LIM)["ok"]: ok = path
            if ok:
                out.append(dict(cid=cid, len=len(ok), rec=t["rec"], k=t["k"], ours=t["ours"], src=src, cut=cut,
                                rise=rise, fwd=fl, back=bl, path=ok)); break
    json.dump(out, open(OUTF, "w"))
    for o in out:
        tag = "BEAT" if o["len"] < o["rec"] else ("TIE" if o["len"] == o["rec"] else "improves")
        print(tag, o["cid"], o["len"], "record", o["rec"], "k", o["k"], "ours", o["ours"], "via", o["src"],
              "cut", o["cut"], "rise" if o["rise"] else "flat", "bridge %d+%d" % (o["fwd"], o["back"]))
    print("done; verified improvements:", len(out))
