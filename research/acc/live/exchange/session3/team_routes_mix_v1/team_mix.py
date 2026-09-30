# SCRIPT: ACC_TEAM_MIX  every eye along all 183 verified team routes; test today's findings at team scale
import sys,json,math,numpy as np
sys.path.insert(0,'.'); sys.path.insert(0,'../solve')
from trace import mv
import splitbeam as SB
from sanov import sd
from scipy.stats import spearmanr
P=json.load(open('team_paths_verified.json'))
M={'x':1,'x^-1':-1,'y':2,'y^-1':-2}; R={}
for l in open('../pool/ACC_Replay_Idea_Pool/inputs/official_ac.jsonl'):
    d=json.loads(l); s=d['description'].split('|')[1].rsplit('>',1)[0]
    R[d['challenge_id']]=[tuple(M[t] for t in r.replace('= 1','').split()) for r in s.split(';')]
def ex(A): t=abs(A[0]+A[3]); return math.acosh(t/2) if t>2 else 0.0
EY=['total','san0','san1','ex0','ex1','kgap','comm']
pool={e:[] for e in EY}; hts=[]; within={e:[] for e in EY}
land=[]; kpit=0; kclimb=[]; conjshare=[]; breaks_pre={e:[] for e in EY}; breaks_oth={e:[] for e in EY}; studies={}
for cid,moves in P.items():
    st=(R[cid][0],R[cid][1]); Rp=SB.reps(st); S=[(st,Rp)]
    for m in moves: st=mv(*st,m); Rp=SB.step(Rp,m); S.append((st,Rp))
    T=len(moves); rows=[]
    for i,(s,Rr) in enumerate(S):
        k=SB.kap(Rr[0],Rr[1])
        rows.append(dict(total=len(s[0])+len(s[1]),san0=sd(s[0],1),san1=sd(s[1],2),ex0=ex(Rr[0]),ex1=ex(Rr[1]),kgap=math.log1p(abs(k-18)),comm=SB.comm(s[0],s[1])))
    h=[T-i for i in range(T+1)]
    for e in EY:
        v=[r[e] for r in rows]; pool[e]+=v
        if np.std(v)>0: within[e].append(spearmanr(v,h)[0])
    hts+=h
    e0=max((i for i,r in enumerate(rows) if r['ex0']>0),default=-1)+1; e1=max((i for i,r in enumerate(rows) if r['ex1']>0),default=-1)+1
    land.append((T-e0,T-e1))
    kg=[r['kgap'] for r in rows]; 
    if max(kg[1:],default=0)>kg[0]+1e-9: kpit+=1; kclimb.append(max(kg)-kg[0])
    conjshare.append(sum(1 for m in moves if m>=6)/T)
    tot=[r['total'] for r in rows]
    br={j for j in range(1,len(tot)) if tot[j]<tot[j-1]}
    for e in EY:
        v=[r[e] for r in rows]
        for j in range(1,len(v)):
            (breaks_pre if any(b in br for b in range(j+1,j+4)) else breaks_oth)[e].append(v[j]-v[j-1])
    studies[cid]=rows
json.dump(studies,open('team_mix_rows.json','w'))
print(f'{len(P)} team routes, {len(hts)} states')
print('eye      tracks progress (pooled / median within route)   change before breaks minus elsewhere')
for e in EY: print(f"  {e:6s} {spearmanr(pool[e],hts)[0]:+.2f} / {np.median(within[e]):+.2f}          {np.mean(breaks_pre[e])-np.mean(breaks_oth[e]):+.3f}")
la=np.array(land); print('moves left when each line loses its vectors: r0 median',int(np.median(la[:,0])),'max',la[:,0].max(),'; r1 median',int(np.median(la[:,1])),'max',la[:,1].max())
print('both lines keep vectors until the last 10 moves on',int(np.sum((la<=10).all(1))),'of',len(la),'routes')
print(f'kappa gap climbs above its start on {kpit} of {len(P)} routes (median climb {np.median(kclimb):.2f} in log units)')
print('share of conjugation moves per route: median',round(float(np.median(conjshare)),2))
