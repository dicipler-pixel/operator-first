# /tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpadIPT: TWIN_BEAM  Follow a good run. Each unsolved row has a good-run twin: the solved row whose start reads closest on
# all six eyes. The beam keeps the states whose eye readings are closest to the twin's readings at the same step
# (distance scaled by the good runs' own spread; no hand constants). Opposite arm: the twin's profile played BACKWARDS
# (its finish-side shape first). Records the attempt's eye trace next to the twin's for the mixer.
import json,sys,time,statistics as st
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'; ns={}; exec(open(S+'/picture/eyes_all_paths.py').read().split("P=json.load")[0],ns)
_eyes,T,core=ns['eyes'],ns['T'],ns['core']
def eyes(s):
    try: return _eyes(s)
    except OverflowError: return None
U=json.load(open(S+'/unknown/unknown_placed.json')); EN=U['eye_names']
E=json.load(open(S+'/picture/all_paths_eyes.json')); good={}
for p in E['paths']:
    if p['status']=='at_record' and (p['id'] not in good or p['n']<good[p['id']]['n']): good[p['id']]=p
sd=[st.pstdev(c) or 1 for c in zip(*[p['eyes'][0] for p in good.values()])]
def beam(cid,twin,W,backwards=False,extra=10):
    prof=twin['eyes'][::-1] if backwards else twin['eyes']; D=len(prof)-1+extra
    s0=tuple(map(tuple,T[cid]['initial_relators'])); e0=eyes(s0)
    front=[(0,s0,(),[e0])]; seen={s0}; best=(e0[0],(),[e0])
    for d in range(1,D+1):
        g=prof[min(d,len(prof)-1)]; cand=[]
        for _,s,path,tr in front:
            for m in range(14):
                t=core.apply_move(s,m)
                if t in seen: continue
                seen.add(t); ev=eyes(t)
                if ev is None: continue
                if ev[0]==2: return dict(solved=True,path=list(path)+[m],trace=tr+[ev])
                dist=sum(((a-b)/c)**2 for a,b,c in zip(ev,g,sd))**.5
                cand.append((dist,t,path+(m,),tr+[ev]))
                if ev[0]<best[0]: best=(ev[0],path+(m,),tr+[ev])
        if not cand: break
        cand.sort(key=lambda c:c[0]); front=cand[:W]
    return dict(solved=False,min_total=best[0],start_total=e0[0],path=list(best[1]),trace=best[2],
                end_trace=front[0][3] if front else [], end_dist=front[0][0] if front else None)
if __name__=='__main__' and 'twin_all' not in sys.argv[0]:
    W,N=int(sys.argv[1]),int(sys.argv[2]); out=open(f'twin_beam_W{W}.jsonl','a')
    for r in U['rows'][:N]:
        cid=r['id']; twin=good[r['nearest'][0][1]]
        for bw in (False,True):
            t0=time.time(); x=beam(cid,twin,W,bw)
            x.update(id=cid,twin=twin['id'],twin_n=twin['n'],backwards=bw,secs=round(time.time()-t0,1))
            if x['solved']: x['verified']=core.verify(T[cid],x['path'],'ac-r2-v1',ns['rl'].LIMITS)['ok']
            out.write(json.dumps(x)+'\n'); out.flush()
            print(cid,'twin',twin['id'],twin['n'],'backwards' if bw else 'forward',
                  ('SOLVED verified=%s len %d'%(x['verified'],len(x['path']))) if x['solved'] else
                  f"min total {x['min_total']} (start {x['start_total']}) end dist {x['end_dist']:.2f}",x['secs'],'s',flush=True)
