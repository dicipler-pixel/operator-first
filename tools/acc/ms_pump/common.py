import sys, json
S='/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad'
sys.path.insert(0, S+'/sair/competition/tools')
from verifier import core
R0 = (-2,-1,-2,-1,2,1)
def fr(w):
    o=[]
    for g in w:
        if o and o[-1]==-g: o.pop()
        else: o.append(g)
    return tuple(o)
INV0 = tuple(-g for g in reversed(R0))
def moves(r1):  # r1-only moves, r0 = R0 fixed; returns (move, new r1)
    yield 1, tuple(-g for g in reversed(r1))
    yield 4, fr(r1+R0)
    yield 5, fr(r1+INV0)
    for m,g in ((10,1),(11,-1),(12,2),(13,-2)):
        yield m, fr((g,)+r1+(-g,))
INVM = {1:1,4:5,5:4,10:11,11:10,12:13,13:12}
def tail(k): return [6,8,2,9,7,5,11]+[3]*(k-1)+[5]
def xyk(k): return (1,2)*k+(1,)
