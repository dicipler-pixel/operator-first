# SCRIPT: ACC_FLAT_TEAM_TEST  do the team's beams miss FLAT rows (low scale for their length)? If yes, those are the
# targets for a climb-first lane. Scale percentile = rank of a row's start scale among ALL solved starts of the same
# total length (no constants). Outcome = we hold the AC record (SENT_ROWS status tie/beat) vs not, on solved rows <=45.
import sys,json,gzip,glob,math,csv,numpy as np
sys.path.insert(0,'/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad/acc_private/ladder/../solve'); sys.path.insert(0,'/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad/acc_private/ladder'); import splitbeam as SB
from sklearn.metrics import roc_auc_score
A={r['challengeId']:(r['currentBestLength'],r['kTeams']) for r in next(v for v in json.load(gzip.open(sorted(glob.glob('research/acc/live/boards/ac_2026*.json.gz'))[-1]))['data'].values() if isinstance(v,list))}
held={}
for l in open('research/acc/live/SENT_ROWS.txt'):
    if l.startswith('#') or not l.strip(): continue
    t=l.split()
    if t[0].startswith('ac-'): held[t[0]]=int(t[1])
MAP={'x':1,'x^-1':-1,'y':2,'y^-1':-2}; R={}
for l in open('/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad/acc_private/ladder/../pool/ACC_Replay_Idea_Pool/inputs/official_ac.jsonl'):
    d=json.loads(l); s=d['description'].split('|')[1].rsplit('>',1)[0]
    R[d['challenge_id']]=[tuple(MAP[t] for t in r.replace('= 1','').split()) for r in s.split(';')]
def eyes(a,b):
    P,Q=SB.reps((a,b))[:2]; x=P[0]+P[3]; y=Q[0]+Q[3]; k=SB.kap(P,Q)
    return math.log1p(abs(x*x-4))+math.log1p(abs(y*y-4)), math.log1p(abs(k-18))
E={c:eyes(*R[c]) for c in R}
byL={}
for c,(rec,k) in A.items():
    if rec and c in R: byL.setdefault(len(R[c][0])+len(R[c][1]),[]).append(E[c])
def pct(c,i):
    ref=[e[i] for e in byL.get(len(R[c][0])+len(R[c][1]),[])]
    return None if len(ref)<20 else float(np.mean(np.array(ref)<E[c][i]))
rows=[]
for c,(rec,k) in A.items():
    if not rec or c not in R or rec>45: continue
    ps,pr=pct(c,0),pct(c,1)
    if ps is None: continue
    rows.append(dict(id=c,rec=rec,k=k,held=held.get(c)==rec or (held.get(c) or 999)<rec,ps=ps,pr=pr,L=len(R[c][0])+len(R[c][1])))
y=[0 if r['held'] else 1 for r in rows]
print('solved rows rec<=45 with length reference:',len(rows),' held by us:',len(rows)-sum(y))
print('AUC (NOT held vs held) of scale percentile: %.3f   of relation percentile: %.3f'%(roc_auc_score(y,[r['ps'] for r in rows]),roc_auc_score(y,[r['pr'] for r in rows])))
for lo,hi in ((0,.1),(.1,.25),(.25,.5),(.5,.75),(.75,1.01)):
    g=[r for r in rows if lo<=r['ps']<hi]
    if g: print(f'  scale pct {lo:.2f}-{hi:.2f}: {len(g):5d} rows, we hold {sum(r["held"] for r in g)/len(g):.2f}; k1 unheld {sum(1 for r in g if r["k"]==1 and not r["held"])}')
# control: record length alone
print('control AUC of record length: %.3f'%roc_auc_score(y,[r['rec'] for r in rows]))
# same inside record-length bands (is it just length?)
for lo,hi in ((0,25),(25,35),(35,46)):
    g=[r for r in rows if lo<=r['rec']<hi]; yy=[0 if r['held'] else 1 for r in g]
    if len(set(yy))==2: print(f'  records {lo}-{hi-1}: n={len(g)} AUC scale pct {roc_auc_score(yy,[r["ps"] for r in g]):.3f} relation pct {roc_auc_score(yy,[r["pr"] for r in g]):.3f}')
json.dump(rows,open('/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad/acc_private/ladder/flat_team_rows.json','w'))
