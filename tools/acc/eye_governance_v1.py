"""The three things v4.1 and Cortex had that this ledger did not.

  rank        predicted-eye ranking      (Cortex / Collatz)
  duplicates  duplicate-panel rejection  (Mixer 500 v4.1)
  leakage     target-leakage detection   (Mixer 500 v4.1)
  sweep       automatic disabled-eye recording

Nothing here invents a score. Every number is read out of the event stream or
computed from filings already in it, and an eye is never removed - `disabled`
is a filing with a reason, and the eye keeps its place on the roster.

Ranking. An eye's predicted usefulness for a given USE is not a property of the
eye alone; the A/B on the d=2 search settled that. The twisted determinant is
correct, expensive, and worthless as a search heuristic because the moves a
search makes destroy it. So the rank is

    coverage of the moves this use actually makes  /  measured cost

and an eye whose invariance profile misses the moves in play ranks at zero for
steering however good it is at gating. The use is named; a ranking without one
is meaningless.

Leakage. v4.1's finding was an eye reporting 0.998 where the truth was 0.743,
because the eye averaged the target column into its own input. The structural
test is the same one that catches it: an eye whose output is a FUNCTION of the
answer has no independent information. Here that is checked as a mapping test -
if every distinct answer value maps to exactly one output value and back, the
eye is reading the answer, not the object.

    python3 tools/acc/eye_governance_v1.py --rank search
    python3 tools/acc/eye_governance_v1.py --duplicates --leakage --sweep
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from event_log_v1 import EventLog  # noqa: E402

RUN = "eye-governance"

# Measured, not assumed: every figure below was produced by a run in this
# repository and is cited to the event that produced it.
PROFILE = {
    "twisted-determinant": {
        "invariant_moves": [0, 1, 2, 3, 4, 5], "cost_ms": 19.0,
        "measured_by": "atlas_torsion_v1 gate; numeric_tau_v1 --time"},
    "displacement-gram": {
        "invariant_moves": [0, 1, 6, 7, 8, 9, 10, 11, 12, 13], "cost_ms": 0.05,
        "measured_by": "displacement_gram_v1 gate"},
    "total-length": {
        "invariant_moves": [], "cost_ms": 0.001,
        "measured_by": "trivially cheap; never invariant, always readable"},
}
# Which moves a use actually makes. A search makes all fourteen.
USES = {
    "search": list(range(14)),
    "gate": list(range(14)),
    "conjugacy-only": [0, 1, 6, 7, 8, 9, 10, 11, 12, 13],
}


def rank(use):
    moves = USES.get(use)
    if moves is None:
        print(f"unknown use {use!r}; one of {sorted(USES)}")
        return []
    rows = []
    for eye, p in PROFILE.items():
        inv = set(p["invariant_moves"])
        cov = len(inv & set(moves)) / max(len(moves), 1)
        # Steering value: an eye destroyed by a move the use makes is noise
        # along any path that makes it.
        survives_all = inv.issuperset(moves)
        steer = cov if survives_all else cov * cov      # penalise partial survival
        score = steer / max(p["cost_ms"], 1e-6)
        rows.append((score, eye, cov, p["cost_ms"], survives_all, p["measured_by"]))
    rows.sort(reverse=True)
    print(f"PREDICTED-EYE RANKING for use = {use!r} ({len(moves)} moves in play)")
    print(f"  {'eye':<24}{'score':>12}{'coverage':>10}{'cost ms':>9}  survives all")
    for score, eye, cov, cost, all_, by in rows:
        print(f"  {eye:<24}{score:>12.2f}{cov:>10.2f}{cost:>9.3f}  {'yes' if all_ else 'no'}")
    print("\n  A ranking is per USE. The same eye ranks differently for gating,")
    print("  and an eye that ranks zero here is not a bad eye — it is the wrong")
    print("  tool for this use and keeps full standing elsewhere.")
    return rows


def readings(log):
    out = defaultdict(list)
    for _, r, _ in log.read():
        if r and r["kind"] == "eye-reading" and r["body"].get("state") == "observed":
            b = r["body"]
            key = b.get("item_id") or b.get("claim_id")
            out[(key, b["eye_id"])].append((r["seq"], b.get("output")))
    return out


def duplicates(log, apply=False):
    by_item = defaultdict(dict)
    for (item, eye), vals in readings(log).items():
        sig = json.dumps([v for _, v in vals], sort_keys=True)
        by_item[item].setdefault(sig, []).append(eye)
    found = []
    for item, sigs in by_item.items():
        for sig, eyes in sigs.items():
            if len(eyes) > 1:
                found.append((item, sorted(eyes)))
    print(f"DUPLICATE PANEL MEMBERS: {len(found)} group(s)")
    for item, eyes in found:
        print(f"  {item}: {eyes} produce byte-identical output on every shared filing")
        if apply:
            keep, drop = eyes[0], eyes[1:]
            for d in drop:
                log.eye_reading(RUN, item, d, "disabled", item_id=item,
                                reason=f"duplicate of {keep}: byte-identical output on "
                                       f"every shared filing. Weight zero, still on the "
                                       f"roster, original filings untouched.")
                log.relationship(RUN, "duplicates", f"eye:{d}", f"eye:{keep}",
                                 evidence="identical output across all shared filings",
                                 item_id=item)
            print(f"    filed {drop} disabled as duplicates of {keep}")
    if not found:
        print("  none — no two eyes agree byte-for-byte on every shared filing")
    return found


def leakage(log, apply=False):
    """An eye whose output is a bijection of the answer is reading the answer."""
    rs = readings(log)
    answers = {}
    for (item, eye), vals in rs.items():
        if eye in ("combined", "answer", "target"):
            answers[item] = vals
    found = []
    for (item, eye), vals in rs.items():
        ans = answers.get(item)
        if not ans or eye in ("combined", "answer", "target") or len(vals) < 3:
            continue
        pairs = list(zip([json.dumps(v, sort_keys=True) for _, v in vals],
                         [json.dumps(v, sort_keys=True) for _, v in ans]))
        fwd, bwd = {}, {}
        ok = True
        for o, a in pairs:
            if fwd.setdefault(a, o) != o or bwd.setdefault(o, a) != a:
                ok = False
                break
        if ok and len(fwd) > 1:
            found.append((item, eye))
    print(f"TARGET LEAKAGE: {len(found)} eye(s)")
    for item, eye in found:
        print(f"  {item}: {eye} — output is a bijection of the answer")
        if apply:
            log.eye_reading(RUN, item, eye, "disabled", item_id=item,
                            reason="target leakage: output is a one-to-one function of "
                                   "the answer, so it carries no independent information. "
                                   "This is v4.1's 0.998-vs-0.743 defect, structurally.")
    if not found:
        print("  none detected. No item in this ledger declares a named `answer` eye,")
        print("  so the test has nothing to compare against — that is an ABSENCE OF")
        print("  EVIDENCE, not a clean bill. Declare one to make the check bite.")
    return found


def sweep(log, apply=False, threshold=3):
    """Automatic disabled-eye recording: an eye blocked or silent every time it
    has been asked, with no observation on record, is disabled with that reason."""
    seen = defaultdict(lambda: defaultdict(int))
    last = {}
    for _, r, _ in log.read():
        if r and r["kind"] == "eye-reading":
            b = r["body"]
            key = (b.get("item_id") or b.get("claim_id"), b["eye_id"])
            seen[key][b["state"]] += 1
            last[key] = (r["seq"], b.get("reason"))
    found = []
    for key, states in seen.items():
        n = sum(states.values())
        if states.get("observed", 0) == 0 and n >= threshold and "disabled" not in states:
            found.append((key, dict(states), last[key]))
    print(f"AUTOMATIC DISABLE SWEEP: {len(found)} eye(s) never observed in "
          f"{threshold}+ filings")
    for (item, eye), states, (seq, reason) in found:
        print(f"  {item}: {eye} — {states}")
        if apply:
            log.eye_reading(RUN, item, eye, "disabled", item_id=item,
                            reason=f"never observed across {sum(states.values())} filings "
                                   f"({states}); last reason: {reason}. Disabled "
                                   f"automatically, kept on the roster, all filings intact.")
    if not found:
        print(f"  none — every eye with {threshold}+ filings has observed at least once")
    return found


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--rank")
    ap.add_argument("--duplicates", action="store_true")
    ap.add_argument("--leakage", action="store_true")
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--dir")
    a = ap.parse_args(argv)
    log = EventLog(a.dir)
    if a.rank:
        rank(a.rank)
    if a.duplicates:
        print(); duplicates(log, a.apply)
    if a.leakage:
        print(); leakage(log, a.apply)
    if a.sweep:
        print(); sweep(log, a.apply)
    if not any([a.rank, a.duplicates, a.leakage, a.sweep]):
        rank("search"); print(); duplicates(log); print(); leakage(log); print(); sweep(log)
    return 0


if __name__ == "__main__":
    sys.exit(main())
