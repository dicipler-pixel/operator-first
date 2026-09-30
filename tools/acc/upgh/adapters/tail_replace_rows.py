#!/usr/bin/env python3
"""UPG-H adapter: run research/acc/optimality/tail_replace.py on each row of jobs.json and write
harvestable JSON lines {"row": ..., "final_path": [...], "start_len": n}.

usage: tail_replace_rows.py SAIR BIN T9 WORK JOBS OUT CAPSLACK BUDGET PER_ROW_SECONDS
A row that hits its time limit keeps whatever the tool printed so far (a scoped miss, never a claim)."""
import json
import re
import subprocess
import sys
from pathlib import Path

SAIR, BIN, T9, WORK, JOBS, OUT, SLACK, BUDGET, PER_ROW = sys.argv[1:10]
TOOL = Path(__file__).resolve().parents[4] / "research/acc/optimality/tail_replace.py"
if not TOOL.is_file():
    sys.exit("tool not found: %s" % TOOL)
errors = 0
for row, path in json.loads(Path(JOBS).read_text()).items():
    try:
        p = subprocess.run([sys.executable, str(TOOL), SAIR, BIN, T9, WORK, row, json.dumps(path), SLACK, BUDGET],
                           capture_output=True, text=True, timeout=float(PER_ROW))
        text, ended = p.stdout, "finished"
        if p.returncode != 0 or "FINAL" not in text:
            ended = "tool_error (exit %s): %s" % (p.returncode, (p.stderr or "")[-300:])
            errors += 1
    except subprocess.TimeoutExpired as exc:
        text, ended = (exc.stdout or b"").decode() if isinstance(exc.stdout, bytes) else (exc.stdout or ""), "row_time_limit"
    best = path
    fin = re.search(r"^FINAL (\S+) (\d+) (\[[\d,]*\])", text, re.M)
    if fin:
        best = json.loads(fin.group(3))
    rec = {"row": row, "start_len": len(path), "end_len": len(best), "final_path": best, "ended": ended,
           "splices": len(re.findall(r"splice at", text))}
    with open(OUT, "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(json.dumps({k: v for k, v in rec.items() if k != "final_path"}), flush=True)
sys.exit(3 if errors else 0)
