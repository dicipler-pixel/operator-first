import json,subprocess,sys,time
C2P={1:0,-1:1,2:2,-2:3}
ENG="./bidir2"
def run(rel,cap,budget):
    a=[C2P[c] for c in rel[0]]; b=[C2P[c] for c in rel[1]]
    args=[ENG,str(cap),str(budget),str(len(a))]+[str(x) for x in a]+[str(len(b))]+[str(x) for x in b]+["1","0","1","2"]
    t=time.time()
    p=subprocess.run(args,capture_output=True,text=True,timeout=900)
    return p.stdout.split("\n")[0].strip(), time.time()-t
rows=json.load(open("calib_rows.json"))
budget=int(sys.argv[1]) if len(sys.argv)>1 else 3000000
print(f"budget {budget}/side")
print(f"{'id':10}{'|r|':>5}{'rec':>5}  " + "".join(f"cap{d:+d}".rjust(11) for d in (0,2,4,6,8,12,16)))
for r in rows:
    line=f"{r['id']:10}{r['ini']:5}{r['rec']:5}  "
    for d in (0,2,4,6,8,12,16):
        cap=r['ini']+d
        if cap>64: line+=f"{'-':>11}"; continue
        try:
            v,el=run(r['rel'],cap,budget)
        except subprocess.TimeoutExpired:
            v="TIMEOUT"; el=0
        tok=v.split()
        if tok and tok[0]=="MEET": s="M"+tok[1].split("=")[1]
        elif tok and tok[0].startswith("CLOSED"): s="CLOSED"
        elif tok and tok[0]=="BUDGET": s="budget"
        elif tok and tok[0]=="START_OUTSIDE_CAP": s="oob"
        else: s=(tok[0][:9] if tok else "?")
        line+=f"{s:>11}"
    print(line,flush=True)
