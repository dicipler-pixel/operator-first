#!/usr/bin/env python3
"""Rhythm compression: long roads often contain a steady rhythm, one short block of moves repeated r times (e.g. [3,9,9,7] x 9,
[10,5] x 8, [11] x 15). For every such run (period 1..6, r >= 3) in our best road on near-record rows, try to reach the state
right after the run from the state right before it in fewer moves: the same block repeated r-1 / r-2 times plus an exact bridge of
<= 3 + 3 moves (bidirectional BFS, relator-total cap = road peak + 4). Any shorter road is replayed from the official start on the
pinned core. 0 API, no model.

usage: python3 tools/acc/upgh/rhythm.py [--gap 12] [--kmax 3] [--out FILE]"""
import argparse
import glob
import json
import sys
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import twin_lookup as T  # noqa: E402
from sources import load_board  # noqa: E402

core = T.core


def tot(s):
    return sum(map(len, s))


def ball(src, depth, cap, rev=False):
    seen, q = {src: []}, deque([src])
    while q:
        s = q.popleft()
        if len(seen[s]) >= depth:
            continue
        for m in range(14):
            t = core.apply_move(s, m)
            if t not in seen and tot(t) <= cap:
                seen[t] = seen[s] + [m]
                q.append(t)
    return seen


INV = {0: 0, 1: 1, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6, 8: 9, 9: 8, 10: 11, 11: 10, 12: 13, 13: 12}


def bridge(a, b, d, cap, cache={}):
    fa = ball(a, d, cap)
    key = (b, d, cap)
    if key not in cache:
        cache.clear()
        cache[key] = ball(b, d, cap)
    fb = cache[key]
    best = None
    for s, pa in fa.items():
        if s in fb:
            pb = [INV[m] for m in reversed(fb[s])]
            if best is None or len(pa) + len(pb) < len(best):
                best = pa + pb
    return best


def runs(path):
    out, i, n = [], 0, len(path)
    while i < n:
        found = None
        for p in range(1, 7):
            blk = path[i:i + p]
            r = 1
            while path[i + r * p:i + (r + 1) * p] == blk:
                r += 1
            if r >= 3 and (found is None or r * p > found[1] * found[0]):
                found = (p, r)
        if found:
            out.append((i, found[0], found[1]))
            i += found[0] * found[1]
        else:
            i += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gap", type=int, default=12)
    ap.add_argument("--kmax", type=int, default=3)
    ap.add_argument("--out")
    a = ap.parse_args()
    st = T.h.state()
    A = load_board(sorted(glob.glob(str(T.REPO / "research/acc/live/boards/ac_2026*.json.gz")))[-1])
    never = set(T.h.cfg["gates"].get("never_rows", []))
    hits, tried = [], 0
    for cid, b in sorted(st.best.items()):
        if not cid.startswith("ac-") or cid.split("-")[1] in never:
            continue
        r = A.get(cid, {})
        if r.get("record") is None or (r.get("k") or 99) > a.kmax:
            continue
        path = list(b["moves"])
        if not 1 <= len(path) - r["record"] <= a.gap:
            continue
        states = [T.REL[cid]]
        for m in path:
            states.append(core.apply_move(states[-1], m))
        cap = max(map(tot, states)) + 4
        best = path
        for i, p, rr in runs(path):
            blk = path[i:i + p]
            s0, s1 = states[i], states[i + p * rr]
            for drop in (1, 2):
                if rr - drop < 0:
                    continue
                mid = s0
                for m in blk * (rr - drop):
                    mid = core.apply_move(mid, m)
                tried += 1
                br = bridge(mid, s1, 3, cap)
                if br is not None and p * (rr - drop) + len(br) < p * rr:
                    cand = path[:i] + blk * (rr - drop) + br + path[i + p * rr:]
                    if len(cand) < len(best) and core.verify(T.CH[cid], cand, "ac-r2-v1", T.man["limits"])["ok"]:
                        best = cand
        if len(best) < len(path):
            hits.append((cid, len(path), len(best), r["record"], r.get("k"), best))
    print("runs tried %d; roads shortened %d" % (tried, len(hits)))
    for h in hits:
        print("  %s %d -> %d (record %d, k %s)%s" % (h[0], h[1], h[2], h[3], h[4], "  <= RECORD" if h[2] <= h[3] else ""))
    if a.out and hits:
        Path(a.out).write_text("# UPG-H rhythm compression (song 8); official core ok\n" +
                               "".join("%s: [%s]\n" % (h[0], ", ".join(map(str, h[5]))) for h in hits))


if __name__ == "__main__":
    main()
