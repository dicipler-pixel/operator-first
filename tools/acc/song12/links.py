import sys; sys.path.insert(0, '.'); from roadset import *
ROWS = ['ac-09632','ac-00764','ac-03320','ac-05538','ac-06036','ac-00738','ac-06611','ac-10099']
st = {r: (tuple(CODE[x] for x in MAN[r]['initial_relators'][0]), tuple(CODE[x] for x in MAN[r]['initial_relators'][1])) for r in ROWS}
for r in ROWS: print(r, ','.join(''.join('xXyY'[c] for c in w) for w in st[r]), len(st[r][0]) + len(st[r][1]))
img = {}
for r in ROWS:
    for k in range(16): img.setdefault(sym(st[r], k), []).append((r, k))
R = int(sys.argv[1]) if len(sys.argv) > 1 else 5
for r in ROWS:
    seen = {st[r]: []}; fr = [st[r]]
    for d in range(R):
        nf = []
        for s in fr:
            for m in range(14):
                t = move(s, m)
                if t is None or t in seen or len(t[0]) + len(t[1]) > 40: continue
                seen[t] = seen[s] + [m]; nf.append(t)
        fr = nf
    for t, p in seen.items():
        for (o, k) in img.get(t, []):
            if o != r: print('LINK', r, '->', o, 'sym', k, 'moves', p)
    print('#', r, 'ball', len(seen))
