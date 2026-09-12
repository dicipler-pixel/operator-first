"""Independent cap-B closure engine built on the OFFICIAL SAIR verifier kernel.

Purpose: cross-check length-well closure counts that were previously produced
only by this project's own move kernels. This engine shares no code with
`length_well_fast.cpp` / `length_well_packed.cpp`; it imports the competition's
`verifier.core` directly, so agreement is evidence about the mathematics rather
than about one implementation.

Usage (from the SAIR repo root, with PYTHONPATH=competition/tools):
    python3 official_closure.py --challenge ac-00015 --cap 26 --manifest <path>
"""

import argparse
import json
import sys

from verifier import core

# Compact key so a multi-million-state frontier fits in memory: letters
# {1,-1,2,-2} map to bytes {1,2,3,4}, relators separated by 0.
_ENC = {1: 1, -1: 2, 2: 3, -2: 4}


def key(state):
    out = bytearray()
    for i, r in enumerate(state):
        if i:
            out.append(0)
        out.extend(_ENC[a] for a in r)
    return bytes(out)


def length(state):
    return sum(len(r) for r in state)


def closure(initial, cap, progress_every=0):
    """Exact connected component of `initial` under legal moves, never exceeding `cap`.

    Returns (size, min_length, closed, level_census). `closed` is True when the
    component was fully enumerated, i.e. every legal move from every member
    either stays within the cap or leaves it -- no frontier remained.
    """
    start = tuple(tuple(r) for r in initial)
    start_len = length(start)
    if start_len > cap:
        raise ValueError(f"start length {start_len} already exceeds cap {cap}")

    seen = {key(start)}
    frontier = [start]
    min_len = start_len
    census = {start_len: 1}

    while frontier:
        nxt = []
        for s in frontier:
            for m in range(core.NUM_MOVES):
                t = core.apply_move(s, m)
                lt = length(t)
                if lt > cap:
                    continue
                k = key(t)
                if k in seen:
                    continue
                seen.add(k)
                nxt.append(t)
                census[lt] = census.get(lt, 0) + 1
                if lt < min_len:
                    min_len = lt
        frontier = nxt
        if progress_every and len(seen) >= progress_every:
            print(f"  ... {len(seen)} states, frontier {len(frontier)}", file=sys.stderr, flush=True)
            progress_every = len(seen) + progress_every

    return len(seen), min_len, True, dict(sorted(census.items()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--challenge", required=True)
    ap.add_argument("--cap", type=int, required=True)
    ap.add_argument("--expect-size", type=int)
    ap.add_argument("--state", help="JSON pair of relators, overriding the manifest start")
    args = ap.parse_args()

    if args.state:
        initial = json.loads(args.state)
    else:
        man = json.load(open(args.manifest))
        ch = {c["challenge_id"]: c for c in man["challenges"]}
        initial = ch[args.challenge]["initial_relators"]

    size, min_len, closed, census = closure(initial, args.cap, progress_every=1_000_000)
    start_len = sum(len(r) for r in initial)
    descends = min_len < start_len
    print(json.dumps({
        "challenge": args.challenge, "cap": args.cap, "start_length": start_len,
        "component_size": size, "min_length": min_len, "closed": closed,
        "descent_found": descends, "level_census": census,
    }, indent=2))

    if args.expect_size is not None and size != args.expect_size:
        print(f"MISMATCH: expected {args.expect_size}, got {size}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
