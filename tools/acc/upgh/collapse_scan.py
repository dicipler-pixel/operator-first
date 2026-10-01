#!/usr/bin/env python3
"""Collapse-ridge scan (Grok's idea 2, 1 Oct): the pair C_k = (Y x Y^(k-1) x Y^(k-1), x Y^k) reaches ((x),(y)) in exactly k+3 moves,
[1, 8, 2, 4] + [2]*(k-1) (ac-00766 steps 25-34 are k=6). For k >= 7 that finish is longer than the T9 table's 9 moves, so window/tail searches
built on T9 may not see it. For every state on every road we hold, look for C_k up to the 16 symmetries and per-relator rotation/inversion
(paid prefix moves, as in twin_lookup.py), and report any road the ridge finish shortens. Every candidate is replayed on the official core.
0 API, no model.

usage: python3 tools/acc/upgh/collapse_scan.py [--kmax 24] [--write]"""
import argparse
import json
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import twin_lookup as T  # noqa: E402  (module import: no main run)
from sources import load_board  # noqa: E402
import glob  # noqa: E402

REPO = T.REPO


def ridge(k):
    r0 = (-2, 1) + (-2,) * (k - 1) + (1,) + (-2,) * (k - 1)
    r1 = (1,) + (-2,) * k
    return (r0, r1), [1, 8, 2, 4] + [2] * (k - 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kmax", type=int, default=24)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    keys = {}
    for k in range(2, a.kmax + 1):
        C, moves = ridge(k)
        s = C
        for m in moves:
            s = T.core.apply_move(s, m)
        assert s == T.GOAL, k
        keys[T.key(C)] = (k, C, moves)
    st = T.h.state()
    A = load_board(sorted(glob.glob(str(REPO / "research/acc/live/boards/ac_2026*.json.gz")))[-1])
    hits, scanned = [], 0
    for cid, b in st.best.items():
        if not cid.startswith("ac-") or cid not in T.CH:
            continue
        path = b["moves"]
        s = T.REL[cid]
        states = [s]
        for m in path:
            s = T.core.apply_move(s, m)
            states.append(s)
        best = None
        for i, s in enumerate(states[:-1]):
            scanned += 1
            kk = T.key(s)
            if kk not in keys:
                continue
            k, C, moves = keys[kk]
            for g in T.SYMS:
                Tt = T.apply_g(g, C)          # the ridge as seen in s's frame
                if tuple(T.ccanon(w) for w in Tt) != tuple(T.ccanon(w) for w in s):
                    continue
                pre = T.prefix_moves(s, Tt)
                if pre is None:
                    continue
                body = [T.mmap(g, m) for m in moves]
                e = s
                for m in pre + body:
                    e = T.core.apply_move(e, m)
                fin = T.finish(e)
                if fin is None:
                    continue
                cand = path[:i] + pre + body + fin
                if len(cand) < len(path) and (best is None or len(cand) < len(best[0])):
                    if T.core.verify(T.CH[cid], cand, "ac-r2-v1", T.man["limits"])["ok"]:
                        best = (cand, i, k, g)
        if best:
            rec = A.get(cid, {}).get("record")
            hits.append({"row": cid, "old": len(path), "new": len(best[0]), "record": rec, "k": A.get(cid, {}).get("k"),
                         "at_step": best[1], "ridge_k": best[2], "path": best[0]})
    print("states scanned %d, roads shortened by the ridge finish: %d" % (scanned, len(hits)))
    for x in sorted(hits, key=lambda x: x["new"] - (x["record"] or 999))[:25]:
        print("  %s %d -> %d (record %s, k %s; ridge k=%d at step %d)" % (x["row"], x["old"], x["new"], x["record"], x["k"], x["ridge_k"], x["at_step"]))
    if a.write and hits:
        out = REPO / ("research/acc/live/inbox/upgh_collapse_ridge_%s.txt" % time.strftime("%Y%m%dT%H%MZ", time.gmtime()))
        out.write_text("# UPG-H collapse-ridge scan (Grok's idea 2): official-core verified\n" +
                       "".join("%s: [%s]\n" % (x["row"], ", ".join(map(str, x["path"]))) for x in hits))
        print("wrote", out)


if __name__ == "__main__":
    main()
