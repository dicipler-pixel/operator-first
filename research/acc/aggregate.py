"""Merge every corridor run into one double-checked submission file."""
import sys, json, glob, datetime
sys.path.insert(0,'vendor'); sys.path.insert(0,'.')
from verifier import core, specs
from acc.moves import apply_move, TARGET
SAIR="/home/user/saircompetition/andrews-curtis"
LIM={"max_path_length":100000,"max_total_relator_length":10000,"max_work":5000000}
MAN={c["challenge_id"]:c for c in json.load(
    open(f"{SAIR}/competition/tools/verifier/data/manifest.json"))["challenges"]}

best={}
for path in sorted(glob.glob("runs/pool-*.json"))+sorted(glob.glob("runs/board-corridor-*.json")):
    try: d=json.load(open(path))
    except Exception: continue
    for f in d.get("found",[]):
        cid=f["challenge_id"]; mv=f["moves"]
        if cid not in best or len(mv)<len(best[cid]): best[cid]=mv

rows=[]
for cid,mv in sorted(best.items()):
    ch=MAN[cid]
    ac=bool(core.verify(ch,mv,"ac-r2-v1",LIM).get("ok"))
    s=tuple(tuple(w) for w in ch["initial_relators"])
    for m in mv: s=apply_move(s,m)
    rep=(s==TARGET)
    sid="s"+cid; st=False; full=None
    if sid in MAN:
        full=list(mv)+[16,15]; sc=MAN[sid]
        st=bool(specs.SPECS[sc["move_spec_version"]].verify(sc,full,sc["move_spec_version"],LIM).get("ok"))
    rows.append({"challenge_id":cid,"moves":mv,"move_count":len(mv),
                 "official_verifier_ok":ac,"independent_replay_ok":rep,
                 "stable_id":sid,"stable_moves":full,"stable_ok":st})

good=[r for r in rows if r["official_verifier_ok"] and r["independent_replay_ok"]]
with open("runs/submission.txt","w") as fh:
    fh.write("# Andrews-Curtis Discovery Track solutions.\n")
    fh.write("# Method: bidirectional corridor BFS over ac-r2-v1, expanding the smaller\n")
    fh.write("# frontier and meeting in the middle, at caps relative to each start length.\n")
    fh.write("# Stable lines are the same ordinary path plus [16,15] (destabilize y, then x).\n")
    fh.write("# Every line self-checked against the pinned reference verifier and an\n")
    fh.write("# independent replay to the exact ordered target before writing.\n")
    for r in good:
        fh.write(f"{r['challenge_id']}: {json.dumps(r['moves'])} # AC: reach (x, y).\n")
        if r["stable_ok"]:
            fh.write(f"{r['stable_id']}: {json.dumps(r['stable_moves'])} # Stable AC: + [16,15].\n")
json.dump({"finalized_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
   "ac_lines":len(good),"stable_lines":sum(1 for r in good if r["stable_ok"]),
   "total_lines":len(good)+sum(1 for r in good if r["stable_ok"]),
   "rejected_before_writing":len(rows)-len(good),"rows":rows,
   "scope":"LOCAL_VERIFIED_UNPRICED_NOT_SUBMITTED; reference verifier is self-check only, the server is the sole authority"},
   open("runs/submission_report.json","w"), indent=1)
print(f"AC {len(good)} | Stable {sum(1 for r in good if r['stable_ok'])} "
      f"| total {len(good)+sum(1 for r in good if r['stable_ok'])} lines -> runs/submission.txt")
print("rejected before writing:", len(rows)-len(good))
