# /tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpadIPT: BOB_JOB3_CHECK  Verify every line in Bob's job 3 final with the official core; compare with the newest ac and
# stable boards and with SENT_ROWS. Fast pass only (no search).
import json,re,sys,gzip,glob,collections
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'; sys.path.insert(0,S+'/acc_private/pool/ACC_Replay_Idea_Pool')
from verifier import core; import replay_loop as rl
T=rl.load_targets(); sec=None; R=[]
for l in open('bob_job3_final.txt'):
    l=l.strip()
    if l in ('# A','# B','# C'): sec=l[2]; continue
    m=re.match(r'(s?ac-\d{5}): (\[[\d, ]*\])',l)
    if m: R.append((sec,m.group(1),json.loads(m.group(2))))
B='/home/claude/rally/research/acc/live/boards/'
def board(prefix):
    f=sorted(glob.glob(B+prefix+'_2026*.json.gz'))[-1]; out={}
    def walk(x):
        if isinstance(x,dict):
            if 'challengeId' in x: out[x['challengeId']]=(x.get('status'),x.get('currentBestLength'),x.get('kTeams'))
            for v in x.values(): walk(v)
        elif isinstance(x,list):
            for v in x: walk(v)
    walk(json.load(gzip.open(f))); return out,f.split('/')[-1]
AC,fa=board('ac'); SAC,fs=board('stable_ac')
sent={}
for l in open('/home/claude/rally/research/acc/live/SENT_ROWS.txt'):
    p=l.split()
    if len(p)>=2 and p[0][:3] in ('ac-','sac') and p[1].isdigit(): sent[p[0]]=int(p[1])
print('boards',fa,fs,'| lines',len(R),collections.Counter(s for s,_,_ in R))
out=[]
for sec,cid,mv in R:
    base=cid[1:] if cid.startswith('s') else cid
    if cid.startswith('s'):
        ok=None  # stable line: check AC part if it ends with the swap tail
    else: ok=core.verify(T[cid],mv,'ac-r2-v1',rl.LIMITS)['ok']
    st,rec,k=(SAC if cid.startswith('s') else AC).get(cid,(None,None,None))
    n=len(mv); tag=('BEAT' if rec and n<rec else 'TIE' if rec and n==rec else 'FIRST' if st and st!='solved' else 'OVER')
    ours=sent.get(cid); gain= (ours is None or n<ours)
    out.append(dict(sec=sec,id=cid,n=n,ok=ok,status=st,record=rec,k=k,sent=ours,tag=tag,new_for_us=gain,path=mv))
json.dump(out,open('bob_job3_checked.json','w'))
c=collections.Counter((o['sec'],o['tag'],o['ok'],o['new_for_us']) for o in out)
for kk,v in sorted(c.items(),key=str): print(kk,v)
for o in out:
    if o['tag'] in ('BEAT','TIE','FIRST'): print(o['sec'],o['id'],o['n'],'rec',o['record'],'k',o['k'],o['status'],'ok',o['ok'],'sent',o['sent'])
