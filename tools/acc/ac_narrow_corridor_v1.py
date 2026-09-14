"""Exhaustive NARROW-corridor sweep over the whole ACC AC pool.
Calibration: all 424 shipped training trivializations use headroom <= 2
(94.6% use ZERO), so a +2 corridor should contain most solutions that exist.
Corridors this narrow exhaust in seconds, so every challenge gets a definite
verdict: certificate, or proof that none fits in +2."""
import json, subprocess, sys, os, pickle
sys.path.insert(0,"/home/user/saircompetition/andrews-curtis/competition/tools")
from verifier import core
AM=core.apply_move
man=json.load(open("/home/user/saircompetition/andrews-curtis/competition/tools/verifier/data/manifest.json"))
LIM=man["limits"]; C2P={1:0,-1:1,2:2,-2:3}
ac=[c for c in man["challenges"] if c["challenge_id"].startswith("ac-")]
BACK=pickle.load(open("/tmp/claude-0/back7.pkl","rb"))
def descend(s):
    out=[]; d=BACK[s]
    while d>0:
        for m in range(14):
            t=AM(s,m)
            if BACK.get(t,99)==d-1: out.append(m); s=t; d-=1; break
        else: raise RuntimeError("stuck")
    return out
EXTRA=int(sys.argv[1]); shard=int(sys.argv[2]); nsh=int(sys.argv[3]); BUD=sys.argv[4]
mine=[c for i,c in enumerate(ac) if i%nsh==shard]
out=open(f"/tmp/claude-0/narrow{EXTRA}_{shard}.jsonl","w")
env=dict(os.environ, AC_BALL="/tmp/claude-0/ball7.bin")
nc=ncl=nb=0
for k,c in enumerate(mine):
    cid=c["challenge_id"]; r0,r1=c["initial_relators"]; cap=len(r0)+len(r1)+EXTRA
    if cap>64: continue
    args=["/tmp/claude-0/c/corridor64b",str(cap),BUD,str(len(r0))]+[str(C2P[a]) for a in r0]+[str(len(r1))]+[str(C2P[a]) for a in r1]
    try: p=subprocess.run(args,capture_output=True,text=True,timeout=300,env=env)
    except subprocess.TimeoutExpired:
        out.write(json.dumps({"challenge_id":cid,"verdict":"timeout"})+"\n"); out.flush(); continue
    o=p.stdout.strip(); rec={"challenge_id":cid,"cap":cap,"init_len":len(r0)+len(r1)}
    if o.startswith("FOUND") or o.startswith("BALLHIT"):
        mv=[int(x) for x in o.split()[1:]]
        s=(tuple(r0),tuple(r1))
        for m in mv: s=AM(s,m)
        full=mv+(descend(s) if s!=((1,),(2,)) else [])
        v=core.verify({"challenge_id":cid,"move_spec_version":"ac-r2-v1",
            "initial_relators":[r0,r1],"target_relators":c["target_relators"]},full,"ac-r2-v1",LIM)
        rec.update(verdict="certificate",length=len(full),official_verify=bool(v.get("ok")),moves=full)
        nc+=1
    elif o.startswith("EXHAUSTED"):
        rec.update(verdict="closed",component=int(o.split("states=")[1].split()[0])); ncl+=1
    elif o.startswith("BUDGET"):
        rec.update(verdict="budget",states=int(o.split("states=")[1].split()[0])); nb+=1
    else: rec.update(verdict="other",raw=o[:50])
    out.write(json.dumps(rec)+"\n"); out.flush()
    if k%200==0: print(f"shard{shard} {k}/{len(mine)} certs={nc} closed={ncl} budget={nb}",flush=True)
print(f"shard{shard} DONE certs={nc} closed={ncl} budget={nb}",flush=True)
