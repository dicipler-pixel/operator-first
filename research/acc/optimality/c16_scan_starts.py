"""Check all short-start AC rows against a completed ceiling reverse table.
Usage: python c16_scan_starts.py MANIFEST BOARD_GZ TABLE BINARY OUT_PREFIX
"""
import gzip
import json
import subprocess
import sys
from pathlib import Path

manifest_file, board_file, table, binary, out = sys.argv[1:]
sys.path.insert(0, str(Path(manifest_file).parents[2]))
from verifier import core

manifest = json.load(open(manifest_file))["challenges"]
board = json.load(gzip.open(board_file))
live = {x["challengeId"]: x for x in board["data"]["items"]}
enc = {1: 0, -1: 1, 2: 2, -2: 3}
rows = [x for x in manifest if x["challenge_id"].startswith("ac-")
        and len(x["initial_relators"]) == 2
        and sum(map(len, x["initial_relators"])) <= 16]
with open(out + ".queries", "w") as f:
    for row in rows:
        q = []
        for w in row["initial_relators"]:
            q += [len(w)] + [enc[v] for v in w]
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
         "ceiling_distance": d, "record_at_snapshot": rec,
         "k_at_snapshot": live[row["challenge_id"]]["kTeams"]}
    if d >= 0 and (rec is None or d <= rec):
        path = list(map(int, tail.split()))
        v = core.verify(row, path, core.MOVE_SPEC_VERSION, lim)
        r["verified"] = bool(v.get("ok")) and v.get("length") == d
        r["path"] = path
        if r["verified"]:
            hits.append(r)
    results.append(r)
with open(out + ".json", "w") as f:
    json.dump({"snapshot": board["pulledAt"], "scanned": len(rows), "hits": hits,
               "results": results}, f, indent=2)
print(json.dumps({"snapshot": board["pulledAt"], "scanned": len(rows),
                  "in_table": sum(x["ceiling_distance"] >= 0 for x in results),
                  "verified_hits": len(hits),
                  "hits_summary": [{k: h[k] for k in ("id", "ceiling_distance", "record_at_snapshot", "k_at_snapshot")}
                                   for h in hits]}))
