# /tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpadIPT: TWIN_ALL  Twin-following on EVERY unsolved AC row (2,672), in parallel over the cores.
# For each row: its good-run twin (closest start on all six eyes), a short twin-following beam, and the readings that
# rank a row as a target: how many steps it stays with the twin, which eye leaves first, how far total length falls,
# and how many of the 14 first moves change the pattern eye the way the twin's opening does.
import json,sys,time,multiprocessing as mp,statistics as st
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'; sys.path.insert(0,S+'/unknown')
import twin_beam as TB
U=json.load(open(S+'/unknown/unknown_placed.json')); EN=U['eye_names']
E=json.load(open(S+'/picture/all_paths_eyes.json')); good=TB.good
step=[st.pstdev([b[j]-a[j] for p in good.values() for a,b in zip(p['eyes'],p['eyes'][1:])]) or 1 for j in range(len(EN))]
W,EXTRA=int(sys.argv[1]),int(sys.argv[2])
def one(r):
    cid=r['id']; twin=good[r['nearest'][0][1]]
    tcap=dict(twin); tcap['eyes']=twin['eyes'][:21]   # first 20 steps are where rows leave their twin
    try: x=TB.beam(cid,tcap,W,False,extra=EXTRA)
    except Exception as e: return dict(id=cid,error=str(e))
    tw=twin['eyes']; at=x.get('end_trace') or x.get('trace'); n=min(len(tw),len(at))
    leave={e:next((i for i in range(n) if abs(at[i][j]-tw[i][j])>2*step[j]),None) for j,e in enumerate(EN)}
    lv=[v for v in leave.values() if v is not None]; stay=min(lv) if lv else n
    first=min(((v,e) for e,v in leave.items() if v is not None),default=(n,'none'))[1]
    # opening: twin's first-step change of the pattern eye; count first moves that make the same-sign change
    g=EN.index('grams2'); s0=tuple(map(tuple,TB.T[cid]['initial_relators'])); e0=TB.eyes(s0)
    dg=tw[1][g]-tw[0][g] if len(tw)>1 else 0; same=0
    for m in range(14):
        ev=TB.eyes(TB.core.apply_move(s0,m))
        if ev and ((ev[g]-e0[g])*dg>0 or (dg==0 and ev[g]==e0[g])): same+=1
    out=dict(id=cid,twin=twin['id'],twin_n=twin['n'],twin_dist=r['nearest'][0][0],stay=stay,first_leave=first,leave=leave,
             start_total=e0[0],min_total=x.get('min_total',2),drop=e0[0]-x.get('min_total',2),opening_matches=same,solved=x['solved'])
    if x['solved']:
        out['path']=x['path']; out['verified']=TB.core.verify(TB.T[cid],x['path'],'ac-r2-v1',TB.ns['rl'].LIMITS)['ok']
    return out
if __name__=='__main__':
    done=set()
    try: done={json.loads(l)['id'] for l in open(f'twin_all_W{W}.jsonl')}
    except FileNotFoundError: pass
    rows=[r for r in U['rows'] if r['id'] not in done]
    f=open(f'twin_all_W{W}.jsonl','a'); t0=time.time()
    with mp.Pool(mp.cpu_count()) as P:
        for i,o in enumerate(P.imap_unordered(one,rows,chunksize=2)):
            f.write(json.dumps(o)+'\n'); f.flush()
            if o.get('solved'): print('SOLVED',o['id'],o.get('verified'),len(o['path']),flush=True)
            if i%100==0: print(i,'done',round(time.time()-t0),'s',flush=True)
    print('done',flush=True)
