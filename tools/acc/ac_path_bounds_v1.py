"""Turn a budget-limited bidirectional run into a LOWER BOUND on path length.

Both sides run complete BFS levels, so when the run stops without meeting,
the forward ball of radius df and the backward ball of radius db are each
complete and provably disjoint. Any path of length L <= df + db would place
some vertex in both. So no solution of length <= df + db exists at that cap.
"""
import json, subprocess, sys, re
sys.path.insert(0,'/tmp/claude-0')
from bidir_run import R, av
ENG="/tmp/claude-0/c/corridor64bi"
JOBS=[("ac-02422",23),("ac-01083",23),("ac-01558",23),("ac-01956",23),
      ("ac-02828",23),("ac-00399",21)]
BUD=20_000_000
out=open('/tmp/claude-0/bounds.jsonl','w')
for cid,cap in JOBS:
    args=[ENG,str(cap),str(BUD)]+av(R[cid])+av([[1],[2]])
    p=subprocess.run(args,capture_output=True,text=True,timeout=2400)
    o=p.stdout.strip()
    m=re.search(r"states_f=(\d+) states_b=(\d+) depth_f=(\d+) depth_b=(\d+)",o)
    if o.startswith("MEET"):
        print(f"{cid}: MEET {o.splitlines()[0]}"); continue
    sf,sb,df,db=map(int,m.groups())
    rec={"id":cid,"cap":cap,"states_f":sf,"states_b":sb,"depth_f":df,"depth_b":db,
         "bound":df+db,"claim":f"no solution of length <= {df+db} at cap {cap}"}
    out.write(json.dumps(rec)+"\n"); out.flush()
    print(f"{cid} cap={cap}: fwd r={df} ({sf:,})  bwd r={db} ({sb:,})  "
          f"-> NO PATH <= {df+db}",flush=True)
out.close(); print("DONE")
