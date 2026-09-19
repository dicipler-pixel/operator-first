"""Re-run every challenge a log says MEET, so certificates survive an unfinished sweep.

The sweep only writes its JSON at the end and the log line carries no move
list, so a killed run would lose its finds.  The engine is deterministic and
fast, so recomputing is cheap and the certificate is re-derived rather than
trusted.
"""
import sys, re, json, glob, datetime
sys.path.insert(0,'engines'); sys.path.insert(0,'vendor'); sys.path.insert(0,'.')
from run_corridor import run, manifest
from verifier import core
LIM={"max_path_length":100000,"max_total_relator_length":10000,"max_work":5000000}

pat=re.compile(r"\*\*\* (ac-\d+) cap(\d+): MEET")
todo={}
for path in sys.argv[1:]:
    for line in open(path, errors="ignore"):
        m=pat.search(line)
        if m: todo[m.group(1)]=int(m.group(2))
print(f"{len(todo)} MEET rows named across the logs")

found=[]
for i,(cid,cap) in enumerate(sorted(todo.items()),1):
    r=run(cid,cap,20_000_000,timeout=600)
    if r["verdict"]!="MEET" or not r["moves"]:
        print(f"  {cid}: did not reproduce ({r['verdict']})"); continue
    ok=core.verify(manifest()[cid], r["moves"], "ac-r2-v1", LIM).get("ok")
    if not ok:
        print(f"  {cid}: REPRODUCED BUT FAILED VERIFIER"); continue
    found.append({"challenge_id":cid,"cap":cap,"move_count":len(r["moves"]),
                  "moves":r["moves"],"official_verifier_ok":True})
    if i%20==0: print(f"  ...{i}/{len(todo)}",flush=True)
json.dump({"finalized_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
   "source":"re-run of MEET rows named in sweep logs","certificates_found":len(found),
   "found":found,"records":[]}, open("runs/pool-harvest.json","w"), indent=1)
print(f"harvested {len(found)} verified certificates -> runs/pool-harvest.json")
