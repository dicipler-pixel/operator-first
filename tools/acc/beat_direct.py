#!/usr/bin/env python3
"""Certificates straight from a descball2 SOLVED line -- no tail stage.

descball2 finishes inside the ball, so a SOLVED entry's DMOVES is already a
complete path from the row's own relators to (x,y). This compresses it, replays
it, and keeps it only if it lands exactly on the target AND beats the standing
record.

BALLHIT entries (reached T_16 but did not finish within FINSTEPS) are counted
and reported, not silently dropped -- they are real hits whose tail still has to
come from the shared ball.

Usage: beat_direct.py <beat_meta.json> <pairs.txt> <descball2.log> <out.json>
"""
import sys, json
sys.path.insert(0, "/home/user/operator-first/tools/acc")
sys.path.insert(0, "/home/user/operator-first/tools/acc/eyes")
from path_compress import compress
from replay import replay


def parse(path):
    """id -> (kind, moves) for SOLVED and BALLHIT entries."""
    out, pend = {}, None
    for line in open(path):
        if " SOLVED " in line:
            pend = (line.split()[0], "SOLVED")
        elif " BALLHIT " in line:
            pend = (line.split()[0], "BALLHIT")
        elif line.startswith("DMOVES") and pend:
            out[pend[0]] = (pend[1], [int(t) for t in line.split()[1:]])
            pend = None
    return out


def main():
    meta = json.load(open(sys.argv[1]))
    pairs = {}
    for line in open(sys.argv[2]):
        t = line.split()
        if not t:
            continue
        cid, l0 = t[0], int(t[1])
        a = [int(x) for x in t[2:2 + l0]]
        l1 = int(t[2 + l0])
        b = [int(x) for x in t[3 + l0:3 + l0 + l1]]
        pairs[cid] = (a, b)
    entries = parse(sys.argv[3])

    certs, ctl, ballonly, dropped = [], [], 0, []
    for cid, (kind, mv) in entries.items():
        if kind == "BALLHIT":
            ballonly += 1
            continue
        a, b = pairs[cid]
        try:
            mv = compress(a, b, mv)
        except AssertionError as e:
            dropped.append((cid, f"compression broke the path: {e}")); continue
        _, _, ok = replay(a, b, mv)
        if not ok:
            dropped.append((cid, "does not replay to (x,y)")); continue
        if cid.startswith("pd-"):
            ctl.append((cid, len(mv))); continue
        m = meta.get(cid)
        if m is None:
            dropped.append((cid, "no record metadata")); continue
        if len(mv) >= m["best"]:
            dropped.append((cid, f"len {len(mv)} >= record {m['best']}")); continue
        certs.append({"challengeId": cid, "moves": mv, "len": len(mv),
                      "record": m["best"], "kTeams": m["kTeams"],
                      "saving": m["best"] - len(mv)})

    certs.sort(key=lambda c: -c["saving"])
    json.dump(certs, open(sys.argv[4], "w"), indent=1)
    print(f"controls SOLVED and replay-verified: {len(ctl)}  lengths {[l for _,l in ctl][:12]}")
    print(f"rows SOLVED: {sum(1 for k,_ in entries.values() if k=='SOLVED') - len(ctl)}"
          f"   reached ball but unfinished: {ballonly}")
    print(f"BEATING certificates (replay-verified, strictly shorter): {len(certs)}")
    for c in certs[:40]:
        print(f"  {c['challengeId']}  {c['record']} -> {c['len']}  "
              f"(saves {c['saving']}, kTeams={c['kTeams']})")
    if dropped:
        why = {}
        for _c, w in dropped:
            k = w.split(" len ")[0] if "len " not in w else "did not beat record"
            why[k] = why.get(k, 0) + 1
        print("dropped:", why)


if __name__ == "__main__":
    main()
