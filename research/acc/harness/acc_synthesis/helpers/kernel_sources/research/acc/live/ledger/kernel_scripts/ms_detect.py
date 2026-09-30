# SCRIPT: KERNEL-MS-DETECT-01
# For each row, search small Nielsen automorphisms psi (images of x, y as short words)
# such that psi(row relators) contains a Baumslag-Solitar/Miller-Schupp relator
# x^-1 y^n x y^-(n+1) up to cyclic permutation and inversion. Reports n and the
# other relator (the "w" side) in those coordinates.
import json, itertools
def red(w):
    o=[]
    for a in w:
        if o and o[-1]==-a: o.pop()
        else: o.append(a)
    return o
def cred(w):
    w=red(w)
    while len(w)>1 and w[0]==-w[-1]: w=w[1:-1]
    return w
def inv(w): return [-a for a in reversed(w)]
def cyc_forms(w):
    w=cred(w); out=set()
    for v in (w, inv(w)):
        for i in range(max(1,len(v))): out.add(tuple(v[i:]+v[:i]))
    return out
def sub(w, img):  # img: {1:word,2:word}
    o=[]
    for a in w: o += img[abs(a)] if a>0 else inv(img[abs(a)])
    return red(o)
BS={}
for n in range(1,12):
    for f in cyc_forms([-1]+[2]*n+[1]+[-2]*(n+1)): BS[f]=n
# candidate automorphisms: images of x and y as words of length <= 3 that form a basis
words=[]
for L in range(1,4):
    for t in itertools.product([1,-1,2,-2],repeat=L):
        if red(list(t))==list(t): words.append(list(t))
def is_basis(a,b):
    # abelianization det +-1 is necessary; test Nielsen reduction to {x,y}
    import numpy as np
    ea=[sum(1 for c in a if c==1)-sum(1 for c in a if c==-1), sum(1 for c in a if c==2)-sum(1 for c in a if c==-2)]
    eb=[sum(1 for c in b if c==1)-sum(1 for c in b if c==-1), sum(1 for c in b if c==2)-sum(1 for c in b if c==-2)]
    if abs(ea[0]*eb[1]-ea[1]*eb[0])!=1: return False
    S=[a,b]
    for _ in range(40):
        if sorted(map(len,S))==[1,1]: return {abs(S[0][0]),abs(S[1][0])}=={1,2}
        best=None
        for i in range(2):
            for j in range(2):
                if i==j: continue
                for v in (S[j],inv(S[j])):
                    for side in (0,1):
                        n=red(v+S[i]) if side==0 else red(S[i]+v)
                        if len(n)<len(S[i]) and (best is None or len(n)<best[0]): best=(len(n),i,n)
        if best is None: return False
        S[best[1]]=best[2]
    return False
autos=[(a,b) for a in words for b in words if is_basis(a,b)]
rows=json.load(open('rows_101_213.json'))
res=[]
for r in rows:
    found=None
    for a,b in autos:
        img={1:a,2:b}
        R=[cred(sub(r['rel'][0],img)), cred(sub(r['rel'][1],img))]
        for k in (0,1):
            n=BS.get(tuple(R[k]))
            if n is not None:
                o=R[1-k]
                if found is None or len(o)<len(found[3]): found=(a,b,n,o,k)
    res.append(dict(row=r['row'],id=r['id'],auto=found and [found[0],found[1]],n=found and found[2],other=found and found[3],bs_index=found and found[4]))
json.dump(res,open('ms_detect.json','w'))
hit=[x for x in res if x['n']]
print('autos tried',len(autos),'rows with MS relator',len(hit),'of',len(res))
from collections import Counter
print(Counter(x['n'] for x in hit))
for x in hit[:6]: print(x)
