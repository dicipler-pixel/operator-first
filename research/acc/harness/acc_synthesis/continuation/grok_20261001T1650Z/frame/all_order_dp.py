"""All orders of 15 YYx->xxYY rewrites, with primitive frame costs.

One separately authorized batch; resource-capped partial runs are incomplete.
Only routes of total entry length <=48 are sought. No arbitrary conjugating
tails or different normal-closure derivations are represented.
"""
import hashlib, heapq, json, resource, signal, sys, time
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
sys.path.insert(0,str(ROOT))
from official_checker import load_kernel, render
WALL=20; MEMORY=192*1024**2; CAP=600000; BUDGET=48
resource.setrlimit(resource.RLIMIT_AS,(MEMORY,MEMORY))
def timeout(*_):raise TimeoutError('wall cap')
signal.signal(signal.SIGALRM,timeout)
signal.setitimer(signal.ITIMER_REAL,WALL)
started=time.monotonic()
core,specs,pins,selected=load_kernel()
RHO=(1,1,-2,-2,-1,2,2)
START=((-1,)+(2,)*10+(1,)+(-2,)*11,RHO)
TARGET=((-2,-2)+(1,)*16+(2,2,2,-1),RHO)
FRAME_MOVES=(0,1,6,7,8,9,10,11,12,13)
records=0
def tick():
    global records
    records+=1
    if records>CAP:raise RuntimeError('record cap')
def cyclic_reduce(w):
    w=core.free_reduce(w)
    while len(w)>1 and w[0]==-w[-1]:w=w[1:-1]
    return w
def rotations(w):return {w[i:]+w[:i] for i in range(len(w))} if w else {()}
def orbit(w):return rotations(w)|rotations(core.invert(w))
def canon(w):return min(rotations(cyclic_reduce(w)))
def pretty(w):return render((w,()))[0]
def path_to(key):
    reverse=[]
    while key!=(0,START):
        l,s,m=parents[key]
        reverse.append(m);key=(l,s)
    return list(reversed(reverse))
levels=[{canon(core.invert(START[0]))}]
stats=[];edges=[];parents={};all_costs={(0,START):0}
dist={START:0};status='not_started';solution=None;error=None
try:
    for layer in range(15):
        nxt=set()
        for word in sorted(levels[-1]):
            for i in range(len(word)):
                tick()
                r=word[i:]+word[:i]
                if r[:3]!=(-2,-2,1):continue
                u=cyclic_reduce((1,1,-2,-2)+r[3:])
                if u.count(2)<3:continue
                u=canon(u)
                nxt.add(u);edges.append((layer,word,i,u))
        levels.append(nxt)
    assert canon(TARGET[0]) in levels[15]
    allowed=[set().union(*(orbit(w) for w in words)) for words in levels]
    rho_frames=orbit(RHO)
    # Exact paid r1 return distance: it is unaffected by moves 0,2,3,6..9.
    rho_return={RHO:0};pending=[RHO]
    for r in pending:
        for m in (1,10,11,12,13):
            tick();u=core.apply_move(((),r),m)[1]
            if u in rho_frames and u not in rho_return:
                rho_return[u]=rho_return[r]+1;pending.append(u)
    for layer in range(16):
        heap=[(d,s) for s,d in dist.items()];heapq.heapify(heap)
        while heap:
            cost,state=heapq.heappop(heap)
            if dist[state]!=cost:continue
            if layer==15 and state==TARGET:
                solution=path_to((layer,state));status='verified_hit_within48';break
            for m in FRAME_MOVES:
                tick();u=core.apply_move(state,m)
                if u[0] not in allowed[layer] or u[1] not in rho_frames:continue
                nc=cost+1
                if nc+15-layer+rho_return[u[1]]>BUDGET:continue
                if nc<dist.get(u,10**9):
                    dist[u]=nc;parents[(layer,u)]=(layer,state,m)
                    all_costs[(layer,u)]=nc
                    heapq.heappush(heap,(nc,u))
        stats.append({'layer':layer,'necklaces':len(levels[layer]),
            'exact_frames_reached':len(dist),'min_cost':min(dist.values()) if dist else None,
            'records':records})
        if solution is not None:break
        if layer==15:
            status='completed_no_route_within48_in_restricted_graph';break
        nd={}
        for state,cost in dist.items():
            for m in (2,3):
                tick();u=core.apply_move(state,m)
                if u[0] not in allowed[layer+1] or u[1] not in rho_frames:continue
                nc=cost+1
                if nc+14-layer+rho_return[u[1]]>BUDGET:continue
                if nc<nd.get(u,10**9):
                    nd[u]=nc;parents[(layer+1,u)]=(layer,state,m)
                    all_costs[(layer+1,u)]=nc
        dist=nd
        if not dist:
            status='completed_no_route_within48_in_restricted_graph';break
except (TimeoutError,MemoryError,RuntimeError) as ex:
    status='incomplete_'+type(ex).__name__;error=str(ex)
signal.setitimer(signal.ITIMER_REAL,0)
trace=None
if solution is not None:
    s=START;trace=[{'step':0,'state':render(s)}]
    for i,m in enumerate(solution,1):
        s=core.apply_move(s,m);trace.append({'step':i,'move':m,'state':render(s)})
    assert s==TARGET and len(solution)<=48
load_kernel()
with (OUT/'all_order_reached.jsonl').open('w') as f:
    for (layer,state),cost in sorted(all_costs.items()):
        parent=parents.get((layer,state))
        item={'layer':layer,'state':render(state),'cost':cost}
        if parent:item['parent']={'layer':parent[0],'state':render(parent[1]),'move':parent[2]}
        f.write(json.dumps(item,separators=(',',':'))+'\n')
report={'status':status,'error':error,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'checker_commit':pins['source_commit'],'core_sha256':hashlib.sha256((ROOT/'vendor/verifier/core.py').read_bytes()).hexdigest(),
    'start':render(START),'target':render(TARGET),'entry_budget':48,
    'scope':'All generated YYx->xxYY rewrite orders through15 additions, with >=3 positive y; exact cyclic/inverse frames and moves0,1,6..13, transition multiplications2,3. No conjugating tails, changed r1 normal-closure class, or other derivations.',
    'bounds':{'seconds':WALL,'memory_bytes':MEMORY,'records':CAP,'rewrite_layers':15},
    'necklaces_per_layer':[len(x) for x in levels],
    'necklaces':[[pretty(w) for w in sorted(x)] for x in levels],
    'rewrite_edges':[{'layer':l,'from':pretty(w),'cut':i,'to':pretty(u)} for l,w,i,u in edges],
    'stats':stats,'records':records,'states_retained':len(all_costs),
    'moves':solution,'trace':trace,
    'elapsed_seconds':time.monotonic()-started,
    'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
    'reached_sha256':hashlib.sha256((OUT/'all_order_reached.jsonl').read_bytes()).hexdigest()}
(OUT/'all_order_receipt.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ('status','error','necklaces_per_layer','records','states_retained','moves','elapsed_seconds','peak_rss_mib')}))
