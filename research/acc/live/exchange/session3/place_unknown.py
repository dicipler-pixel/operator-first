# /tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpadIPT: PLACE_UNKNOWN  Put every unsolved AC start on the good-run map: read the same six eyes at the start, and find how
# close it sits to the starts of the 433 good runs (eye readings scaled by the good runs' own spread, no hand constants).
# Also learns the good-run envelope: how far each eye climbs above its start along a good run (quantiles).
import json,gzip,sys,statistics as st
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'; sys.path.insert(0,S+'/picture')
import importlib.util
spec=importlib.util.spec_from_file_location('ea',S+'/picture/eyes_all_paths.py')
src=open(S+'/picture/eyes_all_paths.py').read().split("P=json.load")[0]; ns={}; exec(src,ns); eyes=ns['eyes']; T=ns['T']
E=json.load(open(S+'/picture/all_paths_eyes.json')); EN=E['eye_names']
good=[p for p in E['paths'] if p['status']=='at_record']
starts=[p['eyes'][0] for p in good]; sd=[st.pstdev(c) or 1 for c in zip(*starts)]
env={e:sorted(max(z[j] for z in p['eyes'])-p['eyes'][0][j] for p in good) for j,e in enumerate(EN)}
q=lambda a,f:a[min(len(a)-1,int(f*len(a)))]
envelope={e:dict(q50=q(a,.5),q90=q(a,.9),q100=a[-1]) for e,a in env.items()}
d=json.load(gzip.open('/home/claude/rally/research/acc/live/boards/ac_20260929T1145Z.json.gz')); uns=[]
def w(x):
    if isinstance(x,dict):
        if x.get('challengeId','').startswith('ac-') and x.get('status')=='unsolved': uns.append(x['challengeId'])
        [w(v) for v in x.values()]
    elif isinstance(x,list): [w(v) for v in x]
w(d)
rows=[]
for cid in uns:
    if cid not in T: continue
    s=tuple(map(tuple,T[cid]['initial_relators'])); ev=eyes(s)
    dist=[(sum(((a-b)/c)**2 for a,b,c in zip(ev,g,sd))**.5,p['id'],p['record']) for g,p in zip(starts,good)]
    dist.sort(); rows.append(dict(id=cid,eyes=ev,nearest=dist[:3]))
rows.sort(key=lambda r:r['nearest'][0][0])
json.dump(dict(eye_names=EN,envelope=envelope,rows=rows),open('unknown_placed.json','w'))
gd=sorted(min(sum(((a-b)/c)**2 for a,b,c in zip(g,h,sd))**.5 for h in starts if h is not g) for g in starts)
print('unsolved rows placed:',len(rows),'| good-run envelope (climb above start):',{e:v['q90'] for e,v in envelope.items()})
print('distance of a good start to its nearest other good start: median %.2f q90 %.2f'%(st.median(gd),q(gd,.9)))
print('unsolved start to nearest good start: min %.2f median %.2f; within the good-to-good q90: %d rows'%(rows[0]['nearest'][0][0],st.median(r['nearest'][0][0] for r in rows),sum(r['nearest'][0][0]<=q(gd,.9) for r in rows)))
for r in rows[:12]: print(r['id'],'eyes',[round(v,1) for v in r['eyes']],'nearest good',r['nearest'][0][1],'rec',r['nearest'][0][2],'d=%.2f'%r['nearest'][0][0])
