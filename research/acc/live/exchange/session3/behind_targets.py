# SCRIPT: BEHIND_TARGETS  Solved rows we do not hold at record, read with the good-run profile from the mixer.
# For our best path on each row: ledger climb and scale climb above its start, and whether the ledger peaks after kappa
# clears (order broken). Good runs: ledger climb median 1, scale climbs in 38%, order broken 3%.
# A row is a target when our path breaks the good-run shape (so a good-shaped road likely exists) and we are close.
import json,gzip,collections
E=json.load(open('../picture/all_paths_eyes.json')); EN=E['eye_names']; k,s,l=EN.index('kappa'),EN.index('scale'),EN.index('ledger')
d=json.load(gzip.open('/home/claude/rally/research/acc/live/boards/ac_20260929T1145Z.json.gz')); B={}
def w(x):
    if isinstance(x,dict):
        if str(x.get('challengeId','')).startswith('ac-'): B[x['challengeId']]=(x.get('currentBestLength'),x.get('kTeams'))
        [w(v) for v in x.values()]
    elif isinstance(x,list): [w(v) for v in x]
w(d)
by=collections.defaultdict(list)
for p in E['paths']: by[p['id']].append(p)
out=[]
for cid,ps in by.items():
    if any(p['status']=='at_record' for p in ps) or cid not in B: continue
    rec,kt=B[cid]; p=min(ps,key=lambda p:p['n'])
    if rec is None or p['n']<=rec: continue
    K=[z[k] for z in p['eyes']];Sc=[z[s] for z in p['eyes']];Lg=[z[l] for z in p['eyes']];n=len(K)-1
    kclear=n-next(i for i in range(n+1) if all(abs(v)<1e-9 for v in K[i:])); lpeak=n-max(range(n+1),key=lambda i:(Lg[i],i))
    lclimb=max(Lg)-Lg[0]; sclimb=max(Sc)-Sc[0]; broken=lpeak<kclear
    shape=int(lclimb>1)+int(sclimb>0)+int(broken)   # how many of the three good-run traits our path misses
    out.append(dict(id=cid,record=rec,k=kt,ours=p['n'],gap=p['n']-rec,ledger_climb=lclimb,scale_climb=round(sclimb,2),order_broken=broken,shape_misses=shape,source=p['source']))
out.sort(key=lambda r:(r['gap'],-r['shape_misses'],r['k'] or 99))
json.dump(out,open('behind_targets.json','w'),indent=0)
print('rows we hold above record:',len(out))
c=collections.Counter((min(r['gap'],6),r['shape_misses']) for r in out)
for g in range(1,7): print('gap',g if g<6 else '6+',{m:c[(g,m)] for m in range(4)})
