"""Generator symmetries of the AC graph, and the transport orbits they induce.

An automorphism phi of the free group F(x,y) commutes with every AC move:
inversion and multiplication are phi-equivariant outright, and conjugation
r -> g r g^-1 maps to phi(r) -> phi(g) phi(r) phi(g)^-1. So phi permutes the
14 moves of ac-r2-v1 by permuting the conjugators only, and induces a graph
automorphism of the capped AC graph. Components therefore come in
phi-isomorphic pairs of exactly equal size.

Emits the orbits of the pool under the seven non-trivial symmetries,
unioned with the components already measured by the transport sweep.
"""
import json, re
from collections import defaultdict

DATA = "/home/user/saircompetition/andrews-curtis/competition/tools/verifier/data"

# conjugator images: 1 = x, -1 = x^-1, 2 = y, -2 = y^-1
SYM = {"swap":     {1: 2, -1: -2, 2: 1, -2: -1},
       "x->X":     {1: -1, -1: 1, 2: 2, -2: -2},
       "y->Y":     {1: 1, -1: -1, 2: -2, -2: 2},
       "xy->XY":   {1: -1, -1: 1, 2: -2, -2: 2},
       "swapinvx": {1: -2, -1: 2, 2: 1, -2: -1},
       "swapinvy": {1: 2, -1: -2, 2: -1, -2: 1},
       "swapinv":  {1: -2, -1: 2, 2: -1, -2: 1}}

# move ids by (relator, conjugator); inversion 0,1 and multiplication 2..5 are fixed
CONJ = {(0, 1): 6, (0, -1): 7, (0, 2): 8, (0, -2): 9,
        (1, 1): 10, (1, -1): 11, (1, 2): 12, (1, -2): 13}


def move_relabel(sym):
    """The permutation phi induces on the 14 moves."""
    s = SYM[sym]
    rel = {m: m for m in range(6)}
    for (r, g), m in CONJ.items():
        rel[m] = CONJ[(r, s[g])]
    return rel


def inv(w):
    return [-c for c in reversed(w)]


def fr(w):
    o = []
    for c in w:
        if o and o[-1] == -c:
            o.pop()
        else:
            o.append(c)
    return o


def cyc(w):
    w = fr(w)
    while len(w) >= 2 and w[0] == -w[-1]:
        w = w[1:-1]
    return w


def canon(w):
    w = cyc(w)
    if not w:
        return ()
    return min(min(tuple(v[i:] + v[:i]) for i in range(len(v))) for v in (w, inv(w)))


def cp(rs):
    return tuple(sorted(canon(r) for r in rs))


def apply_sym(sym, relators):
    s = SYM[sym]
    return [fr([s[a] for a in w]) for w in relators]


def main():
    man = json.load(open(f"{DATA}/manifest.json"))
    ch = [c for c in man["challenges"] if c["challenge_id"].startswith("ac-")]
    R = {c["challenge_id"]: c["initial_relators"] for c in ch}
    idx = {cp(c["initial_relators"]): c["challenge_id"] for c in ch}
    assert len(idx) == len(ch), "pool is not distinct up to rotation/inversion/order"

    par = {c: c for c in R}

    def find(a):
        while par[a] != a:
            par[a] = par[par[a]]
            a = par[a]
        return a

    def uni(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            par[rb] = ra

    pairs = defaultdict(set)
    for cid in R:
        for name in SYM:
            o = idx.get(cp(apply_sym(name, R[cid])))
            if o and o != cid:
                pairs[name].add(tuple(sorted((cid, o))))
                uni(cid, o)
    for name in SYM:
        print(f"{name:9s}: {len(pairs[name]):5d} symmetry pairs")

    # fold in the measured transport components
    txt = open("tools/acc/ACC_NFOR1_TARGETS_v1.txt").read()
    for m in re.finditer(r"(\d+)x\s+rep\s+(ac-\d+)\s+->\s+\[([^\]]*)\]", txt):
        g = [m.group(2)] + re.findall(r"ac-\d+", m.group(3))
        for x in g[1:]:
            uni(g[0], x)

    ms = {r["challenge_id"]: r["status_at_freeze"]
          for r in (json.loads(l) for l in open("tools/acc/ms1190_to_challenge_v1.jsonl"))}
    openms = {k for k, v in ms.items() if v == "open"}

    orb = defaultdict(list)
    for c in R:
        orb[find(c)].append(c)
    out = []
    for v in orb.values():
        if any(x in openms for x in v):
            out.append({"size": len(v), "members": sorted(v),
                        "ms_open": sorted(x for x in v if x in openms)})
    out.sort(key=lambda z: -z["size"])
    with open("tools/acc/ac_msopen_orbits_v1.jsonl", "w") as f:
        for o in out:
            f.write(json.dumps(o) + "\n")
    tot = sum(o["size"] for o in out)
    print(f"\n{len(out)} orbits touching MS-open, covering {tot} challenges "
          f"({sum(len(o['ms_open']) for o in out)} MS-open)")
    print(f"mean challenges per MS-open solve: {tot/len(out):.2f}")


if __name__ == "__main__":
    main()
