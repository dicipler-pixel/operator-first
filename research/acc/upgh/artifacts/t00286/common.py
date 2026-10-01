# Local shim for tools/acc/ms_pump/common.py: point at the pinned verifier (~/.cache/upgh/sair).
import sys, os
sys.path.insert(0, os.path.expanduser('~/.cache/upgh/sair/competition/tools'))
from verifier import core
R0 = (-2,-1,-2,-1,2,1)
def fr(w):
    o=[]
    for g in w:
        if o and o[-1]==-g: o.pop()
        else: o.append(g)
    return tuple(o)
