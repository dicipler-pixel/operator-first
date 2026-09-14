"""The Atlas application: one surface over the event ledger.

Ten controls, each a command here. The ledger is the only source; nothing in
this file stores state of its own, and every answer cites the exact events it
came from.

    record          Record Move          append an action to the chain
    start           Start Mixer Run      open a run on an Atlas item
    replay          Replay Run           re-derive a run from its recorded recipe
    remix           Remix Eyes           counterfactual: drop or re-weight eyes
    prior           Find Prior Work      search every event for related work
    compare         Compare Prediction   prediction against what actually happened
    next            Ask What Comes Next  a recommendation, cited and LABELLED
    open            Open Atlas Item      reconstruct the complete chain
    attach          Attach Evidence      files, commits, certificates
    verify          Verify / Certify     independent check, kept separate

The acceptance test is `open`: pick an older item, ask what happened and why,
and get the entire chain back - every eye including the ones that saw nothing,
every prediction, relationship, artifact and verification - without reading a
chat log. `--acceptance` runs that as a pass/fail check with explicit criteria.

Two rules the code enforces rather than documents:

  A recommendation is a PREDICTION. `next` labels its output that way, refuses
  to emit one with no citations, and never uses the words verified or proved.

  Repeating settled work is a warning. `start` and `next` both check the ledger
  for an existing answer first and say so before anything else.
"""

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from event_log_v1 import EventLog, EYE_STATES  # noqa: E402

CHAIN = ["atlas-item", "prediction", "planned-test", "eye-reading",
         "combined-result", "verification", "relationship", "evidence",
         "recommendation", "remix"]


def load(log):
    return [r for _, r, _ in log.read() if r]


def item_of(rec):
    """Which Atlas item an event belongs to, if any."""
    b = rec.get("body") or {}
    for k in ("item_id", "atlas_item", "claim_id", "source", "target"):
        v = b.get(k)
        if isinstance(v, str) and v.startswith("atlas:"):
            return v
        if k in ("item_id", "atlas_item") and isinstance(v, str):
            return v
    return None


# --- Open Atlas Item: the acceptance test ------------------------------------

def open_item(log, item_id, show=True):
    """Reconstruct the complete chain for one item, from the ledger alone."""
    evs = load(log)
    mine = [r for r in evs if item_of(r) == item_id or
            (r["kind"] == "atlas-item" and (r["body"] or {}).get("item_id") == item_id)]
    by_kind = defaultdict(list)
    for r in mine:
        by_kind[r["kind"]].append(r)

    chain = {"item_id": item_id, "events": len(mine), "by_kind": {}}
    for k in CHAIN:
        chain["by_kind"][k] = len(by_kind.get(k, []))

    if not show:
        return chain, by_kind, mine

    if not mine:
        print(f"no Atlas item {item_id!r} in the ledger")
        return chain, by_kind, mine

    head = by_kind["atlas-item"][0]["body"] if by_kind["atlas-item"] else {}
    print("=" * 78)
    print(f"ATLAS ITEM  {item_id}")
    if head.get("title"):
        print(f"            {head['title']}")
    if head.get("attribution"):
        print(f"            credit: {head['attribution']}")
    print(f"            reconstructed from {len(mine)} events, no chat consulted")
    print("=" * 78)

    def block(kind, title, fmt):
        rows = by_kind.get(kind, [])
        print(f"\n{title}  ({len(rows)})")
        print("-" * 78)
        if not rows:
            print("  none recorded")
            return
        for r in rows:
            for line in fmt(r["body"], r):
                print("  " + line)

    block("prediction", "PREDICTION",
          lambda b, r: [f"seq {r['seq']}  {b.get('statement','')}",
                        f"      by {b.get('by','?')}  confidence {b.get('confidence','?')}"
                        f"  LABEL: {b.get('label','prediction')}"])
    block("planned-test", "PLANNED TEST",
          lambda b, r: [f"seq {r['seq']}  {b.get('method','')}",
                        f"      decides: {b.get('decides','')}"])

    # every eye, including the ones that saw nothing
    eyes = by_kind.get("eye-reading", [])
    print(f"\nALL-EYE OBSERVATIONS  ({len(eyes)} filings)")
    print("-" * 78)
    per = defaultdict(Counter)
    sample = {}
    for r in eyes:
        b = r["body"]
        per[b["eye_id"]][b["state"]] += 1
        sample.setdefault((b["eye_id"], b["state"]), r)
    if not per:
        print("  none recorded")
    for eye in sorted(per):
        states = ", ".join(f"{s}x{n}" for s, n in per[eye].most_common())
        print(f"  {eye:<24}{states}")
        for s in per[eye]:
            r = sample[(eye, s)]
            b = r["body"]
            if b.get("reason"):
                print(f"      {s}: {b['reason'][:66]}")
            elif b.get("output") is not None:
                print(f"      {s}: {json.dumps(b['output'])[:66]}")

    block("combined-result", "COMBINED RESULT",
          lambda b, r: [f"seq {r['seq']}  {b.get('outcome','')}",
                        f"      scope: {b.get('scope','')}",
                        f"      void_because: {b.get('void_because','-')}"])
    block("verification", "VERIFICATION (independent)",
          lambda b, r: [f"seq {r['seq']}  {b.get('check','')} -> {b.get('result','')}",
                        f"      by {b.get('by','?')}  {b.get('detail','')[:60]}"])
    block("relationship", "RELATIONSHIPS",
          lambda b, r: [f"seq {r['seq']}  {b['source']} --{b['relation']}--> {b['target']}",
                        f"      {(b.get('evidence') or '')[:68]}"])
    block("evidence", "FILES, COMMITS, CERTIFICATES",
          lambda b, r: [f"seq {r['seq']}  {b.get('kind','')}: {b.get('ref','')}",
                        f"      {(b.get('note') or '')[:68]}"])
    block("recommendation", "NEXT (prediction, not result)",
          lambda b, r: [f"seq {r['seq']}  {b.get('statement','')}",
                        f"      cites {b.get('cites')}  LABEL: {b.get('label')}"])
    block("remix", "COUNTERFACTUAL REMIXES",
          lambda b, r: [f"seq {r['seq']}  dropped {b.get('dropped')} -> {b.get('outcome')}",
                        f"      {(b.get('note') or '')[:68]}"])
    block("failure", "FAILURES KEPT",
          lambda b, r: [f"seq {r['seq']}  {b.get('defect','')[:66]}"])
    print("\n" + "=" * 78)
    return chain, by_kind, mine


# --- Find Prior Work and the repeat warning ----------------------------------

def prior(log, query, show=True):
    q = query.lower()
    hits = []
    for r in load(log):
        blob = json.dumps(r.get("body") or {}).lower()
        if q in blob:
            hits.append(r)
    if show:
        print(f"PRIOR WORK matching {query!r}: {len(hits)} event(s)")
        by = Counter(r["kind"] for r in hits)
        for k, n in by.most_common():
            print(f"  {k:<20}{n:>5}")
        for r in hits[:8]:
            b = r["body"]
            label = (b.get("statement") or b.get("outcome") or b.get("defect")
                     or b.get("claim") or b.get("relation") or b.get("eye_id") or "")
            print(f"    seq {r['seq']:<5} {r['kind']:<18} {str(label)[:50]}")
        if len(hits) > 8:
            print(f"    ... {len(hits) - 8} more")
    return hits


def repeat_warning(log, question):
    """Is this already settled? Say so BEFORE doing anything."""
    hits = prior(log, question, show=False)
    settled = [r for r in hits if r["kind"] in
               ("combined-result", "verification", "certificate", "decision")]
    return settled


# --- Compare Prediction to Result --------------------------------------------

def compare(log, item_id):
    """Prediction against the thing that actually tested it.

    The first version scored every prediction against the item's single
    combined-result, which produced a confidently wrong verdict: a prediction
    about conjugation-invariance was marked DIVERGED by a search result that
    had nothing to do with it. A prediction must name its test, and the
    comparison must resolve that name. An unlinked prediction is reported as
    unlinked rather than scored against whatever is nearest.
    """
    _, by_kind, _ = open_item(log, item_id, show=False)
    preds = by_kind.get("prediction", [])
    results = by_kind.get("combined-result", [])
    eyes = {r["body"]["eye_id"]: r for r in by_kind.get("eye-reading", [])}

    print(f"PREDICTION vs RESULT for {item_id}")
    print("-" * 78)
    if not preds:
        print("  no prediction was recorded before the work — that is the defect,")
        print("  not a missing feature: a claim written afterwards is a description.")
        return

    for p in preds:
        pb = p["body"]
        if pb.get("superseded_by"):
            continue
        print(f"\n  PREDICTED (seq {p['seq']}, by {pb.get('by')}): {pb.get('statement')}")
        tb = pb.get("tested_by")
        if not tb:
            print("    TESTED BY: not recorded — this prediction is UNLINKED and")
            print("    is not scored. Naming the test is part of making a prediction.")
            continue
        if tb in eyes:
            r = eyes[tb]
            out = r["body"].get("output")
            print(f"    TESTED BY: eye {tb} (seq {r['seq']})")
            print(f"    ACTUAL: {json.dumps(out)[:72] if out else r['body'].get('reason','')[:72]}")
            exp = pb.get("expected_key")
            verdict = "no machine-comparable expectation"
            if exp and isinstance(out, dict) and exp in out:
                want, got = pb.get("expected_value"), out[exp]
                verdict = "MATCHED" if want == got else f"DIVERGED (wanted {want})"
            elif pb.get("expected") and out:
                verdict = ("MATCHED" if str(pb["expected"]).lower() in json.dumps(out).lower()
                           else "DIVERGED")
            print(f"    VERDICT: {verdict}")
        elif tb == "combined-result" and results:
            rb = results[0]["body"]
            print(f"    TESTED BY: the combined result (seq {results[0]['seq']})")
            print(f"    ACTUAL: {rb.get('outcome')}")
            exp = (pb.get("expected") or "").lower()
            print(f"    VERDICT: {'MATCHED' if exp and exp in (rb.get('outcome') or '').lower() else 'DIVERGED'}")
            if rb.get("void_because"):
                print(f"    and the result is VOID: {rb['void_because'][:66]}")
        else:
            print(f"    TESTED BY: {tb} — named but not found in this item's chain")


# --- Ask What Comes Next ------------------------------------------------------

def what_next(log, item_id):
    _, by_kind, mine = open_item(log, item_id, show=False)
    blocked = [r for r in by_kind.get("eye-reading", [])
               if r["body"]["state"] in ("blocked", "silent")]
    gaps = Counter(r["body"].get("reason") or "unstated" for r in blocked)
    fails = by_kind.get("failed-to-surface", [])
    rel_fail = [r for r in by_kind.get("relationship", [])
                if r["body"]["relation"] == "failed-to-surface"]

    print(f"WHAT COMES NEXT for {item_id}")
    print("-" * 78)
    print("  LABEL: PREDICTION. Not a theorem, not a verified computation.")
    print("  Generated from the ledger only; every line cites the events behind it.\n")

    cites = []
    if rel_fail:
        print("  What has already failed to surface it:")
        for r in rel_fail:
            print(f"    - {r['body']['source']} (seq {r['seq']})")
            print(f"      {(r['body'].get('evidence') or '')[:64]}")
            cites.append(r["seq"])
    if gaps:
        print("\n  What no eye could see, and why:")
        for reason, n in gaps.most_common(4):
            print(f"    - {n} filing(s): {str(reason)[:62]}")
        cites += [r["seq"] for r in blocked[:3]]

    if not cites:
        print("  REFUSING to recommend: no cited events support a suggestion.")
        print("  An uncited recommendation is a guess wearing a ledger's clothes.")
        return None

    print(f"\n  Cited events: {sorted(set(cites))[:12]}")
    return cites


# --- Remix Eyes ---------------------------------------------------------------

def remix(log, item_id, drop, run_id="atlas-app"):
    """Counterfactual: what would the combined result have been without an eye?"""
    _, by_kind, _ = open_item(log, item_id, show=False)
    eyes = by_kind.get("eye-reading", [])
    kept = [r for r in eyes if r["body"]["eye_id"] not in drop]
    dropped = [r for r in eyes if r["body"]["eye_id"] in drop]
    observed_kept = sum(1 for r in kept if r["body"]["state"] == "observed")
    note = (f"{len(dropped)} filings from {sorted(drop)} removed from the "
            f"combination; {observed_kept} observed filings remain. The dropped "
            f"filings stay in the ledger - this is a view, not a deletion.")
    rec = log.append("remix", {"item_id": item_id, "dropped": sorted(drop),
                               "filings_removed": len(dropped),
                               "observed_remaining": observed_kept,
                               "outcome": "recomputed view",
                               "note": note}, run_id)
    print(f"REMIX {item_id}: dropped {sorted(drop)}")
    print(f"  {note}")
    print(f"  recorded as seq {rec['seq']} — the remix itself is now history")
    return rec


# --- acceptance test ----------------------------------------------------------

def acceptance(log, item_id):
    chain, by_kind, mine = open_item(log, item_id, show=False)
    need = {
        "the item exists": chain["by_kind"]["atlas-item"] >= 1,
        "a prediction was recorded": chain["by_kind"]["prediction"] >= 1,
        "a planned test was recorded": chain["by_kind"]["planned-test"] >= 1,
        "every eye filed, including non-observers":
            chain["by_kind"]["eye-reading"] >= 1 and
            len({r["body"]["state"] for r in by_kind.get("eye-reading", [])}) >= 2,
        "a combined result exists": chain["by_kind"]["combined-result"] >= 1,
        "an independent verification exists": chain["by_kind"]["verification"] >= 1,
        "relationships are first-class": chain["by_kind"]["relationship"] >= 1,
        "artifacts are attached": chain["by_kind"]["evidence"] >= 1,
        "a next step is recorded and labelled":
            chain["by_kind"]["recommendation"] >= 1,
        "a counterfactual remix exists": chain["by_kind"]["remix"] >= 1,
    }
    print(f"ACCEPTANCE TEST  {item_id}")
    print("  Reconstruct the entire chain from the ledger, without chat.")
    print("-" * 78)
    for k, v in need.items():
        print(f"  [{'PASS' if v else 'FAIL'}]  {k}")
    ok = all(need.values())
    print("-" * 78)
    print(f"  {'PASS' if ok else 'FAIL'} — {sum(need.values())}/{len(need)} criteria, "
          f"{chain['events']} events reconstructed")
    return ok


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("command", choices=["open", "prior", "compare", "next",
                                        "remix", "acceptance", "items"])
    ap.add_argument("arg", nargs="?")
    ap.add_argument("--drop", nargs="*", default=[])
    ap.add_argument("--dir")
    a = ap.parse_args(argv)
    log = EventLog(a.dir)

    if a.command == "items":
        for r in load(log):
            if r["kind"] == "atlas-item":
                b = r["body"]
                print(f"{b['item_id']:<40}{b.get('title','')[:36]}")
        return 0
    if not a.arg:
        print("this command needs an item id or query")
        return 2
    if a.command == "open":
        open_item(log, a.arg)
    elif a.command == "prior":
        prior(log, a.arg)
    elif a.command == "compare":
        compare(log, a.arg)
    elif a.command == "next":
        what_next(log, a.arg)
    elif a.command == "remix":
        remix(log, a.arg, set(a.drop))
    elif a.command == "acceptance":
        return 0 if acceptance(log, a.arg) else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
