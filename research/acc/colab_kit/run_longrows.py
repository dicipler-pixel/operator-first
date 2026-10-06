#!/usr/bin/env python3
"""Long-row shortener for Colab or the owner's PC (no model, no API, no repo pull).

Our roads on the long Miller-Schupp rows (records 93..2079, mostly held by one team) are constructed roads, and constructed
roads collapse under exact window shortening (session 2: ac-05698 128 -> 110, ac-06018 164 -> 152). The exact window optimizer
(acc_window: every pair i<j with j-i <= 14 is checked through radius-6/7 balls) costs about 6 s per road state per pass, so a
2,000-move road needs hours per pass. This driver cuts each road into PIECES of about 140 moves, optimizes the pieces in
parallel (one per CPU core), stitches the road back, cleans commuting pairs, re-checks the whole road on the pinned official
verifier, and repeats with shifted cut points until a full round gives nothing. Every improvement is saved at once, piece by piece (a restart loses at most one piece).

Kit files (same folder): run_longrows.py, acc_window.c, acc_opt.c, commute_clean.py, roads.jsonl.
Outputs in --out (e.g. a Google Drive folder):
  state.jsonl                 best road per row so far (the run resumes from it)
  LINES_COLAB_LONGROWS.txt    every row whose road got shorter, as "ac-XXXXX: [moves]" (UPG-H's check-in picks it up)
  log.txt                     progress
usage:  python3 run_longrows.py --out DIR [--hours 10] [--rows ac-00676,ac-03773] [--piece 140] [--jobs N]
"""
import argparse
import concurrent.futures as cf
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

KIT = Path(__file__).resolve().parent
PIN = "a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e"
SAIR_URL = "https://github.com/SAIRcompetition/Andrews-Curtis"
E = {1: 0, -1: 1, 2: 2, -2: 3}
sys.path.insert(0, str(KIT))
from commute_clean import clean  # noqa: E402


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")


class Log:
    def __init__(self, path):
        self.f = open(path, "a")

    def __call__(self, msg):
        line = "[%s] %s" % (utc(), msg)
        print(line, flush=True)
        self.f.write(line + "\n")
        self.f.flush()


def ensure_sair(path):
    path = Path(path)
    if not (path / "competition/tools/verifier").is_dir():
        subprocess.run(["git", "clone", "-q", SAIR_URL, str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "checkout", "-q", PIN], check=True)
    return path


def ensure_bin(workdir):
    exe = Path(workdir) / "acc_window_kit"
    if not exe.exists():
        subprocess.run(["gcc", "-O3", "-march=native", "-Wno-misleading-indentation", "-o", str(exe),
                        str(KIT / "acc_window.c"), "-lm"], check=True, cwd=str(KIT))
    return exe


def piece(job):
    """Run acc_window on one piece; return (index, moves) with the best path it printed (even if stopped early)."""
    exe, work, idx, st0, moves, secs = job
    r0, r1 = st0
    args = [str(exe), work, str(len(r0)), *[str(E[t]) for t in r0], str(len(r1)), *[str(E[t]) for t in r1],
            str(len(moves)), *map(str, moves)]
    os.makedirs(work, exist_ok=True)
    best = list(moves)
    try:
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True,
                             env=dict(os.environ, ACC_ANY_END="1"))
        t0 = time.time()
        for line in p.stdout:
            if line.startswith(("PATH ", "FINALPATH")):
                m = list(map(int, line.split()[1:]))
                if len(m) < len(best):
                    best = m
            if time.time() - t0 > secs:
                p.kill()
                break
        p.wait()
    except Exception:
        pass
    shutil.rmtree(work, ignore_errors=True)
    return idx, best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--hours", type=float, default=10)
    ap.add_argument("--rows", default="", help="comma list; default = every row in roads.jsonl, smallest gap first")
    ap.add_argument("--piece", type=int, default=140, help="piece length in moves")
    ap.add_argument("--piece-minutes", type=float, default=60, help="time cap per piece")
    ap.add_argument("--jobs", type=int, default=os.cpu_count() or 2)
    ap.add_argument("--sair", default="/content/sair" if Path("/content").is_dir() else str(Path.home() / ".cache/acc_sair"))
    ap.add_argument("--work", default="/content/acc_work" if Path("/content").is_dir() else str(Path.home() / ".cache/acc_work"))
    a = ap.parse_args()
    out = Path(a.out)
    out.mkdir(parents=True, exist_ok=True)
    log = Log(out / "log.txt")
    t_end = time.time() + a.hours * 3600
    sair = ensure_sair(a.sair)
    sys.path.insert(0, str(sair / "competition/tools"))
    from verifier import core
    man = json.load(open(sair / "competition/tools/verifier/data/manifest.json"))
    CH = {c["challenge_id"]: c for c in man["challenges"]}
    Path(a.work).mkdir(parents=True, exist_ok=True)
    exe = ensure_bin(a.work)

    roads = {}
    for src in (KIT / "roads.jsonl", out / "state.jsonl"):          # state.jsonl (progress) wins
        if src.exists():
            for line in open(src):
                x = json.loads(line)
                if x["id"] not in roads or len(x["moves"]) < len(roads[x["id"]]["moves"]):
                    roads[x["id"]] = x
    order = [r.strip() for r in a.rows.split(",") if r.strip()] or sorted(roads, key=lambda c: (roads[c]["moves"].__len__() - (roads[c].get("record") or 0), c))
    start_len = {c: len(roads[c]["moves"]) for c in roads}
    log("start: %d rows, %d cores, %.1f h budget" % (len(order), a.jobs, a.hours))

    def save():
        with open(out / "state.jsonl", "w") as f:
            for c in roads:
                f.write(json.dumps(roads[c]) + "\n")
        better = [c for c in roads if len(roads[c]["moves"]) < roads[c].get("orig", start_len[c])]
        with open(out / "LINES_COLAB_LONGROWS.txt", "w") as f:
            f.write("# Colab long-row shortener; each line passed the pinned official verifier (ac-r2-v1)\n")
            for c in sorted(better):
                f.write("%s: [%s]\n" % (c, ",".join(map(str, roads[c]["moves"]))))

    for c in roads:
        roads[c].setdefault("orig", len(roads[c]["moves"]))
    for cid in order:
        if time.time() > t_end:
            break
        if cid not in roads or cid not in CH:
            log("skip %s (no road or unknown row)" % cid)
            continue
        R = roads[cid]
        moves = list(R["moves"])
        log("%s: start %d (record %s)" % (cid, len(moves), R.get("record")))
        shift, quiet = 0, 0
        while time.time() < t_end and quiet < 2:
            st = [tuple(tuple(r) for r in CH[cid]["initial_relators"])]
            for m in moves:
                st.append(core.apply_move(st[-1], m))
            cuts = list(range(shift, len(moves), a.piece))
            if not cuts or cuts[0] != 0:
                cuts = [0] + cuts
            cuts.append(len(moves))
            jobs = [(exe, "%s/%s_%d" % (a.work, cid, i), i, st[cuts[i]], moves[cuts[i]:cuts[i + 1]],
                     min(a.piece_minutes * 60, max(60, t_end - time.time()))) for i in range(len(cuts) - 1)]
            # checkpoint per piece: as soon as one piece comes back shorter, splice it in, re-verify the whole road and save
            new = {i: jobs[i][4] for i in range(len(jobs))}
            improved = False
            with cf.ThreadPoolExecutor(max_workers=a.jobs) as ex:
                for f in cf.as_completed([ex.submit(piece, j) for j in jobs]):
                    idx, m = f.result()
                    if len(m) >= len(new[idx]):
                        continue
                    new[idx] = m
                    cand = clean([x for i in range(len(jobs)) for x in new[i]])
                    if len(cand) < len(R["moves"]) and core.verify(CH[cid], cand, "ac-r2-v1", man["limits"]).get("ok"):
                        log("%s: piece %d shorter; road %d -> %d (shift %d, saved)" % (cid, idx, len(R["moves"]), len(cand), shift))
                        R["moves"] = cand
                        save()
                        improved = True
            if improved:
                moves = list(R["moves"])
                quiet = 0
            else:
                quiet += 1
            shift = (shift + a.piece // 2) % a.piece
        log("%s: done at %d (started %d, record %s)" % (cid, len(moves), R["orig"], R.get("record")))
        save()
    log("finished; results in %s" % out)


if __name__ == "__main__":
    main()
