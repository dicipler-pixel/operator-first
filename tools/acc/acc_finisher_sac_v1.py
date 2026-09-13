#!/usr/bin/env python3
# SCRIPT: acc_finisher_sac
"""acc_finisher_sac v1 — stable-AC counterpart of acc_finisher: exact capped BFS to the empty
presentation () from the earliest state where some relator is a single letter, over the 257 official
stable moves (verifier.stable_core.apply_move), splice only if strictly shorter, re-verify every output
line with the official sac-r8-v1 verify().  Never overwrites.  Python 3 stdlib only.
"""
import argparse, collections, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import acc_run_decoder_v2 as D
TARGET = ()

def total(s): return sum(len(w) for w in s)

def bfs(sc, start, cap, node_limit):
    seen = {start: None}; q = collections.deque([start]); n = 0
    while q:
        s = q.popleft(); n += 1
        if n > node_limit: return None, n
        for m in range(sc.NUM_MOVES):
            t, reason = sc.apply_move(s, m)
            if t is None or total(t) > cap or t in seen: continue
            seen[t] = (s, m)
            if t == TARGET:
                path, cur = [], t
                while seen[cur] is not None:
                    p, mm = seen[cur]; path.append(mm); cur = p
                return path[::-1], n
            q.append(t)
    return None, n

def finish(sc, verify, c, moves, limits, cap, node_limit):
    state = tuple(tuple(w) for w in c["initial_relators"]); states = [state]
    for m in moves:
        state, reason = sc.apply_move(state, m)
        if state is None: return {"challenge_id": c["challenge_id"], "action": "rejected_original", "reason": reason}, None
        states.append(state)
    v0 = verify(c, moves, "sac-r8-v1", limits)
    rec = {"challenge_id": c["challenge_id"], "original_len": len(moves), "original_ok": bool(v0.get("ok"))}
    if not v0.get("ok"): rec.update({"action": "rejected_original"}); return rec, None
    entry = next((k for k, s in enumerate(states) if any(len(w) == 1 for w in s) and s != TARGET), None)
    if entry is None: rec.update({"action": "no_corridor", "final_len": len(moves)}); return rec, moves
    L = total(states[entry]); tail = len(moves) - entry
    path, n = bfs(sc, states[entry], L + cap, node_limit)
    rec.update({"entry": entry, "L_entry": L, "rank_entry": len(states[entry]), "original_tail": tail, "bfs_nodes": n})
    if path is None: rec.update({"action": "bfs_limit", "final_len": len(moves)}); return rec, moves
    if len(path) >= tail: rec.update({"action": "kept", "exact_tail": len(path), "final_len": len(moves)}); return rec, moves
    new = list(moves[:entry]) + path; v1 = verify(c, new, "sac-r8-v1", limits)
    if not v1.get("ok"): rec.update({"action": "splice_rejected_by_verifier", "verify": v1, "final_len": len(moves)}); return rec, moves
    rec.update({"action": "shortened", "exact_tail": len(path), "final_len": len(new), "saved": tail - len(path)}); return rec, new

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--sair", default="/home/user/saircompetition/andrews-curtis")
    g = ap.add_mutually_exclusive_group(required=True); g.add_argument("--submission"); g.add_argument("--candidates"); g.add_argument("--stable-training", action="store_true")
    ap.add_argument("--cap", type=int, default=2); ap.add_argument("--node-limit", type=int, default=200_000); ap.add_argument("--out", required=True); a = ap.parse_args()
    if os.path.exists(a.out): print("refusing to overwrite", a.out); sys.exit(2)
    core, sc, specs = D.load_verifier(a.sair); limits, manifest = D.load_manifest(a.sair); tindex = D.training_index(a.sair); verify = specs.get("sac-r8-v1").verify
    stable_index = {c["challenge_id"]: c for c, m in D.load_training(a.sair, "sac-r8-v1")}
    if a.stable_training: runs = [(c["challenge_id"], m) for c, m in D.load_training(a.sair, "sac-r8-v1")]
    elif a.submission: runs = D.parse_submission(a.submission)
    else: runs = D.parse_candidates(a.candidates)
    rep = {"finisher": "acc_finisher_sac v1", "cap": a.cap, "input_paths": len(runs), "shortened": 0, "kept": 0, "bfs_limit": 0, "rejected_original": 0, "no_corridor": 0, "ac_passthrough": 0, "unknown_id": 0, "moves_saved": 0, "runs": []}
    t0 = time.time(); out = []
    for cid, moves in runs:
        if a.stable_training: c, spec = stable_index[cid], "sac-r8-v1"   # training ids are shared with AC; force the stable spec
        else: c, spec = D.resolve_challenge(cid, manifest, tindex)
        if c is None: rep["unknown_id"] += 1; rep["runs"].append({"challenge_id": cid, "action": "unknown_id"}); continue
        if spec != "sac-r8-v1": rep["ac_passthrough"] += 1; out.append(f"{cid}: {json.dumps(moves, separators=(',', ':'))}"); rep["runs"].append({"challenge_id": cid, "action": "ac_passthrough"}); continue
        r, final = finish(sc, verify, c, moves, limits, a.cap, a.node_limit); rep["runs"].append(r)
        k = r["action"]; rep[k if k in rep else "kept"] += 1
        if k == "shortened": rep["moves_saved"] += r["saved"]
        if final is not None: out.append(f"{cid}: {json.dumps(final, separators=(',', ':'))}")
    rep["seconds"] = round(time.time() - t0, 1)
    with open(a.out, "w") as f: f.write("# acc_finisher_sac v1 output — every line re-verified by the official sac-r8-v1 verifier\n" + "\n".join(out) + "\n")
    with open(a.out + ".report.json", "w") as f: json.dump(rep, f, indent=1)
    print(json.dumps({k: v for k, v in rep.items() if k != "runs"}, indent=1))

if __name__ == "__main__": main()
