#!/usr/bin/env python3
"""Price a shared-ball meet log against the board. The missing step.

Everything in this repo produced diagnostics; this turns a meet into a
SUBMITTABLE, PRICED certificate. For each path it: compresses, replays against
the row's original relators, and compares the length to the standing record.

Scoring on this board: k teams tied at the shortest length each get 2^(1-k).
So a TIE against a sole holder is worth 0.5 and is worth submitting -- ties are
not failures. Beating outright is worth 1.0.

Output buckets:
  BEAT   strictly shorter than the record   -> sole holder, 1.0
  TIE    equal to the record                -> 2^(1-k) share
  FIRST  row currently unsolved             -> a first solve
  WORSE  longer than the record             -> kept out of the certificate file

A path that does not replay to exactly (x,y) is DROPPED and named. Nothing
reaches the certificate file on trust.

Usage: price_meets.py <pairs.txt> <meet.log> <meta.json> <out.json>
"""
import sys, json
sys.path.insert(0, "/home/user/operator-first/tools/acc")
sys.path.insert(0, "/home/user/operator-first/tools/acc/eyes")
from path_compress import compress
from lift_certs import parse_meets
from replay import replay

L = "xXyY"


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
    meets = parse_meets(sys.argv[2])
    meta = json.load(open(sys.argv[3]))

    out = {"BEAT": [], "TIE": [], "FIRST": [], "WORSE": []}
    dropped, controls = [], []
    for cid, mv in meets.items():
        if cid not in pairs:
            continue
        # CONTROLS ARE NOT CERTIFICATES. Synthetic pairs (pc-*, pd-*) are built by
        # this session to prove an engine works; they are not board rows and have
        # no record. Pricing them as FIRST solves invents score out of nothing --
        # an early run of this tool reported "25 certificates, value 25.00" that
        # were all controls. Anything with no board metadata is a control or a
        # mistake, and either way it is not submittable.
        if cid.startswith("pc-") or cid.startswith("pd-") or cid not in meta:
            controls.append(cid)
            continue
        a, b = pairs[cid]
        raw = len(mv)
        try:
            mv = compress(a, b, mv)
        except AssertionError as e:
            dropped.append((cid, f"compression broke the path: {e}")); continue
        _, _, ok = replay(a, b, mv)
        if not ok:
            dropped.append((cid, "does not replay to (x,y)")); continue
        m = meta[cid]
        rec, kt = m.get("best"), m.get("kTeams")
        e = {"challengeId": cid, "moves": mv, "len": len(mv), "raw_path": raw,
             "record": rec, "kTeams": kt,
             "r0": "".join(L[c] for c in a), "r1": "".join(L[c] for c in b)}
        if rec is None:
            e["value"] = 1.0; out["FIRST"].append(e)
        elif len(mv) < rec:
            e["value"] = 1.0; e["saving"] = rec - len(mv); out["BEAT"].append(e)
        elif len(mv) == rec:
            e["value"] = 2 ** (1 - ((kt or 1) + 1)); out["TIE"].append(e)
        else:
            out["WORSE"].append(e)

    for k in ("BEAT", "TIE", "FIRST"):
        out[k].sort(key=lambda c: -(c.get("saving") or c.get("value") or 0))
    json.dump({k: v for k, v in out.items() if k != "WORSE"},
              open(sys.argv[4], "w"), indent=1)

    val = sum(c["value"] for k in ("BEAT", "TIE", "FIRST") for c in out[k])
    print(f"meets {len(meets)} ({len(controls)} were controls, not priced)  ->  "
          f"FIRST {len(out['FIRST'])}  BEAT {len(out['BEAT'])}"
          f"  TIE {len(out['TIE'])}  worse {len(out['WORSE'])}  dropped {len(dropped)}")
    print(f"estimated score value of the submittable set: {val:.2f}")
    for k in ("FIRST", "BEAT", "TIE"):
        for c in out[k][:25]:
            print(f"  {k:5s} {c['challengeId']}  len={c['len']}  record={c['record']}"
                  f"  kTeams={c['kTeams']}  value={c['value']}")
    for cid, why in dropped[:15]:
        print(f"  DROPPED {cid}: {why}")


if __name__ == "__main__":
    main()
