#!/usr/bin/env python3
# SCRIPT: acc_segment_optimizer_sac
"""acc_segment_optimizer_sac v1 — whole-path shortening for stable-AC certificates (257 official moves,
verifier.stable_core).  Same idea as acc_segment_optimizer_v1: cut revisited states, then slide a window of
W moves and replace it by a strictly shorter exact segment found by forward BFS (depth <= W-1, states
capped at the window's own peak total length +extra).  Forward-only because stabilize/destabilize have
no single inverse id.  Final path re-verified by the official sac-r8-v1 verify().  Never overwrites.
"""
import argparse, json, os, sys, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import acc_run_decoder_v2 as D
G = {}
def init(sair):
    core, sc, specs = D.load_verifier(sair); limits, manifest = D.load_manifest(sair)
    G.update(sc=sc, verify=specs.get("sac-r8-v1").verify, limits=limits, manifest=manifest)
def L(s): return sum(len(w) for w in s)
def states_of(sc, c, moves):
    s = tuple(tuple(w) for w in c["initial_relators"]); out = [s]
    for m in moves:
        s, r = sc.apply_move(s, m)
        if s is None: return None
        out.append(s)
    return out
def cut_loops(moves, states):
    changed = True
    while changed:
        changed = False; first = {}
        for k, s in enumerate(states):
            if s in first: i = first[s]; moves = moves[:i] + moves[k:]; states = states[:i] + states[k:]; changed = True; break
            first[s] = k
    return moves, states
def bfs(sc, start, goal, maxlen, cap, node_limit):
    if start == goal: return []
    seen = {start: None}; frontier = [start]; d = 0; n = 0
    while frontier and d < maxlen:
        nxt = []
        for s in frontier:
            for m in range(sc.NUM_MOVES):
                t, r = sc.apply_move(s, m); n += 1
                if t is None or L(t) > cap or t in seen: continue
                seen[t] = (s, m)
                if t == goal:
                    p = []; cur = t
                    while seen[cur] is not None: ps, pm = seen[cur]; p.append(pm); cur = ps
                    return p[::-1]
                nxt.append(t)
            if n > node_limit: return None
        frontier = nxt; d += 1
    return None
def optimize(args):
    cid, moves, W, extra, node_limit = args; sc = G["sc"]
    c = G["manifest"].get(cid)
    if c is None or c.get("move_spec_version") != "sac-r8-v1": return {"challenge_id": cid, "action": "passthrough"}, moves
    if not G["verify"](c, moves, "sac-r8-v1", G["limits"]).get("ok"): return {"challenge_id": cid, "action": "rejected_original"}, None
    n0 = len(moves); states = states_of(sc, c, moves); moves, states = cut_loops(list(moves), states); loops = n0 - len(moves)
    i = 0; splices = 0; t0 = time.time()
    while i + 2 <= len(moves):
        j = min(len(moves), i + W); cap = max(L(s) for s in states[i:j + 1]) + extra
        p = bfs(sc, states[i], states[j], j - i - 1, cap, node_limit)
        if p is not None and len(p) < j - i:
            moves = moves[:i] + p + moves[j:]; states = states_of(sc, c, moves); splices += 1; i = max(0, i - W)
        else: i += 1
    v1 = G["verify"](c, moves, "sac-r8-v1", G["limits"])
    rec = {"challenge_id": cid, "len": n0, "loops_cut": loops, "splices": splices, "new_len": len(moves), "saved": n0 - len(moves), "verify_ok": bool(v1.get("ok")), "seconds": round(time.time() - t0, 1)}
    if not v1.get("ok"): rec["action"] = "splice_rejected"; return rec, None
    rec["action"] = "shortened" if len(moves) < n0 else "kept"; return rec, moves
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--sair", default="/home/user/saircompetition/andrews-curtis")
    ap.add_argument("--submission", required=True); ap.add_argument("--window", type=int, default=5); ap.add_argument("--extra-cap", type=int, default=0)
    ap.add_argument("--node-limit", type=int, default=300_000); ap.add_argument("--workers", type=int, default=4); ap.add_argument("--out", required=True); a = ap.parse_args()
    if os.path.exists(a.out): print("refusing to overwrite", a.out); sys.exit(2)
    runs = D.parse_submission(a.submission); t0 = time.time()
    with Pool(a.workers, initializer=init, initargs=(a.sair,)) as pool:
        results = pool.map(optimize, [(cid, m, a.window, a.extra_cap, a.node_limit) for cid, m in runs], chunksize=1)
    rep = {"tool": "acc_segment_optimizer_sac v1", "window": a.window, "paths": len(runs), "shortened": 0, "kept": 0, "rejected": 0, "moves_saved": 0, "loops_cut": 0, "runs": []}; out = []
    for (cid, orig), (rec, final) in zip(runs, results):
        rep["runs"].append(rec)
        if rec["action"] == "shortened": rep["shortened"] += 1; rep["moves_saved"] += rec["saved"]; rep["loops_cut"] += rec["loops_cut"]
        elif rec["action"] == "kept": rep["kept"] += 1
        elif rec["action"] != "passthrough": rep["rejected"] += 1
        if final is not None: out.append(f"{cid}: {json.dumps(final, separators=(',', ':'))}")
    rep["seconds"] = round(time.time() - t0, 1)
    open(a.out, "w").write(f"# acc_segment_optimizer_sac v1 (window {a.window}); every line re-verified by the official sac-r8-v1 verifier\n" + "\n".join(out) + "\n")
    json.dump(rep, open(a.out + ".report.json", "w"), indent=1); print(json.dumps({k: v for k, v in rep.items() if k != "runs"}, indent=1))
if __name__ == "__main__": main()
