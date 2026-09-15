"""Transport a verified certificate along a generator symmetry.

phi maps challenge A's presentation to something canonically equal to
challenge B's -- equal up to relator order, cyclic rotation and inversion,
which are the pool's own uniqueness relation but NOT free in the AC graph.
So the transported path is

    bridge(B -> phi(A))  +  relabel_phi(path_A)  +  target_fixup

and every step is replayed through the official verifier core, never a
re-implementation. Transport is sound but not length-preserving: the bridge
and fixup cost moves, so a transported path is generally LONGER than a
direct search. Its value is coverage on challenges with no path at all,
not improvement on ones already solved.
"""
import json, sys
from collections import deque

sys.path.insert(0, "/home/user/saircompetition/andrews-curtis/competition/tools")
from verifier import core  # noqa: E402
sys.path.insert(0, "tools/acc")
from ac_symmetry_orbits_v1 import SYM, move_relabel, apply_sym  # noqa: E402

DATA = "/home/user/saircompetition/andrews-curtis/competition/tools/verifier/data"
TARGET = ((1,), (2,))


def st(rs):
    return tuple(tuple(core.free_reduce(list(w))) for w in rs)


def bridge(a, b, maxdepth=12, cap=40):
    """Shortest move sequence a -> b, via the official core."""
    if a == b:
        return []
    seen, dq = {a}, deque([(a, [])])
    while dq:
        s, path = dq.popleft()
        if len(path) >= maxdepth:
            continue
        succ = 0
        for m in range(core.NUM_MOVES):
            try:
                t = core.apply_move(s, m)
            except Exception:
                continue
            succ += 1
            if t is None or sum(len(w) for w in t) > cap:
                continue
            if t == b:
                return path + [m]
            if t not in seen:
                seen.add(t)
                dq.append((t, path + [m]))
        assert succ > 0, "no successors -- dead search, do not trust a negative"
    return None


def transport(src_relators, src_moves, dst_relators, sym):
    """Return a verified path for dst, or None."""
    P = st(apply_sym(sym, src_relators))
    Q = st(dst_relators)
    br = bridge(Q, P)
    if br is None:
        return None
    rel = move_relabel(sym)
    for fixup in ([], [0], [1], [0, 1], [1, 0]):
        path = br + [rel[m] for m in src_moves] + fixup
        s = Q
        ok = True
        for m in path:
            s = core.apply_move(s, m)
            if s is None:
                ok = False
                break
        if ok and s == TARGET:
            return path
    return None


if __name__ == "__main__":
    import glob
    man = json.load(open(f"{DATA}/manifest.json"))
    R = {c["challenge_id"]: c["initial_relators"]
         for c in man["challenges"] if c["challenge_id"].startswith("ac-")}
    certs = {}
    for fn in glob.glob("tools/acc/ac_*certificates*_v1.jsonl"):
        for l in open(fn):
            r = json.loads(l)
            if r.get("moves"):
                certs.setdefault(r["challenge_id"], r["moves"])
    n = 0
    for src in sorted(certs):
        for sym in SYM:
            for dst in R:
                if dst == src:
                    continue
                from ac_symmetry_orbits_v1 import cp
                if cp(apply_sym(sym, R[src])) != cp(R[dst]):
                    continue
                p = transport(R[src], certs[src], R[dst], sym)
                if p:
                    n += 1
                    have = len(certs.get(dst, [])) or None
                    print(f"{src}({len(certs[src])}) --{sym}--> {dst}: "
                          f"{len(p)} moves" + (f"  [direct: {have}]" if have else ""))
    print(f"\n{n} verified transports")
