"""Compare every Stable AC move in C rank-3 pilot with pinned official core."""
import json
import random
import subprocess
import sys

sys.path.insert(0, "SAIR-AC/competition/tools")
from verifier import stable_core

rng = random.Random(20260928)
states = [((1,), (2,))]
for index in range(39):
    state = states[-1] if index % 5 else ((1,), (2,))
    for _ in range(100):
        m = rng.randrange(257)
        nxt, reason = stable_core.apply_move(state, m)
        if nxt is not None and 2 <= len(nxt) <= 3 and sum(map(len, nxt)) <= 35:
            states.append(nxt)
            break
    else:
        states.append(((1,), (2,), (3,)))
query = []
for state in states:
    vals = [len(state)]
    for word in state:
        vals.extend((len(word), *word))
    for m in range(257):
        query.append(" ".join(map(str, [m, *vals])))
p = subprocess.run(["work/abc_beam/sac_rank3", "apply"],
                   input="\n".join(query)+"\n", text=True, capture_output=True)
assert p.returncode == 0, p.stderr
lines = p.stdout.splitlines()
assert len(lines) == len(states)*257
bad = []
for i, state in enumerate(states):
    for m in range(257):
        got = lines[i*257+m]
        want, reason = stable_core.apply_move(state, m)
        if want is None:
            if got != "NA":
                bad.append({"state": i, "move": m, "got": got, "reason": reason})
            continue
        nums = list(map(int, got.split()))
        if nums[0] != len(want):
            bad.append({"state": i, "move": m, "got": got, "want": want})
            continue
        k = 1
        words = []
        for _ in want:
            n = nums[k]
            k += 1
            words.append(tuple(nums[k:k+n]))
            k += n
        if tuple(words) != want:
            bad.append({"state": i, "move": m, "got": got, "want": want})
print(json.dumps({"states": len(states), "moves_per_state": 257,
                  "comparisons": len(lines), "mismatches": bad[:20],
                  "mismatch_count": len(bad),
                  "official_revision": "a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e"},
                 indent=2))
