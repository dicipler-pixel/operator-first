# Row-op geometry of a chain level: rows = exponent-sum vectors of (r0, r1).
# Moves: r1 += +-r0 (E21), r0 += +-r1 (E12); inversions (row sign) and conjugations are free here.
# Count shortest row-op words taking M0=[[-1,0],[a-1,-1]] to M1=[[-1,0],[2a-1,-1]] up to row signs.
from collections import deque
def canon(M):
    (a,b),(c,d)=M
    if (a,b)<(0,0) or (a==0 and b<0) : a,b=-a,-b
    if (c,d)<(0,0) or (c==0 and d<0): c,d=-c,-d
    return ((a,b),(c,d))
def nbrs(M):
    (a,b),(c,d)=M
    for s in (1,-1):
        yield ('r1+%dr0'%s, canon(((a,b),(c+s*a,d+s*b))))
        yield ('r0+%dr1'%s, canon(((a+s*c,b+s*d),(c,d))))
for a in (1,2,3,4,6,8):
    src=canon(((-1,0),(a-1,-1))); dst=canon(((-1,0),(2*a-1,-1)))
    dist={src:0}; cnt={src:1}; q=deque([src]); B=60
    while q:
        M=q.popleft()
        if dist[M]>=a+3: continue
        for _,N in nbrs(M):
            if max(abs(v) for r in N for v in r)>B: continue
            if N not in dist: dist[N]=dist[M]+1; cnt[N]=cnt[M]; q.append(N)
            elif dist[N]==dist[M]+1: cnt[N]+=cnt[M]
    print('a=%d level: min row-ops %s, #geodesic words %s'%(a,dist.get(dst),cnt.get(dst)))
