#!/usr/bin/env python3
"""UPG-H adapter: Stable AC through the (y,x) orientation.

For each SAC row in targets.json whose AC twin has a path in jobs.json, run tools/acc/yx_shortcut.py
(exact meet in the middle from late states of the AC path to (y, x)) with target = the SAC record,
and write a harvestable line {"id": "sac-XXXXX", "sac": route + [15, 15]}. From (y, x), destabilizing
r0 then r1 (moves 15, 15) reaches the empty presentation. The official verifier replays every line.

usage: yx_rows.py SAIR JOBS TARGETS OUT PER_ROW_SECONDS"""
import json
import os
import subprocess
import sys
from pathlib import Path

SAIR, JOBS, TARGETS, OUT, PER_ROW = sys.argv[1:6]
TOOL = Path(__file__).resolve().parents[2] / "yx_shortcut.py"
jobs = json.loads(Path(JOBS).read_text())
for t in json.loads(Path(TARGETS).read_text()):
    ac = t["id"]
    path = jobs.get(ac)
    if path is None or t.get("record") is None:
        continue
    try:
        p = subprocess.run([sys.executable, str(TOOL), ac, json.dumps(path), str(t["record"])], capture_output=True,
                           text=True, timeout=float(PER_ROW), env={**os.environ, "SAIR": SAIR})
        out = [json.loads(l) for l in p.stdout.splitlines() if l.startswith("{")]
        ended = "finished"
    except subprocess.TimeoutExpired:
        out, ended = [], "row_time_limit"
    rec = {"row": "s" + ac, "target": t["record"], "ended": ended}
    hit = next((o for o in out if o.get("line") is not None), None)
    if hit:
        rec.update({"id": "s" + ac, "sac": hit["line"] + [15, 15], "prefix": hit.get("prefix")})
    with open(OUT, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(json.dumps({k: v for k, v in rec.items() if k != "sac"}), flush=True)
