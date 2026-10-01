#!/usr/bin/env python3
"""Stable height web: heights toward (y, x) instead of (x, y).

A Stable AC line may end with the route to (y, x) followed by [15, 15], so its length is d_yx(start) + 2. The height web
(height_web.py; paper idea from the Strong Papadimitriou-Ratajczak proof) already holds (y, x) as the image of the goal under the
x<->y symmetry, so one more BFS from (y, x) gives every junction its Stable height. For every row whose d_yx + 2 is at or under
the Stable record and below the Stable line we hold, the route is realised move by move from the official start, checked to end
at (y, x) on the pinned core, and written as `sac-XXXXX: [... , 15, 15]` for plan_offline / send. 0 API, no model.

usage: python3 tools/acc/upgh/stable_web.py [--slack 0] [--out FILE]"""
import argparse
import glob
import sys
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import height_web as HW  # noqa: E402
import twin_lookup as T  # noqa: E402
from sources import load_board  # noqa: E402

core = T.core
YX = ((2,), (1,))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slack", type=int, default=0, help="also list rows up to this many moves over the Stable record")
    ap.add_argument("--out")
    a = ap.parse_args()
    S = load_board(sorted(glob.glob(str(T.REPO / "research/acc/live/boards/stable_ac_2026*.json.gz")))[-1])
    never = set(T.h.cfg["gates"].get("never_rows", []))
    W, _, roads, st = HW.build()
    src = W.id[HW.enc(YX)]
    dist = [-1] * len(W.node_src)
    dist[src] = 0
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v in W.adj[u]:
            if dist[v] < 0:
                dist[v] = dist[u] + 1
                dq.append(v)
    out, near = [], []
    for cid in sorted(c for c in T.REL if c.startswith("ac-")):
        if cid.split("-")[1] in never:
            continue
        sid = W.id.get(HW.enc(T.REL[cid]))
        if sid is None or dist[sid] < 0:
            continue
        L = dist[sid] + 2
        r = S.get("s" + cid, {})
        rec, held = r.get("record"), st.best.get("s" + cid)
        held = len(held["moves"]) if held else None
        if rec is None or L > rec + a.slack or (held is not None and L >= held):
            continue
        path, cur = [], T.REL[cid]
        while cur != YX:
            hc = dist[W.id[HW.enc(cur)]]
            for m in HW.MOVES:
                c = core.apply_move(cur, m)
                v = W.id.get(HW.enc(c))
                if v is not None and 0 <= dist[v] == hc - 1:
                    path.append(m)
                    cur = c
                    break
            else:
                path = None
                break
        if path is None:
            continue
        line = path + [15, 15]
        (out if L <= rec else near).append((cid, L, rec, r.get("k"), held, line))
    for tag, rows in (("AT/UNDER STABLE RECORD", out), ("NEAR", near)):
        print("%s: %d" % (tag, len(rows)))
        for cid, L, rec, k, held, _ in rows:
            print("  s%s %d (Stable record %s, k %s; held %s)" % (cid, L, rec, k, held))
    if a.out and out:
        Path(a.out).write_text("# UPG-H stable web: route to (y,x) in the height web + [15,15]; ends at (y,x) on the core\n" +
                               "".join("s%s: [%s]\n" % (c, ", ".join(map(str, l))) for c, _, _, _, _, l in out))
        print("wrote", a.out)


if __name__ == "__main__":
    main()
