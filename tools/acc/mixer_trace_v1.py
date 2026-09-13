"""Query and check the Compound Eye run ledger.

The ledger at ledger/mixer/run_ledger_v1.jsonl is the project's single
append-only record of work. Every run is written there by mixer_log_v1.js,
which validates it through the frozen mixer core, so a row in this ledger is
backed by an instrument rather than by prose.

    python3 tools/acc/mixer_trace_v1.py --check          # invariants
    python3 tools/acc/mixer_trace_v1.py --summary        # one line per lane
    python3 tools/acc/mixer_trace_v1.py --lane acc       # runs in one lane
    python3 tools/acc/mixer_trace_v1.py --open           # what is unfinished
    python3 tools/acc/mixer_trace_v1.py --blocked        # what is stuck, and why
    python3 tools/acc/mixer_trace_v1.py --trace <run_id> # a run and its ancestry
    python3 tools/acc/mixer_trace_v1.py --weak           # claims with thin evidence
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "ledger" / "mixer" / "run_ledger_v1.jsonl"

EVIDENCE_RANK = {
    "exact-replay": 4,
    "computation": 3,
    "repo-provenance": 2,
    "external-source": 1,
    "none": 0,
}
STATUSES = {"verified", "refuted", "open", "blocked"}


def load(path=LEDGER):
    if not Path(path).exists():
        return []
    rows = []
    for n, line in enumerate(Path(path).read_text().splitlines(), 1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{n}: {exc}") from exc
    return rows


def key(row):
    return f"{row['lane']}/{row['run_id']}"


def check(rows):
    """Invariants. Mirrors research/acc/dag/dag.py, extended for the mixer."""
    problems = []
    seen = {}
    for r in rows:
        k = key(r)
        if k in seen:
            # Re-recording the same run is allowed only as an explicit supersede.
            if not r.get("supersedes"):
                problems.append(f"{k}: recorded twice without a supersedes pointer")
        seen[k] = r
        if r.get("status") not in STATUSES:
            problems.append(f"{k}: bad status {r.get('status')!r}")
        if r.get("evidence") not in EVIDENCE_RANK:
            problems.append(f"{k}: bad evidence {r.get('evidence')!r}")
        if r.get("status") == "verified" and r.get("evidence") == "none":
            problems.append(f"{k}: verified but evidence is none")
        if r.get("mixable") and r.get("roundtrip_ok") is False:
            problems.append(f"{k}: recipe does not replay to the same mix")
        if r.get("mixable") and not r.get("traces_path"):
            problems.append(f"{k}: marked mixable but has no traces file")
        for dep in r.get("depends_on") or []:
            if dep not in seen and dep not in {key(x) for x in rows}:
                problems.append(f"{k}: depends_on {dep} which is not in the ledger")
    # artifacts named by the ledger must exist
    for r in rows:
        for field in ("traces_path", "recipe_path"):
            p = r.get(field)
            if p and not (ROOT / p).exists():
                problems.append(f"{key(r)}: {field} {p} is missing from disk")
    return problems


def summary(rows):
    by_lane = defaultdict(list)
    for r in rows:
        by_lane[r["lane"]].append(r)
    out = []
    for lane in sorted(by_lane):
        rs = by_lane[lane]
        st = Counter(r["status"] for r in rs)
        mix = sum(1 for r in rs if r.get("mixable"))
        refused = sum(1 for r in rs if r.get("units_commensurable") is False)
        out.append(
            f"{lane:<14} {len(rs):>4} runs   "
            f"verified {st['verified']:>3}  open {st['open']:>3}  "
            f"blocked {st['blocked']:>3}  refuted {st['refuted']:>3}   "
            f"mixable {mix:>4}  unit-guard refusals {refused:>4}")
    return out


def line(r):
    bits = [f"{key(r):<38}", f"{r['status']:<9}", f"{r['evidence']:<16}"]
    if r.get("mixable"):
        bits.append(f"{r.get('channel_count', 0):>2}ch")
        bits.append("units-ok " if r.get("units_commensurable") else "unit-guard")
        bits.append("replays" if r.get("roundtrip_ok") else "NO-REPLAY")
    else:
        bits.append("claim-only".ljust(22))
    return "  ".join(bits) + "   " + r["claim"][:70]


def trace(rows, run_id):
    index = {key(r): r for r in rows}
    hits = [r for r in rows if r["run_id"] == run_id or key(r) == run_id]
    if not hits:
        return [f"no run matching {run_id!r}"]
    out = []
    for r in hits:
        out.append(line(r))
        for field in ("reproduce", "caveat", "traces_path", "recipe_path"):
            if r.get(field):
                out.append(f"      {field}: {r[field]}")
        seen, stack = set(), list(r.get("depends_on") or [])
        depth = 1
        while stack:
            nxt = []
            for d in stack:
                if d in seen:
                    continue
                seen.add(d)
                parent = index.get(d)
                out.append("      " + "  " * depth + "^ " +
                           (line(parent) if parent else f"{d}  [NOT IN LEDGER]"))
                if parent:
                    nxt.extend(parent.get("depends_on") or [])
            stack = nxt
            depth += 1
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger", default=str(LEDGER))
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--summary", action="store_true")
    ap.add_argument("--lane")
    ap.add_argument("--open", action="store_true")
    ap.add_argument("--blocked", action="store_true")
    ap.add_argument("--weak", action="store_true")
    ap.add_argument("--trace")
    args = ap.parse_args(argv)

    rows = load(args.ledger)
    if not rows:
        print(f"ledger {args.ledger} is empty or absent")
        return 0

    if args.check:
        problems = check(rows)
        if problems:
            print(f"{len(problems)} problem(s):")
            for p in problems:
                print("  " + p)
            return 1
        print(f"ledger OK — {len(rows)} runs, all invariants hold")
        return 0

    if args.summary or not any([args.lane, args.open, args.blocked, args.weak, args.trace]):
        print(f"{len(rows)} runs in {args.ledger}\n")
        for s in summary(rows):
            print(s)
        return 0

    if args.trace:
        for s in trace(rows, args.trace):
            print(s)
        return 0

    sel = rows
    if args.lane:
        sel = [r for r in sel if r["lane"] == args.lane]
    if args.open:
        sel = [r for r in sel if r["status"] == "open"]
    if args.blocked:
        sel = [r for r in sel if r["status"] == "blocked"]
    if args.weak:
        sel = [r for r in sel if EVIDENCE_RANK.get(r.get("evidence"), 0) <= 1]
    for r in sel:
        print(line(r))
        if args.blocked and r.get("caveat"):
            print(f"      blocked by: {r['caveat']}")
    print(f"\n{len(sel)} run(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
