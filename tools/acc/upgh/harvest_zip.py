#!/usr/bin/env python3
"""Pull every road and every finished (COMPLETE) miss out of a team results zip or folder, e.g. the Colab
ACC_SPLIT30_RESULTS_20261004.zip, without unpacking it to disk. Runs on the owner's PC; no model, no API.

Outputs (in the repo):
  research/acc/live/inbox/harvest_<name>_roads.txt     every road, replayed on the pinned official core; only valid ones kept
  research/acc/live/catalog/closed_<name>.jsonl        every receipt marked COMPLETE / COMPLETE_MISS / exhausted, with its scope
  research/acc/live/catalog/incomplete_<name>.jsonl    every INCOMPLETE receipt (counts and scope only; never a closure)
The PC autopilot then feeds the roads to the global webs on its next round, and the Moves Manual row catalog reads the closures.

It understands: text lines "ac-01234: [1, 2, 3]" anywhere; JSON objects holding a move list under "moves"/"path"/"road"/
"solution"/"route" next to a row id under "challenge_id"/"row"/"problem"/"id"/"cid"; and result receipts with a "status" and a
"scope". Large binary files (sqlite checkpoints) are skipped.

usage: python3 tools/acc/upgh/harvest_zip.py PATH_TO.zip|FOLDER [--name split30] [--no-verify]
"""
import argparse
import io
import json
import os
import re
import sys
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
LINE = re.compile(r"\b(s?ac-\d{5})\s*:\s*\[([0-9,\s]+)\]")
ID_KEYS = ("challenge_id", "row", "problem", "cid", "id", "target", "problem_id")
MOVE_KEYS = ("moves", "path", "road", "solution", "route", "saved_moves", "baseline_moves", "candidate")
SKIP_EXT = (".sqlite", ".sqlite3", ".db", ".gz", ".zip", ".bin", ".pkl", ".npy", ".png", ".jpg", ".pdf")


def norm_id(v):
    s = str(v).strip()
    m = re.fullmatch(r"(s?ac-)?(\d{1,5})", s)
    if not m:
        return None
    return (m.group(1) or "ac-") + m.group(2).zfill(5)


def walk(obj, roads, receipts, src, ctx=None):
    if isinstance(obj, dict):
        own = next((norm_id(obj[k]) for k in ID_KEYS if k in obj and norm_id(obj[k])), None)
        # a parent's prefixed id (sac-06768) wins over a bare digits id (06768 -> ac-06768) for the same row
        rid = ctx if (ctx and own and own[-5:] == ctx[-5:] and not str(next((obj[k] for k in ID_KEYS if k in obj), "")).startswith(("ac-", "sac-"))) else (own or ctx)
        for k in MOVE_KEYS:
            v = obj.get(k)
            if rid and isinstance(v, list) and v and all(isinstance(x, int) and 0 <= x <= 16 for x in v):
                roads.append((rid, v, src))
        st = str(obj.get("status", "")).upper()
        if st and ("scope" in obj or "scope_fingerprint" in obj):
            sc = obj.get("scope") or {}
            row = rid
            if isinstance(sc, dict) and sc.get("row") and not rid:
                row = norm_id(sc.get("row"))
            ev = obj.get("evidence") or {}
            receipts.append({"row": row, "status": st, "exhausted": obj.get("exhausted", ev.get("exhausted")),
                             "name": obj.get("name"), "fingerprint": obj.get("scope_fingerprint") or obj.get("fingerprint"),
                             "depth_bound": sc.get("depth_bound") if isinstance(sc, dict) else None,
                             "peak_bound": sc.get("peak_bound") if isinstance(sc, dict) else None,
                             "states": ev.get("states"), "completed_depth": ev.get("completed_depth"),
                             "reason": ev.get("reason"), "source": src})
        for v in obj.values():
            walk(v, roads, receipts, src, rid)
    elif isinstance(obj, list):
        for v in obj:
            walk(v, roads, receipts, src, ctx)


def scan_text(name, data, roads, receipts):
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return
    for m in LINE.finditer(text):
        roads.append((m.group(1), [int(x) for x in m.group(2).split(",") if x.strip()], name))
    if name.endswith((".json", ".jsonl")):
        docs = []
        try:
            docs = [json.loads(text)]
        except ValueError:
            for line in text.splitlines():
                try:
                    docs.append(json.loads(line))
                except ValueError:
                    pass
        for d in docs:
            walk(d, roads, receipts, name)


def iter_files(path):
    p = Path(path)
    if p.is_dir():
        for f in p.rglob("*"):
            if f.is_file() and not f.name.lower().endswith(SKIP_EXT) and f.stat().st_size < 200_000_000:
                yield str(f.relative_to(p)), f.read_bytes()
        return
    with zipfile.ZipFile(p) as z:
        for info in z.infolist():
            n = info.filename
            if info.is_dir() or info.file_size > 200_000_000:
                continue
            if n.lower().endswith(".zip"):           # nested archive
                try:
                    inner = zipfile.ZipFile(io.BytesIO(z.read(n)))
                except zipfile.BadZipFile:
                    continue
                for ii in inner.infolist():
                    if not ii.is_dir() and not ii.filename.lower().endswith(SKIP_EXT) and ii.file_size < 200_000_000:
                        yield n + "!" + ii.filename, inner.read(ii.filename)
                continue
            if n.lower().endswith(SKIP_EXT):
                continue
            yield n, z.read(n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--name", default=None)
    ap.add_argument("--no-verify", action="store_true")
    a = ap.parse_args()
    name = a.name or re.sub(r"[^A-Za-z0-9]+", "_", Path(a.source).stem).strip("_").lower()
    roads, receipts, nfiles = [], [], 0
    for fname, data in iter_files(a.source):
        nfiles += 1
        scan_text(fname, data, roads, receipts)
    best = {}
    for rid, mv, src in roads:
        if rid not in best or len(mv) < len(best[rid][0]):
            best[rid] = (mv, src)
    print("files read %d; road mentions %d; distinct rows %d; receipts %d" % (nfiles, len(roads), len(best), len(receipts)))
    kept = best
    if not a.no_verify:
        sys.path.insert(0, str(HERE))
        import autopilot                     # clones/pins the official verifier on first use
        autopilot.ensure_verifier()
        import subprocess
        import tempfile
        sair = autopilot.SAIR
        kept, items = {}, sorted(best.items())
        for c in range(0, len(items), 400):  # the official CLI verifier takes at most 500 solutions per file
            with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as tmp:
                tmp.write("".join("%s: [%s]\n" % (rid, ",".join(map(str, mv))) for rid, (mv, _) in items[c:c + 400]))
            r = subprocess.run([sys.executable, "-m", "verifier", "--manifest", "competition/tools/verifier/data/manifest.json",
                                "--submission", tmp.name], cwd=str(sair), capture_output=True, text=True,
                               env=dict(os.environ, PYTHONPATH="competition/tools"))
            os.remove(tmp.name)
            try:
                ok = {x["challenge_id"] for x in json.loads(r.stdout).get("results", []) if x.get("ok")}
            except ValueError:
                print("verifier error:", (r.stdout + r.stderr)[-400:])
                ok = set()
            for rid, val in items[c:c + 400]:
                if rid in ok:
                    kept[rid] = val
        print("replayed on the official verifier: %d of %d valid" % (len(kept), len(best)))
    inbox = REPO / "research/acc/live/inbox"
    cat = REPO / "research/acc/live/catalog"
    inbox.mkdir(parents=True, exist_ok=True)
    cat.mkdir(parents=True, exist_ok=True)
    out = inbox / ("harvest_%s_roads.txt" % name)
    out.write_text("# roads harvested from %s (%s)\n" % (Path(a.source).name, "official verifier ok" if not a.no_verify else "NOT verified") +
                   "".join("%s: [%s]\n" % (r, ",".join(map(str, kept[r][0]))) for r in sorted(kept)))
    closed = [r for r in receipts if r["status"] in ("COMPLETE", "COMPLETE_MISS", "MISS", "CLOSED") or r.get("exhausted") is True]
    inc = [r for r in receipts if r not in closed]
    (cat / ("closed_%s.jsonl" % name)).write_text("".join(json.dumps(r) + "\n" for r in closed))
    (cat / ("incomplete_%s.jsonl" % name)).write_text("".join(json.dumps(r) + "\n" for r in inc))
    print("wrote %s (%d roads), catalog/closed_%s.jsonl (%d), catalog/incomplete_%s.jsonl (%d)" %
          (out.relative_to(REPO), len(kept), name, len(closed), name, len(inc)))


if __name__ == "__main__":
    main()
