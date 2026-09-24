"""Validate acc_opt's C kernel against the official core.apply_move on N random (state, move) pairs."""
import random, subprocess, sys, json
sys.path.insert(0, sys.argv[2] + '/competition/tools')
from verifier import core
N = int(sys.argv[3]) if len(sys.argv) > 3 else 100000
rng = random.Random(20260924)
ENC = {1: 0, -1: 1, 2: 2, -2: 3}; DEC = {v: k for k, v in ENC.items()}
man = json.load(open(sys.argv[2] + '/competition/tools/verifier/data/manifest.json'))
starts = [tuple(tuple(r) for r in c['initial_relators']) for c in man['challenges'] if c['challenge_id'].startswith('ac-')]
def rword(n):
    w = []
    while len(w) < n:
        a = rng.choice((1, -1, 2, -2))
        if w and w[-1] == -a: continue
        w.append(a)
    return tuple(w)
def rstate():
    k = rng.random()
    if k < 0.3:  # random walk from an official start
        s = rng.choice(starts)
        for _ in range(rng.randint(0, 12)): s = core.apply_move(s, rng.randrange(14))
        return s
    if k < 0.4:  # tiny / degenerate words to hit cancellation edge cases
        return (rword(rng.randint(0, 3)), rword(rng.randint(0, 3)))
    return (rword(rng.randint(0, 150)), rword(rng.randint(0, 150)))
cases = [(rstate(), rng.randrange(14)) for _ in range(N)]
inp = ''.join(f"{m} {len(s[0])} {len(s[1])} " + ' '.join(str(ENC[a]) for a in s[0] + s[1]) + '\n' for s, m in cases)
out = subprocess.run([sys.argv[1], 'apply'], input=inp, capture_output=True, text=True, check=True).stdout.splitlines()
bad = 0
for (s, m), line in zip(cases, out):
    v = list(map(int, line.split())); l0, l1 = v[0], v[1]
    got = (tuple(DEC[x] for x in v[2:2 + l0]), tuple(DEC[x] for x in v[2 + l0:2 + l0 + l1]))
    if got != core.apply_move(s, m): bad += 1
print(f"pairs={N} outputs={len(out)} mismatches={bad}")
sys.exit(0 if bad == 0 and len(out) == N else 1)
