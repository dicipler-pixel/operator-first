"""Direct-form training (T0,T1)=(X y^n x Y^(n+1), xxyyXYYY) -> challenge: r0 = (yinv T1)^-1, r1 = (yinv T0)^-1 exactly
(yinv = automorphism y -> y^-1).  Path: [0,1] + swap(yinv(moves)) + [2,5,2,8] (end (Y,x) -> (x,y) per the spec table)."""
from fam import *
YINV = {8: 9, 9: 8, 12: 13, 13: 12}
def yinv_moves(ms): return [YINV.get(m, m) for m in ms]
def mapped_direct(ms): return [0, 1] + swap(yinv_moves(ms)) + [2, 5, 2, 8]
for n, tid in sorted(DIRECT.items()):
    t = TRID[tid]; p = mapped_direct(t['moves']); v = verify(synth(n), p)
    print(f'direct n={n} {tid}: train {len(t["moves"])} -> mapped {len(p)} ok={v["ok"]} len={v.get("length")} peak={v.get("peak_total_relator_length")}')
# replay the direct n=6 (100) and n=3 (14) move lists on the n=4 / n=5 official rows via the same mapping prefix
for n, cid in ((4, 'ac-09632'), (5, 'ac-05538')):
    for an in (3, 6):
        ms = [0, 1] + swap(yinv_moves(TRID[DIRECT[an]]['moves']))
        st = states(CH[cid]['initial_relators'], ms); tots = [tot(s) for s in st]
        bi = min(range(len(tots)), key=lambda i: tots[i])
        print(f'{cid} <- direct n={an} list: min tot {tots[bi]} at step {bi} ({w(st[bi][0])} | {w(st[bi][1])}), end tot {tots[-1]}')
        print('   totals:', ' '.join(map(str, tots[:40])), '...' if len(tots) > 40 else '')
