#!/usr/bin/env python3
"""Audit our recent SAIR submissions: per line, was it accepted, a duplicate of what we already held, an improvement,
and does it score on the live board (our length == record; per-team points 2^(1-k))? usage: audit_submissions.py SINCE_ISO"""
import json, gzip, glob, sys, collections
R = "/home/user/operator-first/research/acc/live/"
since = sys.argv[1]
items = sorted(json.load(open(sorted(glob.glob(R + "mine_2*.json"))[-1]))["items"], key=lambda x: x["receivedAt"])
B = {}
for p in ("ac", "stable_ac"):
    f = sorted(glob.glob(R + "boards/%s_2*.json.gz" % p))[-1]
    for it in json.load(gzip.open(f))["data"]["items"]:
        B[it["challengeId"]] = (it.get("currentBestLength"), it.get("kTeams"))
best = {}                      # our best accepted length per row, as of each moment
rows = []
for x in items:
    seen_here = collections.Counter(r["challenge_id"] for r in (x.get("results") or []))
    for r in x.get("results") or []:
        cid, ok, L = r["challenge_id"], r.get("ok"), r.get("length")
        if x["receivedAt"] >= since:
            prev = best.get(cid)
            if not ok: kind = "REJECTED"
            elif prev is None: kind = "first"
            elif L < prev: kind = "improved"
            elif L == prev: kind = "DUPE"
            else: kind = "WORSE"
            rec, k = B.get(cid, (None, None))
            rows.append(dict(sub=x["submissionId"], at=x["receivedAt"][:16], cid=cid, len=L, prev=prev, kind=kind,
                             rec=rec, k=k, inbatch=seen_here[cid]))
        if ok and isinstance(L, int):
            best[cid] = min(L, best.get(cid, L))
# score now: our best == record
def pts(cid):
    rec, k = B.get(cid, (None, None))
    b = best.get(cid)
    return (2.0 ** (1 - k)) if (b is not None and rec is not None and b == rec and k) else 0.0
out = []
by = collections.defaultdict(list)
for r in rows: by[r["sub"]].append(r)
for s, rr in by.items():
    c = collections.Counter(r["kind"] for r in rr)
    sc = [r for r in rr if r["len"] == r["rec"]]
    out.append("#%s %s  lines %d  | first %d improved %d DUPE %d WORSE %d REJECTED %d | at record now %d (pts now %.4f) | over record %d" % (
        s, rr[0]["at"], len(rr), c["first"], c["improved"], c["DUPE"], c["WORSE"], c["REJECTED"], len(sc),
        sum(2.0 ** (1 - r["k"]) for r in sc if r["k"]), sum(1 for r in rr if r["rec"] is not None and r["len"] > r["rec"])))
# cross-submission duplicates inside the window
cnt = collections.Counter((r["cid"], r["len"]) for r in rows)
dups = sorted(k for k, v in cnt.items() if v > 1)
print("\n".join(out))
print("same row+length sent more than once in this window: %d" % len(dups))
json.dump({"rows": rows, "dups": dups}, open(R + "sweeps/rival3/audit_submissions_%s.json" % since[:10], "w"))
tot_now = sum(pts(c) for c in best)
print("our points now (all rows, from history + live board): %.3f AC+SAC" % tot_now)
