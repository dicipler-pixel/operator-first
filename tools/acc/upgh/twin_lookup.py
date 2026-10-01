#!/usr/bin/env python3
"""Twin lookup: for given AC rows, list every other row that is the same presentation up to a symmetry, and transfer the
team's roads from each twin as fully paid witnesses (0 API calls, no model).

Symmetries: g = (perm, sx, sy, rswap): perm swaps x<->y, sx/sy invert x/y, rswap swaps the relator order; then each relator
may also be inverted or cyclically rotated. A twin route is built as
    prefix (paid moves on the target row: 1 inversion move per inverted relator, 1 conjugation move per rotation step)
  + the donor route with every move relabelled by g (conjugators mapped by the letter map, relator indices by rswap)
  + an exact shortest finish from g((x),(y)) to ((x),(y)) found by BFS.
Every emitted path is replayed from the official start with the pinned core (ac-r2-v1). Nothing is erased by class
equivalence: every junction cost is a real move in the path.

usage: python3 tools/acc/upgh/twin_lookup.py ROW [ROW ...] [--out FILE]"""
import argparse
import itertools
import json
import sys
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
from harness import Harness  # noqa: E402
from harvest import extract  # noqa: E402

h = Harness(config_path=HERE / "config.json", state_dir=REPO / "research/acc/upgh", repo=REPO)
sys.path.insert(0, str(h.sair_dir / "competition/tools"))
from verifier import core  # noqa: E402

man = json.load(open(h.sair_dir / "competition/tools/verifier/data/manifest.json"))
CH = {c["challenge_id"]: c for c in man["challenges"]}
REL = {cid: tuple(tuple(r) for r in c["initial_relators"]) for cid, c in CH.items() if cid.startswith("ac-")}
SYMS = [(p, sx, sy, rs) for p in (0, 1) for sx in (1, -1) for sy in (1, -1) for rs in (0, 1)]
CONJ = {6: (0, 1), 7: (0, -1), 8: (0, 2), 9: (0, -2), 10: (1, 1), 11: (1, -1), 12: (1, 2), 13: (1, -2)}
CONJ_INV = {v: k for k, v in CONJ.items()}
BASIC = {0: ("inv", 0), 1: ("inv", 1), 2: ("mul", 0, 1), 3: ("mulinv", 0, 1), 4: ("mul", 1, 0), 5: ("mulinv", 1, 0)}
BASIC_INV = {v: k for k, v in BASIC.items()}
GOAL = ((1,), (2,))


def lmap(g, t):
    p, sx, sy, _ = g
    gen, sgn = abs(t), (1 if t > 0 else -1)
    sgn *= sx if gen == 1 else sy
    return sgn * ((3 - gen) if p else gen)


def apply_g(g, pres):
    r = tuple(tuple(lmap(g, t) for t in w) for w in pres)
    return (r[1], r[0]) if g[3] else r


def mmap(g, m):
    rs = g[3]
    if m in CONJ:
        rel, c = CONJ[m]
        return CONJ_INV[((1 - rel) if rs else rel, lmap(g, c))]
    b = BASIC[m]
    if b[0] == "inv":
        return BASIC_INV[("inv", (1 - b[1]) if rs else b[1])]
    i, j = (1 - b[1], 1 - b[2]) if rs else (b[1], b[2])
    return BASIC_INV[(b[0], i, j)]


def inv(w):
    return tuple(-t for t in reversed(w))


def cyc_reduced(w):
    return len(w) < 2 or w[0] != -w[-1]


def ccanon(w):
    if not cyc_reduced(w):
        return w
    return min([w[i:] + w[:i] for i in range(len(w))] + [inv(w)[i:] + inv(w)[:i] for i in range(len(w))])


def prefix_moves(B, T):
    out, s = [], B
    for i in (0, 1):
        found = None
        if cyc_reduced(s[i]):
            for do_inv in (0, 1):
                w = inv(s[i]) if do_inv else s[i]
                for k in range(len(w)):
                    if w[k:] + w[:k] == T[i]:
                        found = (do_inv, k)
                        break
                if found:
                    break
        elif s[i] == T[i]:
            found = (0, 0)
        if found is None:
            return None
        do_inv, k = found
        if do_inv:
            out.append(i)
            s = core.apply_move(s, i)
        n = len(s[i])
        for _ in range(k if k <= n - k else n - k):
            c = -s[i][0] if k <= n - k else s[i][-1]
            m = CONJ_INV[(i, c)]
            out.append(m)
            s = core.apply_move(s, m)
    return out if s == T else None


_fin = {}


def finish(state, limit=6):
    if state in _fin:
        return _fin[state]
    seen, q = {state: []}, deque([state])
    while q:
        s = q.popleft()
        if s == GOAL:
            _fin[state] = seen[s]
            return seen[s]
        if len(seen[s]) < limit:
            for m in range(14):
                t = core.apply_move(s, m)
                if t not in seen and sum(map(len, t)) <= 8:
                    seen[t] = seen[s] + [m]
                    q.append(t)
    _fin[state] = None
    return None


def key(pres):
    return min(tuple(ccanon(w) for w in apply_g(g, pres)) for g in SYMS)


def team_roads():
    """Every AC road the team holds: UPG-H ledger path.best history plus team files under research/acc/live and ACC_*.txt."""
    roads = {}
    for line in open(REPO / "research/acc/upgh/ledger.jsonl", encoding="utf-8"):
        if '"path.best"' in line:
            d = json.loads(line)["data"]
            if d.get("cid", "").startswith("ac-"):
                roads.setdefault(d["cid"], {}).setdefault(tuple(d["moves"]), "UPG-H ledger path.best")
    files = list((REPO / "research/acc/live").rglob("*.txt")) + list(REPO.glob("ACC_*.txt"))
    for f in files:
        if f.stat().st_size > 30_000_000:
            continue
        for cid, moves, _ in extract(f):
            if cid.startswith("ac-"):
                roads.setdefault(cid, {}).setdefault(tuple(moves), f.relative_to(REPO).as_posix())
    return roads


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("rows", nargs="+")
    ap.add_argument("--out")
    a = ap.parse_args()
    groups = {}
    for cid, pres in REL.items():
        groups.setdefault(key(pres), []).append(cid)
    roads = team_roads()
    lines, summary = [], []
    for b in a.rows:
        twins = [t for t in groups[key(REL[b])] if t != b]
        lines.append("# %s start %s; twins: %s" % (b, json.dumps([list(w) for w in REL[b]]), ", ".join(twins) or "none"))
        best = None
        for t in twins:
            for g in SYMS:
                T = apply_g(g, REL[t])
                if tuple(ccanon(w) for w in T) != tuple(ccanon(w) for w in REL[b]):
                    continue
                pre = prefix_moves(REL[b], T)
                if pre is None:
                    continue
                lines.append("#   twin %s start %s; symmetry (perm, sx, sy, relator swap) = %s; paid prefix %s (%d moves)"
                             % (t, json.dumps([list(w) for w in REL[t]]), g, pre, len(pre)))
                for route, src in sorted(roads.get(t, {}).items(), key=lambda kv: len(kv[0]))[:3]:
                    body = [mmap(g, m) for m in route]
                    s = REL[b]
                    for m in pre + body:
                        s = core.apply_move(s, m)
                    fin = finish(s)
                    if fin is None:
                        continue
                    p = pre + body + fin
                    if core.verify(CH[b], p, "ac-r2-v1", man["limits"])["ok"]:
                        lines.append("#     donor road %d moves from %s; finish %s; total %d, official core ok" % (len(route), src, fin, len(p)))
                        lines.append("%s: [%s]" % (b, ", ".join(map(str, p))))
                        best = len(p) if best is None else min(best, len(p))
                break
        summary.append((b, len(twins), best))
        lines.append("")
    text = "\n".join(lines) + "\n"
    if a.out:
        Path(a.out).write_text(text)
    print("row, twins, best transferred road:", summary)


if __name__ == "__main__":
    main()
