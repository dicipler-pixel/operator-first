"""Bob's fallback, bounded: BFS from the official start over all 14 moves, total length <= CAP, depth <= D,
state budget N; flag states where a relator has exactly one x-letter (|r|_x = 1), i.e. x = y^k.
usage: onex_bfs.py ROW CAP D N"""
import sys, time; from fam import *
row, CAP, D, N = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
s0 = tuple(tuple(r) for r in CH[row]['initial_relators'])
def nx(r): return sum(1 for t in r if abs(t) == 1)
seen = {s0: 0}; frontier = [s0]; hits = []; t0 = time.time(); d = 0
while frontier and d < D and len(seen) < N:
    d += 1; nxt = []
    for s in frontier:
        for m in range(14):
            t = core.apply_move(s, m)
            if len(t[0]) + len(t[1]) > CAP or t in seen: continue
            seen[t] = d; nxt.append(t)
            if nx(t[0]) == 1 or nx(t[1]) == 1: hits.append((d, t))
    frontier = nxt
    print(f'd={d} new={len(nxt)} total={len(seen)} onex_hits={len(hits)} {time.time()-t0:.0f}s', flush=True)
hits.sort(key=lambda h: (tot(h[1]), h[0]))
for d, t in hits[:40]: print(f'  depth {d} tot {tot(t)}: {w(t[0])} | {w(t[1])}')
print('ended:', 'frontier empty (closed)' if not frontier else ('depth limit' if d >= D else 'state budget'))
