#!/usr/bin/env python3
"""Quiet wake: reopen parked misses whose row received a NEW team road that did not improve our best.

The harness wakes a parked miss when our best path on its row improves (event new_path). A teammate's road of equal or greater
length from a different lineage changes nothing in `best`, so it wakes nothing, yet it is exactly the new material a splice or
cross needs. For every parked, un-reopened miss whose reopen_when is {event: new_path, row: R}, this script looks for team roads
on R (twin_lookup.team_roads: ledger + research/acc/live/*.txt + ACC_*.txt) that live in files modified after the miss was
parked and that differ from every road the ledger already held when it was parked. If any exist, it sends the wake
{event: new_path, row: R, lineage: <hash of the new roads>}: the extra key matches the parked reopen_when and makes the wake
key distinct, so each new lineage set wakes a row once. Near-record rows only (gap <= --gap to the live record). 0 API, no model.

usage: python3 tools/acc/upgh/quiet_wake.py [--gap 2] [--kmax 3] [--limit 12] [--dry]"""
import argparse
import glob
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import twin_lookup as T  # noqa: E402
from sources import load_board  # noqa: E402

REPO = T.REPO


def ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gap", type=int, default=2)
    ap.add_argument("--kmax", type=int, default=3)
    ap.add_argument("--limit", type=int, default=12)
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    st = T.h.state()
    boards = {}
    for kind in ("ac", "stable_ac"):
        boards.update(load_board(sorted(glob.glob(str(REPO / ("research/acc/live/boards/%s_2026*.json.gz" % kind))))[-1]))
    never = set(T.h.cfg["gates"].get("never_rows", []))
    seq_at, held_before = {}, {}
    for i, line in enumerate(open(REPO / "research/acc/upgh/ledger.jsonl", encoding="utf-8"), 1):
        d = json.loads(line)
        seq_at[i] = d["at"]
        if d.get("kind") == "path.best":
            held_before.setdefault(d["data"].get("cid"), []).append((i, tuple(d["data"]["moves"])))
    roads = T.team_roads()
    files_mtime = {}
    out, cand = [], []
    for p in st.parked.values():
        rw = p.get("reopen_when") or {}
        row = rw.get("row")
        if rw.get("event") != "new_path" or not row or p.get("reopened_by") or row.split("-")[1] in never:
            continue
        b, rec = st.best.get(row), boards.get(row, {}).get("record")
        k = boards.get(row, {}).get("k") or 99
        if not b or rec is None or not 1 <= len(b["moves"]) - rec <= a.gap or k > a.kmax:
            continue
        parked_at = ts(seq_at.get(p["seq"], "2026-01-01T00:00:00Z"))
        known = {m for s, m in held_before.get(row, []) if s <= p["seq"]}
        fresh = []
        base = row[1:] if row.startswith("sac-") else row          # Stable rows: the AC roads are the material
        for path, src in roads.get(base, {}).items():
            f = REPO / src if not src.startswith("UPG-H") else None
            if f is None or not f.exists():
                continue
            mt = files_mtime.setdefault(f, f.stat().st_mtime)
            if mt > parked_at and path not in known:
                fresh.append(path)
        if not fresh:
            continue
        cand.append((k, len(b["moves"]) - rec, row, p["task"], fresh, len(b["moves"]), rec))
    rows_done = set()
    for k, gap, row, task, fresh, ours, rec in sorted(cand):
        if row not in rows_done and len(rows_done) >= a.limit:
            continue
        rows_done.add(row)
        lineage = hashlib.sha256(json.dumps(sorted(fresh)).encode()).hexdigest()[:12]
        ev = {"event": "new_path", "row": row, "lineage": lineage}
        res = None if a.dry else T.h.wake(ev)
        out.append((row, task, len(fresh), ours, rec, res and res.get("reopened")))
    seen = set()
    for row, task, n, ours, rec, reopened in out:
        print("%s parked %s: %d new team road(s); ours %d, record %d -> %s" % (row, task, n, ours, rec,
              "dry" if a.dry else (reopened or "duplicate/none")))
        seen.add(row)
    print("rows woken: %d" % len(seen))


if __name__ == "__main__":
    main()
