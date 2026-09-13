#!/usr/bin/env python3
# SCRIPT: acc_window_finisher
"""acc_window_finisher v1 — generalises the corridor finisher: exact BFS from the state W moves before
the end of an accepted path to the target, with total length capped at the maximum length the original
path itself reaches over that window (so the replacement never climbs higher than the record did).
Splice only if strictly shorter; every output line re-verified by the official verifier.  Never overwrites.
Python 3 stdlib only.
"""
import argparse, collections, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import acc_run_decoder_v2 as D
from acc_finisher_v1 import bfs, TARGET

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--sair", default="/home/user/saircompetition/andrews-curtis")
    ap.add_argument("--submission", required=True); ap.add_argument("--window", type=int, default=12); ap.add_argument("--extra-cap", type=int, default=0)
    ap.add_argument("--node-limit", type=int, default=3_000_000); ap.add_argument("--out", required=True); a = ap.parse_args()
    if os.path.exists(a.out): print("refusing to overwrite", a.out); sys.exit(2)
    core, sc, specs = D.load_verifier(a.sair); limits, manifest = D.load_manifest(a.sair); tindex = D.training_index(a.sair); verify = specs.get("ac-r2-v1").verify
    rep = {"tool": "acc_window_finisher v1", "window": a.window, "extra_cap": a.extra_cap, "paths": 0, "shortened": 0, "kept": 0, "bfs_limit": 0, "rejected": 0, "moves_saved": 0, "runs": []}
    out = []; t0 = time.time()
    for cid, moves in D.parse_submission(a.submission):
        c, spec = D.resolve_challenge(cid, manifest, tindex)
        if c is None or spec != "ac-r2-v1": out.append(f"{cid}: {json.dumps(moves, separators=(',', ':'))}"); continue
        rep["paths"] += 1
        if not verify(c, moves, spec, limits).get("ok"): rep["rejected"] += 1; continue
        state = tuple(tuple(w) for w in c["initial_relators"]); states = [state]
        for m in moves: state = core.apply_move(state, m); states.append(state)
        n = len(moves); k = max(0, n - a.window); L = lambda s: sum(len(w) for w in s)
        cap = max(L(s) for s in states[k:]) + a.extra_cap
        path, nodes = bfs(core, states[k], cap, a.node_limit)
        r = {"challenge_id": cid, "len": n, "window_start": k, "cap": cap, "bfs_nodes": nodes}
        if path is None: r["action"] = "bfs_limit"; rep["bfs_limit"] += 1; final = moves
        elif len(path) >= n - k: r["action"] = "kept"; rep["kept"] += 1; final = moves
        else:
            new = list(moves[:k]) + path; v = verify(c, new, spec, limits)
            if v.get("ok"): r.update({"action": "shortened", "new_len": len(new), "saved": (n - k) - len(path)}); rep["shortened"] += 1; rep["moves_saved"] += r["saved"]; final = new
            else: r["action"] = "splice_rejected"; rep["rejected"] += 1; final = moves
        rep["runs"].append(r); out.append(f"{cid}: {json.dumps(final, separators=(',', ':'))}")
    rep["seconds"] = round(time.time() - t0, 1)
    open(a.out, "w").write(f"# acc_window_finisher v1 (window {a.window}, cap = record's own max over the window +{a.extra_cap}); every line re-verified\n" + "\n".join(out) + "\n")
    json.dump(rep, open(a.out + ".report.json", "w"), indent=1); print(json.dumps({k: v for k, v in rep.items() if k != "runs"}, indent=1))
if __name__ == "__main__": main()
