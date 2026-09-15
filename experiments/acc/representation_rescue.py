#!/usr/bin/env python3
"""Representation-rescue / unique-generator unstick experiment for rank-two ACC.

Purpose
-------
This is an ordinary-AC search instrument inspired by the representation-rescue
architecture reported in SauersML/group-approximation (2026-09-14), but it does
NOT import Stable-AC certificates or treat spanning-tree changes as ordinary AC.

The executable search below emits only the following rank-two operations on the
ordered relator pair:
  inv(i)             r_i <- r_i^-1
  mulR(i,j,s)        r_i <- r_i r_j^s
  mulL(i,j,s)        r_i <- r_j^s r_i
  conj(i,g)          r_i <- g r_i g^-1, g a generator or inverse generator
  swap               swap the two relators

Each candidate path is replayed from the literal input before it is reported.
The search objective is not merely short words: it seeks a state where some
generator occurs exactly once in some relator (an "eliminability" signal).
That signal is a routing heuristic, not by itself an ACC solution certificate.

Input JSON example:
  {"rels": [[1,2,-1,2], [1,1,-2]], "max_depth": 6,
   "max_states": 50000, "length_cap": 40}

Letters are signed integers: 1=x, -1=x^-1, 2=y, -2=y^-1.
"""

from __future__ import annotations

import argparse
import json
from collections import deque
from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

Word = Tuple[int, ...]
Presentation = Tuple[Word, Word]
Move = Tuple


def free_reduce(word: Sequence[int]) -> Word:
    out: List[int] = []
    for a in word:
        if a == 0:
            raise ValueError("0 is not a generator letter")
        if out and out[-1] == -a:
            out.pop()
        else:
            out.append(int(a))
    return tuple(out)


def inverse(word: Sequence[int]) -> Word:
    return tuple(-a for a in reversed(word))


def multiply(a: Sequence[int], b: Sequence[int]) -> Word:
    return free_reduce(tuple(a) + tuple(b))


def conjugate(word: Sequence[int], letter: int) -> Word:
    if letter == 0:
        raise ValueError("conjugating letter must be nonzero")
    return free_reduce((letter,) + tuple(word) + (-letter,))


def normalize(rels: Sequence[Sequence[int]]) -> Presentation:
    if len(rels) != 2:
        raise ValueError("this experiment currently expects exactly two relators")
    return (free_reduce(rels[0]), free_reduce(rels[1]))


def total_length(p: Presentation) -> int:
    return len(p[0]) + len(p[1])


def eliminability_hits(p: Presentation, generators: Sequence[int] = (1, 2)):
    hits = []
    for i, rel in enumerate(p):
        for g in generators:
            count = sum(1 for a in rel if abs(a) == abs(g))
            if count == 1:
                hits.append({"relator": i, "generator": abs(g)})
    return hits


def cancellation_gain(a: Sequence[int], b: Sequence[int]) -> int:
    return len(a) + len(b) - len(multiply(a, b))


def representation_observation(p: Presentation):
    """A non-certificate eye summarizing how sensitive the state is to relator views.

    All reported views are derived from ordinary relator inversion/swap/cyclic
    conjugacy.  We do not infer that an arbitrary generator-basis change is an
    ordinary-AC certificate step.
    """
    views = []
    rel_variants = []
    for rel in p:
        v = {rel, inverse(rel)}
        n = len(rel)
        for k in range(n):
            rot = free_reduce(rel[k:] + rel[:k])
            v.add(rot)
            v.add(inverse(rot))
        rel_variants.append(sorted(v))
    for a in rel_variants[0]:
        for b in rel_variants[1]:
            q = (a, b)
            views.append((q, len(eliminability_hits(q)), total_length(q)))
            q2 = (b, a)
            views.append((q2, len(eliminability_hits(q2)), total_length(q2)))
    best = min(views, key=lambda z: (-z[1], z[2], z[0]))
    return {
        "view_count": len(views),
        "best_eliminability_hits": best[1],
        "best_total_length": best[2],
        "best_view": [list(best[0][0]), list(best[0][1])],
    }


def apply_move(p: Presentation, mv: Move) -> Presentation:
    r = [p[0], p[1]]
    op = mv[0]
    if op == "inv":
        i = mv[1]
        r[i] = inverse(r[i])
    elif op == "mulR":
        i, j, s = mv[1:]
        rhs = r[j] if s == 1 else inverse(r[j])
        r[i] = multiply(r[i], rhs)
    elif op == "mulL":
        i, j, s = mv[1:]
        lhs = r[j] if s == 1 else inverse(r[j])
        r[i] = multiply(lhs, r[i])
    elif op == "conj":
        i, letter = mv[1:]
        r[i] = conjugate(r[i], letter)
    elif op == "swap":
        r[0], r[1] = r[1], r[0]
    else:
        raise ValueError(f"unknown move {mv!r}")
    return (r[0], r[1])


def replay(start: Presentation, path: Sequence[Move]) -> Presentation:
    p = start
    for mv in path:
        p = apply_move(p, mv)
    return p


def neighbors(p: Presentation, generators: Sequence[int] = (1, 2)) -> Iterable[Tuple[Presentation, Move]]:
    for i in (0, 1):
        mv = ("inv", i)
        yield apply_move(p, mv), mv

    for i, j in ((0, 1), (1, 0)):
        for s in (1, -1):
            for op in ("mulR", "mulL"):
                mv = (op, i, j, s)
                yield apply_move(p, mv), mv

    for i in (0, 1):
        for g in generators:
            for sign in (1, -1):
                mv = ("conj", i, sign * abs(g))
                yield apply_move(p, mv), mv

    mv = ("swap",)
    yield apply_move(p, mv), mv


@dataclass
class SearchResult:
    found: bool
    explored: int
    depth: int | None
    path: List[Move]
    final: Presentation | None
    hits: list


def search_unstick(
    start: Presentation,
    *,
    max_depth: int = 6,
    max_states: int = 50_000,
    length_cap: int | None = None,
    generators: Sequence[int] = (1, 2),
) -> SearchResult:
    initial_hits = eliminability_hits(start, generators)
    if initial_hits:
        return SearchResult(True, 1, 0, [], start, initial_hits)

    q = deque([(start, [])])
    seen = {start}
    while q and len(seen) < max_states:
        state, path = q.popleft()
        if len(path) >= max_depth:
            continue
        for nxt, mv in neighbors(state, generators):
            if length_cap is not None and total_length(nxt) > length_cap:
                continue
            if nxt in seen:
                continue
            seen.add(nxt)
            new_path = path + [mv]
            hits = eliminability_hits(nxt, generators)
            if hits:
                # Mandatory internal replay check.  This is still not the SAIR
                # official verifier; it only checks this script's literal move semantics.
                replayed = replay(start, new_path)
                if replayed != nxt:
                    raise AssertionError("internal replay mismatch")
                return SearchResult(True, len(seen), len(new_path), new_path, nxt, hits)
            q.append((nxt, new_path))

    return SearchResult(False, len(seen), None, [], None, [])


def result_json(start: Presentation, result: SearchResult):
    return {
        "start": [list(start[0]), list(start[1])],
        "start_total_length": total_length(start),
        "representation_eye": representation_observation(start),
        "found_unstick": result.found,
        "explored_states": result.explored,
        "depth": result.depth,
        "path": [list(mv) for mv in result.path],
        "final": None if result.final is None else [list(result.final[0]), list(result.final[1])],
        "eliminability_hits": result.hits,
        "scope": {
            "ordinary_ac_search_moves_only": True,
            "official_sair_replay_done": False,
            "stable_ac_claim": False,
            "solution_claim": False,
        },
    }


def self_test() -> None:
    p = normalize([[1, 2, -1], [2, 1, -2]])
    path = [("inv", 0), ("swap",), ("conj", 1, -2), ("mulR", 0, 1, 1)]
    assert replay(p, path) == apply_move(apply_move(apply_move(apply_move(p, path[0]), path[1]), path[2]), path[3])
    assert inverse(inverse(p[0])) == p[0]
    assert free_reduce([1, 2, -2, -1]) == ()

    # Deliberately starts without a unique occurrence; bounded search is allowed
    # either to find one or to exhaust its declared finite search.  In either
    # case every reported path must replay exactly.
    hardish = normalize([[1, 1, 2, 2], [1, 2, -1, -2]])
    r = search_unstick(hardish, max_depth=3, max_states=5_000, length_cap=20)
    if r.found:
        assert replay(hardish, r.path) == r.final
        assert eliminability_hits(r.final)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("input", nargs="?", help="JSON file; omit for --self-test")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        self_test()
        print(json.dumps({"self_test": "PASS"}, sort_keys=True))
        return
    if not args.input:
        ap.error("provide an input JSON file or --self-test")

    with open(args.input, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    start = normalize(cfg["rels"])
    result = search_unstick(
        start,
        max_depth=int(cfg.get("max_depth", 6)),
        max_states=int(cfg.get("max_states", 50_000)),
        length_cap=cfg.get("length_cap"),
    )
    print(json.dumps(result_json(start, result), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
