#!/usr/bin/env python3
"""Driver for join_bidi (C): per-row join of the row start onto the canonical macro trajectory, then the per-row road.
usage: join_run.py N CID [KMAX] [SLACK] [VARIANTS]"""
import os, subprocess, sys, tempfile, shutil, time
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
sys.path.insert(0, "/home/user/operator-first/research/acc/live/sweeps/ladder_law")
import bs_doubling as B
from ladder_rows import GINV, loops, frame_fin
T = B.T
core = B.core
E = {1: 0, -1: 1, 2: 2, -2: 3}
BIN = os.path.expanduser("~/.cache/acc_beam_bin/join_bidi")
SCR = "/tmp/claude-0/-home-user-operator-first/644f7765-aca6-5d39-980a-3e4ddc6288c0/scratchpad/dbl"


def enc(st):
    return [str(len(st[0]))] + [str(E[t]) for t in st[0]] + [str(len(st[1]))] + [str(E[t]) for t in st[1]]


def join(S0, loop, kset, slack):
    traj = [B.ms(len(loop) and 0 or 0)]  # placeholder, replaced below
    return None


def per_row(n, cid, kmax=40, slack=2, nvar=3):
    m = 2 ** (n - 1)
    P = B.ms(n)
    out = None
    for g in T.SYMS:
        if tuple(T.ccanon(x) for x in T.apply_g(g, P)) != tuple(T.ccanon(x) for x in T.REL[cid]):
            continue
        S0 = T.apply_g(GINV[g], T.REL[cid])
        for loop in loops(n)[:nvar]:
            traj = [P]
            for mv in loop:
                traj.append(core.apply_move(traj[-1], mv))
            ks = list(range(0, min(kmax, len(loop)) + 1))
            kk = max(ks)
            cap = max(max(len(traj[k][0]) + len(traj[k][1]) for k in ks), len(S0[0]) + len(S0[1])) + slack
            wd = tempfile.mkdtemp(dir=SCR)
            tf = os.path.join(wd, "traj.txt")
            with open(tf, "w") as f:
                for k in ks:
                    f.write("%d %d %s\n" % (k, kk - k, " ".join(enc(traj[k]))))
            t0 = time.time()
            p = subprocess.run([BIN, wd, str(cap), "120", hex(0x3FCF), tf] + enc(S0), capture_output=True, text=True, env=dict(os.environ, BUDGET=os.environ.get("BUDGET", "120000000")))
            shutil.rmtree(wd, ignore_errors=True)
            line = [l for l in p.stdout.splitlines() if l.startswith("JOIN")]
            if not line:
                print("   %s loop%d: no join (%s) %.0fs" % (cid, len(loop), p.stdout.strip()[:80] or p.stderr[-200:], time.time() - t0), flush=True)
                continue
            parts = line[0].split()
            k = int(parts[2])
            pre = list(map(int, line[0].split("PATH")[1].split()))
            s = S0
            for mv in pre:
                s = core.apply_move(s, mv)
            assert s == traj[k], "join mismatch"
            canon = pre + loop[k:]
            road = [T.mmap(g, mv) for mv in canon]
            ff = frame_fin(g, m)
            if ff is None:
                tail = [T.mmap(g, mv) for mv in B.fin2(m)]
                e = T.REL[cid]
                for mv in road + tail:
                    e = core.apply_move(e, mv)
                road = road + tail + (T.finish(e) or [])
            else:
                road = road + ff
            ok = core.verify(T.CH[cid], road, "ac-r2-v1", T.man["limits"])["ok"]
            print("   %s g=%s loop%d: prefix %d joins k=%d -> AC %d ok=%s (%.0fs)" % (cid, g, len(loop), len(pre), k, len(road), ok, time.time() - t0), flush=True)
            if ok and (out is None or len(road) < len(out)):
                out = road
    return out


if __name__ == "__main__":
    n, cid = int(sys.argv[1]), sys.argv[2]
    kmax = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    slack = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    nvar = int(sys.argv[5]) if len(sys.argv) > 5 else 3
    road = per_row(n, cid, kmax, slack, nvar)
    if road:
        print("ROAD %s %d %s" % (cid, len(road), ",".join(map(str, road))), flush=True)
