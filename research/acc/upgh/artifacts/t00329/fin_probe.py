#!/usr/bin/env python3
"""t00329: probe for a finish entry other than (Y x^m y y X, x x Y X y) + fin2(m) at the end of the BS-doubling loop.

Reuses the alternating-orientation loop of artifacts/t00312/bs_alt.py (read only; imported). For each n it builds the exact
state at the end of level n-2 (one level early, the fin2 entry level) and at the end of level n-3 (two levels early), in
both orientations, and runs the repository beam search acc_beam (forward beam + exact T9 ball finish) from that state with
the depth cap set to the current finish cost (bridge + fin2). A hit is a finish strictly shorter than the current one; every
hit is replayed on the pinned official core, spliced into the canonical road, transferred to each board row by symmetry and
replayed from the official row start before it is written.

usage: python3 fin_probe.py --n 4 5 --width 200000 [--out lines.txt] [--json roads.jsonl] [--log beam.log]
"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path("/home/user/operator-first")
ART = REPO / "research/acc/upgh/artifacts/t00329"
sys.path.insert(0, str(REPO / "tools/acc/upgh"))
sys.path.insert(0, str(REPO / "research/acc/upgh/artifacts/t00312"))
import twin_lookup as T  # noqa: E402
import bs_alt as B  # noqa: E402

core = T.core
X, x, Y, y = -1, 1, -2, 2
ENC = {1: 0, -1: 1, 2: 2, -2: 3}
BEAM = Path.home() / ".cache/upgh/bin/acc_beam"
T9 = Path.home() / ".cache/upgh/T9.tab"


def apply(s, moves):
    for mv in moves:
        s = core.apply_move(s, mv)
    return s


def loop_levels(n, orient, levels):
    """Alternating loop from loop_entry(n, orient) for `levels` levels (levels = n-1 is the full loop of bs_alt)."""
    s = B.loop_entry(n, orient)
    path = []
    a, b, c = 1, n + 1, n
    for L in range(levels):
        if orient == 1:
            assert s[0] == tuple([x] * (a - 1) + [y] * b + [X] + [Y] * c + [x]) and s[1] == B.RHO
            for i in range(a):
                s = core.apply_move(s, 2); path.append(2)
                if i < a - 1:
                    s = core.apply_move(s, 7); path.append(7)
            if L < levels - 1:
                for mv in (0, 9, 6, 10):
                    s = core.apply_move(s, mv); path.append(mv)
                orient = 2
        else:
            assert s[0] == tuple([X] * (a - 1) + [y] * c + [x] + [Y] * b + [X]) and s[1] == B.RHO2
            for i in range(a):
                s = core.apply_move(s, 3); path.append(3)
                if i < a - 1:
                    s = core.apply_move(s, 6); path.append(6)
            if L < levels - 1:
                for mv in (0, 9, 7, 11):
                    s = core.apply_move(s, mv); path.append(mv)
                orient = 1
        a, b, c = 2 * a, b - 1, c - 1
    return path, s


def state_args(s):
    out = []
    for w in s:
        out.append(str(len(w)))
        out += [str(ENC[t]) for t in w]
    return out


def run_beam(s, width, dmax, log, env=None):
    cmd = [str(BEAM), str(T9), str(width), str(dmax)] + state_args(s)
    e = dict(os.environ)
    if env:
        e.update(env)
    t0 = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True, env=e)
    dt = time.time() - t0
    log.write("CMD %s\nENV %s\n%s\n%s\n(%.1fs)\n\n" % (" ".join(cmd[:4]) + " <state>", env, r.stderr[-3000:], r.stdout, dt))
    log.flush()
    path = None
    for line in r.stdout.splitlines():
        if line.startswith("AC ") and "PATH" in line:
            parts = line.split()
            path = [int(t) for t in parts[parts.index("PATH") + 1:]]
    return path, dt


def transfer(cid, n, canon_path):
    """Board row cid (an MS(n) twin): map row start to canonical letters by each symmetry, prefix by rotation/inversion
    moves, run canon_path, finish from g(goal) by BFS, replay on the official core. Returns the shortest verified road."""
    P = B.ms(n)
    best = None
    for h in T.SYMS:
        S = T.apply_g(h, T.REL[cid])
        if tuple(T.ccanon(w) for w in S) != tuple(T.ccanon(w) for w in P):
            continue
        for g in T.SYMS:
            if T.apply_g(g, S) != T.REL[cid]:
                continue
            pre = B.mitm(S, P, depth=4, slack=4)
            if pre is None:
                pre = B.bridge(S, P, limit=20)
            if pre is None:
                continue
            route = pre + canon_path
            body = [T.mmap(g, mv) for mv in route]
            e = apply(T.REL[cid], body)
            fin = T.finish(e)
            if fin is None:
                continue
            p = B.reopt_suffix(T.REL[cid], body + fin)
            if core.verify(T.CH[cid], p, "ac-r2-v1", T.man["limits"])["ok"] and (best is None or len(p) < len(best)):
                best = p
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, nargs="+", default=[4, 5])
    ap.add_argument("--width", type=int, default=200000)
    ap.add_argument("--early", type=int, nargs="+", default=[1, 2], help="levels early: 1 = fin2 entry level, 2 = one more")
    ap.add_argument("--slack", type=int, default=0, help="DMAX = current finish cost - 1 + slack")
    ap.add_argument("--env", default="", help="extra BEAM_* env, e.g. BEAM_H=1,BEAM_DIV=0.5")
    ap.add_argument("--out", default=str(ART / "lines.txt"))
    ap.add_argument("--json", default=str(ART / "roads.jsonl"))
    ap.add_argument("--log", default=str(ART / "beam.log"))
    ap.add_argument("--contract", default=str(REPO / "research/acc/upgh/tasks/t00329.json"))
    a = ap.parse_args()
    env = dict(kv.split("=") for kv in a.env.split(",") if kv)
    ctx = json.load(open(a.contract))["context"]
    idx = {}
    for cid, p in T.REL.items():
        idx.setdefault(T.key(p), []).append(cid)
    log = open(a.log, "a")
    lines, recs = [], []
    summary = []
    for n in a.n:
        m = 2 ** (n - 1)
        for early in a.early:
            for orient in (1, 2):
                levels = n - early
                body, s = loop_levels(n, orient, levels)
                pre = B.bridge(B.ms(n), B.loop_entry(n, orient))
                # current finish from this state: continue the loop to level n-1 (if early 2), bridge, fin2
                rest, s_end = loop_levels(n, orient, n - 1)
                rest = rest[len(body):]
                br = B.bridge(s_end, B.FIN_ENTRY(m))
                cur_fin = rest + br + B.fin2(m)
                assert apply(s, cur_fin) == T.GOAL
                cur_total = len(pre) + len(body) + len(cur_fin)
                dmax = len(cur_fin) - 1 + a.slack
                path, dt = run_beam(s, a.width, dmax, log, env)
                found = None
                if path is not None and apply(s, path) == T.GOAL and len(path) < len(cur_fin):
                    found = path
                rec = {"n": n, "early": early, "orient": orient, "state": [B.W(s[0]), B.W(s[1])], "cur_finish": len(cur_fin),
                       "beam_finish": len(path) if path else None, "beam_s": round(dt, 1), "width": a.width, "dmax": dmax,
                       "env": env, "improved": found is not None}
                summary.append(rec)
                print(json.dumps(rec), flush=True)
                if found is None:
                    continue
                canon = pre + body + found
                assert apply(B.ms(n), canon) == T.GOAL
                print("  canonical road n=%d: %d (was %d)" % (n, len(canon), cur_total), flush=True)
                for cid in idx.get(T.key(B.ms(n)), []):
                    p = transfer(cid, n, canon)
                    ours = ctx.get(cid, {}).get("our_best")
                    print("   %s %s (our_best %s, record %s)" % (cid, len(p) if p else "no transfer", ours, ctx.get(cid, {}).get("record")), flush=True)
                    if p and cid in ctx and len(p) < ours:
                        lines.append("%s: [%s]" % (cid, ", ".join(map(str, p))))
                        lines.append("s%s: [%s]" % (cid, ", ".join(map(str, p + [16, 15]))))
                        recs.append({"id": cid, "n": n, "len": len(p), "ac": p, "sac": p + [16, 15], "our_best": ours})
    (ART / "beam_summary.jsonl").open("a").write("".join(json.dumps(r) + "\n" for r in summary))
    if lines:
        with open(a.out, "a") as f:
            f.write("\n".join(lines) + "\n")
        with open(a.json, "a") as f:
            f.write("".join(json.dumps(r) + "\n" for r in recs))
        print("wrote", a.out, a.json)
    else:
        print("no road shorter than the current row roads; nothing written to lines.txt")


if __name__ == "__main__":
    main()
