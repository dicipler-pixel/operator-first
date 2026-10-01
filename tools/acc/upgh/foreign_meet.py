#!/usr/bin/env python3
"""Foreign meeting: a state on our road for row A may equal, up to the 16 symmetries and per-relator rotation/inversion, a state
on a road the team holds for a DIFFERENT row B. From there B's remaining suffix, relabelled by the symmetry and paid for with
prefix moves (as in twin_lookup.py), finishes A. twin_lookup does this for starting presentations only; this does it for every
intermediate state of every road. Targets: k <= kmax rows our road is 1..gap over. Every candidate is replayed from A's official
start on the pinned core. 0 API, no model.

usage: python3 tools/acc/upgh/foreign_meet.py [--gap 6] [--kmax 3] [--out FILE]"""
import argparse
import glob
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import twin_lookup as T  # noqa: E402
from sources import load_board  # noqa: E402

core = T.core


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gap", type=int, default=6)
    ap.add_argument("--kmax", type=int, default=3)
    ap.add_argument("--out")
    a = ap.parse_args()
    st = T.h.state()
    A = load_board(sorted(glob.glob(str(T.REPO / "research/acc/live/boards/ac_2026*.json.gz")))[-1])
    never = set(T.h.cfg["gates"].get("never_rows", []))
    roads = T.team_roads()
    for c, b in st.best.items():
        if c.startswith("ac-"):
            roads.setdefault(c, {}).setdefault(tuple(b["moves"]), "ledger")
    index = {}                                   # key -> (remaining, cid, step, path)
    n_states = 0
    for cid, rs in roads.items():
        if cid not in T.REL:
            continue
        for p in rs:
            s = T.REL[cid]
            seq = [s]
            for m in p:
                s = core.apply_move(s, m)
                seq.append(s)
            if s != T.GOAL:
                continue
            for j, sj in enumerate(seq[:-1]):
                if sum(map(len, sj)) > 60:
                    continue
                n_states += 1
                k = T.key(sj)
                rem = len(p) - j
                if k not in index or rem < index[k][0]:
                    index[k] = (rem, cid, j, p)
    print("indexed states %d, distinct keys %d" % (n_states, len(index)))
    hits = []
    for cid, b in sorted(st.best.items()):
        if not cid.startswith("ac-") or cid.split("-")[1] in never:
            continue
        r = A.get(cid, {})
        if r.get("record") is None or (r.get("k") or 99) > a.kmax:
            continue
        path = list(b["moves"])
        if not 1 <= len(path) - r["record"] <= a.gap:
            continue
        s = T.REL[cid]
        best = path
        for i in range(len(path)):
            hit = index.get(T.key(s))
            if hit and hit[1] != cid and i + hit[0] < len(best):
                rem, fcid, j, fp = hit
                t = T.REL[fcid]
                for m in fp[:j]:
                    t = core.apply_move(t, m)
                for g in T.SYMS:
                    Tt = T.apply_g(g, t)
                    if tuple(T.ccanon(w) for w in Tt) != tuple(T.ccanon(w) for w in s):
                        continue
                    pre = T.prefix_moves(s, Tt)
                    if pre is None:
                        continue
                    body = [T.mmap(g, m) for m in fp[j:]]
                    e = s
                    for m in pre + body:
                        e = core.apply_move(e, m)
                    fin = T.finish(e)
                    if fin is None:
                        continue
                    cand = path[:i] + pre + body + fin
                    if len(cand) < len(best) and core.verify(T.CH[cid], cand, "ac-r2-v1", T.man["limits"])["ok"]:
                        best = cand
            s = core.apply_move(s, path[i])
        if len(best) < len(path):
            hits.append((cid, len(path), len(best), r["record"], r.get("k"), best))
    print("roads shortened by a foreign meeting: %d" % len(hits))
    for h in hits:
        print("  %s %d -> %d (record %d, k %s)%s" % (h[0], h[1], h[2], h[3], h[4], "  <= RECORD" if h[2] <= h[3] else ""))
    if a.out and hits:
        Path(a.out).write_text("# UPG-H foreign meeting (song 9); official core ok\n" +
                               "".join("%s: [%s]\n" % (h[0], ", ".join(map(str, h[5]))) for h in hits))


if __name__ == "__main__":
    main()
