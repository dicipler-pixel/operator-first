#!/usr/bin/env python3
"""Team comms sweep for the UPG-H lead: what changed in the repo's message spots since the last sweep.

The team talks through files: UPDATE_/ORDERS_/WORKING_/SESSION*_to_* notes in research/acc/live, scoring lines in
queue/ and inbox/, roads in sweeps/ and exchange/, and Astra's harness messages. Lines that nobody reads cost points
(Bob's ac-08031 tie sat unsent from 07:03Z to 17:36Z on 30 September). This prints every new or changed item since the
last sweep, marks the ones addressed to UPG-H, the lead or Fable, and exits 0. The Drive hub is not visible from here:
the lead checks it with the Drive tools at the same check-in.

usage: python3 tools/acc/upgh/comms.py [--since ISO8601|--hours H] [--no-mark]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
LIVE = REPO / "research/acc/live"
MARK = REPO / "research/acc/upgh/cache/comms_last.json"
SPOTS = [
    ("note", LIVE, re.compile(r"^(UPDATE_|ORDERS_|WORKING_|SESSION\d?_to_|TARGETS_|READY_|OWNER_|GIT_STATUS|ONBOARDING)")),
    ("queue", LIVE / "queue", None),
    ("inbox", LIVE / "inbox", None),
    ("sweeps", LIVE / "sweeps", None),
    ("exchange", LIVE / "exchange", None),
    ("astra", REPO / "research/acc/harness/acc_synthesis/continuation/messages", None),
]
TO_US = re.compile(r"to_(?:[a-z0-9]+_)*(?:upgh|lead|fable|all)\b|to_upgh|UPG-?H|\blead\b|Fable", re.I)


def commit_time(path: Path):
    out = subprocess.run(["git", "-C", str(REPO), "log", "-1", "--format=%ct", "--", str(path)],
                         capture_output=True, text=True).stdout.strip()
    return float(out) if out else None


def sweep(since: float):
    items = []
    for kind, base, pattern in SPOTS:
        if not base.is_dir():
            continue
        files = base.iterdir() if kind == "note" else base.rglob("*")
        for f in files:
            if not f.is_file() or f.name.startswith(".") or "/sent/" in f.as_posix():
                continue
            if pattern and not pattern.match(f.name):
                continue
            when = max(f.stat().st_mtime, commit_time(f) or 0) if kind == "note" else f.stat().st_mtime
            if when <= since:
                continue
            rel = f.relative_to(REPO).as_posix()
            head = f.read_text(encoding="utf-8", errors="replace")[:600] if f.stat().st_size < 5_000_000 else ""
            ours = "upgh" in f.name.lower() and "_to_" in f.name.lower() and f.name.lower().split("_to_")[0].endswith("upgh")
            addressed = bool(TO_US.search(f.name) or TO_US.search(head)) and not ours
            items.append({"kind": kind, "file": rel, "at": dt.datetime.utcfromtimestamp(when).strftime("%H:%MZ"),
                          "addressed": addressed, "ours": ours, "lines": sum(1 for _ in re.finditer(
                              r"\b(?:ac|sac)-\d{5}\s*:\s*\[", head)) if kind in ("queue", "inbox") else None})
    return sorted(items, key=lambda i: (not i["addressed"], i["kind"], i["file"]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since")
    ap.add_argument("--hours", type=float)
    ap.add_argument("--no-mark", action="store_true")
    a = ap.parse_args()
    now = dt.datetime.now(dt.timezone.utc).timestamp()
    if a.since:
        since = dt.datetime.fromisoformat(a.since.replace("Z", "+00:00")).timestamp()
    elif a.hours:
        since = now - a.hours * 3600
    elif MARK.is_file():
        since = json.loads(MARK.read_text())["at"]
    else:
        since = now - 2 * 3600
    items = sweep(since)
    print("comms since %s UTC: %d item(s)" % (dt.datetime.utcfromtimestamp(since).strftime("%Y-%m-%d %H:%M"), len(items)))
    for i in items:
        flag = "TO US " if i["addressed"] else ("ours  " if i["ours"] else "      ")
        extra = "" if i["lines"] is None else "  (%d line(s) in the first 600 chars)" % i["lines"]
        print("  %s%-8s %s  %s%s" % (flag, i["kind"], i["at"], i["file"], extra))
    todo = [i for i in items if i["addressed"] or i["kind"] in ("queue", "inbox")]
    if todo:
        print("act on: read each TO US note and reply in the repo; harvest inbox/queue/sweeps (`upgh harvest`), "
              "then `upgh plan --queue`; send per the standing rule.")
    if not a.no_mark:
        MARK.parent.mkdir(parents=True, exist_ok=True)
        MARK.write_text(json.dumps({"at": now}))


if __name__ == "__main__":
    main()
