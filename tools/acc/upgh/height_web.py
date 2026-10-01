#!/usr/bin/env python3
"""Height web: one global height map (exact distance to the goal) over every road the team holds, on every row, under the 16
symmetries, with 1-move junction edges, and optional 2-move junctions. Each row's best road in the web is then its start's height.

Idea taken from the Strong Papadimitriou-Ratajczak proof (ProofAtlas manuscript, 9 Sep 2026; summary by Lech Mazur): give every
junction a height so that from any junction some neighbour makes progress toward the destination, and let an established method
place the geometry afterwards without breaking the routing. Here:
  - junctions = every state on every verified road of every row, plus its 16 symmetric images (each image road is finished from
    g(goal) to the goal by the BFS finish, so every image road is a real road);
  - heights = BFS distance to the goal over road edges and every exact 1-move edge between any two junctions (hash join on the
    14 neighbours), so routing can hop across rows, lineages and symmetry frames many times, not once (foreign_meet.py: once);
  - geometry = the symmetry frame: the route is found in the web and realised move by move from the row's official start (each
    edge is an exact move between actual states), then replayed on the pinned official core.
With --r2, any non-junction state adjacent to two junctions (found by symmetry-normalised hashing) becomes a junction too
(2-move bridges). 0 API, no model.

usage: python3 tools/acc/upgh/height_web.py [--r2] [--kmax 99] [--out FILE]"""
import argparse
import glob
import sys
import time
from collections import deque
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import twin_lookup as T  # noqa: E402
from sources import load_board  # noqa: E402

core = T.core
SYMS = T.SYMS
MOVES = range(14)


def enc(s):
    """Exact compact key. Not hash(): in Python hash(-1) == hash(-2), so X and Y would collide."""
    return bytes(a + 3 for a in s[0]) + b"\x00" + bytes(a + 3 for a in s[1])


def seq_of(start, path):
    s, out = start, [start]
    for m in path:
        s = core.apply_move(s, m)
        out.append(s)
    return out


class Web:
    def __init__(self):
        self.id = {}          # enc(state) -> node id
        self.base = []        # base states (identity frame), by base index
        self.node_src = []    # node id -> (base index, symmetry index)
        self.adj = []

    def add_base(self, s):
        h = enc(s)
        if h in self.id:
            return
        b = len(self.base)
        self.base.append(s)
        for gi, g in enumerate(SYMS):
            t = T.apply_g(g, s)
            ht = enc(t)
            if ht not in self.id:
                self.id[ht] = len(self.node_src)
                self.node_src.append((b, gi))
                self.adj.append([])

    def state(self, nid):
        b, gi = self.node_src[nid]
        return T.apply_g(SYMS[gi], self.base[b])

    def link(self, a, b):
        if b not in self.adj[a]:
            self.adj[a].append(b)
            self.adj[b].append(a)

    def join(self, first_base=0):
        n = 0
        for bi in range(first_base, len(self.base)):
            s = self.base[bi]
            for m in MOVES:
                c = core.apply_move(s, m)
                hc = enc(c)
                if hc not in self.id or c == s:
                    continue
                for g in SYMS:
                    u, v = self.id.get(enc(T.apply_g(g, s))), self.id.get(enc(T.apply_g(g, c)))
                    if u is not None and v is not None and u != v:
                        self.link(u, v)
                        n += 1
        return n


def norm(s):
    return min(T.apply_g(g, s) for g in SYMS)


def build(maxlen=70, r2=False, log=print):
    """The web over every team road: returns (W, dist, roads, st). dist[node] = height (BFS distance to the goal)."""
    t0 = time.time()
    st = T.h.state()
    roads = T.team_roads()
    for c, b in st.best.items():
        if c.startswith("ac-"):
            roads.setdefault(c, {}).setdefault(tuple(b["moves"]), "ledger")
    W = Web()
    W.add_base(T.GOAL)
    for g in SYMS:                                   # finish roads g(goal) -> goal
        e = T.apply_g(g, T.GOAL)
        f = T.finish(e)
        if f is not None:
            for s in seq_of(e, f):
                W.add_base(s)
    nroads = 0
    for cid, rs in roads.items():
        if cid not in T.REL:
            continue
        for p in rs:
            q = seq_of(T.REL[cid], p)
            if q[-1] != T.GOAL:
                continue
            nroads += 1
            for s in q:
                if sum(map(len, s)) <= maxlen or s == q[0]:
                    W.add_base(s)
    nb = len(W.base)
    log("roads %d, base junctions %d, nodes with images %d (%.0fs)" % (nroads, nb, len(W.node_src), time.time() - t0))
    ne = W.join()
    log("1-move edges (with images) %d (%.0fs)" % (ne, time.time() - t0))
    if r2:
        seen, extra = {}, []
        for bi in range(nb):
            s = W.base[bi]
            for m in MOVES:
                c = core.apply_move(s, m)
                if enc(c) in W.id or sum(map(len, c)) > maxlen:
                    continue
                k = enc(norm(c))
                if k in seen:
                    if seen[k] is not None:
                        extra.append(seen[k])
                        seen[k] = None
                    extra.append(c)
                else:
                    seen[k] = c
        for c in extra:
            W.add_base(c)
        ne2 = W.join(first_base=nb)
        log("2-move junctions %d, extra edges %d, nodes %d (%.0fs)" % (len(extra), ne2, len(W.node_src), time.time() - t0))
    goal = W.id[enc(T.GOAL)]
    dist = [-1] * len(W.node_src)
    dist[goal] = 0
    dq = deque([goal])
    while dq:
        u = dq.popleft()
        for v in W.adj[u]:
            if dist[v] < 0:
                dist[v] = dist[u] + 1
                dq.append(v)
    log("heights computed (%.0fs)" % (time.time() - t0))
    return W, dist, roads, st


def descend(W, dist, s):
    """Moves from state s (a junction) down the heights to the goal, or None."""
    path, cur = [], s
    while cur != T.GOAL:
        hc = dist[W.id[enc(cur)]]
        for m in MOVES:
            c = core.apply_move(cur, m)
            v = W.id.get(enc(c))
            if v is not None and 0 <= dist[v] == hc - 1:
                path.append(m)
                cur = c
                break
        else:
            return None
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--r2", action="store_true", help="add 2-move junctions")
    ap.add_argument("--kmax", type=int, default=99)
    ap.add_argument("--maxlen", type=int, default=70, help="skip states with relator total above this")
    ap.add_argument("--out")
    a = ap.parse_args()
    t0 = time.time()
    A = load_board(sorted(glob.glob(str(T.REPO / "research/acc/live/boards/ac_2026*.json.gz")))[-1])
    never = set(T.h.cfg["gates"].get("never_rows", []))
    W, dist, roads, st = build(a.maxlen, a.r2)
    hits = []
    for cid in sorted(roads):
        if cid not in T.REL or cid.split("-")[1] in never:
            continue
        sid = W.id.get(enc(T.REL[cid]))
        if sid is None or dist[sid] < 0:
            continue
        ours = min(len(p) for p in roads[cid])
        if dist[sid] >= ours:
            continue
        path = descend(W, dist, T.REL[cid])
        ver = core.verify(T.CH[cid], path, "ac-r2-v1", T.man["limits"]) if path is not None else {"ok": False, "why": "no descent"}
        if not ver["ok"]:
            print("  %s: web height %d but the route did not replay (%s; ours %d)" % (cid, dist[sid], str(ver)[:160], ours))
            continue
        r = A.get(cid, {})
        if (r.get("k") or 99) > a.kmax:
            continue
        hits.append((cid, ours, len(path), r.get("record"), r.get("k"), path))
    print("rows whose web height is below every road we hold: %d" % len(hits))
    for h in sorted(hits, key=lambda h: (h[2] - (h[3] or 0), h[0])):
        tag = "  <= RECORD" if h[3] is not None and h[2] <= h[3] else ""
        print("  %s %d -> %d (record %s, k %s)%s" % (h[0], h[1], h[2], h[3], h[4], tag))
    if a.out and hits:
        Path(a.out).write_text("# UPG-H height web (paper idea: Strong Papadimitriou-Ratajczak, heights for greedy routing); "
                               "official core ok\n" + "".join("%s: [%s]\n" % (h[0], ", ".join(map(str, h[5]))) for h in hits))
        print("wrote", a.out)
    print("done (%.0fs)" % (time.time() - t0))


if __name__ == "__main__":
    main()
