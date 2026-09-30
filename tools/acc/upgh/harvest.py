"""Find every move path already sitting in files, so none stays unwritten (S4).

Recognised shapes (all present in this repository):
  text lines        ac-00145: [6, 4, 12, ...]      (anywhere on a line)
  beam results      {"id": "ac-00145", "ac": [...], "sac": [...]}
  window / capped   {"row": "ac-09058", "final_path" | "path" | "sac_path": [...]}
  per-row files     ac-00286.jsonl with lines {"path": [...]}
  leads             {"id": ..., "our_best_path": [...]}
Anything else is ignored. A result the harness cannot parse counts as not
found; it is never counted as a miss.
"""
from __future__ import annotations

import glob
import json
import os
import re
from pathlib import Path

CID = re.compile(r"^(ac|sac)-(\d{5})$")
LINE = re.compile(r"\b((?:ac|sac)-\d{5})\s*:\s*\[([\d,\s]*)\]")
NAMED = re.compile(r"((?:ac|sac)-\d{5})")
AC_FIELDS = ("ac", "path", "final_path", "our_best_path", "moves", "best_path", "route", "line", "selected_path")
SAC_FIELDS = ("sac", "sac_path")


def _moves(value):
    if isinstance(value, list) and value and all(type(x) is int and x >= 0 for x in value):
        return value
    return None


def _from_obj(obj, fallback_cid, depth=0):
    """Paths in one JSON object, including objects nested up to 4 levels deep (a nested object without its
    own id inherits the enclosing row). The 20:35Z audit found valid routes skipped under nested keys."""
    if isinstance(obj, list):
        if depth < 4:
            for x in obj:
                if isinstance(x, (dict, list)):
                    yield from _from_obj(x, fallback_cid, depth + 1)
        return
    if not isinstance(obj, dict):
        return
    if depth < 4:
        own = next((obj.get(k) for k in ("id", "row", "row_id", "cid", "challenge_id")
                    if isinstance(obj.get(k), str) and CID.match(obj.get(k))), None)
        for v in obj.values():
            if isinstance(v, (dict, list)) and not _moves(v):
                yield from _from_obj(v, own or fallback_cid, depth + 1)
    cid = None
    for key in ("id", "row", "row_id", "cid", "challenge_id"):
        v = obj.get(key)
        if isinstance(v, str) and CID.match(v):
            cid = v
            break
    cid = cid or fallback_cid
    if cid is None:
        return
    m = CID.match(cid)
    ac_cid, sac_cid = "ac-" + m.group(2), "sac-" + m.group(2)
    for key in AC_FIELDS:
        moves = _moves(obj.get(key))
        if moves:
            # a "path" in a sac- file belongs to the sac row
            yield (cid if key != "ac" else ac_cid), moves, key
    for key in SAC_FIELDS:
        moves = _moves(obj.get(key))
        if moves:
            yield sac_cid, moves, key


def extract(path: Path):
    """Yield (cid, moves, where) from one file."""
    name = path.name
    named = NAMED.search(name)
    fallback = named.group(1) if named else None
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return
    if name.endswith(".jsonl"):
        for n, line in enumerate(text.splitlines(), 1):
            try:
                obj = json.loads(line)
            except ValueError:
                continue
            for cid, moves, key in _from_obj(obj, fallback):
                yield cid, moves, "%d:%s" % (n, key)
    elif name.endswith(".json"):
        try:
            data = json.loads(text)
        except ValueError:
            return
        items = data if isinstance(data, list) else [data]
        for n, obj in enumerate(items):
            for cid, moves, key in _from_obj(obj, fallback):
                yield cid, moves, "[%d].%s" % (n, key)
    else:
        for n, line in enumerate(text.splitlines(), 1):
            for m in LINE.finditer(line):
                body = m.group(2).replace(" ", "").strip(",")
                try:
                    moves = [int(x) for x in body.split(",") if x != ""]
                except ValueError:
                    continue
                if moves:
                    yield m.group(1), moves, "%d" % n


def scan(repo: Path, globs, exclude):
    files = set()
    for pattern in globs:
        for f in glob.glob(str(repo / pattern), recursive=True):
            p = Path(f)
            rel = p.relative_to(repo).as_posix()
            if p.is_file() and not any(rel.startswith(x) for x in exclude):
                files.add(p)
    return sorted(files)


def newest_mtime(files):
    return max((os.path.getmtime(f) for f in files), default=0.0)
