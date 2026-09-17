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
from replay import replay, apply_move
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

    # 17,934 candidates improve SOME row, but compiling a transport is the
    # expensive step (inverse_aut runs a search). Only the best few per row can
    # possibly matter, so rank by projected length and compile the top K. That
    # turns ~18k compilations into ~73*K.
    # MIN-SUFFIX INDEX, not a pairwise loop. The first version compared every pair
    # inside each hash bucket: fine for 29 runs, intractable at 125, because the
    # cost is quadratic in trajectories. Job A made the index bigger, so the index
    # had to get smarter. Only one number matters per state -- the shortest known
    # suffix from it to (x,y) over every run that ever passed through it.
    minsuf = {}
    for rid, b in R.items():
        if not b["landed_on_target"]:
            continue
        n = b["moves_total"]
        for s_ in b["steps"]:
            h, k = s_["canonical_state_hash"], s_["step"]
            suf = n - k
            cur = minsuf.get(h)
            if cur is None or suf < cur[0]:
                minsuf[h] = (suf, rid, k)

    TOPK = int(os.environ.get("SPLICE_TOPK", "6"))
    percand = {}
    statecache = {}

    def states_of(rid):
        if rid not in statecache:
            B = R[rid]
            b0, b1 = init_of(B)
            acc = [(b0, b1)]
            x, y = list(b0), list(b1)
            for m in B["moves"]:
                x, y = apply_move(x, y, m)
                acc.append((list(x), list(y)))
            statecache[rid] = acc
        return statecache[rid]

    for ra, A in R.items():
        if not A["landed_on_target"]:
            continue
        for s_ in A["steps"]:
            ia = s_["step"]
            ent = minsuf.get(s_["canonical_state_hash"])
            if ent is None:
                continue
            suf, rb, jb = ent
            if ia + suf >= A["moves_total"]:
                continue
            if rb == ra and jb == ia:
                continue
            percand.setdefault(ra, []).append((ia + suf, ia, rb, jb))

    best = {}
    tried = compiled = 0
    for ra, cands in percand.items():
        A = R[ra]
        a0, a1 = init_of(A)
        cid = A["challenge_id"]
        seen = set()
        for proj, ia, rb, jb in sorted(cands)[:TOPK * 4]:
            if len(seen) >= TOPK:
                break
            key = (ia, rb, jb)
            if key in seen:
                continue
            seen.add(key)
            tried += 1
            sa = states_of(ra)[ia]
            sb = states_of(rb)[jb]
            tail = bridge_pair((sa[0], sa[1]), (sb[0], sb[1]), R[rb]["moves"][jb:])
            if tail is None:
                continue
            compiled += 1
            cand = list(A["moves"][:ia]) + tail
            x, y, ok = replay(a0, a1, cand)
            if not ok:
                fin = ac_bridge(x, y, cap=max(24, len(x) + len(y) + 6), budget=200000)
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
            if len(cand) < A["moves_total"] and (
                    cid not in best or len(cand) < best[cid]["len"]):
                best[cid] = {"challengeId": cid, "len": len(cand),
                             "was": A["moves_total"], "moves": cand,
                             "from_run": ra, "i": ia,
                             "suffix_run": rb, "suffix_challenge": R[rb]["challenge_id"],
                             "j": jb}

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
