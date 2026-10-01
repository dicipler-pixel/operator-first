"""Fresh bounded DP for the 15 specified YYx->xxYY rewrite necklaces.

Every inversion, cyclic shift and relation application is an official paid move.
This is optimal only inside the explicitly enumerated frame/necklace graph.
"""
import hashlib, heapq, json, resource, signal, sys, time
from pathlib import Path
OUT=Path(__file__).resolve().parent
ROOT=OUT.parents[2]
sys.path.insert(0,str(ROOT))
from official_checker import load_kernel, render
WALL=20
MEMORY=192*1024**2
MAX_RECORDS=600000
resource.setrlimit(resource.RLIMIT_AS,(MEMORY,MEMORY))
started=time.monotonic()
def timeout(*_):raise TimeoutError('bounded frame DP wall cap')
signal.signal(signal.SIGALRM,timeout)
signal.setitimer(signal.ITIMER_REAL,WALL)
core,specs,pins,selected=load_kernel()
RHO=(1,1,-2,-2,-1,2,2)
START=((-1,)+(2,)*10+(1,)+(-2,)*11,RHO)
TARGET=((-2,-2)+(1,)*16+(2,2,2,-1),RHO)
FRAME_MOVES=(0,1,6,7,8,9,10,11,12,13)
MULT_MOVES=(2,3)
def cyclic_reduce(w):
    w=core.free_reduce(w)
    while len(w)>1 and w[0]==-w[-1]:w=w[1:-1]
    return w
def orbit(w):
    w=cyclic_reduce(w)
    if not w:return {()}
    return {z[i:]+z[:i] for z in (w,core.invert(w)) for i in range(len(z))}
def canon(w):return min(orbit(w))
def pretty(w):return render((w,()))[0]
chain=[core.invert(START[0])]
rewrite_locations=[]
rewrite_branch_counts=[]
for layer in range(15):
    w=chain[-1]
    variants=[]
    for i in range(len(w)):
        r=w[i:]+w[:i]
        if r[:3]==(-2,-2,1):
            candidate=cyclic_reduce((1,1,-2,-2)+r[3:])
            if candidate.count(2)>=3:
                variants.append((i,candidate))
    assert variants,('no rewrite',layer,pretty(w))
    rewrite_branch_counts.append(len({canon(v) for _,v in variants}))
    cut,nxt=variants[0]
    rewrite_locations.append(cut)
    chain.append(nxt)
assert canon(chain[-1])==canon(TARGET[0])
frames=[orbit(w) for w in chain]
rho_frames=orbit(RHO)
records=0
def move(state,m):
    global records
    records+=1
    if records>MAX_RECORDS:raise RuntimeError('primitive record cap')
    return core.apply_move(state,m)
stats=[]
parents={}
dist={START:0}
status='not_started'
best=None
try:
    for layer in range(16):
        heap=[(d,s) for s,d in dist.items()]
        heapq.heapify(heap)
        while heap:
            cost,state=heapq.heappop(heap)
            if dist[state]!=cost:continue
            for m in FRAME_MOVES:
                nxt=move(state,m)
                if nxt[0] not in frames[layer] or nxt[1] not in rho_frames:continue
                if cost+1<dist.get(nxt,10**9):
                    dist[nxt]=cost+1
                    parents[(layer,nxt)]=(layer,state,m)
                    heapq.heappush(heap,(cost+1,nxt))
        stats.append({'layer':layer,'cyclic_r0_length':len(chain[layer]),
                      'exact_frames_reached':len(dist),'min_cost':min(dist.values()),
                      'max_cost':max(dist.values()),'records':records})
        if layer==15:
            best=dist.get(TARGET)
            status='completed_restricted_optimum'
            break
        nd={}
        for state,cost in dist.items():
            for m in MULT_MOVES:
                nxt=move(state,m)
                if nxt[0] not in frames[layer+1] or nxt[1] not in rho_frames:continue
                if cost+1<nd.get(nxt,10**9):
                    nd[nxt]=cost+1
                    parents[(layer+1,nxt)]=(layer,state,m)
        if not nd:
            status='completed_restricted_disconnection'
            break
        dist=nd
except (TimeoutError,MemoryError,RuntimeError) as ex:
    status='incomplete_'+type(ex).__name__
    error=str(ex)
route=None
trace=None
if best is not None:
    key=(15,TARGET)
    reverse=[]
    while key!=(0,START):
        layer,state,m=parents[key]
        reverse.append(m)
        key=(layer,state)
    route=list(reversed(reverse))
    assert len(route)==best
    state=START
    trace=[{'step':0,'state':render(state)}]
    for i,m in enumerate(route,1):
        state=core.apply_move(state,m)
        trace.append({'step':i,'move':m,'state':render(state)})
    assert state==TARGET
load_kernel()
signal.setitimer(signal.ITIMER_REAL,0)
result={'status':status,'checker_commit':pins['source_commit'],
    'core_sha256':hashlib.sha256((ROOT/'vendor/verifier/core.py').read_bytes()).hexdigest(),
    'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'reservation_commit':'9ad348cbbe861127764bfced9562f67a0bbebceb',
    'bounds':{'seconds':WALL,'memory_bytes':MEMORY,'primitive_records':MAX_RECORDS,
              'rewrite_layers':15},
    'start':render(START),'target':render(TARGET),
    'rewrite_necklaces':[pretty(w) for w in chain],
    'rewrite_rotation_offsets':rewrite_locations,
    'rewrite_branch_counts':rewrite_branch_counts,
    'rewrite_order':'first admissible cut at each layer; other rewrite orders not searched',
    'frame_moves':FRAME_MOVES,'multiplication_moves':MULT_MOVES,
    'layer_stats':stats,'records':records,'best_cost':best,
    'meets_entry_budget_48':best is not None and best<=48,
    'moves':route,'trace':trace,'error':locals().get('error'),
    'elapsed_seconds':time.monotonic()-started,
    'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
    'scope':'Exact optimum only for specified 15 rewrite necklaces, r0/r1 cyclic rotations and inverses; no conjugating tails, alternate normal-closure derivations or changes of r1 beyond these frames. No scored-row route claim.'}
(OUT/'paid_frame_dp_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ('status','best_cost','meets_entry_budget_48','records','elapsed_seconds','peak_rss_mib','moves')}))
