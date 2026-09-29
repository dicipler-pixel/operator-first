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
    "ac-04612": "Easy-rows lane fe", "sac-04612": "Easy-rows lane fe", "ac-09507": "Easy-rows lane fe", "sac-09507": "Easy-rows lane fe",
    "ac-03714": "Session 1 road11", "sac-03714": "Session 1 road11", "ac-04308": "Session 1 road11", "sac-04308": "Session 1 road11",
    "ac-00905": "Session 1 road11", "sac-00905": "Session 1 road11", "ac-07548": "Easy-rows lane fe", "sac-07548": "Easy-rows lane fe",
    "ac-02007": "Easy-rows lane fe", "sac-02007": "Easy-rows lane fe", "sac-00797": "Easy-rows lane fe ((y,x) finish)",
    "ac-03040": "Easy-rows lane fe", "sac-03040": "Easy-rows lane fe", "sac-00826": "Easy-rows lane fe", "sac-00201": "yx_mid (Stable = AC+1)",
    "sac-01639": "yx_mid (Stable = AC+1)", "sac-05612": "Astra ranked list", "ac-07188": "Two-eyes ranked lane rk2", "sac-07188": "Two-eyes ranked lane rk2",
    "ac-01089": "Easy-rows lane fe", "sac-01089": "Easy-rows lane fe", "sac-05668": "yx_mid (Stable = AC+1)",
    "ac-08883": "Easy-rows lane fe", "sac-08883": "Easy-rows lane fe", "ac-01542": "Astra easy pool", "sac-01542": "Astra easy pool",
    "ac-09729": "Fresh-value lane fvb", "sac-09729": "Fresh-value lane fvb", "ac-08638": "Astra easy pool", "sac-08638": "Astra easy pool",
    "ac-06591": "Astra easy pool", "sac-06591": "Astra easy pool", "ac-05229": "Astra easy pool", "ac-02649": "Astra easy pool", "sac-02649": "Astra easy pool",
    "ac-06015": "Astra easy pool", "sac-06015": "Astra easy pool", "ac-01738": "Astra easy pool", "sac-01738": "Astra easy pool",
    "ac-01561": "Session 1 family lane", "sac-01561": "Session 1 family lane", "ac-04062": "Fresh-value lane fvb", "sac-04062": "Fresh-value lane fvb",
    "ac-09550": "Astra easy pool", "sac-09550": "Astra easy pool", "ac-06183": "Astra easy pool", "sac-06183": "Astra easy pool", "ac-08825": "Astra easy pool", "sac-08825": "Astra easy pool", "ac-01929": "Astra easy pool", "sac-01929": "Astra easy pool",
    "ac-04037": "Astra easy pool", "sac-04037": "Astra easy pool", "ac-01404": "Astra easy pool", "sac-01404": "Astra easy pool", "ac-05630": "Astra easy pool", "sac-05630": "Astra easy pool", "ac-02655": "Astra easy pool", "sac-02655": "Astra easy pool", "ac-08204": "Astra easy pool", "sac-08204": "Astra easy pool",
    "ac-09870": "two-eyes beam (fresh value, bottom half)", "sac-09870": "two-eyes beam (fresh value, bottom half)", "ac-07055": "two-eyes beam (fresh easy)", "sac-07055": "two-eyes beam (fresh easy)",
    "ac-06766": "Astra easy pool", "sac-06766": "Astra easy pool", "ac-09685": "Astra easy pool", "sac-09685": "Astra easy pool", "ac-02182": "Astra easy pool", "sac-02182": "Astra easy pool", "ac-01503": "Astra easy pool", "sac-01503": "Astra easy pool", "ac-06503": "Astra easy pool", "sac-06503": "Astra easy pool", "ac-09774": "Astra easy pool", "sac-09774": "Astra easy pool", "ac-07837": "Astra easy pool", "sac-07837": "Astra easy pool", "ac-07443": "Astra easy pool", "sac-07443": "Astra easy pool", "ac-09193": "Astra easy pool", "sac-09193": "Astra easy pool", "ac-01548": "Astra easy pool", "sac-01548": "Astra easy pool", "ac-07665": "Astra easy pool", "sac-07665": "Astra easy pool", "ac-00621": "Astra easy pool", "sac-00621": "Astra easy pool", "ac-04414": "Astra easy pool", "sac-04414": "Astra easy pool", "ac-02907": "Astra easy pool", "sac-02907": "Astra easy pool", "ac-06391": "Astra easy pool", "sac-06391": "Astra easy pool", "ac-03389": "Astra easy pool", "sac-03389": "Astra easy pool", "ac-04702": "Astra easy pool", "sac-04702": "Astra easy pool", "ac-04688": "Astra easy pool", "sac-04688": "Astra easy pool",
    "ac-09763": "two-eyes beam (fresh easy)", "sac-09763": "two-eyes beam (fresh easy)", "ac-07893": "two-eyes beam (fresh easy)",
    "ac-05400": "two-eyes beam (fresh easy)", "sac-05400": "two-eyes beam (fresh easy)", "ac-06137": "two-eyes beam (fresh easy)", "sac-06137": "two-eyes beam (fresh easy)", "ac-06124": "two-eyes beam (fresh value, bottom half)", "sac-06124": "two-eyes beam (fresh value, bottom half)",
    "ac-08398": "two-eyes beam (fresh value)", "sac-08398": "two-eyes beam (fresh value)", "ac-05871": "Astra easy pool", "sac-05871": "Astra easy pool", "ac-09663": "Astra easy pool", "sac-09663": "Astra easy pool",
    "ac-00253": "Astra easy pool", "sac-00253": "Astra easy pool", "ac-00654": "Astra easy pool", "sac-00654": "Astra easy pool", "ac-01081": "Astra easy pool", "sac-01081": "Astra easy pool", "ac-01815": "Astra easy pool", "sac-01815": "Astra easy pool", "ac-02062": "Astra easy pool", "sac-02062": "Astra easy pool", "ac-02174": "Astra easy pool", "sac-02174": "Astra easy pool", "ac-04296": "Astra easy pool", "sac-04296": "Astra easy pool", "ac-04838": "Astra easy pool", "sac-04838": "Astra easy pool", "ac-06405": "Astra easy pool", "sac-06405": "Astra easy pool", "ac-06511": "Astra easy pool", "sac-06511": "Astra easy pool", "ac-06513": "Astra easy pool", "sac-06513": "Astra easy pool", "ac-07358": "Astra easy pool", "sac-07358": "Astra easy pool", "ac-07678": "Astra easy pool", "sac-07678": "Astra easy pool", "ac-07701": "Astra easy pool", "sac-07701": "Astra easy pool", "ac-07950": "Astra easy pool", "sac-07950": "Astra easy pool",
    "ac-07550": "two-eyes beam (fresh easy)", "sac-07550": "two-eyes beam (fresh easy)"}
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
