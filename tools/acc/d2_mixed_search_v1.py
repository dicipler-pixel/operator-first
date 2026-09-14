"""Mix the eyes into the search and go deeper than blind breadth could.

The blind bidirectional run covered 4,217,788 states at 8 plies per side under
a total-length cap of 30 and found nothing. That is breadth. This is the other
axis: a beam, steered by the eyes, that goes far deeper on a narrow front.

The mix, and why each weight is what it is:

  cycle-type agreement   the displacement-Gram reading of r1 against the goal's.
                         Conjugation-invariant, so it does not thrash as the
                         search conjugates. Weighted highest.
  tau agreement          the twisted determinant's exact sampled fingerprint.
                         Invariant under inversion and multiplication, which is
                         exactly the half the cycle reading is blind to. This is
                         the complementarity being spent, not admired.
  length pressure        total relator length against the goal's. Cheap, and the
                         only reading that is never destroyed by any move.

None of these is an AC invariant, and the search does not pretend otherwise:
they steer, they never prune on an invariance claim, and every hit is replayed
through the official verifier before it counts as anything.

    python3 tools/acc/d2_mixed_search_v1.py --beam 3000 --depth 60
"""

import argparse
import heapq
import json
import os
import sys
import time
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SAIR = Path(os.environ.get(
    "SAIR_ROOT", "/home/user/saircompetition/andrews-curtis")) / "competition" / "tools"
sys.path.insert(0, str(SAIR))
sys.path.insert(0, str(HERE))

from verifier import core                                    # noqa: E402
from d2_restoration_v1 import B2, C2, D2, total              # noqa: E402
from displacement_gram_v1 import PermRep, cycle_type         # noqa: E402
from numeric_tau_v1 import NumRep, tau_at                    # noqa: E402

GRAM = PermRep([1, 2, 0, 3, 4], [1, 0, 3, 4, 2])
TAU = NumRep([1, 2, 0], [1, 0, 2], weights=(1, 0))
TAU_T = 2          # one sample point: the beam needs speed, not a fingerprint

WEIGHTS = {"cycle": 3.0, "tau": 1.0, "length": 0.6}


def cyc(state):
    return tuple(cycle_type(GRAM.of_word(r)) for r in state)


def tau1(state):
    try:
        return tau_at(state, TAU, TAU_T)
    except Exception:
        return None


def score(state, goal_cyc, goal_tau, goal_len):
    """Lower is better. A mix, with each term's own unit normalised out."""
    c = cyc(state)
    cyc_d = sum(0 if a == b else 1 for a, b in zip(c, goal_cyc))
    t = tau1(state)
    if t is None or goal_tau is None or goal_tau == 0:
        tau_d = 1.0
    else:
        r = abs(t / goal_tau)
        tau_d = 0.0 if r == 1 else min(1.0, abs(float(r.numerator) - float(r.denominator))
                                       / max(float(r.denominator), 1.0))
        tau_d = min(tau_d, 1.0)
    len_d = abs(total(state) - goal_len) / max(goal_len, 1)
    return (WEIGHTS["cycle"] * cyc_d + WEIGHTS["tau"] * tau_d
            + WEIGHTS["length"] * len_d)


def cheap(state, goal_cyc, goal_len):
    """Pass one: the readings every candidate can afford."""
    c = cyc(state)
    cyc_d = sum(0 if a == b else 1 for a, b in zip(c, goal_cyc))
    len_d = abs(total(state) - goal_len) / max(goal_len, 1)
    return WEIGHTS["cycle"] * cyc_d + WEIGHTS["length"] * len_d


def beam_search(start, goal, beam, depth, cap, gate=6, log_every=5, use_tau=True):
    """Two passes, because one of the eyes costs 400x what the others do.

    Pass one scores every candidate on the cheap readings. Pass two spends the
    twisted determinant only on the survivors -- `gate` times the beam width.
    That is the whole reason to mix rather than average: an eye earns its cost
    where it discriminates, and the cheap eyes decide where that is.
    """
    goal_cyc, goal_tau, goal_len = cyc(goal), tau1(goal), total(goal)
    seen = {start}
    frontier = [(0.0, start, [])]
    stats = {"expanded": 0, "tau_evals": 0, "cheap_evals": 0,
             "best_score": None, "best_state": None, "widths": []}
    t0 = time.time()

    for d in range(depth):
        cand = []
        for _, s, path in frontier:
            stats["expanded"] += 1
            for m in range(core.NUM_MOVES):
                nxt = core.apply_move(s, m)
                if nxt is None or total(nxt) > cap or nxt in seen:
                    continue
                seen.add(nxt)
                if nxt == goal:
                    stats["seen"] = len(seen)
                    return path + [m], stats, time.time() - t0
                cand.append((nxt, path + [m]))
        if not cand:
            break

        # pass one
        c1 = [(cheap(s, goal_cyc, goal_len), s, p) for s, p in cand]
        stats["cheap_evals"] += len(c1)
        c1.sort(key=lambda x: x[0])
        survivors = c1[:beam * gate]

        # pass two, on survivors only
        if not use_tau:
            frontier = [x for x in survivors[:beam]]
            stats['widths'].append(len(frontier))
            if stats['best_score'] is None or frontier[0][0] < stats['best_score']:
                stats['best_score'] = frontier[0][0]
                stats['best_state'] = [list(frontier[0][1][0]), list(frontier[0][1][1])]
            if (d + 1) % log_every == 0:
                print(f"  ply {d+1:>3}  seen {len(seen):>8,}  cheap-only"
                      f"  best {frontier[0][0]:.3f}  {time.time()-t0:.0f}s", flush=True)
            continue
        c2 = []
        for base, s, p in survivors:
            t = tau1(s)
            stats["tau_evals"] += 1
            if t is None or goal_tau is None or goal_tau == 0 or t == 0:
                tau_d = 1.0
            else:
                r = abs(t / goal_tau)
                tau_d = 0.0 if r == 1 else min(1.0, abs(float(r) - 1.0) / (1.0 + abs(float(r))))
            c2.append((base + WEIGHTS["tau"] * tau_d, s, p))
        c2.sort(key=lambda x: x[0])
        frontier = c2[:beam]
        stats["widths"].append(len(frontier))
        if stats["best_score"] is None or frontier[0][0] < stats["best_score"]:
            stats["best_score"] = frontier[0][0]
            stats["best_state"] = [list(frontier[0][1][0]), list(frontier[0][1][1])]
        if (d + 1) % log_every == 0:
            print(f"  ply {d+1:>3}  seen {len(seen):>8,}  tau {stats['tau_evals']:>7,}"
                  f"  best {frontier[0][0]:.3f}  {time.time()-t0:.0f}s", flush=True)
    stats["seen"] = len(seen)
    return None, stats, time.time() - t0


def replay(start, goal, moves):
    ch = {"challenge_id": "d2-mixed", "move_spec_version": core.MOVE_SPEC_VERSION,
          "initial_relators": [list(start[0]), list(start[1])],
          "target_relators": [list(goal[0]), list(goal[1])]}
    lim = {"max_path_length": 10**6, "max_total_relator_length": 10**6,
           "max_work": 10**9}
    return core.verify(ch, moves, core.MOVE_SPEC_VERSION, lim)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--beam", type=int, default=3000)
    ap.add_argument("--depth", type=int, default=60)
    ap.add_argument("--cap", type=int, default=40)
    ap.add_argument("--d", type=int, default=2)
    ap.add_argument("--r", type=int, default=2)
    ap.add_argument("--gate", type=int, default=6)
    ap.add_argument("--no-tau", action="store_true",
                    help="control arm: cheap eyes only, so the mix can be judged")
    ap.add_argument("--out")
    a = ap.parse_args(argv)

    b = B2()
    start, goal = (b, D2(a.r, a.d)), (b, C2(a.d))
    print(f"MIXED BEAM  kernel {core.MOVE_SPEC_VERSION}")
    print(f"  start total {total(start)}  goal total {total(goal)}  "
          f"cap {a.cap}  beam {a.beam}  depth {a.depth}")
    print(f"  weights {WEIGHTS}")
    print(f"  start cycles {cyc(start)}   goal cycles {cyc(goal)}")

    moves, stats, secs = beam_search(start, goal, a.beam, a.depth, a.cap, a.gate, use_tau=not a.no_tau)
    res = {"d": a.d, "r": a.r, "beam": a.beam, "depth": a.depth, "cap": a.cap,
           "weights": WEIGHTS, "seconds": round(secs, 1), "stats": stats}
    if moves is None:
        print(f"\nNO PATH on this beam. {stats['expanded']:,} expanded, "
              f"{stats.get('seen', 0):,} distinct, {secs:.0f}s")
        print(f"  best score reached {stats['best_score']:.3f} "
              f"(0 would be all three readings agreeing with the goal)")
        print("  BOUNDED NEGATIVE over this beam and cap. Not an impossibility,")
        print("  and a beam that misses proves less than breadth that closes.")
        res["found"] = False
    else:
        v = replay(start, goal, moves)
        print(f"\nPATH FOUND: {len(moves)} moves")
        print(f"  {moves}")
        print(f"  OFFICIAL REPLAY: {json.dumps(v)}")
        res["found"] = True
        res["moves"] = moves
        res["official"] = v
    if a.out:
        Path(a.out).write_text(json.dumps(res, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
