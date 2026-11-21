#!/usr/bin/env python3
"""New-order search: rebuild whole sections of our own roads, not single deletions.

For each target row, every state on every road we hold for that row (and the finish (x,y), plus (y,x) for
Stable) gets a backward ball of radius BK, recording the moves left to the finish through that state. From
every state on those roads a forward ball of radius FW is grown. A meeting at a shared state replaces the
section between the two cut points by a fresh ordered bridge of at most FW+BK moves, which can also jump from
one of our roads to another. The total is prefix + forward bridge + backward bridge + suffix, in actual moves.
Every candidate shorter than our best is replayed on the official core.

usage: reorder.py BOARD_AC.gz BOARD_STABLE.gz MINE.txt OUT.json FW BK [MAXGAP] [extra road files...]
"""
import sys, os, json, gzip, re, glob, time
from multiprocessing import Pool
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as SR
from verifier import core, stable_core

BA, BS, MINEF, OUTF = sys.argv[1:5]; FW = int(sys.argv[5]); BK = int(sys.argv[6])
MAXGAP = int(sys.argv[7]) if len(sys.argv) > 7 else 1; EXTRA = sys.argv[8:]
NPROC = int(os.environ.get("NPROC", "1")); NROADS = int(os.environ.get("NROADS", "6"))
NO = {"09839", "02257", "09311", "06403", "04718", "05378"}
XY, YX = ((1,), (2,)), ((2,), (1,))
INV = (0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10, 13, 12)

def start(num): return tuple(tuple(w) for w in SR.CH["ac-" + num]["initial_relators"])
def board(f):
    d = json.load(gzip.open(f))["data"]; lst = next(v for v in d.values() if isinstance(v, list))
    return {r["challengeId"]: (r["currentBestLength"], r["kTeams"]) for r in lst}

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
def addtext(lines):
    for l in lines:
        m = re.match(r"\s*(s?ac-\d+):\s*(\[.*\])", l)
        if m: add(m.group(1), json.loads(m.group(2)))
addtext(gzip.open("/home/user/operator-first/ACC_ROUNDUP_20261020/moves/ALL_VERIFIED_ROADS.txt.gz", "rt"))
for l in open("/home/user/operator-first/research/acc/upgh/ledger.jsonl"):
    try: d = json.loads(l).get("data", {})
    except Exception: continue
    if isinstance(d, dict) and d.get("cid") and isinstance(d.get("moves"), list): add(d["cid"], d["moves"])
for f in EXTRA:
    if f.endswith(".json"):
        for o in json.load(open(f)): add(o["cid"], o.get("path"))
    else: addtext(open(f))
SCR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for f in glob.glob(SCR + "/mine*/*.best.json"):
    cid = os.path.basename(f).split(".")[0]; d = json.load(open(f))
    for k in ("ac", "stable"): add(cid, d.get(k))
for f in glob.glob(SCR + "/mine*/*.road"): add(os.path.basename(f).split(".")[0], json.load(open(f)))

def finished(num, p):
    s = start(num); st = [s]
    for j, m in enumerate(p):
        s = core.apply_move(s, m); st.append(s)
        if s == XY or s == YX: return list(p[:j + 1]), st, (0 if s == XY else 1)
    return None
FIN = {}
for num, ps in roads.items():
    for p in ps:
        r = finished(num, p)
        if r: FIN.setdefault(num, []).append(r)

A, B = board(BA), board(BS)
mine = {}
for l in open(MINEF):
    t = l.split()
    if len(t) == 2 and t[1].isdigit(): mine[t[0]] = int(t[1])
held = {}
for num, lst in FIN.items():
    a = [len(p) for p, _, e in lst if e == 0]; s = [len(p) for p, _, e in lst]
    if a: held["ac-" + num] = min(a)
    if s: held["sac-" + num] = min(s) + 2
TG = []
for cid in set(mine) | set(held):
    num = cid.split("-")[1]
    if num in NO or num not in FIN: continue
    rec, k = (A if cid.startswith("ac-") else B).get(cid, (None, 0))
    if not rec: continue
    ours = min(mine.get(cid, 10**9), held.get(cid, 10**9))
    if 1 <= ours - rec <= MAXGAP: TG.append(dict(cid=cid, ours=ours, rec=rec, k=k))
ONLY = set(filter(None, os.environ.get("ONLY", "").split(",")))
if ONLY: TG = [t for t in TG if t["cid"].split("-")[1] in ONLY]
TG.sort(key=lambda t: (t["ours"] - t["rec"], t["k"], t["ours"]))

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

def work(t):
    t0 = time.time(); cid = t["cid"]; num = cid.split("-")[1]; stable = cid.startswith("sac-")
    extra = 2 if stable else 0
    lst = [r for r in FIN[num] if stable or r[2] == 0]
    lst = sorted(lst, key=lambda r: len(r[0]))[:NROADS]
    # backward frontier: state -> (moves left to a finish, bridge into the road, road, cut)
    back = {}
    def put(s, rem, br, p, j):
        if s not in back or rem < back[s][0]: back[s] = (rem, br, p, j)
    anchors = []
    for p, st, e in lst:
        for j, s in enumerate(st): anchors.append((s, len(p) - j, p, j))
    for E in ((XY, YX) if stable else (XY,)): anchors.append((E, 0, (), 0))
    seen_anchor = {}
    for s, rem, p, j in anchors:
        if s in seen_anchor and seen_anchor[s] <= rem: continue
        seen_anchor[s] = rem
        for v, path in ball(s, BK).items():   # path goes s -> v; reversed inverse goes v -> s
            br = tuple(INV[m] for m in reversed(path))
            put(v, rem + len(br), br, p, j)
    best = None
    for p, st, e in lst:
        for i, s in enumerate(st):
            if i + extra >= (best[0] if best else t["ours"]): break
            for u, fpath in ball(s, FW).items():
                h = back.get(u)
                if not h: continue
                rem, br, p2, j = h
                L = i + len(fpath) + rem + extra
                if L < (best[0] if best else t["ours"]):
                    path = list(p[:i]) + list(fpath) + list(br) + list(p2[j:])
                    best = (L, path, i, len(fpath), len(br))
    out = None
    if best:
        L, path, i, fl, bl = best
        if stable:
            for fin in ([16, 15], [15, 15]):
                if stable_core.verify(SR.CH["sac-" + num], path + fin, "sac-r8-v1", SR.LIM).get("ok"): out = path + fin; break
        elif core.verify(SR.CH[cid], path, "ac-r2-v1", SR.LIM)["ok"]: out = path
        if out: return dict(t, len=len(out), cut=i, fwd=fl, back=bl, path=out, sec=round(time.time() - t0))
    return dict(t, len=None, sec=round(time.time() - t0))

if __name__ == "__main__" and os.environ.get("DUMPTG"):
    out = []
    for t in TG:
        cid = t["cid"]; num = cid.split("-")[1]; stable = cid.startswith("sac-")
        lst = sorted([r for r in FIN[num] if stable or r[2] == 0], key=lambda r: len(r[0]))
        for p, st, e in lst:
            if stable:
                q = next((p + f for f in ([16, 15], [15, 15]) if stable_core.verify(SR.CH["sac-" + num], p + f, "sac-r8-v1", SR.LIM).get("ok")), None)
            else: q = p if core.verify(SR.CH[cid], p, "ac-r2-v1", SR.LIM)["ok"] else None
            if q: out.append(dict(t, path=q)); break
    json.dump(out, open(os.environ["DUMPTG"], "w")); print("dumped", len(out)); sys.exit(0)

if __name__ == "__main__":
    print("targets", len(TG), "fw", FW, "bk", BK, "roads per row", NROADS, flush=True)
    res = []
    with Pool(NPROC) as P:
        for r in P.imap_unordered(work, TG):
            res.append(r)
            if r["len"]:
                tag = "BEAT" if r["len"] < r["rec"] else ("TIE" if r["len"] == r["rec"] else "improves")
                print(tag, r["cid"], r["len"], "record", r["rec"], "k", r["k"], "ours", r["ours"],
                      "cut", r["cut"], "bridge %d+%d" % (r["fwd"], r["back"]), "%ds" % r["sec"], flush=True)
            json.dump(res, open(OUTF, "w"))
    print("done", len(res), "rows;", sum(1 for r in res if r["len"]), "improved", flush=True)
