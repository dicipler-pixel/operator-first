"""Bounded rank-3 Stable AC pilot on long rows; no claim beyond A+B."""
import json
import os
import subprocess
import sys
import time

manifest = json.load(open("SAIR-AC/competition/tools/verifier/data/manifest.json"))
rows = {x["challenge_id"]: x for x in manifest["challenges"]}
A, B = int(sys.argv[1]), int(sys.argv[2])
ids = sys.argv[3:]
inputs = []
for cid in ids:
    r0, r1 = rows[cid]["initial_relators"]
    inputs.append(" ".join(map(str, [cid, len(r0), *r0, len(r1), *r1])))
cmd = ["work/abc_beam/sac_rank3", "3", str(A), str(B)]
env = os.environ.copy()
env["NSLOTS"] = "1048576"
t0 = time.monotonic()
p = subprocess.run(cmd, input="\n".join(inputs)+"\n", capture_output=True,
                   text=True, env=env, timeout=120)
print(json.dumps({"ids": ids, "rank_cap": 3, "forward_radius": A,
                  "backward_radius": B, "state_key": "128-bit fingerprint",
                  "returncode": p.returncode, "wall_s": round(time.monotonic()-t0, 2),
                  "stdout": p.stdout, "stderr": p.stderr,
                  "scope": "pilot only; no long-row record claim"}, indent=2))
