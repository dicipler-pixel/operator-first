#!/usr/bin/env python3
"""Join roads that pass through the same exact state (same row or different rows): for row A with road P and any verified
road Q (of any row) that visits state s_i(P) at position j, P[:i] + Q[j:] is a road for A. Keeps the shortest per row and
replays every result on the official core. Needs the SAIR verifier (core.apply_move/verify) and challenge manifest.
usage: crossroad_join.py ROADS.txt [ROADS2.txt ...]  > shorter_roads.txt"""
import sys, re, collections
from verifier import core            # official SAIR verifier, ac-r2-v1
import manifest_loader as M          # your loader: M.CH[cid] -> challenge dict, M.LIM -> limits
pat = re.compile(r"\b(ac-\d{5})\s*:\s*\[([0-9,\s]+)\]")
roads = collections.defaultdict(set)
for f in sys.argv[1:]:
    for c, mv in pat.findall(open(f).read()): roads[c].add(tuple(int(x) for x in mv.split(",") if x.strip()))
XY = ((1,), (2,)); idx = {}; traj = {}
for c, rs in roads.items():
    s0 = tuple(tuple(x) for x in M.CH[c]["initial_relators"])
    for p in rs:
        st = [s0]
        for m in p: st.append(core.apply_move(st[-1], m))
        if st[-1] != XY: continue
        if c not in traj or len(p) < len(traj[c][0]): traj[c] = (list(p), st)
        for j, s in enumerate(st):
            if s not in idx or len(p) - j < idx[s][0]: idx[s] = (len(p) - j, c, p, j)
for c, (p, st) in traj.items():
    best = None
    for i, s in enumerate(st):
        tl, c2, p2, j = idx[s]
        if i + tl < len(p) and (best is None or i + tl < best[0]): best = (i + tl, i, c2, p2, j)
    if best:
        _, i, c2, p2, j = best; new = p[:i] + list(p2[j:])
        if core.verify(M.CH[c], new, "ac-r2-v1", M.LIM)["ok"]:
            print("# %s %d -> %d via %s\n%s: [%s]" % (c, len(p), len(new), c2, c, ", ".join(map(str, new))))
