#!/usr/bin/env python3
"""Song 5 ("The universe reorganizes what no longer serves", session 1's idea): drop the prefix that no longer serves.
For each high-value row of mid_restart_lane_v2/jobs.json (1 over a k<=2 record, or 2 over a k1 record), take our best (x,y) road,
pick its 3 LOWEST-total intermediate states, and restart the production beam there with route noise (BEAM_NOISE=2, seeds 1..3,
W 20000, depth = target - cut), keeping the prefix. Any AC tail (<= AC record) or Stable (y,x) tail (<= Stable record) is verified
on the pinned official core and written to research/acc/live/inbox/upgh_song5.txt. Resumes from done.txt.
usage: song5_drop_prefix.py"""
import json, os, re, subprocess, sys, time
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as S
from verifier import core, stable_core
R = "/home/user/operator-first"
D = R + "/research/acc/live/sweeps/song_lane"
B = os.path.expanduser("~/.cache/acc_beam_bin")
E = {1: 0, -1: 1, 2: 2, -2: 3}
jobs = json.load(open(R + "/research/acc/live/sweeps/mid_restart_lane_v2/jobs.json"))
donef = D + "/song5_done.txt"
done = set(open(donef).read().split()) if os.path.exists(donef) else set()
for j in jobs:
    cid, best = j["id"], j["moves"]
    if cid in done:
        continue
    st = [tuple(tuple(x) for x in S.CH[cid]["initial_relators"])]
    for m in best:
        st.append(core.apply_move(st[-1], m))
    T = max(j["rec"] or 0, (j["srec"] or 0) - 2)
    cuts = sorted(range(2, len(best) - 6), key=lambda c: (len(st[c][0]) + len(st[c][1]), c))[:3]
    t0, hits = time.time(), []
    for c in cuts:
        a, b = st[c]
        for seed in (1, 2, 3):
            env = dict(os.environ, BEAM_H="1", BEAM_DIV="0.8", BEAM_P2="2", BEAM_QUOTA="16", BEAM_ELITE="5000", BEAM_DUAL="0.75",
                       BEAM_NOISE="2", BEAM_SEED=str(seed))
            p = subprocess.run([B + "/acc_beam", B + "/T8.tab", "20000", str(T - c), str(len(a)), *[str(E[t]) for t in a],
                                str(len(b)), *[str(E[t]) for t in b]], capture_output=True, text=True, env=env)
            m = re.search(r"^AC (\d+) PATH ([\d ]*)", p.stdout, re.M)
            if m and j["rec"]:
                full = best[:c] + list(map(int, m.group(2).split()))
                if len(full) <= j["rec"] and core.verify(S.CH[cid], full, "ac-r2-v1", S.LIM).get("ok"):
                    hits.append((cid, full))
            m = re.search(r"^SAC (\d+) PATH ([\d ]*)", p.stdout, re.M)
            if m and j["srec"]:
                full = best[:c] + list(map(int, m.group(2).split()))
                sid = "sac-" + cid[3:]
                if len(full) <= j["srec"] and stable_core.verify(S.CH[sid], full, "sac-r8-v1", S.LIM).get("ok"):
                    hits.append((sid, full))
    with open(D + "/song5_log.txt", "a") as f:
        f.write("%s len %d cuts %s AC rec %s ST rec %s: %d hits, %.0fs\n" % (cid, len(best), cuts, j["rec"], j["srec"], len(hits), time.time() - t0))
    if hits:
        with open(R + "/research/acc/live/inbox/upgh_song5.txt", "a") as f:
            for x, full in hits:
                f.write("%s: [%s]\n" % (x, ",".join(map(str, full))))
    with open(donef, "a") as f:
        f.write(cid + "\n")
