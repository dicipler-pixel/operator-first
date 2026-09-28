# Find competition rows AC-equivalent-by-symmetry to Lisitsa MS_n(w*) = (X y^n x Y^(n+1), XYxyX)
import os
import json,itertools
m=json.load(open(os.environ.get('SAIR','sair')+'/competition/tools/verifier/data/manifest.json'))
L={1:'x',-1:'X',2:'y',-2:'Y'}
def w(r): return ''.join(L[i] for i in r)
def red(s):
    o=[]
    for c in s:
        if o and o[-1]==c.swapcase(): o.pop()
        else:o.append(c)
    return ''.join(o)
def cred(s):
    s=red(s)
    while len(s)>1 and s[0]==s[-1].swapcase(): s=s[1:-1]
    return s
def inv(s): return s.swapcase()[::-1]
def canon(s):
    s=cred(s); c=[]
    for t in (s,inv(s)):
        c+= [t[i:]+t[:i] for i in range(len(t))]
    return min(c)
maps=[]
for sx in 'xXyY':
    for sy in 'xXyY':
        if sx.lower()==sy.lower(): continue
        maps.append({'x':sx,'X':sx.swapcase(),'y':sy,'Y':sy.swapcase()})
def key(a,b):
    ks=[]
    for mp in maps:
        A=canon(''.join(mp[c] for c in a)); B=canon(''.join(mp[c] for c in b))
        ks.append(tuple(sorted((A,B))))
    return min(ks)
target={}
for n in range(1,12):
    target[key('X'+'y'*n+'x'+'Y'*(n+1),'XYxyX')]=n
hits=[]
for ch in m['challenges']:
    a,b=[w(r) for r in ch['initial_relators']]
    if len(a)+len(b)>40: continue
    k=key(a,b)
    if k in target: hits.append((ch['challenge_id'],target[k],a,b))
for h in hits: print(*h)
print(len(hits),'hits')
