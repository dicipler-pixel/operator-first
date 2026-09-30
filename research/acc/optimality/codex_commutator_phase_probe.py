#!/usr/bin/env python3
"""Check Lisitsa/MS mapping and cyclic commutator phases with pinned SAIR core.

Run from the repository:
  python3 research/acc/optimality/codex_commutator_phase_probe.py --sair-root SAIR-AC
The P -> AK(3) endpoint is equivalence data, never a scoring solution.
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / "research/acc/live/ledger"),
                 str(ROOT / "tools/acc")]
import yxxyx_chain as Y
import codex_yxxyx_trace as T
import ak3_p_to_ak3_replay as A

H_TO_SAIR = {1: 4, 2: 3, 3: 5, 4: 2, 5: 11, 6: 9, 7: 13,
             8: 6, 9: 10, 10: 8, 11: 12, 12: 7}
LETTER = {"a": 1, "A": -1, "b": 2, "B": -2}


def as_word(word):
    return tuple(LETTER[c] for c in word)


def comm_len(state, free_reduce, invert):
    a, b = state
    word = free_reduce(a + b + invert(a) + invert(b))
    left, right = 0, len(word)
    while right - left > 1 and word[left] == -word[right - 1]:
        left += 1
        right -= 1
    return right - left


def probe(start, moves, apply_move, free_reduce, invert):
    state = start
    cs = [comm_len(state, free_reduce, invert)]
    delta = {"nielsen": [0, 0, 0], "conjugation": [0, 0, 0]}
    first_four = None
    for i, move in enumerate(moves, 1):
        next_state = apply_move(state, move)
        before = cs[-1]
        after = comm_len(next_state, free_reduce, invert)
        kind = "nielsen" if move < 6 else "conjugation"
        delta[kind][(after > before) - (after < before) + 1] += 1
        if kind == "nielsen":
            assert before == after, (i, move, before, after)
        if after == 4 and first_four is None:
            first_four = {"step": i, "moves_remaining": len(moves) - i,
                          "state": [Y.word(w) for w in next_state]}
        state = next_state
        cs.append(after)
    return {"moves": len(moves), "comm_start": cs[0], "comm_max": max(cs),
            "comm_end": cs[-1], "first_comm_four": first_four,
            "nielsen_down_flat_up": delta["nielsen"],
            "conjugation_down_flat_up": delta["conjugation"],
            "endpoint": [Y.word(w) for w in state]}


def local_early_four(start, moves, apply_move, free_reduce, invert,
                     radius, cap=100):
    """Search detours near a given route, without asserting global optimality."""
    prefixes = [start]
    for m in moves:
        prefixes.append(apply_move(prefixes[-1], m))
    first = next(i for i, s in enumerate(prefixes)
                 if comm_len(s, free_reduce, invert) == 4)
    best = first
    winner = None
    visited = 0
    for i, origin in enumerate(prefixes[:first]):
        seen = {origin}
        layer = [(origin, ())]
        for depth in range(1, min(radius, best - i - 1) + 1):
            next_layer = []
            for state, sequence in layer:
                for move in range(14):
                    child = apply_move(state, move)
                    if child in seen or sum(map(len, child)) > cap:
                        continue
                    seen.add(child)
                    visited += 1
                    trial = sequence + (move,)
                    if comm_len(child, free_reduce, invert) == 4:
                        if i + depth < best:
                            best, winner = i + depth, {
                                "prefix": i, "detour": list(trial)}
                    if depth < radius:
                        next_layer.append((child, trial))
            layer = next_layer
    return {"radius": radius, "max_total_length": cap,
            "neighbor_states_checked": visited, "original_first": first,
            "best_first": best, "improving_detour": winner}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sair-root", required=True)
    parser.add_argument("--detour-radius", type=int, default=0,
                        help="check first c=4 in local n=5 neighborhoods")
    args = parser.parse_args()
    sys.path.insert(0, str(Path(args.sair_root) / "competition/tools"))
    from verifier.core import apply_move, free_reduce, invert, verify

    for n in range(5, 11):
        # a=x, b=Y in Lisitsa/Shehper; invert Q0, rotate Q1 by three.
        q0 = (-1,) + (-2,) * n + (1,) + (2,) * (n + 1)
        q1 = (-1, 2, 1, -2, -1)
        assert (q1[3:] + q1[:3], invert(q0)) == Y.initial(n)

    limits = {"max_path_length": 100000, "max_total_relator_length": 100000,
              "max_work": 10000000}  # synthetic checks only
    out = {"source_commit": "a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e",
           "mapping_n": list(range(5, 11)), "routes": {}}
    for n, path in ((3, T.N3), (4, T.N4),
                    (5, Y.generate(5, apply_move)[0])):
        start = Y.initial(n)
        challenge = {"challenge_id": f"synthetic-yxxyx-{n}",
                     "move_spec_version": "ac-r2-v1",
                     "initial_relators": start, "target_relators": ((1,), (2,))}
        result = verify(challenge, path, "ac-r2-v1", limits)
        assert result["ok"], result
        out["routes"][f"YXXyx_n{n}"] = probe(
            start, path, apply_move, free_reduce, invert)
        if n == 5 and args.detour_radius:
            out["n5_local_detours"] = local_early_four(
                start, path, apply_move, free_reduce, invert,
                args.detour_radius)

    start = tuple(as_word(w) for w in A.P)
    target = tuple(as_word(w) for w in A.AK3)
    moves = [H_TO_SAIR[h] for h in A.MOVES]
    challenge = {"challenge_id": "synthetic-p-ak3",
                 "move_spec_version": "ac-r2-v1",
                 "initial_relators": start, "target_relators": target}
    result = verify(challenge, moves, "ac-r2-v1", limits)
    assert result["ok"], result
    state = start
    source_state = A.P
    for h, move in zip(A.MOVES, moves):
        state = apply_move(state, move)
        source_state = A.apply_h(source_state, h)
        assert state == tuple(as_word(w) for w in source_state)
    out["routes"]["P_to_AK3"] = probe(
        start, moves, apply_move, free_reduce, invert)
    out["routes"]["P_to_AK3"]["synthetic_verify"] = result
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
