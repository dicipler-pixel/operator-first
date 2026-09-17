#!/usr/bin/env python3
"""Job A: feed EVERY usable trajectory into the harness index, not just winners.

The splice machinery was mathematically correct and operationally useless
because its index held only 29 already-optimal paths -- there was nothing left
to splice out of them. The fix is not more engines, it is more trajectories.

A path that is 72 moves against a 48-move record is NOT waste. It lands on
(x,y), so every state along it carries a known suffix to the target, and its
middle may be exactly the state some other row's prefix can reach. The harness
mines trajectories; it does not judge endpoints.

Ingests: shared-ball meet logs (MEET/MOVES), descent logs (SOLVED/DMOVES), and
walk-ball logs (WALKMEET/WMOVES). Every path is REPLAYED before it is recorded,
and one that does not land on (x,y) is refused -- the index must never hold a
trajectory that is not a real AC path.

Usage: ingest.py <pairs.txt> <log> <tag> [more pairs/log/tag triples...]
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from replay import replay
from recorder import record_run, chain_append


def read_pairs(path):
    out = {}
    for line in open(path):
        t = line.split()
        if not t:
            continue
        cid, l0 = t[0], int(t[1])
        a = [int(x) for x in t[2:2 + l0]]
        l1 = int(t[2 + l0])
        b = [int(x) for x in t[3 + l0:3 + l0 + l1]]
        out[cid] = (a, b)
    return out


def read_paths(path):
    """(id, moves) for every path-bearing line shape the engines emit."""
    out, pend = [], None
    for line in open(path):
        if " MEET len=" in line or " WALKMEET " in line or " SOLVED " in line \
           or " BALLHIT " in line:
            pend = line.split()[0]
        elif pend and line.split(" ", 1)[0] in ("MOVES", "WMOVES", "DMOVES"):
            out.append((pend, [int(x) for x in line.split()[1:]]))
            pend = None
    return out


def main():
    args = sys.argv[1:]
    added = refused = 0
    while args:
        pf, lf, tag = args[0], args[1], args[2]
        args = args[3:]
        if not os.path.exists(lf):
            continue
        pairs = read_pairs(pf)
        for n, (cid, mv) in enumerate(read_paths(lf)):
            if cid not in pairs:
                continue
            a, b = pairs[cid]
            x, y, ok = replay(a, b, mv)
            if not ok:
                refused += 1
                continue
            rid = f"{tag}-{cid}-{n}"
            if os.path.exists(os.path.join(HERE, "runs", rid + ".json")):
                continue
            body = record_run(rid, cid, a, b, mv, "ingested",
                              {"source": lf, "tag": tag,
                               "note": "valid AC path; may be longer than the "
                                       "board record. Indexed for its STATES."})
            chain_append(body)
            added += 1
    print(f"trajectories indexed: {added}   refused (did not replay to target): {refused}")
    runs = [f for f in os.listdir(os.path.join(HERE, "runs")) if f.endswith(".json")]
    print(f"harness index now holds {len(runs)} runs")


if __name__ == "__main__":
    main()
