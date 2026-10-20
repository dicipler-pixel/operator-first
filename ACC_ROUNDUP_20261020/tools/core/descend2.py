#!/usr/bin/env python3
"""Iterated mid-road restarts, v2. Row spec CID:AC_TARGET:MODE[:CUTHI[:LINK]]
MODE xy = beam aims at (x,y) (AC tails, plus the beam's own SAC tails); yx = beam on the letter-swapped state, so the
search aims at (y,x): Stable line = prefix + mapped tail + [15,15]. CUTHI limits restart points (shared tails run once).
LINK=OTHER:K means: our state K equals OTHER's state 1, so every OTHER improvement is transferred as best[:K] + other[1:].
A pass adopts the shortest strict gain; a pass without gain escalates the setting (ladder) instead of repeating."""
import sys, os, json, re, subprocess, time
from multiprocessing import Pool
sys.path.insert(0, "/home/user/operator-first/tools/acc/upgh")
import symmetry_recog as SR
from verifier import core, stable_core
OUT = sys.argv[1]
BIN = os.path.expanduser("~/.cache/acc_beam_bin"); E = {1: 0, -1: 1, 2: 2, -2: 3}
SWAPL = {1: 2, -1: -2, 2: 1, -2: -1}
BACK_YX = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 8, 7: 9, 8: 6, 9: 7, 10: 12, 11: 13, 12: 10, 13: 11}
BASE = dict(os.environ, BEAM_H="1", BEAM_DIV="0.8", BEAM_P2="2", BEAM_QUOTA="16", BEAM_ELITE="5000", BEAM_DUAL="0.75")
LADDERS = {"xy": [(20000, None), (5000, 7), (5000, 13), (20000, 31), (60000, None)],
           "yx": [(5000, None), (20000, None), (5000, 7), (20000, 31)]}
def log(msg):
    line = time.strftime("%H:%M:%SZ ", time.gmtime()) + msg
    print(line, flush=True); open(OUT + "/log.txt", "a").write(line + "\n")
def states(cid, p):
    st = [tuple(tuple(x) for x in SR.CH[cid]["initial_relators"])]
    for m in p: st.append(core.apply_move(st[-1], m))
    return st
def okA(cid, p): return core.verify(SR.CH[cid], p, "ac-r2-v1", SR.LIM)["ok"]
def okS(cid, p): return bool(stable_core.verify(SR.CH["s" + cid], p, "sac-r8-v1", SR.LIM).get("ok"))
def beam(args):
    cid, c, mode, a, b, W, seed, d = args
    if mode == "yx": a, b = tuple(SWAPL[t] for t in a), tuple(SWAPL[t] for t in b)
    env = dict(BASE)
    if seed: env.update(BEAM_SEED=str(seed), BEAM_NOISE="2")
    p = subprocess.run([BIN + "/acc_beam", BIN + "/T8.tab", str(W), str(d), str(len(a)), *[str(E[t]) for t in a], str(len(b)), *[str(E[t]) for t in b]], capture_output=True, text=True, env=env)
    out = {}
    for k in ("AC", "SAC"):
        m = re.search(r"^%s \d+ PATH ([\d ]+)" % k, p.stdout, re.M)
        if m: out[k] = list(map(int, m.group(1).split()))
    return cid, c, mode, out
def main():
    rows = {}
    for spec in sys.argv[2:]:
        f = spec.split(":"); cid = f[0]
        best = json.load(open(OUT + "/%s.road" % cid))
        if os.path.exists(OUT + "/%s.best.json" % cid):
            prev = json.load(open(OUT + "/%s.best.json" % cid))
            if len(prev["ac"]) < len(best) and okA(cid, prev["ac"]): best = prev["ac"]
        rows[cid] = dict(target=int(f[1]), mode=f[2], cuthi=int(f[3]) if len(f) > 3 and f[3] else None,
                         link=(f[4], int(f[5])) if len(f) > 5 else None, best=best, sbest=best + [16, 15], step=0)
        log("v2 %s start AC %d (target %d) Stable %d mode %s cuts<=%s link %s" % (cid, len(best), rows[cid]["target"], len(best) + 2, f[2], rows[cid]["cuthi"], rows[cid]["link"]))
    pool = Pool(4)
    while True:
        live = [c for c, r in rows.items() if r["step"] < len(LADDERS[r["mode"]]) and len(r["sbest" if r["mode"] == "yx" else "best"]) > r["target"]]
        if not live: break
        jobs = []
        for cid in live:
            r = rows[cid]; W, seed = LADDERS[r["mode"]][r["step"]]; st = states(cid, r["best"]); L = len(r["best"])
            hi = min(L - 6, r["cuthi"] + 1) if r["cuthi"] else L - 6
            jobs += [(cid, c, r["mode"], st[c][0], st[c][1], W, seed, (len(r["sbest"]) - 3 - c) if r["mode"] == "yx" else (L - 1 - c)) for c in range(1, hi)]
        jobs.sort(key=lambda j: -j[7]); t0 = time.time()
        found = {c: None for c in live}; sfound = {c: None for c in live}
        for cid, c, mode, out in pool.imap_unordered(beam, jobs):
            r = rows[cid]
            if mode == "xy":
                if "AC" in out:
                    full = r["best"][:c] + out["AC"]
                    if len(full) < len(r["best"]) and (found[cid] is None or len(full) < len(found[cid])) and okA(cid, full):
                        found[cid] = full; log("%s cut %d: AC %d" % (cid, c, len(full)))
                if "SAC" in out:
                    full = r["best"][:c] + out["SAC"]
                    if len(full) < len(r["sbest"]) and (sfound[cid] is None or len(full) < len(sfound[cid])) and okS(cid, full):
                        sfound[cid] = full; log("%s cut %d: Stable %d" % (cid, c, len(full)))
            elif "AC" in out:  # yx: tail reaches (y,x) in the original letters
                full = r["best"][:c] + [BACK_YX[m] for m in out["AC"]] + [15, 15]
                if len(full) < len(r["sbest"]) and (sfound[cid] is None or len(full) < len(sfound[cid])) and okS(cid, full):
                    sfound[cid] = full; log("%s cut %d (yx): Stable %d" % (cid, c, len(full)))
        for cid in live:
            r = rows[cid]; W, seed = LADDERS[r["mode"]][r["step"]]
            if sfound[cid]: r["sbest"] = sfound[cid]
            if found[cid]:
                r["best"] = found[cid]
                if len(r["best"]) + 2 < len(r["sbest"]): r["sbest"] = r["best"] + [16, 15]
                log("%s pass W%d seed %s: AC now %d, Stable %d (%.0fs)" % (cid, W, seed, len(r["best"]), len(r["sbest"]), time.time() - t0))
            else:
                r["step"] += 1
                lad = LADDERS[r["mode"]]
                log("%s pass W%d seed %s: no AC gain, Stable %d (%.0fs) -> %s" % (cid, W, seed, len(r["sbest"]), time.time() - t0, "next %s" % (lad[r["step"]],) if r["step"] < len(lad) else "ladder done"))
            for oc, orow in rows.items():  # transfer through links
                if orow["link"] and orow["link"][0] == cid:
                    K = orow["link"][1]; cand = orow["best"][:K] + r["best"][1:]
                    if len(cand) < len(orow["best"]) and okA(oc, cand):
                        orow["best"] = cand; orow["sbest"] = min(orow["sbest"], cand + [16, 15], key=len); log("%s via link to %s: AC %d" % (oc, cid, len(cand)))
            json.dump({"ac": r["best"], "stable": r["sbest"]}, open(OUT + "/%s.best.json" % cid, "w"))
        for oc, orow in rows.items(): json.dump({"ac": orow["best"], "stable": orow["sbest"]}, open(OUT + "/%s.best.json" % oc, "w"))
    log("v2 finished: " + ", ".join("%s AC %d / Stable %d" % (c, len(r["best"]), len(r["sbest"])) for c, r in rows.items()))
main()
