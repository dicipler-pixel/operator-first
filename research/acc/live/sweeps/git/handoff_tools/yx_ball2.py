# SCRIPT: YX_BALL  DP keeps our class road but stores EVERY orientation state it reaches in every class (with cost);
# a backward ball around (y,x) (depth BD) meets them. Stable line = DP prefix + ball route to (y,x) + [15,15].
import json,sys,heapq,time,signal
import skel_dp_fixed as SD
core=SD.core; INV=(0,1,3,2,5,4,7,6,9,8,11,10,13,12); YX=((2,),(1,))
BD=int(sys.argv[1]) if len(sys.argv)>1 else 6
def ball(T,d,cap=int(__import__("os").environ.get("BCAP","16"))):
    B={T:[]}; fr=[T]
    for _ in range(d):
        nf=[]
        for s in fr:
            for m in range(14):
                y=core.apply_move(s,m)
                if y in B or len(y[0])+len(y[1])>cap: continue
                B[y]=[INV[m]]+B[s]; nf.append(y)
        fr=nf
    return B
def sweep(start,R,GROW,SLACK,MAXC,Bl,budget):
    # same as SD.solve but checks every settled state against the ball
    front={start:(0,None,None)}; parents={}; best=None
    for k in range(len(R)):
        dist={}; pq=[(c,i,s) for i,(s,(c,_,_)) in enumerate(front.items())]; heapq.heapify(pq); par=dict(front)
        best0=min(c for c,_,_ in pq); cnt=len(pq)
        while pq:
            c,_,s=heapq.heappop(pq)
            if s in dist: continue
            dist[s]=c
            if s in Bl and c+len(Bl[s])<=budget and (best is None or c+len(Bl[s])<best[0]): best=(c+len(Bl[s]),k,s)
            if c>best0+MAXC: continue
            for m in SD.INNER:
                t=core.apply_move(s,m)
                if t in dist: continue
                if any(len(t[i])>len(SD.cyc(t[i]))+2*GROW and len(t[i])>len(s[i]) for i in (0,1)): continue
                if t not in par or par[t][0]>c+1: par[t]=(c+1,s,m); cnt+=1; heapq.heappush(pq,(c+1,cnt,t))
        for s in dist: parents[(k,s)]=par[s]
        if k==len(R)-1: break
        nxt={}; lo=min(dist.values())
        for s,c in dist.items():
            if c>lo+SLACK+MAXC: continue
            for m in SD.MULT:
                t=core.apply_move(s,m)
                if SD.cls(t)==R[k+1] and (t not in nxt or nxt[t][0]>c+1): nxt[t]=(c+1,('X',s),m)
        if not nxt: break
        lo=min(v[0] for v in nxt.values()); front={t:v for t,v in nxt.items() if v[0]<=lo+SLACK}
    if not best: return None
    _,kk,s=best; out=[]
    while True:
        c,p,m=parents[(kk,s)]
        if p is None: break
        out.append(m)
        if isinstance(p,tuple) and len(p)==2 and p[0]=='X': kk,s=kk-1,p[1]
        else: s=p
    return out[::-1]+Bl[best[2]]
R=json.load(open('../midk/newlist_roads.json')); Q='/home/claude/rally/research/acc/live/queue/'
t0=time.time(); Bl=ball(YX,BD); print('ball',BD,len(Bl),round(time.time()-t0),'s',flush=True)
for c,tgt in (('ac-02288',38),('ac-04493',53)):
    t=SD.T[c]; st=tuple(tuple(r) for r in t['initial_relators'])
    for p in sorted([p for p in R[c] if core.verify(t,p,'ac-r2-v1',SD.rl.LIMITS)['ok']],key=len):
        for cfg in ((1,3,8),(2,4,16)):
            signal.alarm(300)
            try: x=sweep(st,SD.road(st,p),*cfg,Bl,tgt-2)
            except SD._TO: x='timeout'
            finally: signal.alarm(0)
            ok=False
            if isinstance(x,list):
                s=st
                for m in x: s=core.apply_move(s,m)
                ok=s==YX
            print(c,'road',len(p),'cfg',cfg,'->',(len(x)+2 if isinstance(x,list) else x),'ok' if ok else '',flush=True)
            if ok:
                line=x+[15,15]
                open(Q+time.strftime('%Y%m%dT%H%M%SZ',time.gmtime())+'_git_s'+c+'.txt','w').write(f"# git: DP over our class road + ball to (y,x); route {len(x)} (end (y,x) checked on AC core) + [15,15] = {len(line)} vs Stable record {tgt}. Please run the official Stable verifier. [skip ci]\ns{c}: {json.dumps(line)}\n")
                print('QUEUED s'+c,len(line),flush=True); break
        else: continue
        break
