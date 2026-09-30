# For each MS(n,w) row: does some y-run of w (cyclically) sit in the orientation the MS rewrite needs?
# rules: X y^L x -> y^(L+1) needs L==n ; x y^L X -> y^(L-1) needs L==n+1 (same for Y-runs)
from lib import *
import re,json
def ms(c):
    a,b=st(c)[0]
    for r0,r1 in ((a,b),(b,a)):
        m=re.fullmatch(r'(Y+)X(y+)x',S(r1))
        if m and len(m.group(1))==len(m.group(2))+1: return len(m.group(2)),S(r0)
def runs(w):
    n=len(w); out=[]; i=0
    # cyclic maximal runs of y/Y
    ww=w+w
    seen=set()
    for i in range(n):
        if ww[i].lower()!='y' or ww[i-1]==ww[i]: continue
        j=i
        while j<i+n and ww[j]==ww[i]: j+=1
        L=j-i; a=ww[i-1]; b=ww[j%(2*n)] if j<2*n else ww[j-n]
        if (i%n) in seen: continue
        seen.add(i%n); out.append((L,a,b))
    return out
def cls(n,w):
    tags=[]
    for L,a,b in runs(w):
        if a.lower()=='x' and b.lower()=='x':
            if (a,b)==('X','x') and L==n: tags.append(f'X{L}x=n')
            if (a,b)==('x','X') and L==n+1: tags.append(f'x{L}X=n+1')
            if (a,b)==('X','x') and L==n+1: tags.append(f'X{L}x=n+1(wrong)')
            if (a,b)==('x','X') and L==n: tags.append(f'x{L}X=n(wrong)')
    return tags
soft=json.load(open('/tmp/claude-0/-home-user-operator-first/644f7765-aca6-5d39-980a-3e4ddc6288c0/scratchpad/fable_zoom/soft_unsolved.json'))
softids={r[0] for r in soft}
# family map: w -> {n: cid}
fam={}
for c in CH:
    if c.startswith('sac'): continue
    r=ms(c)
    if r: fam.setdefault(r[1],{})[r[0]]=c
good_un=0; wrong_un=0; rows=[]
for cid,n,w,_,sibs in soft:
    t=cls(n,w); rows.append((cid,n,w,t))
    if any('wrong' not in x for x in t): good_un+=1
    else: wrong_un+=1
print('unsolved y-run rows: right-orientation',good_un,'wrong-only',wrong_un)
for cid,n,w,t in rows[:37]: print(cid,n,w,t)
# solved siblings of the first 37: orientation at their n
print('--- solved siblings (first 37 rows)')
for cid,n,w,_,sibs in soft[:37]:
    for sn,rec,k in sibs:
        sc=fam.get(w,{}).get(sn); print(' ',cid,'sib',sc,'n',sn,'rec',rec,'k',k,cls(sn,w))
