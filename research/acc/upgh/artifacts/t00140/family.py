"""Match MS(n,w) metadata rows to manifest challenges (up to cyclic permutation / inversion of each relator),
then print every n in the families of the six task rows with the matched challenge ids."""
import csv, json, re, sys
SAIR = '/root/.cache/upgh/sair'
man = json.load(open(SAIR + '/competition/tools/verifier/data/manifest.json'))
rows = list(csv.DictReader(open(SAIR + '/competition/tools/verifier/data/ms1190_metadata.csv')))
def red(w):
    out = []
    for a in w:
        if out and out[-1] == -a: out.pop()
        else: out.append(a)
    return tuple(out)
def variants(r):
    r = red(r); out = set()
    for w in (r, tuple(-a for a in reversed(r))):
        for i in range(len(w)): out.add(w[i:] + w[:i])
    return out
def key(rel): return min(variants(rel))
idx = {}
for c in man['challenges']:
    r0, r1 = c['initial_relators']
    idx.setdefault(frozenset([key(r0), key(r1)]), []).append(c['challenge_id'])
fam = {}
for r in rows:
    n = int(r['n']); w = [int(t) for t in r['w_vector'].split()]
    a = [-1] + [2] * n + [1] + [-2] * (n + 1); b = [-1] + w
    k = frozenset([key(a), key(b)])
    ids = idx.get(k, [])
    fam.setdefault(r['w'], []).append((n, r['training_id'], ids, r['prototype_path_length']))
want = sys.argv[1:] or ['ac-01432', 'ac-06752', 'ac-00183']
for w, lst in fam.items():
    if any(cid in ids for _, _, ids, _ in lst for cid in want):
        print('w =', w)
        for n, tid, ids, pl in sorted(lst): print('   n=%d %s proto=%s ids=%s' % (n, tid, pl, ids))
