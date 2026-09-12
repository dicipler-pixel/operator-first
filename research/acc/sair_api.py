"""Thin client for the SAIR ACC public API (api.sair.foundation/api/public/v1).

Reads SAIR_API_KEY from the environment only; never accepts it as an argument,
never prints or stores it. Plain urllib so it works wherever egress to
api.sair.foundation is permitted. Nothing here POSTs except `submit`, which
is never called by tests.

    python3 sair_api.py me | spec
    python3 sair_api.py snapshot --problem ac --out snapshot_ac.json [--relators]
    python3 sair_api.py leaderboard --problem ac
    python3 sair_api.py mine [--all] [--out submissions_mine.json]
    python3 sair_api.py status <submissionId> [--wait]
    python3 sair_api.py submit submission.txt [--note "..."]     # consumes quota
    python3 sair_api.py reconcile snapshot.json mine.json CERT.txt... [--out-dir DIR]

`mine --all` follows nextCursor until it is null, de-duplicates by submissionId,
and reports pages / submissions / results. `reconcile` delegates to
reconcile_live.py and never touches the network.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.sair.foundation/api/public/v1/competitions/acc"


def _http(path, method="GET", body=None):
    """Perform one request. Module-level so tests can monkeypatch it."""
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
            return resp.status, json.loads(resp.read().decode("utf-8")), dict(resp.headers)
    except urllib.error.HTTPError as e:
        try:
            payload = json.loads(e.read().decode("utf-8"))
        except Exception:
            payload = {"error": str(e)}
        return e.code, payload, dict(e.headers)
    except urllib.error.URLError as e:
        return 0, {"error": f"network: {e.reason}"}, {}


def _data(payload):
    return payload.get("data", payload) if isinstance(payload, dict) else payload


def _items(payload):
    d = _data(payload)
    if isinstance(d, list):
        return d
    for k in ("items", "submissions", "results"):
        if isinstance(d.get(k), list):
            return d[k]
    return []


def _next_cursor(payload):
    d = _data(payload)
    for holder in (d, payload if isinstance(payload, dict) else {}):
        if isinstance(holder, dict):
            for k in ("nextCursor", "next_cursor", "cursor"):
                if holder.get(k):
                    return holder[k]
            meta = holder.get("meta") or holder.get("pagination") or {}
            if isinstance(meta, dict) and meta.get("nextCursor"):
                return meta["nextCursor"]
    return None


def fetch_all(path, http=None, max_pages=1000):
    """Follow nextCursor until exhausted. Returns (items, pages, errors)."""
    http = http or _http
    items, seen, pages, errors = [], set(), 0, []
    cursor = None
    while pages < max_pages:
        q = path
        if cursor:
            sep = "&" if "?" in path else "?"
            q = f"{path}{sep}cursor={urllib.parse.quote(str(cursor))}"
        status, payload, _ = http(q)
        pages += 1
        if status != 200:
            errors.append({"page": pages, "status": status, "payload": payload})
            break
        for it in _items(payload):
            sid = it.get("submissionId") or it.get("id")
            if sid is None:
                items.append(it)
                continue
            if sid in seen:
                continue
            seen.add(sid)
            items.append(it)
        cursor = _next_cursor(payload)
        if not cursor:
            break
    return items, pages, errors


def cmd_mine(all_pages, out):
    if all_pages:
        subs, pages, errors = fetch_all("/submissions/mine")
    else:
        status, payload, _ = _http("/submissions/mine")
        subs, pages, errors = _items(payload), 1, ([] if status == 200 else [{"status": status, "payload": payload}])
    subs = sorted(subs, key=lambda s: str(s.get("submissionId") or s.get("id")))
    n_results = sum(len(s.get("results") or []) for s in subs)
    doc = {"pages": pages, "submissions": len(subs), "results": n_results, "errors": errors, "items": subs}
    text = json.dumps(doc, indent=1, sort_keys=True)
    if out:
        open(out, "w", encoding="utf-8").write(text + "\n")
    else:
        print(text)
    print(f"pages={pages} submissions={len(subs)} results={n_results} errors={len(errors)}", file=sys.stderr)
    return 0 if not errors else 1


def cmd_submit(path, note):
    text = open(path, encoding="utf-8").read()
    body = {"payload": {"text": text}}
    if note:
        body["meta"] = {"description": note}
    status, data, _ = _http("/submissions", "POST", body)
    print(json.dumps(data, indent=2))
    return 0 if status == 202 else 1


def cmd_status(sid, wait):
    while True:
        status, data, headers = _http(f"/submissions/{sid}")
        st = _data(data).get("status") if isinstance(_data(data), dict) else None
        if not wait or st in ("complete", "failed") or status != 200:
            print(json.dumps(data, indent=2))
            return 0 if st == "complete" else 1
        delay = int(headers.get("Retry-After", "10") or 10)
        print(f"status={st}; retry in {delay}s", file=sys.stderr)
        time.sleep(delay)


def main(argv=None):
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("me"); sub.add_parser("spec")
    p = sub.add_parser("mine"); p.add_argument("--all", action="store_true"); p.add_argument("--out")
    p = sub.add_parser("snapshot"); p.add_argument("--problem", default="ac"); p.add_argument("--out"); p.add_argument("--relators", action="store_true")
    p = sub.add_parser("leaderboard"); p.add_argument("--problem", default="ac")
    p = sub.add_parser("submit"); p.add_argument("file"); p.add_argument("--note")
    p = sub.add_parser("status"); p.add_argument("id"); p.add_argument("--wait", action="store_true")
    p = sub.add_parser("reconcile"); p.add_argument("snapshot"); p.add_argument("mine"); p.add_argument("certs", nargs="+"); p.add_argument("--out-dir", default="private_out")
    a = ap.parse_args(argv)

    if a.cmd == "me":
        _, d, _ = _http("/me"); print(json.dumps(d, indent=2))
    elif a.cmd == "spec":
        _, d, _ = _http("/submission-spec"); print(json.dumps(d, indent=2))
    elif a.cmd == "leaderboard":
        _, d, _ = _http(f"/leaderboard?problem={a.problem}"); print(json.dumps(d, indent=2))
    elif a.cmd == "snapshot":
        q = f"/discoveries/snapshot?problem={a.problem}" + ("&include=initialRelators" if a.relators else "")
        status, d, _ = _http(q)
        if status != 200:
            print(json.dumps(d, indent=2)); return 1
        if a.out:
            open(a.out, "w").write(json.dumps(d, indent=1, sort_keys=True) + "\n"); print(f"saved {a.out} ({len(_items(d))} items)", file=sys.stderr)
        else:
            print(json.dumps(d, indent=2))
    elif a.cmd == "mine":
        return cmd_mine(a.all, a.out)
    elif a.cmd == "submit":
        return cmd_submit(a.file, a.note)
    elif a.cmd == "status":
        return cmd_status(a.id, a.wait)
    elif a.cmd == "reconcile":
        import reconcile_live
        return reconcile_live.run(a.snapshot, a.mine, a.certs, a.out_dir)
    return 0


if __name__ == "__main__":
    sys.exit(main())
