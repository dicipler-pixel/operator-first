"""Phase 3: splice and shorten, with the KILL CONDITION.
A candidate is prefix(A,0..i) + transport + suffix(B,j..end) for two runs meeting at the same
canonical state. Nothing is promoted unless it replays end to end and lands on the trivial
presentation. Transport is only attempted when the symmetry element is the identity; every
other element is logged as needing compilation, never assumed free."""
import json,os
from collections import defaultdict
from replay import replay, TARGET
HERE=os.path.dirname(os.path.abspath(__file__)); RUNS=os.path.join(HERE,"runs")

def load():
    R={}
    for fn in sorted(os.listdir(RUNS)):
        if fn.endswith(".json"): 
            b=json.load(open(os.path.join(RUNS,fn))); R[b["run_id"]]=b
    return R

def is_identity(e):
    return (e["gen"]==(0,0,0) and e["inv_r0"]==0 and e["rot_r0"]==0
            and e["inv_r1"]==0 and e["rot_r1"]==0 and e["swap"]==0)

def run(limit=None):
    R=load()
    idx=defaultdict(list)
    for rid,b in R.items():
        if not b["landed_on_target"]: continue
        for s in b["steps"]:
            idx[s["canonical_state_hash"]].append((rid,s["step"],s["symmetry_element"]))
    passed=[]; fails=[]
    seen=set()
    for h,entries in idx.items():
        if len(entries)<2: continue
        for (ra,ia,ea) in entries:
            for (rb,jb,eb) in entries:
                if ra==rb and ia>=jb: continue
                if (ra,ia,rb,jb) in seen: continue
                seen.add((ra,ia,rb,jb))
                A=R[ra]; B=R[rb]
                cand=A["moves"][:ia]+B["moves"][jb:]
                if len(cand)>=A["moves_total"] and ra==rb: continue
                r0,r1=A["initial_relators"]
                if not (is_identity(ea) and is_identity(eb)):
                    fails.append({"challenge_id":A["challenge_id"],"from":ra,"i":ia,
                                  "to":rb,"j":jb,"reason":"non-identity symmetry element; "
                                  "transport not compiled to primitive moves"})
                    continue
                a,b_,ok=replay(r0,r1,cand)
                if ok and len(cand)<A["moves_total"]:
                    passed.append({"challenge_id":A["challenge_id"],"new_len":len(cand),
                                   "old_len":A["moves_total"],"moves":cand,
                                   "from":ra,"i":ia,"to":rb,"j":jb})
                elif not ok:
                    fails.append({"challenge_id":A["challenge_id"],"from":ra,"i":ia,
                                  "to":rb,"j":jb,"reason":"replay did not reach trivial"})
                if limit and len(fails)+len(passed)>limit: break
    return passed,fails

if __name__=="__main__":
    p,f=run()
    print("splice candidates PASSED (replayed to trivial AND shorter):",len(p))
    print("splice candidates FAILED:",len(f))
    from collections import Counter
    print(Counter(x["reason"] for x in f))
    best=sorted(p,key=lambda x:x["new_len"]-x["old_len"])[:20]
    for x in best:
        print(f"  {x['challenge_id']}: {x['old_len']} -> {x['new_len']}  (saving {x['old_len']-x['new_len']})")
    json.dump(p,open(os.path.join(HERE,"SPLICE_PASSED_20260916.json"),"w"),indent=1)
    with open(os.path.join(HERE,"SPLICE_FAILS_20260916.jsonl"),"w") as fh:
        for x in f: fh.write(json.dumps(x)+"\n")
