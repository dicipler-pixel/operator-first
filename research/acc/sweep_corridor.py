"""Bidirectional corridor sweep. Escalating caps, engine verdicts recorded verbatim."""
import sys, json, time, datetime
sys.path.insert(0,'engines'); sys.path.insert(0,'vendor'); sys.path.insert(0,'.')
from run_corridor import run, manifest
from verifier import core
LIM={"max_path_length":100000,"max_total_relator_length":10000,"max_work":5000000}

ids=json.loads(sys.argv[1]) if sys.argv[1].startswith("[") else json.load(open(sys.argv[1]))
CAPS=[int(c) for c in sys.argv[2].split(",")]
BUDGET=int(sys.argv[3]); OUT=sys.argv[4]

recs=[]; found=[]
for i,cid in enumerate(ids,1):
    ch=manifest()[cid]; start=sum(len(w) for w in ch["initial_relators"])
    best=None
    for cap in CAPS:
        if cap<start: continue
        t=time.time()
        try: r=run(cid,cap,BUDGET,timeout=600)
        except Exception as e: r={"verdict":"TIMEOUT","head":str(e)[:120],"moves":None,"cap":cap}
        r["seconds"]=round(time.time()-t,1); best=r
        if r["verdict"]=="MEET":
            ok=core.verify(ch,r["moves"],"ac-r2-v1",LIM)
            r["official_verifier_ok"]=bool(ok.get("ok"))
            found.append({"challenge_id":cid,"cap":cap,"move_count":len(r["moves"]),
                          "moves":r["moves"],"official_verifier_ok":r["official_verifier_ok"]})
            print(f"  *** {cid} cap{cap}: MEET {len(r['moves'])} moves  verifier_ok={r['official_verifier_ok']}",flush=True)
            break
        if r["verdict"] in ("CLOSED_F","CLOSED_B"): break
    recs.append({"run":f"corridor-{cid}","phase":"bidirectional corridor sweep",
        "result":"CERTIFICATE_CANDIDATE" if best and best["verdict"]=="MEET" else "NO_CERTIFICATE",
        "stop_reason":best["verdict"] if best else "NO_CAP_TRIED",
        "completeness_or_impossibility_claim":False,"raw_result_file":OUT,
        "parameters_and_counts":{"challenge_id":cid,"algorithm":"ac_corridor64_bidir_v2",
            "start_total_length":start,"cap":best.get("cap") if best else None,
            "budget_per_side":BUDGET,"engine_line":best.get("head") if best else None,
            "moves":best.get("moves") if best else None,
            "official_verifier_ok":best.get("official_verifier_ok") if best else None,
            "seconds":best.get("seconds") if best else None}})
    print(f"[{i:3}/{len(ids)}] {cid} start{start} -> {best['verdict'] if best else '-':10} {best.get('head','') if best else ''}",flush=True)

json.dump({"finalized_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
  "engine":"ac_corridor64_bidir_v2 (compiled)","caps":CAPS,"budget_per_side":BUDGET,
  "certificates_found":len(found),"found":found,"records":recs,
  "correction_scope":"BUDGET carries only the df+db lower bound. CLOSED_F/CLOSED_B is disconnection at that cap, not impossibility."},
  open(OUT,"w"), indent=1)
print(f"\ncertificates: {len(found)}")
