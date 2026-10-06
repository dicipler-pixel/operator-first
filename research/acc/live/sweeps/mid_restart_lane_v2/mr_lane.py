#!/usr/bin/env python3
"""Mid-restart lane v2 (W 60000; rows 1 over a k<=2 record or 2 over a k1 record, live board).\nMid-restart lane (Moves Manual trick #2, session 2's beat-maker; tools/acc/ops/mid_restart.py extended to Stable):
for each row 1 move over an AC or Stable record (best tie value first), restart the production beam from EVERY state s_i of
our best (x,y) road with depth = target - i; keep any AC tail (to (x,y)) with i + tail <= AC record, and any Stable tail (to
(y,x) + [15,15], the beam's swap finish) with i + tail <= Stable record. Hits are verified and written to the inbox at once.
usage: mr_lane.py plan | run SHARD NSHARDS [W]"""
import glob, gzip, json, os, re, subprocess, sys, time
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as S
from verifier import core, stable_core
R = "/home/user/operator-first"; D = R + "/research/acc/live/sweeps/mid_restart_lane_v2"
B = os.path.expanduser("~/.cache/acc_beam_bin"); E = {1: 0, -1: 1, 2: 2, -2: 3}; XY = ((1,), (2,))
if sys.argv[1] == "plan":
    REC = {it["challengeId"][-5:]: (it["currentBestLength"], it["kTeams"]) for it in json.load(gzip.open(sorted(glob.glob(R + "/research/acc/live/boards/ac_*.json.gz"))[-1]))["data"]["items"]}
    SREC = {it["challengeId"][-5:]: (it["currentBestLength"], it["kTeams"]) for it in json.load(gzip.open(sorted(glob.glob(R + "/research/acc/live/boards/stable_ac_*.json.gz"))[-1]))["data"]["items"]}
    xy, sb = {}, {}
    for cid, mv in S.load_roads():
        if cid not in S.CH or cid[-5:] in S.FORBID: continue
        st = tuple(tuple(r) for r in S.CH[cid]["initial_relators"])
        try:
            for m in mv: st = core.apply_move(st, m)
        except Exception: continue
        r = cid[-5:]
        if st == XY and (r not in xy or len(mv) < len(xy[r])): xy[r] = list(mv)
        if st in (XY, ((2,), (1,))): sb[r] = min(sb.get(r, 9999), len(mv) + 2)
    jobs = []
    for r, mv in xy.items():
        rec, k = REC.get(r, (None, 0)); srec, sk = SREC.get(r, (None, 0))
        ga, gs = (len(mv) - rec) if rec else 99, (sb.get(r, 9999) - srec) if srec else 99
        va = 2.0 ** -k if rec and ((ga == 1 and k <= 2) or (ga == 2 and k == 1)) else 0
        vs = 2.0 ** -sk if srec and ((gs == 1 and sk <= 2) or (gs == 2 and sk == 1)) else 0
        if va or vs: jobs.append({"id": "ac-" + r, "moves": mv, "rec": rec if va else None, "srec": srec if vs else None, "value": va + vs})
    jobs.sort(key=lambda j: (-j["value"], len(j["moves"])))
    json.dump(jobs, open(D + "/jobs.json", "w")); print("rows", len(jobs), "value if all tie", round(sum(j["value"] for j in jobs), 2)); sys.exit()
i, n = int(sys.argv[2]), int(sys.argv[3]); W = sys.argv[4] if len(sys.argv) > 4 else "20000"
env = dict(os.environ, BEAM_H="1", BEAM_DIV="0.8", BEAM_P2="2", BEAM_QUOTA="16", BEAM_ELITE="5000", BEAM_DUAL="0.75")
donef = D + "/done_%d.txt" % i; done = set(open(donef).read().split()) if os.path.exists(donef) else set()
for j in json.load(open(D + "/jobs.json"))[i::n]:
    if j["id"] in done: continue
    cid, best = j["id"], j["moves"]; st = [tuple(tuple(x) for x in S.CH[cid]["initial_relators"])]
    for m in best: st.append(core.apply_move(st[-1], m))
    T = max(j["rec"] or 0, (j["srec"] or 0) - 2); t0 = time.time(); hits = []
    for c in range(1, len(best) - 6):
        dmax = T - c
        if dmax < 1: break
        a, b = st[c]
        p = subprocess.run([B + "/acc_beam", B + "/T8.tab", W, str(dmax), str(len(a)), *[str(E[t]) for t in a], str(len(b)), *[str(E[t]) for t in b]], capture_output=True, text=True, env=env)
        m = re.search(r"^AC (\d+) PATH ([\d ]*)", p.stdout, re.M)
        if m and j["rec"]:
            full = best[:c] + list(map(int, m.group(2).split()))
            if len(full) <= j["rec"] and core.verify(S.CH[cid], full, "ac-r2-v1", S.LIM).get("ok"): hits.append((cid, full))
        m = re.search(r"^SAC (\d+) PATH ([\d ]*)", p.stdout, re.M)
        if m and j["srec"]:
            full = best[:c] + list(map(int, m.group(2).split())); sid = "sac-" + cid[3:]
            if len(full) <= j["srec"] and stable_core.verify(S.CH[sid], full, "sac-r8-v1", S.LIM).get("ok"): hits.append((sid, full))
    with open(D + "/log_%d.txt" % i, "a") as f: f.write("%s len %d AC rec %s ST rec %s: %d hits, %.0fs\n" % (cid, len(best), j["rec"], j["srec"], len(hits), time.time() - t0))
    if hits:
        with open(R + "/research/acc/live/inbox/upgh_midrestart2_%d.txt" % i, "a") as f:
            for x, full in hits: f.write("%s: [%s]\n" % (x, ",".join(map(str, full))))
    with open(donef, "a") as f: f.write(cid + "\n")
