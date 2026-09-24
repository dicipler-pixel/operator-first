"""Validate sac_rank3 apply against official stable_core.apply_move on N random (state, move) pairs, ranks 0..8."""
import random, subprocess, sys
sys.path.insert(0, sys.argv[2] + '/competition/tools'); from verifier import stable_core
rng = random.Random(7); N = int(sys.argv[3])
def rw(k, n):
    w = []
    while len(w) < n:
        a = rng.choice([g * s for g in range(1, k + 1) for s in (1, -1)])
        if w and w[-1] == -a: continue
        w.append(a)
    return tuple(w)
def rs():
    k = rng.choice([0, 1, 2, 2, 3, 3, 3, 4, 8])
    st = []
    for _ in range(k):
        r = rng.random()
        st.append((rng.randint(1, k),) if r < 0.25 else rw(k, rng.randint(0, 3 if r < 0.4 else 30)))
    return tuple(st)
cases = [(rs(), rng.randrange(257)) for _ in range(N)]
inp = ''.join(f"{m} {len(s)} " + ' '.join(f"{len(w)} " + ' '.join(map(str, w)) for w in s) + "\n" for s, m in cases)
out = subprocess.run([sys.argv[1], 'apply'], input=inp, capture_output=True, text=True).stdout.splitlines()
bad = 0; na = 0
for (s, m), line in zip(cases, out):
    exp, reason = stable_core.apply_move(s, m)
    if line == 'NA': got = None; na += 1
    else:
        v = list(map(int, line.split())); k = v[0]; i = 1; got = []
        for _ in range(k): L = v[i]; got.append(tuple(v[i + 1:i + 1 + L])); i += 1 + L
        got = tuple(got)
    if got != exp: bad += 1
print(f"pairs={N} outputs={len(out)} not_applicable={na} mismatches={bad}")
