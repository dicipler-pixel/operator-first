#!/usr/bin/env python3
"""Independent free-group equational certificate; NOT an AC move route."""
import hashlib,json,sys,time,resource
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(192*1024**2,192*1024**2))
resource.setrlimit(resource.RLIMIT_CPU,(10,10))
root=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(root))
from official_checker import load_kernel,render
core,_,pins,_=load_kernel()
mp=root/'integration/repo/official_manifest.json'
assert hashlib.sha256(mp.read_bytes()).hexdigest()==pins['source_manifest_sha256']
manifest=json.loads(mp.read_text())
row=next(c for c in manifest['challenges'] if c['challenge_id']=='ac-07824')
rels=[tuple(w) for w in row['initial_relators']]
def red(w):
    out=[]
    for a in w:
        if out and out[-1]==-a:out.pop()
        else:out.append(a)
    return tuple(out)
def inv(w):return tuple(-x for x in reversed(w))
def word(s):return tuple({'x':1,'X':-1,'y':2,'Y':-2}[a] for a in s)
nodes=[]
def add(rule,l,r,parents=(),**data):
    nodes.append({'rule':rule,'left':list(red(l)),'right':list(red(r)),'parents':list(parents),**data})
    return len(nodes)-1
def L(i):return tuple(nodes[i]['left'])
def R(i):return tuple(nodes[i]['right'])
def ax(i,l,r):return add('axiom',word(l),word(r),relator=i)
def refl(w):return add('refl',w,w)
def sym(i):return add('sym',R(i),L(i),(i,))
def inverse(i):return add('inverse',inv(L(i)),inv(R(i)),(i,))
def product(i,j):return add('product',L(i)+L(j),R(i)+R(j),(i,j))
def chain(i,j):
    assert R(i)==L(j),(i,j)
    return add('transitive',L(i),R(j),(i,j))
def power(i,n):
    out=refl(())
    for _ in range(n):out=product(out,i)
    return out
def conjugate(i,w):return product(product(refl(w),i),refl(inv(w)))
def cyclic_forms(w):
    w=red(w)
    while len(w)>1 and w[0]==-w[-1]:w=w[1:-1]
    return {v[k:]+v[:k] for v in (w,inv(w)) for k in range(len(v))}

# Exact consequences of the two pinned relators.
A=ax(0,'Xyyx','yyy')
B=ax(1,'Yxxxxy','xxxxx')
B4=power(B,4)                        # T(x^16)=x^20
B5=power(B,5)                        # T(x^20)=x^25
T2=chain(conjugate(B4,word('Y')),B5)  # T^2(x^16)=x^25
frame=product(product(sym(inverse(A)),refl(word('x'*16))),sym(A))
T3=chain(frame,conjugate(T2,word('X'))) # T^3(x^16)=x^25
fixed=conjugate(chain(T3,sym(T2)),word('yy')) # T(x^16)=x^16
four=product(chain(sym(B4),fixed),refl(word('X'*16))) # x^4=1
five=chain(sym(B),conjugate(four,word('Y'))) # x^5=1
xproof=product(five,inverse(four))     # x=1
collapsed=product(product(inverse(xproof),refl(word('yy'))),xproof)
yproof=sym(product(refl(word('YY')),chain(sym(collapsed),A)))
assert (L(xproof),R(xproof))==((1,),())
assert (L(yproof),R(yproof))==((2,),())

# Replay certificate from scratch, trusting only axioms from pinned relators.
checked=[]
for i,n in enumerate(nodes):
    l,r=tuple(n['left']),tuple(n['right']);p=n['parents'];rule=n['rule']
    assert all(0<=j<i for j in p)
    if rule=='axiom':assert red(l+inv(r)) in cyclic_forms(rels[n['relator']])
    elif rule=='refl':assert l==r
    elif rule=='sym':assert (l,r)==checked[p[0]][::-1]
    elif rule=='inverse':assert (l,r)==tuple(inv(w) for w in checked[p[0]])
    elif rule=='product':assert (l,r)==tuple(red(checked[p[0]][k]+checked[p[1]][k]) for k in (0,1))
    elif rule=='transitive':
        a,b=checked[p[0]],checked[p[1]];assert a[1]==b[0] and (l,r)==(a[0],b[1])
    else:raise AssertionError(rule)
    checked.append((l,r))
out={'scope':'Group triviality only, not an AC or Stable AC route','row_id':'ac-07824',
     'instance_hash':row['instance_hash'],'manifest_sha256':pins['source_manifest_sha256'],
     'checker_core_sha256':hashlib.sha256((root/'vendor/verifier/core.py').read_bytes()).hexdigest(),
     'checked_nodes':len(nodes),'generator_conclusions':{'x':xproof,'y':yproof},
     'peak_equational_word_length':max(len(n[k]) for n in nodes for k in ('left','right')),
     'nodes':nodes,'passed':True,'solver_route':None}
Path(__file__).with_name('group_proof_certificate.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='nodes'}))
