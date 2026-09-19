"""First real search pass over the 51 board presentations. Round-robin, bounded."""
import sys, json, time, datetime; sys.path.insert(0,'.')
from acc.solve import solve
from acc.moves import apply_move, TARGET
from acc.image_distance import lower_bound

P=json.load(open("config/presentations.json"))
TB=float(sys.argv[1]) if len(sys.argv)>1 else 45.0
CAP_OVER=int(sys.argv[2]) if len(sys.argv)>2 else 6
recs=[]; found=[]
t0=time.time()
for i,(suf,case) in enumerate(sorted(P["cases"].items()), 1):
    s=tuple(tuple(w) for w in case["initial_relators"])
    cap=case["total_length"]+CAP_OVER
    mv,stats = solve(s, length_cap=cap, time_budget=TB, max_nodes=3_000_000)
    rec={"run":f"board-ida-{suf}","phase":"first ordinary IDA* pass with admissible image-distance h",
         "result":"CERTIFICATE_CANDIDATE" if mv else "NO_CERTIFICATE",
         "stop_reason":stats.get("stop_reason"),
         "completeness_or_impossibility_claim":False,
         "raw_result_file":"runs/board-ida-pass1.json",
         "parameters_and_counts":{"challenge_id":case["ac_id"],"algorithm":"ida*-image-distance-p5p7",
            "start_total_length":case["total_length"],"length_cap":cap,
            "h0":stats.get("h0"),"final_bound":stats.get("final_bound"),
            "nodes":stats.get("nodes"),"seconds":stats.get("seconds"),
            "time_budget":TB,"found":bool(mv)}}
    if mv:
        v=s
        for m in mv: v=apply_move(v,m)
        rec["parameters_and_counts"]["moves"]=mv
        rec["parameters_and_counts"]["independent_replay_reached_target"]=(v==TARGET)
        found.append((suf,mv,v==TARGET))
    recs.append(rec)
    print(f"[{i:2}/51] ac-{suf}  cap{cap}  h0={stats.get('h0')}  "
          f"{rec['result']:22} {str(stats.get('stop_reason')):28} "
          f"{stats.get('nodes',0):>9,} nodes  {stats.get('seconds')}s", flush=True)

out={"finalized_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
     "pass":"board IDA* pass 1","time_budget_per_case":TB,"length_cap_over_start":CAP_OVER,
     "certificates_found":len(found),"records":recs,
     "correction_scope":"Bounded first pass. Every NO_CERTIFICATE is budget- or cap-limited, not an impossibility claim."}
json.dump(out, open("runs/board-ida-pass1.json","w"), indent=1)
print(f"\ntotal {time.time()-t0:.0f}s | certificates found: {len(found)}")
for suf,mv,ok in found: print(f"  ac-{suf}: {len(mv)} moves, replay ok={ok}")
