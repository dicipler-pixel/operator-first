#!/usr/bin/env python3
# SCRIPT: atlas_export
"""atlas_export v1 — regenerate the Atlas console snapshot from the event stream.

The snapshot is a DERIVED VIEW. `ledger/events/stream_v1.jsonl` is the record;
this rebuilds the view from it and may be deleted and rebuilt at any time.

Until now the exporter lived only in session notes, which meant a committed
derived artifact with no committed generator -- exactly the drift this project
refuses elsewhere (see the blueprint-ledger discipline: a generated file that is
not regenerable is just a stale file with extra steps). This closes that.

    python3 tools/acc/atlas_export_v1.py            # rebuild the snapshot
    python3 tools/acc/atlas_export_v1.py --check    # non-zero if stale
"""
import argparse, json, os, sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
STREAM = ROOT / "ledger" / "events" / "stream_v1.jsonl"
OUT    = ROOT / "ledger" / "atlas" / "snapshot_v1.json"

ITEM_KINDS = {"atlas-item", "prediction", "planned-test", "eye-reading",
              "combined-result", "verification", "relationship", "evidence",
              "recommendation", "remix", "search-transition"}

def events():
    with open(STREAM, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try: yield json.loads(line)
            except Exception: continue   # a torn tail line is not a view input

def item_of(rec):
    b = rec.get("body") or {}
    return b.get("item_id") or b.get("claim_id")

def build():
    items = defaultdict(lambda: {"head": None, "counts": Counter(), "events": []})
    index, failures, relationships = [], [], []
    eye_states = Counter()
    total = 0
    for rec in events():
        total += 1
        kind = rec.get("kind"); b = rec.get("body") or {}
        iid = item_of(rec)
        if kind == "eye-reading" and b.get("state"):
            eye_states[b["state"]] += 1
        if kind == "atlas-item" and iid:
            items[iid]["head"] = dict(b)
        if iid and kind in ITEM_KINDS:
            items[iid]["counts"][kind] += 1
            items[iid]["events"].append({"seq": rec.get("seq"), "kind": kind, "body": b})
        if kind == "index-entry" or (kind == "evidence" and b.get("ref")):
            index.append({"seq": rec.get("seq"), "kind": b.get("kind") or b.get("class"),
                          "ref": b.get("ref"), "title": b.get("title"),
                          "status": b.get("status"), "seen": b.get("seen"),
                          "source": b.get("source")})
        if kind == "failure" or (isinstance(b.get("defect"), str)):
            failures.append({"seq": rec.get("seq"), "component": b.get("component"),
                             "defect": b.get("defect"), "caught_by": b.get("caught_by"),
                             "fix": b.get("fix")})
        if kind == "relationship":
            relationships.append({"seq": rec.get("seq"), "relation": b.get("relation"),
                                  "source": b.get("source"), "target": b.get("target"),
                                  "evidence": b.get("evidence")})
    out = {
        "generated_from": "ledger/events/stream_v1.jsonl",
        "total_events": total,
        "items": {k: {"head": v["head"], "counts": dict(v["counts"]), "events": v["events"]}
                  for k, v in items.items() if v["head"] is not None},
        "index": index,
        "failures": failures,
        "relationships": relationships,
        "eye_states": dict(eye_states),
    }
    return out

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    snap = build()
    text = json.dumps(snap, indent=1, sort_keys=False)
    if a.check:
        cur = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        try: same = json.loads(cur) == snap
        except Exception: same = False
        if not same:
            print("atlas_export: snapshot_v1.json is stale — run tools/acc/atlas_export_v1.py")
            return 1
        print("atlas_export: snapshot up to date"); return 0
    OUT.write_text(text, encoding="utf-8")
    print(f"atlas_export: wrote {OUT.relative_to(ROOT)}")
    print(f"  events={snap['total_events']}  items={len(snap['items'])}  "
          f"index={len(snap['index'])}  failures={len(snap['failures'])}  "
          f"relationships={len(snap['relationships'])}")
    print(f"  eye states: {snap['eye_states']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
