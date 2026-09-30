#!/usr/bin/env python3
"""Scout: low-team-count rows where the team already has a road, ranked by what a few moves would pay.

Reads only local data (0 API calls): the newest board snapshots in research/acc/live/boards/, the UPG-H ledger
(every checked road, what we already hold, heat, open tasks) and every WORKING_*.md claim. Writes
research/acc/live/SCOUT_latest.md (team-readable) and research/acc/upgh/cache/scout_latest.json.

Sections, best value first:
  SEND   our checked road is at or under the record and not yet held: it belongs in the next send
  LOST   we held a line, the record has since dropped below it (a rival moved): the gap is fresh and small
  TWIN   we hold the AC record but not the Stable twin (Stable record = AC + 1: (y,x) finish; AC + 2: P + [16,15])
  NEAR   k <= max_k, our road 1-3 over the record
  ROAD   k <= max_k, our road 4-10 over the record: shorten lanes (window, DP, tail, cross-road splice)
Value: a beat pays 1.0, a tie 2^-k (k = teams holding the record now). Rows claimed in a WORKING file show the claimant.

usage: python3 tools/acc/upgh/scout.py [--max-k 3] [--top 25] [--no-write]
"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from harness import Harness  # noqa: E402
from sources import load_board  # noqa: E402

REPO = HERE.parents[2]


def newest(pattern):
    files = sorted(glob.glob(str(REPO / pattern)))
    return Path(files[-1]) if files else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-k", type=int, default=3)
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args()

    h = Harness(config_path=HERE / "config.json", state_dir=REPO / "research/acc/upgh", repo=REPO)
    st = h.state()
    held = h.held(st)
    claims = h.external_claims()
    fa, fs = newest("research/acc/live/boards/ac_2026*.json.gz"), newest("research/acc/live/boards/stable_ac_2026*.json.gz")
    if not fa or not fs:
        sys.exit("scout: no board snapshots in research/acc/live/boards/")
    board = {"ac": load_board(fa), "sac": load_board(fs)}
    age_min = int((time.time() - min(fa.stat().st_mtime, fs.stat().st_mtime)) / 60)
    running = {r for t in st.tasks.values() if t["status"] in ("queued", "claimed") for r in t["contract"].get("rows", [])}
    heat = {}
    for (row, _), n in st.heat.items():
        heat[row] = heat.get(row, 0) + n

    def info(cid):
        tr = "sac" if cid.startswith("sac-") else "ac"
        return board[tr].get(cid) or {}

    def who(cid):
        num = cid.split("-")[1]
        if num in claims:
            return claims[num].replace("WORKING_", "").replace(".md", "")
        return "upgh (running)" if cid in running else ""

    sections = {k: [] for k in ("SEND", "LOST", "TWIN", "NEAR", "ROAD")}
    for cid, best in st.best.items():
        b = info(cid)
        rec, k = b.get("record"), b.get("k") or 0
        if rec is None or b.get("status") not in (None, "solved", "open"):
            continue
        ours, hv = best["length"], held.get(cid)
        gap = ours - rec
        tie = 2.0 ** (-k) if k else 1.0
        base = {"row": cid, "record": rec, "k": k, "ours": ours, "held": hv, "gap": gap,
                "heat": heat.get(cid, 0), "who": who(cid)}
        if gap <= 0 and (hv is None or hv > ours):
            sections["SEND"].append({**base, "value": 1.0 if gap < 0 else tie})
            continue
        if k > a.max_k:
            continue
        if hv is not None and hv > rec and hv - rec <= 3:
            sections["LOST"].append({**base, "value": tie})
        elif 1 <= gap <= 3:
            sections["NEAR"].append({**base, "value": tie + 0.3 * 1.0 / gap})
        elif 4 <= gap <= 10:
            sections["ROAD"].append({**base, "value": tie / gap})
    # AC record held, Stable twin not held
    for cid, hv in held.items():
        if not cid.startswith("ac-"):
            continue
        num = cid[3:]
        a_b, s_b = info(cid), info("sac-" + num)
        if a_b.get("record") is None or s_b.get("record") is None or hv > a_b["record"]:
            continue
        sk = s_b.get("k") or 0
        if sk > a.max_k or (held.get("sac-" + num) is not None and held["sac-" + num] <= s_b["record"]):
            continue
        d = s_b["record"] - a_b["record"]
        route = {1: "(y,x) finish", 2: "P + [16,15]"}.get(d, "Stable +%d" % d)
        sb = st.best.get("sac-" + num)
        sections["TWIN"].append({"row": "sac-" + num, "record": s_b["record"], "k": sk, "ours": sb["length"] if sb else None,
                                 "held": held.get("sac-" + num), "gap": (sb["length"] - s_b["record"]) if sb else None,
                                 "heat": heat.get("sac-" + num, 0), "who": who("sac-" + num), "route": route,
                                 "value": 2.0 ** (-sk) if sk else 1.0})
    for s in sections.values():
        s.sort(key=lambda r: (-r["value"], r["gap"] if r["gap"] is not None else 99, r["row"]))

    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%MZ")
    out = ["# SCOUT: low-k rows where the team has a road (%s)" % now, "",
           "Built by `tools/acc/upgh/scout.py` from the newest boards (%s, %s; %d min old) and the UPG-H ledger. 0 API calls."
           % (fa.name, fs.name, age_min),
           "Value: beat 1.0, tie 2^-k. `who` = the lane that claims the row (WORKING files) or `upgh (running)`. "
           "Take an unclaimed row by writing it in your WORKING file. Scoring lines go to `queue/`.", ""]
    heads = {"SEND": "SEND: our road is at or under the record, not held yet (next send)",
             "LOST": "LOST: we held it, a rival moved the record 1-3 below our line",
             "TWIN": "TWIN: we hold the AC record, not the Stable twin",
             "NEAR": "NEAR: 1-3 over, k <= %d" % a.max_k,
             "ROAD": "ROAD: 4-10 over, k <= %d (shorten lanes)" % a.max_k}
    for name, rows in sections.items():
        out.append("## %s (%d)" % (heads[name], len(rows)))
        if not rows:
            out += ["(none)", ""]
            continue
        out.append("| row | record | k | ours | held | gap | heat | who | value |" + (" route |" if name == "TWIN" else ""))
        out.append("|---|---|---|---|---|---|---|---|---|" + ("---|" if name == "TWIN" else ""))
        for r in rows[:a.top]:
            out.append("| %s | %s | %s | %s | %s | %s | %s | %s | %.3f |%s" % (
                r["row"], r["record"], r["k"], r["ours"], r["held"] if r["held"] is not None else "",
                "+%d" % r["gap"] if r["gap"] is not None and r["gap"] > 0 else (r["gap"] if r["gap"] is not None else ""),
                r["heat"], r["who"], r["value"], (" %s |" % r["route"]) if name == "TWIN" else ""))
        if len(rows) > a.top:
            out.append("(%d more in research/acc/upgh/cache/scout_latest.json)" % (len(rows) - a.top))
        out.append("")
    text = "\n".join(out) + "\n"
    summary = {k: len(v) for k, v in sections.items()}
    print("scout %s board %d min old: %s" % (now, age_min, summary))
    for name in ("SEND", "LOST", "TWIN", "NEAR"):
        for r in sections[name][:6]:
            print("  %-4s %-10s rec %-4s k %-2s ours %-4s gap %-3s heat %-2s %s" % (
                name, r["row"], r["record"], r["k"], r["ours"], r["gap"], r["heat"], r["who"]))
    if not a.no_write:
        (REPO / "research/acc/live/SCOUT_latest.md").write_text(text, encoding="utf-8")
        cache = REPO / "research/acc/upgh/cache"
        cache.mkdir(parents=True, exist_ok=True)
        (cache / "scout_latest.json").write_text(json.dumps({"at": now, "board_age_min": age_min, "sections": sections}))


if __name__ == "__main__":
    main()
