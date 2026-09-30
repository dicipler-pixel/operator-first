"""Query a C16 reverse table at every eligible state of a known AC path.

Usage: python c16_splice_path.py MANIFEST ID MOVES TABLE C16_BINARY OUT_PREFIX
Outputs queries, batch answers, and a JSON record with any shortening candidate.
The official verifier checks each candidate before it is recorded.
"""
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).parents[2]))
from verifier import core

manifest, row_id, moves_file, table, binary, out = sys.argv[1:]
with open(manifest) as fh:
    challenges = json.load(fh)
if isinstance(challenges, dict):
    challenges = challenges.get("challenges", challenges.get("rows", []))
challenge = next(ch for ch in challenges if ch["challenge_id"] == row_id)
moves = json.load(open(moves_file))
assert all(isinstance(m, int) and 0 <= m < 14 for m in moves)
state = tuple(map(tuple, challenge["initial_relators"]))
enc = {1: 0, -1: 1, 2: 2, -2: 3}
queries = []
for idx in range(len(moves) + 1):
    if sum(map(len, state)) <= 16:
        r0, r1 = state
        q = [len(r0), *(enc[v] for v in r0), len(r1), *(enc[v] for v in r1)]
        queries.append((idx, state, q))
    if idx < len(moves):
        state = core.apply_move(state, moves[idx])
query_file, answer_file = out + ".queries", out + ".answers"
with open(query_file, "w") as fh:
    for _, _, q in queries:
        fh.write(" ".join(map(str, q)) + "\n")
subprocess.run([binary, "batch", table, query_file, answer_file], check=True)
answers = open(answer_file).read().splitlines()
assert len(answers) == len(queries)
lim = {"max_path_length": 10**6, "max_total_relator_length": 10**6, "max_work": 10**12}
records = []
for (idx, st, _), answer in zip(queries, answers):
    dist_text, _, path_text = answer.partition("|")
    d = int(dist_text.strip())
    suffix = list(map(int, path_text.split()))
    rec = {"prefix_moves": idx, "state_lengths": [len(st[0]), len(st[1])],
           "old_remaining": len(moves) - idx, "c16_distance": d}
    if d >= 0:
        assert len(suffix) == d
        candidate = moves[:idx] + suffix
        v = core.verify(challenge, candidate, core.MOVE_SPEC_VERSION, lim)
        rec["verified"] = bool(v.get("ok")) and v.get("length") == len(candidate)
        if not rec["verified"]:
            rec["verifier"] = v
        rec["candidate_length"] = len(candidate)
        if rec["verified"] and len(candidate) < len(moves):
            rec["candidate"] = candidate
    records.append(rec)
result = {"id": row_id, "old_length": len(moves), "queried": len(queries),
          "best_length": min((r["candidate_length"] for r in records if r.get("verified")), default=None),
          "records": records}
with open(out + ".json", "w") as fh:
    json.dump(result, fh, indent=2)
print(json.dumps({k: v for k, v in result.items() if k != "records"}))
print(json.dumps([r for r in records if "candidate" in r]))
