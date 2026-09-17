#!/usr/bin/env python3
"""Verify and price walk-ball meets.

A WALKMEET line's WMOVES is already a complete path for the row: the row-side
walk row -> s, followed by the target-side walk (x,y) -> s reversed, giving
s -> (x,y). Both halves come from the same engine, so neither is taken on trust:
the concatenation is compressed and then REPLAYED against the row's original
relators, and anything that does not land exactly on (x,y) is DROPPED.

Kept only if strictly shorter than the standing record -- on this board length
is the score.

Usage: walkball_certs.py <pairs.txt> <walkball.log> <meta.json|-> <out.json>
"""
import sys, json
sys.path.insert(0, "/home/user/operator-first/tools/acc")
sys.path.insert(0, "/home/user/operator-first/tools/acc/eyes")
from path_compress import compress
from replay import replay


def main():
    pairs = {}
    for line in open(sys.argv[1]):
        t = line.split()
        if not t:
            continue
        cid, l0 = t[0], int(t[1])
        a = [int(x) for x in t[2:2 + l0]]
        l1 = int(t[2 + l0])
        b = [int(x) for x in t[3 + l0:3 + l0 + l1]]
        pairs[cid] = (a, b)

    meets, pend = {}, None
    for line in open(sys.argv[2]):
        if " WALKMEET " in line:
            pend = line.split()[0]
        elif line.startswith("WMOVES") and pend:
            meets[pend] = [int(x) for x in line.split()[1:]]
            pend = None

    meta = {} if sys.argv[3] == "-" else json.load(open(sys.argv[3]))
    certs, ctl, dropped = [], [], []
    for cid, mv in meets.items():
        a, b = pairs[cid]
        raw = len(mv)
        try:
            mv = compress(a, b, mv)
        except AssertionError as e:
            dropped.append((cid, f"compression broke the path: {e}")); continue
        _, _, ok = replay(a, b, mv)
        if not ok:
            dropped.append((cid, "does not replay to (x,y)")); continue
        if cid.startswith("pd-") or cid.startswith("pc-"):
            ctl.append((cid, raw, len(mv))); continue
        m = meta.get(cid)
        rec = m["best"] if m else None
        entry = {"challengeId": cid, "moves": mv, "len": len(mv), "raw": raw,
                 "record": rec, "kTeams": m["kTeams"] if m else None}
        if rec is not None and len(mv) >= rec:
            dropped.append((cid, f"len {len(mv)} does not beat record {rec}")); continue
        certs.append(entry)

    certs.sort(key=lambda c: (c["record"] or 0) - c["len"], reverse=True)
    json.dump(certs, open(sys.argv[4], "w"), indent=1)
    print(f"meets: {len(meets)}   controls verified: {len(ctl)}"
          f"   BEATING certificates: {len(certs)}   dropped: {len(dropped)}")
    for cid, raw, n in ctl[:12]:
        print(f"  control {cid}: {raw} -> {n} moves, replays to (x,y)")
    for c in certs[:40]:
        print(f"  {c['challengeId']}  record {c['record']} -> {c['len']} "
              f"(raw {c['raw']}, kTeams={c['kTeams']})")
    for cid, why in dropped[:15]:
        print(f"  DROPPED {cid}: {why}")


if __name__ == "__main__":
    main()
