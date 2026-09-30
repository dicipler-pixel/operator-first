#!/usr/bin/env python3
"""UPG-H adapter: join saved roads (cross-road splice) with tools/acc/splice/splice.py.

Astra's receipt audit (research/acc/live/UPDATE_astra_to_upgh_20260930T2216Z_mathagent_release.md) found that all
five independently verified improving attempts of the day came from unions of saved roads (Kernel ac-00028 58->51,
Kernel ac-00003 92->84, Bob ac-00003 53->49), none from fresh bridges. This rung does exactly that for each row:

  pool = our best AC path (jobs.json) + every AC path the ledger ever recorded for the row (path.best, including the
         AC part of Stable lines that end in [16, 15]) + every team road for the row in research/acc/** and ACC_*.txt
  splice.py puts all states of all pool paths in one graph, adds exact radius-R shortcut edges, runs Dijkstra, then
  restarts acc_beam from waypoints on the spliced path and splices again.

Writes one harvestable line per row: {"id": "ac-XXXXX", "ac": best, "sac": best + [16, 15]} (Stable = AC + [16,15]).
The official verifier replays every line at harvest; splice.py already checks each pool path and each result.

usage: splice_rows.py SAIR BIN T9 WORK JOBS TARGETS OUT RADIUS ROUNDS ROW_S [SEED]
The ladder rung passes no SEED: the run is deterministic for a given pool, so code runs it once per row and moves on;
`upgh wake` reopens a row when a new road arrives. SEED (default 0) shifts the waypoint fractions for manual reruns."""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

SAIR, BIN, T9, WORK, JOBS, TARGETS, OUT = sys.argv[1:8]
RADIUS, ROUNDS, ROW_S = (int(x) for x in sys.argv[8:11])
SEED = int(sys.argv[11]) if len(sys.argv) > 11 else 0
HERE = Path(__file__).resolve()
REPO = HERE.parents[4]
TOOL = REPO / "tools/acc/splice/splice.py"
LEDGER = REPO / "research/acc/upgh/ledger.jsonl"
MAX_POOL, MAX_FILE = 40, 30_000_000
sys.path.insert(0, str(HERE.parents[1]))
from harvest import extract  # noqa: E402

if not TOOL.is_file():
    sys.exit("tool not found: %s" % TOOL)


def ledger_paths(num):
    out = []
    if not LEDGER.is_file():
        return out
    for line in open(LEDGER, encoding="utf-8"):
        if '"path.best"' not in line or num not in line:
            continue
        d = json.loads(line).get("data", {})
        moves = d.get("moves") or []
        if d.get("cid") == "ac-" + num:
            out.append(moves)
        elif d.get("cid") == "sac-" + num and moves[-2:] == [16, 15]:
            out.append(moves[:-2])
    return out


def team_paths(num):
    """AC roads for the row anywhere the team drops them (inbox, queue, exchange, sweeps, ledger notes) and in
    UPG-H task artifacts (lines.txt, out.jsonl)."""
    hits = subprocess.run(["grep", "-rlsF", "--exclude-dir=upgh", "-e", "-" + num, "research/acc", "--include=*.txt", "--include=*.jsonl",
                           "--include=*.json"], cwd=REPO, capture_output=True, text=True).stdout.split()
    hits += [p.name for p in REPO.glob("ACC_*.txt")]
    # task artifacts hold other lineages (mirror starts, beams, constructions) that never became path.best
    hits += subprocess.run(["grep", "-rlsF", "-e", "-" + num, "research/acc/upgh/artifacts", "--include=lines.txt",
                            "--include=out.jsonl"], cwd=REPO, capture_output=True, text=True).stdout.split()
    out = []
    for rel in hits:
        p = REPO / rel
        if not p.is_file() or p.stat().st_size > MAX_FILE:
            continue
        for cid, moves, _ in extract(p):
            if cid == "ac-" + num:
                out.append(moves)
            elif cid == "sac-" + num and moves[-2:] == [16, 15]:
                out.append(moves[:-2])
    return out


jobs = json.loads(Path(JOBS).read_text())
work = Path(WORK)
work.mkdir(parents=True, exist_ok=True)
errors = 0
for t in json.loads(Path(TARGETS).read_text()):
    ac, num = t["id"], t["id"].split("-")[1]
    src = {"ours": [jobs[ac]] if ac in jobs else [], "ledger": ledger_paths(num), "team": team_paths(num)}
    seen, pool = set(), []
    for kind in ("ours", "ledger", "team"):
        for p in src[kind]:
            if p and tuple(p) not in seen:
                seen.add(tuple(p))
                pool.append(p)
    pool.sort(key=len)
    pool = pool[:MAX_POOL]
    pool_file = work / ("pool_%s.jsonl" % ac)
    pool_file.write_text("".join(json.dumps({"path": p}) + "\n" for p in pool))
    # SEED moves the waypoint fractions so a repeat restarts beams from different states on the spliced path
    fracs = ",".join("%.2f" % (0.15 + ((f + 0.07 * SEED) % 0.7)) for f in (0.05, 0.25, 0.45, 0.65))
    log = work / ("splice_%s.log" % ac)
    rec = {"row": ac, "target": t["record"], "pool": len(pool),
           "sources": {k: len(v) for k, v in src.items()}, "radius": RADIUS, "rounds": ROUNDS, "fracs": fracs}
    t0 = time.time()
    with open(log, "w") as fh:
        proc = subprocess.Popen([sys.executable, str(TOOL), SAIR, BIN, T9, ac, str(pool_file), "--radius", str(RADIUS),
                                 "--rounds", str(ROUNDS), "--fracs", fracs, "--seeds", "1", "--jobs", "2"],
                                stdout=fh, stderr=subprocess.STDOUT, cwd=REPO, start_new_session=True)
        try:
            proc.wait(timeout=ROW_S)
            ended = "finished" if proc.returncode == 0 else "tool_error (exit %s)" % proc.returncode
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, 9)
            proc.wait()
            ended = "row_time_limit"
    text = log.read_text(errors="replace")
    best = None
    for m in re.finditer(r"^BEST (\d+) (\[[\d,]*\])", text, re.M):
        p = json.loads(m.group(2))
        if best is None or len(p) < len(best):
            best = p
    if ended.startswith("tool_error") and best is None:
        errors += 1
        rec["tail"] = text[-300:]
    rec.update({"ended": ended, "wall_s": round(time.time() - t0, 1),
                "rounds_log": [l for l in text.splitlines() if l.startswith("ROUND")]})
    if best:
        rec.update({"id": ac, "ac": best, "sac": best + [16, 15], "length": len(best),
                    "min_pool": len(pool[0]) if pool else None})
    with open(OUT, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(json.dumps({k: v for k, v in rec.items() if k not in ("ac", "sac")}), flush=True)
sys.exit(3 if errors else 0)
