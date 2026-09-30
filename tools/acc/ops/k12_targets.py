#!/usr/bin/env python3
"""Offline target list: every row whose record is held by 1 or 2 teams (AC and Stable), joined with what we hold.

Sources (no API calls): the newest board snapshot in research/acc/live/boards/, a snapshot about 24 h older for
"what changed", our accepted lengths (mine_2*.json + mine_recent.json + submit_log.jsonl), and every unsent path in
the capped-run files (*.jsonl with "id"/"ac"/"sac" fields) under ACC_S (default: none).

Writes research/acc/live/TARGETS_K12_<board stamp>.json and .md:
  - WIN NOW: a verified-length path in hand at or under the record that we have not had accepted (send candidates).
  - CLOSE: we hold a path 1-3 over the record (search / DP work).
  - HELD: our accepted line is already on the record (only a beat adds points).
  - OPEN: no path of ours (fresh work; sorted by record length, shortest first).
  - NEW: rows whose record or k changed in the last ~24 h (fresh 1-2 team rows).
Value: a beat is 1.0; joining a k-team tie is 2^-k (k=1 -> 0.5, k=2 -> 0.25).

usage: ACC_S=<scratchpad> python3 tools/acc/ops/k12_targets.py
"""
import datetime as dt
import glob
import gzip
import json
import os
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
LIVE = ROOT / "research" / "acc" / "live"
NEVER = {"ac-09839", "sac-02257", "ac-09311", "ac-06403", "ac-04718", "ac-05378"}


def load_board(stamp_glob):
    out = {}
    for p in ("ac", "stable_ac"):
        f = sorted(glob.glob(str(LIVE / "boards" / f"{p}_{stamp_glob}.json.gz")))[-1]
        for x in json.load(gzip.open(f))["data"]["items"]:
            out[x["challengeId"]] = (x.get("currentBestLength"), x.get("kTeams") or 0)
    return out, f


def stamp_of(f):
    return pathlib.Path(f).name.split("_")[-1].split(".")[0]


def main():
    now_board, fnow = load_board("*")
    t_now = dt.datetime.strptime(stamp_of(fnow), "%Y%m%dT%H%MZ")
    old = None
    for f in sorted(glob.glob(str(LIVE / "boards" / "ac_*.json.gz"))):
        t = dt.datetime.strptime(stamp_of(f), "%Y%m%dT%H%MZ")
        if t <= t_now - dt.timedelta(hours=20):
            old = stamp_of(f)
    old_board = load_board(old)[0] if old else {}

    mine = {}
    for fn in glob.glob(str(LIVE / "mine_2*.json")) + [str(LIVE / "mine_recent.json")]:
        if not os.path.exists(fn):
            continue
        for it in json.load(open(fn)).get("items", []):
            for r in it.get("results") or []:
                if r.get("ok"):
                    mine[r["challenge_id"]] = min(mine.get(r["challenge_id"], 1 << 30), r["length"])
    for line in open(LIVE / "submit_log.jsonl"):
        try:
            x = json.loads(line)
        except ValueError:
            continue
        if x.get("event") == "result":
            for r in x.get("results") or []:
                if r.get("ok") and r.get("length"):
                    mine[r["challenge_id"]] = min(mine.get(r["challenge_id"], 1 << 30), r["length"])

    pool = {}  # row -> (length, source file) for unsent capped-run paths (lengths as reported by the runner)
    S = os.environ.get("ACC_S")
    if S:
        for fn in glob.glob(f"{S}/**/*.jsonl", recursive=True):
            try:
                fh = open(fn)
            except OSError:
                continue
            for line in fh:
                if '"id"' not in line:
                    continue
                try:
                    x = json.loads(line)
                except ValueError:
                    continue
                i = x.get("id")
                if not isinstance(i, str) or not i.startswith("ac-"):
                    continue
                for key, rid in (("ac", i), ("sac", "s" + i)):
                    p = x.get(key)
                    if isinstance(p, list) and p and all(isinstance(m, int) for m in p):
                        if rid not in pool or len(p) < pool[rid][0]:
                            pool[rid] = (len(p), os.path.relpath(fn, S))

    rows = []
    for rid, (rec, k) in now_board.items():
        if rec is None or k not in (1, 2) or rid in NEVER:
            continue
        acc = mine.get(rid)
        pl = pool.get(rid, (None, None))
        best = min([v for v in (acc, pl[0]) if v is not None], default=None)
        orec, ok_ = old_board.get(rid, (None, None))
        new = orec != rec or ok_ != k
        if acc is not None and acc <= rec:
            status = "HELD"
        elif pl[0] is not None and pl[0] <= rec:
            status = "WIN NOW"
        elif best is not None and best - rec <= 3:
            status = "CLOSE"
        else:
            status = "OPEN"
        gain = 1.0 if (best is not None and best < rec) else 2.0 ** -k
        rows.append({"id": rid, "board": "stable" if rid.startswith("sac") else "ac", "record": rec, "k": k,
                     "ours_accepted": acc, "ours_pool": pl[0], "pool_file": pl[1], "gap": None if best is None else best - rec,
                     "status": status, "value_if_tie": 2.0 ** -k, "new_24h": new, "old_record": orec, "old_k": ok_,
                     "gain": gain if status != "HELD" else 0.0})
    order = {"WIN NOW": 0, "CLOSE": 1, "OPEN": 2, "HELD": 3}
    rows.sort(key=lambda r: (order[r["status"]], r["k"], r["gap"] if r["gap"] is not None else 99, r["record"]))
    st = stamp_of(fnow)
    (LIVE / f"TARGETS_K12_{st}.json").write_text(json.dumps(rows, indent=0))

    def cnt(pred):
        return sum(1 for r in rows if pred(r))
    md = [f"# Rows held by 1 or 2 teams (boards {st}; changes vs {old or 'n/a'})", "",
          "Value: beat 1.0; joining a tie 0.5 at k=1, 0.25 at k=2. Owner rows excluded.", "",
          "| | AC k=1 | AC k=2 | Stable k=1 | Stable k=2 |", "|---|---|---|---|---|"]
    for s_ in ("WIN NOW", "CLOSE", "OPEN", "HELD"):
        md.append(f"| {s_} | " + " | ".join(str(cnt(lambda r: r['status'] == s_ and r['board'] == b and r['k'] == kk))
                                             for b in ("ac", "stable") for kk in (1, 2)) + " |")
    md.append(f"| new in 24 h | " + " | ".join(str(cnt(lambda r: r['new_24h'] and r['board'] == b and r['k'] == kk))
                                               for b in ("ac", "stable") for kk in (1, 2)) + " |")
    md += ["", "Potential if every non-HELD row were tied: "
           f"{sum(r['value_if_tie'] for r in rows if r['status'] != 'HELD'):.1f} points.", ""]

    def table(title, sel, lim):
        md.extend([f"## {title} ({len(sel)})", "", "| row | record | k | ours (accepted / pool) | gap | new 24h |",
                   "|---|---|---|---|---|---|"])
        for r in sel[:lim]:
            md.append(f"| {r['id']} | {r['record']} | {r['k']} | {r['ours_accepted'] or '-'} / {r['ours_pool'] or '-'} | "
                      f"{'' if r['gap'] is None else ('+' if r['gap'] > 0 else '') + str(r['gap'])} | "
                      f"{'yes (was ' + str(r['old_record']) + '/k' + str(r['old_k']) + ')' if r['new_24h'] else ''} |")
        if len(sel) > lim:
            md.append(f"| … {len(sel) - lim} more in the JSON | | | | | |")
        md.append("")
    table("WIN NOW: path in hand at/under record, not yet accepted", [r for r in rows if r["status"] == "WIN NOW"], 200)
    table("CLOSE: 1-3 over", [r for r in rows if r["status"] == "CLOSE"], 150)
    table("NEW in 24 h and not held", [r for r in rows if r["new_24h"] and r["status"] != "HELD"], 80)
    table("OPEN, shortest records first", [r for r in rows if r["status"] == "OPEN"], 60)
    (LIVE / f"TARGETS_K12_{st}.md").write_text("\n".join(md) + "\n")
    print(f"k12 targets {st}: {len(rows)} rows; WIN NOW {cnt(lambda r: r['status'] == 'WIN NOW')}, "
          f"CLOSE {cnt(lambda r: r['status'] == 'CLOSE')}, OPEN {cnt(lambda r: r['status'] == 'OPEN')}, "
          f"HELD {cnt(lambda r: r['status'] == 'HELD')}, new 24h {cnt(lambda r: r['new_24h'])}")


if __name__ == "__main__":
    main()
