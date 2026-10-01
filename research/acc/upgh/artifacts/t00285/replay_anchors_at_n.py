"""Replay each twin anchor's move list on the training-frame start for n=4,5; report divergence from the
anchor's own trace (first step where the state differs modulo the n-dependent y-runs), total profile, best states."""
import sys; from fam import *
def tstart(n): return [[-1]+[2]*n+[1]+[-2]*(n+1), [1,-2,-2,-1,2,2,2,1]]
def ylen_free(word):  # word with maximal y-runs compressed to a single sign marker (to compare shapes across n)
    out=[]; 
    for t in word:
        if abs(t)==2 and out and out[-1]==t: continue
        out.append(t)
    return tuple(out)
for n in (4,5):
    for an, tid in sorted(TWIN.items()):
        t = TRID[tid]; mv = t['moves']
        sa = states(t['initial_relators'], mv); sn = states(tstart(n), mv)
        div = next((i for i,(a,b) in enumerate(zip(sa,sn)) if (ylen_free(a[0]),ylen_free(a[1]))!=(ylen_free(b[0]),ylen_free(b[1]))), None)
        tots = [tot(s) for s in sn]; bi = min(range(len(tots)), key=lambda i: tots[i])
        print(f'n={n} anchor n={an} {tid} len={len(mv)}: shape-divergence at step {div}; end=({w(sn[-1][0])},{w(sn[-1][1])}) tot {tots[-1]}; min tot {tots[bi]} at step {bi}: ({w(sn[bi][0])},{w(sn[bi][1])})')
        print('   totals:', ' '.join(map(str,tots)))
