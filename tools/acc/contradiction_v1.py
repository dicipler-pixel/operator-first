"""A contradiction is an eye, not a footnote.

Jeromie's instruction: append contradictions as separate eyes. That is stronger
than flagging them. A flag hangs off something else and disappears when that
thing is superseded; an eye has its own filing, its own output, its own state,
and it survives independently of either side.

So a contradiction here files THREE things:

  1. a new eye `contradiction:<a>-vs-<b>` in state `observed`, whose output is
     both readings and the key they disagree on;
  2. a `contradicted` filing against EACH side — append-only, so each side's
     original `observed` filing stays exactly where it was. Nothing is edited
     into agreement;
  3. a `contradicts` relationship between the two, permanent and first-class.

A contradiction is never resolved by deletion. If one side is later shown
wrong, that is a further filing, and both remain readable.

    python3 tools/acc/contradiction_v1.py --detect
    python3 tools/acc/contradiction_v1.py --list
"""

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from event_log_v1 import EventLog  # noqa: E402

RUN = "contradictions"


def file_contradiction(log, item_id, a, b, key, a_val, b_val, note, a_seq=None, b_seq=None):
    """One contradiction, three filings, nothing overwritten."""
    cid = f"contradiction:{a}-vs-{b}"
    log.eye_reading(RUN, item_id, cid, "observed", item_id=item_id, output={
        "disagree_on": key,
        "side_a": {"eye": a, "value": a_val, "seq": a_seq},
        "side_b": {"eye": b, "value": b_val, "seq": b_seq},
        "resolved": False,
        "note": note})
    for side, other, seq in ((a, b, a_seq), (b, a, b_seq)):
        log.eye_reading(RUN, item_id, side, "contradicted", item_id=item_id,
                        reason=f"contradicted by {other} on {key}; see {cid}. "
                               f"This filing does not replace that eye's own "
                               f"observation, which stands unedited.",
                        original_seq=seq)
    log.relationship(RUN, "contradicts", f"eye:{a}", f"eye:{b}",
                     evidence=f"{key}: {json.dumps(a_val)} vs {json.dumps(b_val)}. {note}",
                     item_id=item_id)
    return cid


def detect(log, apply=False):
    """Two eyes disagreeing ABOUT THE SAME THING.

    The first version flagged any two eyes reporting different values under the
    same output key, and every candidate it produced was a false positive:

      displacement-gram destroyed_by "the 4 multiplication moves"
      twisted-determinant destroyed_by "all 8 conjugation moves"

    That is not disagreement, it is the complementarity result. Two eyes
    describing THEMSELVES under a shared key name are not contradicting each
    other. Likewise two searches reporting different `states` counts: different
    runs, different numbers, no conflict.

    A contradiction needs a shared SUBJECT, which is the mixer's own coordinate
    rule applied one level up: readings combine only on a genuine common
    coordinate, and they conflict only about a genuine common subject. So a
    reading must declare `about` before it can contradict anything, and a
    same-key collision without one is reported as rejected, with the reason.
    """
    rows = [r for _, r, _ in log.read()
            if r and r["kind"] == "eye-reading" and r["body"].get("state") == "observed"
            and isinstance(r["body"].get("output"), dict)]
    per = defaultdict(list)
    loose = 0
    for r in rows:
        b = r["body"]
        about = b["output"].get("about") or b.get("about")
        if not about:
            loose += 1
            continue
        key = (b.get("item_id") or b.get("claim_id"), about)
        per[key].append((b["eye_id"], b["output"].get("value"), r["seq"]))

    found = []
    for (item, about), vals in per.items():
        eyes = {}
        for eye, v, seq in vals:
            eyes.setdefault(eye, (v, seq))
        if len(eyes) > 1 and len({json.dumps(v, sort_keys=True) for v, _ in eyes.values()}) > 1:
            names = sorted(eyes)
            a, b = names[0], names[1]
            found.append((item, a, b, about, eyes[a][0], eyes[b][0], eyes[a][1], eyes[b][1]))

    print(f"scan over readings that declare a subject: {len(found)} contradiction(s)")
    for item, a, b, k, av, bv, asq, bsq in found:
        print(f"  {item}: {a}(seq {asq}) vs {b}(seq {bsq}) about '{k}'")
        if apply:
            print(f"    filed as {file_contradiction(log, item, a, b, k, av, bv, 'automatic scan over declared subjects', asq, bsq)}")
    print(f"\n{loose} reading(s) declare no subject and were NOT scanned.")
    print("  A same-key collision without a declared subject is rejected, not flagged:")
    print("  two eyes describing themselves under one key name do not disagree.")
    return found


def listing(log):
    rows = [r for _, r, _ in log.read() if r and r["kind"] == "eye-reading"]
    cons = [r for r in rows if r["body"]["eye_id"].startswith("contradiction:")]
    marks = [r for r in rows if r["body"]["state"] == "contradicted"]
    print(f"{len(cons)} contradiction eye(s), {len(marks)} contradicted filing(s)\n")
    for r in cons:
        o = r["body"]["output"]
        print(f"seq {r['seq']}  {r['body']['eye_id']}")
        print(f"   on: {o['disagree_on']}")
        print(f"   A  {o['side_a']['eye']} (seq {o['side_a']['seq']}): {json.dumps(o['side_a']['value'])[:70]}")
        print(f"   B  {o['side_b']['eye']} (seq {o['side_b']['seq']}): {json.dumps(o['side_b']['value'])[:70]}")
        print(f"   resolved: {o['resolved']}")
        print(f"   {o['note'][:74]}\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--detect", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--dir")
    a = ap.parse_args(argv)
    log = EventLog(a.dir)
    if a.list:
        listing(log)
    else:
        detect(log, apply=a.apply)
    return 0


if __name__ == "__main__":
    sys.exit(main())
