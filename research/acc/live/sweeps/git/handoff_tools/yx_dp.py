# SCRIPT: YX_DP  keep each road's class sequence, but have the DP end at (y,x) instead of (x,y).
# Stable line = DP route to (y,x) + [15,15]. Tight and loose settings.
import json,sys,signal,time
import skel_dp_fixed as SD
R=json.load(open('../midk/newlist_roads.json')); YX=((2,),(1,))
Q='/home/claude/rally/research/acc/live/queue/'
for c,tgt in (('ac-02288',38),('ac-04493',53)):
    t=SD.T[c]; st=tuple(tuple(r) for r in t['initial_relators'])
    roads=[p for p in R[c] if SD.core.verify(t,p,'ac-r2-v1',SD.rl.LIMITS)['ok']]
    best=None
    for p in sorted(roads,key=len):
        for cfg in ((1,3,8),(2,4,16),(2,6,24)):
            signal.alarm(240)
            try: out=SD.solve(st,YX,SD.road(st,p),*cfg)
            except SD._TO: out='timeout'
            finally: signal.alarm(0)
            n=len(out)+2 if isinstance(out,list) else out
            if isinstance(out,list):
                s=st
                for m in out: s=SD.core.apply_move(s,m)
                assert s==YX
                if best is None or len(out)<len(best): best=out
            print(c,'road',len(p),'cfg',cfg,'-> SAC',n,'record',tgt,flush=True)
    if best and len(best)+2<=tgt:
        line=best+[15,15]
        open(Q+time.strftime('%Y%m%dT%H%M%SZ',time.gmtime())+'_git_s'+c+'.txt','w').write(f"# git: DP to (y,x) on our class road, route {len(best)} (end (y,x) checked on AC core) + [15,15] = {len(line)} vs Stable record {tgt}. Please run the official Stable verifier. [skip ci]\ns{c}: {json.dumps(line)}\n")
        print('QUEUED s'+c,len(line),flush=True)
