#!/usr/bin/env python3
"""Turn shared-ball MEET results on MINIMISED pairs into certificates for the
ORIGINAL rows.

Leverage: many rows minimise to the same pair (219 rows collapse to 181 distinct
pairs at total <= 16), so one search result can certify several rows at once --
each row supplies its own psi and its own prefix P, but they all reuse the same
solving path Q for the shared minimised pair.

Every emitted certificate is replayed against that row's ORIGINAL relators by
eyes/replay.py, and a row that does not replay to (x,y) is DROPPED, loudly. The
lift generates candidates; the replay decides.

Usage: python3 lift_certs.py <lift_targets.json> <meet.log> <out.json>
"""
import sys, json, collections
sys.path.insert(0, "/home/user/operator-first/tools/acc")
sys.path.insert(0, "/home/user/operator-first/tools/acc/eyes")
from wh_lift import transport, inverse_aut, ac_bridge, apply_aut
from replay import replay, free_reduce

P2C = {"x": 0, "X": 1, "y": 2, "Y": 3}


def parse_meets(path):
    """id -> move list, for every 'MEET' in a shared-ball log."""
    out, pending = {}, None
    for line in open(path):
        if " MEET len=" in line:
            pending = line.split()[0]
        elif line.startswith("MOVES") and pending:
            out[pending] = [int(t) for t in line.split()[1:]]
            pending = None
    return out


def main():
    targets = json.load(open(sys.argv[1]))
    meets = parse_meets(sys.argv[2])
    dst = sys.argv[3]

    by_pair = collections.defaultdict(list)
    for o in targets:
        by_pair[(o["m0"], o["m1"])].append(o)
    rep = {o["id"]: (o["m0"], o["m1"]) for o in targets}

    certs, dropped = [], []
    for cid, Q in meets.items():
        pair = rep.get(cid)
        if pair is None:
            dropped.append((cid, "meet id not in targets"))
            continue
        for o in by_pair[pair]:            # every row sharing this minimised pair
            r0 = [P2C[c] for c in o["r0"]]
            r1 = [P2C[c] for c in o["r1"]]
            psi = ([P2C[c] for c in o["psi"][0]], [P2C[c] for c in o["psi"][1]])
            try:
                moves = transport(o["P"] + Q, inverse_aut(psi))
            except Exception as e:
                dropped.append((o["id"], f"lift failed: {e}"))
                continue
            a, b, ok = replay(r0, r1, moves)
            if not ok:
                tail = ac_bridge(a, b, cap=max(24, len(a) + len(b) + 6))
                if tail is None:
                    dropped.append((o["id"], f"no bridge from ({len(a)},{len(b)})"))
                    continue
                moves = moves + tail
                _, _, ok = replay(r0, r1, moves)
            if not ok:
                dropped.append((o["id"], "lifted path does not reach (x,y)"))
                continue
            certs.append({"challengeId": o["id"], "moves": moves, "len": len(moves),
                          "via": f"{pair[0]}|{pair[1]}", "before": o["before"],
                          "after": o["after"]})

    certs.sort(key=lambda c: c["len"])
    json.dump(certs, open(dst, "w"), indent=1)
    print(f"meets parsed: {len(meets)}   certificates VERIFIED: {len(certs)}   dropped: {len(dropped)}")
    for cid, why in dropped[:20]:
        print(f"  DROPPED {cid}: {why}")
    for c in certs[:20]:
        print(f"  {c['challengeId']}  moves={c['len']}  raw_len={c['before']} -> min={c['after']}")


if __name__ == "__main__":
    main()
