#!/usr/bin/env python3
"""Compare scored Lisitsa archive routes with Codex YXXyx routes (n=5..7).

Exact connectors: at most 2 scored moves, total relator length <= 100.
Additional class test: archive's changing word conjugate to the inverse
of Codex's changing word while its other relator is fixed. No global
shortest-path or optimality claim.
"""
import argparse
import json
import sys
from pathlib import Path
from zipfile import ZipFile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools/acc"))
import ms_lisitsa_replay as A
import ms_archive_to_sair as M
import yxxyx_chain as Y

BACK = {1: "a", -1: "A", 2: "B", -2: "b"}


def states(start, path, apply_move):
    result = [start]
    for move in path:
        result.append(apply_move(result[-1], move))
    return result


def exact_join(a, b, apply_move, cap=100):
    la, lb = len(a) - 1, len(b) - 1
    first, last = {}, {}
    for j, state in enumerate(b):
        first.setdefault(state, j)
        last[state] = j
    best = (la, None)
    checked = 0
    for i, origin in enumerate(a):
        layer = [(origin, ())]
        seen = {origin}
        for depth in range(3):
            next_layer = []
            for state, connector in layer:
                checked += 1
                if state in first:
                    j = first[state]
                    cost = j + depth + la - i
                    if cost < best[0]:
                        best = (cost, ["archive-prefix", i, j, connector])
                if state in last:
                    j = last[state]
                    cost = i + depth + lb - j
                    if cost < best[0]:
                        best = (cost, ["codex-prefix", i, j, connector])
                if depth < 2:
                    for move in range(14):
                        child = apply_move(state, move)
                        if child not in seen and sum(map(len, child)) <= cap:
                            seen.add(child)
                            next_layer.append((child, connector + (move,)))
            layer = next_layer
    return {"radius": 2, "length_cap": cap, "states_checked": checked,
            "best_moves": best[0], "improving_join": best[1]}


def conjugacy_join(n, a, archive_rows, archive_positions, audit):
    la = len(a) - 1
    start_fixed = a[0][0]
    hits = 0
    best = (la, None)
    for i, state in enumerate(a):
        if state[0] != start_fixed:
            continue
        inverse = tuple(-v for v in reversed(state[1]))
        requested = "".join(BACK[v] for v in inverse)
        for j, ((archive_word, _), (_, scored_index)) in enumerate(
                zip(archive_rows, archive_positions)):
            z = audit.conjugator(archive_word, requested)
            if z is None:
                continue
            hits += 1
            # P1 -> scored fixed relator (2 conjugations), invert the
            # changing relator (1), and align it by |z| conjugations.
            cost = scored_index + 3 + len(z) + la - i
            if cost < best[0]:
                best = (cost, [i, j, scored_index, z])
    return {"conjugacy_matches": hits, "best_moves": best[0],
            "improving_join": best[1]}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("zipfile", type=Path)
    p.add_argument("--sair-root", type=Path, required=True)
    args = p.parse_args()
    sys.path.insert(0, str(args.sair_root / "competition/tools"))
    from verifier.core import apply_move
    out = []
    with ZipFile(args.zipfile) as archive:
        for n in (5, 6, 7):
            rows = A.replay(archive, n)
            bpath, bpositions, info = M.generate(
                n, rows, A, apply_move)
            apath, _ = Y.generate(n, apply_move)
            a = states(Y.initial(n), apath, apply_move)
            b = states(Y.initial(n), bpath, apply_move)
            out.append({"n": n, "codex_moves": len(apath),
                        "archive_scored_moves": len(bpath),
                        "exact": exact_join(a, b, apply_move),
                        "cyclic_class": conjugacy_join(
                            n, a, rows, bpositions, A)})
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
