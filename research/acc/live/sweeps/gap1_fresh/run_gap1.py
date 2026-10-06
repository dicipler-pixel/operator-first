#!/usr/bin/env python3
"""Fresh gap-1 lane (UPG-H, 6 Oct): exact window-14 shortening (acc_window, end state kept fixed) on our best (x,y) and
(y,x) roads for single-holder rows nobody has worked. Writes verified shorter roads to inbox/upgh_gap1_window_<UTC>.txt."""
import datetime, json, os, subprocess, sys
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as S
from verifier import core
ROWS = sys.argv[1].split(",")
EXE = "/tmp/acc_work/acc_window_kit"
E = {1: 0, -1: 1, 2: 2, -2: 3}
best = {}
for cid, moves in S.load_roads():
    if cid[-5:] not in ROWS or cid not in S.CH: continue
    st = tuple(tuple(r) for r in S.CH[cid]["initial_relators"])
    try:
        for m in moves: st = core.apply_move(st, m)
    except Exception: continue
    end = {((1,), (2,)): "xy", ((2,), (1,)): "yx"}.get(st)
    if end and ((cid, end) not in best or len(moves) < len(best[(cid, end)])): best[(cid, end)] = list(moves)
out = "/home/user/operator-first/research/acc/live/inbox/upgh_gap1_window_%s.txt" % datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
log = open("/home/user/operator-first/research/acc/live/sweeps/gap1_fresh/log.txt", "a")
for (cid, end), mv in sorted(best.items()):
    r0, r1 = S.CH[cid]["initial_relators"]
    args = [EXE, "/tmp/acc_gap1", str(len(r0)), *[str(E[t]) for t in r0], str(len(r1)), *[str(E[t]) for t in r1], str(len(mv)), *map(str, mv)]
    os.makedirs("/tmp/acc_gap1", exist_ok=True)
    p = subprocess.run(args, capture_output=True, text=True, env=dict(os.environ, ACC_ANY_END="1"))
    fin = [l for l in p.stdout.splitlines() if l.startswith("FINALPATH")]
    new = list(map(int, fin[0].split()[1:])) if fin else mv
    st = tuple(tuple(r) for r in S.CH[cid]["initial_relators"])
    for m in new: st = core.apply_move(st, m)
    ok = st == ({"xy": ((1,), (2,)), "yx": ((2,), (1,))}[end])
    msg = "%s %s: %d -> %d (%s)%s" % (cid, end, len(mv), len(new), "ok" if ok else "BAD", "" if fin else " no FINALPATH: " + (p.stdout + p.stderr)[-200:])
    print(msg, flush=True); log.write(datetime.datetime.now(datetime.timezone.utc).strftime("[%H:%MZ] ") + msg + "\n"); log.flush()
    if ok and len(new) < len(mv):
        with open(out, "a") as f:
            fin_moves = [16, 15] if end == "xy" else [15, 15]
            if end == "xy": f.write("%s: [%s]\n" % (cid, ",".join(map(str, new))))
            f.write("sac-%s: [%s]\n" % (cid[-5:], ",".join(map(str, new + fin_moves))))
