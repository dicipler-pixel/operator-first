import json,subprocess,sys,os,re,math,time
C2P={1:0,-1:1,2:2,-2:3}
ENG=os.path.abspath("./bidir2")
def curve(rel,cap,budget,to=2400):
    a=[C2P[c] for c in rel[0]]; b=[C2P[c] for c in rel[1]]
    args=[ENG,str(cap),str(budget),str(len(a))]+[str(x) for x in a]+[str(len(b))]+[str(x) for x in b]+["1","0","1","2"]
    p=subprocess.run(args,capture_output=True,text=True,timeout=to)
    F=[];B=[]
    for ln in p.stderr.split("\n"):
        m=re.match(r"([FB]) depth (\d+) states (\d+)",ln.strip())
        if m: (F if m.group(1)=="F" else B).append((int(m.group(2)),int(m.group(3))))
    return p.stdout.split("\n")[0].strip(),F,B
def fit(c):
    # cumulative states vs depth; return (poly_exponent, exp_base) over last half
    pts=[(d,n) for d,n in c if d>=3 and n>1]
    if len(pts)<6: return None
    pts=pts[len(pts)//2:]
    xs=[math.log(d) for d,_ in pts]; ys=[math.log(n) for _,n in pts]
    n=len(xs); sx=sum(xs); sy=sum(ys); sxx=sum(x*x for x in xs); sxy=sum(x*y for x,y in zip(xs,ys))
    alpha=(n*sxy-sx*sy)/(n*sxx-sx*sx+1e-12)
    xs2=[d for d,_ in pts]
    sx2=sum(xs2); sxx2=sum(x*x for x in xs2); sxy2=sum(x*y for x,y in zip(xs2,ys))
    beta=(n*sxy2-sx2*sy)/(n*sxx2-sx2*sx2+1e-12)
    # residuals to decide which model fits
    a0=(sy-alpha*sx)/n; b0=(sy-beta*sx2)/n
    rp=sum((y-(a0+alpha*x))**2 for x,y in zip(xs,ys))
    re_=sum((y-(b0+beta*x))**2 for x,y in zip(xs2,ys))
    return alpha,math.exp(beta),rp,re_
rows=json.load(open(sys.argv[1]))
budget=int(sys.argv[2]); delta=int(sys.argv[3]); lo=int(sys.argv[4]); hi=int(sys.argv[5])
out=open(sys.argv[6],"a")
for r in rows[lo:hi]:
    cap=r["ini"]+delta
    t=time.time()
    try: v,F,B=curve(r["rel"],cap,budget)
    except subprocess.TimeoutExpired: continue
    ff=fit(F); bf=fit(B)
    rec={"id":r["id"],"ini":r["ini"],"cap":cap,"verdict":v,"rec":r.get("rec",0),
         "F":F,"B":B,"fitF":ff,"fitB":bf,"secs":round(time.time()-t,1)}
    out.write(json.dumps(rec)+"\n"); out.flush()
    if ff: print(f"{r['id']} cap={cap} {v.split()[0]:9} depthF={F[-1][0] if F else 0:4} polyExp={ff[0]:6.2f} expBase={ff[1]:6.3f} residPoly={ff[2]:9.3f} residExp={ff[3]:9.3f}",flush=True)
