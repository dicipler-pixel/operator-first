"""The d=2 companion restoration, searched on the official SAIR kernel.

The open point in Robert Sneiderman's square-divisibility package
(ACC-P000002, https://github.com/Robby955/ac-square-divisibility, pinned at
d0ed2c06bb3a9e7ed31e2f31e24d17de6323efe8) is the restoration hypothesis of
`ACSquareHalving.lean`:

    forall j, Reachable (pair (P2.root 2) (shiftedCompanion 2 (2^(j+1))))
                        (pair (P2.root 2) (twoRootCompanion   (2^(j+1))))

`degree_three_all_iff_restoration` proves this is EQUIVALENT to the whole
G(3,3m+1) family. The first case, j=0, is d=2. In the War Room's naming:

    B2 = P2.root 2            = y^-2 x^2 y^2 x^-1
    D2 = shiftedCompanion 2 2 = y^-3 x^-1 y^-1 x^-1 y^3 x^-2
    C2 = twoRootCompanion 2   = y^-1 x^-1 y^-1 x^-1 y x^-2

    target: (B2, D2) -> (B2, C2), BOTH relators mobile.

Words are built from the Lean definitions here rather than transcribed, and
every move is applied by the official `verifier.core`, never by a
re-implementation. Any hit is replayed through `core.verify` before it is
reported.

Grammar note: Lean's `Step.conj` conjugates by an arbitrary word; ac-r2-v1
conjugates by one generator. Conjugation by w = g1...gk is the composition of
single-generator conjugations, and Lean's `inv` + `mulRight` give the
inverted-multiplication moves, so the two grammars reach the same states and a
path found here is a genuine `Reachable` witness.

    python3 tools/acc/d2_restoration_v1.py --cap 30 --depth 7
"""

import argparse
import json
import os
import sys
from pathlib import Path

SAIR = Path(os.environ.get(
    "SAIR_ROOT", "/home/user/saircompetition/andrews-curtis")) / "competition" / "tools"
sys.path.insert(0, str(SAIR))

from verifier import core  # noqa: E402  the official kernel, not a re-implementation

X, Y = 1, 2


def w(*parts):
    """Concatenate letter blocks and free-reduce with the official reducer."""
    out = []
    for p in parts:
        out.extend(p)
    return tuple(core.free_reduce(out))


def pw(g, e):
    """g^e as a letter list."""
    return [g] * e if e >= 0 else [-g] * (-e)


# --- the three words, built from the Lean definitions ----------------------
def B2():
    "P2.root k = y^(-k) * x^2 * y^k * x^-1, at k = 2"
    k = 2
    return w(pw(Y, -k), pw(X, 2), pw(Y, k), pw(X, -1))


def D2(r=2, d=2):
    "shiftedCompanion r d = y^-(r+1) x^-1 y^-1 x^-1 y^(r+1) x^-d"
    return w(pw(Y, -(r + 1)), pw(X, -1), pw(Y, -1), pw(X, -1),
             pw(Y, r + 1), pw(X, -d))


def C2(d=2):
    "twoRootCompanion d = y^-1 x^-1 y^-1 x^-1 y x^-d"
    return w(pw(Y, -1), pw(X, -1), pw(Y, -1), pw(X, -1), pw(Y, 1), pw(X, -d))


def total(state):
    return len(state[0]) + len(state[1])


def neighbours(state, cap):
    for m in range(core.NUM_MOVES):
        nxt = core.apply_move(state, m)
        if nxt is None:
            continue
        if total(nxt) <= cap:
            yield m, nxt


def bidirectional(start, goal, cap, depth):
    """Meet in the middle. The move set is closed under inversion, so the
    backward search is an ordinary search from the goal.

    Parent pointers, not stored paths: a path list per state costs more memory
    than the state, and the frontier is the thing that has to get large here.
    """
    if start == goal:
        return [], {"note": "start equals goal"}
    fwd = {start: (None, None)}     # state -> (parent, move that reached it)
    bwd = {goal: (None, None)}
    fq, bq = [start], [goal]
    stats = {"cap": cap, "depth_each_side": depth,
             "fwd_levels": [], "bwd_levels": []}

    def climb(table, s):
        out = []
        while True:
            parent, m = table[s]
            if parent is None:
                break
            out.append(m)
            s = parent
        out.reverse()
        return out

    def stitch(meet):
        f = climb(fwd, meet)
        b = climb(bwd, meet)
        return f + [core.INVERSE_MOVE[m] for m in reversed(b)]

    for d in range(depth):
        for name, table, queue, other in (("fwd", fwd, fq, bwd),
                                          ("bwd", bwd, bq, fwd)):
            nq = []
            for s in queue:
                for m, nxt in neighbours(s, cap):
                    if nxt in table:
                        continue
                    table[nxt] = (s, m)
                    if nxt in other:
                        stats["meet_depth"] = d + 1
                        stats["fwd_size"], stats["bwd_size"] = len(fwd), len(bwd)
                        return stitch(nxt), stats
                    nq.append(nxt)
            queue[:] = nq
            stats[f"{name}_levels"].append(len(nq))
        if not fq and not bq:
            stats["exhausted"] = True
            break
    stats["fwd_size"], stats["bwd_size"] = len(fwd), len(bwd)
    return None, stats


def replay(start, goal, moves):
    """Confirm any hit with the official verifier, not with my own walk."""
    challenge = {
        "challenge_id": "d2-companion-restoration",
        "move_spec_version": core.MOVE_SPEC_VERSION,
        "initial_relators": [list(start[0]), list(start[1])],
        "target_relators": [list(goal[0]), list(goal[1])],
    }
    limits = {"max_path_length": 10 ** 6,
              "max_total_relator_length": 10 ** 6,
              "max_work": 10 ** 9}
    return core.verify(challenge, moves, core.MOVE_SPEC_VERSION, limits)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cap", type=int, default=30, help="max TOTAL relator length")
    ap.add_argument("--depth", type=int, default=7, help="plies per side")
    ap.add_argument("--d", type=int, default=2, help="companion degree d")
    ap.add_argument("--r", type=int, default=2, help="outer shift r of the source")
    ap.add_argument("--out")
    a = ap.parse_args(argv)

    b, dsrc, cgoal = B2(), D2(a.r, a.d), C2(a.d)
    start, goal = (b, dsrc), (b, cgoal)

    print(f"kernel {core.MOVE_SPEC_VERSION}  ({core.NUM_MOVES} moves)")
    print(f"B2 = {list(b)}   len {len(b)}")
    print(f"D2 = {list(dsrc)}   len {len(dsrc)}     (shiftedCompanion r={a.r} d={a.d})")
    print(f"C2 = {list(cgoal)}   len {len(cgoal)}     (twoRootCompanion d={a.d})")
    print(f"start total {total(start)}, goal total {total(goal)}, cap {a.cap}")
    print()

    moves, stats = bidirectional(start, goal, a.cap, a.depth)
    result = {"start": [list(start[0]), list(start[1])],
              "goal": [list(goal[0]), list(goal[1])],
              "d": a.d, "r": a.r, "stats": stats}

    if moves is None:
        print(f"NO PATH within {a.depth} plies per side under total-length cap {a.cap}")
        print(f"  forward states  {stats['fwd_size']}")
        print(f"  backward states {stats['bwd_size']}")
        print(f"  fwd level sizes {stats['fwd_levels']}")
        print(f"  bwd level sizes {stats['bwd_levels']}")
        print("  This is a BOUNDED NEGATIVE. It is not an impossibility theorem.")
        result["found"] = False
    else:
        verdict = replay(start, goal, moves)
        print(f"PATH FOUND, {len(moves)} moves: {moves}")
        print(f"OFFICIAL REPLAY: {json.dumps(verdict)}")
        result["found"] = True
        result["moves"] = moves
        result["official_verdict"] = verdict
        if not verdict.get("ok"):
            print("  !! the official verifier REJECTS this path; it is not a witness")

    if a.out:
        Path(a.out).write_text(json.dumps(result, indent=1))
        print(f"\nwritten to {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
