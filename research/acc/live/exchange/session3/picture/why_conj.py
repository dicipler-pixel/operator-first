# /tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpadIPT: ACC_WHY_CONJ  Where do our extra conjugations go? For every maximal run of conjugations, compare the moves spent
# with the cheapest way to reach the same pair of relators by conjugation alone: per relator, the free-reduced net
# conjugator length, or the rotation distance min(m, L-m) when the result is a cyclic rotation of the start.
# waste = run length - sum of those. Split by group and by approach/landing (landing = after kappa resolves).
import json,sys,statistics as st,collections
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'; sys.path.insert(0,S+'/acc_private/pool/ACC_Replay_Idea_Pool'); sys.path.insert(0,S+'/acc_private/pool/ACC_Replay_Idea_Pool/verifier')
from verifier import core; import replay_loop as rl
T=rl.load_targets(); A=json.load(open(S+'/picture/all_paths.json')); E=json.load(open(S+'/picture/all_paths_eyes.json'))['paths']
fr=core.free_reduce
def start(cid):
    t=T[cid]; return [list(t['relators'][0]) if 'relators' in t else None, None] if False else None
st0=lambda cid: core_start(cid)
def core_start(cid):
    t=T[cid]
    for k in ('initial_relators',):
        if k in t: return [list(r) for r in t[k]]
    raise KeyError(list(t))
def rot_dist(a,b):
    L=len(a)
    if L!=len(b) or L==0: return None
    for m in range(L):
        if a[m:]+a[:m]==b: return min(m,L-m)
    return None
res=collections.defaultdict(lambda: collections.defaultdict(list))
for p,e in zip(A,E):
    assert p['id']==e['id']
    if not (25<=p['record']<=50): continue
    g='at_record' if p['status']=='at_record' else ('above_1_3' if p['gap']<=3 else 'above_4up')
    kap=[z[1] for z in e['eyes']]
    land=next(i for i in range(len(kap)) if all(abs(v)<1e-9 for v in kap[i:]))  # state index where kappa has resolved
    s=tuple(tuple(r) for r in core_start(p['id'])); states=[s]
    for m in p['path']: s=core.apply_move(s,m); states.append(s)
    mv=p['path']; i=0; w={'approach':0,'landing':0}; spent={'approach':0,'landing':0}; runs=collections.Counter()
    while i<len(mv):
        if mv[i]<6: i+=1; continue
        j=i
        while j<len(mv) and mv[j]>=6: j+=1
        net=[[],[]]
        for m in mv[i:j]:
            r=0 if m<=9 else 1; gl=core.GENS[(m-6)%4] if hasattr(core,'GENS') else None
            net[r]=list(fr([gl]+list(net[r])))
        best=0
        for r in (0,1):
            if not net[r]: continue
            rd=rot_dist(states[i][r],states[j][r]); best+=min(len(net[r]), rd if rd is not None else 10**9)
        ph='approach' if i<land else 'landing'
        w[ph]+=(j-i)-best; spent[ph]+=j-i; runs[ph]+=1; i=j
    for ph in w:
        res[g][ph+'_waste'].append(w[ph]); res[g][ph+'_conj'].append(spent[ph])
for g in ('at_record','above_1_3','above_4up'):
    R=res[g]; n=len(R['approach_waste'])
    print(g,n,'paths | approach conj mean %.1f waste mean %.2f (paths with waste>0: %d%%) | landing conj %.1f waste %.2f'%(
        st.mean(R['approach_conj']),st.mean(R['approach_waste']),100*sum(x>0 for x in R['approach_waste'])/n,st.mean(R['landing_conj']),st.mean(R['landing_waste'])))
