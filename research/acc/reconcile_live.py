"""Reconcile live SAIR state, our server submission history, and local certificates.

Inputs
  snapshot        GET /discoveries/snapshot?problem=ac  (items: challengeId, status,
                  currentBestLength, kTeams; field-name fallbacks tolerated)
  mine            `sair_api.py mine --all` output (items: submissionId, results[] with
                  challenge_id / ok / length)
  certs           one or more TXT files of `ac-xxxxx: [moves] # comment` lines

Every local path is replayed through the OFFICIAL kernel when `verifier.core` is
importable (PYTHONPATH=<sair>/competition/tools); otherwise it is classified
INVALID_OR_UNVERIFIED rather than trusted.

Outputs (written to --out-dir, PRIVATE — never commit them):
  PRIVATE_SUBMIT_NOW.txt                 unsolved-with-path + strict live wins
  PRIVATE_TIES_NOT_ON_SERVER.txt         local == live, not yet on our server record
  PRIVATE_LOCAL_BETTER_THAN_SERVER.txt   beats our own server path but not the live record
  PRIVATE_OBSOLETE.txt                   loses to live and to server
  PRIVATE_RECONCILIATION.json            per-challenge table
Stdout carries sanitized counts only.
"""

import hashlib
import json
import os
import re
import sys
from collections import defaultdict

CLASSES = ("UNSOLVED_LOCAL_SOLUTION", "STRICT_LIVE_WIN", "TIE_NOT_ON_SERVER", "TIE_ALREADY_ON_SERVER",
           "LOCAL_BETTER_THAN_SERVER", "SERVER_BETTER_THAN_LOCAL", "OBSOLETE_LOCAL", "NO_LOCAL_CERT",
           "INVALID_OR_UNVERIFIED")
LINE = re.compile(r"^\s*(s?ac-\d{5})\s*:\s*(\[[^\]]*\])")


def _first(d, *keys, default=None):
    for k in keys:
        if isinstance(d, dict) and d.get(k) is not None:
            return d[k]
    return default


def _items(doc):
    if isinstance(doc, list):
        return doc
    d = doc.get("data", doc)
    if isinstance(d, list):
        return d
    for k in ("items", "submissions", "results"):
        if isinstance(d.get(k), list):
            return d[k]
    return []


def load_snapshot(path):
    live = {}
    for it in _items(json.load(open(path))):
        cid = _first(it, "challengeId", "challenge_id")
        if not cid:
            continue
        best = _first(it, "currentBestLength", "shortestMoveCount", "bestLength", "best")
        status = str(_first(it, "status", default="")).lower()
        unsolved = best in (None, 0) or "unsolved" in status or status in ("open", "none")
        live[cid] = {"status": "unsolved" if unsolved else (status or "solved"),
                     "best": None if unsolved else int(best),
                     "k": _first(it, "kTeams", "teamsAtBest", "k", default=None)}
    return live


def load_mine(path):
    """server_best[cid] -> (length, [submissionIds]) over ok results only."""
    doc = json.load(open(path))
    subs = _items(doc)
    best, ids_by_len = {}, defaultdict(lambda: defaultdict(list))
    for s in subs:
        sid = _first(s, "submissionId", "id")
        for r in s.get("results") or []:
            if not r.get("ok"):
                continue
            cid = _first(r, "challenge_id", "challengeId")
            L = _first(r, "length", "moveCount", "moves")
            if cid is None or L is None:
                continue
            L = int(L)
            ids_by_len[cid][L].append(sid)
            if cid not in best or L < best[cid]:
                best[cid] = L
    complete = not doc.get("errors") and (doc.get("pages") is None or True)
    return best, ids_by_len, len(subs), complete


def parse_certs(paths):
    """cid -> list of (moves, source, sha256) — every candidate, all files."""
    out = defaultdict(list)
    for p in paths:
        for line in open(p, encoding="utf-8"):
            m = LINE.match(line)
            if not m or m.group(1).startswith("sac"):
                continue
            try:
                moves = json.loads(m.group(2))
            except json.JSONDecodeError:
                continue
            if not all(isinstance(x, int) and not isinstance(x, bool) for x in moves):
                continue
            sha = hashlib.sha256(json.dumps(moves, separators=(",", ":")).encode()).hexdigest()
            out[m.group(1)].append((moves, os.path.basename(p), sha))
    return out


def _verifier():
    try:
        from verifier import core  # noqa: F401
        return core
    except Exception:
        return None


def verify_local(cands, manifest_challenges, core, limits):
    """Return cid -> best verified (length, moves, source, sha) or None."""
    best = {}
    for cid, lst in cands.items():
        ch = manifest_challenges.get(cid)
        for moves, src, sha in sorted(lst, key=lambda t: len(t[0])):
            if core is None or ch is None:
                break
            v = core.verify(ch, moves, ch["move_spec_version"], limits)
            if v.get("ok"):
                best[cid] = (v["length"], moves, src, sha)
                break
        else:
            continue
    return best


def classify(live, server, local):
    if local is None:
        return "NO_LOCAL_CERT"
    if live is None or live["status"] == "unsolved":
        return "UNSOLVED_LOCAL_SOLUTION"
    lb = live["best"]
    if local < lb:
        return "STRICT_LIVE_WIN"
    if local == lb:
        return "TIE_ALREADY_ON_SERVER" if (server is not None and server <= local) else "TIE_NOT_ON_SERVER"
    if server is not None and server < local:
        return "SERVER_BETTER_THAN_LOCAL"
    if server is not None and local < server:
        return "LOCAL_BETTER_THAN_SERVER"
    return "OBSOLETE_LOCAL"


def run(snapshot_path, mine_path, cert_paths, out_dir, manifest_path=None, trust_unverified=False):
    live = load_snapshot(snapshot_path)
    server_best, ids_by_len, n_subs, complete = load_mine(mine_path)
    cands = parse_certs(cert_paths)

    core = _verifier()
    challenges, limits = {}, None
    if core is not None:
        mp = manifest_path or os.environ.get("SAIR_MANIFEST")
        if mp and os.path.exists(mp):
            man = json.load(open(mp))
            challenges = {c["challenge_id"]: c for c in man["challenges"]}
            limits = man["limits"]
        else:
            core = None
    verified = verify_local(cands, challenges, core, limits) if core else {}

    table, counts = {}, {c: 0 for c in CLASSES}
    for cid in sorted(set(cands) | set(server_best)):
        v = verified.get(cid)
        if cid in cands and v is None and not trust_unverified:
            cls = "INVALID_OR_UNVERIFIED"; local = None; src = sha = None; moves = None
        else:
            if v is None and trust_unverified and cid in cands:
                moves, src, sha = min(cands[cid], key=lambda t: len(t[0])); local = len(moves)
            elif v is not None:
                local, moves, src, sha = v
            else:
                local = moves = src = sha = None
            cls = classify(live.get(cid), server_best.get(cid), local)
        counts[cls] += 1
        lv = live.get(cid) or {"status": "not_in_snapshot", "best": None, "k": None}
        table[cid] = {"live_status": lv["status"], "live_best": lv["best"], "live_k": lv["k"],
                      "server_best_ours": server_best.get(cid), "local_best": local,
                      "local_source_file": src, "local_sequence_sha256": sha,
                      "submission_ids_containing_ours": ids_by_len[cid].get(local, []) if local is not None else [],
                      "classification": cls, "_moves": moves}

    os.makedirs(out_dir, exist_ok=True)
    def dump(name, classes):
        with open(os.path.join(out_dir, name), "w", encoding="utf-8") as f:
            f.write(f"# {name} — PRIVATE. classes={list(classes)}\n")
            for cid, row in table.items():
                if row["classification"] in classes and row["_moves"] is not None:
                    f.write(f"{cid}: {json.dumps(row['_moves'])} # {row['classification']} local={row['local_best']} live={row['live_best']} k={row['live_k']} server={row['server_best_ours']}\n")
    dump("PRIVATE_SUBMIT_NOW.txt", ("UNSOLVED_LOCAL_SOLUTION", "STRICT_LIVE_WIN"))
    dump("PRIVATE_TIES_NOT_ON_SERVER.txt", ("TIE_NOT_ON_SERVER",))
    dump("PRIVATE_LOCAL_BETTER_THAN_SERVER.txt", ("LOCAL_BETTER_THAN_SERVER",))
    dump("PRIVATE_OBSOLETE.txt", ("OBSOLETE_LOCAL", "SERVER_BETTER_THAN_LOCAL"))
    with open(os.path.join(out_dir, "PRIVATE_RECONCILIATION.json"), "w") as f:
        json.dump({"server_submissions": n_subs, "server_history_complete": complete,
                   "live_challenges": len(live), "verifier": "official" if core else "none",
                   "counts": counts, "table": {k: {kk: vv for kk, vv in v.items() if kk != "_moves"} for k, v in table.items()}},
                  f, indent=1, sort_keys=True)
    print(json.dumps({"server_submissions": n_subs, "server_history_complete": complete, "live_challenges": len(live),
                      "local_candidates": len(cands), "verifier": "official" if core else "none", "counts": counts}, indent=1))
    return 0


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("snapshot"); ap.add_argument("mine"); ap.add_argument("certs", nargs="+")
    ap.add_argument("--out-dir", default="private_out"); ap.add_argument("--manifest")
    ap.add_argument("--trust-unverified", action="store_true", help="classify unverified local paths anyway (NOT for submission)")
    a = ap.parse_args()
    sys.exit(run(a.snapshot, a.mine, a.certs, a.out_dir, a.manifest, a.trust_unverified))
