#!/usr/bin/env python3
"""Build the ACC dashboard data (one JSON object per dashboard doc) from local files only; no API calls.

  python3 tools/acc/dashboard_data.py [--work SCRATCH/work] [--out research/acc/live/dashboard.json]

Docs: summary, scores, days, standing, rivals, searches, methods, log. The published tracker page
reads them from its database (collection `dash`); push with ArtifactData batch `set dash/<name>`.
"""
import argparse, collections, glob, gzip, json, os, pathlib, sys, datetime as dt

REPO = pathlib.Path(__file__).resolve().parents[2]
LIVE = REPO / "research" / "acc" / "live"
sys.path.insert(0, str(REPO / "tools" / "acc"))
import sair_api as s  # noqa: E402

US = "ACC01-T00051"


def jl(path):
    out = []
    if os.path.exists(path):
        for line in open(path):
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except ValueError:
                    pass
    return out


def history():
    """Our submissions: history pull + later local sends, oldest first; and our best per row."""
    h = json.load(open(sorted(glob.glob(str(LIVE / "mine_*.json")))[-1]))
    subs = {}
    for it in h["items"]:
        subs[it["submissionId"]] = {"id": it["submissionId"], "at": it["receivedAt"][:16] + "Z",
                                    "results": it["results"] or []}
    for r in jl(LIVE / "submit_log.jsonl"):
        if r.get("event") == "result" and r["submissionId"] not in subs:
            a = r["at"]
            subs[r["submissionId"]] = {"id": r["submissionId"],
                                       "at": f"{a[:4]}-{a[4:6]}-{a[6:8]}T{a[9:11]}:{a[11:13]}Z",
                                       "results": r["results"]}
    subs = sorted(subs.values(), key=lambda x: x["at"])
    best = {}
    for x in subs:
        for r in x["results"]:
            if r.get("ok") and isinstance(r.get("length"), int):
                c = r["challenge_id"]
                best[c] = min(r["length"], best.get(c, 999))
    return subs, best


def leaderboards():
    """[(generatedAt, problem, items)] one per SAIR refresh we saved."""
    seen = {}
    for f in sorted(glob.glob(str(LIVE / "boards" / "leaderboard_*.json.gz"))):
        d = json.load(gzip.open(f, "rt"))["data"]
        prob = "ac" if os.path.basename(f).startswith("leaderboard_ac_") else "stable_ac"
        seen[(d.get("generatedAt"), prob)] = d["items"]
    return seen


def build(work):
    subs, best = history()
    board = s.load_board(LIVE / "boards")
    # rows we sent after the newest board refresh: the board doesn't count us yet
    newest = sorted(glob.glob(str(LIVE / "boards" / "ac_*.json.gz")))[-1]
    gen_at = json.load(gzip.open(newest, "rt"))["data"].get("generatedAt", "")[:16] + "Z"
    pending = {r["challenge_id"] for x in subs if x["at"] > gen_at for r in x["results"] if r.get("ok")}
    lbs = leaderboards()

    # standing: gap to the live record for every row SAIR accepted from us
    buckets = ["0", "1", "2", "3", "4-5", "6-10", "11+"]
    gaps = {p: dict.fromkeys(buckets, 0) for p in ("ac", "sac")}
    ties = {p: collections.Counter() for p in ("ac", "sac")}
    est = {"ac": 0.0, "sac": 0.0}
    for c, L in best.items():
        rec, k = board.get(c, (None, 0))
        if rec is None:
            continue
        p = "sac" if c.startswith("sac") else "ac"
        g = L - rec
        b = "0" if g <= 0 else str(g) if g <= 3 else "4-5" if g <= 5 else "6-10" if g <= 10 else "11+"
        gaps[p][b] += 1
        if g <= 0:
            if c in pending:
                k = 1 if g < 0 else k + 1          # our line isn't on the board yet
            ties[p][min(k, 12)] += 1
            est[p] += 2.0 ** (1 - k)
    standing = {"gaps": gaps, "buckets": buckets,
                "ties": {p: {str(k): ties[p][k] for k in range(1, 13)} for p in ties}}

    # score history from saved leaderboard refreshes
    pts = collections.defaultdict(dict)
    for (gen, prob), items in lbs.items():
        for x in items:
            if x["team"]["teamNumber"] == US:
                key = "ac" if prob == "ac" else "sac"
                pts[gen][key] = float(x["score"])
                pts[gen][key + "Rank"] = x["rank"]
                pts[gen][key + "Teams"] = len(items)
    scores = [{"at": g, **v} for g, v in sorted(pts.items()) if "ac" in v and "sac" in v]

    # submissions per day
    days = collections.OrderedDict()
    for x in subs:
        d = x["at"][:10]
        e = days.setdefault(d, {"d": d, "subs": 0, "ac": 0, "sac": 0})
        e["subs"] += 1
        for r in x["results"]:
            if r.get("ok"):
                e["sac" if r["challenge_id"].startswith("sac") else "ac"] += 1

    # rivals: latest leaderboard, 6 teams above us and 2 below, with rows held alone when we have them
    teams_snap = {}
    for prob in ("ac", "stable_ac"):
        files = sorted(glob.glob(str(LIVE / "teams" / f"{prob}_*.json.gz")))
        if files:
            teams_snap[prob] = json.load(gzip.open(files[-1], "rt"))["teams"]
    rivals = {}
    for prob, key in (("ac", "ac"), ("stable_ac", "sac")):
        latest = max((g for g, p in lbs if p == prob), default=None)
        if not latest:
            continue
        items = sorted(lbs[(latest, prob)], key=lambda x: x["rank"])
        me = next(x for x in items if x["team"]["teamNumber"] == US)
        near = [x for x in items if me["rank"] - 6 <= x["rank"] <= me["rank"] + 2]
        snap = teams_snap.get(prob, {})
        rivals[key] = [{"rank": x["rank"], "name": x["team"]["teamName"] or x["team"]["teamNumber"],
                        "score": float(x["score"]), "rows": x["currentBestCount"],
                        "alone": sum(1 for v in snap.get(x["team"]["teamNumber"], {}).get("rows", {}).values()
                                     if v[1] == 1) if x["team"]["teamNumber"] in snap else None,
                        "us": x["team"]["teamNumber"] == US} for x in near]
        rivals[key + "At"] = latest

    # searches (scratch files; absent files just drop out)
    searches = []
    hunt = [l for l in open(work + "/hunt_ac-06969_summary.log")] if os.path.exists(work + "/hunt_ac-06969_summary.log") else []
    hb = min((int(l.split("ac,sac ")[1].split()[0]) for l in hunt if "ac,sac " in l and l.split("ac,sac ")[1].split()[0].isdigit()), default=None)
    caps = [l for l in open(work + "/cap_ac-06969.log")] if os.path.exists(work + "/cap_ac-06969.log") else []
    capmax = max((int(l.split("cap=")[1].split()[0]) for l in caps if "cap=" in l), default=None)
    searches.append({"key": "ac-06969", "row": "ac-06969", "goal": "Tie Ryan's best row", "record": 38, "k": 2,
                     "best": 41, "status": "paused",
                     "detail": f"Exact: no path of 38 or fewer stays within total length {capmax or 32} for its first "
                               f"29 moves (caps 27–32 proved). Beam restarts: {len(hunt)} runs, best {hb}. "
                               "Paused: caps 33+ need more memory than we have; posted to helpers."})
    ec = jl(work + "/easy_cap.jsonl")
    eb = jl(work + "/beam_easy.jsonl")
    T = {t["id"]: t for t in json.load(open(work + "/easy_cap_targets.json"))} if os.path.exists(work + "/easy_cap_targets.json") else {}
    hits = [r["id"] for r in ec if T.get(r["id"]) and ((r.get("ac_len") or 999) <= (T[r["id"]]["ac_record"] or 0)
                                                     or (r.get("sac_len") or 999) <= (T[r["id"]]["sac_record"] or 0))]
    searches.append({"key": "easy-exact", "row": f"{len(T)} easy rows", "goal": "Rows held by 1–2 teams, record ≤ 36",
                     "record": None, "k": None, "best": None, "status": "running",
                     "detail": f"Exact capped sweep: {len(ec)} of {len(T)} rows done, {len(hits)} with a tie or beat"
                               + (f" ({', '.join(hits)})" if hits else "") + "."})
    for name, label, goal in (("midB", "Mid rows 33–40", "ac-00145 first, then records 33–40 held by 1–6 teams"),
                              ("midC", "Mid rows 25–32", "Records 25–32 held by 1–6 teams (cheapest first)")):
        res = jl(f"{work}/{name}_cap.jsonl")
        TT = {t["id"]: t for t in json.load(open(f"{work}/{name}_targets.json"))} if os.path.exists(f"{work}/{name}_targets.json") else {}
        hh = [r["id"] for r in res if TT.get(r["id"]) and ((TT[r["id"]].get("ac_record") and (r.get("ac_len") or 999) <= TT[r["id"]]["ac_record"])
                                                          or (TT[r["id"]].get("sac_record") and (r.get("sac_len") or 999) <= TT[r["id"]]["sac_record"]))]
        searches.append({"key": name, "row": f"{len(TT)} rows", "goal": goal, "record": None, "k": None, "best": None,
                         "status": "running", "detail": f"Exact capped sweep: {len(res)} of {len(TT)} rows done, "
                                                        f"{len(hh)} with a tie or beat" + (f" ({', '.join(hh)})" if hh else "") + "."})
    bh = [r["id"] for r in eb if r.get("verdict") in ("TIE", "BEAT")]
    searches.append({"key": "easy-beam", "row": f"{len(T)} easy rows", "goal": "Same rows, H-beam",
                     "record": None, "k": None, "best": None, "status": "stopped",
                     "detail": f"H-beam sweep: {len(eb)} of {len(T)} rows done, {len(bh)} ties or beats. "
                               "Stopped: the exact search finds more."})

    methods = [
        {"name": "Adaptive exact capped search", "use": "Short rows held by 1–2 teams", "state": "works",
         "evidence": "sac-03305 tie on a row held by one team (+0.5) at cap 37; ac-03305 at cap 40. Proves the caps below are empty."},
        {"name": "H-beam + T9 finish", "use": "First path on rows with record ≤ ~45", "state": "works",
         "evidence": "Most of our 440+ accepted ties."},
        {"name": "Seeded beam restarts", "use": "Last 1–2 moves on near misses", "state": "works",
         "evidence": "Ties at 30–35 moves (ac-09391, ac-01373, ac-00313)."},
        {"name": "Our AC path + [16,15]", "use": "Free Stable AC ties", "state": "works",
         "evidence": "6 Stable AC ties in submission 2565, no new search."},
        {"name": "(y,x) finish for Stable AC", "use": "Stable AC shorter than AC + 2", "state": "works",
         "evidence": "7 Stable AC lines shorter than team-held lengths (2026-09-24)."},
        {"name": "Window-14 shortening", "use": "Polishing our own paths", "state": "partial",
         "evidence": "2 of 9 paths shortened by 1–2 moves."},
        {"name": "Beam on mid rows (k=2, 44–70)", "use": "", "state": "not yet",
         "evidence": "0 of 34. Record paths climb above what the beam keeps."},
        {"name": "Beam on long rows (≥ 70)", "use": "", "state": "not yet", "evidence": "Path found on 1 of 195."},
        {"name": "Beam on unsolved rows", "use": "", "state": "not yet", "evidence": "0 of 126."},
    ]

    log = [
        {"at": "2026-09-11", "kind": "submit", "text": "First submissions: 21 batches, 617 lines accepted."},
        {"at": "2026-09-18", "kind": "submit", "text": "Big Stable AC push: 529 lines accepted in one day."},
        {"at": "2026-09-24", "kind": "proof", "text": "Exact screen of all 10,115 rows: every distance ≤ 14 decided. 7 Stable AC lines shorter than team-held lengths."},
        {"at": "2026-09-25", "kind": "proof", "text": "Capped proofs: record paths must first grow the relators (ac-00037, ac-00313)."},
        {"at": "2026-09-26", "kind": "proof", "text": "Proof-track write-up: 53 exact optima, board-wide lower bounds, forced humps."},
        {"at": "2026-09-27T22:35Z", "kind": "tool", "text": "SAIR API live from the cloud session: boards, history, team pages."},
    ]
    notes = {"2558": "6 ties (NEW15).", "2565": "6 Stable AC ties from our AC paths + [16,15].",
             "2566": "sac-03305 tie on a row held by one team (+0.5) and ac-03305.",
             "2569": "ac-01629 and sac-01629 ties (+0.19) from exact sweep C."}
    for x in subs:
        if x["id"] in notes:
            ok = sum(1 for r in x["results"] if r.get("ok"))
            log.append({"at": x["at"], "kind": "submit",
                        "text": f"Submission {x['id']}: {ok}/{len(x['results'])} accepted. {notes[x['id']]}"})
    log.sort(key=lambda e: e["at"])

    last = scores[-1] if scores else {}
    today = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d")
    summary = {
        "updatedAt": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ"),
        "leaderboardAt": last.get("at"),
        "ac": {"rank": last.get("acRank"), "teams": last.get("acTeams"), "score": last.get("ac"),
               "estimate": round(est["ac"], 4), "ties": gaps["ac"]["0"]},
        "sac": {"rank": last.get("sacRank"), "teams": last.get("sacTeams"), "score": last.get("sac"),
                "estimate": round(est["sac"], 4), "ties": gaps["sac"]["0"]},
        "sentToday": days.get(today, {}).get("subs", 0), "quota": 40,
        "alone": sum(ties[p][1] for p in ties), "boardAt": gen_at,
        "subsTotal": len(subs),
    }
    return {"summary": summary, "scores": {"points": scores}, "days": {"days": list(days.values())},
            "standing": standing, "rivals": rivals, "searches": {"items": searches},
            "methods": {"items": methods}, "log": {"items": log}}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad/work")
    ap.add_argument("--out", default=str(LIVE / "dashboard.json"))
    ap.add_argument("--page", help="also write the tracker page with this data baked in (fallback before live data)")
    a = ap.parse_args()
    data = build(a.work)
    json.dump(data, open(a.out, "w"), indent=1)
    if a.page:
        tpl = (REPO / "tools" / "acc" / "dashboard" / "acc_tracker_template.html").read_text(encoding="utf-8")
        seed = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
        pathlib.Path(a.page).write_text(tpl.replace("__SEED__", seed), encoding="utf-8")
    print(json.dumps(data["summary"], indent=1))
