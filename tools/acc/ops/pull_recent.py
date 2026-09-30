#!/usr/bin/env python3
"""30-minute submission tracker (ONE SAIR API call per run).

GET /submissions/mine (first page = our 20 newest submissions, each with per-line results), merged into
research/acc/live/mine_recent.json (deduped by submissionId). New results are appended to submit_log.jsonl as
"result" events so SENT_ROWS / dashboards pick them up. Writes research/acc/live/RECENT_SUBMISSIONS.md:
- uploads used today (UTC) out of the team's 40,
- API calls left today (from the rate-limit headers) out of 360,
- every submission in the last 30 minutes and the last 24 hours, with accepted/total and any failed line.

usage: python3 tools/acc/ops/pull_recent.py            (never retries on 429; prints one summary line)
"""
import datetime as dt
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve()
sys.path.insert(0, str(HERE.parents[1]))
import sair_api as s  # noqa: E402

LIVE = HERE.parents[3] / "research" / "acc" / "live"
CACHE = LIVE / "mine_recent.json"
LOG = LIVE / "submit_log.jsonl"
OUT = LIVE / "RECENT_SUBMISSIONS.md"


def when(item):
    t = item.get("receivedAt") or ""
    try:
        return dt.datetime.fromisoformat(t.replace("Z", "+00:00"))
    except ValueError:
        return None


def main():
    now = dt.datetime.now(dt.timezone.utc)
    code, body, headers = s.call("GET", "/submissions/mine", retry=False)
    left = headers.get("X-Ratelimit-Remaining") or headers.get("x-ratelimit-remaining")
    if code != 200:
        detail = body.get("error", {}) if isinstance(body, dict) else {}
        print(f"pull_recent: HTTP {code} ({detail.get('code', '')}); API calls left {left}; resets {(detail.get('details') or {}).get('resetsAt', '?')}")
        return 1
    page = body.get("data", body)
    items = page.get("items", [])

    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {"items": []}
    known = {str(i.get("submissionId")) for i in cache["items"]}
    fresh = [i for i in items if str(i.get("submissionId")) not in known]
    # keep the newest status for submissions still in progress
    by_id = {str(i.get("submissionId")): i for i in cache["items"]}
    for i in items:
        by_id[str(i.get("submissionId"))] = i
    merged = sorted(by_id.values(), key=lambda i: i.get("receivedAt") or "", reverse=True)
    CACHE.write_text(json.dumps({"pulledAt": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "totalCount": page.get("totalCount"),
                                 "items": merged}, indent=1))

    logged = set()
    if LOG.exists():
        for line in LOG.read_text().splitlines():
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("event") == "result" and d.get("status") == "complete":
                logged.add(str(d.get("submissionId")))
    with LOG.open("a") as fh:
        for i in merged:
            sid = str(i.get("submissionId"))
            if i.get("status") == "complete" and sid not in logged:
                fh.write(json.dumps({"at": now.strftime("%Y%m%dT%H%MZ"), "event": "result", "submissionId": sid,
                                     "status": "complete", "source": "pull_recent", "receivedAt": i.get("receivedAt"),
                                     "results": i.get("results", [])}) + "\n")

    today = [i for i in merged if (when(i) or now).date() == now.date()]
    last30 = [i for i in merged if when(i) and now - when(i) <= dt.timedelta(minutes=30)]
    last24 = [i for i in merged if when(i) and now - when(i) <= dt.timedelta(hours=24)]

    def row(i):
        res = i.get("results") or []
        ok = sum(1 for r in res if r.get("ok"))
        bad = [r.get("challenge_id") for r in res if not r.get("ok")]
        t = (when(i) or now).strftime("%m-%d %H:%MZ")
        return (f"| {i.get('submissionId')} | {t} | {i.get('status')} | {ok}/{len(res) or i.get('solutionCount', '?')} | "
                f"{', '.join(bad[:8]) + (' …' if len(bad) > 8 else '') or '-'} |")

    lines = [
        "# Recent submissions (auto, every 30 min; one API call per pull)",
        "",
        f"Pulled {now.strftime('%Y-%m-%d %H:%MZ')}. **Uploads today (UTC): {len(today)} / 40** (team-wide). "
        f"**API calls left today: {left} / 360** (resets 00:00Z).",
        "",
        f"## Last 30 minutes ({len(last30)})",
        "",
        "| id | received | status | accepted | failed lines |",
        "|---|---|---|---|---|",
        *([row(i) for i in last30] or ["| - | - | - | - | - |"]),
        "",
        f"## Last 24 hours ({len(last24)})",
        "",
        "| id | received | status | accepted | failed lines |",
        "|---|---|---|---|---|",
        *([row(i) for i in last24] or ["| - | - | - | - | - |"]),
        "",
        "Only the newest 20 submissions come back per pull; older ones stay in mine_recent.json.",
    ]
    OUT.write_text("\n".join(lines) + "\n")
    print(f"pull_recent: {len(items)} newest, {len(fresh)} new; last 30 min {len(last30)}; uploads today {len(today)}/40; "
          f"API calls left {left}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
