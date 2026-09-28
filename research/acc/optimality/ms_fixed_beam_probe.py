#!/usr/bin/env python3
"""Bounded scored search for MS(5) with the Lisitsa second relator fixed."""
import argparse
import heapq
import random
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools/acc"))
import ms_lisitsa_replay as A
import ms_archive_to_sair as M


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--sair-root", type=Path, required=True)
    p.add_argument("--width", type=int, default=5000)
    p.add_argument("--depth", type=int, default=62)
    p.add_argument("--total-cap", type=int, default=22)
    p.add_argument("--key", choices=("length", "p1", "p2"), default="p1")
    p.add_argument("--seed", type=int, default=7)
    args = p.parse_args()
    sys.path.insert(0, str(args.sair_root / "competition/tools"))
    from verifier.core import apply_move, invert, free_reduce

    fixed = M.word(A.SECOND)
    start = M.word("A" + "b" * 5 + "a" + "B" * 6)
    goal = M.word(A.TARGET)
    moves = (1, 4, 5, 10, 11, 12, 13)
    rng = random.Random(args.seed)

    @lru_cache(maxsize=1000000)
    def children(w):
        return tuple((m, apply_move((fixed, w), m)[1]) for m in moves)

    @lru_cache(maxsize=1000000)
    def p1(w):
        return min(len(w), len(free_reduce(w + fixed)),
                   len(free_reduce(w + invert(fixed))))

    @lru_cache(maxsize=1000000)
    def score(w):
        if args.key == "length":
            return len(w)
        if args.key == "p1":
            return p1(w)
        return min(p1(v) for _, v in children(w))

    frontier = [(start, ())]
    seen = {start}
    print("start", len(start), "goal", len(goal), "fixed", len(fixed),
          "width", args.width, "cap", args.total_cap, "key", args.key,
          flush=True)
    for depth in range(1, args.depth + 1):
        candidates = {}
        for w, path in frontier:
            for m, v in children(w):
                if v in seen or len(v) + len(fixed) > args.total_cap:
                    continue
                if v == goal:
                    full = path + (m,)
                    print("HIT", depth, list(full), flush=True)
                    return
                if v not in candidates:
                    candidates[v] = path + (m,)
        seen.update(candidates)
        if not candidates:
            print("EMPTY", depth, flush=True)
            return
        winners = heapq.nsmallest(
            args.width, candidates,
            key=lambda w: (score(w), len(w), rng.random()))
        frontier = [(w, candidates[w]) for w in winners]
        if depth % 10 == 0 or depth == args.depth:
            print("depth", depth, "frontier", len(frontier),
                  "unique", len(seen), "candidate", len(candidates),
                  "min_score", min(score(w) for w in winners), flush=True)
    print("NO HIT at depth", args.depth, flush=True)


if __name__ == "__main__":
    main()
