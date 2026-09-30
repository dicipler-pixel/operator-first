"""Collect routes exactly like research/acc/optimality/build_echo.py (run from the repo root, EXACT_JSONL honoured), replay them,
and write unique route states (min remaining) for echo_ball.c:  OUT.src (b l0 w.. l1 w..) and OUT.srcmap.json."""
import sys, os, json
sys.argv = ['x'] + sys.argv[1:4] + ['0', sys.argv[4]]       # MANIFEST ROW OUT MAXREM
src = open('research/acc/optimality/build_echo.py').read().split("best = {}")[0]
exec(src)                                                     # defines start, routes, apply, E, INV ...
uniq = {}; allroutes = []
for mv in sorted({tuple(r) for r in routes}):
    s = start; st = [s]
    for m in mv: s = apply(s, m); st.append(s)
    if s != ((1,), (2,)): continue
    ri = len(allroutes); allroutes.append(list(mv)); L = len(mv)
    for i, si in enumerate(st):
        b = L - i
        if b > MAXREM: continue
        if si not in uniq or b < uniq[si][0]: uniq[si] = (b, ri, i)
order = sorted(uniq.items(), key=lambda kv: (kv[1][0], kv[1][1]))
with open(OUT + '.src', 'w') as f:
    for x, (b, ri, i) in order:
        f.write(f"{b} {len(x[0])} {' '.join(str(E[a]) for a in x[0])} {len(x[1])} {' '.join(str(E[a]) for a in x[1])}\n")
json.dump({'routes': allroutes, 'sources': [[b, ri, i] for x, (b, ri, i) in order]}, open(OUT + '.srcmap.json', 'w'))
print(f"{len(allroutes)} verified routes, {len(order)} unique route states with remaining <= {MAXREM}")
