import json,subprocess,sys,time,os
C2P={1:0,-1:1,2:2,-2:3}
ENG=os.path.abspath("./bidir2")
def run(rel,cap,budget,to=1800):
    a=[C2P[c] for c in rel[0]]; b=[C2P[c] for c in rel[1]]
    args=[ENG,str(cap),str(budget),str(len(a))]+[str(x) for x in a]+[str(len(b))]+[str(x) for x in b]+["1","0","1","2"]
    p=subprocess.run(args,capture_output=True,text=True,timeout=to)
    return p.stdout.strip()
rows=json.load(open(sys.argv[1]))
budget=int(sys.argv[2]); deltas=[int(x) for x in sys.argv[3].split(",")]
lo=int(sys.argv[4]); hi=int(sys.argv[5])
res=open(sys.argv[6],"a")
for r in rows[lo:hi]:
    for d in deltas:
        cap=r["ini"]+d
        if cap>64: continue
        t=time.time()
        try: v=run(r["rel"],cap,budget)
        except subprocess.TimeoutExpired: v="TIMEOUT"
        head=v.split("\n")[0]
        rec={"id":r["id"],"ini":r["ini"],"cap":cap,"verdict":head,"secs":round(time.time()-t,1)}
        if head.startswith("MEET"):
            rec["moves"]=v.split("MOVES")[-1].strip()
        res.write(json.dumps(rec)+"\n"); res.flush()
        print(f"{r['id']} cap={cap} {head} [{rec['secs']}s]",flush=True)
        if head.startswith("MEET"): break
