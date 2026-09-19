"""Build and self-check a Discovery Track submission from verified corridor runs.

Every line is checked twice before it is written: the pinned official verifier,
and an independent replay through this package's own engine reaching the exact
ordered target.  Nothing here prices, uploads or submits.
"""
import sys, json, datetime
sys.path.insert(0,'vendor'); sys.path.insert(0,'.')
from verifier import core, specs
from acc.moves import apply_move, TARGET

SAIR="/home/user/saircompetition/andrews-curtis"
LIM={"max_path_length":100000,"max_total_relator_length":10000,"max_work":5000000}
MAN={c["challenge_id"]:c for c in json.load(
    open(f"{SAIR}/competition/tools/verifier/data/manifest.json"))["challenges"]}

def ac_ok(cid, moves):
    return bool(core.verify(MAN[cid], moves, "ac-r2-v1", LIM).get("ok"))

def replay_ok(cid, moves):
    s=tuple(tuple(w) for w in MAN[cid]["initial_relators"])
    for m in moves: s=apply_move(s,m)
    return s==TARGET

def stable_ok(cid, moves):
    """A Stable line is the ordinary path plus [16,15]: destabilize y, then x.

    Stable challenges verify through their OWN spec (sac-r8-v1, 257 moves,
    max_rank 8), not through the ordinary verifier.  Each spec object carries
    its own `verify`; dispatch on the challenge's move_spec_version.
    """
    sid="s"+cid
    if sid not in MAN: return False, None
    full=list(moves)+[16,15]
    ch=MAN[sid]
    spec=specs.SPECS[ch["move_spec_version"]]
    v=spec.verify(ch, full, ch["move_spec_version"], LIM)
    return bool(v.get("ok")), full

def main(src, out):
    d=json.load(open(src))
    rows=[]
    for f in d["found"]:
        cid=f["challenge_id"]; mv=f["moves"]
        a=ac_ok(cid,mv); r=replay_ok(cid,mv)
        s_ok, full = stable_ok(cid,mv)
        rows.append({"challenge_id":cid,"moves":mv,"move_count":len(mv),
                     "official_verifier_ok":a,"independent_replay_ok":r,
                     "stable_id":"s"+cid,"stable_moves":full,"stable_ok":s_ok})
    good=[x for x in rows if x["official_verifier_ok"] and x["independent_replay_ok"]]
    with open(out,"w") as fh:
        fh.write("# Andrews-Curtis Discovery Track solutions.\n")
        fh.write("# Found with a bidirectional corridor BFS over ac-r2-v1 (meet-in-the-middle,\n")
        fh.write("# expanding the smaller frontier), recovered from prior Operator-First work.\n")
        fh.write("# Every line self-checked against the pinned reference verifier and an\n")
        fh.write("# independent replay to the exact ordered target before writing.\n")
        for x in good:
            fh.write(f"{x['challenge_id']}: {json.dumps(x['moves'])} # AC: reach (x, y).\n")
            if x["stable_ok"]:
                fh.write(f"{x['stable_id']}: {json.dumps(x['stable_moves'])} # Stable AC: same path + [16,15].\n")
    json.dump({"finalized_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
               "source":src,"ac_lines":len(good),
               "stable_lines":sum(1 for x in good if x["stable_ok"]),
               "rows":rows,
               "scope":"LOCAL_VERIFIED_UNPRICED_NOT_SUBMITTED; reference verifier is self-check only, the server is the sole authority"},
              open(out.replace(".txt","_report.json"),"w"), indent=1)
    print(f"AC lines {len(good)} | Stable lines {sum(1 for x in good if x['stable_ok'])} -> {out}")
    bad=[x for x in rows if not (x["official_verifier_ok"] and x["independent_replay_ok"])]
    print("rejected before writing:", len(bad))

if __name__=="__main__":
    main(sys.argv[1], sys.argv[2])
