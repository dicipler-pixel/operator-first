#!/usr/bin/env python3
"""Symmetry recognition (Git's untested idea from the 6 Oct handoff, generalised).

Every state on every verified road we hold is a state with a known finish. A row's START that equals such a state up to
  - a signed letter permutation of {x, y} (8 maps), and/or a swap of the two relators (16 frames),
  - cyclic rotation of either relator, inversion of either relator, cyclic reduction (all of which are real AC moves:
    conjugation by a letter l sends r to l r l^-1, moves 0/1 invert),
is solved by: rotate/invert into the frame image of that state, follow the frame-relabelled rest of the donor road,
then fix the frame image of (x,y) back to (x,y). Every candidate is replayed on the pinned official core.

Writes research/acc/live/inbox/upgh_symrecog_<UTC>.txt (AC lines, plus Stable lines = AC + [16,15]) and prints a
summary: first solves (unsolved rows), and lines at or under the live record. No model, no API.
usage: python3 tools/acc/upgh/symmetry_recog.py [--rows unsolved|all] [--radius 0|1]
"""
import argparse, collections, datetime, functools, glob, gzip, json, os, re, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SAIR = Path(os.environ.get("SAIR_REPO") or Path.home() / ".cache/upgh/sair")
sys.path.insert(0, str(SAIR / "competition/tools"))
from verifier import core  # noqa: E402

MAN = json.load(open(SAIR / "competition/tools/verifier/data/manifest.json"))
CH = {c["challenge_id"]: c for c in MAN["challenges"]}
LIM = MAN["limits"]
FORBID = {"09839", "02257", "09311", "06403", "04718", "05378"}
CH_ = {1: "x", -1: "X", 2: "y", -2: "Y"}
INT = {v: k for k, v in CH_.items()}
INVL = {"x": "X", "X": "x", "y": "Y", "Y": "y"}
# 8 signed letter permutations as string maps, with the matching conjugation-letter relabel
MAPS = []
for swapxy in (0, 1):
    for sx in (1, -1):
        for sy in (1, -1):
            fx = (2 if swapxy else 1) * sx
            fy = (1 if swapxy else 2) * sy
            img = {1: fx, -1: -fx, 2: fy, -2: -fy}
            MAPS.append({CH_[k]: CH_[v] for k, v in img.items()})
CONJ = {"x": 0, "X": 1, "y": 2, "Y": 3}
SW = {0: 1, 1: 0, 2: 4, 3: 5, 4: 2, 5: 3, 6: 10, 7: 11, 8: 12, 9: 13, 10: 6, 11: 7, 12: 8, 13: 9}


def w2s(r):
    return "".join(CH_[t] for t in r)


def s2w(s):
    return tuple(INT[c] for c in s)


def inv(s):
    return "".join(INVL[c] for c in reversed(s))


def cred(s):
    """cyclic reduction: (v, c) with s = v c v^-1 and c cyclically reduced"""
    i, j = 0, len(s) - 1
    while i < j and s[i] == INVL[s[j]]:
        i += 1
        j -= 1
    return s[:i], s[i:j + 1]


def cc(s):
    c = cred(s)[1]
    if not c:
        return ""
    best = min(c[i:] + c[:i] for i in range(len(c)))
    ci = inv(c)
    return min(best, min(ci[i:] + ci[:i] for i in range(len(ci))))


@functools.lru_cache(maxsize=4_000_000)
def ccs(word):
    """cyclic class of the word under each of the 8 letter maps (one relator is unchanged by every move, so cache)"""
    return tuple(cc("".join(mp[c] for c in word)) for mp in MAPS)


def frame_state(st, mp, swap):
    a, b = ("".join(mp[c] for c in st[0]), "".join(mp[c] for c in st[1]))
    return (b, a) if swap else (a, b)


def frame_moves(moves, mp, swap):
    out = []
    for m in moves:
        if 6 <= m <= 13:
            base, l = (6 if m < 10 else 10), "xXyY"[(m - 6) % 4]
            m = base + CONJ[mp[l]]
        out.append(SW[m] if swap else m)
    return out


def slot_moves(cur, tgt, slot):
    """AC moves on one relator only (inversion + letter conjugations) turning word cur into word tgt (same cyclic class
    up to inversion). Returns a move list or None."""
    seq = []
    base, invm = (6, 0) if slot == 0 else (10, 1)
    vt, ct = cred(tgt)
    for flip in (False, True):
        w = inv(cur) if flip else cur
        _, c = cred(w)
        if len(c) != len(ct):
            return None
        rot = [k for k in range(len(c)) if c[k:] + c[:k] == ct]
        if not rot:
            continue
        seq = [invm] if flip else []
        # 1) cyclically reduce w: w = a u a^-1 -> conjugate by a^-1
        while True:
            v, c2 = cred(w)
            if not v:
                break
            seq.append(base + CONJ[INVL[w[0]]])
            w = w[1:-1]
        # 2) rotate c to ct: left by k (conj by inverse of first letter) or right (conj by last letter)
        k = rot[0]
        n = len(w)
        if k <= n - k:
            for _ in range(k):
                seq.append(base + CONJ[INVL[w[0]]])
                w = w[1:] + w[0]
        else:
            for _ in range(n - k):
                seq.append(base + CONJ[w[-1]])
                w = w[-1] + w[:-1]
        # 3) un-reduce to tgt = vt ct vt^-1: conjugate by vt letters, innermost first
        for l in reversed(vt):
            seq.append(base + CONJ[l])
            w = l + w + INVL[l]
        return seq if w == tgt else None
    return None


def load_roads():
    pat = re.compile(r"\b(s?ac-\d{5})\s*:\s*\[([0-9,\s]+)\]")
    files = glob.glob(str(REPO / "research/acc/live/**/*.txt"), recursive=True)
    files += glob.glob(str(REPO / "research/acc/live/handoffs/attachments/*.txt"))
    seen = set()
    for f in files:
        try:
            txt = open(f, errors="replace").read()
        except OSError:
            continue
        for cid, mv in pat.findall(txt):
            m = tuple(int(x) for x in mv.split(",") if x.strip())
            key = (cid[-5:], m)
            if key not in seen:
                seen.add(key)
                yield "ac-" + cid[-5:], [x for x in m if x <= 13] if cid.startswith("sac") else list(m)
    led = REPO / "research/acc/upgh/ledger.jsonl"
    if led.exists():
        for line in open(led):
            try:
                d = json.loads(line).get("data") or {}
            except ValueError:
                continue
            c, m = d.get("cid"), d.get("moves")
            if c and isinstance(m, list) and m and (c[-5:], tuple(m)) not in seen:
                seen.add((c[-5:], tuple(m)))
                yield "ac-" + c[-5:], [x for x in m if x <= 13] if c.startswith("sac") else m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rows", default="all", choices=["all", "unsolved"])
    ap.add_argument("--radius", type=int, default=0, help="also match states 1 move from each start")
    a = ap.parse_args()
    t0 = datetime.datetime.now(datetime.timezone.utc)
    boards = sorted(glob.glob(str(REPO / "research/acc/live/boards/ac_*.json.gz")))[-1]
    sboards = sorted(glob.glob(str(REPO / "research/acc/live/boards/stable_ac_*.json.gz")))[-1]
    REC = {it["challengeId"][-5:]: (it["currentBestLength"], it["kTeams"]) for it in json.load(gzip.open(boards))["data"]["items"]}
    SREC = {it["challengeId"][-5:]: (it["currentBestLength"], it["kTeams"]) for it in json.load(gzip.open(sboards))["data"]["items"]}
    # our best per row (AC), from every road source
    best = {}
    # starts to recognise, keyed by their cyclic-class pair (as a sorted pair: the frame search below fixes the order)
    rows = [cid for cid in CH if cid.startswith("ac-") and cid[-5:] not in FORBID and (a.rows == "all" or REC.get(cid[-5:], (None,))[0] is None)]
    need = collections.defaultdict(list)          # canonical key -> [(cid, start_state_strings, pre_moves)]
    lens = set()

    def canon(st):
        A, B = ccs(st[0]), ccs(st[1])
        return min(min((p, q), (q, p)) for p, q in zip(A, B))

    for cid in rows:
        s0 = tuple(w2s(r) for r in CH[cid]["initial_relators"])
        cands = [(s0, [])]
        if a.radius >= 1:
            st = tuple(tuple(r) for r in CH[cid]["initial_relators"])
            for m in range(14):
                n = core.apply_move(st, m)
                cands.append((tuple(w2s(r) for r in n), [m]))
        for s, pre in cands:
            k = canon(s)
            need[k].append((cid, s, pre))
            lens.add(tuple(sorted((len(k[0]), len(k[1])))))
    print("rows %d, start keys %d" % (len(rows), len(need)), flush=True)
    # index road states with a matching cyclic-length profile
    hits = collections.defaultdict(list)
    nroads = nstates = 0
    for cid, moves in load_roads():
        if cid not in CH:
            continue
        st = tuple(tuple(r) for r in CH[cid]["initial_relators"])
        chain = [st]
        ok = True
        for m in moves:
            try:
                st = core.apply_move(st, m)
            except Exception:
                ok = False
                break
            chain.append(st)
        if not ok or not (chain[-1] in (((1,), (2,)), ((2,), (1,)))):
            continue
        nroads += 1
        L = len(moves)
        best[cid] = min(best.get(cid, 10 ** 9), L) if chain[-1] == ((1,), (2,)) else best.get(cid, 10 ** 9)
        for i, s in enumerate(chain[:-1]):
            ws = (w2s(s[0]), w2s(s[1]))
            lp = tuple(sorted((len(cred(ws[0])[1]), len(cred(ws[1])[1]))))
            if lp not in lens:
                continue
            nstates += 1
            k = canon(ws)
            if k in need:
                hits[k].append((cid, ws, moves[i:], chain[-1]))
    print("roads replayed %d, candidate states %d, matched keys %d" % (nroads, nstates, len(hits)), flush=True)
    # fix-ups from every frame image of (x,y) / (y,x) back to (x,y)
    goal = ((1,), (2,))
    fix = {goal: []}
    frontier = [goal]
    for _ in range(8):
        nxt = []
        for s in frontier:
            for m in range(14):
                n = core.apply_move(s, m)
                if n not in fix and sum(map(len, n)) <= 4:
                    fix[n] = fix[s] + [m]
                    nxt.append(n)
        frontier = nxt
    inv_fix = {}
    for s, path in fix.items():          # path goes goal -> s; we need s -> goal: reverse with inverse moves
        INVM = {0: 0, 1: 1, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6, 8: 9, 9: 8, 10: 11, 11: 10, 12: 13, 13: 12}
        inv_fix[s] = [INVM[m] for m in reversed(path)]
    found = {}
    for k, donors in hits.items():
        for cid, s, pre in need[k]:
            for dcid, dws, rest, dend in donors:
                if dcid == cid and not pre:
                    continue
                for mp in MAPS:
                    for swap in (False, True):
                        t = frame_state(dws, mp, swap)
                        if cc(t[0]) != cc(s[0]) or cc(t[1]) != cc(s[1]):
                            continue
                        m0 = slot_moves(s[0], t[0], 0)
                        m1 = slot_moves(s[1], t[1], 1)
                        if m0 is None or m1 is None:
                            continue
                        tail = frame_moves(rest, mp, swap)
                        end = tuple(s2w(x) for x in frame_state((w2s(dend[0]), w2s(dend[1])), mp, swap))
                        if end not in inv_fix:
                            continue
                        road = list(pre) + m0 + m1 + tail + inv_fix[end]
                        if cid not in found or len(road) < len(found[cid][0]):
                            if core.verify(CH[cid], road, "ac-r2-v1", LIM).get("ok"):
                                found[cid] = (road, dcid)
    stamp = t0.strftime("%Y%m%dT%H%M%SZ") + ("_r%d_%s" % (a.radius, a.rows))
    out = REPO / ("research/acc/live/inbox/upgh_symrecog_%s.txt" % stamp)
    lines, report = [], []
    for cid, (road, dcid) in sorted(found.items()):
        r = cid[-5:]
        rec, k = REC.get(r, (None, 0))
        srec, sk = SREC.get(r, (None, 0))
        tag = "FIRST SOLVE" if rec is None else ("BEAT" if len(road) < rec else ("TIE" if len(road) == rec else "+%d" % (len(road) - rec)))
        ours = best.get(cid)
        report.append("%s %d via %s | AC record %s (k%s) %s | ours %s" % (cid, len(road), dcid, rec, k, tag, ours if ours != 10 ** 9 else None))
        lines.append("%s: [%s]\n" % (cid, ",".join(map(str, road))))
        lines.append("sac-%s: [%s]\n" % (r, ",".join(map(str, road + [16, 15]))))
    out.write_text("# symmetry recognition %s: %d rows (AC + Stable = AC + [16,15]); official core ok\n" % (stamp, len(found)) + "".join(lines))
    print("\n".join(report))
    print("wrote %s (%d rows)" % (out.relative_to(REPO), len(found)))


if __name__ == "__main__":
    main()
