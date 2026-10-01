#!/usr/bin/env python3
"""One bounded paid cyclic-insertion macro experiment, no raw-move beam."""
import hashlib,heapq,json,resource,sys,time
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(256*1024**2,256*1024**2))
resource.setrlimit(resource.RLIMIT_CPU,(32,32))
ROOT=Path(__file__).resolve().parents[3];sys.path.insert(0,str(ROOT))
from official_checker import load_kernel,render
c,_,_,_=load_kernel(); deadline=time.monotonic()+30;began=time.monotonic()
def w(s):return tuple({'x':1,'X':-1,'y':2,'Y':-2}[a]for a in s)
start=(w('YYYXyyx'),w('YXXXXyxxxxx'));MAX=100000;DEPTH=3;CAP=64
def cyc(a):
    while len(a)>1 and a[0]==-a[-1]:a=a[1:-1]
    return a
def structure(a):
    a=cyc(a)
    if len(set(map(abs,a)))==1:return 0
    for g in (1,2):
        if sum(abs(v)==g for v in a)!=2:continue
        ix=[i for i,v in enumerate(a)if abs(v)==g]
        if a[ix[0]]!=-a[ix[1]]:continue
        b=a[ix[0]+1:ix[1]];d=a[ix[1]+1:]+a[:ix[0]]
        if b and d and len(set(b))==len(set(d))==1 and b[0]==-d[0]:
            if min(len(b),len(d))==1:return 1
    return 2
def det(s):
    v=[[sum(x for x in a if abs(x)==g)//g for g in(1,2)]for a in s]
    return v[0][0]*v[1][1]-v[0][1]*v[1][0]
def frames(a,ri):
    choices={}
    for inv in (False,True):
        z=c.invert(a)if inv else a
        for k in range(len(z)):
            v=z[k:]+z[:k]
            if k<=len(z)-k:gs=tuple(-x for x in z[:k])
            else:gs=tuple(reversed(z[k:]))
            p=([ri]if inv else[])+[6+4*ri+c.GENS.index(g)for g in gs]
            if v not in choices or len(p)<len(choices[v]):choices[v]=p
    return list(choices.items())
records=[(start,-1,[],0)];seen={start};q=[(0,18,0)];hits=[];generated=0;pruned=0;reason='macro_depth_exhausted';best=(18,0)
while q:
    if time.monotonic()>=deadline:reason='wall_time_cap';break
    if len(records)>=MAX:reason='admitted_state_cap';break
    _,_,idx=heapq.heappop(q);s,parent,path,depth=records[idx]
    if depth>=DEPTH:continue
    for target in (0,1):
        source=1-target
        for a,pa in frames(s[target],target):
            for b,pb in frames(s[source],source):
                generated+=1
                if generated%256==0 and(time.monotonic()>=deadline or len(records)>=MAX):break
                if not a or not b or a[-1]!=-b[0]:continue
                # Each macro must genuinely consume a boundary, not merely append.
                z=c.free_reduce(a+b)
                if len(z)>=len(a)+len(b):continue
                ns=(z,s[1])if target==0 else(s[0],z)
                if sum(map(len,ns))>CAP or ns in seen:continue
                if abs(det(ns))!=1:pruned+=1;continue
                macro=pa+pb+[2 if target==0 else 4]+[c.INVERSE_MOVE[m]for m in reversed(pb)]
                # Budget bounds apply to the paid path too, including temporary source frames.
                test=s; peak=sum(map(len,s))
                for m in macro:test=c.apply_move(test,m);peak=max(peak,sum(map(len,test)))
                assert test==ns
                if peak>CAP:continue
                if len(records)>=MAX:break
                seen.add(ns);n=len(records);records.append((ns,idx,macro,depth+1))
                score=min(structure(ns[0]),structure(ns[1]));ln=sum(map(len,ns))
                if (ln,n)<best:best=(ln,n)
                if score<=1:hits.append(n)
                # Prefer one-stage unit residue, but every admitted macro remains eligible.
                heapq.heappush(q,(depth+1,ln,n))
            if time.monotonic()>=deadline or len(records)>=MAX:break
        if time.monotonic()>=deadline or len(records)>=MAX:break
    if hits:reason='structural_hit';break
def trace(idx):
    chunks=[];j=idx
    while records[j][1]>=0:
        chunks.append(records[j][2]);j=records[j][1]
    moves=[m for p in reversed(chunks)for m in p];s=start;peak=sum(map(len,s))
    for m in moves:s=c.apply_move(s,m);peak=max(peak,sum(map(len,s)))
    assert s==records[idx][0]
    return {'moves':moves,'endpoint':render(s),'macrodepth':records[idx][3],
            'paid_moves':len(moves),'peak_total_relator_length':peak,
            'determinant':det(s),'structure_codes':[structure(a)for a in s]}
out={'method':'cyclic_inverse_source_insertion_unit_residue_v1','row':'ac-07824',
    'reservation_commit':'9ad348cbbe861127764bfced9562f67a0bbebceb',
    'bounds':{'wall_seconds':30,'memory_mib':256,'admitted_states':MAX,'macrodepth':DEPTH,'peak_total_length':CAP},
    'initial_relators':render(start),'elapsed_seconds':time.monotonic()-began,'stop_reason':reason,
    'admitted_states':len(records),'generated_macros':generated,'determinant_rejections':pruned,
    'frontier_states':len(q),'hits':[trace(i)for i in hits[:10]],'best_length_state':trace(best[1]),
    'negative_scope':'Only completed enumerated macros in this exact run; cap stop is not depth exhaustion or an impossibility result.',
    'scored_route_found':any(records[i][0]==((1,),(2,))for i in hits),
    'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
Path(__file__).with_name('unit_residue_probe_result.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
