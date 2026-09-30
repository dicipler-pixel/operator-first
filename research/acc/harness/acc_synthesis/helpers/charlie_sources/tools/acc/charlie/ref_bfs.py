# SCRIPT: ACC_REF_BFS -- plain in-memory BFS with the official kernel, for controls
import os, sys
sys.path.insert(0,os.environ.get('SAIR_TOOLS', os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SAIR/competition/tools'))))
from verifier import core
def comp(start,cap):
    seen={start}; fr=[start]; sizes=[1]
    while fr:
        nf=[]
        for s in fr:
            for m in range(14):
                t=core.apply_move(s,m)
                if len(t[0])+len(t[1])<=cap and t not in seen: seen.add(t); nf.append(t)
        fr=nf
        if nf: sizes.append(len(nf))
    return len(seen),sizes
if __name__=='__main__':
    for cap in (4,6,8):
        n,s=comp(((1,),(2,)),cap); print('trivial cap',cap,'component',n,'layers',s)
