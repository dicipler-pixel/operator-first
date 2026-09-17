#!/usr/bin/env python3
"""Assemble record-beating certificates from a descent-into-the-ball run.

    DMOVES   r -> s        (descball, s a member of T_16)
    TAIL     s -> (x,y)    (shared ball, found at depth 0 since s is a member)

Concatenate, compress, replay against the row's ORIGINAL relators, and keep the
result ONLY if it lands exactly on (x,y) AND is strictly shorter than the
board's current record. On this board length is the score: a tie is worth
2^(1-k) shared, beating outright is worth 1.0 as sole holder.

Compression matters here more than anywhere else. descball records the walk it
actually took, and a temperature-driven walk loops constantly; path_compress
splices those loops out. The compressed path is re-replayed, never assumed.

Nothing is emitted that has not landed on (x,y) under eyes/replay.py.

Usage: beat_certs.py <beat_meta.json> <descball_map.json> <tail_meet.log> <out.json>
"""
import sys, json
sys.path.insert(0, "/home/user/operator-first/tools/acc")
sys.path.insert(0, "/home/user/operator-first/tools/acc/eyes")
from path_compress import compress
from lift_certs import parse_meets
from replay import replay

P2C = {"x": 0, "X": 1, "y": 2, "Y": 3}


def main():
    meta = json.load(open(sys.argv[1]))
    dmap = json.load(open(sys.argv[2]))
    tails = parse_meets(sys.argv[3])
    dst = sys.argv[4]

    certs, dropped = [], []
    for cid, d in dmap.items():
        m = meta.get(cid)
        if m is None:
            dropped.append((cid, "row not in meta")); continue
        tail = tails.get(cid)
        if tail is None:
            dropped.append((cid, "no tail path recovered")); continue
        r0 = [P2C[c] for c in m["r0"]]
        r1 = [P2C[c] for c in m["r1"]]
        moves = list(d["dmoves"]) + list(tail)
        try:
            moves = compress(r0, r1, moves)
        except AssertionError as e:
            dropped.append((cid, f"compression broke the path: {e}")); continue
        _, _, ok = replay(r0, r1, moves)
        if not ok:
            dropped.append((cid, "path does not replay to (x,y)")); continue
        if len(moves) >= m["best"]:
            dropped.append((cid, f"len {len(moves)} does not beat record {m['best']}"))
            continue
        certs.append({"challengeId": cid, "moves": moves, "len": len(moves),
                      "record": m["best"], "kTeams": m["kTeams"],
                      "saving": m["best"] - len(moves)})

    certs.sort(key=lambda c: -c["saving"])
    json.dump(certs, open(dst, "w"), indent=1)
    print(f"descball hits: {len(dmap)}   BEATING certificates: {len(certs)}   dropped: {len(dropped)}")
    for c in certs[:40]:
        print(f"  {c['challengeId']}  {c['record']} -> {c['len']}  "
              f"(saves {c['saving']}, kTeams={c['kTeams']})")
    seen = {}
    for _cid, why in dropped:
        k = why.split(" len ")[0]
        seen[k] = seen.get(k, 0) + 1
    if seen:
        print("dropped reasons:", seen)


if __name__ == "__main__":
    main()
