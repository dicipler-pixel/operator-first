"""Read-only SAIR data: the live boards and our full submission history.

Reuses tools/acc/sair_api.py for transport (browser User-Agent, proxy-added
key, plain-language errors). This module never POSTs. Sending stays a human
decision made with `sair_api.py submit FILE --yes`.
"""
from __future__ import annotations

import gzip
import json
import sys
import time
import urllib.parse
from pathlib import Path

from ledger import sha256_file

TOOLS_ACC = Path(__file__).resolve().parents[1]
if str(TOOLS_ACC) not in sys.path:
    sys.path.insert(0, str(TOOLS_ACC))


def _api():
    import sair_api  # noqa: WPS433  (tools/acc/sair_api.py)
    return sair_api


def pull_boards(out_dir: Path) -> list[dict]:
    """Pull both boards. Returns board.snapshot event data (grade C)."""
    api = _api()
    out_dir.mkdir(parents=True, exist_ok=True)
    snaps = []
    for problem in ("ac", "stable_ac"):
        pulled_at = time.time()
        data = api.get("/discoveries/snapshot?problem=%s" % problem)
        stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(pulled_at))
        path = out_dir / ("%s_%s.json.gz" % (problem, stamp))
        with gzip.open(path, "wt", encoding="utf-8") as fh:
            json.dump({"pulledAt": pulled_at, "data": data}, fh)
        items = data.get("items", [])
        snaps.append({"problem": problem, "file": str(path), "sha256": sha256_file(path),
                      "pulled_at": pulled_at, "rows": len(items), "generated_at": data.get("generatedAt"),
                      "read_budget_left": api.RATE.get("remaining"),
                      "solved": sum(1 for i in items if i.get("currentBestLength") is not None),
                      "contract": data.get("contractVersion")})
    return snaps


def newest_live_board(live_dir: Path, problem: str):
    """The newest board the team's sair_api.py already pulled (no API call). Returns snapshot data or None."""
    import calendar
    files = sorted(Path(live_dir).glob("%s_2*.json.gz" % problem))
    if not files:
        return None
    path = files[-1]
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        raw = json.load(fh)
    stamp = raw.get("pulledAt")
    try:
        pulled_at = float(stamp) if not isinstance(stamp, str) else float(
            calendar.timegm(time.strptime(stamp, "%Y%m%dT%H%MZ")))
    except (TypeError, ValueError):
        pulled_at = path.stat().st_mtime
    items = raw["data"].get("items", [])
    return {"problem": problem, "file": str(path), "sha256": sha256_file(path), "pulled_at": pulled_at,
            "rows": len(items), "generated_at": raw["data"].get("generatedAt"),
            "solved": sum(1 for i in items if i.get("currentBestLength") is not None),
            "source": "imported from a sair_api.py pull (no API call)"}


def load_board(path) -> dict:
    """{cid: {"record": int|None, "k": int, "status": str}}"""
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        data = json.load(fh)["data"]
    return {it["challengeId"]: {"record": it.get("currentBestLength"),
                                "k": it.get("kTeams") or 0, "status": it.get("status")}
            for it in data["items"]}


def _sid(sub):
    try:
        return int(sub.get("submissionId"))
    except (TypeError, ValueError):
        return -1


def pull_history(out_dir: Path, previous=None, max_pages=200) -> dict:
    """Our submission history, newest first. With a previous snapshot, pages stop once they reach
    submissions already seen, so a routine pull costs one call instead of eight. Returns
    history.snapshot event data (grade C)."""
    api = _api()
    out_dir.mkdir(parents=True, exist_ok=True)
    pulled_at = time.time()
    seen_max = (previous or {}).get("max_submission_id", -1)
    items, cursor, pages, complete = [], None, 0, False
    for _ in range(max_pages):
        path = "/submissions/mine" + ("?cursor=" + urllib.parse.quote(cursor) if cursor else "")
        page = api.get(path)
        pages += 1
        got = page.get("items", [])
        items += got
        cursor = page.get("nextCursor")
        if not cursor:
            complete = True
            break
        if previous and got and min(_sid(s) for s in got) <= seen_max:
            break
    else:
        raise RuntimeError("history has more than %d pages; raise max_pages" % max_pages)
    incremental = bool(previous) and not complete
    best = dict(previous.get("best", {})) if incremental else {}
    day = time.strftime("%Y-%m-%d", time.gmtime(pulled_at))
    today = set(previous.get("today_ids", [])) if incremental and previous.get("day") == day else set()
    pending = 0
    for sub in items:
        if (sub.get("receivedAt") or "").startswith(day):
            today.add(_sid(sub))
        if sub.get("status") not in ("complete", "failed"):
            pending += 1
        for r in sub.get("results") or []:
            cid, length = r.get("challenge_id"), r.get("length")
            if r.get("ok") and isinstance(length, int):
                best[cid] = min(length, best.get(cid, length))
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime(pulled_at))
    path = out_dir / ("mine_%s.json.gz" % stamp)
    with gzip.open(path, "wt", encoding="utf-8") as fh:
        json.dump({"pulledAt": pulled_at, "items": items}, fh)
    return {"file": str(path), "sha256": sha256_file(path), "pulled_at": pulled_at,
            "submissions": (previous or {}).get("submissions", 0) + sum(1 for s in items if _sid(s) > seen_max)
            if previous and not complete else len(items),
            "max_submission_id": max([seen_max] + [_sid(s) for s in items]),
            "pages": pages, "full": complete or not previous,
            "day": day, "today_ids": sorted(today), "submitted_today_utc": len(today), "pending": pending,
            "read_budget_left": api.RATE.get("remaining"), "read_budget_reset": api.RATE.get("reset"),
            "rows": len(best), "best": dict(sorted(best.items()))}
