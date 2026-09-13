#!/usr/bin/env python3
# SCRIPT: acc_finisher
"""acc_finisher v1 — mandatory final stage for ACC certificates before submission.

For every path in a submission file (`id: [moves]` lines) or a candidates file (JSONL with
challenge_id + moves): replay it with the official verifier, find the earliest state where exactly
one relator is a single letter (the corridor), run an exact BFS from that state to the target with
total length capped at L_entry + cap (verifier.core.apply_move only), and, if the exact finish is
shorter than the original tail, splice it in.  Every output path — shortened or not — is passed
through the official verify() and only accepted paths are written.  Original file is never modified.

Standard AC (ac-r2-v1) only; stable paths are copied through untouched and reported.
Python 3 stdlib only.  New files only.
"""
import argparse, collections, json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import acc_run_decoder_v2 as D

TARGET = ((1,), (2,))

def bfs(core, start, cap, node_limit):
    seen = {start: None}; q = collections.deque([start]); n = 0
    while q:
        s = q.popleft(); n += 1
        if n > node_limit: return None, n
        for m in range(core.NUM_MOVES):
            t = core.apply_move(s, m)
            if sum(len(w) for w in t) > cap or t in seen: continue
            seen[t] = (s, m)
            if t == TARGET:
                path, cur = [], t
                while seen[cur] is not None:
                    p, mm = seen[cur]; path.append(mm); cur = p
                return path[::-1], n
            q.append(t)
    return None, n

def finish(core, verify, c, moves, limits, cap, node_limit):
    state = tuple(tuple(w) for w in c["initial_relators"]); states = [state]
    for m in moves:
        state = core.apply_move(state, m); states.append(state)
    v0 = verify(c, moves, "ac-r2-v1", limits)
    rec = {"challenge_id": c["challenge_id"], "original_len": len(moves), "original_ok": bool(v0.get("ok"))}
    if not v0.get("ok"):
        rec.update({"action": "rejected_original", "verify": v0}); return rec, None
    entry = next((k for k, s in enumerate(states) if (len(s[0]) == 1) != (len(s[1]) == 1)), None)
    if entry is None:
        rec.update({"action": "no_corridor", "final_len": len(moves)}); return rec, moves
    L = sum(len(w) for w in states[entry]); tail = len(moves) - entry
    path, n = bfs(core, states[entry], L + cap, node_limit)
    rec.update({"entry": entry, "L_entry": L, "original_tail": tail, "bfs_nodes": n})
    if path is None or len(path) >= tail:
        rec.update({"action": "kept", "exact_tail": None if path is None else len(path), "final_len": len(moves)}); return rec, moves
    new = list(moves[:entry]) + path
    v1 = verify(c, new, "ac-r2-v1", limits)
    if not v1.get("ok"):
        rec.update({"action": "splice_rejected_by_verifier", "verify": v1, "final_len": len(moves)}); return rec, moves
    rec.update({"action": "shortened", "exact_tail": len(path), "final_len": len(new), "saved": tail - len(path),
                "verify_length": v1.get("length"), "verify_peak": v1.get("peak_total_relator_length")})
    return rec, new

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sair", default="/home/user/saircompetition/andrews-curtis")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--submission"); g.add_argument("--candidates"); g.add_argument("--training", action="store_true")
    ap.add_argument("--cap", type=int, default=2); ap.add_argument("--node-limit", type=int, default=2_000_000)
    ap.add_argument("--out", required=True, help="output submission file (must not exist)")
    a = ap.parse_args()
    if os.path.exists(a.out):
        print("refusing to overwrite", a.out); sys.exit(2)
    core, stable_core, specs = D.load_verifier(a.sair); limits, manifest = D.load_manifest(a.sair); tindex = D.training_index(a.sair)
    verify = specs.get("ac-r2-v1").verify
    if a.training: runs = [(c["challenge_id"], m) for c, m in D.load_training(a.sair, "ac-r2-v1")]
    elif a.submission: runs = D.parse_submission(a.submission)
    else: runs = D.parse_candidates(a.candidates)
    report = {"finisher": "acc_finisher v1", "cap_over_entry_length": a.cap, "input_paths": len(runs), "shortened": 0, "kept": 0,
              "rejected_original": 0, "no_corridor": 0, "stable_passthrough": 0, "unknown_id": 0, "moves_saved": 0, "runs": []}
    t0 = time.time(); out_lines = []
    for cid, moves in runs:
        c, spec = D.resolve_challenge(cid, manifest, tindex)
        if c is None:
            report["unknown_id"] += 1; report["runs"].append({"challenge_id": cid, "action": "unknown_id"}); continue
        if spec != "ac-r2-v1":
            report["stable_passthrough"] += 1; out_lines.append(f"{cid}: {json.dumps(moves, separators=(',', ':'))}")
            report["runs"].append({"challenge_id": cid, "action": "stable_passthrough"}); continue
        rec, final = finish(core, verify, c, moves, limits, a.cap, a.node_limit)
        report["runs"].append(rec)
        if rec["action"] == "shortened": report["shortened"] += 1; report["moves_saved"] += rec["saved"]
        elif rec["action"] == "rejected_original": report["rejected_original"] += 1
        elif rec["action"] == "no_corridor": report["no_corridor"] += 1
        else: report["kept"] += 1
        if final is not None:
            out_lines.append(f"{cid}: {json.dumps(final, separators=(',', ':'))}")
    report["seconds"] = round(time.time() - t0, 2)
    with open(a.out, "w") as f:
        f.write("# acc_finisher v1 output — every line re-verified by the official verifier; exact corridor finish, cap L_entry+%d\n" % a.cap)
        f.write("\n".join(out_lines) + "\n")
    with open(a.out + ".report.json", "w") as f:
        json.dump(report, f, indent=1)
    print(json.dumps({k: v for k, v in report.items() if k != "runs"}, indent=1))

if __name__ == "__main__":
    main()
