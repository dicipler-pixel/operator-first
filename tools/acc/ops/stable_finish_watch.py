"""Check a beam JSONL for scoreable Stable AC finishes of its AC paths.

Example:
  python stable_finish_watch.py --manifest SAIR/competition/tools/verifier/data/manifest.json \
      --board stable_board.json.gz --sweep ac_sweep.jsonl --out stable_hits.jsonl

This scans all path prefixes for a legal rank-two destabilization, with an
optional relator inversion, followed by the shortest rank-one finish. Every
reported line is checked with the pinned official Stable AC verifier.
The board is a snapshot; the sender must check the live record and sent ledger.
"""
import argparse
import gzip
import json
import sys
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--manifest", required=True)
parser.add_argument("--board", required=True)
parser.add_argument("--sweep", required=True)
parser.add_argument("--out", required=True)
args = parser.parse_args()
sys.path.insert(0, str(Path(args.manifest).resolve().parents[2]))
from verifier import core, stable_core

manifest = {r["challenge_id"]: r for r in
            json.load(open(args.manifest))["challenges"]}
opener = gzip.open if args.board.endswith(".gz") else open
with opener(args.board, "rt") as file:
    board_json = json.load(file)
board_data = board_json.get("data", board_json)
board = {r["challengeId"]: r for r in board_data["items"]}
limits = {"max_path_length": 10**6, "max_total_relator_length": 10**6,
          "max_work": 10**12}


def endings(state):
    """Yield short rank-2 -> empty finishes using legal rank-1 moves."""
    for j in range(2):
        pre = [j] if state[j] and len(state[j]) == 1 and state[j][0] < 0 else []
        s = core.apply_move(state, j) if pre else state
        t, reason = stable_core.apply_move(s, 15 + j)
        if reason is not None:
            continue
        if t == ((1,),):
            yield pre + [15 + j, 15]
        elif t == ((-1,),):
            yield pre + [15 + j, 0, 15]


hits = {}
scanned = 0
for raw in open(args.sweep):
    item = json.loads(raw)
    ac_id = item.get("id")
    path = item.get("ac") or item.get("path")
    if not ac_id or not ac_id.startswith("ac-") or not isinstance(path, list):
        continue
    if ac_id not in manifest:
        continue
    sac_id = ac_id.replace("ac-", "sac-")
    if sac_id not in board:
        continue
    check = core.verify(manifest[ac_id], path, core.MOVE_SPEC_VERSION, limits)
    if not check.get("ok"):
        raise ValueError(f"Input AC line invalid: {ac_id}: {check}")
    scanned += 1
    state = tuple(map(tuple, manifest[ac_id]["initial_relators"]))
    best = None
    best_index = None
    for i in range(len(path) + 1):
        for tail in endings(state):
            candidate = path[:i] + tail
            if best is None or len(candidate) < len(best):
                best, best_index = candidate, i
        if i < len(path):
            state = core.apply_move(state, path[i])
    record_length = board[sac_id].get("currentBestLength")
    if best is None or (record_length is not None and len(best) > record_length):
        continue
    verdict = stable_core.verify(manifest[sac_id], best,
                                  stable_core.MOVE_SPEC_VERSION, limits)
    if not verdict.get("ok"):
        raise ValueError(f"Stable candidate invalid: {sac_id}: {verdict}")
    rec = {"id": sac_id, "source_ac_id": ac_id,
           "source_ac_length": len(path), "prefix_index": best_index,
           "sac_len": len(best),
           "snapshot_record": record_length,
           "snapshot_k": board[sac_id]["kTeams"],
           "certificate_hash": verdict["certificate_hash"],
           "sac": best}
    if sac_id not in hits or rec["sac_len"] < hits[sac_id]["sac_len"]:
        hits[sac_id] = rec

with open(args.out, "w") as file:
    for key in sorted(hits):
        file.write(json.dumps(hits[key]) + "\n")
print(json.dumps({"verified_ac_paths": scanned,
                  "snapshot_scoring_stable_lines": len(hits),
                  "ids": sorted(hits)}))
