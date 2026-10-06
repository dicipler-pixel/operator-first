#!/usr/bin/env python3
"""Dump per-row ladder roads (canonical macro + exact prefix join with KMAX 13 + frame finish) for the XXYxy rows n=NMIN..NMAX
into rows_roads.jsonl ({"id","ac"}), for fixpoint_shorten. usage: dump_rows.py NMIN NMAX"""
import json, sys
sys.path.insert(0, "/home/user/operator-first/research/acc/live/sweeps/ladder_law")
import ladder_rows as LR
LR.KMAX, LR.SLACK = 13, 2
B, T = LR.B, LR.T
a, b = int(sys.argv[1]), int(sys.argv[2])
idx = {}
for cid, p in T.REL.items():
    idx.setdefault(T.key(p), []).append(cid)
with open("rows_roads.jsonl", "a") as f:
    for n in range(a, b + 1):
        ll = LR.loops(n)
        for cid in sorted(idx.get(T.key(B.ms(n)), [])):
            res = LR.run_row(cid, n, ll[:2])
            if res:
                f.write(json.dumps({"id": cid, "ac": res[0], "n": n}) + "\n"); f.flush()
                print(cid, n, len(res[0]), flush=True)
