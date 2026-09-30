# BFS from start, all 14 moves, total-length cap; report states with few x-letters. usage: bfs.py CID DEPTH CAP [r0only]
from lib import *
import sys
cid,D,CAP=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]); r0only=len(sys.argv)>4
s0,_=st(cid); MV=[0,2,3,6,7,8,9] if r0only else range(14)
nx=lambda t:sum(1 for a in t if abs(a)==1)
P={s0:[]}; fr=[s0]; best={}
for d in range(D):
    nf=[]
    for s in fr:
        for m in MV:
            y=core.apply_move(s,m)
            if y in P or len(y[0])+len(y[1])>CAP: continue
            P[y]=P[s]+[m]; nf.append(y)
            k=(nx(y[0]),nx(y[1]))
            if min(k)<=1 and (k not in best or len(P[y])<len(best[k][0])): best[k]=(P[y],y)
    fr=nf; print('d',d+1,'frontier',len(nf),'states',len(P),flush=True)
for k,(p,y) in sorted(best.items()): print('X-count',k,'len',len(p),p,S(y[0]),S(y[1]))
