#!/usr/bin/env python3
"""Bridge library: every time one of our roads got shorter, the improvement replaced a middle segment X by a shorter Y
(old and new road share a prefix and a suffix). Collect every such (X, Y) pair from the ledger's path.best history (and from
team roads on the same row), close it under the 16 symmetries (moves relabelled by twin_lookup.mmap), and try each bridge as a
substring rewrite X -> Y on every near-record road (k <= kmax, 1..gap over). A rewrite only counts if the official core accepts
the new road. 0 API, no model.

usage: python3 tools/acc/upgh/bridge_library.py [--gap 6] [--kmax 3] [--maxx 14] [--out FILE]"""
import argparse
import glob
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import twin_lookup as T  # noqa: E402
from sources import load_board  # noqa: E402

core = T.core


def diff(a, b):
    i = 0
    while i < min(len(a), len(b)) and a[i] == b[i]:
        i += 1
    j = 0
    while j < min(len(a), len(b)) - i and a[-1 - j] == b[-1 - j]:
        j += 1
    return tuple(a[i:len(a) - j]), tuple(b[i:len(b) - j])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gap", type=int, default=6)
    ap.add_argument("--kmax", type=int, default=3)
    ap.add_argument("--maxx", type=int, default=14)
    ap.add_argument("--out")
    a = ap.parse_args()
    hist = {}
    for line in open(T.REPO / "research/acc/upgh/ledger.jsonl", encoding="utf-8"):
        if '"path.best"' in line:
            d = json.loads(line)["data"]
            if d.get("cid", "").startswith("ac-"):
                hist.setdefault(d["cid"], []).append(tuple(d["moves"]))
    roads = T.team_roads()
    for c, rs in roads.items():
        hist.setdefault(c, []).extend(rs.keys())
    bridges = set()
    for c, seq in hist.items():
        seq = sorted(set(seq), key=len)
        for k in range(len(seq)):
            for l in range(k + 1, min(len(seq), k + 8)):
                y, x = diff(seq[k], seq[l])
                if 1 <= len(x) <= a.maxx and len(y) < len(x):
                    bridges.add((x, y))
    lib = set()
    for x, y in bridges:
        for g in T.SYMS:
            lib.add((tuple(T.mmap(g, m) for m in x), tuple(T.mmap(g, m) for m in y)))
    print("bridges %d, with symmetries %d" % (len(bridges), len(lib)))
    byfirst = {}
    for x, y in lib:
        byfirst.setdefault(x[0], []).append((x, y))
    st = T.h.state()
    A = load_board(sorted(glob.glob(str(T.REPO / "research/acc/live/boards/ac_2026*.json.gz")))[-1])
    never = set(T.h.cfg["gates"].get("never_rows", []))
    hits = []
    for cid, b in sorted(st.best.items()):
        if not cid.startswith("ac-") or cid.split("-")[1] in never:
            continue
        r = A.get(cid, {})
        if r.get("record") is None or (r.get("k") or 99) > a.kmax:
            continue
        best = list(b["moves"])
        if not 1 <= len(best) - r["record"] <= a.gap:
            continue
        orig = len(best)
        improved = True
        while improved:
            improved = False
            for i in range(len(best)):
                for x, y in byfirst.get(best[i], []):
                    if tuple(best[i:i + len(x)]) == x:
                        cand = best[:i] + list(y) + best[i + len(x):]
                        if core.verify(T.CH[cid], cand, "ac-r2-v1", T.man["limits"])["ok"]:
                            best = cand
                            improved = True
                            break
                if improved:
                    break
        if len(best) < orig:
            hits.append((cid, orig, len(best), r["record"], r.get("k"), best))
    print("roads shortened by the bridge library: %d" % len(hits))
    for h in hits:
        print("  %s %d -> %d (record %d, k %s)%s" % (h[0], h[1], h[2], h[3], h[4], "  <= RECORD" if h[2] <= h[3] else ""))
    if a.out and hits:
        Path(a.out).write_text("# UPG-H bridge library (song 10); official core ok\n" +
                               "".join("%s: [%s]\n" % (h[0], ", ".join(map(str, h[5]))) for h in hits))


if __name__ == "__main__":
    main()
