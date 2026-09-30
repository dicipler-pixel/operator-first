#!/usr/bin/env python3
"""Mad Hatters client for the SAIR Andrews-Curtis Challenge API (standard library only).

The key comes from the environment's API credential for api.sair.foundation (the proxy adds the
Authorization header), or from the environment variable SAIR_API_KEY. It is never printed or written.

  python3 tools/acc/sair_api.py check                   network + key + team status, in plain words
  python3 tools/acc/sair_api.py boards [--out DIR]      pull the live AC and Stable AC boards (gzip JSON)
  python3 tools/acc/sair_api.py mine                    our submission history -> our best length per row
  python3 tools/acc/sair_api.py leaderboard [ac|stable_ac]
  python3 tools/acc/sair_api.py changes                 what other teams did since the previous SAIR refresh
  python3 tools/acc/sair_api.py teams [--above N]       scoring rows of the N teams ranked just above us
Read budget: 360 GETs per window (reset 00:00 UTC seen); non-send reads stop at 40 left.
  python3 tools/acc/sair_api.py spec                    submission rules and limits
  python3 tools/acc/sair_api.py plan FILE... --sair DIR [--board DIR] [--out FILE]
        check every line with the official verifier, compare with the live board and our history,
        and write one file with only the lines that score (unsolved, beat, tie), best first
  python3 tools/acc/sair_api.py send FILE... [--yes]    THE way to submit: fresh boards + history, keep only
        unsolved/beat/tie lines not already sent, POST within 5 minutes of the pull (dry run without --yes)
  python3 tools/acc/sair_api.py send-queue [--yes]      batch rule: send research/acc/live/queue/*.txt once >= 3 lines wait
  python3 tools/acc/sair_api.py submit FILE             dry run of the raw POST (live sends go through `send`)
  python3 tools/acc/sair_api.py status SUBMISSION_ID    wait for one submission to finish
  python3 tools/acc/sair_api.py download ID...          original TXT of our past submissions (cached)

Every live submission is logged to research/acc/live/submit_log.jsonl.
"""
import argparse
import datetime as dt
import glob
import gzip
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.sair.foundation/api/public/v1/competitions/acc"
HOST = "api.sair.foundation"
# Cloudflare answers error 1010 to non-browser user agents before the API sees the request.
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/128.0 Safari/537.36")
REPO = pathlib.Path(__file__).resolve().parents[2]
LIVE = REPO / "research" / "acc" / "live"
LINE = re.compile(r"^\s*((?:ac|sac)-\d{5})\s*:\s*\[([\d,\s]*)\]\s*$")
RANK = {"unsolved": 0, "beat": 1, "tie": 2}


class ApiError(SystemExit):
    pass


# Read budget: X-Ratelimit-Limit 360 per window (reset seen at 00:00 UTC). Keep a reserve so a
# submission (`send`: boards, history, spec, me, POST, polls ~ 20 calls) is never starved.
RESERVE = 40
RATE = {"remaining": None, "reset": None}
ESSENTIAL = False


def explain(exc):
    """Turn a transport failure into a plain-language cause."""
    text = str(exc)
    if "Tunnel connection failed: 403" in text or "CONNECT tunnel failed" in text:
        return (f"blocked by this environment's network policy: add {HOST} to the allowed "
                f"domains (environment settings -> Network access)")
    if "Name or service not known" in text or "getaddrinfo" in text:
        return f"cannot resolve {HOST} (no DNS / no network)"
    if "timed out" in text:
        return f"{HOST} did not answer in time"
    return text


def call(method, path, body=None, retry=True, auth=True):
    # Key source: SAIR_API_KEY if set; otherwise the environment's API credential for
    # api.sair.foundation, which the proxy adds as "Authorization: Bearer ..." on the way out.
    key = os.environ.get("SAIR_API_KEY", "").strip()
    headers = {"Accept": "application/json", "User-Agent": UA}
    if auth and key:
        headers["Authorization"] = f"Bearer {key}"
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    for attempt in range(6 if retry else 1):
        if (not ESSENTIAL and method == "GET" and RATE["remaining"] is not None
                and RATE["remaining"] <= RESERVE):
            raise ApiError(f"read budget low ({RATE['remaining']} left until reset "
                           f"{RATE['reset']}); saving them for submissions")
        req = urllib.request.Request(BASE + path, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                raw = r.read()
                note_rate(r.headers)
                try:
                    body = json.loads(raw) if raw else {}
                except ValueError:                       # e.g. /submissions/{id}/download (TXT)
                    body = {"text": raw.decode("utf-8", "replace")}
                return r.status, body, dict(r.headers)
        except urllib.error.HTTPError as e:
            note_rate(e.headers)
            raw = e.read().decode("utf-8", "replace")
            try:
                payload = json.loads(raw)
            except ValueError:
                payload = {"raw": raw[:400]}
            if e.code == 429 and retry:
                time.sleep(min(int(e.headers.get("Retry-After", "30") or 30), 300))
                continue
            return e.code, payload, dict(e.headers)
        except (urllib.error.URLError, OSError) as e:
            if retry and attempt < 3 and "403" not in str(e):
                time.sleep(2 ** (attempt + 1))
                continue
            raise ApiError(f"cannot reach {HOST}: {explain(getattr(e, 'reason', e))}")
    return 429, {"error": "still rate limited after retries"}, {}


def note_rate(h):
    try:
        RATE["remaining"] = int(h.get("X-Ratelimit-Remaining"))
        RATE["reset"] = dt.datetime.fromtimestamp(int(h.get("X-Ratelimit-Reset")),
                                                  dt.timezone.utc).strftime("%H:%MZ")
    except (TypeError, ValueError):
        pass


def download(sid):
    """Original TXT of one of our submissions, cached in research/acc/live/downloads/."""
    path = LIVE / "downloads" / f"{sid}.txt"
    if path.exists():
        return path.read_text(encoding="utf-8")
    code, body, _ = call("GET", f"/submissions/{sid}/download")
    if code != 200 or "text" not in body:
        raise ApiError(f"download {sid}: {http_problem(code, body)}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body["text"], encoding="utf-8")
    return body["text"]


def fetch_team(team_id, problem):
    """Every row a team currently scores on: {challengeId: [length, kTeams, teamPoints]}."""
    rows, cursor, entry = {}, None, None
    while True:
        q = f"/leaderboard/teams/{team_id}/challenges?problem={problem}&limit=100"
        page = get(q + (f"&cursor={urllib.parse.quote(cursor)}" if cursor else ""))
        entry = entry or page.get("entry")
        for it in page.get("items", []):
            rows[it["challengeId"]] = [it["currentBestLength"], it["kTeams"], float(it["teamPoints"])]
        cursor = page.get("nextCursor")
        if not cursor:
            return entry, rows, page.get("generatedAt")


def teams_cmd(args):
    """Scoring rows of the teams ranked just above us (or --ranks), saved for later diffs."""
    out = LIVE / "teams"
    out.mkdir(parents=True, exist_ok=True)
    for problem in ("ac", "stable_ac"):
        me = get(f"/leaderboard/me?problem={problem}")["entry"]
        lb = get(f"/leaderboard?problem={problem}&limit=100")["items"]
        ranks = set(args.ranks) if args.ranks else set(range(max(1, me["rank"] - args.above), me["rank"] + 1))
        snap = {"problem": problem, "pulledAt": stamp(), "teams": {}}
        print(f"\n{problem}: we are rank {me['rank']}, score {float(me['score']):.4f}")
        for x in sorted(lb, key=lambda x: x["rank"]):
            if x["rank"] not in ranks:
                continue
            entry, rows, gen = fetch_team(x["team"]["teamId"], problem)
            snap["generatedAt"] = gen
            name = x["team"]["teamName"] or x["team"]["teamNumber"]
            snap["teams"][x["team"]["teamNumber"]] = {"name": name, "rank": x["rank"],
                                                     "score": x["score"], "rows": rows}
            top = sorted(rows.items(), key=lambda kv: -kv[1][2])[:args.show]
            alone = sum(1 for v in rows.values() if v[1] == 1)
            print(f"  #{x['rank']:<3} {name[:22]:22} score {float(x['score']):8.4f}  rows {len(rows):5}  "
                  f"alone {alone:3}  best: " + ", ".join(f"{c} {v[0]}/k{v[1]}" for c, v in top))
        path = out / f"{problem}_{stamp()}.json.gz"
        with gzip.open(path, "wt", encoding="utf-8") as fh:
            json.dump(snap, fh)
    print(f"\nreads left: {RATE['remaining']} (reset {RATE['reset']})")


def http_problem(code, body):
    raw = json.dumps(body)[:400]
    if code == 401:
        return ("HTTP 401: no valid key reached SAIR. Check the environment's API credential "
                "(allowed website exactly api.sair.foundation, header Authorization, prefix Bearer, "
                "value = the key only), or make a new key on the SAIR site")
    if code == 403 and "1010" in raw:
        return "HTTP 403 / Cloudflare 1010: browser User-Agent rejected"
    if code == 403:
        return f"HTTP 403: not allowed for this key/team: {raw}"
    return f"HTTP {code}: {raw}"


def get(path):
    code, body, _ = call("GET", path)
    if code != 200:
        raise ApiError(f"GET {path}: {http_problem(code, body)}")
    return body.get("data", body)


def stamp():
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%MZ")


# -- boards ----------------------------------------------------------------

def pull_boards(out, leaderboards=True):
    out = pathlib.Path(out)
    out.mkdir(parents=True, exist_ok=True)
    t = stamp()
    for problem in ("ac", "stable_ac"):
        data = get(f"/discoveries/snapshot?problem={problem}")
        items = data.get("items", [])
        path = out / f"{problem}_{t}.json.gz"
        with gzip.open(path, "wt", encoding="utf-8") as fh:
            json.dump({"pulledAt": t, "data": data}, fh)
        solved = [i for i in items if i.get("currentBestLength") is not None]
        print(f"{problem}: {len(items)} rows, {len(solved)} solved -> {path}")
        if not leaderboards:
            continue
        lb = get(f"/leaderboard?problem={problem}&limit=100")
        with gzip.open(out / f"leaderboard_{problem}_{t}.json.gz", "wt", encoding="utf-8") as fh:
            json.dump({"pulledAt": t, "data": lb}, fh)
    return t


def board_pulls(board_dir, problem, kind=""):
    """[(generatedAt, path)] for every saved pull, one per SAIR refresh, oldest first."""
    seen = {}
    for f in sorted(glob.glob(str(pathlib.Path(board_dir) / f"{kind}{problem}_*.json.gz"))):
        with gzip.open(f, "rt", encoding="utf-8") as fh:
            gen = json.load(fh)["data"].get("generatedAt")
        seen.setdefault(gen, f)
    return sorted(seen.items())


def changes(args):
    """What other teams did between two SAIR refreshes: rows whose record or team count changed,
    and team score/row-count deltas. Rows we sent in that window are marked (ours)."""
    if not args.no_pull:
        pull_boards(args.board)
    # our rows from saved history + local send log (no API reads)
    files = sorted(glob.glob(str(LIVE / "mine_2*.json")))
    mine = our_best(json.load(open(files[-1]))) if files else {}
    for cid, ln in our_best(local_history()).items():
        mine[cid] = min(ln, mine.get(cid, ln))
    for problem in ("ac", "stable_ac"):
        pulls = board_pulls(args.board, problem)
        if len(pulls) < 2:
            print(f"{problem}: need two different SAIR refreshes; pull again after the next one")
            continue
        (g0, f0), (g1, f1) = pulls[-2 - args.back], pulls[-1]
        load = lambda f: {i["challengeId"]: i for i in json.load(gzip.open(f, "rt"))["data"]["items"]}
        a, b = load(f0), load(f1)
        rows = []
        for cid, new in b.items():
            old = a.get(cid, {})
            r0, k0, r1, k1 = old.get("currentBestLength"), old.get("kTeams") or 0, new.get("currentBestLength"), new.get("kTeams") or 0
            if (r0, k0) == (r1, k1):
                continue
            what = ("SOLVED" if r0 is None else "BEAT" if r1 < r0 else "TIE" if k1 > k0 else "k down" if k1 < k0 else "?")
            ours = (" (ours)" if mine.get(cid) == r1 else
                    f" LOST OUR TIE (we have {mine[cid]})" if cid in mine and r0 is not None and mine[cid] == r0 and r1 < r0 else "")
            rows.append((what, cid, r0, k0, r1, k1, ours))
        print(f"\n{problem}: {g0} -> {g1}: {len(rows)} row(s) changed")
        order = {"SOLVED": 0, "BEAT": 1, "TIE": 2}
        for what, cid, r0, k0, r1, k1, ours in sorted(rows, key=lambda x: (order.get(x[0], 3), x[1]))[:args.limit]:
            print(f"  {what:6} {cid}  {r0}/k{k0} -> {r1}/k{k1}{ours}")
        lbs = board_pulls(args.board, problem, "leaderboard_")
        gens = {g for g, _ in lbs}
        if len(lbs) >= 2:
            (h0, l0), (h1, l1) = lbs[-2], lbs[-1]
            ld = lambda f: {x["team"]["teamNumber"]: x for x in json.load(gzip.open(f, "rt"))["data"]["items"]}
            A, B = ld(l0), ld(l1)
            moved = []
            for tn, x in B.items():
                y = A.get(tn, {"score": "0", "currentBestCount": 0, "rank": None})
                ds = float(x["score"]) - float(y["score"])
                dc = x["currentBestCount"] - y["currentBestCount"]
                if abs(ds) > 1e-9 or dc:
                    moved.append((ds, x["team"]["teamName"] or tn, x["rank"], x["score"], dc))
            print(f"  teams ({h0} -> {h1}):")
            for ds, name, rank, score, dc in sorted(moved, reverse=True)[:args.limit]:
                print(f"    {name[:24]:24} rank {rank:>3}  score {float(score):9.3f}  {ds:+8.3f}  rows {dc:+d}")


def load_board(board_dir):
    """challengeId -> (record or None, kTeams) from the newest pulled boards."""
    rec = {}
    for problem in ("ac", "stable_ac"):
        files = sorted(glob.glob(str(pathlib.Path(board_dir) / f"{problem}_*.json.gz")))
        if not files:
            raise ApiError(f"no {problem} board in {board_dir}: run `boards` first")
        with gzip.open(files[-1], "rt", encoding="utf-8") as fh:
            data = json.load(fh)["data"]
        for it in data["items"]:
            rec[it["challengeId"]] = (it.get("currentBestLength"), it.get("kTeams") or 0)
        print(f"board {problem}: {pathlib.Path(files[-1]).name}", file=sys.stderr)
    return rec


# -- our history -------------------------------------------------------------

def our_best(history):
    """challengeId -> shortest length the platform accepted from us, from /submissions/mine
    and the local log. Unknown shapes are walked generically (any dict with challenge_id/ok/length)."""
    best = {}

    def walk(x):
        if isinstance(x, dict):
            cid = x.get("challenge_id") or x.get("challengeId")
            ln = x.get("length")
            if cid and isinstance(ln, int) and x.get("ok", True) is True:
                best[cid] = min(ln, best.get(cid, ln))
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(history)
    return best


def fetch_mine():
    """All pages of /submissions/mine (20 per page, `cursor` = previous nextCursor)."""
    items, cursor = [], None
    while True:
        page = get("/submissions/mine" + (f"?cursor={urllib.parse.quote(cursor)}" if cursor else ""))
        items += page.get("items", [])
        cursor = page.get("nextCursor")
        if not cursor:
            return {"items": items, "totalCount": page.get("totalCount", len(items))}


def local_history():
    log = LIVE / "submit_log.jsonl"
    rows = []
    if log.exists():
        for line in log.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rows.append(json.loads(line))
    return rows


# -- official check ----------------------------------------------------------

def parse_lines(files):
    lines = {}
    for f in files:
        for n, raw in enumerate(pathlib.Path(f).read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip() or raw.lstrip().startswith("#"):
                continue
            m = LINE.match(raw)
            if not m:
                print(f"skip {f}:{n}: not a clean line: {raw[:60]}", file=sys.stderr)
                continue
            cid = m.group(1)
            moves = [int(x) for x in m.group(2).replace(" ", "").split(",") if x]
            if cid not in lines or len(moves) < len(lines[cid]):
                lines[cid] = moves
    return lines


def official_check(sair, lines):
    """Replay every line in the official SAIR verifier. Returns {challengeId: verified length}."""
    sair = pathlib.Path(sair)
    manifest = sair / "competition/tools/verifier/data/manifest.json"
    if not manifest.exists():
        raise ApiError(f"official verifier not found under {sair}")
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as fh:
        for cid, mv in lines.items():
            fh.write(f"{cid}: [{', '.join(map(str, mv))}]\n")
        name = fh.name
    try:
        p = subprocess.run([sys.executable, "-m", "verifier", "--manifest", str(manifest),
                            "--submission", name], capture_output=True, text=True, cwd=str(sair),
                           env={**os.environ, "PYTHONPATH": str(sair / "competition/tools")})
    finally:
        os.unlink(name)
    try:
        receipt = json.loads(p.stdout)
    except ValueError:
        raise ApiError(f"official verifier gave no JSON (exit {p.returncode}): {p.stderr[:400]}")
    ok = {}
    for r in receipt.get("results", []):
        if r.get("ok"):
            ok[r["challenge_id"]] = r["length"]
        else:
            print(f"REJECTED {r.get('challenge_id')}: {r.get('code') or r}", file=sys.stderr)
    return ok


def plan(args):
    lines = parse_lines(args.files)
    ok = official_check(args.sair, lines)
    board = load_board(args.board)
    sent = our_best(local_history())
    if not args.no_history:
        sent.update({k: min(v, sent.get(k, v)) for k, v in our_best(fetch_mine()).items()})
    rows, behind = [], []
    for cid, mv in lines.items():
        if cid not in ok or ok[cid] != len(mv):
            continue
        if cid not in board:
            print(f"{cid}: not on the live board, skipped", file=sys.stderr)
            continue
        rec, k = board[cid]
        L = len(mv)
        if cid in sent and sent[cid] <= L:
            continue                                  # already counted for us
        if rec is None:
            kind = "unsolved"
        elif L < rec:
            kind = "beat"
        elif L == rec:
            kind = "tie"
        else:
            behind.append((cid, L, rec, k))
            continue
        rows.append({"cid": cid, "kind": kind, "len": L, "rec": rec, "k": k, "moves": mv})
    rows.sort(key=lambda r: (RANK[r["kind"]], -((r["rec"] or 0) - r["len"]), r["k"], r["cid"]))
    for r in rows:
        pts = 1.0 if r["kind"] in ("unsolved", "beat") else 2.0 ** (1 - (r["k"] + 1))
        print(f"{r['kind']:8} {r['cid']}  ours {r['len']}  live {r['rec']}  k {r['k']}  ~{pts:.3g} pt")
    print(f"scoring lines: {len(rows)}   behind live: {len(behind)}")
    for cid, L, rec, k in sorted(behind, key=lambda x: x[1] - x[2])[:20]:
        print(f"  behind {cid}: ours {L} live {rec} k {k}")
    if rows:
        out = args.out or str(REPO / f"ACC_SUBMIT_API_{stamp()}.txt")
        pathlib.Path(out).write_text(
            "".join(f"{r['cid']}: [{', '.join(map(str, r['moves']))}]\n" for r in rows), encoding="utf-8")
        print(f"wrote {out}")


# -- submit ------------------------------------------------------------------

def log(entry):
    LIVE.mkdir(parents=True, exist_ok=True)
    with (LIVE / "submit_log.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")


POLL_MIN_S = 0          # `send --lean` raises this so a send spends few API calls on status polls


def wait(sid, timeout_s=1800):
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        code, body, h = call("GET", f"/submissions/{sid}")
        data = body.get("data", {})
        if code == 200 and data.get("status") in ("complete", "failed"):
            return data
        time.sleep(max(int(h.get("Retry-After", 15) or 15), POLL_MIN_S))
    return None


def summarize(sid, final, source):
    res = final.get("results", [])
    good = [r for r in res if r.get("ok")]
    print(f"submission {sid}: {final.get('status')}  accepted {len(good)} / {len(res)}")
    for r in res:
        if not r.get("ok"):
            print(f"  not accepted {r.get('challenge_id')}: {r.get('code')}")
    log({"at": stamp(), "event": "result", "submissionId": sid, "file": source,
         "status": final.get("status"),
         "results": [{k: r.get(k) for k in ("challenge_id", "ok", "length", "code")} for r in res]})


FRESH_S = 300   # user rule: the live check must be at most 5 minutes old when we POST


def send(args):
    """User rule (2026-09-27): pull boards + history fresh, keep only lines that are unsolved, beat
    or tie on their exact row and are shorter than anything we already sent, and POST within
    5 minutes of that pull. Lines must already have passed the official verifier (search session)."""
    global ESSENTIAL, POLL_MIN_S
    ESSENTIAL = True
    t0 = time.time()
    board_dir = LIVE / "boards"
    if getattr(args, "lean", False):
        # ~8 API calls instead of ~15 (owner, 2026-09-30): board snapshots only (no leaderboards), the newest page
        # of our history (older sends are already in submit_log.jsonl via the 30-min pull), slower status polls.
        pull_boards(board_dir, leaderboards=False)
        hist = {"items": get("/submissions/mine").get("items", [])}
        POLL_MIN_S = 30
    else:
        pull_boards(board_dir)
        hist = fetch_mine()
    board = load_board(board_dir)
    sent = our_best(hist)
    for cid, ln in our_best(local_history()).items():
        sent[cid] = min(ln, sent.get(cid, ln))
    lines = parse_lines(args.files)
    keep = []
    print(f"{'row':10} {'ours':>4} {'live':>4} {'k':>3}  decision")
    for cid in sorted(lines):
        L = len(lines[cid])
        rec, k = board.get(cid, (None, None))
        if cid not in board:
            why = "DROP not on board"
        elif cid in sent and sent[cid] <= L:
            why = f"DROP already sent {sent[cid]}"
        elif rec is None:
            why = "SEND unsolved"
        elif L < rec:
            why = "SEND beat"
        elif L == rec:
            why = f"SEND tie (k {k} -> {k + 1})"
        else:
            why = "DROP behind"
        print(f"{cid:10} {L:>4} {str(rec):>4} {str(k):>3}  {why}")
        if why.startswith("SEND"):
            keep.append(cid)
    if not keep:
        print("nothing to send")
        return
    out = REPO / f"ACC_SUBMIT_API_{stamp()}.txt"
    out.write_text("".join(f"{c}: [{','.join(map(str, lines[c]))}]\n" for c in keep), encoding="utf-8")
    print(f"{len(keep)} line(s) -> {out.name}")
    submit(argparse.Namespace(file=str(out), yes=args.yes), fresh_t0=t0)


def send_queue(args):
    """User rule (2026-09-28): batch sends. Verified lines wait in research/acc/live/queue/*.txt;
    send only when at least --min-lines lines are queued (or --force), through `send`."""
    qdir = LIVE / "queue"
    qdir.mkdir(parents=True, exist_ok=True)
    files = sorted(p for p in qdir.glob("*.txt"))
    lines = parse_lines([str(p) for p in files]) if files else {}
    print(f"queue: {len(lines)} line(s) in {len(files)} file(s): {', '.join(sorted(lines)) or '-'}")
    if len(lines) < args.min_lines and not args.force:
        print(f"waiting: fewer than {args.min_lines} lines queued (use --force for an urgent line)")
        return
    merged = REPO / f"ACC_QUEUE_{stamp()}.txt"
    merged.write_text("".join(f"{c}: [{','.join(map(str, lines[c]))}]\n" for c in sorted(lines)), encoding="utf-8")
    send(argparse.Namespace(files=[str(merged)], yes=args.yes, lean=getattr(args, "lean", False)))
    if args.yes:
        done = qdir / "sent"
        done.mkdir(exist_ok=True)
        for p in files:
            p.rename(done / f"{stamp()}_{p.name}")


def submit(args, fresh_t0=None):
    text = pathlib.Path(args.file).read_text(encoding="utf-8")
    body_lines = [l for l in text.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    bad = [l for l in body_lines if not LINE.match(l)]
    if bad:
        raise ApiError(f"{len(bad)} unclean line(s), first: {bad[0][:80]}")
    spec = get("/submission-spec")
    me = get("/me")
    lim = spec.get("limits", {})
    print(f"{args.file}: {len(body_lines)} lines, {len(text.encode())} bytes; "
          f"limits {lim}; open={spec.get('submissionOpen')} canSubmit={me.get('canSubmit')}")
    if lim.get("maxSolutions") and len(body_lines) > lim["maxSolutions"]:
        raise ApiError("too many lines for one submission; split the file")
    if not args.yes:
        print("dry run: nothing sent (add --yes to send; uses daily quota)")
        return
    if fresh_t0 is None:
        raise ApiError("not sending: use `send`, which checks the live board first (user rule)")
    age = time.time() - fresh_t0
    if age > FRESH_S:
        raise ApiError(f"not sending: live check is {age:.0f}s old (limit {FRESH_S}s); run `send` again")
    print(f"live check age at send: {age:.0f}s")
    if not spec.get("submissionOpen") or not me.get("canSubmit"):
        raise ApiError(f"not sending: open={spec.get('submissionOpen')} canSubmit={me.get('canSubmit')} "
                       f"reason={me.get('submitBlockedReason')}")
    try:
        code, body, _ = call("POST", "/submissions",
                             {"payload": {"text": "\n".join(body_lines) + "\n"},
                              "meta": {"description": f"Mad Hatters {pathlib.Path(args.file).name}"}},
                             retry=False)
    except ApiError as e:
        log({"at": stamp(), "event": "post-uncertain", "file": args.file, "error": str(e)})
        raise ApiError(f"POST outcome uncertain ({e}); check `mine` before sending again")
    log({"at": stamp(), "event": "post", "file": args.file, "lines": len(body_lines),
         "status": code, "body": body})
    if code != 202:
        raise ApiError(f"not accepted for verification: {http_problem(code, body)}")
    sid = body["data"]["submissionId"]
    print(f"queued as submission {sid}; waiting for verification")
    final = wait(sid)
    if final is None:
        print(f"still verifying; run: status {sid}")
    else:
        summarize(sid, final, args.file)


# -- main --------------------------------------------------------------------

def check():
    try:
        code, _, _ = call("GET", "/submission-spec", auth=False, retry=False)
        print(f"network: {HOST} reachable (HTTP {code} without key)")
    except ApiError as e:
        print(f"network: {e}")
        return 2
    if os.environ.get("SAIR_API_KEY", "").strip():
        print("key: from SAIR_API_KEY")
    else:
        print("key: none in this process; relying on the environment's API credential")
    code, body, _ = call("GET", "/me")
    if code != 200:
        print(f"key: {http_problem(code, body)}")
        return 2
    me = body.get("data", body)
    safe = {k: v for k, v in me.items() if "key" not in k.lower() and "token" not in k.lower()}
    print("key: accepted")
    print("team:", json.dumps(safe)[:800])
    spec = get("/submission-spec")
    print("submissions open:", spec.get("submissionOpen"), " limits:", json.dumps(spec.get("limits"))[:300])
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("check")
    sub.add_parser("spec")
    sub.add_parser("mine")
    b = sub.add_parser("boards")
    b.add_argument("--out", default=str(LIVE / "boards"))
    lb = sub.add_parser("leaderboard")
    lb.add_argument("problem", nargs="?", default="ac", choices=["ac", "stable_ac"])
    p = sub.add_parser("plan")
    p.add_argument("files", nargs="+")
    p.add_argument("--sair", default=os.environ.get("SAIR_REPO", ""), required=not os.environ.get("SAIR_REPO"))
    p.add_argument("--board", default=str(LIVE / "boards"))
    p.add_argument("--out")
    p.add_argument("--no-history", action="store_true", help="skip /submissions/mine")
    s = sub.add_parser("submit")
    s.add_argument("file")
    s.add_argument("--yes", action="store_true")
    tm = sub.add_parser("teams")
    tm.add_argument("--above", type=int, default=6, help="teams ranked this many places above us")
    tm.add_argument("--ranks", type=int, nargs="*")
    tm.add_argument("--show", type=int, default=4)
    ch = sub.add_parser("changes")
    ch.add_argument("--board", default=str(LIVE / "boards"))
    ch.add_argument("--no-pull", action="store_true")
    ch.add_argument("--back", type=int, default=0, help="compare with an older refresh")
    ch.add_argument("--limit", type=int, default=40)
    sd = sub.add_parser("send")
    sd.add_argument("files", nargs="+")
    sd.add_argument("--yes", action="store_true")
    sd.add_argument("--lean", action="store_true", help="~8 API calls: snapshots only, newest history page + local log")
    dl = sub.add_parser("download")
    dl.add_argument("sids", nargs="+")
    sq = sub.add_parser("send-queue")
    sq.add_argument("--min-lines", type=int, default=3)
    sq.add_argument("--force", action="store_true")
    sq.add_argument("--yes", action="store_true")
    sq.add_argument("--lean", action="store_true", help="send through `send --lean` (~8 API calls)")
    st = sub.add_parser("status")
    st.add_argument("sid")
    args = ap.parse_args()

    if args.cmd == "check":
        return check()
    if args.cmd == "spec":
        print(json.dumps(get("/submission-spec"), indent=1)[:4000])
    elif args.cmd == "boards":
        pull_boards(args.out)
    elif args.cmd == "leaderboard":
        print(json.dumps(get(f"/leaderboard?problem={args.problem}&limit=100"), indent=1)[:6000])
    elif args.cmd == "mine":
        hist = fetch_mine()
        best = our_best(hist)
        path = LIVE / f"mine_{stamp()}.json"
        LIVE.mkdir(parents=True, exist_ok=True)
        keep = ("submissionId", "status", "receivedAt", "solutionCount", "results", "errorMessage")
        path.write_text(json.dumps({"items": [{k: it.get(k) for k in keep} for it in hist["items"]]}),
                        encoding="utf-8")
        print(f"history saved to {path}; submissions: {len(hist['items'])}; accepted rows: {len(best)}")
        for cid in sorted(best):
            print(cid, best[cid])
    elif args.cmd == "plan":
        plan(args)
    elif args.cmd == "teams":
        teams_cmd(args)
    elif args.cmd == "changes":
        changes(args)
    elif args.cmd == "send-queue":
        send_queue(args)
    elif args.cmd == "send":
        send(args)
    elif args.cmd == "submit":
        submit(args)
    elif args.cmd == "download":
        for sid in args.sids:
            text = download(sid)
            print(f"{sid}: {sum(1 for l in text.splitlines() if LINE.match(l))} lines -> "
                  f"research/acc/live/downloads/{sid}.txt")
    elif args.cmd == "status":
        final = wait(args.sid, timeout_s=60) or get(f"/submissions/{args.sid}")
        summarize(args.sid, final, None)
    else:
        ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
