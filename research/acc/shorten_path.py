"""Shorten a verified AC path by local window re-optimisation.

For each position i along the path, BFS a ball of radius R around state S_i
and look for the furthest later state S_j inside it with dist < j-i. Replace
the window with the BFS path and repeat until no window improves. Output is
re-verified through the official kernel; a path that fails verification is
never emitted.

This converts "solved" into "competitive": scoring rewards only the shortest
path, and greedy harvest paths run 2-3x the current records.
"""

import argparse
import json
import sys

from verifier import core

_ENC = {1: 1, -1: 2, 2: 3, -2: 4}


def key(state):
    out = bytearray()
    for i, r in enumerate(state):
        if i:
            out.append(0)
        out.extend(_ENC[a] for a in r)
    return bytes(out)


def replay(start, moves):
    states = [start]
    s = start
    for m in moves:
        s = core.apply_move(s, m)
        states.append(s)
    return states


def ball(center, radius, cap):
    """BFS ball: key -> (depth, path_from_center)."""
    out = {key(center): (0, [])}
    frontier = [(center, [])]
    for _ in range(radius):
        nxt = []
        for s, p in frontier:
            for m in range(core.NUM_MOVES):
                t = core.apply_move(s, m)
                if len(t[0]) + len(t[1]) > cap:
                    continue
                k = key(t)
                if k not in out:
                    out[k] = (len(p) + 1, p + [m])
                    nxt.append((t, p + [m]))
        frontier = nxt
    return out


def peephole(moves):
    """Cancel adjacent inverse move pairs."""
    out = []
    for m in moves:
        if out and core.INVERSE_MOVE[out[-1]] == m:
            out.pop()
        else:
            out.append(m)
    return out


def shorten(start, moves, radius=4, cap=200, max_passes=50):
    moves = peephole(moves)
    for _ in range(max_passes):
        states = replay(start, moves)
        n = len(moves)
        improved = False
        i = 0
        while i < n:
            b = ball(states[i], radius, cap)
            best_j, best_gain, best_path = None, 0, None
            for j in range(min(n, i + 60), i, -1):
                hit = b.get(key(states[j]))
                if hit is not None and hit[0] < j - i:
                    gain = (j - i) - hit[0]
                    if gain > best_gain:
                        best_j, best_gain, best_path = j, gain, hit[1]
            if best_j is not None:
                moves = moves[:i] + best_path + moves[best_j:]
                states = replay(start, moves)
                n = len(moves)
                improved = True
                i += max(1, len(best_path))
            else:
                i += 1
        if not improved:
            break
    return moves


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--results", required=True, help="results jsonl from solve_batch.py")
    ap.add_argument("--out", required=True)
    ap.add_argument("--radius", type=int, default=4)
    ap.add_argument("--cap", type=int, default=200)
    args = ap.parse_args()

    man = json.load(open(args.manifest))
    limits = man["limits"]
    ch = {c["challenge_id"]: c for c in man["challenges"]}
    recs = [json.loads(l) for l in open(args.results) if l.strip()]
    recs = [r for r in recs if r.get("ok")]
    tot_before = tot_after = 0
    with open(args.out, "w", encoding="utf-8") as out:
        for r in recs:
            c = ch[r["challenge_id"]]
            start = (tuple(c["initial_relators"][0]), tuple(c["initial_relators"][1]))
            new = shorten(start, r["moves"], args.radius, args.cap)
            v = core.verify(c, new, c["move_spec_version"], limits)
            if not v.get("ok"):
                print(f"{r['challenge_id']}: shortened path FAILED verification, keeping original", file=sys.stderr)
                new, v = r["moves"], core.verify(c, r["moves"], c["move_spec_version"], limits)
            tot_before += len(r["moves"]); tot_after += len(new)
            out.write(json.dumps({"challenge_id": r["challenge_id"], "ok": True, "length": len(new),
                                  "before": len(r["moves"]), "work": v["work"],
                                  "certificate_hash": v["certificate_hash"], "moves": new}) + "\n")
            print(f"{r['challenge_id']}: {len(r['moves'])} -> {len(new)}", file=sys.stderr, flush=True)
    print(f"total moves {tot_before} -> {tot_after} over {len(recs)} paths", file=sys.stderr)


if __name__ == "__main__":
    main()
