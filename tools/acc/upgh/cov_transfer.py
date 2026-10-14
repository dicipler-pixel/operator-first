"""Change-of-variables (automorphism) transfer web.
For rows A, B whose starts have the same Whitehead-minimal form (up to the 8 letter maps, relator swap, cyclic rotation and
inversion), B ~ psi(A) for an automorphism psi of F(x,y). A road P for A becomes a road for B:
  prefix  : conjugations/inversions turning B's relators into exactly psi(A's start) (exact BFS per relator);
  body    : every move of P, with each letter conjugation g replaced by conjugation by the word psi(g) (|psi(g)| moves),
            multiplications and inversions unchanged (relator indices relabelled if psi swaps the relators);
  finish  : exact BFS from (psi(x), psi(y)) to (x, y) over all 14 moves.
Every candidate is replayed on the pinned official core. usage: cov_transfer.py WH.json OUT.txt [maxpairs]   (WH.json from whitehead_min.py)"""
import os, sys, json, collections, itertools
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import symmetry_recog as SR
from whitehead_min import red, cyc, inv, apply, AUTS, total, INV
core = SR.core
C2I = {"x": 1, "X": -1, "y": 2, "Y": -2}
def s(t): return "".join({1: "x", -1: "X", 2: "y", -2: "Y"}[a] for a in t)
def w(st): return tuple(C2I[c] for c in st)
def inv_aut(phi):  # inverse of a single Whitehead automorphism given as (phi, a, img)
    p, a, img = phi; g = [k for k in p if p[k] != k][0]; other = "x" if g == "y" else "y"
    if img == g + a: ii = g + INV[a]
    elif img == INV[a] + g: ii = a + g
    else: ii = a + g + INV[a]
    return {g: ii, other: other}
def descend(t):
    """returns minimal tuple and the list of automorphisms applied (in order)"""
    t = tuple(cyc(x) for x in t); chain = []
    while True:
        best = None
        for au in AUTS:
            u = tuple(cyc(apply(au[0], x)) for x in t)
            if total(u) < total(t) and (best is None or total(u) < total(best[0])): best = (u, au)
        if best is None: return t, chain
        t = best[0]; chain.append(best[1])
def compose(maps):
    """maps applied left to right: w -> m_k(...m_1(w))  as a dict on x, y"""
    cur = {"x": "x", "y": "y"}
    for m in maps:
        cur = {g: apply(m, cur[g]) for g in "xy"}
    return cur
def cyc_eq(a, b):
    a, b = cyc(a), cyc(b)
    if len(a) != len(b): return None
    for cand, flip in ((b, False), (inv(b), True)):
        if a and cand in (a + a): return flip
        if not a and not cand: return flip
    return None
LETMAP = {}
for mp in SR.MAPS:
    LETMAP[tuple(sorted(mp.items()))] = mp
def find_psi(SA, SB):
    """psi with psi(SA) relator-wise cyclically equal (up to inversion) to SB, possibly swapped. returns (psi, swap)"""
    MA, ca = descend(SA); MB, cb = descend(SB)
    for mp in SR.MAPS:
        sig = {"x": mp["x"], "y": mp["y"]}
        img = tuple(cyc(apply(sig, x)) for x in MA)
        for swap in (False, True):
            tgt = (MB[1], MB[0]) if swap else MB
            if cyc_eq(img[0], tgt[0]) is not None and cyc_eq(img[1], tgt[1]) is not None:
                # psi = cb^-1 o sig o ca  (apply ca first)
                maps = [au[0] for au in ca] + [sig] + [inv_aut(au) for au in reversed(cb)]
                return compose(maps), swap
    return None
CONJ = {(0, "x"): 6, (0, "X"): 7, (0, "y"): 8, (0, "Y"): 9, (1, "x"): 10, (1, "X"): 11, (1, "y"): 12, (1, "Y"): 13}
MOVE_CONJ = {6: (0, "x"), 7: (0, "X"), 8: (0, "y"), 9: (0, "Y"), 10: (1, "x"), 11: (1, "X"), 12: (1, "y"), 13: (1, "Y")}
def conj_moves(slot, word):  # r <- word r word^-1, innermost letter first
    return [CONJ[(slot, c)] for c in reversed(word)]
def rel_bfs(src, tgt, slot, cap=14):
    """single-relator exact BFS: conjugations by letters and inversion (moves on one slot) from src word to tgt word"""
    if src == tgt: return []
    moves = [CONJ[(slot, c)] for c in "xXyY"] + [slot]  # inversion id = slot (0 or 1)
    def step(u, m):
        if m in (0, 1): return inv(u)
        g = MOVE_CONJ[m][1]; return red(g + u + INV[g])
    prev = {src: None}; fr = [src]; L = max(len(src), len(tgt)) + 6
    for d in range(cap):
        nf = []
        for u in fr:
            for m in moves:
                v = step(u, m)
                if v in prev or len(v) > L: continue
                prev[v] = (u, m)
                if v == tgt:
                    out = []; x = v
                    while prev[x]: x, mm = prev[x]; out.append(mm)
                    return out[::-1]
                nf.append(v)
        fr = nf
    return None
def finish_bfs(st, cap=9, extra=4):
    """exact BFS over all 14 moves from state st=(a,b) (strings) to ('x','y')"""
    start = (st[0], st[1]); goal = ("x", "y")
    if start == goal: return []
    L = len(st[0]) + len(st[1]) + extra
    prev = {start: None}; fr = [start]
    for d in range(cap):
        nf = []
        for u in fr:
            for m in range(14):
                v = tuple(s(x) for x in core.apply_move((w(u[0]), w(u[1])), m))
                if v in prev or len(v[0]) + len(v[1]) > L: continue
                prev[v] = (u, m)
                if v == goal:
                    out = []; x = v
                    while prev[x]: x, mm = prev[x]; out.append(mm)
                    return out[::-1]
                nf.append(v)
        fr = nf
        if len(fr) > 3_000_000: return None
    return None
def finish_greedy(st, maxsteps=400):
    """greedy length descent over all 14 moves, exact BFS (depth 9) once the total length is <= 10 or stuck"""
    cur = (st[0], st[1]); out = []
    for _ in range(maxsteps):
        if len(cur[0]) + len(cur[1]) <= 10:
            b = finish_bfs(cur)
            if b is not None: return out + b
        best = None
        for m in range(14):
            v = tuple(s(x) for x in core.apply_move((w(cur[0]), w(cur[1])), m))
            L = len(v[0]) + len(v[1])
            if best is None or L < best[0]: best = (L, m, v)
        if best[0] >= len(cur[0]) + len(cur[1]):
            b = finish_bfs(cur, cap=10, extra=6)
            return None if b is None else out + b
        out.append(best[1]); cur = best[2]
    return None
SWID = SR.SW
def transfer(cidA, road, cidB):
    SA = tuple(SR.w2s(r) for r in SR.CH[cidA]["initial_relators"]); SB = tuple(SR.w2s(r) for r in SR.CH[cidB]["initial_relators"])
    got = find_psi(SA, SB)
    if not got: return None, "no psi"
    psi, swap = got
    roadA = [SWID[m] for m in road] if swap else list(road)
    SAf = (SA[1], SA[0]) if swap else SA      # A's start in the (possibly swapped) frame
    tgt = tuple(apply(psi, x) for x in SAf)   # exact words the B road must start from
    pre = []
    for slot in (0, 1):
        p = rel_bfs(SB[slot], tgt[slot], slot)
        if p is None: return None, "prefix bfs failed"
        pre += p
    body = []
    for m in roadA:
        if m in MOVE_CONJ:
            slot, g = MOVE_CONJ[m]; body += conj_moves(slot, apply(psi, g))
        else: body.append(m)
    endA = ("y", "x") if swap else ("x", "y")
    endB = tuple(apply(psi, x) for x in endA)
    fin = finish_greedy(endB)
    if fin is None: return None, "finish failed %s" % (endB,)
    full = pre + body + fin
    ver = core.verify(SR.CH[cidB], full, "ac-r2-v1", SR.LIM)
    return full, ("ok" if ver["ok"] else "verify failed: %s" % ver.get("error", ver)), (len(pre), len(body), len(fin), {g: psi[g] for g in "xy"}, swap)
if __name__ == "__main__":
    wh = json.load(open(sys.argv[1])); outp = sys.argv[2]; maxp = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
    best = {}
    for cid, m in SR.load_roads():
        if cid in wh and (cid not in best or len(m) < len(best[cid])):
            if core.verify(SR.CH[cid], m, "ac-r2-v1", SR.LIM)["ok"]: best[cid] = m
    g = collections.defaultdict(list)
    for cid, v in wh.items(): g[v["key"]].append(cid)
    pairs = []
    for k, rows in g.items():
        if len(rows) < 2: continue
        for A in rows:
            if A not in best: continue
            for B in rows:
                if B == A: continue
                recB = wh[B]["rec"]
                if recB is None or len(best[A]) < recB + 60: pairs.append((len(best[A]) - (recB or 10**4), A, B))
    pairs.sort()
    print("pairs to try", len(pairs), flush=True)
    hits = []
    with open(outp, "w") as f:
        for _, A, B in pairs[:maxp]:
            try:
                r = transfer(A, best[A], B)
            except Exception as e:
                print("ERR", A, B, e, flush=True); continue
            if r[0] is None: print("skip", A, "->", B, r[1], flush=True); continue
            full, status, info = r
            recB, kB = wh[B]["rec"], wh[B]["k"]
            tag = "BEAT" if status == "ok" and recB and len(full) < recB else "TIE" if status == "ok" and recB and len(full) == recB else ""
            print(A, len(best[A]), "->", B, len(full), "rec", recB, "k", kB, status, "pre/body/fin", info[:3], "psi", info[3], "swap", info[4], tag, flush=True)
            if status == "ok":
                f.write("# %s from %s (%d) via psi %s swap %s: %d vs record %s k%s %s\n%s: [%s]\n" % (B, A, len(best[A]), info[3], info[4], len(full), recB, kB, tag, B, ", ".join(map(str, full))))
                f.flush()
