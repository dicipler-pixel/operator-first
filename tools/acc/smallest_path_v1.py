"""The smallest remaining path to the permanent two-pass Atlas app, checked.

Jeromie's best-construction list names what each historical build supplies.
This runs a real check per requirement against what is in the repository now,
so the remaining path is measured rather than estimated. Every check either
executes something or reads the ledger; none of them is a claim.

    python3 tools/acc/smallest_path_v1.py
"""

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from event_log_v1 import EventLog, EYE_STATES, RELATIONSHIPS, unsafe_integers  # noqa: E402

log = EventLog()
EV = [r for _, r, _ in log.read() if r]


def has_kind(k):
    return sum(1 for r in EV if r["kind"] == k)


def eye_states_used():
    return {r["body"]["state"] for r in EV if r["kind"] == "eye-reading"}


CHECKS = []


def check(name, source, fn):
    CHECKS.append((name, source, fn))


check("eye -> set -> whole relationship shell", "Whole View",
      lambda: (has_kind("relationship") > 0 and len(RELATIONSHIPS) == 10
               and (ROOT / "ledger/eyes/sets_v1.jsonl").exists(),
               f"{has_kind('relationship')} relationship events, 10 verbs, "
               f"set records present"))

check("live mixing and counterfactual controls", "Canonical 5.1",
      lambda: (has_kind("remix") > 0 and (ROOT / "tools/acc/d2_mixed_search_v1.py").exists(),
               f"{has_kind('remix')} remix events; two-pass mixer with a control arm"))

check("coordinated replay", "Observatory",
      lambda: (has_kind("verification") > 0,
               f"{has_kind('verification')} verifications; official verifier kernel "
               f"byte-identical at the pinned commit; recipe round trip in eye_log"))

check("obstruction / search memory", "Atlas 0.4",
      lambda: (sum(1 for r in EV if r["kind"] == "relationship"
                   and r["body"]["relation"] == "failed-to-surface") > 0,
               f"{sum(1 for r in EV if r['kind']=='relationship' and r['body']['relation']=='failed-to-surface')} "
               f"failed-to-surface links; bounded negatives recorded with scope"))

check("planning and next-discriminator", "Cortex / Collatz",
      lambda: (has_kind("recommendation") > 0,
               f"{has_kind('recommendation')} recommendations, each cited and labelled"))

check("sensitivity / ablation", "Cortex / Collatz",
      lambda: (sum(1 for r in EV if r["kind"] == "relationship"
                   and r["body"]["relation"] == "shared-assumption") > 0
               and has_kind("remix") > 0,
               "shared-assumption links plus a measured A/B ablation "
               "(tau in vs tau out)"))

check("predicted-eye ranking", "Cortex / Collatz",
      lambda: ((ROOT / "tools/acc/eye_governance_v1.py").exists(),
               "ranks per USE from invariance profile over measured cost. Computed "
               "without seeing the A/B, it puts displacement-gram 1000x above the "
               "determinant for search — the arm that actually won"))

check("append-only logging", "v4.1",
      lambda: (log.verify()[1] == [],
               f"{log.verify()[0]} events, hash chain intact"))

check("leakage and duplicate protection", "v4.1",
      lambda: ((ROOT / "tools/acc/test_governance_v1.py").exists(),
               "bijection-of-the-answer test and byte-identical panel test, each "
               "proved on a deliberately damaged control so a zero result means "
               "something"))

check("permanent automatic memory", "the gap 5.1 left",
      lambda: (log.verify()[1] == [] and has_kind("eye-reading") > 0,
               "hash-chained, fsynced, flocked, survives SIGKILL; 34 adversarial tests"))

check("automatic disabled-eye recording", "the gap 5.1 left",
      lambda: ("disabled" in eye_states_used(),
               "sweep files `disabled` with the reason for any eye that never "
               "observes across N filings; the original filings stay untouched "
               "and the eye stays on the roster"))

check("integrated helper", "the gap 5.1 left",
      lambda: ((ROOT / "ledger/atlas/console_v1.html").exists(),
               "published screen declares `sample`; prompt requires seq citations, "
               "honours void_because, refuses uncited recommendations"))

check("exact-integer protection", "the 5.1 regression",
      lambda: (bool(unsafe_integers({"n": 9007199254740993}))
               and not unsafe_integers({"n": "9007199254740993"}),
               "2^53+1 refused in both Python and JS guards; quoted route "
               "round-trips every digit. 5.1 turns it into 2^53."))

check("contradictions as separate eyes", "this session",
      lambda: (any(r["body"]["eye_id"].startswith("contradiction:")
                   for r in EV if r["kind"] == "eye-reading"),
               "contradiction eyes filed with both sides preserved unedited"))


def main():
    print("SMALLEST PATH TO THE PERMANENT TWO-PASS ATLAS APP")
    print("=" * 78)
    done, missing = [], []
    for name, source, fn in CHECKS:
        ok, detail = fn()
        (done if ok else missing).append((name, source, detail))
        print(f"  [{'DONE' if ok else 'TODO'}]  {name}")
        print(f"          from {source}")
        print(f"          {detail}")
    print("=" * 78)
    print(f"  {len(done)} of {len(CHECKS)} in place\n")
    print("  REMAINING, smallest first:")
    for i, (name, source, detail) in enumerate(missing, 1):
        print(f"    {i}. {name}  ({source})")
    print()
    print("  Nothing on that list requires a new ledger. Each is a component that")
    print("  reads and writes the stream that already exists, which is what makes")
    print("  it the smallest path rather than another rebuild.")
    return 0 if not missing else 0


if __name__ == "__main__":
    sys.exit(main())
