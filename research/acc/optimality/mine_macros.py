"""Schur elimination of the hump, step 1: mine "excursions" (macro-moves).
An excursion is a segment of a known AC path, 2..KMAX moves long, whose interior climbs above both
endpoints (total relator length) and comes back down. Eliminating those interior (hidden) states and
keeping only the endpoint-to-endpoint effect is the Schur-complement idea (atlas UPG-FEEDBACK). Every
excursion is expanded by the 16 symmetries of the move set (generator swap, generator inversions,
relator swap), which map the 14 moves onto themselves.
usage: mine_macros.py MANIFEST OUT.txt TOP [EXCLUDE_ROW ...]   -> one macro per line: "count: m1 m2 ..."
Paths: every clean ac- line in the repo's ACC_*.txt, live/*/sent/*.txt and downloads/*.txt, plus
exact sweep paths in the scratch work dir if given via EXACT_JSONL (colon separated)."""
import collections, glob, itertools, json, os, sys

MAN, OUT, TOP = sys.argv[1], sys.argv[2], int(sys.argv[3])
EXCL = set(sys.argv[4:])
KMAX = int(os.environ.get('KMAX', '6'))
GENS = (1, -1, 2, -2)


def red(w):
    o = []
    for a in w:
        if o and o[-1] == -a: o.pop()
        else: o.append(a)
    return tuple(o)


def inv(w): return tuple(-a for a in reversed(w))


def apply(s, m):
    r0, r1 = s
    if m == 0: return (inv(r0), r1)
    if m == 1: return (r0, inv(r1))
    if m == 2: return (red(r0 + r1), r1)
    if m == 3: return (red(r0 + inv(r1)), r1)
    if m == 4: return (r0, red(r1 + r0))
    if m == 5: return (r0, red(r1 + inv(r0)))
    if m <= 9: g = GENS[m - 6]; return (red((g,) + r0 + (-g,)), r1)
    g = GENS[m - 10]; return (r0, red((g,) + r1 + (-g,)))


SIG = {6: 8, 8: 6, 7: 9, 9: 7, 10: 12, 12: 10, 11: 13, 13: 11}           # swap x <-> y
TX = {6: 7, 7: 6, 10: 11, 11: 10}                                        # x -> x^-1
TY = {8: 9, 9: 8, 12: 13, 13: 12}                                        # y -> y^-1
RHO = {0: 1, 1: 0, 2: 4, 4: 2, 3: 5, 5: 3, 6: 10, 10: 6, 7: 11, 11: 7, 8: 12, 12: 8, 9: 13, 13: 9}
SYMS = []
for sg, tx, ty, rh in itertools.product((0, 1), repeat=4):
    def f(m, sg=sg, tx=tx, ty=ty, rh=rh):
        if tx: m = TX.get(m, m)
        if ty: m = TY.get(m, m)
        if sg: m = SIG.get(m, m)
        if rh: m = RHO.get(m, m)
        return m
    SYMS.append(f)

LINE = __import__('re').compile(r'^\s*(ac-\d{5})\s*:\s*\[([\d,\s]*)\]')
man = {c['challenge_id']: tuple(map(tuple, c['initial_relators'])) for c in json.load(open(MAN))['challenges']}
paths = {}
for f in glob.glob('ACC_*.txt') + glob.glob('research/acc/live/*/sent/*.txt') + glob.glob('research/acc/live/downloads/*.txt'):
    for l in open(f):
        m = LINE.match(l.split('#')[0])
        if m and m.group(1) not in EXCL:
            mv = [int(x) for x in m.group(2).replace(' ', '').split(',') if x]
            if m.group(1) not in paths or len(mv) < len(paths[m.group(1)]): paths[m.group(1)] = mv
for jf in filter(None, os.environ.get('EXACT_JSONL', '').split(':')):
    for l in open(jf):
        r = json.loads(l)
        if r.get('ac') and r['id'] not in EXCL: paths[r['id']] = r['ac']

count = collections.Counter(); used = 0
for cid, mv in paths.items():
    s = man[cid]; st = [s]
    for m in mv: s = apply(s, m); st.append(s)
    if s != ((1,), (2,)): continue
    used += 1
    L = [len(a) + len(b) for a, b in st]
    for i in range(len(mv)):
        for k in range(2, KMAX + 1):
            j = i + k
            if j > len(mv): break
            if max(L[i + 1:j]) > max(L[i], L[j]):            # climbs above both ends, then comes back
                seg = tuple(mv[i:j])
                for f in SYMS: count[tuple(f(m) for m in seg)] += 1
top = count.most_common(TOP)
with open(OUT, 'w') as fh:
    for seg, c in top: fh.write(f"{c}: {' '.join(map(str, seg))}\n")
print(f'{used} paths, {len(count)} distinct excursions (with symmetries); top {len(top)} written to {OUT}')
