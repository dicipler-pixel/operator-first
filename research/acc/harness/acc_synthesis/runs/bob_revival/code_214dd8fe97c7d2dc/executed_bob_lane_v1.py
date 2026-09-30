#!/usr/bin/env python3
"""Bounded Bob job-3 cross-class generator transfer for one AC row.

Only exact ordered reduced presentation states enter route unions. Every generator
change is compiled into the official unit moves, including conjugator letters,
relator alignment and endpoint finishing. This is an offline experiment.
"""
from __future__ import annotations
import argparse
from collections import deque
import hashlib
import json
import math
from pathlib import Path
import resource
import shutil
import sqlite3
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import official_checker

SOURCE = ROOT/'helpers/bob_sources/research/acc/live/bob/bob_crossclass_bundle2_20260929.json'
ROUTES = ROOT/'integration/recovered_routes.json'
CURRENT_ROUTES = ROOT/'continuation/routes.json'
RULESET = 'e13f57d82b5db1a79c1bd9d5ee1f6665ac4d96a634a3656ea20c0ada82e07643'
T = ((1,), (2,))
CONJ = {(0, 1):6,(0,-1):7,(0,2):8,(0,-2):9,
        (1, 1):10,(1,-1):11,(1,2):12,(1,-2):13}
SWAP = (1,0,4,5,2,3,10,11,12,13,6,7,8,9)


def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p, d): Path(p).write_text(json.dumps(d, indent=2, allow_nan=False)+'\n')
def inv(w): return tuple(-x for x in reversed(w))
def red(w):
    out=[]
    for x in w:
        if out and out[-1]==-x: out.pop()
        else: out.append(x)
    return tuple(out)
def sub(w, img): return red(x for a in w for x in (img[abs(a)] if a>0 else inv(img[abs(a)])))
def cyclic(w):
    w=red(w)
    while len(w)>1 and w[0]==-w[-1]: w=w[1:-1]
    return {v[i:]+v[:i] for v in (w, inv(w)) for i in range(max(1,len(v)))}

def autos(max_image=3):
    """Generate short free-group bases by Nielsen operations, tracking exact inverse."""
    identity=((1,), (2,)); seen={identity}; q=deque([identity])
    while q:
        a,b=q.popleft()
        for c in ((inv(a),b),(a,inv(b)),(b,a),
                  (red(a+b),b),(red(a+inv(b)),b),(red(b+a),b),(red(inv(b)+a),b),
                  (a,red(b+a)),(a,red(b+inv(a))),(a,red(a+b)),(a,red(inv(a)+b))):
            if max(map(len,c))<=max_image and c not in seen:
                seen.add(c);q.append(c)
    return sorted(seen, key=lambda p:(sum(map(len,p)),p))

def inverse_auto(a,b):
    # A short Nielsen basis need not have a same-length inverse.
    img={1:a,2:b}; q=deque([(1,),(-1,),(2,),(-2,)]); seen=set(q); got={}
    while q and len(got)<2:
        w=q.popleft(); v=sub(w,img)
        if v==(1,):got[1]=w
        if v==(2,):got[2]=w
        if len(w)<7:
            for g in (1,-1,2,-2):
                if w[-1]!=-g and (w+(g,)) not in seen:
                    seen.add(w+(g,));q.append(w+(g,))
    return got if len(got)==2 else None

def replay(core,start,path):
    s=start
    for m in path:s=core.apply_move(s,m)
    return s

def validate_limits(args):
    if not (math.isfinite(args.wall_seconds) and 0 < args.wall_seconds <= 180):
        raise ValueError('wall-seconds must be finite and in (0, 180]')
    if not (type(args.node_cap) is int and 0 < args.node_cap <= 600000):
        raise ValueError('node-cap must be in [1, 600000]')
    if not (type(args.memory_mib) is int and 0 < args.memory_mib <= 1024):
        raise ValueError('memory-mib must be in [1, 1024]')
    if not (type(args.target_length) is int and 0 <= args.target_length <= 10000):
        raise ValueError('invalid target-length')

def constrain_memory(mib):
    # An OS-enforced virtual-address-space bound, including mapped Python memory.
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    requested = mib*1024*1024
    bound = min(requested, hard) if hard != resource.RLIM_INFINITY else requested
    resource.setrlimit(resource.RLIMIT_AS, (bound,hard))

def own_seeds(row, bundle_row):
    paths=[]; seen=set()
    for source in (CURRENT_ROUTES,ROUTES):
        if source.exists():
            for r in json.loads(source.read_text())['routes']:
                if r['row_id']==row and tuple(r['moves']) not in seen:
                    paths.append(r['moves']);seen.add(tuple(r['moves']))
    if bundle_row is not None and tuple(bundle_row['moves']) not in seen:
        paths.append(bundle_row['moves'])
    return paths

class Budget:
    def __init__(self, wall, nodes, memory):
        self.begin=time.monotonic();self.wall=wall;self.nodes=nodes;self.memory=memory
        self.count=0;self.reason=None
    def admit(self,n=1):
        if self.reason:return False
        if time.monotonic()-self.begin>=self.wall:self.reason='wall_seconds'
        elif self.count+n>self.nodes:self.reason='node_cap'
        elif resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024>=self.memory:self.reason='memory_mib'
        elif self.count%1024==0 and controller_stopped():self.reason='controller_stop'
        else:self.count+=n
        return self.reason is None

def controller_stopped():
    ledger=ROOT/'state/ledger.sqlite3'
    if not ledger.exists():return False
    try:
        with sqlite3.connect('file:'+str(ledger)+'?mode=ro',uri=True,timeout=0.1) as db:
            row=db.execute('SELECT stopped FROM control WHERE singleton=1').fetchone()
            return bool(row and row[0])
    except sqlite3.OperationalError:
        return False


def bridge_word(core, start, goal, k, budget, max_moves):
    """Exact bounded single-relator BFS; every edge is an official move."""
    if start==goal:return []
    other=(1,); s=(start,other) if k==0 else (other,start)
    q=deque([(start,())]);seen={start}; moves=(k,)+(6,7,8,9) if k==0 else (k,10,11,12,13)
    maxword=max(len(start),len(goal))+2
    while q:
        w,p=q.popleft()
        if len(p)>=max_moves:continue
        for m in moves:
            if not budget.admit():return None
            u=core.apply_move((w,other) if k==0 else (other,w),m)[k]
            if len(u)>maxword or u in seen:continue
            t=p+(m,)
            if u==goal:return list(t)
            seen.add(u);q.append((u,t))
    return None


def finish(core,start,budget,max_moves):
    if start==T:return []
    q=deque([(start,())]);seen={start}
    cap=max(8,sum(map(len,start))+4)
    while q:
        s,p=q.popleft()
        if len(p)>=max_moves:continue
        for m in range(14):
            if not budget.admit():return None
            u=core.apply_move(s,m)
            if sum(map(len,u))>cap or u in seen:continue
            t=p+(m,)
            if u==T:return list(t)
            seen.add(u);q.append((u,t))
    return None


def pullback(path, inverse):
    p=[]
    for m in path:
        if m<6:p.append(m);continue
        rel=0 if m<10 else 1
        g=(1,-1,2,-2)[(m-6)%4]
        word=inverse[abs(g)] if g>0 else inv(inverse[abs(g)])
        p.extend(CONJ[rel,letter] for letter in reversed(word))
    return p


def transfer(core,target,donor,auto,inverse,budget,cutoff):
    """auto(target) matches donor cyclic relators; pull donor path into target."""
    ts=target;ds=donor['start']; img={1:auto[0],2:auto[1]}
    transformed=[sub(w,img) for w in ts]
    for swap in (False,True):
        aligned=[ds[1],ds[0]] if swap else ds
        if any(cyclic(transformed[k])!=cyclic(tuple(aligned[k])) for k in (0,1)):continue
        # Pulled donor source, then align target relators by paid atomic moves.
        pulled=[sub(w,inverse) for w in aligned]
        b0=bridge_word(core,ts[0],pulled[0],0,budget,min(cutoff,12))
        if b0 is None:continue
        b1=bridge_word(core,ts[1],pulled[1],1,budget,min(cutoff-len(b0),12))
        if b1 is None:continue
        path=donor['moves']; path=[SWAP[m] for m in path] if swap else path
        middle=pullback(path,inverse)
        if len(b0)+len(b1)+len(middle)>=cutoff:continue
        prefix=b0+b1+middle
        end=replay(core,ts,prefix)
        tail=finish(core,end,budget,min(12,cutoff-len(prefix)-1))
        if tail is not None and len(prefix)+len(tail)<cutoff:
            line=prefix+tail
            if replay(core,ts,line)==T:
                return line, {'auto':[list(auto[0]),list(auto[1])], 'inverse':[list(inverse[1]),list(inverse[2])], 'swap':swap,
                              'alignment_moves':len(b0)+len(b1),'pulled_moves':len(middle),'finisher_moves':len(tail)}
    return None


def shortest_saved(core,start,paths):
    if not paths:return None,0,0
    graph={start:set(),T:set()}; valid=0
    for p in paths:
        if replay(core,start,p)!=T:raise ValueError('invalid saved path')
        valid+=1;s=start
        for m in p:
            u=core.apply_move(s,m);graph.setdefault(s,set()).add((u,m));graph.setdefault(u,set()).add((s,core.INVERSE_MOVE[m]));s=u
    q=deque([start]); found={start:[]}
    while q:
        s=q.popleft()
        if s==T:return found[s],valid,len(graph)
        for u,m in sorted(graph[s],key=lambda a:(a[1],a[0])):
            if u not in found:found[u]=found[s]+[m];q.append(u)
    raise ValueError('saved routes disconnected')


def run(args):
    validate_limits(args)
    out=Path(args.output_dir).resolve();out.mkdir(parents=True,exist_ok=True)
    if any(out.iterdir()):raise FileExistsError('output directory must be empty')
    shutil.copy2(__file__,out/'executed_bob_lane_v1.py')
    test=ROOT/'tests/test_bob_lane.py'
    if test.exists():shutil.copy2(test,out/'executed_test_bob_lane.py')
    shutil.copy2(ROOT/'helpers/bob_protocol.json',out/'executed_bob_protocol.json')
    constrain_memory(args.memory_mib)
    core, specs, doc, challenges=official_checker.load_kernel()
    challenge=challenges[args.row]; start=tuple(tuple(w) for w in challenge['initial_relators'])
    if challenge['move_spec_version']!='ac-r2-v1' or specs.get('ac-r2-v1').move_spec_hash.removeprefix('sha256:')!=RULESET:raise ValueError('ruleset')
    bundle=json.loads(SOURCE.read_text()); donors=bundle['rows']
    row=next((r for r in donors if r['id']==args.row),None)
    if row is not None and tuple(tuple(w) for w in row['start'])!=start:raise ValueError('source start mismatch')
    saved=own_seeds(args.row,row)
    original_best=min(map(len,saved)) if saved else None
    best,valid,graph_nodes=shortest_saved(core,start,saved)
    union_best=len(best) if best is not None else None
    baseline=original_best
    budget=Budget(args.wall_seconds,args.node_cap,args.memory_mib)
    auto_list=autos(); comparisons=0;matches=0;donors_checked=0; transfer_attempts=0; successful=0; best_origin='saved_union' if best is not None else 'none'; detail=None
    # Donor rows are read as solved path data only: no exploration from their states.
    for donor in donors:
        if budget.reason:break
        if donor['id']==args.row:continue
        ds=[tuple(w) for w in donor['start']]
        donors_checked+=1
        for a,b in auto_list:
            if not budget.admit():break
            comparisons+=1;img={1:a,2:b}
            transformed=[sub(w,img) for w in start]
            if not (cyclic(transformed[0])==cyclic(ds[0]) and cyclic(transformed[1])==cyclic(ds[1]) or
                    cyclic(transformed[0])==cyclic(ds[1]) and cyclic(transformed[1])==cyclic(ds[0])):continue
            matches+=1
            inverse=inverse_auto(a,b)
            if inverse is None:continue
            if replay(core,tuple(ds),donor['moves'])!=T:raise ValueError('donor path invalid: '+donor['id'])
            transfer_attempts+=1
            got=transfer(core,start,donor,(a,b),inverse,budget,len(best) if best is not None else args.target_length+1)
            if got:
                successful+=1;line,detail=got;best=line;best_origin=donor['id']
            if budget.reason:break
    improved=best is not None and (baseline is None or len(best)<baseline)
    candidate=None;receipt=None
    if improved:
        candidate={'row_id':args.row,'track':'AC','start':official_checker.render(start),'moves':best,'ruleset_sha256':RULESET,
                   'evidence_grade':'V','family':'bob-cross-class-generator-transfer'}
        receipt=official_checker.check(candidate)
        if not receipt['valid']:raise ValueError('independent official replay rejected candidate')
        dump(out/'candidate.json',candidate);dump(out/'receipt.json',receipt)
    coverage={'method':'bob-cross-class-generator-transfer-v1.1','row_id':args.row,'saved_routes_replayed':valid,
              'saved_union_states':graph_nodes,'saved_union_best':union_best,'original_shortest_saved_route':baseline,
              'donors_in_bundle':len(donors),
              'donors_examined':donors_checked,'automorphisms':len(auto_list),'automorphism_comparisons':comparisons,
              'relator_class_matches':matches,'verified_donor_transfer_attempts':transfer_attempts,
              'successful_transfers':successful,'admitted_records':budget.count,'elapsed_seconds':time.monotonic()-budget.begin,
              'termination_reason':budget.reason or 'exhausted_donor_automorphisms','best_length':len(best) if best is not None else None,
              'best_origin':best_origin,'transfer_detail':detail,'target_length':args.target_length,
              'limits':{'wall_seconds':args.wall_seconds,'node_cap':args.node_cap,'memory_mib':args.memory_mib}}
    dump(out/'coverage.json',coverage)
    if improved:
        result={'kind':'candidate','summary':f'Bob route {baseline} -> {len(best)} on {args.row}, official replay valid.',
                'candidate':candidate}
    else:
        result={'kind':'bounded_miss','summary':f'No improvement from the tested Bob cross-class transfers; saved baseline {baseline}, target {args.target_length}.',
                'limits':coverage['limits'],'actual_coverage':coverage,'termination_reason':coverage['termination_reason'],
                'reopen_when':{'event':'new_exact_crossclass_seed','row_id':args.row}}
    # Snapshots were captured before any run computations.
    result['evidence']=[{'path':str(p.relative_to(ROOT)),'sha256':sha(p)} for p in sorted(out.iterdir()) if p.is_file() and p.name!='worker_result.json']
    dump(out/'worker_result.json',result)
    print(json.dumps({'kind':result['kind'],'row_id':args.row,'best_length':len(best) if best is not None else None,'saved_baseline':baseline,
                      'coverage':str(out/'coverage.json'),'result':str(out/'worker_result.json')}))
    return result


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--row',default='ac-00012');ap.add_argument('--output-dir',required=True)
    ap.add_argument('--wall-seconds',type=float,default=180);ap.add_argument('--node-cap',type=int,default=600000)
    ap.add_argument('--target-length',type=int,default=47);ap.add_argument('--memory-mib',type=int,default=1024)
    args=ap.parse_args();run(args)
if __name__=='__main__':main()
