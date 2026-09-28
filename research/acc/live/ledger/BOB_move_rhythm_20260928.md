# BOB — move-rhythm test on the 424 SAIR training solutions (2026-09-28)

Worker: Bob. Status: COMPLETE. Data: SAIR `competition/examples/training_424.json` (official repo commit a0fd6e6, sha256 4a607b16…). All 424 replay to (x, y) under the official `verifier.core.apply_move`.

## Idea
Solutions contain repeated macros ("rhythm"): blocks of moves reused back to back inside one solution and across many solutions. If so, the blocks are candidate supermoves for `acc_beam` / `acc_capped`.

## Why the test proves what it claims
Two null models, both keep each solution's length and first move:
- **B0 (permutation):** shuffle the moves. It keeps how many of each move a solution uses and destroys all order.
- **B1 (doublet):** a uniform random sequence with exactly the same adjacent pairs (Altschul–Erickson shuffle, random Eulerian trail). Every "never follow m by its inverse" rule and every adjacency habit survives. Only structure longer than two moves is destroyed.

Beating B0 alone could just be adjacency rules. **Only beating B1 means real multi-move macros.**

Statistics:
- `tandem`: blocks of length 2–6 immediately repeated (u u), summed over solutions.
- `sharedK`: K-grams appearing in ≥ 5 different solutions.
- `specpeak`: largest periodogram share of the conjugation on/off signal, summed over solutions.

p-values come from 1000 full-pool shuffles.

**Kill condition (fixed before the run):** no statistic beats B1 at p < 0.01 means the idea is dead beyond adjacency.

**Controls:**
- The doublet shuffle preserves pairs on all 424.
- Positive control: plant (6,2,9,4)×3 into every solution. It must beat B1, and it does.
- Negative control: a pool drawn from B1. It must not beat B1, and it doesn't (p 0.24–0.81).

## Result (N = 1000)
| statistic | real | B0 mean±sd | B1 mean±sd | p vs B1 |
|---|---|---|---|---|
| tandem | 589 | 152 ± 13 | 365 ± 17 | 0.001 (floor) |
| shared4 | 608 | 227 ± 11 | 607 ± 12 | 0.48 |
| shared5 | 404 | 1.6 ± 1.3 | 176 ± 8 | 0.001 (floor) |
| shared6 | 326 | 0.0 | 36 ± 4 | 0.001 (floor) |
| specpeak | 110.7 | 111.4 ± 1.6 | 109.7 ± 1.3 | 0.22 |

**Verdict: the rhythm idea SURVIVES in block form and DIES in frequency form.**
- Tandem repeats: about 13 sd above B1.
- Shared 5- and 6-grams: about 28 and 67 sd above B1.
- The conjugation periodogram shows nothing (p 0.22). There is no steady beat, only reused blocks.
- Shared 4-grams are fully explained by pairs, so macros matter at length 5 and up.

## What the blocks are
- **Top tandem blocks:** [4,4] (r1·=r0 twice), [4,3], [9,9], [13,4]/[4,13]/[12,4]. These are conjugate-then-multiply units. [4,3] has ledger [[0,-1],[1,1]], a finite-order element of GL2(Z), so repeating it cycles the ledger.
- **Top shared 6-grams:** the core is `4,·,2,5,2`: r1·=r0, r0·=r1, r1·=r0⁻¹, r0·=r1. It is spread over 20–43 different w values, so it is not one family repeating itself. [4,0,2,5,2,8] alone appears in 55 solutions.
- **Library:** `bob_macro_library_20260928.json` holds 977 macros (k = 3..8, ≥ 10 solutions, ≥ 5 distinct w), each with its ledger action.

## Limits (untested)
- Training rows are all Miller–Schupp presentations. Whether these macros help on the scored pool is **untested**.
- The real test is `acc_beam` with the top macros added as supermoves, on rows where the plain beam stalls, against the plain beam at matched state budget.
- Cross-solution sharing may partly reflect the tool that generated the training paths. Tandem repeats inside one solution do not depend on that.

## Scripts
### BOB-RHYTHM-01
```python
# SCRIPT: BOB-RHYTHM-01
# Move-rhythm test on the 424 official SAIR training solutions.
# Question: do solutions contain repeated macros (rhythm) beyond
#   (B0) their move composition, and
#   (B1) their adjacent-pair (doublet) structure?
# Kill condition (fixed before the run): if no statistic beats B1 at p < 0.01,
# the rhythm idea is dead beyond local adjacency rules.
import json, random, sys, math
from collections import Counter, defaultdict
import numpy as np

SAIR = '/home/claude/sair'
sys.path.insert(0, SAIR + '/competition/tools')
from verifier.core import apply_move, free_reduce

D = json.load(open(SAIR + '/competition/examples/training_424.json'))
INST = D['instances']
SEQS = [tuple(i['moves']) for i in INST]

# ---- control 0: every solution replays to the target under the official kernel
ok = 0
for i in INST:
    st = (free_reduce(tuple(i['initial_relators'][0])), free_reduce(tuple(i['initial_relators'][1])))
    for m in i['moves']:
        st = apply_move(st, m)
    ok += st == (tuple(i['target_relators'][0]), tuple(i['target_relators'][1]))
print('replay ok', ok, 'of', len(INST))

# ---- shufflers
def perm_shuffle(s, rng):
    s = list(s); rng.shuffle(s); return tuple(s)

def doublet_shuffle(s, rng):
    # Altschul-Erickson: uniform random sequence with the same first symbol and
    # the same multiset of adjacent pairs (random Eulerian trail, Wilson tree).
    n = len(s)
    if n < 3:
        return tuple(s)
    out = defaultdict(list)
    for a, b in zip(s, s[1:]):
        out[a].append(b)
    root = s[-1]
    verts = set(out) | {root}
    last = {}
    in_tree = {root}
    for v in verts:
        if v in in_tree or not out[v]:
            continue
        path = {}
        u = v
        while u not in in_tree:
            path[u] = rng.choice(out[u])
            u = path[u]
        u = v
        while u not in in_tree:
            last[u] = path[u]; in_tree.add(u); u = path[u]
    edges = {}
    for v, lst in out.items():
        lst = list(lst)
        if v in last:
            lst.remove(last[v]); rng.shuffle(lst); lst.append(last[v])
        else:
            rng.shuffle(lst)
        edges[v] = lst
    ptr = defaultdict(int)
    res = [s[0]]
    for _ in range(n - 1):
        v = res[-1]
        res.append(edges[v][ptr[v]]); ptr[v] += 1
    return tuple(res)

# ---- statistics
def tandem(s):
    # blocks of length k = 2..6 immediately repeated (u u)
    c = 0
    for k in range(2, 7):
        for i in range(len(s) - 2 * k + 1):
            if s[i:i + k] == s[i + k:i + 2 * k]:
                c += 1
    return c

def shared_grams(seqs, k, minsol=5):
    cnt = Counter()
    for s in seqs:
        cnt.update({s[i:i + k] for i in range(len(s) - k + 1)})
    return sum(1 for g, c in cnt.items() if c >= minsol)

def spec_peak(s):
    # largest periodogram ordinate of the conjugation indicator, as a share of total power
    x = np.array([1.0 if m >= 6 else 0.0 for m in s])
    if len(x) < 8 or x.std() == 0:
        return 0.0
    p = np.abs(np.fft.rfft(x - x.mean()))[1:] ** 2
    return float(p.max() / p.sum())

def stats(seqs):
    return {
        'tandem': sum(tandem(s) for s in seqs),
        'shared4': shared_grams(seqs, 4),
        'shared5': shared_grams(seqs, 5),
        'shared6': shared_grams(seqs, 6),
        'specpeak': sum(spec_peak(s) for s in seqs),
    }

def test(seqs, shuf, N, seed):
    rng = random.Random(seed)
    obs = stats(seqs)
    base = {k: [] for k in obs}
    for _ in range(N):
        b = stats([shuf(s, rng) for s in seqs])
        for k in obs:
            base[k].append(b[k])
    rows = {}
    for k in obs:
        arr = np.array(base[k], dtype=float)
        p_hi = (1 + (arr >= obs[k]).sum()) / (N + 1)
        p_lo = (1 + (arr <= obs[k]).sum()) / (N + 1)
        rows[k] = dict(obs=obs[k], mean=round(arr.mean(), 2), sd=round(arr.std(), 2), p_hi=round(p_hi, 4), p_lo=round(p_lo, 4))
    return rows

if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    # control 1: the doublet shuffle preserves first symbol and doublet multiset
    rng = random.Random(7)
    for s in SEQS:
        t = doublet_shuffle(s, rng)
        assert t[0] == s[0] and Counter(zip(s, s[1:])) == Counter(zip(t, t[1:])) and len(t) == len(s)
    print('doublet shuffle preserves pairs on all 424')
    # control 2 (positive): plant a tandem macro into every solution -> must beat B1
    rng = random.Random(11)
    planted = []
    for s in SEQS:
        i = rng.randrange(len(s) + 1)
        planted.append(s[:i] + (6, 2, 9, 4) * 3 + s[i:])
    # control 3 (negative): a pool drawn from B1 itself -> must NOT beat B1
    rng = random.Random(13)
    nullpool = [doublet_shuffle(s, rng) for s in SEQS]
    out = {}
    for name, pool in [('REAL', SEQS), ('POSCTRL_planted', planted), ('NEGCTRL_B1draw', nullpool)]:
        for bname, sh in [('B0_perm', perm_shuffle), ('B1_doublet', doublet_shuffle)]:
            r = test(pool, sh, N, 1)
            out[name + '|' + bname] = r
            print(name, bname)
            for k, v in r.items():
                print('   %-9s obs=%-8s base=%s+-%s  p_hi=%s  p_lo=%s' % (k, round(v['obs'], 2), v['mean'], v['sd'], v['p_hi'], v['p_lo']))
    json.dump(out, open('/home/claude/bob_rhythm/rhythm_results_v1.json', 'w'), indent=1)
```
### BOB-MACRO-MINE-01
```python
# SCRIPT: BOB-MACRO-MINE-01
# Which blocks make the rhythm? Tandem blocks and shared 6-grams in the 424
# training solutions, with how many distinct (n, w) instances use them and what
# each block does to the exponent-sum ledger M (inversions/multiplications act on M,
# conjugations do not).
import json
from collections import Counter, defaultdict
import numpy as np
D = json.load(open('/home/claude/sair/competition/examples/training_424.json'))
INST = D['instances']
def ledger_op(m):
    E = np.eye(2, dtype=int)
    if m == 0: E[0,0] = -1
    elif m == 1: E[1,1] = -1
    elif m == 2: E[0,1] = 1
    elif m == 3: E[0,1] = -1
    elif m == 4: E[1,0] = 1
    elif m == 5: E[1,0] = -1
    return E
def ledger(block):
    M = np.eye(2, dtype=int)
    for m in block: M = ledger_op(m) @ M
    return M.tolist()
NAME = {0:'inv r0',1:'inv r1',2:'r0*=r1',3:'r0*=r1^-1',4:'r1*=r0',5:'r1*=r0^-1',6:'r0^x',7:'r0^X',8:'r0^y',9:'r0^Y',10:'r1^x',11:'r1^X',12:'r1^y',13:'r1^Y'}
tand = Counter(); tand_inst = defaultdict(set)
for ins in INST:
    s = tuple(ins['moves'])
    for k in range(2, 7):
        for i in range(len(s) - 2*k + 1):
            if s[i:i+k] == s[i+k:i+2*k]:
                tand[s[i:i+k]] += 1; tand_inst[s[i:i+k]].add((ins['n'], ins['w']))
print('families (n,w) distinct:', len({(i['n'], i['w']) for i in INST}), ' distinct w:', len({i['w'] for i in INST}))
print('TOP TANDEM BLOCKS (block repeated back to back)')
for b, c in tand.most_common(15):
    print('  %-22s x%-4d in %3d instances  ledger %s  | %s' % (list(b), c, len(tand_inst[b]), ledger(b), ', '.join(NAME[m] for m in b)))
g6 = Counter(); g6w = defaultdict(set)
for ins in INST:
    s = tuple(ins['moves'])
    for g in {s[i:i+6] for i in range(len(s)-5)}:
        g6[g] += 1; g6w[g].add(ins['w'])
print('TOP SHARED 6-GRAMS (solutions containing it, distinct w)')
for b, c in g6.most_common(15):
    print('  %-22s %3d sols  %3d w  ledger %s | %s' % (list(b), c, len(g6w[b]), ledger(b), ', '.join(NAME[m] for m in b)))
```
### BOB-MACRO-LIBRARY-01
```python
# SCRIPT: BOB-MACRO-LIBRARY-01
# Export the macro library: shared k-grams (k=3..8) used by >= 10 training
# solutions across >= 5 distinct w, with ledger action and counts.
import json
from collections import Counter, defaultdict
exec(open('/home/claude/bob_rhythm/macro_mine_v1.py').read().split("tand = Counter()")[0])
lib = []
for k in range(3, 9):
    c = Counter(); ws = defaultdict(set)
    for ins in INST:
        s = tuple(ins['moves'])
        for g in {s[i:i+k] for i in range(len(s)-k+1)}:
            c[g] += 1; ws[g].add(ins['w'])
    for g, n in c.items():
        if n >= 10 and len(ws[g]) >= 5:
            lib.append(dict(moves=list(g), k=k, solutions=n, distinct_w=len(ws[g]), ledger=ledger(g)))
lib.sort(key=lambda r: (-r['k'] * r['solutions']))
json.dump(dict(source='SAIR competition/examples/training_424.json (sha256 4a607b16...)', rule='k=3..8, >=10 solutions, >=5 distinct w', count=len(lib), macros=lib), open('/home/claude/bob_rhythm/bob_macro_library_20260928.json', 'w'), indent=1)
print(len(lib), 'macros; by k:', Counter(r['k'] for r in lib))
```
