# /tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpadIPT: ACC_FULL_PICTURE_ANALYSIS  what we did, what we missed, and where. All 1,746 verified paths.
import json,statistics,collections,math
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'; D=json.load(open(S+'/picture/all_paths_eyes.json')); P=D['paths']; EN=D['eye_names']
md=statistics.median
def landing(p):   # first state where the relation rail is resolved (kappa back at the vacuum value) and stays there
    e=p['eyes']; n=len(e)
    for i in range(n):
        if all(r[1]<1e-9 for r in e[i:]): return i
    return n-1
def cls(m): return 'mult' if 2<=m<=5 else 'inv' if m<=1 else 'conj'
print('=== A. all paths, record band 25-50, mean eye by moves still to go ===')
grp={'AT RECORD':[p for p in P if p['status']=='at_record' and 25<=p['record']<=50],
     'ABOVE 1-3':[p for p in P if p['status']=='above' and p['gap']<=3 and 25<=p['record']<=50],
     'ABOVE 4+':[p for p in P if p['status']=='above' and p['gap']>=4 and 25<=p['record']<=50]}
for g,S_ in grp.items(): print(f'  {g}: {len(S_)} paths, {len({p["id"] for p in S_})} rows')
for j,e in enumerate(EN):
    line=f'  {e:7s}'
    for k in (24,16,12,8,4):
        vals=[]
        for g,S_ in grp.items():
            v=[p['eyes'][-1-k][j] for p in S_ if len(p['eyes'])>k]; vals.append(statistics.mean(v) if v else float('nan'))
        line+=f' | {k:2d} to go: '+' / '.join(f'{x:5.1f}' for x in vals)
    print(line)
print('  (columns: at record / above 1-3 / above 4+)')
print('=== B. landing: moves before and after the relation rail resolves (kappa at vacuum for good) ===')
for g,S_ in grp.items():
    b=[landing(p) for p in S_]; a=[len(p['path'])-landing(p) for p in S_]
    print(f'  {g:10s}: approach {md(b)} moves, landing {md(a)} moves')
print('=== C. same row, record path vs our longer path (pairs) ===')
by=collections.defaultdict(list)
for p in P: by[p['id']].append(p)
pairs=[]
for cid,ps in by.items():
    R=[p for p in ps if p['status']=='at_record']; O=[p for p in ps if p['status']=='above' and p['gap']<=10]
    if R and O:
        r=min(R,key=lambda p:p['n'])
        for o in O: pairs.append((r,o))
print('  pairs:',len(pairs),'rows:',len({r['id'] for r,_ in pairs}))
ex=collections.Counter(); ap=[]; ld=[]
for r,o in pairs:
    cr=collections.Counter(cls(m) for m in r['path']); co=collections.Counter(cls(m) for m in o['path'])
    for c in ('mult','conj','inv'): ex[c]+=co[c]-cr[c]
    ap.append(landing(o)-landing(r)); ld.append((len(o['path'])-landing(o))-(len(r['path'])-landing(r)))
tot=sum(ex.values())
print('  extra moves in our longer path, by kind:',{k:f'{v} ({v/tot:.0%})' for k,v in ex.items()},'total',tot)
print(f'  where the extra moves go: approach (before kappa resolves) median {md(ap)}, mean {statistics.mean(ap):.2f}; landing (after) median {md(ld)}, mean {statistics.mean(ld):.2f}')
# where do the paired paths first part ways on the matrix rails? first index where ours carries more scale than the record path at the same moves-to-go
div=[]
for r,o in pairs:
    er,eo=r['eyes'],o['eyes']; K=min(len(er),len(eo))
    first=next((k for k in range(K-1,-1,-1) if eo[-1-k][2]>er[-1-k][2]+1e-9),None)
    div.append(None if first is None else first)
d=[x for x in div if x is not None]
print(f'  ours first carries more scale than the record path (same moves to go): median {md(d) if d else None} moves to go; never: {div.count(None)} of {len(div)}')
print('=== D. which rows we miss: start state of rows with a record-length path vs rows with only longer paths ===')
first={}
for p in P: first.setdefault(p['id'],p['eyes'][0])
hit={p['id'] for p in P if p['status']=='at_record'}; miss={p['id'] for p in P}-hit
recs={p['id']:p['record'] for p in P}
for j,e in enumerate(EN):
    for lo,hi in ((0,34),(35,50)):
        a=[first[c][j] for c in hit if recs[c] and lo<=recs[c]<=hi]; b=[first[c][j] for c in miss if recs[c] and lo<=recs[c]<=hi]
        if a and b: print(f'  {e:7s} records {lo}-{hi}: held rows {md(a):6.2f} (n={len(a)})  vs missed rows {md(b):6.2f} (n={len(b)})')
