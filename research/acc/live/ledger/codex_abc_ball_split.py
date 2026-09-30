"""Compare T8 and T9 goal balls with the same capped start search."""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, "SAIR-AC/competition/tools")
from verifier import core, stable_core

manifest = json.load(open("SAIR-AC/competition/tools/verifier/data/manifest.json"))
rows = {x["challenge_id"]: x for x in manifest["challenges"]}
cid = sys.argv[1]
cap, budget, maxd = map(int, sys.argv[2:5])
r0, r1 = rows[cid]["initial_relators"]
enc = {1: 0, -1: 1, 2: 2, -2: 3}
state = [str(len(r0)), *(str(enc[x]) for x in r0),
         str(len(r1)), *(str(enc[x]) for x in r1)]
work = Path("work/abc_split")
work.mkdir(exist_ok=True, parents=True)
result = {"id": cid, "cap": cap, "budget": budget, "maxd": maxd,
          "tool": "acc_capped_disk", "status": "benchmark only",
          "official_revision": "a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e"}
for radius in (9, 8):
    tag = "t" + str(radius)
    cmd = ["work/abc_beam/acc_capped_disk", f"work/T{radius}.tab",
           str(cap), str(budget), str(work), tag, *state]
    env = os.environ.copy()
    env["MAXD"] = str(maxd)
    env["VISITED_FILE"] = str(work / (tag + "_visited.tab"))
    start = time.monotonic()
    p = subprocess.run(cmd, capture_output=True, text=True, env=env,
                       timeout=300)
    (work / (tag + ".stdout")).write_text(p.stdout)
    (work / (tag + ".stderr")).write_text(p.stderr)
    found = {}
    for label, length, moves in re.findall(r"\] (AC|SAC) (\d+) PATH([\d ]+)",
                                            p.stdout):
        path = list(map(int, moves.split()))
        assert len(path) == int(length)
        target = rows[cid if label == "AC" else "sac-" + cid[3:]]
        verdict = (core.verify(target, path, "ac-r2-v1", manifest["limits"])
                   if label == "AC" else stable_core.verify(
                       target, path, "sac-r8-v1", manifest["limits"]))
        found[label] = {"path": path, "verifier": verdict}
    result[tag] = {
        "returncode": p.returncode,
        "wall_s": round(time.monotonic() - start, 2),
        "summary": next((line for line in p.stdout.splitlines()
                         if " states=" in line), None),
        "paths": found,
        "stderr_tail": p.stderr.splitlines()[-3:]}
print(json.dumps(result, indent=2))
