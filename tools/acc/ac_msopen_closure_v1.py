"""Closure profile across every MS-open challenge of length <= 15.

These are k=0 rows: nobody has solved one, so ANY verified path scores the
full point. Narrow caps are cheap, and a MEET at any cap is a certificate.
Each challenge is walked from headroom 1 upward until it stops closing.
"""
import json, subprocess, sys, time
sys.path.insert(0,'/tmp/claude-0')
from bidir_run import R, av
ENG="/tmp/claude-0/c/corridor64bi2"
BUD=20_000_000
ids=json.load(open('/tmp/claude-0/msopen_short.json'))
out=open('/tmp/claude-0/msopen_sweep.jsonl','w')
solves=0
for cid in ids:
    L=sum(len(w) for w in R[cid]); rows=[]; verdict="none"; t0=time.time()
    for hr in range(1,9):
        cap=L+hr
        a=[ENG,str(cap),str(BUD)]+av(R[cid])+av([[1],[2]])
        try: o=subprocess.run(a,capture_output=True,text=True,timeout=2400).stdout.strip()
        except subprocess.TimeoutExpired: rows.append([cap,"timeout",None]); break
        lines=o.splitlines(); ln=lines[0] if lines else ""
        if ln.startswith("MEET"):
            n=int(ln.split("len=")[1].split()[0])
            mv=[int(x) for x in lines[1].split()[1:]] if len(lines)>1 else []
            rows.append([cap,"MEET",n]); verdict="SOLVED"; solves+=1
            out.write(json.dumps({"id":cid,"len":L,"cap":cap,"solved":True,
                                  "length":n,"moves":mv})+"\n"); out.flush()
            print(f"*** {cid} SOLVED at cap {cap}: {n} moves ***",flush=True)
            break
        if ln.startswith("CLOSED_F"):
            rows.append([cap,"closed",int(ln.split("component=")[1].split()[0])])
        else:
            rows.append([cap,"budget",None]); break
    if verdict!="SOLVED":
        closed=[r for r in rows if r[1]=="closed"]
        out.write(json.dumps({"id":cid,"len":L,"solved":False,"rows":rows,
                              "max_closed_cap":closed[-1][0] if closed else None})+"\n")
        out.flush()
        top=f"closed<=cap{closed[-1][0]}({closed[-1][2]:,})" if closed else "no closure"
        print(f"{cid} len={L}: {top} [{time.time()-t0:.0f}s]",flush=True)
out.close(); print(f"DONE  solves={solves}")
