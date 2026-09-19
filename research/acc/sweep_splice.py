"""Splice pass: big exact suffix dictionary, forward ball from each board start."""
import sys, json, time, datetime; sys.path.insert(0,'.'); sys.path.insert(0,'vendor')
from acc.splice import SuffixDictionary, forward_splice
from acc.moves import apply_move, TARGET
from verifier import core

SAIR="/home/user/saircompetition/andrews-curtis"
LIM={"max_path_length":100000,"max_total_relator_length":10000,"max_work":5000000}
BACK_DEPTH=int(sys.argv[1]); BACK_CAP=int(sys.argv[2])
FWD_DEPTH=int(sys.argv[3]); FWD_OVER=int(sys.argv[4])

T=json.load(open(f"{SAIR}/competition/examples/training_424.json"))["instances"]
sd=SuffixDictionary()
for r in T:
    sd.add_certificate_path(tuple(tuple(w) for w in r["initial_relators"]), r["moves"], "training-424")
t=time.time()
sd.add_backward_ball(depth=BACK_DEPTH, length_cap=BACK_CAP, max_states=6_000_000)
print(f"suffix dictionary: {len(sd):,} exact states "
      f"(backward depth {BACK_DEPTH} cap {BACK_CAP}) in {time.time()-t:.0f}s", flush=True)

P=json.load(open("config/presentations.json"))
recs=[]; found=[]
for i,(suf,case) in enumerate(sorted(P["cases"].items()),1):
    s=tuple(tuple(w) for w in case["initial_relators"])
    cap=case["total_length"]+FWD_OVER
    t0=time.time()
    mv,stats=forward_splice(s, sd, depth=FWD_DEPTH, length_cap=cap, max_states=1_200_000)
    rec={"run":f"splice-{suf}","phase":"suffix-splice meet-in-the-middle",
         "result":"CERTIFICATE_CANDIDATE" if mv else "NO_CERTIFICATE",
         "stop_reason":stats.get("stop_reason"),
         "completeness_or_impossibility_claim":False,
         "raw_result_file":"runs/board-splice-pass1.json",
         "parameters_and_counts":{"challenge_id":case["ac_id"],
            "algorithm":"forward-ball x exact-suffix-dictionary",
            "dictionary_states":len(sd),"backward_depth":BACK_DEPTH,"backward_cap":BACK_CAP,
            "forward_depth":FWD_DEPTH,"length_cap":cap,
            "depth_reached":stats.get("depth_reached"),"expanded":stats.get("expanded"),
            "seen":stats.get("seen"),"seconds":round(time.time()-t0,1)}}
    if mv:
        v=s
        for m in mv: v=apply_move(v,m)
        ch={"challenge_id":case["ac_id"],"generators":["x","y"],
            "initial_relators":case["initial_relators"],"target_relators":[[1],[2]],
            "move_spec_version":"ac-r2-v1"}
        ver=core.verify(ch, mv, "ac-r2-v1", LIM)
        rec["parameters_and_counts"].update({"moves":mv,"move_count":len(mv),
            "independent_replay_reached_target":(v==TARGET),
            "official_verifier_ok":bool(ver.get("ok")),"official_verifier":ver})
        found.append((suf,len(mv),v==TARGET,bool(ver.get("ok"))))
        print(f"  *** SPLICE ac-{suf}: {len(mv)} moves | replay={v==TARGET} | verifier={ver.get('ok')}", flush=True)
    recs.append(rec)
    print(f"[{i:2}/51] ac-{suf} cap{cap} {rec['result']:22} {str(stats.get('stop_reason')):34} "
          f"depth{stats.get('depth_reached')} seen={stats.get('seen',0):>9,} {rec['parameters_and_counts']['seconds']}s", flush=True)

json.dump({"finalized_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "pass":"suffix-splice pass 1","dictionary_states":len(sd),
  "certificates_found":len(found),"records":recs,
  "correction_scope":"Bounded pass. Every NO_CERTIFICATE is budget- or cap-limited, not an impossibility claim."},
  open("runs/board-splice-pass1.json","w"), indent=1)
print(f"\ncertificates found: {len(found)}")
for f in found: print("  ",f)
