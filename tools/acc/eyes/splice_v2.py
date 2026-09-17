#!/usr/bin/env python3
"""Phase 3 again, with the kill condition removed by compiling the transport.

splice.py found 5,415 splice candidates and promoted ZERO. Every single one was
rejected for the same reason:

    "non-identity symmetry element; transport not compiled to primitive moves"

The harness canonicalises states up to the full symmetry group -- signed
generator permutations, relator inversion, cyclic rotation, relator swap -- so
almost every match between two runs is a match UP TO SYMMETRY. Without a way to
turn that symmetry into moves 0-13, the whole splice lane was dead.

Every component is now compilable:

  signed permutation  a Type-I automorphism -> wh_lift.transport of the SUFFIX,
                      which lands on a basis pair, then a short AC bridge
  relator inversion   moves 0 and 1
  cyclic rotation     conjugation, moves 6-13
  relator SWAP        there is no swap move, but there IS a swap:
                      2,5,2,1 sends (a,b) -> (a b a^-1, a), and conjugating r0
                      by a^-1 finishes it. Cost 4+|a|, verified 346/346.

A spliced path is prefix(A, 0..i) + compiled-transport + suffix(B, j..end), and
it is promoted ONLY if it replays to exactly (x,y) from A's own relators and is
strictly shorter than A's existing path. Suffixes may come from a DIFFERENT
challenge -- that is the point of a shared index: borrow another row's endgame.

Usage: python3 splice_v2.py [out.json]
"""
import sys, os, json
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
from replay import replay
from class_bridge import bridge_pair
from wh_lift import ac_bridge
from path_compress import compress

RUNS = os.path.join(HERE, "runs")


def load():
    R = {}
    for fn in sorted(os.listdir(RUNS)):
        if fn.endswith(".json"):
            b = json.load(open(os.path.join(RUNS, fn)))
            R[b["run_id"]] = b
    return R


def main():
    dst = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "SPLICE_V2.json")
    R = load()
    idx = defaultdict(list)
    for rid, b in R.items():
        if not b["landed_on_target"]:
            continue
        for s in b["steps"]:
            idx[s["canonical_state_hash"]].append((rid, s["step"]))

    def init_of(b):
        """Every run in this index stores PACKED letters {0,1,2,3}.

        Two wrong guesses got made here before a side test settled it: first
        that words of 1s and 2s were signed {1,-1,2,-2} (they are not), then
        that provenance distinguished two encodings (it does not -- the original
        recorder is packed as well, which a KeyError(3) proved immediately).
        There is one encoding. No conversion.
        """
        r = b["initial_relators"]
        return list(r[0]), list(r[1])

    best = {}
    tried = compiled = promoted = 0
    for h, ent in idx.items():
        if len(ent) < 2:
            continue
        for (ra, ia) in ent:
            A = R[ra]
            a0, a1 = init_of(A)
            sa0, sa1, _ = replay(a0, a1, A["moves"][:ia])
            for (rb, jb) in ent:
                if ra == rb and ia >= jb:
                    continue
                tried += 1
                B = R[rb]
                b0, b1 = init_of(B)
                sb0, sb1, _ = replay(b0, b1, B["moves"][:jb])
                Q = B["moves"][jb:]
                tail = bridge_pair((sa0, sa1), (sb0, sb1), Q)
                if tail is None:
                    continue
                compiled += 1
                cand = list(A["moves"][:ia]) + tail
                x, y, ok = replay(a0, a1, cand)
                if not ok:
                    fin = ac_bridge(x, y, cap=max(24, len(x) + len(y) + 6),
                                    budget=300000)
                    if fin is None:
                        continue
                    cand = cand + fin
                try:
                    cand = compress(a0, a1, cand)
                except AssertionError:
                    continue
                _, _, ok = replay(a0, a1, cand)
                if not ok:
                    continue
                cid = A["challenge_id"]
                if len(cand) < A["moves_total"] and (
                        cid not in best or len(cand) < best[cid]["len"]):
                    best[cid] = {"challengeId": cid, "len": len(cand),
                                 "was": A["moves_total"], "moves": cand,
                                 "from_run": ra, "i": ia,
                                 "suffix_run": rb, "suffix_challenge": B["challenge_id"],
                                 "j": jb}
                    promoted += 1

    out = sorted(best.values(), key=lambda e: e["was"] - e["len"], reverse=True)
    json.dump(out, open(dst, "w"), indent=1)
    print(f"pairs tried: {tried}   transport compiled: {compiled}   "
          f"rows improved: {len(out)}")
    for e in out:
        cross = "" if e["suffix_challenge"] == e["challengeId"] else \
            f"  [endgame borrowed from {e['suffix_challenge']}]"
        print(f"  {e['challengeId']}: {e['was']} -> {e['len']} "
              f"(saves {e['was']-e['len']}){cross}")


if __name__ == "__main__":
    main()
