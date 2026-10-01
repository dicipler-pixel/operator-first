#!/usr/bin/env python3
"""Complete cycle-free successor to the preserved eight-way beam experiment; offline checker only."""
import argparse, functools, gzip, hashlib, io, json, math, resource, shutil, sys, time
from collections import deque
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import official_checker

I=(1,0,0,1); X=(1,2,0,1); Y=(1,0,2,1)
RULESET='e13f57d82b5db1a79c1bd9d5ee1f6665ac4d96a634a3656ea20c0ada82e07643'
PROTOCOL=ROOT/'helpers/geometry_simple_protocol.json'
def dump(p,x):
    p=Path(p); tmp=p.with_suffix(p.suffix+'.tmp')
    tmp.write_text(json.dumps(x,indent=2,allow_nan=False)+'\n');tmp.replace(p)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def mul(a,b):
    p,q,r,s=a;t,u,v,w=b
    return(p*t+q*v,p*u+q*w,r*t+s*v,r*u+s*w)
def inv(a):p,q,r,s=a;return(s,-q,-r,p)
G={1:X,2:Y,-1:inv(X),-2:inv(Y)}
@functools.lru_cache(maxsize=100000)
def rho(w):
    m=I
    for a in w:m=mul(m,G[a])
    return m
def cm(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def cj(a):return(a[0],-a[1])
def cs(a,b):return(a[0]-b[0],a[1]-b[1])
def cn(a):return(-a[0],-a[1])
def disk(m):
    a,b,c,d=m
    return((b+c,a-d),(b-c,a+d))
def ray_difference(z,a):
    n=cs(cm(z[0],a[1]),cm(a[0],z[1]));d=cm(z[1],a[1])
    return cm(n,cj(d))
def ray_local(z,a):
    # Exact Gaussian-integer direction of (z-a)/(1-conj(a)*z).
    n=cm(cs(cm(z[0],a[1]),cm(a[0],z[1])),cj(a[1]))
    d=cm(a[1],cs(cm(cj(a[1]),z[1]),cm(cj(a[0]),z[0])))
    return cm(n,cj(d))
def cosine(u,v):
    nu=math.hypot(*u);nv=math.hypot(*v)
    return max(-1.,min(1.,(u[0]/nu)*(v[0]/nv)+(u[1]/nu)*(v[1]/nv))) if nu and nv else 0.
def hd(m):return math.acosh(max(1.,sum(x*x for x in m)/2))
def state_hash(s):return hashlib.sha256(json.dumps(s,separators=(',',':')).encode()).hexdigest()

class BudgetEnd(Exception):pass
class Budget:
    def __init__(self,wall,cap,overall):
        self.begin=time.monotonic();self.wall=wall;self.cap=cap;self.n=0;self.overall=overall
        self.last_poll=0.;self.reason=None
    def tick(self,n=1):
        now=time.monotonic()
        if now-self.last_poll>.1:
            self.last_poll=now
            cp=json.loads((ROOT/'continuation/checkpoint.json').read_text())
            if cp['stopped']:self.reason='controller_stop';raise BudgetEnd
        if now>=self.overall or now-self.begin>=self.wall:self.reason='wall_seconds';raise BudgetEnd
        if self.n+n>self.cap:self.reason='record_cap';raise BudgetEnd
        self.n+=n

def trace(core,start,moves):
    states=[start]
    for m in moves:states.append(core.apply_move(states[-1],m))
    return states

def run_arm(core,start,goal,road,states,name,protocol,out,overall,graph):
    backward=name=='reverse_toward'
    source,dest=(goal,start) if backward else (start,goal)
    join={}
    for i,s in enumerate(states):
        tail=road[:i] if backward else road[i:]
        if s not in join or len(tail)<len(join[s]):join[s]=tail
    targets=tuple(inv(rho(w)) for w in dest)
    @functools.lru_cache(maxsize=60000)
    def features(s):
        ms=tuple(mul(t,rho(w)) for t,w in zip(targets,s))
        return sum(hd(m) for m in ms),tuple(disk(m) for m in ms)
    @functools.lru_cache(maxsize=60000)
    def word_disk(w,j):return disk(mul(targets[j],rho(w)))
    budget=Budget(protocol['per_arm_wall_seconds'],protocol['per_arm_records'],overall)
    # state, paid path, previous distinct word per relator, last change tick
    beam=[(source,(),source,(0,0),frozenset([source]))];seen={(source,source,(0,0),frozenset([source])):0}
    baseline=len(road);best=road;layers=[];hits=[];generated=0;accepted=0;depth=0
    log=io.TextIOWrapper(gzip.GzipFile(filename='',mode='wb',fileobj=(out/(name+'_layers.jsonl.gz')).open('wb'),mtime=0),encoding='utf-8')
    reason='depth_cap'
    try:
        for depth in range(1,baseline):
            candidates={};parent_by_path={p:s for s,p,pr,ts,anc in beam}
            for s,path,previous,ticks,ancestors in beam:
                current=features(s)[1]
                for move in range(14):
                    budget.tick();generated+=1
                    u=core.apply_move(s,move)
                    if u in ancestors or sum(map(len,u))>protocol['total_word_cap']:continue
                    pp=path+(move,)
                    if u in join:
                        new=(list(join[u])+[core.INVERSE_MOVE[m] for m in reversed(pp)]) if backward else (list(pp)+list(join[u]))
                        if len(new)<len(best):
                            best=new;hits.append({'depth':depth,'length':len(new),'join_sha256':state_hash(u),'moves':new,'records':budget.n})
                            dump(out/(name+'_best.json'),{'row_id':protocol['row'],'moves':best,'hits':hits})
                    if depth>=baseline-1:continue
                    last=tuple(s[j] if u[j]!=s[j] else previous[j] for j in range(2))
                    tt=tuple(depth if u[j]!=s[j] else ticks[j] for j in range(2))
                    key=(u,last,tuple(depth-t for t in tt),ancestors|{u})
                    if seen.get(key,10**9)<depth:continue
                    h,points=features(u);length=sum(map(len,u))
                    momentum=0.
                    if name in {'fixed_heading','local_heading','local_heading_reverse','layer_clock_heading'}:
                        for j in range(2):
                            if previous[j]==s[j] or u[j]==s[j]:continue
                            old=word_disk(previous[j],j)
                            local=name!='fixed_heading'
                            incoming=cn(ray_local(old,current[j])) if local else ray_difference(current[j],old)
                            outgoing=ray_local(points[j],current[j]) if local else ray_difference(points[j],current[j])
                            speed=min(2.,hd(mul(inv(rho(previous[j])),rho(s[j]))))
                            age=1 if name=='layer_clock_heading' else max(1,depth-ticks[j])
                            momentum+=speed*cosine(incoming,outgoing)/age
                    if name=='length':priority=(float(length),h)
                    elif name=='away':priority=(-h,float(length))
                    elif name=='local_heading_reverse':priority=(h+.25*momentum,float(length))
                    else:priority=(h-.25*momentum,float(length))
                    rank=priority+(pp,)
                    if key not in candidates or rank<candidates[key][0]:
                        budget.tick();accepted+=1;candidates[key]=(rank,(u,pp,last,tt,ancestors|{u}),key)
            ordered=sorted(candidates.values(),key=lambda x:x[0]);beam=[];per_state={}
            for rank,label,key in ordered:
                if per_state.get(label[0],0)>=protocol['histories_per_state']:continue
                budget.tick(3);parent=parent_by_path[label[1][:-1]];move=label[1][-1]
                graph.setdefault(parent,set()).add((label[0],move));graph.setdefault(label[0],set()).add((parent,core.INVERSE_MOVE[move]))
                beam.append(label);seen[key]=depth;per_state[label[0]]=per_state.get(label[0],0)+1
                if len(beam)>=protocol['beam_width']:break
            record={'depth':depth,'generated_total':generated,'records':budget.n,'candidate_histories':len(candidates),
                    'beam_size':len(beam),'best_length':len(best),'beam':[{'state':s,'path':p,'previous':pr,'last_ticks':ts} for s,p,pr,ts,anc in beam]}
            log.write(json.dumps(record,separators=(',',':'))+'\n');log.flush()
            layers.append({k:v for k,v in record.items() if k!='beam'})
            dump(out/'heartbeat.json',{'arm':name,'depth':depth,'records':budget.n,'best':len(best),'utc_unix':time.time()})
            if not beam:reason='frontier_exhausted';break
    except BudgetEnd:
        reason=budget.reason
    finally:log.close()
    status='partial' if reason in {'wall_seconds','controller_stop'} else 'completed_bounded'
    result={'arm':name,'direction':'backward' if backward else 'forward','status':status,'termination_reason':reason,
            'best_length':len(best),'moves':best,'records':budget.n,'generated_moves':generated,'accepted_candidates':accepted,
            'last_depth_entered':depth,'completed_layers':len(layers),'layers':layers,'improvements':hits,
            'elapsed_seconds':time.monotonic()-budget.begin,'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024}
    dump(out/(name+'_result.json'),result)
    return result

def run(args):
    if not (0<args.wall_seconds<=180 and 0<args.node_cap<=600000 and 0<args.memory_mib<=1024):raise ValueError('bounds')
    resource.setrlimit(resource.RLIMIT_AS,(args.memory_mib*1024**2,args.memory_mib*1024**2))
    out=Path(args.output_dir).resolve();out.mkdir(parents=True,exist_ok=True)
    if any(out.iterdir()):raise FileExistsError('immutable output exists')
    p=json.loads(PROTOCOL.read_text())
    if args.row!=p['row']:raise ValueError('row outside explicit experiment')
    if len(p['arms'])*p['per_arm_records']+2000>args.node_cap:raise ValueError('record caps exceed batch')
    if len(p['arms'])*p['per_arm_wall_seconds']+10>args.wall_seconds:raise ValueError('time caps exceed batch')
    shutil.copy2(__file__,out/'executed_geometry_simple_v1.py');shutil.copy2(PROTOCOL,out/'executed_protocol.json')
    core,spec,doc,starts=official_checker.load_kernel()
    if spec.get('ac-r2-v1').move_spec_hash.removeprefix('sha256:')!=RULESET:raise ValueError('ruleset')
    start=tuple(tuple(w) for w in starts[args.row]['initial_relators']);goal=((1,),(2,))
    saved=json.loads((ROOT/'continuation/routes.json').read_text())
    roads=sorted({tuple(r['moves']) for r in saved['routes'] if r['row_id']==args.row},key=lambda x:(len(x),x))
    road=list(roads[0]);states=trace(core,start,road)
    if states[-1]!=goal:raise ValueError('seed endpoint')
    dump(out/'captured_input.json',{'row':args.row,'start':start,'baseline':len(road),'moves':road,'all_own_road_hashes':[hashlib.sha256(json.dumps(r).encode()).hexdigest() for r in roads],
         'source_commit':doc['source_commit'],'protocol':p,'claim':'Fresh owner-authorized method comparison; previous bridge misses retained.'})
    begin=time.monotonic();overall=begin+args.wall_seconds-2;results=[];best=road;best_arm=None;candidate=None
    graph={}
    for s,u,m in zip(states,states[1:],road):
        graph.setdefault(s,set()).add((u,m));graph.setdefault(u,set()).add((s,core.INVERSE_MOVE[m]))
    for name in p['arms']:
        r=run_arm(core,start,goal,road,states,name,p,out,overall,graph);results.append(r)
        if r['best_length']<len(road):
            c={'row_id':args.row,'track':'AC','start':official_checker.render(start),'moves':r['moves'],'ruleset_sha256':RULESET,'evidence_grade':'V','family':'geometry-simple-'+name}
            receipt=official_checker.check(c)
            if not receipt['valid']:raise ValueError('independent verifier rejected '+name)
            dump(out/(name+'_candidate.json'),c);dump(out/(name+'_receipt.json'),receipt)
            if len(c['moves'])<len(best):best=c['moves'];best_arm=name;candidate=c
        dump(out/'portfolio_progress.json',{'completed_arms':[x['arm'] for x in results],'best_length':len(best),'best_arm':best_arm})
        if r['termination_reason']=='controller_stop':break
    # One exact union, after all independent arms; its gain belongs to the pool.
    pool_budget=Budget(8.,args.node_cap-sum(x['records'] for x in results)-len(road),overall)
    q=deque([start]);parents={start:None};pool_reason='frontier_exhausted';pool_moves=None
    try:
        while q:
            pool_budget.tick();s=q.popleft()
            if s==goal:
                path=[]
                while parents[s] is not None:
                    parent,m=parents[s];path.append(m);s=parent
                pool_moves=list(reversed(path));pool_reason='exact_goal';break
            for u,m in sorted(graph.get(s,()),key=lambda z:(z[1],z[0])):
                pool_budget.tick()
                if u not in parents:parents[u]=(s,m);q.append(u)
    except BudgetEnd:pool_reason=pool_budget.reason
    pool={'termination_reason':pool_reason,'records':pool_budget.n,'vertices':len(graph),'directed_edges':sum(map(len,graph.values())),
          'best_length':len(pool_moves) if pool_moves is not None else None,'moves':pool_moves}
    dump(out/'pool_result.json',pool)
    vertices=sorted(graph);ids={s:i for i,s in enumerate(vertices)}
    raw=json.dumps({'states':vertices,'edges':[[ids[s],ids[u],m] for s in vertices for u,m in sorted(graph[s],key=lambda z:(z[1],z[0]))]},separators=(',',':')).encode()
    (out/'exact_graph.json.gz').write_bytes(gzip.compress(raw,mtime=0))
    if pool_moves is not None and len(pool_moves)<len(best):
        candidate={'row_id':args.row,'track':'AC','start':official_checker.render(start),'moves':pool_moves,'ruleset_sha256':RULESET,'evidence_grade':'V','family':'geometry-simple-exact-pool'}
        receipt=official_checker.check(candidate)
        if not receipt['valid']:raise ValueError('pool official verifier rejected')
        dump(out/'pool_candidate.json',candidate);dump(out/'pool_receipt.json',receipt)
        best=pool_moves;best_arm='exact_union_after_independent_arms'
    coverage={'row':args.row,'baseline':len(road),'best_length':len(best),'best_arm':best_arm,'elapsed_seconds':time.monotonic()-begin,
              'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'records':sum(x['records'] for x in results)+pool_budget.n+len(road),'pool':pool,
              'arms':[{k:v for k,v in r.items() if k not in {'moves','layers','improvements'}} for r in results],
              'limits':{'wall_seconds':args.wall_seconds,'node_cap':args.node_cap,'memory_mib':args.memory_mib},
              'interpretation':'Beam pruning makes every negative local to this exact policy/budget. Clocks and plots do not change paid costs. No physical dynamics or scoring claim.'}
    dump(out/'coverage.json',coverage)
    if candidate:result={'kind':'candidate','summary':f"Cycle-free eight-way geometry experiment: {args.row} {len(road)} -> {len(best)} via {best_arm}; independent official replay passed.",'candidate':candidate}
    elif len(results)!=len(p['arms']) or any(r['status']=='partial' for r in results):
        result={'kind':'blocked','summary':'Cycle-free geometry comparison partially executed; time/stop interruptions are not misses. See per-arm coverage.'}
    else:result={'kind':'bounded_miss','summary':f"Cycle-free eight-way geometry comparison found no shorter route than {len(road)} under the recorded beam bounds.",'limits':coverage['limits'],'reopen_when':{'event':'new_own_route_or_explicitly_justified_method','row_id':args.row}}
    result['actual_coverage']=coverage;result['evidence']=[{'path':str(f.relative_to(ROOT)),'sha256':sha(f)} for f in sorted(out.iterdir()) if f.is_file()]
    dump(out/'worker_result.json',result);print(json.dumps(coverage))

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--row',required=True);a.add_argument('--output-dir',required=True)
    a.add_argument('--wall-seconds',type=float,default=180);a.add_argument('--node-cap',type=int,default=600000)
    a.add_argument('--memory-mib',type=int,default=1024);a.add_argument('--target-length',type=int,required=True)
    run(a.parse_args())
