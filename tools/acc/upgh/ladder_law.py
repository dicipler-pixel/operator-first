#!/usr/bin/env python3
"""Ladder law (VOTKP "column rhythm" test on Miller-Schupp ladders).
Every scored row with a relator X y^n x Y^(n+1) (up to the 8 letter maps, rotation, inversion) is put on a ladder keyed by
its OTHER relator (same map). Along a ladder, rung n -> board AC / Stable record.
Registered test (fixed before reading the result): predict each rung from the two rungs below it by the affine law
rec(n) = 2 rec(n-1) - rec(n-2) (consecutive n only). Kill: exact-hit rate < 50 % on rungs where all three records exist.
Outputs (research/acc/live/sweeps/ladder_law/):
  ladders.json   every ladder: rungs, records, k, our best
  slack.tsv      rungs whose board record exceeds the law  -> a road at the law length would BEAT (1 point)
  predict.tsv    unsolved rungs with a law prediction      -> first-solve target lengths
usage: python3 tools/acc/upgh/ladder_law.py
"""
import collections, glob, gzip, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import symmetry_recog as S  # noqa: E402

R = S.REPO
OUT = R / "research/acc/live/sweeps/ladder_law"


def board(prefix):
    f = sorted(glob.glob(str(R / ("research/acc/live/boards/%s_*.json.gz" % prefix))))[-1]
    return {it["challengeId"][-5:]: (it["currentBestLength"], it["kTeams"]) for it in json.load(gzip.open(f))["data"]["items"]}, Path(f).name


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    REC, fa = board("ac")
    SREC, fs = board("stable_ac")
    STD = {S.cc("X" + "y" * n + "x" + "Y" * (n + 1)): n for n in range(1, 16)}
    ours = {}
    for cid, mv in S.load_roads():
        if cid.startswith("ac-"):
            r = cid[-5:]
            ours[r] = min(ours.get(r, 9999), len(mv))
    lad = collections.defaultdict(lambda: collections.defaultdict(set))
    for cid, c in S.CH.items():
        if not cid.startswith("ac-") or cid[-5:] in S.FORBID:
            continue
        w = [S.w2s(x) for x in c["initial_relators"]]
        A, B = S.ccs(w[0]), S.ccs(w[1])
        for i, (P, Q) in enumerate(((A, B), (B, A))):
            ns = {STD[p] for p in P if p in STD}
            for n in ns:
                key = min(q for p, q in zip(P, Q) if STD.get(p) == n)
                lad[key][n].add(cid[-5:])
    ladders, tests, slack, pred = [], collections.Counter(), [], []
    for key, d in lad.items():
        if len(d) < 2:
            continue
        rungs = {}
        for n, rows in d.items():
            best = min(rows, key=lambda r: (REC.get(r, (9999, 0))[0], r))
            rungs[n] = {"rows": sorted(rows), "rec": REC.get(best, (None, 0))[0], "k": REC.get(best, (None, 0))[1],
                        "srec": SREC.get(best, (None, 0))[0], "sk": SREC.get(best, (None, 0))[1], "ours": ours.get(best), "row": best}
        ladders.append({"other": key, "rungs": {str(n): v for n, v in sorted(rungs.items())}})
        for n in sorted(rungs):
            a, b = rungs.get(n - 2), rungs.get(n - 1)
            if not (a and b and a["rec"] and b["rec"]):
                continue
            law = 2 * b["rec"] - a["rec"]
            cur = rungs[n]
            if cur["rec"]:
                tests["n"] += 1
                tests["hit" if cur["rec"] == law else ("over" if cur["rec"] > law else "under")] += 1
                if cur["rec"] > law:
                    for r in cur["rows"]:
                        slack.append((cur["rec"] - law, r, n, key, cur["rec"], REC.get(r, (0, 0))[1], law, SREC.get(r, (None, 0))[0], ours.get(r)))
            else:
                for r in cur["rows"]:
                    pred.append((r, n, key, law, a["row"], b["row"], b["ours"]))
    json.dump({"boards": [fa, fs], "ladders": ladders}, open(OUT / "ladders.json", "w"))
    slack.sort(key=lambda x: (-x[0], x[1]))
    with open(OUT / "slack.tsv", "w") as f:
        f.write("excess\trow\tn\tother\tac_rec\tk\tlaw\tst_rec\tours\n")
        for x in slack:
            f.write("\t".join(map(str, x)) + "\n")
    with open(OUT / "predict.tsv", "w") as f:
        f.write("row\tn\tother\tlaw\tfrom_n-2\tfrom_n-1\tours_n-1\n")
        for x in pred:
            f.write("\t".join(map(str, x)) + "\n")
    rows_on = sum(len(v["rows"]) for L in ladders for v in L["rungs"].values())
    print("boards %s %s; ladders >=2 rungs %d; rows on ladders %d" % (fa, fs, len(ladders), rows_on))
    print("law test (3 consecutive recorded rungs): %d cases; exact %d (%.0f%%), over %d, under %d" % (
        tests["n"], tests["hit"], 100.0 * tests["hit"] / max(1, tests["n"]), tests["over"], tests["under"]))
    print("slack rows (record above law): %d; unsolved rungs with a prediction: %d" % (len(slack), len(pred)))


if __name__ == "__main__":
    main()
