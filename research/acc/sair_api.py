"""Thin client for the SAIR ACC public API (api.sair.foundation/api/public/v1).

Reads SAIR_API_KEY from the environment only; never accepts it as an argument,
never logs it. Every call is a plain HTTPS request through the standard
library so it works wherever egress to api.sair.foundation is permitted.

    python3 sair_api.py me
    python3 sair_api.py spec
    python3 sair_api.py snapshot --problem ac --out snapshot_ac.json
    python3 sair_api.py leaderboard --problem ac
    python3 sair_api.py submit submission.txt --note "batch 1"
    python3 sair_api.py status <submissionId>
    python3 sair_api.py mine

`snapshot` is the targeting feed: every scored challenge with status, current
shortest length and teams tied (k). `targets` post-processes a saved snapshot
into an ordered attack list without touching the network.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE = "https://api.sair.foundation/api/public/v1/competitions/acc"


def _req(path, method="GET", body=None):
    key = os.environ.get("SAIR_API_KEY")
    if not key:
        sys.exit("SAIR_API_KEY is not set in the environment")
    req = urllib.request.Request(BASE + path, method=method)
    req.add_header("Authorization", "Bearer " + key)
    data = None
    if body is not None:
        req.add_header("Content-Type", "application/json")
        data = json.dumps(body).encode("utf-8")
    try:
        with urllib.request.urlopen(req, data=data, timeout=60) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8")), resp.headers
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read().decode("utf-8"))
        except Exception:
            payload = {"error": str(e)}
        return e.code, payload, e.headers


def cmd_submit(path, note):
    text = open(path, encoding="utf-8").read()
    body = {"payload": {"text": text}}
    if note:
        body["meta"] = {"description": note}
    status, data, _ = _req("/submissions", "POST", body)
    print(json.dumps(data, indent=2))
    if status == 202:
        print("submissionId:", data.get("data", {}).get("submissionId"), file=sys.stderr)
    return 0 if status == 202 else 1


def cmd_status(sid, wait):
    while True:
        status, data, headers = _req(f"/submissions/{sid}")
        st = data.get("data", {}).get("status")
        if not wait or st in ("complete", "failed") or status != 200:
            print(json.dumps(data, indent=2))
            return 0 if st == "complete" else 1
        delay = int(headers.get("Retry-After", "10") or 10)
        print(f"status={st}; retry in {delay}s", file=sys.stderr)
        time.sleep(delay)


def cmd_targets(snapshot_path, my_team, limit):
    snap = json.load(open(snapshot_path))
    items = snap.get("data", {}).get("items", snap if isinstance(snap, list) else [])
    unsolved, soft = [], []
    for it in items:
        cid = it.get("challengeId")
        best = it.get("shortestMoveCount") or it.get("bestMoves") or it.get("shortest")
        k = it.get("teamsAtBest") or it.get("tiedTeams") or it.get("k")
        if not best:
            unsolved.append(cid)
        else:
            soft.append((int(best), int(k or 1), cid))
    soft.sort(reverse=True)  # longest current records first
    print(f"# unsolved (any verified path = 1.0 point): {len(unsolved)}")
    for cid in unsolved[:limit]:
        print(cid)
    print(f"\n# longest current records (beat by one move = full point when k=1): {len(soft)}")
    for best, k, cid in soft[:limit]:
        print(f"{cid}\tbest={best}\tk={k}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("me"); sub.add_parser("spec"); sub.add_parser("mine")
    p = sub.add_parser("snapshot"); p.add_argument("--problem", default="ac"); p.add_argument("--out"); p.add_argument("--relators", action="store_true")
    p = sub.add_parser("leaderboard"); p.add_argument("--problem", default="ac")
    p = sub.add_parser("submit"); p.add_argument("file"); p.add_argument("--note")
    p = sub.add_parser("status"); p.add_argument("id"); p.add_argument("--wait", action="store_true")
    p = sub.add_parser("targets"); p.add_argument("snapshot"); p.add_argument("--team"); p.add_argument("--limit", type=int, default=50)
    a = ap.parse_args()

    if a.cmd == "me":          _, d, _ = _req("/me"); print(json.dumps(d, indent=2))
    elif a.cmd == "spec":      _, d, _ = _req("/submission-spec"); print(json.dumps(d, indent=2))
    elif a.cmd == "mine":      _, d, _ = _req("/submissions/mine"); print(json.dumps(d, indent=2))
    elif a.cmd == "leaderboard": _, d, _ = _req(f"/leaderboard?problem={a.problem}"); print(json.dumps(d, indent=2))
    elif a.cmd == "snapshot":
        q = f"/discoveries/snapshot?problem={a.problem}" + ("&include=initialRelators" if a.relators else "")
        _, d, _ = _req(q)
        if a.out:
            json.dump(d, open(a.out, "w"), indent=1); print(f"saved {a.out}", file=sys.stderr)
        else:
            print(json.dumps(d, indent=2))
    elif a.cmd == "submit":    return cmd_submit(a.file, a.note)
    elif a.cmd == "status":    return cmd_status(a.id, a.wait)
    elif a.cmd == "targets":   return cmd_targets(a.snapshot, a.team, a.limit)
    return 0


if __name__ == "__main__":
    sys.exit(main())
