"""The d=2 search, re-run with every eye filing on every state.

Two jobs.

  --import-legacy   Bring in the earlier cap-30 run as what it actually is: a
                    LEGACY INCOMPLETE EVENT. It recorded totals and nothing
                    per-state. It is imported with that gap named in the record
                    rather than smoothed over, because a ledger that hides its
                    own incompleteness is worse than one that has none.

  --run             Re-run with full recording. Every expanded state produces
                    one eye-reading event PER ROSTER EYE, including the eyes
                    that see nothing, and one search-transition carrying the
                    parent reference, the move, the decision and its reason.

The roster is the two eyes whose complementarity was measured earlier plus two
cheap ones, and all four file on every state. An eye that contributes nothing
to the decision still files `observed`; an eye that cannot see files `silent`
or `blocked` with a reason. Nothing is dropped for being uninformative.

    python3 tools/acc/d2_recorded_v1.py --import-legacy
    python3 tools/acc/d2_recorded_v1.py --run --cap 20 --depth 3
"""

import argparse
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SAIR = Path(os.environ.get(
    "SAIR_ROOT", "/home/user/saircompetition/andrews-curtis")) / "competition" / "tools"
sys.path.insert(0, str(SAIR))
sys.path.insert(0, str(HERE))

from verifier import core                               # noqa: E402
from event_log_v1 import EventLog                       # noqa: E402
from d2_restoration_v1 import B2, C2, D2, total         # noqa: E402
from displacement_gram_v1 import PermRep                # noqa: E402
from numeric_tau_v1 import (NumRep, fingerprint,        # noqa: E402
                            default_rep as tau_rep)

RUN = "d2-restoration"
REP = PermRep([1, 2, 0, 3, 4], [1, 0, 3, 4, 2])
TAU = tau_rep()


def eyes_on(state, tau_budget=None):
    """Every roster eye files. Four of them, none optional.

    Returns {eye_id: (state, output, reason)} with state in the six-way
    vocabulary. The point is that the low-signal eyes are here too.
    """
    r0, r1 = state
    out = {}

    # 1. total length: cheap, always sees, drives the cap.
    out["total-length"] = ("observed", {"total": len(r0) + len(r1),
                                        "r0": len(r0), "r1": len(r1)}, None)

    # 2. displacement Gram / cycle type: conjugation-invariant, multiplication
    #    destroys it. Measured, not assumed.
    out["displacement-gram"] = ("observed",
                                {"cycle_types": [list(c) for c in REP.reading(state)]},
                                None)

    # 3. twisted determinant: invariant under inversion and multiplication,
    #    destroyed by conjugation. Now evaluated exactly at sampled t, so it
    #    OBSERVES instead of filing blocked. Values are strings on purpose:
    #    these determinants run past 2^53 and must never be JSON numbers.
    if tau_budget is None or tau_budget > 0:
        out["twisted-determinant"] = ("observed",
                                      {"tau_at_t": fingerprint(state, TAU)}, None)
    else:
        out["twisted-determinant"] = ("blocked", None,
                                      "per-run sampling budget spent; the eye "
                                      "is rate-limited, not absent")

    # 4. first-relator fixity: B2 is fixed in both endpoints of this problem,
    #    so an eye that watches whether it moved is meaningful here.
    out["b2-fixity"] = ("observed", {"b2_unchanged": list(r0) == list(B2())}, None)

    return out


def import_legacy(log, path):
    p = Path(path)
    if not p.exists():
        print(f"no legacy artifact at {p}")
        return 1
    data = json.loads(p.read_text())
    rec = log.append("import", {
        "source": str(p.relative_to(ROOT)) if ROOT in p.resolve().parents else str(p),
        "completeness": "LEGACY INCOMPLETE EVENT",
        "what_was_recorded": ["endpoints", "cap", "plies per side",
                              "per-level frontier sizes", "final verdict"],
        "what_was_NOT_recorded": [
            "per-state eye readings (no eye filed on any of the 4,217,788 states)",
            "per-transition decisions and their reasons",
            "seed and environment",
            "checkpoints",
            "the states themselves (only counts survive)"],
        "verdict": data.get("found"),
        "stats": data.get("stats"),
        "note": "Imported so the run is not lost. It must not be cited as an "
                "eye-by-eye record, because it is not one.",
    }, RUN)
    print(f"imported as seq {rec['seq']} — LEGACY INCOMPLETE EVENT")
    print(f"  totals kept: {data['stats']['fwd_size']:,} fwd / "
          f"{data['stats']['bwd_size']:,} bwd, no per-state record")
    return 0


def run(log, cap, depth, tau_cap=None):
    b, dsrc, cgoal = B2(), D2(2, 2), C2(2)
    start, goal = (b, dsrc), (b, cgoal)

    log.append("input", {
        "problem": "d=2 companion restoration",
        "attribution": "Robert Sneiderman, ACC-P000002, "
                       "github.com/Robby955/ac-square-divisibility @ d0ed2c06",
        "B2": list(b), "D2": list(dsrc), "C2": list(cgoal),
        "kernel": core.MOVE_SPEC_VERSION,
        "roster": ["total-length", "displacement-gram",
                   "twisted-determinant", "b2-fixity"],
        "cap": cap, "depth": depth,
        "environment": {"python": sys.version.split()[0],
                        "sair_head": "a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e"},
        "seed": None,
    }, RUN)

    start_ref = log.put_chunk({"r0": list(start[0]), "r1": list(start[1])})
    goal_ref = log.put_chunk({"r0": list(goal[0]), "r1": list(goal[1])})
    log.append("state", {"role": "start", "ref": start_ref}, RUN)
    log.append("state", {"role": "goal", "ref": goal_ref}, RUN)

    tau_budget = tau_cap
    seen = {start: start_ref}
    frontier = [start]
    found = None
    expanded = 0

    for ply in range(depth):
        nxt = []
        for s in frontier:
            parent_ref = seen[s]
            readings = eyes_on(s, tau_budget)
            if tau_budget is not None:
                tau_budget -= 1
            for eye_id, (st, output, reason) in readings.items():
                log.eye_reading(RUN, "d2", eye_id, st, output=output,
                                reason=reason, state_ref=parent_ref)
            expanded += 1
            for m in range(core.NUM_MOVES):
                child = core.apply_move(s, m)
                if child is None:
                    continue
                if total(child) > cap:
                    log.search_transition(RUN, parent_ref, m, "prune",
                                          reason=f"total {total(child)} exceeds cap {cap}")
                    continue
                if child in seen:
                    log.search_transition(RUN, parent_ref, m, "prune",
                                          reason="already seen")
                    continue
                child_ref = log.put_chunk({"r0": list(child[0]), "r1": list(child[1])})
                seen[child] = child_ref
                log.search_transition(RUN, parent_ref, m, "expand",
                                      reason="new state within cap",
                                      child_ref=child_ref)
                if child == goal:
                    found = child
                nxt.append(child)
        log.append("checkpoint", {"ply": ply + 1, "frontier": len(nxt),
                                  "seen": len(seen), "expanded": expanded}, RUN)
        frontier = nxt
        if found:
            break

    log.append("decision", {
        "outcome": "path-found" if found else "no-path",
        "scope": f"forward only, {depth} plies, total-length cap {cap}",
        "is_impossibility_theorem": False,
        "reason": "a bounded negative excludes only the specified family",
    }, RUN)
    print(f"recorded run: {expanded} states expanded, {len(seen)} distinct, "
          f"{'PATH FOUND' if found else 'no path'} "
          f"(bounded: {depth} plies, cap {cap})")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--import-legacy", action="store_true")
    ap.add_argument("--legacy-path", default=str(ROOT / "run" / "d2_cap30.json"))
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--cap", type=int, default=20)
    ap.add_argument("--depth", type=int, default=3)
    ap.add_argument("--tau-cap", type=int, default=None,
                    help="max states the determinant eye samples")
    ap.add_argument("--dir")
    a = ap.parse_args(argv)

    log = EventLog(a.dir)
    if a.import_legacy:
        return import_legacy(log, a.legacy_path)
    if a.run:
        return run(log, a.cap, a.depth, a.tau_cap)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
