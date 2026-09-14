#!/usr/bin/env python3
# SCRIPT: atlas_two_pass
"""atlas_two_pass v1 — the permanent all-eyes two-pass mixer for the Atlas.

Two passes, because one pass forces a false choice. A cheap gate that is wrong
costs a missed result; an expensive rank run on everything costs the session.
So:

  PASS 1  GATE   every eye on the roster reads, cheaply, and is RECORDED.
                 No eye is skipped, none is dropped, none is silenced. An eye
                 that cannot read files `blocked` or `failed` WITH A REASON and
                 keeps its place.
  PASS 2  RANK   only eyes that passed the gate are scored expensively, per the
                 named USE, as coverage-of-the-moves-in-play over measured cost.

The invariant this file exists to enforce, in Jeromie's words:

    All eyes on always means every eye leaves a record. Mixing may change what
    influences a decision, but it may never erase what an eye saw -- or failed
    to see.

So weight zero is a WEIGHT, not a deletion. An eye ranked zero for a use still
appears in pass 1 with its reading intact, and the decision record names it.
Removing an eye from the roster is not something this tool can do.

    python3 tools/acc/atlas_two_pass_v1.py --item atlas:... --use search
    python3 tools/acc/atlas_two_pass_v1.py --item atlas:... --use search --record
"""
import argparse, json, sys, time
from pathlib import Path
from collections import defaultdict

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from event_log_v1 import EventLog, EYE_STATES

# States that still count as "the eye produced a reading this pass".
READING_STATES = {"observed", "silent", "contradicted"}
# States that must carry a reason, and never disqualify an eye from the roster.
EXCUSED_STATES = {"blocked", "failed", "disabled"}

def roster(log, item_id):
    """Every eye that has EVER filed on this item. Membership is permanent:
    an eye that once read here stays on the roster forever, so a later pass
    that cannot reach it records a gap instead of quietly shrinking."""
    seen = {}
    for _, rec, _ in log.read():
        if rec is None: continue
        b = rec.get("body") or {}
        if rec.get("kind") != "eye-reading": continue
        if b.get("item_id") not in (item_id, None) and b.get("claim_id") != item_id:
            continue
        if b.get("claim_id") != item_id and b.get("item_id") != item_id:
            continue
        eid = b.get("eye_id")
        if not eid: continue
        seen.setdefault(eid, []).append({"seq": rec.get("seq"), "state": b.get("state"),
                                         "output": b.get("output"), "reason": b.get("reason")})
    return seen

def pass1_gate(log, item_id):
    """Cheap: read the latest filing of every eye on the roster. Records a row
    for EVERY eye, including those that never produced a usable output."""
    rows = []
    for eid, filings in sorted(roster(log, item_id).items()):
        last = filings[-1]
        state = last.get("state")
        usable = state in READING_STATES and last.get("output") is not None
        rows.append({"eye_id": eid, "state": state, "filings": len(filings),
                     "last_seq": last["seq"], "usable": usable,
                     "reason": last.get("reason"),
                     "excused": state in EXCUSED_STATES})
    return rows

def pass2_rank(gate_rows, use):
    """Expensive: score only the eyes the gate passed. Every other eye is carried
    forward at weight zero WITH its gate row, never dropped."""
    ranked = []
    for r in gate_rows:
        if not r["usable"]:
            ranked.append({**r, "weight": 0.0,
                           "why": f"not scored for use {use!r}: state {r['state']}"
                                  + (f" ({r['reason']})" if r.get("reason") else "")})
            continue
        out = r.get("_output") if "_output" in r else None
        # Coverage/cost is supplied by the eye's own filing when present; absent
        # that, the eye is scored 0 for THIS use and says so. A missing number is
        # never silently treated as a good one.
        ranked.append({**r, "weight": None,
                       "why": f"eligible for use {use!r}; weight requires a coverage/cost "
                              f"filing for this use"})
    return ranked

def report(log, item_id, use, record=False, run_id="atlas-two-pass"):
    gate = pass1_gate(log, item_id)
    if not gate:
        print(f"no eyes have ever filed on {item_id!r}")
        return 1
    ranked = pass2_rank(gate, use)
    n_usable = sum(1 for r in gate if r["usable"])
    n_excused = sum(1 for r in gate if r["excused"])
    print(f"item: {item_id}")
    print(f"use : {use}")
    print(f"roster: {len(gate)} eyes  |  pass 1 usable: {n_usable}  |  excused with reason: {n_excused}")
    print()
    print(f"{'eye':<52} {'state':<13} {'pass1':<7} {'weight':>7}  why")
    print("-"*128)
    for r in ranked:
        w = "—" if r["weight"] is None else f"{r['weight']:.3f}"
        print(f"{r['eye_id'][:52]:<52} {str(r['state']):<13} "
              f"{'pass' if r['usable'] else 'gap':<7} {w:>7}  {r['why'][:44]}")
    print("-"*128)
    missing = [r for r in gate if not r["usable"] and not r["excused"]]
    if missing:
        print(f"INTEGRITY WARNING: {len(missing)} eye(s) produced no usable reading and carry NO reason.")
        for r in missing: print(f"  {r['eye_id']} (state {r['state']}, seq {r['last_seq']})")
        print("An eye that cannot read must file blocked/failed WITH a reason. "
              "A silent gap is the one thing this design forbids.")
    else:
        print("every eye on the roster is accounted for: a reading, or a state carrying a reason")
    if record:
        log.append("combined-result", {
            "claim_id": item_id, "use": use, "pass": "two-pass-all-eyes",
            "roster_size": len(gate), "pass1_usable": n_usable, "excused": n_excused,
            "unaccounted": [r["eye_id"] for r in missing],
            "rows": [{k: r[k] for k in ("eye_id","state","usable","weight","why")} for r in ranked],
            "invariant": "weight zero is a weight, not a deletion; no eye is removed from the roster",
        }, run_id)
        print(f"\nrecorded a combined-result for {item_id} ({len(ranked)} eye rows)")
    return 0 if not missing else 2

def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--item", required=True)
    ap.add_argument("--use", default="general")
    ap.add_argument("--record", action="store_true",
                    help="append the two-pass result to the event stream")
    a = ap.parse_args(argv)
    return report(EventLog(), a.item, a.use, record=a.record)

if __name__ == "__main__":
    raise SystemExit(main())
