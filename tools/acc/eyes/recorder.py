"""Phase 1 recorder. Replays a trajectory from its official start presentation and emits
per-step eye channels to runs/<run_id>.json, appending a hash-chained line to EVENTS.jsonl.
Eyes are telemetry only: nothing here prunes a search or certifies anything."""
import json,hashlib,os,sys
from replay import (apply_move, free_reduce, invert, cyclic_reduce, expsum,
                    penultimate_proximity, MOVE_CLASS, TARGET)
from canon import canonical_hash

EYE_SET_VERSION="eyes-v1"
HERE=os.path.dirname(os.path.abspath(__file__))
RUNS=os.path.join(HERE,"runs"); os.makedirs(RUNS,exist_ok=True)
EVENTS=os.path.join(HERE,"EVENTS.jsonl")

def _step_record(step,move_id,r0,r1,prev_total):
    tot=len(r0)+len(r1)
    ch,elem=canonical_hash(r0,r1)
    e0=expsum(r0); e1=expsum(r1)
    return {
        "step":step,"move_id":move_id,
        "move_class":(MOVE_CLASS[move_id] if move_id is not None else None),
        "len_r1":len(r0),"len_r2":len(r1),"len_total":tot,
        "len_delta":(None if prev_total is None else tot-prev_total),
        "cyclic_reduced_len_r1":len(cyclic_reduce(r0)),
        "cyclic_reduced_len_r2":len(cyclic_reduce(r1)),
        "expsum_x_r1":e0[0],"expsum_y_r1":e0[1],
        "expsum_x_r2":e1[0],"expsum_y_r2":e1[1],
        "penultimate_proximity":penultimate_proximity(r0,r1),
        "canonical_state_hash":ch,"symmetry_element":elem,
        "verifier_ok":((tuple(r0),tuple(r1))==TARGET),
    }

def record_run(run_id,challenge_id,r0,r1,moves,outcome,provenance):
    a,b=list(r0),list(r1)
    steps=[_step_record(0,None,a,b,None)]
    prev=len(a)+len(b)
    for i,m in enumerate(moves,1):
        a,b=apply_move(a,b,m)
        steps.append(_step_record(i,m,a,b,prev))
        prev=len(a)+len(b)
    landed=(tuple(a),tuple(b))==TARGET
    body={"run_id":run_id,"challenge_id":challenge_id,"outcome":outcome,
          "final_len":len(a)+len(b),"moves_total":len(moves),
          "landed_on_target":landed,
          "replay_authority":"eyes/replay.py",
          "eye_set_version":EYE_SET_VERSION,
          "provenance":provenance,
          "initial_relators":[list(r0),list(r1)],"moves":list(moves),
          "steps":steps}
    body["sha256"]=hashlib.sha256(json.dumps(
        {k:v for k,v in body.items() if k!="sha256"},sort_keys=True).encode()).hexdigest()
    with open(os.path.join(RUNS,f"{run_id}.json"),"w") as f: json.dump(body,f)
    return body

def chain_append(body):
    prev="0"*64
    if os.path.exists(EVENTS):
        with open(EVENTS) as f:
            for line in f: pass
            try: prev=json.loads(line)["this_hash"]
            except Exception: pass
    ev={"run_id":body["run_id"],"challenge_id":body["challenge_id"],
        "outcome":body["outcome"],"moves_total":body["moves_total"],
        "landed_on_target":body["landed_on_target"],
        "run_sha256":body["sha256"],"prev_hash":prev}
    ev["this_hash"]=hashlib.sha256(json.dumps(ev,sort_keys=True).encode()).hexdigest()
    with open(EVENTS,"a") as f: f.write(json.dumps(ev)+"\n")
    return ev["this_hash"]

def chain_head():
    if not os.path.exists(EVENTS): return None
    h=None
    with open(EVENTS) as f:
        for line in f: h=json.loads(line)["this_hash"]
    return h
