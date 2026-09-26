#!/usr/bin/env python3
"""
COMPOUND EYE HARNESS — ACC v2.0
================================
Standard-library reference implementation.

Principle:
  RUN -> RECORD -> CHECK -> COLLISION-ESCALATE -> MIX -> SHAPE -> ACT

This tool never treats a heuristic signature as exact state equality.
Heuristic screens ROUTE work. Only exact official-move replay / exact
component closure / explicitly certified obstructions may prove or prune.

Modes
-----
1) Verified path:
   python compound_eye_harness_acc_v2.py path \
      --path-json AC02842_TO_SIGNED_AK3.json --out-dir RUN_PATH

2) Exact bounded component + boundary screen:
   python compound_eye_harness_acc_v2.py component \
      --r0 YXXYx --r1 YYYYXyyyx --cap 14 --out-dir RUN_CAP14

3) Large state dump screening (streaming):
   python compound_eye_harness_acc_v2.py states \
      --states-jsonl states.jsonl --out-jsonl features.jsonl --out-dir RUN_STREAM

Accepted state JSONL:
   {"r0":"YXXYx","r1":"YYYYXyyyx"}
or {"state":["YXXYx","YYYYXyyyx"]}

Eye families implemented
------------------------
EXACT / state:
  - exact free reduction and official ordinary AC move grammar 0..13
  - exact state hash
  - ordered target / determinant sanity
  - lengths and imbalance
  - exponent-sum ledger M and bounded-exact row-operation distance d_M

CHEAP / structural:
  - cyclic reduction / cyclic cancellation depth
  - cyclic length-2 / length-3 subword counts
  - longest symbol run
  - 14-labelled immediate move response (not just its histogram)
  - local floor / collapse gain / local child diversity
  - exact profile hashes

DEEP / retained information:
  - noncommutative Magnus expansion through degree 2
  - noncommutative Magnus expansion through degree 3
  - degree-3 signatures modulo 2, 3 and 5
  - collision ladder: scalar -> histogram -> labelled channels -> ledger
    -> Magnus-2 -> Magnus-3

PATH / history:
  - exact path replay
  - path-ordered GL(2,Z) transport
  - gross and net shear currents
  - conjugation currents
  - move bigram / trigram counts
  - future-move profile persistence and turn
  - useful-move-set Jaccard
  - ledger-fiber holonomy events (same M, changed presentation)
  - sign-cancellation warning: zero net shear with nonzero gross shear
  - multi-scale telemetry summaries over 1,3,5,9,17,33,65 where available

FRONTIER / bounded component:
  - exact component census and BFS parent/depth
  - exact distinct crossing children
  - boundary child response R/D/S/U per official move label
  - scalar count vs labelled-orientation collision audit
  - exact rank of one-hot boundary channel matrix
  - low-exit collision ladder
  - one canonical entry edge retained for each boundary child

RECORD:
  - immutable run manifest with tool/input hashes
  - append-only HARNESS_LEDGER.jsonl
  - per-eye coverage/status table
  - no silent disappearance of blocked / staged / inapplicable eyes
"""

import argparse, collections, datetime, fractions, hashlib, json, math, os, sys
from pathlib import Path

VERSION="2.0.0"
CH={1:"x",-1:"X",2:"y",-2:"Y"}
PARSE={"x":1,"X":-1,"y":2,"Y":-2}
MOVE_NAMES={
 0:"invert_r0",1:"invert_r1",
 2:"r0_mul_r1",3:"r0_mul_inv_r1",4:"r1_mul_r0",5:"r1_mul_inv_r0",
 6:"conj_r0_x",7:"conj_r0_X",8:"conj_r0_y",9:"conj_r0_Y",
 10:"conj_r1_x",11:"conj_r1_X",12:"conj_r1_y",13:"conj_r1_Y",
}
ROW_E={
 0:((-1,0),(0,1)), 1:((1,0),(0,-1)),
 2:((1,1),(0,1)), 3:((1,-1),(0,1)),
 4:((1,0),(1,1)), 5:((1,0),(-1,1)),
}
CONJ_CURRENT={
 6:(1,0,0,0),7:(-1,0,0,0),8:(0,1,0,0),9:(0,-1,0,0),
 10:(0,0,1,0),11:(0,0,-1,0),12:(0,0,0,1),13:(0,0,0,-1)
}
SHEAR_CURRENT={2:(1,0),3:(-1,0),4:(0,1),5:(0,-1)}
WINDOWS=(1,3,5,9,17,33,65)

EYE_REGISTRY=[
 {"id":"ce.acc.exact.replay","version":VERSION,"stage":"exact","status":"implemented",
  "meaning":"Official ordinary-AC 0..13 replay and exact state identity."},
 {"id":"ce.acc.state.length","version":VERSION,"stage":"census","status":"implemented",
  "meaning":"Per-relator length, total length and imbalance."},
 {"id":"ce.acc.state.exponent_ledger","version":VERSION,"stage":"census","status":"implemented",
  "meaning":"Exact 2x2 exponent-sum matrix and bounded-exact GL(2,Z) row distance."},
 {"id":"ce.acc.state.cyclic_structure","version":VERSION,"stage":"census","status":"implemented",
  "meaning":"Cyclic reduction, cancellation depth and cyclic 2/3-gram support."},
 {"id":"ce.acc.state.labelled_move_response","version":VERSION,"stage":"census","status":"implemented",
  "meaning":"All 14 official move labels retained separately; no count-only compression."},
 {"id":"ce.acc.state.magnus2","version":VERSION,"stage":"deep","status":"implemented",
  "meaning":"Degree-2 noncommutative Magnus record."},
 {"id":"ce.acc.state.magnus3","version":VERSION,"stage":"deep","status":"implemented",
  "meaning":"Degree-3 noncommutative Magnus record and mod-p hashes."},
 {"id":"ce.acc.path.ordered_transport","version":VERSION,"stage":"path","status":"implemented",
  "meaning":"Ordered GL(2,Z) transport, not net shear alone."},
 {"id":"ce.acc.path.order_memory","version":VERSION,"stage":"path","status":"implemented",
  "meaning":"Move n-grams, gross/net currents and path hash."},
 {"id":"ce.acc.path.profile_persistence","version":VERSION,"stage":"path","status":"implemented",
  "meaning":"Persistence/rotation of the 14-dimensional future-move profile."},
 {"id":"ce.acc.path.fiber_holonomy","version":VERSION,"stage":"path","status":"implemented",
  "meaning":"Same exponent ledger with changed nonabelian presentation/deeper record."},
 {"id":"ce.acc.frontier.boundary_channels","version":VERSION,"stage":"frontier","status":"implemented",
  "meaning":"R/D/S/U response per official move label on an exact bounded boundary."},
 {"id":"ce.acc.frontier.collision_ladder","version":VERSION,"stage":"frontier","status":"implemented",
  "meaning":"Escalate only when a coarser recorded view collides."},
 {"id":"ce.acc.search.highway_suffix","version":VERSION,"stage":"adapter","status":"adapter_ready",
  "meaning":"Exact suffix/Highway lookup when a verified Highway dictionary is supplied."},
 {"id":"ce.acc.search.reverse_ball","version":VERSION,"stage":"adapter","status":"adapter_ready",
  "meaning":"Exact meet lookup when a verified reverse-ball dictionary is supplied."},
 {"id":"ce.acc.search.learned_obstruction","version":VERSION,"stage":"adapter","status":"specified",
  "meaning":"Scope-hashed exact obstructions may prune; heuristic signatures may not."},
 {"id":"ce.acc.search.kstep_response","version":VERSION,"stage":"stall_specialist","status":"specified",
  "meaning":"Depth-k response moments only after one-step labelled profiles still collide."},
]

# ---------------- exact word / move kernel ----------------

def reduce_word(w):
    out=[]
    for a in w:
        if out and out[-1]==-a: out.pop()
        else: out.append(a)
    return tuple(out)

def parse_word(s):
    if s=="1" or s=="": return tuple()
    try: return reduce_word(tuple(PARSE[c] for c in s))
    except KeyError as e: raise ValueError(f"bad word symbol {e.args[0]!r}") from None

def word_text(w): return "".join(CH[a] for a in w) or "1"
def inv(w): return tuple(-a for a in reversed(w))
def mul(a,b): return reduce_word(a+b)
def conj(w,c): return reduce_word((c,)+w+(-c,))

def apply_move(st,m):
    a,b=st
    if m==0:a=inv(a)
    elif m==1:b=inv(b)
    elif m==2:a=mul(a,b)
    elif m==3:a=mul(a,inv(b))
    elif m==4:b=mul(b,a)
    elif m==5:b=mul(b,inv(a))
    elif m==6:a=conj(a,1)
    elif m==7:a=conj(a,-1)
    elif m==8:a=conj(a,2)
    elif m==9:a=conj(a,-2)
    elif m==10:b=conj(b,1)
    elif m==11:b=conj(b,-1)
    elif m==12:b=conj(b,2)
    elif m==13:b=conj(b,-2)
    else: raise ValueError(f"move {m} outside ordinary AC 0..13")
    return (a,b)

def total_len(s): return len(s[0])+len(s[1])
def state_text(s): return (word_text(s[0]),word_text(s[1]))
def state_key_bytes(s): return (word_text(s[0])+"|"+word_text(s[1])).encode()
def state_sha(s): return hashlib.sha256(state_key_bytes(s)).hexdigest()

# ---------------- exact ledger ----------------

def exp_sum(w):
    x=y=0
    for a in w:
        if abs(a)==1:x += 1 if a>0 else -1
        else:y += 1 if a>0 else -1
    return (x,y)

def matrix_M(s): return (exp_sum(s[0]),exp_sum(s[1]))
def det2(A): return A[0][0]*A[1][1]-A[0][1]*A[1][0]
def mm(A,B):
    return ((A[0][0]*B[0][0]+A[0][1]*B[1][0],
             A[0][0]*B[0][1]+A[0][1]*B[1][1]),
            (A[1][0]*B[0][0]+A[1][1]*B[1][0],
             A[1][0]*B[0][1]+A[1][1]*B[1][1]))
def inv_unimod(A):
    d=det2(A)
    if abs(d)!=1: raise ValueError(f"non-unimodular ledger {A}")
    return ((d*A[1][1],-d*A[0][1]),(-d*A[1][0],d*A[0][0]))

def row_distance_table(depth=12):
    I=((1,0),(0,1)); D={I:0}; q=collections.deque([I])
    while q:
        A=q.popleft(); d=D[A]
        if d>=depth: continue
        for E in ROW_E.values():
            B=mm(E,A)
            if B not in D:
                D[B]=d+1;q.append(B)
    return D

# ---------------- cyclic / structural ----------------

def cyclic_reduce(w):
    w=list(reduce_word(w))
    while len(w)>=2 and w[0]==-w[-1]:
        w=w[1:-1]
    return tuple(w)

def cyclic_ngrams(w,n):
    w=cyclic_reduce(w)
    L=len(w)
    if L==0 or L<n:return set()
    return {tuple(w[(i+j)%L] for j in range(n)) for i in range(L)}

def longest_symbol_run(w):
    if not w:return 0
    best=cur=1
    for i in range(1,len(w)):
        if w[i]==w[i-1]:cur+=1;best=max(best,cur)
        else:cur=1
    return best

# ---------------- Magnus through degree 3 ----------------

def gen_series(a,degree=3):
    g=abs(a)
    if a>0:return {():1,(g,):1}
    out={():1}
    mon=()
    for k in range(1,degree+1):
        mon=mon+(g,)
        out[mon]= -1 if k%2 else 1
    return out

def poly_mul(p,q,degree):
    z=collections.defaultdict(int)
    for a,ca in p.items():
        for b,cb in q.items():
            m=a+b
            if len(m)<=degree:z[m]+=ca*cb
    return {m:c for m,c in z.items() if c}

def magnus(w,degree=3):
    p={():1}
    for a in w:p=poly_mul(p,gen_series(a,degree),degree)
    return p

MON2=((1,1),(1,2),(2,1),(2,2))
MON3=tuple((a,b,c) for a in (1,2) for b in (1,2) for c in (1,2))

def magnus_vectors(w):
    p=magnus(w,3)
    d2=tuple(p.get(m,0) for m in MON2)
    d3=tuple(p.get(m,0) for m in MON3)
    return d2,d3

def mod_hash(values,p):
    b=(",".join(str(int(x)%p) for x in values)).encode()
    return hashlib.sha256(b).hexdigest()[:16]

# ---------------- local 14-channel profile ----------------

def local_profile(s,rowdist=None):
    L=total_len(s); M=matrix_M(s); d0=rowdist.get(M) if rowdist else None
    deltas=[]; dmd=[]; child_hash=[]; outcomes=[]
    seen=set()
    for m in range(14):
        t=apply_move(s,m); seen.add(t)
        dl=total_len(t)-L
        deltas.append(dl)
        outcomes.append("D" if dl<0 else "S" if dl==0 else "U")
        child_hash.append(state_sha(t)[:16])
        if rowdist is not None:
            dc=rowdist.get(matrix_M(t))
            dmd.append(None if d0 is None or dc is None else dc-d0)
    return {
      "delta_total_by_move":deltas,
      "outcome_by_move":"".join(outcomes),
      "down":sum(x<0 for x in deltas),
      "same":sum(x==0 for x in deltas),
      "up":sum(x>0 for x in deltas),
      "local_floor":L+min(deltas),
      "collapse_gain":-min(deltas),
      "unique_children":len(seen),
      "dM_delta_by_move":dmd if rowdist is not None else None,
      "child_hash16_by_move":child_hash,
      "profile_sha256":hashlib.sha256(json.dumps([deltas,dmd],sort_keys=True).encode()).hexdigest(),
    }

def state_features(s,rowdist,deep=True):
    M=matrix_M(s); cr=[cyclic_reduce(s[0]),cyclic_reduce(s[1])]
    out={
      "state":list(state_text(s)),
      "state_sha256":state_sha(s),
      "lengths":[len(s[0]),len(s[1])],
      "total_length":total_len(s),
      "imbalance":abs(len(s[0])-len(s[1])),
      "M":[list(M[0]),list(M[1])],
      "detM":det2(M),
      "dM_to_I":rowdist.get(M),
      "cyclic_lengths":[len(cr[0]),len(cr[1])],
      "cyclic_cancel_pairs":[(len(s[0])-len(cr[0]))//2,(len(s[1])-len(cr[1]))//2],
      "cyclic_2gram_counts":[len(cyclic_ngrams(s[0],2)),len(cyclic_ngrams(s[1],2))],
      "cyclic_3gram_counts":[len(cyclic_ngrams(s[0],3)),len(cyclic_ngrams(s[1],3))],
      "longest_symbol_run":[longest_symbol_run(s[0]),longest_symbol_run(s[1])],
      "local":local_profile(s,rowdist),
    }
    if deep:
        a2,a3=magnus_vectors(s[0]); b2,b3=magnus_vectors(s[1])
        all2=a2+b2; all3=a3+b3
        out["magnus2"]=[list(a2),list(b2)]
        out["magnus2_norm2"]=sum(x*x for x in all2)
        out["magnus2_sha16"]=hashlib.sha256(repr(all2).encode()).hexdigest()[:16]
        out["magnus3"]=[list(a3),list(b3)]
        out["magnus3_norm2"]=sum(x*x for x in all3)
        out["magnus3_sha16"]=hashlib.sha256(repr(all3).encode()).hexdigest()[:16]
        out["magnus3_mod"]={str(p):mod_hash(all3,p) for p in (2,3,5)}
    return out

# ---------------- vector persistence ----------------

def cosine(a,b):
    aa=sum(x*x for x in a); bb=sum(x*x for x in b)
    if aa==0 or bb==0:return None
    return sum(x*y for x,y in zip(a,b))/math.sqrt(aa*bb)

def jaccard(A,B):
    U=A|B
    return 1.0 if not U else len(A&B)/len(U)

def addv(a,b):return tuple(x+y for x,y in zip(a,b))

# ---------------- exact rank for channel matrices ----------------

def rational_rank(rows):
    if not rows:return 0
    A=[[fractions.Fraction(x) for x in row] for row in rows]
    r=0; cols=len(A[0])
    for c in range(cols):
        pivot=next((i for i in range(r,len(A)) if A[i][c]),None)
        if pivot is None:continue
        A[r],A[pivot]=A[pivot],A[r]
        pv=A[r][c]; A[r]=[x/pv for x in A[r]]
        for i in range(len(A)):
            if i!=r and A[i][c]:
                f=A[i][c];A[i]=[A[i][j]-f*A[r][j] for j in range(cols)]
        r+=1
        if r==len(A):break
    return r

# ---------------- collision / retention audit ----------------

def key_hist_boundary(rec):
    c=collections.Counter(rec["boundary_outcome_by_move"])
    return (c["R"],c["D"],c["S"],c["U"])

def class_count(records,keyfn):
    return len({keyfn(r) for r in records})

def collision_ladder(records):
    if not records:return []
    levels=[
      ("scalar_total_length",lambda r:r["total_length"]),
      ("boundary_histogram",lambda r:key_hist_boundary(r)),
      ("labelled_14_channel",lambda r:r["boundary_outcome_by_move"]),
      ("exponent_ledger",lambda r:tuple(sum(r["M"],[]))),
      ("cyclic_support",lambda r:tuple(r["cyclic_lengths"]+r["cyclic_2gram_counts"]+r["cyclic_3gram_counts"])),
      ("magnus2",lambda r:r.get("magnus2_sha16")),
      ("magnus3",lambda r:r.get("magnus3_sha16")),
    ]
    return [{"level":name,"unique_classes":class_count(records,fn),
             "collisions":len(records)-class_count(records,fn)} for name,fn in levels]

# ---------------- records / provenance ----------------

def sha_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""):h.update(b)
    return h.hexdigest()

def utcnow():return datetime.datetime.now(datetime.timezone.utc).isoformat()

def ensure_out(path):
    p=Path(path);p.mkdir(parents=True,exist_ok=True);return p

def tool_hash():
    try:return sha_file(__file__)
    except Exception:return None

def write_json(path,obj):
    Path(path).write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def append_ledger(outdir,event):
    with open(outdir/"HARNESS_LEDGER.jsonl","a",encoding="utf-8") as f:
        f.write(json.dumps(event,sort_keys=True,separators=(",",":"))+"\n")

def run_manifest(mode,outdir,input_desc,outputs,eye_coverage,extra=None):
    base={
      "schema":"compound-eye-harness-run-v2",
      "harness_version":VERSION,"mode":mode,"utc":utcnow(),
      "tool_sha256":tool_hash(),"input":input_desc,"outputs":outputs,
      "eye_coverage":eye_coverage,
    }
    if extra:base.update(extra)
    raw=json.dumps(base,sort_keys=True,separators=(",",":")).encode()
    base["run_id"]=hashlib.sha256(raw).hexdigest()[:24]
    write_json(outdir/"RUN_MANIFEST.json",base)
    append_ledger(outdir,base)
    write_json(outdir/"EYE_REGISTRY.json",EYE_REGISTRY)
    return base

# ---------------- path mode ----------------

def ngram_counts(xs,n):
    return collections.Counter(tuple(xs[i:i+n]) for i in range(len(xs)-n+1))

def rolling_summary(xs,w):
    if len(xs)<w:return None
    z=xs[-w:]
    mean=sum(z)/w
    if w==1:return {"n":w,"last":z[-1],"mean":mean,"range":0.0,"slope":0.0,"sign_balance":0.0}
    slope=(z[-1]-z[0])/(w-1)
    dif=[z[i]-z[i-1] for i in range(1,w)]
    sb=(sum(d>0 for d in dif)-sum(d<0 for d in dif))/len(dif)
    return {"n":w,"last":z[-1],"mean":mean,"range":max(z)-min(z),"slope":slope,"sign_balance":sb}

def run_path(args):
    outdir=ensure_out(args.out_dir); rowdist=row_distance_table(args.ledger_depth)
    raw=json.load(open(args.path_json,"r",encoding="utf-8"))
    moves=list(map(int,raw["moves"]))
    if "states" in raw:
        states=[(parse_word(a),parse_word(b)) for a,b in raw["states"]]
        if len(states)!=len(moves)+1:raise ValueError("states length != moves+1")
        cur=states[0]
        for i,m in enumerate(moves):
            cur=apply_move(cur,m)
            if cur!=states[i+1]:raise ValueError(f"replay mismatch step {i+1}")
    else:
        sw=raw.get("start_words") or raw.get("initial_words")
        if not sw:raise ValueError("path JSON needs states or start_words")
        cur=(parse_word(sw[0]),parse_word(sw[1]));states=[cur]
        for m in moves:
            cur=apply_move(cur,m);states.append(cur)

    M0=matrix_M(states[0]); M0i=inv_unimod(M0)
    ordered=((1,0),(0,1)); conjcur=(0,0,0,0); shear=(0,0)
    rows=[]; byM=collections.defaultdict(list)
    gross_shear=0
    prev_delta=None; prev_useful=None
    for i,s in enumerate(states):
        if i:
            m=moves[i-1]
            if m<=5:ordered=mm(ROW_E[m],ordered)
            if m in CONJ_CURRENT:conjcur=addv(conjcur,CONJ_CURRENT[m])
            if m in SHEAR_CURRENT:
                shear=addv(shear,SHEAR_CURRENT[m]);gross_shear+=1
        f=state_features(s,rowdist,deep=True)
        A=mm(matrix_M(s),M0i)
        if A!=ordered:raise AssertionError(f"ordered transport mismatch {i}")
        dv=f["local"]["delta_total_by_move"]
        useful={m for m,d in enumerate(dv) if d<=0}
        c=cosine(prev_delta,dv) if prev_delta is not None else None
        j=jaccard(prev_useful,useful) if prev_useful is not None else None
        f.update({
          "step":i,"incoming_move":None if i==0 else moves[i-1],
          "incoming_move_name":None if i==0 else MOVE_NAMES[moves[i-1]],
          "ordered_row_transport":[list(A[0]),list(A[1])],
          "conjugation_current":list(conjcur),
          "coarse_shear_current":list(shear),
          "future_profile_cosine_prev":c,
          "future_profile_turn_prev":None if c is None else 1-c,
          "useful_move_jaccard_prev":j,
          "prefix_peak":max(total_len(x) for x in states[:i+1]),
          "prefix_floor":min(total_len(x) for x in states[:i+1]),
        })
        rows.append(f);byM[tuple(sum(f["M"],[]))].append(i)
        prev_delta=dv;prev_useful=useful

    hol=[]
    for idxs in byM.values():
        if len(idxs)>1:
            for a,b in zip(idxs,idxs[1:]):
                if rows[a]["state"]!=rows[b]["state"]:
                    seg=moves[a:b]
                    hol.append({
                      "start_step":a,"end_step":b,"M":rows[a]["M"],
                      "segment_moves":seg,
                      "segment_move_names":[MOVE_NAMES[m] for m in seg],
                      "start_state":rows[a]["state"],"end_state":rows[b]["state"],
                      "length_change":rows[b]["total_length"]-rows[a]["total_length"],
                      "magnus2_norm2_change":rows[b]["magnus2_norm2"]-rows[a]["magnus2_norm2"],
                      "magnus3_norm2_change":rows[b]["magnus3_norm2"]-rows[a]["magnus3_norm2"],
                    })

    traces={
      "total_length":[r["total_length"] for r in rows],
      "dM":[r["dM_to_I"] if r["dM_to_I"] is not None else 0 for r in rows],
      "magnus2_norm2":[r["magnus2_norm2"] for r in rows],
      "local_floor":[r["local"]["local_floor"] for r in rows],
      "collapse_gain":[r["local"]["collapse_gain"] for r in rows],
      "profile_turn":[0.0 if r["future_profile_turn_prev"] is None else r["future_profile_turn_prev"] for r in rows],
    }
    multiscale={name:{str(w):rolling_summary(vals,w) for w in WINDOWS if len(vals)>=w} for name,vals in traces.items()}
    result={
      "schema":"compound-eye-harness-path-v2","harness_version":VERSION,
      "source":raw.get("source"),"replay_ok":True,"move_count":len(moves),
      "peak_total_length":max(traces["total_length"]),
      "floor_total_length":min(traces["total_length"]),
      "gross_shear_moves":gross_shear,"net_shear_current":list(shear),
      "shear_sign_cancellation":gross_shear>0 and shear==(0,0),
      "move_counts":dict(sorted(collections.Counter(moves).items())),
      "move_bigrams":{",".join(map(str,k)):v for k,v in ngram_counts(moves,2).items()},
      "move_trigrams":{",".join(map(str,k)):v for k,v in ngram_counts(moves,3).items()},
      "path_sha256":hashlib.sha256(bytes(moves)).hexdigest(),
      "fiber_holonomy_events":hol,
      "multiscale_retina":multiscale,
      "largest_profile_turns":sorted(
        [{"step":r["step"],"incoming_move":r["incoming_move"],"turn":r["future_profile_turn_prev"],
          "from_length":rows[r["step"]-1]["total_length"] if r["step"] else None,
          "to_length":r["total_length"]}
         for r in rows if r["future_profile_turn_prev"] is not None],
        key=lambda x:x["turn"],reverse=True)[:10],
      "rows":rows,
    }
    runfile=outdir/"PATH_RUN.json";write_json(runfile,result)
    coverage=[
      {"eye":e["id"],"status":"ok" if e["stage"] in ("exact","census","deep","path") and e["status"]=="implemented"
       else "not_run_in_path_mode","population":len(rows) if e["stage"] in ("census","deep") else 1}
      for e in EYE_REGISTRY
    ]
    manifest=run_manifest("path",outdir,
      {"path":str(Path(args.path_json).name),"sha256":sha_file(args.path_json)},
      {"path_run":runfile.name},coverage,
      {"summary":{"states":len(rows),"moves":len(moves),"fiber_holonomy_events":len(hol)}})
    print(json.dumps({"ok":True,"run_id":manifest["run_id"],"path_run":str(runfile),
                      "fiber_holonomy_events":len(hol),"shear_sign_cancellation":result["shear_sign_cancellation"]},indent=2))

# ---------------- component / boundary mode ----------------

def boundary_record(child,comp,rowdist,entrances,deep=True):
    f=state_features(child,rowdist,deep=deep)
    code=[]
    retlabels=[]
    for m in range(14):
        t=apply_move(child,m)
        if t in comp:
            code.append("R");retlabels.append(m)
        else:
            d=total_len(t)-total_len(child)
            code.append("D" if d<0 else "S" if d==0 else "U")
    f["boundary_outcome_by_move"]="".join(code)
    f["return_move_labels"]=retlabels
    f["entry_edges"]=[{"parent_sha16":state_sha(p)[:16],"move":m,"move_name":MOVE_NAMES[m]} for p,m in entrances]
    f["entry_edge_count"]=len(entrances)
    f["boundary_histogram"]=dict(collections.Counter(code))
    return f

def onehot_channel_row(code):
    cats="RDSU";row=[]
    for c in code:row.extend(1 if c==k else 0 for k in cats)
    return row

def run_component(args):
    outdir=ensure_out(args.out_dir);rowdist=row_distance_table(args.ledger_depth)
    start=(parse_word(args.r0),parse_word(args.r1)); cap=args.cap
    q=collections.deque([start]); comp={start}; parent={start:(None,None,0)}
    proposals=0
    while q:
        s=q.popleft();depth=parent[s][2]
        for m in range(14):
            proposals+=1;t=apply_move(s,m)
            if total_len(t)<=cap and t not in comp:
                comp.add(t);parent[t]=(s,m,depth+1);q.append(t)
    exits=collections.defaultdict(list)
    for s in comp:
        for m in range(14):
            t=apply_move(s,m)
            if t not in comp:exits[t].append((s,m))
    exit_lengths=collections.Counter(total_len(t) for t in exits)
    min_exit=min(exit_lengths) if exit_lengths else None
    low=[t for t in exits if total_len(t)==min_exit]

    # Census eyes on every component state: cheap only.
    comp_features=[state_features(s,rowdist,deep=False) for s in comp]
    # Boundary children: cheap first, then deep because this is calibration/reference mode.
    bfeatures=[boundary_record(t,comp,rowdist,exits[t],deep=True) for t in exits]
    lowfeatures=[r for r in bfeatures if r["total_length"]==min_exit]

    hist_classes=class_count(lowfeatures,key_hist_boundary) if lowfeatures else 0
    orient_classes=class_count(lowfeatures,lambda r:r["boundary_outcome_by_move"]) if lowfeatures else 0
    channel_rank=rational_rank([onehot_channel_row(r["boundary_outcome_by_move"]) for r in lowfeatures])

    ladder=collision_ladder(lowfeatures)
    first_full=next((x["level"] for x in ladder if x["unique_classes"]==len(lowfeatures)),None)

    compfile=outdir/"COMPONENT_STATES.jsonl"
    with open(compfile,"w",encoding="utf-8") as f:
        for rec in comp_features:f.write(json.dumps(rec,separators=(",",":"))+"\n")
    bfile=outdir/"BOUNDARY_FEATURES.jsonl"
    with open(bfile,"w",encoding="utf-8") as f:
        for rec in bfeatures:f.write(json.dumps(rec,separators=(",",":"))+"\n")
    lowfile=outdir/"LOWEST_EXITS.json"
    write_json(lowfile,lowfeatures)

    summary={
      "schema":"compound-eye-harness-component-v2","harness_version":VERSION,
      "start":[args.r0,args.r1],"cap":cap,"component_states":len(comp),
      "component_length_histogram":dict(sorted(collections.Counter(total_len(s) for s in comp).items())),
      "bfs_max_depth":max(x[2] for x in parent.values()),
      "expansion_proposals":proposals,
      "distinct_boundary_children":len(exits),
      "boundary_edge_count":sum(len(v) for v in exits.values()),
      "boundary_length_histogram":dict(sorted(exit_lengths.items())),
      "lowest_exit_length":min_exit,"lowest_exit_count":len(lowfeatures),
      "lowest_exit_histogram_classes":hist_classes,
      "lowest_exit_labelled_channel_classes":orient_classes,
      "lowest_exit_labelled_channel_onehot_rank":channel_rank,
      "collision_ladder":ladder,
      "first_level_separating_all_lowest_exits":first_full,
      "interpretation_fence":"Signature separation routes screening; it is not exact state equality and never proves an AC solution.",
    }
    sfile=outdir/"COMPONENT_SUMMARY.json";write_json(sfile,summary)

    coverage=[]
    for e in EYE_REGISTRY:
        if e["stage"]=="census" and e["status"]=="implemented":
            coverage.append({"eye":e["id"],"status":"ok","population":len(comp)})
        elif e["stage"] in ("frontier","deep") and e["status"]=="implemented":
            coverage.append({"eye":e["id"],"status":"ok","population":len(exits)})
        elif e["stage"]=="exact" and e["status"]=="implemented":
            coverage.append({"eye":e["id"],"status":"ok","population":1})
        else:
            coverage.append({"eye":e["id"],"status":"not_run_in_component_mode","population":0})
    manifest=run_manifest("component",outdir,
      {"r0":args.r0,"r1":args.r1,"cap":cap},
      {"summary":sfile.name,"component_states":compfile.name,"boundary":bfile.name,"lowest_exits":lowfile.name},
      coverage,{"summary":summary})
    print(json.dumps({"ok":True,"run_id":manifest["run_id"],**summary},indent=2))

# ---------------- streaming state mode ----------------

def run_states(args):
    outdir=ensure_out(args.out_dir);rowdist=row_distance_table(args.ledger_depth)
    n=0
    inp=Path(args.states_jsonl);outp=Path(args.out_jsonl)
    with open(inp,"r",encoding="utf-8") as src, open(outp,"w",encoding="utf-8") as out:
        for line in src:
            if not line.strip():continue
            obj=json.loads(line)
            a,b=obj["state"] if "state" in obj else (obj["r0"],obj["r1"])
            rec=state_features((parse_word(a),parse_word(b)),rowdist,deep=not args.cheap_only)
            for k,v in obj.items():
                if k not in ("state","r0","r1"):rec.setdefault(k,v)
            out.write(json.dumps(rec,separators=(",",":"))+"\n");n+=1
    coverage=[]
    for e in EYE_REGISTRY:
        if e["stage"]=="census" and e["status"]=="implemented":
            coverage.append({"eye":e["id"],"status":"ok","population":n})
        elif e["stage"]=="deep" and e["status"]=="implemented":
            coverage.append({"eye":e["id"],"status":"staged_not_run" if args.cheap_only else "ok",
                             "population":0 if args.cheap_only else n})
        else:coverage.append({"eye":e["id"],"status":"not_run_in_state_stream_mode","population":0})
    manifest=run_manifest("states",outdir,
      {"path":inp.name,"sha256":sha_file(inp),"cheap_only":args.cheap_only},
      {"features":outp.name},coverage,{"summary":{"states":n}})
    print(json.dumps({"ok":True,"run_id":manifest["run_id"],"states":n,"features":str(outp)},indent=2))

def main():
    ap=argparse.ArgumentParser(description="Compound Eye HARNESS ACC v2")
    sub=ap.add_subparsers(dest="mode",required=True)
    p=sub.add_parser("path");p.add_argument("--path-json",required=True);p.add_argument("--out-dir",required=True);p.add_argument("--ledger-depth",type=int,default=12)
    c=sub.add_parser("component");c.add_argument("--r0",required=True);c.add_argument("--r1",required=True);c.add_argument("--cap",type=int,required=True);c.add_argument("--out-dir",required=True);c.add_argument("--ledger-depth",type=int,default=12)
    s=sub.add_parser("states");s.add_argument("--states-jsonl",required=True);s.add_argument("--out-jsonl",required=True);s.add_argument("--out-dir",required=True);s.add_argument("--cheap-only",action="store_true");s.add_argument("--ledger-depth",type=int,default=12)
    args=ap.parse_args()
    if args.mode=="path":run_path(args)
    elif args.mode=="component":run_component(args)
    else:run_states(args)

if __name__=="__main__":main()
