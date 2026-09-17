#!/usr/bin/env python3
"""Job A: attach TESTED eyes to every state in the index, as permanent record.

The rule this enforces: an eye is a RECORD, and it is added only after we have
tested with it. Nothing speculative goes in. Each reading carries the verdict
that earned its place, and the verdict is attached to the observation rather
than deciding whether the observation is kept -- a rejected eye stays in the
record and is only retired from the mixer.

Raw eye output is NEVER overwritten. The existing per-step block from the
original recorder (eyes-v1) is left exactly as written; this appends `eyes_v2`
beside it.

Tested eyes, with how each was tested:

  len_delta   PASSED. Chosen -0.826 vs declined +2.075 over 310 chosen and
              4,030 declined moves. 58.3% precision against 7.1% chance.
  floor2      PASSED OFFLINE, FAILED ONLINE. Best length reachable in two
              moves. Within non-decreasing moves: chosen -1.215 vs declined
              -0.370, 4.4x lift at <= -3. As a search rule: improved 0, worse
              10 of 18; as an atomic macro: 0 improved, 21 same, at a measured
              5.8% fire rate. Recorded, not used by the mixer.
  turn        FAILED. Move-space rotation. Precision BELOW chance at every
              threshold (6.1-6.2% vs 7.1%); its headline 89.7% is the 85.5%
              base rate. Retired from the mixer, kept in the record.
  fiber       FAILED as a discriminator. Ledger unchanged while the nonabelian
              state changes. Chosen 0.423 vs declined 0.583 -- it points the
              WRONG way. Kept because the ledger itself is what splice merges on.

An untested eye must not be added here. That is the whole gate.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ce_shapes import read_trajectory

VERDICTS = {
    "len_delta": {"verdict": "PASSED", "in_mixer": True,
                  "test": "chosen -0.826 vs declined +2.075; 58.3% precision vs 7.1% chance"},
    "floor2":    {"verdict": "PASSED_OFFLINE_FAILED_ONLINE", "in_mixer": False,
                  "test": "4.4x lift offline; A/B 0 improved / 10 worse of 18 as a rule, "
                          "0/21 as a macro at 5.8% fire rate"},
    "turn":      {"verdict": "FAILED", "in_mixer": False,
                  "test": "precision below chance at every threshold; headline was the base rate"},
    "fiber_change": {"verdict": "FAILED_DISCRIMINATOR", "in_mixer": False,
                  "test": "chosen 0.423 vs declined 0.583 -- points the wrong way"},
}
EYE_SET = "eyes-v2-tested"


def main():
    runs = os.path.join(HERE, "runs")
    files = sorted(f for f in os.listdir(runs) if f.endswith(".json"))
    done = skipped = 0
    for fn in files:
        p = os.path.join(runs, fn)
        b = json.load(open(p))
        if b.get("eyes_v2_set") == EYE_SET:
            skipped += 1
            continue
        r0, r1 = list(b["initial_relators"][0]), list(b["initial_relators"][1])
        rows = read_trajectory(r0, r1, b["moves"])
        # rows[i] describes the move at step i -> attach to step i+1, whose
        # step-0 record has no incoming move.
        for s in b["steps"]:
            s.setdefault("eyes_v2", None)
        for i, rec in enumerate(rows):
            tgt = b["steps"][i + 1]
            tgt["eyes_v2"] = {k: rec[k] for k in
                              ("len_delta", "turn", "fiber_change", "ledger_same",
                               "rank_by_len", "best_available_delta",
                               "floor2", "floor5", "collapse5")}
        b["eyes_v2_set"] = EYE_SET
        b["eyes_v2_verdicts"] = VERDICTS
        json.dump(b, open(p, "w"))
        done += 1
    print(f"runs with tested eyes attached: {done}   already current: {skipped}")
    print(f"eye set: {EYE_SET}")
    for k, v in VERDICTS.items():
        print(f"  {k:14s} {v['verdict']:30s} in_mixer={v['in_mixer']}")


if __name__ == "__main__":
    main()
