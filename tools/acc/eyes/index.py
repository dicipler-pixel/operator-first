"""Phase 2: build STATE_INDEX.jsonl and the rediscovery report.
Index maps canonical_state_hash -> [(run_id, step, remaining_moves_to_trivial, symmetry_element)].
Telemetry and indexing only; nothing here prunes or certifies."""
import json,os,sys
from collections import defaultdict
HERE=os.path.dirname(os.path.abspath(__file__))
RUNS=os.path.join(HERE,"runs")

def build():
    idx=defaultdict(list); meta={}
    for fn in sorted(os.listdir(RUNS)):
        if not fn.endswith(".json"): continue
        b=json.load(open(os.path.join(RUNS,fn)))
        rid=b["run_id"]; cid=b["challenge_id"]; tot=b["moves_total"]
        landed=b["landed_on_target"]
        meta[rid]={"challenge_id":cid,"outcome":b["outcome"],"moves_total":tot,
                   "landed":landed}
        for s in b["steps"]:
            rem=(tot-s["step"]) if landed else None
            idx[s["canonical_state_hash"]].append(
                {"run_id":rid,"step":s["step"],"remaining_moves_to_trivial":rem,
                 "symmetry_element":s["symmetry_element"]})
    return idx,meta

def report(idx,meta):
    cross=[]; fail_on_solved=[]; shorter=[]
    for h,entries in idx.items():
        if len(entries)<2: continue
        cids={meta[e["run_id"]]["challenge_id"] for e in entries}
        if len(cids)>1: cross.append((h,entries))
        solved=[e for e in entries if meta[e["run_id"]]["landed"]]
        unsolved=[e for e in entries if not meta[e["run_id"]]["landed"]]
        if solved and unsolved: fail_on_solved.append((h,entries))
        bycid=defaultdict(list)
        for e in entries: bycid[meta[e["run_id"]]["challenge_id"]].append(e)
        for cid,es in bycid.items():
            rems={e["remaining_moves_to_trivial"] for e in es if e["remaining_moves_to_trivial"] is not None}
            if len(rems)>1: shorter.append((h,cid,sorted(rems)))
    return cross,fail_on_solved,shorter

if __name__=="__main__":
    idx,meta=build()
    with open(os.path.join(HERE,"STATE_INDEX.jsonl"),"w") as f:
        for h,e in idx.items(): f.write(json.dumps({"canonical_state_hash":h,"entries":e})+"\n")
    cross,fos,shorter=report(idx,meta)
    print("runs indexed          :",len(meta))
    print("distinct canonical states:",len(idx))
    print("states seen >=2 times  :",sum(1 for e in idx.values() if len(e)>1))
    print("cross-target rediscoveries:",len(cross))
    print("failed-run states on a solved run:",len(fos))
    print("same-challenge shortening candidates:",len(shorter))
    if shorter:
        shorter.sort(key=lambda t:-(max(t[2])-min(t[2])))
        print("\ntop shortening candidates (saving = max-min remaining):")
        for h,cid,rems in shorter[:50]:
            print(f"  {cid} saving={max(rems)-min(rems)} remaining={rems} {h[:16]}")
    if cross:
        print("\ntop cross-target rediscoveries:")
        for h,e in cross[:50]:
            cids=sorted({meta[x['run_id']]['challenge_id'] for x in e})
            print(f"  {h[:16]} challenges={cids}")
