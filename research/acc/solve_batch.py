"""Batch solver on the OFFICIAL SAIR kernel with the official verifier as gate.

Best-first search (priority = total relator length, then depth) from each
challenge, meeting a precomputed reverse basin of the target (x,y). Every
path is replayed through `verifier.core.verify` before it is written; only
`ok: true` paths reach the submission file.

    PYTHONPATH=<sair>/competition/tools python3 solve_batch.py \
        --manifest <sair>/competition/tools/verifier/data/manifest.json \
        --ids ids.txt --out results.jsonl [--budget 150000] [--cap 60] [--radius 6]

Deliberately simple: this is the "harvest what is already reachable" tool,
not the well-escape engine. Length-first search is structurally blind to
states that must grow before they cancel (LENGTH_WELL_STATUS.md); that is
expected and is why unsolved ids are reported rather than retried.
"""

import argparse
import heapq
import json
import sys
import time

from verifier import core

_ENC = {1: 1, -1: 2, 2: 3, -2: 4}


def key(state):
    out = bytearray()
    for i, r in enumerate(state):
        if i:
            out.append(0)
        out.extend(_ENC[a] for a in r)
    return bytes(out)


def length(state):
    return len(state[0]) + len(state[1])


def build_basin(radius):
    """Map key(state) -> move that steps one radius closer to the target."""
    target = ((1,), (2,))
    basin = {key(target): None}
    frontier = [target]
    for _ in range(radius):
        nxt = []
        for s in frontier:
            for m in range(core.NUM_MOVES):
                t = core.apply_move(s, m)
                k = key(t)
                if k not in basin:
                    basin[k] = core.INVERSE_MOVE[m]  # from t, this move returns to s
                    nxt.append(t)
        frontier = nxt
    return basin


def finish_from_basin(state, basin):
    moves = []
    while True:
        m = basin[key(state)]
        if m is None:
            return moves
        moves.append(m)
        state = core.apply_move(state, m)


def search(initial, basin, budget, cap):
    """Return (moves, nodes_expanded) or (None, nodes_expanded)."""
    start = (tuple(initial[0]), tuple(initial[1]))
    sk = key(start)
    if sk in basin:
        return finish_from_basin(start, basin), 0
    parent = {sk: None}
    heap = [(length(start), 0, sk, start)]
    expanded = 0
    while heap and expanded < budget:
        _, depth, k, s = heapq.heappop(heap)
        expanded += 1
        for m in range(core.NUM_MOVES):
            t = core.apply_move(s, m)
            lt = length(t)
            if lt > cap:
                continue
            tk = key(t)
            if tk in parent:
                continue
            parent[tk] = (k, m, s)
            if tk in basin:
                # reconstruct forward path
                path = [m]
                cur = k
                while parent[cur] is not None:
                    pk, pm, _ = parent[cur]
                    path.append(pm)
                    cur = pk
                path.reverse()
                return path + finish_from_basin(t, basin), expanded
            heapq.heappush(heap, (lt, depth + 1, tk, t))
    return None, expanded


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--ids", required=True, help="file of challenge ids, one per line")
    ap.add_argument("--out", required=True, help="results jsonl (appended)")
    ap.add_argument("--budget", type=int, default=150000)
    ap.add_argument("--cap", type=int, default=60)
    ap.add_argument("--radius", type=int, default=6)
    args = ap.parse_args()

    man = json.load(open(args.manifest))
    limits = man["limits"]
    ch = {c["challenge_id"]: c for c in man["challenges"]}
    ids = [l.strip() for l in open(args.ids) if l.strip() and not l.startswith("#")]

    t0 = time.time()
    basin = build_basin(args.radius)
    print(f"basin radius {args.radius}: {len(basin)} states in {time.time()-t0:.1f}s", file=sys.stderr, flush=True)

    solved = 0
    with open(args.out, "a", encoding="utf-8") as out:
        for cid in ids:
            c = ch[cid]
            t1 = time.time()
            moves, expanded = search(c["initial_relators"], basin, args.budget, args.cap)
            rec = {"challenge_id": cid, "expanded": expanded, "seconds": round(time.time() - t1, 2)}
            if moves is None:
                rec["ok"] = False
            else:
                v = core.verify(c, moves, c["move_spec_version"], limits)
                rec["ok"] = bool(v.get("ok"))
                if v.get("ok"):
                    rec.update(length=v["length"], work=v["work"],
                               certificate_hash=v["certificate_hash"], moves=moves)
                    solved += 1
                else:
                    rec["verify_error"] = v  # should never happen; recorded if it does
            out.write(json.dumps(rec) + "\n")
            out.flush()
            print(f"{cid} {'OK len=%d' % rec['length'] if rec['ok'] else 'unsolved'} "
                  f"expanded={expanded} {rec['seconds']}s", file=sys.stderr, flush=True)
    print(f"solved {solved}/{len(ids)} in {time.time()-t0:.0f}s", file=sys.stderr)


if __name__ == "__main__":
    main()
