import json, sys, os
# usage: add.py <branch>  ; stdin lines: workflow run_id conclusion event created_at
out=os.path.join(os.environ.get('LEDGER_WORKDIR', os.path.dirname(os.path.abspath(__file__))),'branch_runs.json')
data=json.load(open(out)); b=sys.argv[1]
seen={r["run_id"] for r in data[b]["runs"]}
n=0
for line in sys.stdin:
    p=line.split()
    if not p: continue
    rid=int(p[1])
    if rid in seen: continue
    data[b]["runs"].append({"workflow":".github/workflows/"+p[0],"run_id":rid,"conclusion":p[2],"event":p[3],"created_at":p[4]}); n+=1
json.dump(data,open(out,'w'),indent=1)
print(b,"added",n,"now",len(data[b]["runs"]))
