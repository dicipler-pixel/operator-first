"""Closure profile: the largest cap at which a challenge is PROVED
disconnected from the AC target.

v1 of the bidirectional engine only said EXHAUSTED when both frontiers
emptied, so these theorems were being reported as BUDGET. Narrow caps are
cheap -- ac-02422 closes at cap 19 in 449k states -- so the profile costs
far less than one headroom-8 run.
"""
import json, subprocess, sys, re
sys.path.insert(0,'/tmp/claude-0')
from bidir_run import R, av
ENG="/tmp/claude-0/c/corridor64bi2"
IDS=["ac-02422","ac-01083","ac-01558","ac-01956","ac-02828","ac-00399",
     "ac-00638","ac-06600","ac-08027","ac-05058"]
BUD=20_000_000
out=open('/tmp/claude-0/closure.jsonl','w')
for cid in IDS:
    L=sum(len(w) for w in R[cid]); best=None; rows=[]
    for hr in range(1,9):
        cap=L+hr
        if cap>64: break
        a=[ENG,str(cap),str(BUD)]+av(R[cid])+av([[1],[2]])
        try: o=subprocess.run(a,capture_output=True,text=True,timeout=1800).stdout.strip()
        except subprocess.TimeoutExpired: rows.append((cap,"timeout",None)); break
        ln=o.splitlines()[0] if o else ""
        if ln.startswith("MEET"):
            rows.append((cap,"MEET",int(ln.split("len=")[1].split()[0]))); best=("MEET",cap); break
        if ln.startswith("CLOSED_F"):
            n=int(ln.split("component=")[1].split()[0]); rows.append((cap,"closed",n)); best=(cap,n)
        else:
            rows.append((cap,"budget",None)); break
    rec={"id":cid,"len":L,"rows":rows,"max_closed_cap":best}
    out.write(json.dumps(rec)+"\n"); out.flush()
    s=" ".join(f"{c}:{v}{'' if n is None else '('+format(n,',')+')'}" for c,v,n in rows)
    print(f"{cid} len={L}  {s}", flush=True)
out.close(); print("DONE")
