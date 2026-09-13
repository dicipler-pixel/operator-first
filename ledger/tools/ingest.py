import json, sys, os
LEDGER=os.environ.get('LEDGER_WORKDIR', os.path.dirname(os.path.abspath(__file__)))
out=os.path.join(LEDGER,'branch_runs.json')
if os.path.exists(out):
    data=json.load(open(out))
else:
    data={}
    for line in open(os.path.join(LEDGER,'branches.txt')):
        b,p=line.split()
        data[b]={"head_prefix":p,"runs":[]}
# usage: ingest.py <branch> <file-with-json> [--append]
branch=sys.argv[1]; f=sys.argv[2]
txt=open(f).read()
try:
    obj=json.loads(txt)
    if isinstance(obj,list): res=json.loads(obj[0]["text"])
    else: res=obj
except Exception:
    i=txt.find('{'); j=txt.rfind('}')
    res=json.loads(txt[i:j+1])
prefix=data[branch]["head_prefix"]
runs=[r for r in res["workflow_runs"] if r["head_sha"].startswith(prefix)]
seen={r["run_id"] for r in data[branch]["runs"]}
for r in runs:
    if r["id"] in seen: continue
    data[branch]["runs"].append({"workflow":r["path"],"run_id":r["id"],"conclusion":r["conclusion"],"event":r["event"],"created_at":r["created_at"]})
json.dump(data,open(out,'w'),indent=1)
print(branch, "total_count=",res["total_count"], "returned=",len(res["workflow_runs"]), "matched=",len(runs), "now=",len(data[branch]["runs"]))
