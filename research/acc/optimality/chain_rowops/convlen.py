# How many consecutive r1<-r1*r0^e moves (no conjugation between) can do useful work?
# Enumerate r0 = conjugates of BS^{+-1} by words w (|w|<=L) and r1 = chain-level word, and see whether
# a run r1*r0^e1*r0^e2... (same r0) can shorten/transform; i.e. measure max #mults per conjugation budget
# by exact search restricted to: conj moves on r0 only at the start (prefix), then only mults of r1.
from acmoves import red, inv
BS='YXXyx'
def conjw(w,r): return red(w+r+inv(w))
import itertools
best=[]
for a in (2,3,4):
    r1=red('YY'+'X'+'y'+'x'*a)   # level k=2 state Y^2 X y x^a
    target_x=2*a
    res=[]
    for L in range(0,5):
        for w in itertools.product('xXyY',repeat=L):
            w=''.join(w)
            if red(w)!=w: continue
            for base in (BS,inv(BS)):
                r0=conjw(w,base)
                cur=r1; seq=[]
                for j in range(2*a+2):
                    for e,rr in ((1,r0),(-1,inv(r0))):
                        pass
                # greedy: apply r1*r0^s repeatedly while it shortens or keeps length
                for s in (1,-1):
                    cur=r1; steps=0; lens=[len(cur)]
                    for j in range(3*a):
                        cur=red(cur+(r0 if s==1 else inv(r0))); steps+=1; lens.append(len(cur))
                    res.append((min(lens[1:]),w,base,s,lens[:8]))
    res.sort()
    print('a',a,'r1',r1,'best min lens after pure mults:',res[:3])
