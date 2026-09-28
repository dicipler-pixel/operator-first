"""Bounded T8 memory-wall trial, with raw logs and official path verification."""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, "SAIR-AC/competition/tools")
from verifier import core, stable_core

cid, cap, budget, maxd, timeout = sys.argv[1], *map(int, sys.argv[2:6])
manifest = json.load(open("SAIR-AC/competition/tools/verifier/data/manifest.json"))
rows = {x["challenge_id"]: x for x in manifest["challenges"]}
r0, r1 = rows[cid]["initial_relators"]
enc = {1: 0, -1: 1, 2: 2, -2: 3}
state = [str(len(r0)), *(str(enc[x]) for x in r0),
         str(len(r1)), *(str(enc[x]) for x in r1)]
work = Path("work/abc_memrow")
work.mkdir(parents=True, exist_ok=True)
tag = cid.replace("-", "")
cmd = ["work/abc_beam/acc_capped_disk", "work/T8.tab", str(cap),
       str(budget), str(work), tag, *state]
env = os.environ.copy()
env["MAXD"] = str(maxd)
stdout_path, stderr_path = work / "trial.stdout", work / "trial.stderr"
start = time.monotonic()
with stdout_path.open("w") as out, stderr_path.open("w") as err:
    p = subprocess.Popen(cmd, stdout=out, stderr=err, env=env)
    try:
        code = p.wait(timeout=timeout)
        timed_out = False
    except subprocess.TimeoutExpired:
        p.kill()
        code = p.wait()
        timed_out = True
stdout = stdout_path.read_text()
stderr = stderr_path.read_text()
found = {}
for label, length, moves in re.findall(r"\] (AC|SAC) (\d+) PATH([\d ]+)", stdout):
    path = list(map(int, moves.split()))
    assert len(path) == int(length)
    target = rows[cid if label == "AC" else "sac-" + cid[3:]]
    official = (core.verify(target, path, "ac-r2-v1", manifest["limits"])
                if label == "AC" else stable_core.verify(
                    target, path, "sac-r8-v1", manifest["limits"]))
    found[label] = {"moves": path, "official": official}
result = {"id": cid, "cap": cap, "budget": budget, "maxd": maxd,
          "timeout_s": timeout, "tool": "acc_capped_disk with T8, anonymous fixed visited",
          "official_revision": "a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e",
          "returncode": code, "timed_out": timed_out,
          "wall_s": round(time.monotonic() - start, 2),
          "summary": next((line for line in stdout.splitlines()
                           if " states=" in line), None),
          "last_depth": next((line for line in reversed(stderr.splitlines())
                              if " cap=" in line and " d=" in line), None),
          "found": found,
          "status": "complete" if " CLOSED" in stdout else "incomplete",
          "stdout_path": str(stdout_path), "stderr_path": str(stderr_path)}
print(json.dumps(result, indent=2))
