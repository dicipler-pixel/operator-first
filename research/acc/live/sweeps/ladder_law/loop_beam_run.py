#!/usr/bin/env python3
"""Driver for loop_beam (C): canonical MS(n, w*) doubling loop -> pre-finish, + fin2. usage: loop_beam_run.py N W [SLACK]"""
import subprocess, sys, os, time
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import bs_doubling as B
core = B.core
E = {1: 0, -1: 1, 2: 2, -2: 3}
BIN = os.path.expanduser("~/.cache/acc_beam_bin/loop_beam")


def enc(st):
    return [str(len(st[0]))] + [str(E[t]) for t in st[0]] + [str(len(st[1]))] + [str(E[t]) for t in st[1]]


def run(start, goal, W, cap, maxd, slot=0, xg=0, mask=0x3FCF):
    p = subprocess.run([BIN, str(W), str(cap), str(maxd), str(slot), str(xg), hex(mask)] + enc(start) + enc(goal), capture_output=True, text=True)
    for line in p.stdout.splitlines():
        if line.startswith("LOOP"):
            return list(map(int, line.split("PATH")[1].split()))
    return None


if __name__ == "__main__":
    n, W = int(sys.argv[1]), int(sys.argv[2])
    slack = int(sys.argv[3]) if len(sys.argv) > 3 else 2
    m = 2 ** (n - 1)
    start = B.ms(n)
    goal = (tuple([-2] + [1] * m + [2, 2, -1]), (1, 1, -2, -1, 2))
    cap = max(len(goal[0]) + len(goal[1]), len(start[0]) + len(start[1])) + slack
    t0 = time.time()
    loop = run(start, goal, W, cap, 4 * m + 60)
    if not loop:
        print("n=%d W=%d: none (%.0fs)" % (n, W, time.time() - t0)); sys.exit()
    road = loop + B.fin2(m)
    s = start
    for mv in road:
        s = core.apply_move(s, mv)
    print("n=%d W=%d: loop %d road %d = 2^(n+1)+%d ok=%s (%.0fs)" % (n, W, len(loop), len(road), len(road) - 2 ** (n + 1), s == B.T.GOAL, time.time() - t0), flush=True)
    print("loop", loop)
