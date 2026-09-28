"""Build the echo table for acc_capped (ECHO_FILE): states on or within R moves of our known routes for one row,
each with an upper bound on its remaining distance to (x, y) and the tail of moves that achieves it.
Routes: clean ac- lines in the repo (ACC_*.txt, live/*/sent, live/downloads), route maps
research/acc/optimality/*<row>*map*.json (key 'routes' -> 'move_ids'), and exact sweep jsonl (EXACT_JSONL).
Writes OUT.echo ("id dist l0 w.. l1 w..", letter codes 0=x 1=x^-1 2=y 3=y^-1) and OUT.tails.json {id: tail}.
Only states with 10 <= remaining <= MAXREM are kept (T9 already covers <= 9).
usage: build_echo.py MANIFEST ROW OUT_PREFIX R MAXREM"""
import glob, json, os, re, sys

MAN, ROW, OUT, R, MAXREM = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
GENS = (1, -1, 2, -2)
INV = {0: 0, 1: 1, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6, 8: 9, 9: 8, 10: 11, 11: 10, 12: 13, 13: 12}
E = {1: 0, -1: 1, 2: 2, -2: 3}


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


start = next(tuple(map(tuple, c['initial_relators'])) for c in json.load(open(MAN))['challenges'] if c['challenge_id'] == ROW)
routes = []
LINE = re.compile(r'^\s*(ac-\d{5})\s*:\s*\[([\d,\s]*)\]')
for f in glob.glob('ACC_*.txt') + glob.glob('research/acc/live/*/sent/*.txt') + glob.glob('research/acc/live/downloads/*.txt'):
    for l in open(f):
        m = LINE.match(l.split('#')[0])
        if m and m.group(1) == ROW:
            routes.append([int(x) for x in m.group(2).replace(' ', '').split(',') if x])
for f in glob.glob(f'research/acc/optimality/*{ROW}*map*.json'):
    for r in json.load(open(f)).get('routes', []):
        routes.append(r['move_ids'])
for jf in filter(None, os.environ.get('EXACT_JSONL', '').split(':')):
    for l in open(jf):
        r = json.loads(l)
        if r['id'] == ROW and r.get('ac'): routes.append(r['ac'])
best = {}                                   # state -> (remaining, tail moves)
nroutes = 0
for mv in {tuple(r) for r in routes}:
    s = start; st = [s]
    for m in mv: s = apply(s, m); st.append(s)
    if s != ((1,), (2,)): continue
    nroutes += 1
    L = len(mv)
    for i, si in enumerate(st):
        base = L - i
        if base - 0 < 10 - R: continue
        seen = {si: []}; front = [si]
        for k in range(0, R + 1):
            if k:
                nxt = []
                for x in front:
                    for m in range(14):
                        y = apply(x, m)
                        if y not in seen: seen[y] = seen[x] + [m]; nxt.append(y)
                front = nxt
            for x in front:
                rem = base + k
                if 10 <= rem <= MAXREM and (x not in best or rem < best[x][0]):
                    back = [INV[m] for m in reversed(seen[x])]          # x -> si
                    best[x] = (rem, back + list(mv[i:]))
tails = {}
with open(OUT + '.echo', 'w') as f:
    for n, (x, (rem, tail)) in enumerate(best.items()):
        f.write(f"{n} {rem} {len(x[0])} {' '.join(str(E[a]) for a in x[0])} {len(x[1])} {' '.join(str(E[a]) for a in x[1])}\n")
        tails[n] = tail
json.dump(tails, open(OUT + '.tails.json', 'w'))
print(f'{ROW}: {nroutes} verified routes, {len(best)} echo states (radius {R}, remaining 10..{MAXREM})')
