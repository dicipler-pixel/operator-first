"""Compare original and fixed file-backed visited table on the same bounded row."""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, "SAIR-AC/competition/tools")
from verifier import core, stable_core

row_id, cap, budget, maxd = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
manifest = json.load(open("SAIR-AC/competition/tools/verifier/data/manifest.json"))
challenges = {r["challenge_id"]: r for r in manifest["challenges"]}
row = challenges[row_id]
enc = {1: 0, -1: 1, 2: 2, -2: 3}
args = [str(len(row["initial_relators"][0])),
        *map(lambda x: str(enc[x]), row["initial_relators"][0]),
        str(len(row["initial_relators"][1])),
        *map(lambda x: str(enc[x]), row["initial_relators"][1])]
work = Path("work/abc_disk_bench")
work.mkdir(parents=True, exist_ok=True)
result = {"id": row_id, "cap": cap, "budget": budget, "maxd": maxd,
          "official_revision": "a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e"}
for variant in ("original", "disk"):
    cmd = [str(Path("work/abc_beam/acc_capped" +
                    ("_disk" if variant == "disk" else ""))),
           "work/T9.tab", str(cap), str(budget), str(work), variant, *args]
    env = os.environ.copy()
    env["MAXD"] = str(maxd)
    env["INIT_LOG2"] = "20"
    if variant == "disk":
        env["VISITED_FILE"] = str(work / "visited.tab")
    t0 = time.monotonic()
    p = subprocess.run(cmd, env=env, capture_output=True, text=True)
    (work / (variant + ".stdout")).write_text(p.stdout)
    (work / (variant + ".stderr")).write_text(p.stderr)
    entry = {"returncode": p.returncode, "wall_s": round(time.monotonic()-t0, 2),
             "summary": next((l for l in p.stdout.splitlines()
                              if " states=" in l), None),
             "memory_type": "MAP_SHARED" if variant == "disk" else "anonymous"}
    paths = {}
    for label, length, moves in re.findall(r"\] (AC|SAC) (\d+) PATH([\d ]+)", p.stdout):
        assert len(moves.split()) == int(length)
        path = list(map(int, moves.split()))
        check = (core.verify(row, path, "ac-r2-v1", manifest["limits"])
                 if label == "AC" else stable_core.verify(
                     challenges["sac-" + row_id[3:]], path, "sac-r8-v1",
                     manifest["limits"]))
        paths[label] = {"moves": path, "official": check}
    entry["paths"] = paths
    result[variant] = entry
print(json.dumps(result, indent=2))
