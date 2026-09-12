"""First-exit experiment: which forbidden move first opens new futures?

Enumerate the frozen-r1 component of a challenge (moves G = {0,2,3,6,7,8,9})
under cap B_g, then apply every NON-grammar move to every member. Each result
is a "first exit". Classify exits by (exit move, new total length) and by
whether the exit state already lies inside the known full-grammar closed
component under cap B_f (i.e. returns to the well we have already certified
holds no descent) or lands in territory that closure has not covered.

    PYTHONPATH=<sair>/competition/tools:research/acc python3 first_exits.py \
        --manifest ... --challenge ac-00002 --grammar-cap 40 --full-cap 32
"""

import argparse
import json
import sys
from collections import Counter, defaultdict

from verifier import core
from official_closure import key, length

GRAMMAR = (0, 2, 3, 6, 7, 8, 9)


def component(initial, cap, moves):
    start = tuple(tuple(r) for r in initial)
    seen = {key(start): start}
    frontier = [start]
    while frontier:
        nxt = []
        for s in frontier:
            for m in moves:
                t = core.apply_move(s, m)
                if length(t) > cap:
                    continue
                k = key(t)
                if k not in seen:
                    seen[k] = t
                    nxt.append(t)
        frontier = nxt
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True); ap.add_argument("--challenge", required=True)
    ap.add_argument("--grammar-cap", type=int, default=40); ap.add_argument("--full-cap", type=int, default=32)
    ap.add_argument("--out")
    a = ap.parse_args()
    man = json.load(open(a.manifest))
    ch = {c["challenge_id"]: c for c in man["challenges"]}[a.challenge]
    init = ch["initial_relators"]; L0 = sum(len(r) for r in init)

    g = component(init, a.grammar_cap, GRAMMAR)
    print(f"frozen-r1 component cap {a.grammar_cap}: {len(g)} states", file=sys.stderr, flush=True)
    f = component(init, a.full_cap, range(core.NUM_MOVES))
    print(f"full-grammar component cap {a.full_cap}: {len(f)} states (certified: no state < {L0})", file=sys.stderr, flush=True)

    forbidden = [m for m in range(core.NUM_MOVES) if m not in GRAMMAR]
    by_move = defaultdict(Counter)          # move -> {'in_known_well','new_territory','over_cap'}
    len_delta = defaultdict(Counter)        # move -> new_len - src_len
    new_states = {}                         # key -> (state, move, src_len)
    min_new_len = defaultdict(lambda: 10**9)
    for k, s in g.items():
        ls = length(s)
        for m in forbidden:
            t = core.apply_move(s, m); lt = length(t); tk = key(t)
            if lt > a.grammar_cap:
                by_move[m]["over_cap"] += 1; continue
            len_delta[m][lt - ls] += 1
            if tk in f:
                by_move[m]["in_known_well"] += 1
            elif tk in g:
                by_move[m]["back_in_grammar_component"] += 1
            else:
                by_move[m]["new_territory"] += 1
                if lt < min_new_len[m]:
                    min_new_len[m] = lt
                if tk not in new_states:
                    new_states[tk] = (t, m, ls, lt)
    report = {"challenge": a.challenge, "start_length": L0, "grammar_cap": a.grammar_cap, "full_cap": a.full_cap,
              "grammar_component": len(g), "full_component": len(f),
              "exits_by_move": {m: dict(c) for m, c in sorted(by_move.items())},
              "length_delta_by_move": {m: dict(sorted(c.items())) for m, c in sorted(len_delta.items())},
              "min_new_territory_length_by_move": {m: v for m, v in sorted(min_new_len.items())},
              "distinct_new_territory_states": len(new_states),
              "new_territory_shorter_than_start": sum(1 for _, (_, _, _, lt) in new_states.items() if lt < L0)}
    print(json.dumps(report, indent=1))
    if a.out:
        with open(a.out, "w") as fh:
            for tk, (t, m, ls, lt) in new_states.items():
                fh.write(json.dumps({"state": [list(t[0]), list(t[1])], "exit_move": m, "src_len": ls, "len": lt}) + "\n")


if __name__ == "__main__":
    main()
