#!/usr/bin/env python3
"""Stage the second half of a descent-into-the-ball hit.

descball reports `<id> BALLHIT` plus DMOVES, a path from the minimised pair m
down to some state s inside T_16. That is only half a certificate: s is provably
AC-trivial, but the moves s -> (x,y) still have to be produced.

This replays DMOVES to recover s and writes it out as a shared-ball challenge.
The shared ball then finds s -> (x,y) at depth 0, because s is already a ball
member. Concatenating the halves and lifting through chi and psi gives the move
list for the ORIGINAL row, which replay.py then judges.

Neither half is trusted on its own: DMOVES is replayed here rather than assumed,
and a state that does not land where descball said it would is DROPPED.

Usage: python3 descball_finish.py <desc_all.txt> <descball.log> <out_challenges.txt> <out_map.json>
"""
import sys, json
sys.path.insert(0, "/home/user/operator-first/tools/acc/eyes")
from replay import replay, free_reduce


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

    hits, pending = {}, None
    for line in open(sys.argv[2]):
        if " BALLHIT " in line:
            pending = line.split()[0]
        elif line.startswith("DMOVES") and pending:
            hits[pending] = [int(x) for x in line.split()[1:]]
            pending = None

    lines, mp, dropped = [], {}, []
    for cid, dm in hits.items():
        if cid not in pairs:
            dropped.append((cid, "hit id not in pair list"))
            continue
        a, b = pairs[cid]
        s0, s1, _ = replay(a, b, dm)
        if not s0 or not s1:
            dropped.append((cid, "descent path empties a relator"))
            continue
        if len(s0) + len(s1) > 16:
            dropped.append((cid, f"landed at length {len(s0)+len(s1)}, not in T_16 range"))
            continue
        lines.append(f"{cid} {len(s0)} {' '.join(map(str,s0))} "
                     f"{len(s1)} {' '.join(map(str,s1))}")
        mp[cid] = {"dmoves": dm,
                   "landed": ["".join("xXyY"[c] for c in s0),
                              "".join("xXyY"[c] for c in s1)]}

    open(sys.argv[3], "w").write("\n".join(lines) + ("\n" if lines else ""))
    json.dump(mp, open(sys.argv[4], "w"), indent=1)
    print(f"BALLHITs: {len(hits)}   staged for path recovery: {len(mp)}   dropped: {len(dropped)}")
    for cid, why in dropped[:20]:
        print(f"  DROPPED {cid}: {why}")


if __name__ == "__main__":
    main()
