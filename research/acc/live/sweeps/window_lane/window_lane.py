#!/usr/bin/env python3
"""Window lane (UPG-H, 6 Oct): exact window-14 shortening (acc_window, end kept fixed) on every distinct road we hold that is
1-2 moves over a record (AC to (x,y); Stable via (x,y)+[16,15] or (y,x)+[15,15]), new team lineages first, highest tie value
first. Saved roads go to inbox/upgh_windowlane_<shard>.txt at once. usage: window_lane.py plan | run SHARD NSHARDS"""
import gzip, glob, json, os, subprocess, sys
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as S
from verifier import core
R = "/home/user/operator-first"; D = R + "/research/acc/live/sweeps/window_lane"
EXE = os.path.expanduser("~/.cache/acc_beam_bin/acc_window_kit")
E = {1: 0, -1: 1, 2: 2, -2: 3}
XY, YX = ((1,), (2,)), ((2,), (1,))
if sys.argv[1] == "plan":
    REC = {it["challengeId"][-5:]: (it["currentBestLength"], it["kTeams"]) for it in json.load(gzip.open(sorted(glob.glob(R + "/research/acc/live/boards/ac_*.json.gz"))[-1]))["data"]["items"]}
    SREC = {it["challengeId"][-5:]: (it["currentBestLength"], it["kTeams"]) for it in json.load(gzip.open(sorted(glob.glob(R + "/research/acc/live/boards/stable_ac_*.json.gz"))[-1]))["data"]["items"]}
    roads = {}
    for cid, mv in S.load_roads():
        if cid not in S.CH: continue
        st = tuple(tuple(r) for r in S.CH[cid]["initial_relators"])
        try:
            for m in mv: st = core.apply_move(st, m)
        except Exception: continue
        end = "xy" if st == XY else "yx" if st == YX else None
        if end: roads.setdefault((cid, end), set()).add(tuple(mv))
    jobs = []
    for (cid, end), ms in roads.items():
        r = cid[-5:]; rec, k = REC.get(r, (None, 0)); srec, sk = SREC.get(r, (None, 0))
        for mv in sorted(ms, key=len)[:3]:                       # up to 3 lineages per row and end
            L = len(mv); best = None
            if end == "xy" and rec and 1 <= L - rec <= 2: best = (L - rec, 2.0 ** -k if k else 1, "AC")
            if srec and 1 <= L + 2 - srec <= 2:
                v = (L + 2 - srec, 2.0 ** -sk if sk else 1, "ST")
                if best is None or (v[0], -v[1]) < (best[0], -best[1]): best = v
            if best: jobs.append({"id": cid, "end": end, "moves": list(mv), "gap": best[0], "value": best[1], "board": best[2]})
    jobs.sort(key=lambda j: (j["gap"], -j["value"], len(j["moves"])))
    json.dump(jobs, open(D + "/jobs.json", "w"))
    print("jobs", len(jobs), "gap1", sum(j["gap"] == 1 for j in jobs), "rows", len({j["id"] for j in jobs}))
    sys.exit()
i, n = int(sys.argv[2]), int(sys.argv[3])
jobs = json.load(open(D + "/jobs.json"))[i::n]
donef = D + "/done_%d.txt" % i
done = set(open(donef).read().split()) if os.path.exists(donef) else set()
work = os.path.expanduser("~/.cache/acc_wl_%d" % i); os.makedirs(work, exist_ok=True)
for j in jobs:
    key = "%s|%s|%d|%s" % (j["id"], j["end"], len(j["moves"]), hash(tuple(j["moves"])) & 0xffffff)
    if key in done: continue
    r0, r1 = S.CH[j["id"]]["initial_relators"]; mv = j["moves"]
    args = [EXE, work, str(len(r0)), *[str(E[t]) for t in r0], str(len(r1)), *[str(E[t]) for t in r1], str(len(mv)), *map(str, mv)]
    p = subprocess.run(args, capture_output=True, text=True, env=dict(os.environ, ACC_ANY_END="1"))
    fin = [l for l in p.stdout.splitlines() if l.startswith("FINALPATH")]
    new = list(map(int, fin[0].split()[1:])) if fin else mv
    st = tuple(tuple(r) for r in S.CH[j["id"]]["initial_relators"])
    for m in new: st = core.apply_move(st, m)
    ok = st == (XY if j["end"] == "xy" else YX)
    with open(D + "/log_%d.txt" % i, "a") as f: f.write("%s %s %s gap%d: %d -> %d %s\n" % (j["id"], j["end"], j["board"], j["gap"], len(mv), len(new), "ok" if ok else "BAD"))
    if ok and len(new) < len(mv):
        with open(R + "/research/acc/live/inbox/upgh_windowlane_%d.txt" % i, "a") as f:
            if j["end"] == "xy": f.write("%s: [%s]\nsac-%s: [%s]\n" % (j["id"], ",".join(map(str, new)), j["id"][3:], ",".join(map(str, new + [16, 15]))))
            else: f.write("sac-%s: [%s]\n" % (j["id"][3:], ",".join(map(str, new + [15, 15]))))
    with open(donef, "a") as f: f.write(key + "\n")
