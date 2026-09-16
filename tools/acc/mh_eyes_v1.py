"""Mad Hatters ACC eyes, v1.  Append-only readings; no eye votes.

Recovered by inverse replay from the target under the frozen verifier
(a0fd6e6): the Gordon controls are G(q) = (x^-2 y^-1 x y, y^-2 x^-q y x^q).
Both control and target families are EXPONENT_PAIR instances:

    Gordon   x^-q y x^q = y^2        (a,b) = (1,2),  u = x^-q
    R_q      x y^q x^-1 = y^(q+1)    (a,b) = (q,q+1), u = x

so the structural task is Euclidean: carry (q,q+1) to a pair with a unit.
"""
import sys
sys.path.insert(0,'/home/user/saircompetition/andrews-curtis/competition/tools')
from verifier import core

LET={'x':1,'X':-1,'y':2,'Y':-2}
SYM={1:'x',-1:'X',2:'y',-2:'Y'}
TARGET=((1,),(2,))

def W(s): return core.free_reduce([LET[c] for c in s])
def P(a,b): return (tuple(W(a)),tuple(W(b)))
def unstr(w): return "".join(SYM[c] for c in w)
def tot(s): return sum(len(w) for w in s)

def runs(w):
    """maximal same-generator runs as (gen, exponent)"""
    out=[]
    for c in w:
        g=abs(c); e=1 if c>0 else -1
        if out and out[-1][0]==g: out[-1][1]+=e
        else: out.append([g,e])
    return [(g,e) for g,e in out if e!=0]

def cyc_rots(w):
    w=list(w)
    while len(w)>=2 and w[0]==-w[-1]: w=w[1:-1]
    return [tuple(w[i:]+w[:i]) for i in range(len(w))] if w else [()]

def exponent_pair(w):
    """EXPONENT_PAIR: u^-1 v^a u = v^b with u a power of the other generator.
    Returns (v, a, b, u_exp) for the best rotation, else None."""
    best=None
    for r in cyc_rots(w):
        rs=runs(r)
        if len(rs)!=4: continue
        (g0,e0),(g1,e1),(g2,e2),(g3,e3)=rs
        if g0==g2 and g1==g3 and g0!=g1 and e0==-e2:
            v,a,b,ue=g1,e1,-e3,e0
            cand=(v,a,b,ue)
            if best is None or abs(a)+abs(b)<abs(best[1])+abs(best[2]): best=cand
        if g1==g3 and g0==g2 and g0!=g1 and e1==-e3:
            v,a,b,ue=g0,e0,-e2,e1
            cand=(v,a,b,ue)
            if best is None or abs(a)+abs(b)<abs(best[1])+abs(best[2]): best=cand
    return best

def eye_exponent_pair(s):
    r=[exponent_pair(w) for w in s]
    hits=[x for x in r if x]
    if not hits: return {"present":0}
    v,a,b,ue=min(hits,key=lambda t:abs(t[1])+abs(t[2]))
    return {"present":1,"v":v,"a":a,"b":b,"u_exp":ue,
            "which":0 if r[0]==(v,a,b,ue) else 1,
            "size":abs(a)+abs(b),"gap":abs(abs(b)-abs(a))}

def eye_euclidean_progress(s):
    """EUCLIDEAN_PROGRESS: how close the exponent pair is to carrying a unit."""
    e=eye_exponent_pair(s)
    if not e["present"]: return {"present":0,"euclid":None}
    a,b=abs(e["a"]),abs(e["b"])
    n=0
    while a and b:
        if a>b: a%=b if b else 1
        else:   b%=a if a else 1
        n+=1
        if a==0 or b==0: break
    unit=1 if min(abs(e["a"]),abs(e["b"]))==1 else 0
    return {"present":1,"euclid":n,"unit":unit,
            "minexp":min(abs(e["a"]),abs(e["b"])),"size":e["size"]}

def eye_exponent_break(s,prev):
    """EXPONENT_BREAK: intact opposition destroyed, length-independent."""
    a=eye_exponent_pair(prev); b=eye_exponent_pair(s)
    if a["present"] and not b["present"]: return {"break":1,"kind":"lost"}
    if a["present"] and b["present"] and b["size"]>a["size"]: return {"break":1,"kind":"grew"}
    return {"break":0}

def eye_donor_exit(s,prev,m):
    """DONOR_EXIT: a multiplication move moved the exponent structure."""
    if m not in (2,3,4,5): return {"exit":0}
    a=eye_exponent_pair(prev); b=eye_exponent_pair(s)
    if not a["present"]: return {"exit":0}
    if not b["present"]: return {"exit":1,"kind":"destroyed"}
    if b["which"]!=a["which"]: return {"exit":1,"kind":"moved"}
    return {"exit":0}

def eye_representation_novelty(s,seen):
    """REPRESENTATION_NOVELTY: a genuinely new exact representation."""
    key=tuple(sorted(min(cyc_rots(w)) for w in s))
    return {"novel":0 if key in seen else 1,"key":key}

def eye_suffix_distance(s,atlas):
    """SUFFIX_DISTANCE: exact distance into the finishing atlas, or None."""
    d=atlas.get(s) if atlas else None
    return {"in_atlas":1 if d is not None else 0,"dist":d}

def read_all(s,prev=None,m=None,seen=None,atlas=None):
    r={"total":tot(s),"len0":len(s[0]),"len1":len(s[1])}
    r["EXPONENT_PAIR"]=eye_exponent_pair(s)
    r["EUCLIDEAN_PROGRESS"]=eye_euclidean_progress(s)
    if prev is not None:
        r["EXPONENT_BREAK"]=eye_exponent_break(s,prev)
        r["DONOR_EXIT"]=eye_donor_exit(s,prev,m)
    if seen is not None: r["REPRESENTATION_NOVELTY"]=eye_representation_novelty(s,seen)
    if atlas is not None: r["SUFFIX_DISTANCE"]=eye_suffix_distance(s,atlas)
    return r

GORDON={6:[4,12,8,10,4,7,4,6,11,6,12,3,10,4,2,4,3],
        8:[4,12,8,10,4,10,4,7,4,11,6,11,6,12,3,10,4,2,2,4,3],
        9:[10,4,8,12,10,4,10,4,7,4,11,11,6,11,2,5,10,3,9,6,8,2,8,6,3,6,3,6,9,13,3,6,2,8,7,12,2,1,7,5,11,2,4,4,4,4,4,0],
        10:[4,12,8,10,4,10,4,7,4,7,4,11,6,11,6,6,12,3,10,4,2,2,2,4,3]}
def gordon(q): return P("XXYxy","YY"+"X"*q+"y"+"x"*q)
R7=P("xxyXy","xyyyyyyyXYYYYYYYY")
R6=P("xxyXy","xyyyyyyXYYYYYYY")

def replay(pres,moves):
    s=pres; tr=[s]
    for m in moves:
        s=core.apply_move(s,m)
        if s is None: return None,tr
        tr.append(s)
    return s,tr
