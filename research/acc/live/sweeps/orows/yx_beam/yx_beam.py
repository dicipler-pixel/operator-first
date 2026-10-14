#!/usr/bin/env python3
"""orows (y,x) beam (2026-10-14; adapted from sweeps/rival3/rival_beam.py, same dual-P2 beam + T8 finish and env).
Default mode "yx": beam the letter-swapped start (x<->y, relator order kept), so a road to (x,y) there is a road to (y,x)
on the real row (moves 6<->8, 7<->9, 10<->12, 11<->13), giving the Stable line road + [15,15]. Every beam output (AC and SAC
lines, any mode) is mapped back and tried as an AC road, a Stable line, and road + [15,15] / [16,15]; only lines the pinned
official core / stable_core accept are kept. Own done/roads/hits files in this directory.
usage: yx_beam.py JOBS.json SHARD NSHARDS     JOBS = [{"cid":..., "W":..., "D":..., "seed":..., "modes":["yx"]}, ...]"""
import gzip, glob, json, os, re, subprocess, sys, time
R = "/home/user/operator-first/"
sys.path.insert(0, R + "tools/acc/upgh")
import twin_lookup as T
import symmetry_recog as SR
from verifier import stable_core
core = T.core
BIN = "/root/.cache/acc_beam_bin"
HERE = os.path.dirname(os.path.abspath(__file__))
REC, SREC = {}, {}
for p, D in (("ac", REC), ("stable_ac", SREC)):
    for it in json.load(gzip.open(sorted(glob.glob(R + "research/acc/live/boards/%s_*.json.gz" % p))[-1]))["data"]["items"]:
        D[it["challengeId"]] = (it["currentBestLength"], it["kTeams"])
FORBID = {"09839", "02257", "09311", "06403", "04718", "05378"}
L = {1: "x", -1: "X", 2: "y", -2: "Y"}
SW = str.maketrans("xXyY", "yYxX")
E = {"x": "0", "X": "1", "y": "2", "Y": "3"}
MODES = {
    "direct": (lambda r0, r1: (r0, r1), {i: i for i in range(14)}),
    "twin": (lambda r0, r1: (r1.translate(SW), r0.translate(SW)), {0: 1, 1: 0, 2: 4, 3: 5, 4: 2, 5: 3, 6: 12, 7: 13, 8: 10, 9: 11, 10: 8, 11: 9, 12: 6, 13: 7}),
    "yx": (lambda r0, r1: (r0.translate(SW), r1.translate(SW)), {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 8, 7: 9, 8: 6, 9: 7, 10: 12, 11: 13, 12: 10, 13: 11}),
}
ENV = dict(os.environ, BEAM_H="1", BEAM_DIV="0.8", BEAM_P2="2", BEAM_QUOTA="16", BEAM_ELITE="5000", BEAM_DUAL="0.75")


def beam(t0, t1, W, D, seed=None):
    env = dict(ENV)
    if seed:
        env.update(BEAM_SEED=str(seed), BEAM_NOISE="2")
    a = [str(len(t0)), *[E[c] for c in t0], str(len(t1)), *[E[c] for c in t1]]
    p = subprocess.run([BIN + "/acc_beam", BIN + "/T8.tab", str(W), str(D), *a], capture_output=True, text=True, env=env)
    out = {}
    for k in ("AC", "SAC"):
        m = re.search(r"^%s \d+ PATH ([\d ]+)" % k, p.stdout, re.M)
        if m:
            out[k] = list(map(int, m.group(1).split()))
    return out


def ok_ac(cid, road):
    return all(0 <= m <= 13 for m in road) and core.verify(T.CH[cid], road, "ac-r2-v1", T.man["limits"])["ok"]


def ok_sac(sac, road):
    return bool(stable_core.verify(SR.CH[sac], road, "sac-r8-v1", SR.LIM).get("ok"))


def run_job(j):
    cid = j["cid"]; sac = "sac-" + cid[3:]
    r0, r1 = ["".join(L[i] for i in r) for r in T.CH[cid]["initial_relators"]]
    bestA, bestS = None, None
    for mode in j.get("modes", ["yx"]):
        tw, back = MODES[mode]
        t0, t1 = tw(r0, r1)
        out = beam(t0, t1, j.get("W", 20000), j.get("D", 200), j.get("seed"))
        for k, path in out.items():
            P = [back[m] if m <= 13 else m for m in path]
            body = [m for m in P if m <= 13]
            if ok_ac(cid, body) and (bestA is None or len(body) < len(bestA)):
                bestA = body
            for c in (P, body + [15, 15], body + [16, 15]):
                if (bestS is None or len(c) < len(bestS)) and ok_sac(sac, c):
                    bestS = c
    if bestA and (bestS is None or len(bestA) + 2 < len(bestS)) and ok_sac(sac, bestA + [16, 15]):
        bestS = bestA + [16, 15]
    return bestA, bestS


def main():
    jobs = json.load(open(sys.argv[1])); sh, ns = int(sys.argv[2]), int(sys.argv[3])
    done_f = os.path.join(HERE, "done.txt")
    done = set(l.split(" :: ")[0] for l in open(done_f)) if os.path.exists(done_f) else set()
    for i, j in enumerate(jobs):
        if i % ns != sh or j["cid"][-5:] in FORBID:
            continue
        key = "%s W%s D%s s%s %s" % (j["cid"], j.get("W", 20000), j.get("D", 200), j.get("seed", 0), "+".join(j.get("modes", ["yx"])))
        if key in done:
            continue
        t = time.time()
        A, S = run_job(j)
        rec, k = REC.get(j["cid"], (None, 0)); srec, sk = SREC.get("sac-" + j["cid"][3:], (None, 0))
        tagA = "-" if not A else ("BEAT" if len(A) < rec else "TIE" if len(A) == rec else "over")
        tagS = "-" if not S else ("BEAT" if len(S) < srec else "TIE" if len(S) == srec else "over")
        line = "%s :: AC %s/%s k%s %s | SAC %s/%s k%s %s | %ds" % (key, len(A) if A else None, rec, k, tagA, len(S) if S else None, srec, sk, tagS, time.time() - t)
        open(done_f, "a").write(line + "\n"); print(line, flush=True)
        with open(os.path.join(HERE, "roads.jsonl"), "a") as f:
            f.write(json.dumps({"cid": j["cid"], "key": key, "ac": A, "sac": S}) + "\n")
        hits = []
        if A and tagA != "over":
            hits.append("# orows yx_beam %s AC %s: %d vs record %s (k%s)\n%s: [%s]\n" % (key, tagA, len(A), rec, k, j["cid"], ", ".join(map(str, A))))
        if S and tagS != "over":
            hits.append("# orows yx_beam %s Stable %s: %d vs record %s (k%s)\nsac-%s: [%s]\n" % (key, tagS, len(S), srec, sk, j["cid"][3:], ", ".join(map(str, S))))
        if hits:
            open(os.path.join(HERE, "hits.txt"), "a").write("".join(hits))
            open(os.path.join(HERE, "..", "HITS.txt"), "a").write("".join(hits)); print("HIT", flush=True)


if __name__ == "__main__":
    main()
