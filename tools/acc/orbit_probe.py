#!/usr/bin/env python3
"""Generate every length-<=LIMIT member of each unsolved row's automorphism
orbit, with the bookkeeping needed to lift a hit back to the original row.

Output: a shared-ball challenge file (one orbit element per line) plus a sidecar
recording, for each element, which row it came from and the (chi, P) pair that
carries the row's minimised form to it.
"""
import sys, json
sys.path.insert(0, "/home/user/operator-first/tools/acc")
from aut_orbit import orbit

L = "xXyY"


def main():
    targets = json.load(open(sys.argv[1]))
    lim = int(sys.argv[2])           # BFS bound: excursions allowed up to here
    keep = int(sys.argv[3])          # only elements this short are testable
    chfile, sidecar = sys.argv[4], sys.argv[5]

    lines, side, shorter = [], [], 0
    for n, o in enumerate(targets):
        m0 = [L.index(c) for c in o["m0"]]
        m1 = [L.index(c) for c in o["m1"]]
        orb = orbit(m0, m1, lim)
        best = min(len(u) + len(v) for u, v in orb)
        if best < o["after"]:
            shorter += 1
        for (u, v), (chi, P) in orb.items():
            if len(u) + len(v) > keep:
                continue
            idx = len(side)
            lines.append(f"e{idx} {len(u)} {' '.join(map(str, u))} "
                         f"{len(v)} {' '.join(map(str, v))}")
            side.append({"e": f"e{idx}", "id": o["id"], "after": o["after"],
                         "len": len(u) + len(v),
                         "u": "".join(L[c] for c in u),
                         "v": "".join(L[c] for c in v),
                         "chi": ["".join(L[c] for c in chi[0]),
                                 "".join(L[c] for c in chi[1])],
                         "P": P})
        if n % 400 == 0:
            print(f"  {n}/{len(targets)} rows, {len(side)} elements", flush=True)

    open(chfile, "w").write("\n".join(lines) + "\n")
    json.dump(side, open(sidecar, "w"))
    print(f"rows: {len(targets)}   testable orbit elements (<= {keep}): {len(side)}")
    print(f"rows whose BFS orbit beats greedy Whitehead descent: {shorter}")


if __name__ == "__main__":
    main()
