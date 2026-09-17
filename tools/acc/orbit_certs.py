#!/usr/bin/env python3
"""Turn a shared-ball hit on an ORBIT ELEMENT into a certificate for the
ORIGINAL row.

Three nested changes of coordinates, each already unit-tested:

    P_row    carries (psi r0, psi r1) -> (m0, m1)         [minimise_record]
    P_orb    carries (chi m0, chi m1) -> (u, v)           [aut_orbit]
    Q        carries (u, v)           -> (x, y)           [shared ball]

so, composing outward,

    inner = P_orb + Q                    solves (chi m0, chi m1)
    mid   = P_row + transport(inner, chi^-1)
                                         drives (psi r0, psi r1) to chi^-1(x,y)
    moves = transport(mid, psi^-1)       drives (r0, r1) to psi^-1 chi^-1 (x,y)

which is a basis pair, and a short AC search closes the gap. The result is then
replayed against the row's ORIGINAL relators; anything that does not land
exactly on (x,y) is DROPPED and reported, never emitted.

Usage: python3 orbit_certs.py <lift_targets.json> <orbit_side.json> <meet.log> <out.json>
"""
import sys, json
sys.path.insert(0, "/home/user/operator-first/tools/acc")
sys.path.insert(0, "/home/user/operator-first/tools/acc/eyes")
from wh_lift import transport, inverse_aut, ac_bridge
from lift_certs import parse_meets
from replay import replay

P2C = {"x": 0, "X": 1, "y": 2, "Y": 3}


def w(s):
    return [P2C[c] for c in s]


def main():
    targets = {o["id"]: o for o in json.load(open(sys.argv[1]))}
    side = {e["e"]: e for e in json.load(open(sys.argv[2]))}
    meets = parse_meets(sys.argv[3])
    dst = sys.argv[4]

    certs, dropped, seen = [], [], set()
    for eid, Q in meets.items():
        el = side.get(eid)
        if el is None:
            dropped.append((eid, "hit id not in orbit sidecar"))
            continue
        row = targets[el["id"]]
        if row["id"] in seen:
            continue
        r0, r1 = w(row["r0"]), w(row["r1"])
        psi = (w(row["psi"][0]), w(row["psi"][1]))
        chi = (w(el["chi"][0]), w(el["chi"][1]))
        try:
            inner = el["P"] + list(Q)
            mid = row["P"] + transport(inner, inverse_aut(chi))
            moves = transport(mid, inverse_aut(psi))
        except Exception as e:
            dropped.append((row["id"], f"lift failed: {e}"))
            continue
        a, b, ok = replay(r0, r1, moves)
        if not ok:
            tail = ac_bridge(a, b, cap=max(24, len(a) + len(b) + 6))
            if tail is None:
                dropped.append((row["id"], f"no bridge from ({len(a)},{len(b)})"))
                continue
            moves = moves + tail
            _, _, ok = replay(r0, r1, moves)
        if not ok:
            dropped.append((row["id"], "lifted path does not reach (x,y)"))
            continue
        seen.add(row["id"])
        certs.append({"challengeId": row["id"], "moves": moves, "len": len(moves),
                      "raw_len": row["before"], "min_len": row["after"],
                      "orbit_elem": f"{el['u']}|{el['v']}", "orbit_len": el["len"]})

    certs.sort(key=lambda c: c["len"])
    json.dump(certs, open(dst, "w"), indent=1)
    print(f"ball hits: {len(meets)}   rows CERTIFIED (replay-verified): {len(certs)}"
          f"   dropped: {len(dropped)}")
    for cid, why in dropped[:20]:
        print(f"  DROPPED {cid}: {why}")
    for c in certs[:30]:
        print(f"  {c['challengeId']}  moves={c['len']}  raw={c['raw_len']} "
              f"min={c['min_len']} via orbit elem len {c['orbit_len']}")


if __name__ == "__main__":
    main()
