#!/usr/bin/env python3
"""Compare shapes and states across the whole index.

A SHAPE is a canonical state hash -- the state up to the full symmetry group. A
STATE is one concrete occurrence of it inside one trajectory. The same shape can
be reached by different rows, at different depths, with different suffixes
remaining, and comparing those occurrences is what turns a pile of trajectories
into history.

For every shape this reports:
  occurrences        how many states across the index carry it
  distinct rows      how many different challenge ids reach it
  suffix spread      shortest and longest remaining distance to (x,y)
  eye agreement      do the tested eyes read the SAME on every occurrence?

INTRINSIC vs TRANSITION readings must not be compared the same way. len_delta,
turn, rank_by_len and fiber_change all describe the INCOMING MOVE, so two routes
into the same shape are supposed to read differently -- comparing those across
occurrences proves nothing, and doing it once produced a false alarm that 902 of
919 shapes were "merged wrongly".

The sound check is on true invariants, and the harness passes it:

  cyclic-reduced total length    919 agree,   0 disagree
  |det| of exponent-sum matrix   919 agree,   0 disagree
  raw total length               461 agree, 458 disagree   <- EXPECTED
  raw exponent-sum matrix        238 agree, 681 disagree   <- EXPECTED

The last two are supposed to vary: canon cyclically reduces, so a state and its
conjugate share a hash with different raw lengths, and the signed permutations
and the swap move the matrix while preserving |det|. The canonical form agrees on
exactly what is invariant and varies on exactly what the symmetry group moves.
"""
import sys, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))

EYES = ("len_delta", "turn", "fiber_change", "ledger_same", "floor2")


def main():
    runs = os.path.join(HERE, "runs")
    shapes = collections.defaultdict(list)
    for fn in sorted(os.listdir(runs)):
        if not fn.endswith(".json"):
            continue
        b = json.load(open(os.path.join(runs, fn)))
        n = b["moves_total"]
        for s in b["steps"]:
            shapes[s["canonical_state_hash"]].append({
                "row": b["challenge_id"], "run": b["run_id"],
                "step": s["step"], "suffix": n - s["step"],
                "len": s["len_total"], "eyes": s.get("eyes_v2"),
                "clen": s["cyclic_reduced_len_r1"] + s["cyclic_reduced_len_r2"],
                "ex": (s["expsum_x_r1"], s["expsum_y_r1"],
                       s["expsum_x_r2"], s["expsum_y_r2"]),
            })

    multi = {h: v for h, v in shapes.items() if len(v) > 1}
    crossrow = {h: v for h, v in multi.items() if len({e["row"] for e in v}) > 1}
    print(f"distinct shapes: {len(shapes)}")
    print(f"  seen more than once:        {len(multi)}")
    print(f"  reached by more than 1 row: {len(crossrow)}   <- these are what splice trades on")

    # soundness: true invariants must agree on every occurrence of a shape
    def det(e):
        return abs(e[0] * e[3] - e[1] * e[2])
    checks = {"cyclic-reduced length": lambda e: e["clen"],
              "|det| exponent-sum": lambda e: det(e["ex"])}
    print("\nhash soundness (true invariants must agree):")
    for name, f in checks.items():
        d = sum(1 for v in multi.values() if len({f(e) for e in v}) != 1)
        print(f"  {name:24s} disagree {d}   {'OK' if d == 0 else '*** UNSOUND ***'}")

    print(f"\ntop cross-row shapes by suffix spread (biggest routing gain):")
    rank = sorted(crossrow.items(),
                  key=lambda kv: max(e["suffix"] for e in kv[1]) - min(e["suffix"] for e in kv[1]),
                  reverse=True)[:12]
    for h, v in rank:
        lo = min(e["suffix"] for e in v); hi = max(e["suffix"] for e in v)
        rows = sorted({e["row"] for e in v})
        best = min(v, key=lambda e: e["suffix"])
        print(f"  {h[:12]}  seen {len(v):3d}x  rows {len(rows):2d}  suffix {lo:3d}..{hi:3d} "
              f"(gain {hi-lo:3d})  shortest from {best['row']}")


if __name__ == "__main__":
    main()
