import json,subprocess,sys,os,re,math,time
C2P={1:0,-1:1,2:2,-2:3}
ENG=os.path.abspath("./bidir2")
def curve(rel,cap,budget,to=3000):
    a=[C2P[c] for c in rel[0]]; b=[C2P[c] for c in rel[1]]
    args=[ENG,str(cap),str(budget),str(len(a))]+[str(x) for x in a]+[str(len(b))]+[str(x) for x in b]+["1","0","1","2"]
    p=subprocess.run(args,capture_output=True,text=True,timeout=to)
    F=[]
    for ln in p.stderr.split("\n"):
        m=re.match(r"F depth (\d+) states (\d+)",ln.strip())
        if m: F.append((int(m.group(1)),int(m.group(2))))
    return p.stdout.split("\n")[0].strip(),F
def collapse_depth(F,thresh=1.5,win=4):
    # first depth where local growth base over a sliding window drops below thresh
    for i in range(win,len(F)):
        d0,n0=F[i-win]; d1,n1=F[i]
        if n0<100: continue
        b=(n1/n0)**(1.0/(d1-d0)) if d1>d0 else 9
        if b<thresh: return d1,b
    return None,None
rows=json.load(open(sys.argv[1]))
sel={r["id"]:r for r in rows}
targets=sys.argv[2].split(",")
budget=int(sys.argv[3])
out=open(sys.argv[4],"a")
for tid in targets:
    r=sel[tid]
    for d in (2,4,6,8,10,12,14,16):
        cap=r["ini"]+d
        if cap>64: continue
        t=time.time()
        try: v,F=curve(r["rel"],cap,budget)
        except subprocess.TimeoutExpired: print(f"{tid} cap={cap} TIMEOUT",flush=True); continue
        cd,cb=collapse_depth(F)
        rec={"id":tid,"ini":r["ini"],"cap":cap,"verdict":v,"maxdepth":F[-1][0] if F else 0,
             "collapse_depth":cd,"collapse_base":cb,"F":F,"secs":round(time.time()-t,1)}
        out.write(json.dumps(rec)+"\n"); out.flush()
        print(f"{tid} cap={cap:3} {v.split()[0]:9} maxdepth={rec['maxdepth']:4} collapse_d*={cd} [{rec['secs']}s]",flush=True)
