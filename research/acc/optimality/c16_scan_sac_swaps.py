"""Check the swapped rank-two reverse finish plus two stable deletions."""
import gzip
import json
import subprocess
import sys
from pathlib import Path

manifest_file, board_file, table, binary, out = sys.argv[1:]
sys.path.insert(0, str(Path(manifest_file).parents[2]))
from verifier import stable_core

manifest = json.load(open(manifest_file))["challenges"]
board = json.load(gzip.open(board_file))
live = {x["challengeId"]: x for x in board["data"]["items"]}
enc = {1: 0, -1: 1, 2: 2, -2: 3}
swap = {0: 2, 1: 3, 2: 0, 3: 1}
PI = [0, 1, 2, 3, 4, 5, 8, 9, 6, 7, 12, 13, 10, 11]
rows = [x for x in manifest if x["challenge_id"].startswith("sac-")
        and len(x["initial_relators"]) == 2
        and sum(map(len, x["initial_relators"])) <= 16]
with open(out + ".queries", "w") as f:
    for row in rows:
        q = []
        for w in row["initial_relators"]:
            q += [len(w)] + [swap[enc[v]] for v in w]
        f.write(" ".join(map(str, q)) + "\n")
subprocess.run([binary, "batch", table, out + ".queries", out + ".answers"], check=True)
lines = open(out + ".answers").read().splitlines()
assert len(lines) == len(rows)
lim = {"max_path_length": 10**6, "max_total_relator_length": 10**6, "max_work": 10**12}
results, hits = [], []
for row, line in zip(rows, lines):
    head, _, tail = line.partition("|")
    d = int(head); rec = live[row["challenge_id"]]["currentBestLength"]
    r = {"id": row["challenge_id"], "start_length": sum(map(len, row["initial_relators"])),
         "swapped_ceiling_distance": d, "record_at_snapshot": rec,
         "k_at_snapshot": live[row["challenge_id"]]["kTeams"]}
    if d >= 0 and (rec is None or d + 2 <= rec):
        path = [PI[x] for x in map(int, tail.split())] + [15, 15]
        v = stable_core.verify(row, path, stable_core.MOVE_SPEC_VERSION, lim)
        r["verified"] = bool(v.get("ok")) and v.get("length") == len(path)
        r["path"] = path
        if r["verified"]:
            hits.append(r)
        else:
            r["verifier"] = v
    results.append(r)
with open(out + ".json", "w") as f:
    json.dump({"snapshot": board["pulledAt"], "scanned": len(rows), "hits": hits,
               "results": results}, f, indent=2)
print(json.dumps({"snapshot": board["pulledAt"], "scanned": len(rows),
                  "in_table": sum(x["swapped_ceiling_distance"] >= 0 for x in results),
                  "verified_hits": len(hits),
                  "hits_summary": [{k: h[k] for k in ("id", "swapped_ceiling_distance", "record_at_snapshot", "k_at_snapshot")}
                                   for h in hits]}))
