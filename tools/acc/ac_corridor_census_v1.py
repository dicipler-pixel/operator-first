"""Unbiased corridor census: uniform random sample of the FULL ACC AC pool,
each run at headroom +8 with a budget large enough that a decent fraction close.
Records: certificate | corridor-closed (with volume) | budget (no information)."""
import json, subprocess, sys, random, os
sys.path.insert(0,"/home/user/saircompetition/andrews-curtis/competition/tools")
from verifier import core
man=json.load(open("/home/user/saircompetition/andrews-curtis/competition/tools/verifier/data/manifest.json"))
LIM=man["limits"]; C2P={1:0,-1:1,2:2,-2:3}
ac=[c for c in man["challenges"] if c["challenge_id"].startswith("ac-")]
def ln(c): return len(c["initial_relators"][0])+len(c["initial_relators"][1])
N=int(sys.argv[1]); budget=sys.argv[2]; shard=int(sys.argv[3]); nsh=int(sys.argv[4])
rng=random.Random(20260914)          # fixed seed: the sample is reproducible
sample=rng.sample(ac,N)
mine=[c for i,c in enumerate(sample) if i%nsh==shard]
out=open(f"/tmp/claude-0/sample_{shard}.jsonl","w")
print(f"shard {shard}: {len(mine)} of a {N}-challenge uniform sample",flush=True)
for k,c in enumerate(mine):
    cid=c["challenge_id"]; r0,r1=c["initial_relators"]; cap=ln(c)+8
    if cap>64:
        out.write(json.dumps({"challenge_id":cid,"skipped":"cap>64"})+"\n"); continue
    args=["/tmp/claude-0/c/corridor64",str(cap),budget,str(len(r0))]+[str(C2P[a]) for a in r0]+[str(len(r1))]+[str(C2P[a]) for a in r1]
    try: r=subprocess.run(args,capture_output=True,text=True,timeout=600)
    except subprocess.TimeoutExpired:
        out.write(json.dumps({"challenge_id":cid,"verdict":"timeout","init_len":ln(c),"cap":cap})+"\n"); out.flush(); continue
    o=r.stdout.strip()
    rec={"challenge_id":cid,"init_len":ln(c),"cap":cap}
    if o.startswith("FOUND"):
        mv=[int(x) for x in o.split()[1:]]
        v=core.verify({"challenge_id":cid,"move_spec_version":"ac-r2-v1",
            "initial_relators":[r0,r1],"target_relators":c["target_relators"]},mv,"ac-r2-v1",LIM)
        rec.update(verdict="certificate",length=len(mv),official_verify=bool(v.get("ok")),moves=mv)
    elif o.startswith("EXHAUSTED"):
        rec.update(verdict="closed",component=int(o.split("states=")[1].split()[0]),
                   depth=int(o.split("depth=")[1].split()[0]))
    elif o.startswith("BUDGET"):
        rec.update(verdict="budget",states=int(o.split("states=")[1].split()[0]))
    else: rec.update(verdict="other",raw=o[:60])
    out.write(json.dumps(rec)+"\n"); out.flush()
    if k%10==0: print(f"  shard{shard} {k}/{len(mine)}",flush=True)
print(f"shard {shard} DONE",flush=True)
