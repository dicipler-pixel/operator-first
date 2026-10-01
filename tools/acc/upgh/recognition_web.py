#!/usr/bin/env python3
"""Recognition web (song 12, "Individual faces come and they go, / but the recognition between us is what make us whole.").

The height web (height_web.py) only asks whether a row's START is itself a junction. Here every row's start is surrounded by an
exact ball of radius R, and every ball state is looked up in the global web (every state on every road of every row, all 16
symmetries) with two heights: toward (x, y) (AC) and toward (y, x) (Stable = height + 2 with [15, 15]). The best prefix + height
is realised move by move from the official start and replayed on the pinned core. A row with no record or no road of ours that
gets a route is a FIRST road. 0 API, no model.

usage: python3 recognition_web.py [--r 3] [--r-target 4] [--deadline-min 40] [--out FILE]"""
import argparse
import glob
import sys
import time
from collections import deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import height_web as HW  # noqa: E402
import twin_lookup as T  # noqa: E402
from sources import load_board  # noqa: E402

core = T.core
YX = ((2,), (1,))


def bfs_from(W, src):
    dist = [-1] * len(W.node_src)
    dist[src] = 0
    dq = deque([src])
    while dq:
        u = dq.popleft()
        for v in W.adj[u]:
            if dist[v] < 0:
                dist[v] = dist[u] + 1
                dq.append(v)
    return dist


def descend(W, dist, s, goal):
    path, cur = [], s
    while cur != goal:
        hc = dist[W.id[HW.enc(cur)]]
        for m in HW.MOVES:
            c = core.apply_move(cur, m)
            v = W.id.get(HW.enc(c))
            if v is not None and 0 <= dist[v] == hc - 1:
                path.append(m)
                cur = c
                break
        else:
            return None
    return path


def ball(s, radius, cap):
    seen, frontier = {s: []}, [s]
    for _ in range(radius):
        nxt = []
        for t in frontier:
            for m in HW.MOVES:
                u = core.apply_move(t, m)
                if u not in seen and sum(map(len, u)) <= cap:
                    seen[u] = seen[t] + [m]
                    nxt.append(u)
        frontier = nxt
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--r", type=int, default=3)
    ap.add_argument("--r-target", type=int, default=4, help="radius on rows with no road of ours / no record / k<=3 over record")
    ap.add_argument("--deadline-min", type=float, default=40)
    ap.add_argument("--out")
    a = ap.parse_args()
    t0 = time.time()
    A = load_board(sorted(glob.glob(str(T.REPO / "research/acc/live/boards/ac_2026*.json.gz")))[-1])
    S = load_board(sorted(glob.glob(str(T.REPO / "research/acc/live/boards/stable_ac_2026*.json.gz")))[-1])
    never = set(T.h.cfg["gates"].get("never_rows", []))
    W, dxy, roads, st = HW.build()
    dyx = bfs_from(W, W.id[HW.enc(YX)])
    print("yx heights (%.0fs)" % (time.time() - t0), flush=True)
    rows = [c for c in sorted(T.REL) if c.startswith("ac-") and c.split("-")[1] not in never]

    def ours(c):
        b = st.best.get(c)
        return len(b["moves"]) if b else None

    def target(c):
        r = A.get(c, {})
        o = ours(c)
        return o is None or r.get("record") is None or (r.get("k") or 99) <= 3 and o > r["record"]
    rows.sort(key=lambda c: (not target(c), c))
    lines, report = [], []
    done = 0
    for cid in rows:
        if time.time() - t0 > a.deadline_min * 60:
            break
        done += 1
        Q = T.REL[cid]
        R = a.r_target if target(cid) else a.r
        bl = ball(Q, R, sum(map(len, Q)) + 8)
        best_ac = best_yx = None
        for s, pre in bl.items():
            v = W.id.get(HW.enc(s))
            if v is None:
                continue
            if dxy[v] >= 0 and (best_ac is None or len(pre) + dxy[v] < best_ac[0]):
                best_ac = (len(pre) + dxy[v], pre, s)
            if dyx[v] >= 0 and (best_yx is None or len(pre) + dyx[v] < best_yx[0]):
                best_yx = (len(pre) + dyx[v], pre, s)
        ra, rs = A.get(cid, {}), S.get("s" + cid, {})
        o, os_ = ours(cid), ours("s" + cid)
        if best_ac and (o is None or best_ac[0] < o):
            down = descend(W, dxy, best_ac[2], T.GOAL)
            p = best_ac[1] + down if down is not None else None
            if p and core.verify(T.CH[cid], p, "ac-r2-v1", T.man["limits"])["ok"]:
                rec = ra.get("record")
                tag = "FIRST" if rec is None else ("BEAT" if len(p) < rec else "TIE" if len(p) == rec else "+%d" % (len(p) - rec))
                report.append((cid, o, len(p), rec, ra.get("k"), tag))
                lines.append("%s: [%s]" % (cid, ", ".join(map(str, p))))
        if best_yx and (os_ is None or best_yx[0] + 2 < os_):
            down = descend(W, dyx, best_yx[2], YX)
            if down is not None:
                p = best_yx[1] + down
                e = Q
                for m in p:
                    e = core.apply_move(e, m)
                if e == YX:
                    rec = rs.get("record")
                    L = len(p) + 2
                    tag = "FIRST" if rec is None else ("BEAT" if L < rec else "TIE" if L == rec else "+%d" % (L - rec))
                    report.append(("s" + cid, os_, L, rec, rs.get("k"), tag))
                    lines.append("s%s: [%s]" % (cid, ", ".join(map(str, p + [15, 15]))))
    print("rows done %d of %d (%.0fs)" % (done, len(rows), time.time() - t0))
    score = [r for r in report if r[5] in ("FIRST", "BEAT", "TIE")]
    print("roads shorter than ours (or first): %d; at/under record or first: %d" % (len(report), len(score)))
    for r in sorted(report, key=lambda r: (r[5] not in ("FIRST", "BEAT", "TIE"), r[0]))[:40]:
        print("  %s %s -> %d (record %s, k %s) %s" % r)
    if a.out and lines:
        Path(a.out).write_text("# UPG-H recognition web (song 12): ball around each row start looked up in the global height web\n" +
                               "\n".join(lines) + "\n")
        print("wrote", a.out)


if __name__ == "__main__":
    main()
