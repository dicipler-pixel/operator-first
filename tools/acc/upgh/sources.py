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
                      "pulled_at": pulled_at, "rows": len(items),
                      "solved": sum(1 for i in items if i.get("currentBestLength") is not None),
                      "contract": data.get("contractVersion")})
    return snaps


def load_board(path) -> dict:
    """{cid: {"record": int|None, "k": int, "status": str}}"""
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        data = json.load(fh)["data"]
    return {it["challengeId"]: {"record": it.get("currentBestLength"),
                                "k": it.get("kTeams") or 0, "status": it.get("status")}
            for it in data["items"]}


def pull_history(out_dir: Path, max_pages=200) -> dict:
    """Every page of /submissions/mine. Returns history.snapshot event data (grade C)."""
    api = _api()
    out_dir.mkdir(parents=True, exist_ok=True)
    pulled_at = time.time()
    items, cursor = [], None
    for _ in range(max_pages):
        path = "/submissions/mine" + ("?cursor=" + urllib.parse.quote(cursor) if cursor else "")
        page = api.get(path)
        items += page.get("items", [])
        cursor = page.get("nextCursor")
        if not cursor:
            break
    else:
        raise RuntimeError("history has more than %d pages; raise max_pages" % max_pages)
    best, today, pending = {}, 0, 0
    day = time.strftime("%Y-%m-%d", time.gmtime(pulled_at))
    for sub in items:
        if (sub.get("receivedAt") or "").startswith(day):
            today += 1
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
            "submissions": len(items), "submitted_today_utc": today, "pending": pending,
            "rows": len(best), "best": dict(sorted(best.items()))}
