"""Results data for the idea/results map: every line accepted since the session start, its value then and now,
the method that found it, and the score history. Writes tools/acc/dashboard/results_data.json."""
import json, glob, gzip, re, os
LOG = "research/acc/live/submit_log.jsonl"; START = "20260927T2240Z"
METHOD_BY_SUB = {"2558": "Beam + exact (NEW15)", "2565": "AC+2 to Stable AC", "2566": "Exact capped sweep",
    "2569": "Exact capped sweep", "2572": "Exact capped sweep", "2581": "Exact capped sweep",
    "2606": "Mirror cross-row", "2607": "Mirror cross-row", "2632": "Road cycle (session 1)"}
METHOD_BY_ROW = {"ac-03060": "P2 lookahead", "sac-03060": "P2 lookahead", "ac-05835": "P2 lookahead",
    "ac-01698": "P2 lookahead", "ac-03789": "P2 lookahead", "sac-01698": "(y,x) shortcut", "sac-05091": "(y,x) shortcut",
    "sac-00487": "Class quota", "ac-00487": "Overlap splice", "ac-03028": "Mirror cross-row", "sac-03028": "Mirror cross-row",
    "ac-09989": "Mirror cross-row", "sac-09989": "Mirror cross-row",
    "sac-00222": "P2 lookahead", "ac-06094": "Two-eyes beam (DUAL)", "sac-06094": "Two-eyes beam (DUAL)",
    "sac-05835": "Two-eyes beam (DUAL)", "sac-08429": "(y,x) lane (letter-swap twin)",
    "ac-08078": "Two-eyes beam (DUAL)", "ac-02528": "User / Charlie line",
    "ac-02275": "Two-eyes beam (DUAL)", "sac-02275": "Two-eyes beam (DUAL)",
    "sac-03771": "Two-eyes beam (DUAL)", "ac-08429": "Two-eyes beam (DUAL)",
    "ac-08578": "Two-eyes beam (DUAL)", "ac-04191": "Helper B two-eyes list", "sac-04191": "Helper B two-eyes list",
    "ac-05818": "Codex mirror twin", "sac-05818": "Codex mirror twin",
    "sac-00021": "yx_mid (Stable = AC+1)", "ac-09365": "Two-eyes ranked lane rk2", "sac-02153": "Two-eyes ranked lane rk2 (y,x) finish",
    "ac-04612": "Easy-rows lane fe", "sac-04612": "Easy-rows lane fe", "ac-09507": "Easy-rows lane fe", "sac-09507": "Easy-rows lane fe"}
def board(kind, ts):
    fs = sorted(glob.glob(f"research/acc/live/boards/{kind}_2026*.json.gz"))
    best = None
    for f in fs:
        t = re.search(r"_(\d{8}T\d{4}Z)", f).group(1)
        if t <= ts: best = f
    return best, fs[-1]
def rows(f):
    d = json.load(gzip.open(f))["data"]; lst = next(v for v in d.values() if isinstance(v, list))
    return {r["challengeId"]: (r["currentBestLength"], r["kTeams"]) for r in lst}
cache = {}
def R(f):
    if f not in cache: cache[f] = rows(f)
    return cache[f]
lines = []
for l in open(LOG):
    e = json.loads(l)
    if e.get("event") != "result" or e["at"] < START: continue
    sid = e["submissionId"]
    for r in e.get("results", []):
        if not r.get("ok"): continue
        cid = r["challenge_id"]; kind = "stable_ac" if cid.startswith("sac") else "ac"
        bf, now = board(kind, e["at"])
        rec_then, k_then = R(bf).get(cid, (None, None)) if bf else (None, None)
        rec_now, k_now = R(now)[cid]
        val_then = (1.0 if rec_then and r["length"] < rec_then else (2 ** -(k_then or 0) if rec_then == r["length"] else 0))
        holding = rec_now == r["length"]
        val_now = 2 ** (1 - k_now) if holding and k_now else 0.0
        lines.append({"sub": sid, "at": e["at"][9:11] + ":" + e["at"][11:13], "row": cid, "kind": "Stable AC" if kind == "stable_ac" else "AC",
                      "len": r["length"], "k_then": k_then, "val_then": round(val_then, 5), "rec_now": rec_now, "k_now": k_now,
                      "holding": holding, "val_now": round(val_now, 5), "method": METHOD_BY_ROW.get(cid, METHOD_BY_SUB.get(sid, "Other"))})
dash = json.load(open("research/acc/live/dashboard.json"))
pts = [p for p in dash["scores"]["points"] if p["at"] >= "2026-09-27T22:40"]
bym = {}
for x in lines:
    m = bym.setdefault(x["method"], {"lines": 0, "now": 0.0, "held": 0})
    m["lines"] += 1; m["now"] += x["val_now"]; m["held"] += x["holding"]
out = {"built": dash["summary"]["updatedAt"], "summary": dash["summary"], "points": pts, "lines": lines,
       "byMethod": sorted(({"method": k, **v, "now": round(v["now"], 4)} for k, v in bym.items()), key=lambda d: -d["now"])}
json.dump(out, open("tools/acc/dashboard/results_data.json", "w"), indent=1)
print(len(lines), "lines;", sum(x["holding"] for x in lines), "still at record;", round(sum(x["val_now"] for x in lines), 4), "points now")
for m in out["byMethod"]: print(m)
print(pts[0], pts[-1])
