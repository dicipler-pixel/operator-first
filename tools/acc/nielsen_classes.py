#!/usr/bin/env python3
"""Nielsen-class routing map over the unsolved ACC rows.

Two steps, both exact and both cheap:

1. WHITEHEAD MINIMISE.  Iterate the finite rank-2 Type-II family (wh_min.MAPS)
   to a fixed point, so every row is represented by a cyclically-shortest
   member of its automorphism orbit.  This is the step the retracted
   cut-vertex eye got wrong; see wh_min.py for the correction.

2. QUOTIENT BY THE LENGTH-PRESERVING SYMMETRIES.  Type-I signed permutations
   of {x,X,y,Y} (8 of them), relator inversion, and cyclic rotation.
   Canonical key = lexicographic minimum over that orbit.

   The r0/r1 SWAP is deliberately NOT quotiented out.  Nielsen theory would
   include it, but the ACC move set 0-13 has no exchange move, so a swapped
   pair is a different search problem here and merging the two would over-route.
   Including it would collapse 1202 classes to 1157.

SCOPE FENCE — read this before using the output.

    Same Nielsen class is NOT a transferable CLOSED count, and NOT a
    transferable solution.

This session has now been burned three separate times by assuming otherwise
(ac-00945/ac-05233 both 386,320 with intersection 0; ac-00026/ac-00036 both
12,012 with intersection 0; the 92,600 family, which conjugacy BFS denied
outright).  The AC moves 0-13 are NOT the Nielsen moves: there is no swap
move and no inverse-automorphism move in the ACC move set, so two rows in
one Nielsen class can sit in disjoint AC components.  What this map is good
for is ROUTING ONLY: it says which IDs are worth attacking with the same
search shape, and which are worth a direct 6-13 conjugacy bridge test.
Every ID still needs its own compiled 0-13 path before anything is claimed.

The unsolved set is read from the CURRENT board snapshot (which carries
status/currentBestLength but no relators); the relators come from the earlier
snapshot that does carry them.  Using the older file for both inflates the lane
by the 58 rows first-solved in between.

Usage:  python3 nielsen_classes.py <snapshot_items.json> <snapshot_items_prev.json> [out.json]
"""
import sys, json, collections
sys.path.insert(0, "/home/user/operator-first/tools/acc")
from wh_min import MAPS, cyc, apply_map, cyclen

L = "xXyY"
C2P = {1: 0, -1: 1, 2: 2, -2: 3}


def minimise_fully(r0, r1):
    """Iterate Type-II to a true fixed point (one pass is not enough)."""
    cur = (cyc(r0), cyc(r1))
    while True:
        base = cyclen(*cur)
        best = None
        for _name, img in MAPS:
            n0 = cyc(apply_map(cur[0], img))
            n1 = cyc(apply_map(cur[1], img))
            c = len(n0) + len(n1)
            if c < base and (best is None or c < best[0]):
                best = (c, (n0, n1))
        if best is None:
            return cur
        cur = best[1]


def type1_maps():
    """Signed permutations of {x,X,y,Y}: bijections commuting with inversion."""
    out = []
    for img0 in range(4):
        for img2 in range(4):
            if img2 >> 1 == img0 >> 1:
                continue
            s = {0: img0, 1: img0 ^ 1, 2: img2, 3: img2 ^ 1}
            out.append(s)
    return out


T1 = type1_maps()


def canon_word(w):
    """Least cyclic rotation of w or of w^-1.

    Ordered on the LETTER CODES (x<X<y<Y), not on ASCII -- in ASCII 'X' sorts
    before 'x' and the chosen representative flips case.  Same partition either
    way, different spelling of the key.
    """
    if not w:
        return ()
    best = None
    for v in (w, [c ^ 1 for c in reversed(w)]):
        d = v + v
        for i in range(len(v)):
            r = tuple(d[i:i + len(v)])
            if best is None or r < best:
                best = r
    return best


def canon(r0, r1):
    """Lexicographic minimum over Type-I x inversion x rotation (no swap)."""
    best = None
    for s in T1:
        k = (canon_word([s[c] for c in r0]), canon_word([s[c] for c in r1]))
        if best is None or k < best:
            best = k
    return "".join(L[c] for c in best[0]) + "|" + "".join(L[c] for c in best[1])


def main():
    cur = sys.argv[1] if len(sys.argv) > 1 else "snapshot_items.json"
    prev = sys.argv[2] if len(sys.argv) > 2 else "snapshot_items_prev.json"
    dst = sys.argv[3] if len(sys.argv) > 3 else "ac_nielsen_classes_v1.json"
    unsolved = {i["challengeId"] for i in json.load(open(cur))
                if i.get("currentBestLength") is None}
    items = json.load(open(prev))
    classes = collections.defaultdict(list)
    n = 0
    for it in items:
        if it["challengeId"] not in unsolved:
            continue                      # solved rows are not in the lane
        r = it["initialRelators"]
        r0 = [C2P[c] for c in r[0]]
        r1 = [C2P[c] for c in r[1]]
        m0, m1 = minimise_fully(r0, r1)
        classes[canon(m0, m1)].append(it["challengeId"])
        n += 1
    for k in classes:
        classes[k].sort()
    out = dict(sorted(classes.items(), key=lambda kv: kv[1][0]))
    json.dump(out, open(dst, "w"), indent=1)
    hist = collections.Counter(len(v) for v in out.values())
    shared = sum(len(v) for v in out.values() if len(v) > 1)
    print(f"rows: {n}   distinct classes: {len(out)}")
    print("class-size histogram:", dict(sorted(hist.items())))
    print("rows sharing a class with at least one other:", shared)
    return out


if __name__ == "__main__":
    out = main()
    # Five facts established INDEPENDENTLY, before this map existed.
    where = {}
    for k, v in out.items():
        for cid in v:
            where[cid] = (k, len(v))
    def chk(cid):
        return where.get(cid, ("<solved/absent>", 0))
    for a, b, why in [("ac-02842", "ac-06556", "ChatGPT twin pair"),
                      ("ac-03467", "ac-08126", "verified 12-move bridge")]:
        print(f"{a} / {b}: same class = {chk(a)[0] == chk(b)[0]} "
              f"(size {chk(a)[1]})   [{why}]")
    for cid, rec, why in [("ac-00945", 26, "branch-root R_7"),
                          ("ac-02799", 20, "branch-root R_6"),
                          ("ac-02842", 14, "branch-root n=3"),
                          ("ac-01440", 14, "branch-root n=4"),
                          ("ac-01223", 14, "branch-root n=5")]:
        got = chk(cid)[1]
        print(f"{cid}: derived {got} vs recorded {rec} -> "
              f"{'MATCH' if got == rec else 'MISMATCH'}   [{why}]")
