#!/usr/bin/env python3
"""Idea B: blind guesses with known roads.  Random walks BACKWARD from the goal (x,y).  Every state on a walk has a
known road to the goal (the reversed walk, each move replaced by its inverse; INV = 0,1,3,2,5,4,7,6,9,8,11,10,13,12).
Walks are biased so that they spend their time among states shaped like the target starts.

Biases:
  band:LO:HI       accept a step only if the relator total stays in [LO, HI] (free growth until LO is reached)
  profile:LO:HI    band + Metropolis bias toward the targets' letter-count profiles
                   (per relator (#x letters, #y letters), symmetry-normalised); needs --targets
  balanced:LO:HI   band + each relator length within 40% of the other (target starts are near-balanced)
Output: one line per walk `w: [forward moves from the goal]`; the reader rebuilds every state.

usage: walks.py --bias band:12:18 --walks 10000 --steps 200 --seed 1 [--targets T.csv --sair DIR] --out FILE"""
import argparse
import json
import math
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import stones_lib as S  # noqa: E402


def prof(s):
    p = []
    for w in s:
        nx = sum(1 for t in w if abs(t) == 1)
        p.append((nx, len(w) - nx))
    a = tuple(sorted(p))
    b = tuple(sorted((y, x) for x, y in p))
    return min(a, b)


def pdist(p, P):
    return min(abs(p[0][0] - q[0][0]) + abs(p[0][1] - q[0][1]) + abs(p[1][0] - q[1][0]) + abs(p[1][1] - q[1][1]) for q in P)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bias", required=True)
    ap.add_argument("--walks", type=int, default=10000)
    ap.add_argument("--steps", type=int, default=200)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--targets")
    ap.add_argument("--sair")
    ap.add_argument("--temp", type=float, default=1.0)
    ap.add_argument("--seed-roads", help="start each walk at a random state of a random held road (waypoint seeding); "
                    "the line then begins with the reversed inverted road tail, so it is still a walk from the goal")
    ap.add_argument("--seed-minlen", type=int, default=0, help="waypoints must have relator total >= this")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    kind, lo, hi = a.bias.split(":")
    lo, hi = int(lo), int(hi)
    rng = random.Random(a.seed)
    P = None
    if kind == "profile":
        _, man = S.load_core(a.sair)
        REL = S.rel_of(man)
        P = sorted({prof(REL["ac-" + l.split(",")[0].split("-")[1]]) for l in open(a.targets) if l.strip()})
    WP = None
    if a.seed_roads:
        _, man = S.load_core(a.sair)
        REL = S.rel_of(man)
        WP = []
        for cid, mv in S.read_roads(a.seed_roads):
            mv = [m for m in mv if m < 14] if all(m < 14 for m in mv[:-2]) else None
            if not mv:
                continue
            st = REL["ac-" + cid.split("-")[1]]
            seq = [st]
            for m in mv:
                seq.append(S.apply(seq[-1], m))
            if seq[-1] != S.GOAL:
                continue
            for pos in range(len(mv)):
                if S.L(seq[pos]) >= a.seed_minlen and S.L(seq[pos]) <= hi:
                    WP.append((mv, pos))
        print("waypoints:", len(WP))
    out = open(a.out, "w")
    out.write("# walks.py bias=%s walks=%d steps=%d seed=%d temp=%s\n" % (a.bias, a.walks, a.steps, a.seed, a.temp))
    tot = 0
    for _ in range(a.walks):
        s, mv, last = S.GOAL, [], None
        if WP:
            road, pos = WP[rng.randrange(len(WP))]
            mv = [S.INV[m] for m in reversed(road[pos:])]
            s = S.run(S.GOAL, mv)
            last = mv[-1] if mv else None
        n0 = len(mv)
        tries = 0
        while len(mv) - n0 < a.steps and tries < a.steps * 30:
            tries += 1
            m = rng.randrange(14)
            if last is not None and m == S.INV[last]:
                continue
            t = S.apply(s, m)
            if t == s:
                continue
            n = S.L(t)
            if n > hi or (S.L(s) >= lo and n < lo):
                continue
            if kind == "balanced" and n >= lo:
                a0, a1 = len(t[0]), len(t[1])
                if min(a0, a1) < 0.6 * max(a0, a1):
                    continue
            if P is not None and S.L(s) >= lo:
                d0, d1 = pdist(prof(s), P), pdist(prof(t), P)
                if d1 > d0 and rng.random() > math.exp(-(d1 - d0) / a.temp):
                    continue
            s, last = t, m
            mv.append(m)
        tot += len(mv)
        out.write("w: [%s]\n" % ",".join(map(str, mv)))
    print("wrote %s: %d walks, %d steps" % (a.out, a.walks, tot))


if __name__ == "__main__":
    main()
