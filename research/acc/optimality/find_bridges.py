"""Find short AC bridges between benchmark starts: pairs (A, B) with d(start A, start B) <= R.
A path for B then gives a path for A of length <= R + len(path B). Moves are invertible, so one BFS
of radius R from each start, looked up in a hash of all starts, finds every pair.
Output JSONL: {"a", "b", "d", "moves_a_to_b"}  (moves use our own kernel; any transported line must
still pass the official verifier before it is sent).
usage: find_bridges.py MANIFEST R OUT.jsonl"""
import json, sys

MAN, R, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3]


def red(w):
    out = []
    for a in w:
        if out and out[-1] == -a:
            out.pop()
        else:
            out.append(a)
    return tuple(out)


def inv(w):
    return tuple(-a for a in reversed(w))


CONJ = (1, -1, 2, -2)


def moves(s):
    r0, r1 = s
    yield 0, (inv(r0), r1)
    yield 1, (r0, inv(r1))
    yield 2, (red(r0 + r1), r1)
    yield 3, (red(r0 + inv(r1)), r1)
    yield 4, (r0, red(r1 + r0))
    yield 5, (r0, red(r1 + inv(r0)))
    for j, c in enumerate(CONJ):
        yield 6 + j, (red((c,) + r0 + (-c,)), r1)
    for j, c in enumerate(CONJ):
        yield 10 + j, (r0, red((c,) + r1 + (-c,)))


ch = [c for c in json.load(open(MAN))['challenges'] if c['challenge_id'].startswith('ac-')]
starts = {}
for c in ch:
    starts.setdefault(tuple(map(tuple, c['initial_relators'])), []).append(c['challenge_id'])

found = 0
with open(OUT, 'w') as f:
    for n, c in enumerate(ch):
        a = c['challenge_id']
        s0 = tuple(map(tuple, c['initial_relators']))
        seen = {s0: ()}
        frontier = [s0]
        for d in range(1, R + 1):
            nxt = []
            for s in frontier:
                path = seen[s]
                for m, t in moves(s):
                    if t in seen:
                        continue
                    seen[t] = path + (m,)
                    nxt.append(t)
                    for b in starts.get(t, ()):
                        if b != a:
                            f.write(json.dumps({'a': a, 'b': b, 'd': d, 'moves_a_to_b': list(seen[t])}) + '\n')
                            found += 1
            frontier = nxt
        if n % 500 == 0:
            print(n, 'starts done,', found, 'bridges', flush=True)
print('done', found, 'bridges')
