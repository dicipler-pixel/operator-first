#!/usr/bin/env python3
"""Independent integer-only checker; no SymPy, NumPy, solver or source verifier.

Reconstructs every generator and tower edge from the public input rules.
Checks primal forcing steps and dual impossibility identities by multiplication.
"""
import hashlib
import itertools
import json
import math
import sys
from fractions import Fraction


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(c):
    require(c.get("schema") == "compound-eye-ak-certificate-v1", "wrong certificate schema")
    p=c["problem"]
    require(p.get("schema") == "arithmetic-kakeya-tower-v1", "wrong problem schema")
    require(c["input_sha256"]==hashlib.sha256(json.dumps(p,sort_keys=True,separators=(',',':')).encode()).hexdigest(), "input hash changed")
    d=p["dims"]
    require(isinstance(d,list) and d and all(type(z) is int and z>0 for z in d), "bad dimensions")
    require(math.prod(d)<=128,"vertex limit")
    X=[]
    for x in p["X"]:
        require(isinstance(x,list) and len(x)==2 and all(type(z) is int for z in x), "bad label")
        require(x==[0,0] or x[0]+x[1]!=0,"forbidden label")
        X.append(tuple(x))
    require(len(X)==len(set(X)) and (0,0) in X,"bad X")
    V=list(itertools.product(*(range(1,z+1) for z in d)))
    ids={v:i for i,v in enumerate(V)};n=len(V)
    def vertex(v):
        require(isinstance(v,list) and all(type(z) is int for z in v) and tuple(v) in ids,"bad vertex")
        return ids[tuple(v)]
    T=[vertex(v) for v in p["initial_known"]]
    require(len(T)==len(set(T)) and len(T)<n,"bad initial T")
    initial=set(T);known=set(T)
    rows=[]
    for g in p["generators"]:
        i=vertex(g["vertex"]); x=g["label"]
        require(isinstance(x,list) and len(x)==2 and all(type(z) is int for z in x),"bad generator label type")
        require(tuple(x) in X and x != [0,0],"generator outside X or zero")
        row=[0]*(2*n);row[2*i:2*i+2]=x;rows.append(row)
    require(len(p["levels"])==len(d),"wrong number of levels")
    m=0
    for i,level in enumerate(p["levels"]):
        seen=set()
        for entry in level:
            key=entry["prefix"];x=entry["label"]
            require(isinstance(key,list) and len(key)==i+1 and all(type(z) is int for z in key),"bad prefix")
            require(all(1<=key[j]<=d[j] for j in range(i)) and 1<=key[-1]<d[i],"prefix range")
            require(tuple(key) not in seen,"repeated prefix");seen.add(tuple(key))
            require(isinstance(x,list) and len(x)==2 and all(type(z) is int for z in x) and tuple(x) in X,"edge label outside X")
            if x==[0,0]:continue
            # Build edges by scanning all vertices matching this prefix; separate
            # implementation from the producer's Cartesian suffix construction.
            for v in V:
                if list(v[:i+1]) != key:continue
                w=list(v);w[i]+=1;a=ids[v];b=ids[tuple(w)]
                row=[0]*(2*n)
                row[2*a]=x[0];row[2*a+1]=x[1];row[2*b]=-x[0];row[2*b+1]=-x[1]
                rows.append(row);m+=1
    for step in c["steps"]:
        e=vertex(step["vertex"])
        require(e not in known,"vertex forced twice or already known")
        coeff=step["coefficients"]
        require(len(coeff)==len(rows) and all(type(z) is int for z in coeff),"bad coefficients")
        w=[sum(coeff[i]*rows[i][j] for i in range(len(rows))) for j in range(2*n)]
        require(w==step["witness"],"witness vector mismatch")
        require(type(step["nonzero_a"]) is int and step["nonzero_a"]!=0,"zero target")
        require(w[2*e]==step["nonzero_a"] and w[2*e+1]==-step["nonzero_a"],"target not nonzero anti-diagonal")
        require(all(w[2*v]==w[2*v+1]==0 for v in range(n) if v not in known and v!=e),"support outside known plus new vertex")
        known.add(e)
    remaining=set(range(n))-known
    duals=c["stalled_dual_certificates"]
    require({vertex(z["vertex"]) for z in duals}==remaining and len(duals)==len(remaining),"incomplete stall certificate")
    for z in duals:
        e=vertex(z["vertex"])
        cols=[j for v in range(n) if v not in known and v!=e for j in [2*v,2*v+1]]
        equations=[[row[j] for row in rows] for j in cols]
        equations.append([row[2*e]+row[2*e+1] for row in rows])
        target=[row[2*e] for row in rows]
        weights=z["constraint_weights"];D=z["target_multiplier"]
        require(type(D) is int and D!=0 and len(weights)==len(equations) and all(type(w) is int for w in weights),"bad dual coefficients")
        require(all(sum(w*equation[j] for w,equation in zip(weights,equations))==D*target[j] for j in range(len(rows))),"dual identity failed")
    r=len(p["generators"]);t=len(initial);q=n-t
    require((c["n"],c["m"],c["r"],c["t"] )==(n,m,r,t),"counts mismatch")
    require(Fraction(c["score"])==Fraction(m+r,q),"score mismatch")
    complete=len(known)==n
    require(c["forcing_complete"] is complete,"completion mismatch")
    require(c["forced_vertices"]==[list(V[i]) for i in sorted(known)],"forced list mismatch")
    require(c["goal1_score_passes"] is (40*(m+r)<=67*q),"score gate mismatch")
    require(c["goal1_candidate_passes_public_conditions"] is (complete and 40*(m+r)<=67*q),"target gate mismatch")
    return {"certificate_valid":True,"integer_steps_checked":len(c["steps"]),"integer_duals_checked":len(duals),
            "forcing_complete":complete,"score":str(Fraction(m+r,q)),
            "target_conditions_met":complete and 40*(m+r)<=67*q,
            "qualification":"Independent local check against public conditions; no official Epoch verifier execution."}


if __name__=="__main__":
    try:
        data=json.load(sys.stdin) if sys.argv[1]=="-" else json.load(open(sys.argv[1]))
        print(json.dumps(check(data),indent=2))
    except (ValueError,TypeError,KeyError,IndexError) as e:
        print(json.dumps({"certificate_valid":False,"error":str(e)}));sys.exit(2)
