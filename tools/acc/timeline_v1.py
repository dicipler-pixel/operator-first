"""What recurs, and what happens either side of it.

Every ledger in this repository is append-only and timestamped, and the commits
that carry them are timestamped too. This reads all of them into one ordered
event stream and asks three questions the per-claim report cannot:

  RECURRENCE   which signals come back — the same blocker, the same unit-guard
               refusal, the same eye going silent, the same area of the repo
               being reopened — with how often, over what span.

  CONTEXT      for a recurring signal, what tends to happen immediately BEFORE
               it and immediately AFTER it, per occurrence and in aggregate.

  BEFORE/AFTER the board as it stood either side of a chosen anchor — a commit,
               a hand-off, a timestamp — and what changed across it.

The honesty gate comes first. A ledger written in one batch has no temporal
spread, and counting repeats inside it would manufacture a trend out of a
single write. `--window` reports the real observation window and every signal
carries a strength that is downgraded when its occurrences share one batch.

    python3 tools/acc/timeline_v1.py --window
    python3 tools/acc/timeline_v1.py --stream [--source S] [--since ISO]
    python3 tools/acc/timeline_v1.py --recurring [--min 2]
    python3 tools/acc/timeline_v1.py --context "<signal key>" [--span 3]
    python3 tools/acc/timeline_v1.py --around <commit|handoff_id|run_id|ISO>
    python3 tools/acc/timeline_v1.py snapshot
"""

import argparse
import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SNAPSHOTS = ROOT / "ledger" / "timeline" / "snapshots_v1.jsonl"

# A write batch: records closer together than this came from one command, so
# repeats inside it are one act, not a pattern over time.
BATCH_GAP_SECONDS = 2.0


def parse_utc(s):
    if not s:
        return None
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        d = datetime.fromisoformat(s)
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def jsonl(rel):
    p = ROOT / rel
    if not p.exists():
        return []
    out = []
    for line in p.read_text().splitlines():
        if line.strip():
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def ev(utc, source, kind, label, signals=(), detail=None, ident=None):
    return {"utc": utc, "source": source, "kind": kind, "label": label,
            "signals": list(signals), "detail": detail, "id": ident}


def short(s, n=70):
    s = " ".join(str(s).split())
    return s if len(s) <= n else s[:n - 1] + "…"


def collect_events():
    """One ordered stream from every ledger plus the commits that carry them."""
    events = []

    for r in jsonl("ledger/mixer/run_ledger_v1.jsonl"):
        sig = [("status", f"{r['lane']}:{r['status']}"), ("evidence", r["evidence"])]
        if r.get("units_commensurable") is False:
            sig.append(("unit-guard", r.get("unit_guard_message")))
        if r.get("caveat"):
            sig.append(("caveat", r["caveat"]))
        events.append(ev(parse_utc(r.get("recorded_utc")), "mixer-run", r["status"],
                         f"{r['lane']}/{r['run_id']}", sig, r.get("claim"),
                         f"{r['lane']}/{r['run_id']}"))

    for r in jsonl("ledger/eyes/claims_v1.jsonl"):
        events.append(ev(parse_utc(r.get("written_utc")), "eye-claim", "claim",
                         r["claim_id"],
                         [("roster", f"{r['claim_id']}:{len(r['eyes_wanted'])} eyes")],
                         r.get("claim"), r["claim_id"]))

    for r in jsonl("ledger/eyes/observations_v1.jsonl"):
        sig = [("verdict", f"{r['eye_id']}:{r['verdict']}"), ("evidence", r["evidence"])]
        if r.get("blocked_on"):
            sig.append(("blocker", r["blocked_on"]))
        if r.get("failure_mode"):
            sig.append(("failure-mode", r["failure_mode"]))
        for a in r.get("assumptions") or []:
            sig.append(("assumption", a))
        if r.get("weight") == 0:
            sig.append(("weight-zero", r["eye_id"]))
        events.append(ev(parse_utc(r.get("observed_utc")), "eye-obs", r["verdict"],
                         f"{r['claim_id']}/{r['eye_id']}", sig, r.get("sees"),
                         r["eye_id"]))

    for r in jsonl("ledger/eyes/sets_v1.jsonl"):
        sig = [("set", r["set_id"])]
        if r.get("units_commensurable") is False:
            sig.append(("unit-guard", r.get("unit_guard_message")))
        if r.get("roundtrip_ok") is False:
            sig.append(("replay-failure", r["set_id"]))
        events.append(ev(parse_utc(r.get("mixed_utc")), "eye-set",
                         "mixed" if r.get("mixed") else "not-mixed",
                         f"{r['claim_id']}/{r['set_id']}", sig, None, r["set_id"]))

    for rel in ("ledger/handoff/handoffs_v1.jsonl", "ledger/handoff/handoffs_v2.jsonl"):
        for r in jsonl(rel):
            rec = r.get("record")
            if rec == "seal":
                n = len(r.get("artifacts") or ([r["artifact"]] if r.get("artifact") else []))
                events.append(ev(parse_utc(r.get("sealed_utc")), "handoff", "seal",
                                 f"{r['handoff_id']} by {r['producer']}",
                                 [("seal", r["producer"]),
                                  ("package", f"{n} artifact(s)")],
                                 short(r.get("claim"), 90), r["handoff_id"]))
            elif rec in ("verify", "check"):
                st = r.get("transport_status") or r.get("status")
                events.append(ev(parse_utc(r.get("checked_utc")), "handoff",
                                 f"transport:{st}",
                                 f"{r['handoff_id']} by {r['checker']}",
                                 [("transport", st)],
                                 r.get("transport_reason") or r.get("failure_reason"),
                                 r["handoff_id"]))
            elif rec == "attest":
                events.append(ev(parse_utc(r.get("attested_utc")), "handoff",
                                 f"claim:{r['claim_status']}",
                                 f"{r['handoff_id']} by {r['checker']}",
                                 [("attest", r["claim_status"])], None,
                                 r["handoff_id"]))

    for r in jsonl("ledger/timeline/snapshots_v1.jsonl"):
        events.append(ev(parse_utc(r.get("taken_utc")), "snapshot", "board",
                         r.get("commit") or "-", [("snapshot", "board")],
                         json.dumps(r.get("board")), r.get("commit")))

    # Commits touching any ledger or the acc tools: the longer clock, and the
    # only series here with real spread.
    try:
        out = subprocess.run(
            ["git", "log", "--format=%H%x1f%aI%x1f%s", "--date=iso-strict",
             "--", "ledger/", "tools/acc/", ".github/workflows/acc-eye.yml"],
            cwd=ROOT, capture_output=True, text=True, timeout=30).stdout
        for line in out.splitlines():
            parts = line.split("\x1f")
            if len(parts) != 3:
                continue
            sha, iso, subject = parts
            area = subject.split(":", 1)[0].strip() if ":" in subject[:20] else "other"
            events.append(ev(parse_utc(iso), "commit", area, sha[:7],
                             [("commit-area", area)], subject, sha[:7]))
    except Exception:
        pass

    return order(events)


def order(events):
    """Time-order and index. Undated records are separated, never interleaved:
    a record with no timestamp cannot support a before/after claim."""
    dated = [e for e in events if e.get("utc")]
    undated = [e for e in events if not e.get("utc")]
    dated.sort(key=lambda e: e["utc"])
    for i, e in enumerate(dated):
        e["ordinal"] = i
    return dated, undated


def batches(events):
    """Group events into write batches separated by more than BATCH_GAP_SECONDS."""
    out, cur = [], []
    prev = None
    for e in events:
        if prev is not None and (e["utc"] - prev).total_seconds() > BATCH_GAP_SECONDS:
            out.append(cur); cur = []
        cur.append(e); prev = e["utc"]
    if cur:
        out.append(cur)
    return out


def window_report(events, undated):
    by_source = defaultdict(list)
    for e in events:
        by_source[e["source"]].append(e)
    w = ["OBSERVATION WINDOW", "-" * 74]
    if not events:
        return "\n".join(w + ["  nothing recorded"])
    span = (events[-1]["utc"] - events[0]["utc"]).total_seconds()
    w.append(f"  {len(events)} dated events from {events[0]['utc'].isoformat()}")
    w.append(f"  {'':>17}to {events[-1]['utc'].isoformat()}")
    w.append(f"  wall-clock span {span / 3600:.2f} h across {len(batches(events))} write batches")
    w.append("")
    w.append(f"  {'source':<14}{'events':>7}{'batches':>9}{'span':>12}   note")
    for src in sorted(by_source):
        es = by_source[src]
        s = (es[-1]["utc"] - es[0]["utc"]).total_seconds()
        b = len(batches(es))
        note = ("single write — no temporal spread" if b == 1 and s < BATCH_GAP_SECONDS
                else "ordered over time")
        w.append(f"  {src:<14}{len(es):>7}{b:>9}{s:>11.1f}s   {note}")
    if undated:
        w.append("")
        w.append(f"  {len(undated)} records carry no timestamp and are ordered only by "
                 f"file position;")
        w.append(f"  they cannot support a before/after claim and are excluded from it.")
    w.append("")
    w.append("  Reading: a source written in one batch was produced by one command.")
    w.append("  Repeats inside it are one act, not a pattern over time.")
    return "\n".join(w)


def signal_index(events):
    idx = defaultdict(list)
    for e in events:
        for kind, key in e["signals"]:
            idx[f"{kind}={key}"].append(e)
    return idx


def strength(occurrences):
    """How much weight a repeat count can carry, given when the repeats happened."""
    if len(occurrences) < 2:
        return "single", "seen once"
    b = len(batches(occurrences))
    span = (occurrences[-1]["utc"] - occurrences[0]["utc"]).total_seconds()
    if b == 1:
        return "one-batch", ("all occurrences written by one command — "
                             "not evidence of recurrence over time")
    if span < 3600:
        return "one-session", f"spread over {span / 60:.0f} min within one session"
    if span < 86400:
        return "one-day", f"spread over {span / 3600:.1f} h"
    return "sustained", f"spread over {span / 86400:.1f} days"


def recurring_report(events, minimum=2):
    idx = signal_index(events)
    rows = []
    for key, occ in idx.items():
        if len(occ) < minimum:
            continue
        s, why = strength(occ)
        rows.append((len(occ), s, key, occ, why))
    order = {"sustained": 0, "one-day": 1, "one-session": 2, "one-batch": 3, "single": 4}
    rows.sort(key=lambda r: (order[r[1]], -r[0]))
    w = [f"RECURRING SIGNALS (seen {minimum}+ times)", "-" * 74]
    if not rows:
        return "\n".join(w + ["  nothing repeats yet"])
    cur = None
    for n, s, key, occ, why in rows:
        if s != cur:
            cur = s
            w.append("")
            w.append(f"  [{s}]  {why if s != 'one-batch' else why}")
        w.append(f"    {n:>3}x  {short(key, 68)}")
        w.append(f"         first {occ[0]['utc'].strftime('%H:%M:%S')}  "
                 f"last {occ[-1]['utc'].strftime('%H:%M:%S')}  "
                 f"sources: {', '.join(sorted({o['source'] for o in occ}))}")
    return "\n".join(w)


def context_report(events, key, span=3):
    idx = signal_index(events)
    matches = [k for k in idx if key.lower() in k.lower()]
    if not matches:
        return f"no signal matching {key!r}\n(try --recurring to list them)"
    w = []
    for k in matches[:5]:
        occ = idx[k]
        s, why = strength(occ)
        w.append(f"CONTEXT FOR  {short(k, 66)}")
        w.append(f"  {len(occ)} occurrence(s), strength {s} — {why}")
        w.append("-" * 74)
        before_kinds, after_kinds = Counter(), Counter()
        for o in occ:
            i = o["ordinal"]
            pre = [e for e in events if i - span <= e["ordinal"] < i]
            post = [e for e in events if i < e["ordinal"] <= i + span]
            for e in pre:
                before_kinds[f"{e['source']}/{e['kind']}"] += 1
            for e in post:
                after_kinds[f"{e['source']}/{e['kind']}"] += 1
            w.append(f"\n  at {o['utc'].isoformat()}  {o['source']}  {o['label']}")
            for e in pre:
                w.append(f"      before  {e['source']:<12}{short(e['label'], 46)}")
            w.append(f"    > HERE    {o['source']:<12}{short(o['label'], 46)}")
            for e in post:
                w.append(f"      after   {e['source']:<12}{short(e['label'], 46)}")
        if len(occ) > 1:
            w.append("\n  most often immediately before:")
            for kk, n in before_kinds.most_common(4):
                w.append(f"      {n:>3}x  {kk}")
            w.append("  most often immediately after:")
            for kk, n in after_kinds.most_common(4):
                w.append(f"      {n:>3}x  {kk}")
        w.append("")
    return "\n".join(w)


def board(events):
    """State implied by every event up to this point."""
    b = {"mixer_runs": Counter(), "eye_verdicts": {}, "blockers": set(),
         "handoff_transport": {}, "handoff_claim": {}, "commits": 0}
    for e in events:
        if e["source"] == "mixer-run":
            b["mixer_runs"][e["kind"]] += 1
        elif e["source"] == "eye-obs":
            b["eye_verdicts"][e["id"]] = e["kind"]
            for kind, key in e["signals"]:
                if kind == "blocker":
                    b["blockers"].add(key)
        elif e["source"] == "handoff":
            if e["kind"].startswith("transport:"):
                b["handoff_transport"][e["id"]] = e["kind"].split(":", 1)[1]
            elif e["kind"].startswith("claim:"):
                b["handoff_claim"][e["id"]] = e["kind"].split(":", 1)[1]
        elif e["source"] == "commit":
            b["commits"] += 1
    return b


def resolve_anchor(events, anchor):
    t = parse_utc(anchor)
    if t:
        return t, f"timestamp {anchor}"
    for e in events:
        if e["id"] and (e["id"] == anchor or str(e["id"]).startswith(anchor)):
            return e["utc"], f"{e['source']} {e['label']}"
    return None, None


def around_report(events, anchor):
    t, what = resolve_anchor(events, anchor)
    if not t:
        return f"no commit, hand-off, run or timestamp matching {anchor!r}"
    before = [e for e in events if e["utc"] < t]
    after = events
    bb, ba = board(before), board(after)
    w = [f"BEFORE AND AFTER  {what}", f"  anchor {t.isoformat()}", "-" * 74,
         f"  {len(before)} events before, {len(after) - len(before)} at or after", ""]

    def line(name, a, b):
        mark = "  " if a == b else "->"
        w.append(f"  {mark} {name:<26} {a!s:<28} {b!s}")

    w.append(f"     {'':<26} {'before':<28} after")
    line("mixer runs verified", bb["mixer_runs"]["verified"], ba["mixer_runs"]["verified"])
    line("mixer runs blocked", bb["mixer_runs"]["blocked"], ba["mixer_runs"]["blocked"])
    line("eyes filed", len(bb["eye_verdicts"]), len(ba["eye_verdicts"]))
    line("eyes silent",
         sum(1 for v in bb["eye_verdicts"].values() if v == "silent"),
         sum(1 for v in ba["eye_verdicts"].values() if v == "silent"))
    line("distinct blockers", len(bb["blockers"]), len(ba["blockers"]))
    line("hand-offs transport-checked", len(bb["handoff_transport"]), len(ba["handoff_transport"]))
    line("hand-offs claim-attested", len(bb["handoff_claim"]), len(ba["handoff_claim"]))
    line("commits touching the ledgers", bb["commits"], ba["commits"])

    new_blockers = ba["blockers"] - bb["blockers"]
    gone = bb["blockers"] - ba["blockers"]
    if new_blockers:
        w.append("\n  blockers that appeared at or after the anchor:")
        for x in sorted(new_blockers):
            w.append(f"      + {x}")
    if gone:
        w.append("\n  blockers present before and not after:")
        for x in sorted(gone):
            w.append(f"      - {x}")
    flips = [(k, bb["eye_verdicts"][k], ba["eye_verdicts"][k])
             for k in bb["eye_verdicts"]
             if ba["eye_verdicts"].get(k) != bb["eye_verdicts"][k]]
    if flips:
        w.append("\n  eyes whose verdict changed across the anchor:")
        for k, a, b in flips:
            w.append(f"      {k}: {a} -> {b}")
    return "\n".join(w)


def take_snapshot(events):
    """Append the current board. Running this on a schedule is what makes the
    record get longer; nothing else here creates temporal spread."""
    sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                         capture_output=True, text=True).stdout.strip()[:12]
    b = board(events)
    row = {
        "schema": "acc-timeline-snapshot-v1",
        "taken_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "commit": sha,
        "board": {
            "mixer_runs": dict(b["mixer_runs"]),
            "eyes_filed": len(b["eye_verdicts"]),
            "eye_verdicts": b["eye_verdicts"],
            "blockers": sorted(b["blockers"]),
            "handoff_transport": b["handoff_transport"],
            "handoff_claim": b["handoff_claim"],
        },
    }
    SNAPSHOTS.parent.mkdir(parents=True, exist_ok=True)
    with SNAPSHOTS.open("a") as fh:
        fh.write(json.dumps(row) + "\n")
    return row


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", nargs="?", choices=["snapshot"])
    ap.add_argument("--window", action="store_true")
    ap.add_argument("--stream", action="store_true")
    ap.add_argument("--recurring", action="store_true")
    ap.add_argument("--min", type=int, default=2)
    ap.add_argument("--context")
    ap.add_argument("--span", type=int, default=3)
    ap.add_argument("--around")
    ap.add_argument("--source")
    ap.add_argument("--since")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    events, undated = collect_events()

    if a.cmd == "snapshot":
        row = take_snapshot(events)
        n = len(jsonl("ledger/timeline/snapshots_v1.jsonl"))
        print(f"snapshot at {row['taken_utc']} on {row['commit']} — "
              f"{n} snapshot(s) on record")
        if n < 2:
            print("  one snapshot is a point, not a series. Take more over time "
                  "before reading anything as a trend.")
        return 0

    if a.json:
        print(json.dumps({
            "events": [{**e, "utc": e["utc"].isoformat()} for e in events],
            "undated": len(undated)}, indent=1))
        return 0

    if a.around:
        print(around_report(events, a.around))
        return 0
    if a.context:
        print(context_report(events, a.context, a.span))
        return 0
    if a.recurring:
        print(window_report(events, undated))
        print()
        print(recurring_report(events, a.min))
        return 0
    if a.stream:
        sel = events
        if a.source:
            sel = [e for e in sel if e["source"] == a.source]
        since = parse_utc(a.since) if a.since else None
        if since:
            sel = [e for e in sel if e["utc"] >= since]
        for e in sel:
            print(f"{e['utc'].strftime('%m-%d %H:%M:%S')}  {e['source']:<12}"
                  f"{e['kind']:<20}{short(e['label'], 40)}")
        print(f"\n{len(sel)} event(s)")
        return 0

    print(window_report(events, undated))
    return 0


if __name__ == "__main__":
    sys.exit(main())
