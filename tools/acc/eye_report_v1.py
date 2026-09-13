"""The compound view: what each eye uniquely saw, and what no eye could see.

This is the second half of the mixer. It never reduces a claim to PASS/FAIL and
it never adds unlike outputs. It reports three levels and the relationships
between them:

  LEVEL 1  every eye, in full — its own output, unit, assumptions, failure mode,
           evidence and weight. Eyes at weight zero are printed like any other:
           they contribute nothing to a scalar and remain part of the record.

  LEVEL 2  set-level combination, only inside sets the eyes themselves declared
           commensurable, mixed through the frozen instrument by eye_log_v1.js.

  LEVEL 3  the whole-system picture — agreement, contradiction, obstruction,
           missing information, sensitivity, persistence — and, from the
           blocked_on declarations, which single new eye or theorem would open
           the most that is currently closed.

    python3 tools/acc/eye_report_v1.py <claim_id>
    python3 tools/acc/eye_report_v1.py <claim_id> --json
    python3 tools/acc/eye_report_v1.py --claims
"""

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
import os

DIR = Path(os.environ.get("ACC_EYE_DIR", ROOT / "ledger" / "eyes"))

VERDICT_ORDER = ["supports", "refutes", "orthogonal", "obstructs", "silent"]


def jsonl(p):
    p = Path(p)
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def load(claim_id=None):
    claims = jsonl(DIR / "claims_v1.jsonl")
    obs = jsonl(DIR / "observations_v1.jsonl")
    sets = jsonl(DIR / "sets_v1.jsonl")
    if claim_id:
        claims = [c for c in claims if c["claim_id"] == claim_id]
        obs = [o for o in obs if o["claim_id"] == claim_id]
        sets = [s for s in sets if s["claim_id"] == claim_id]
    return claims, obs, sets


def latest_per_eye(obs):
    """The current observation per eye, keeping the full history for persistence."""
    cur = {}
    for o in sorted(obs, key=lambda o: o["observed_utc"]):
        cur[o["eye_id"]] = o
    return cur


def relationships(claim, obs):
    """Level 3. Every entry here is derived, never asserted."""
    cur = latest_per_eye(obs)
    eyes = list(cur.values())
    by_verdict = defaultdict(list)
    for e in eyes:
        by_verdict[e["verdict"]].append(e["eye_id"])

    rel = {}

    # Agreement: two or more eyes pointing the same way on the claim itself.
    rel["agreement"] = {v: ids for v, ids in by_verdict.items()
                        if v in ("supports", "refutes") and len(ids) > 1}

    # Contradiction: the hard flag. Support and refutation cannot both stand.
    rel["contradiction"] = [
        {"supports": s, "refutes": r}
        for s in by_verdict.get("supports", []) for r in by_verdict.get("refutes", [])
    ]

    # Obstruction: eyes reporting a structural barrier rather than a result.
    rel["obstruction"] = [
        {"eye": e["eye_id"], "barrier": e.get("blocked_on") or e.get("failure_mode")}
        for e in eyes if e["verdict"] == "obstructs"
    ]

    # Missing information, two kinds. A blind spot is an eye the claim asked for
    # that never filed; a silent eye is built but has nothing it can see yet.
    wanted = {w["eye_id"]: w for w in (claim or {}).get("eyes_wanted", [])}
    rel["blind_spots"] = [
        {"eye": k, "should_see": v.get("sees"), "state": "not built"}
        for k, v in wanted.items() if k not in cur
    ]
    rel["silent"] = [
        {"eye": e["eye_id"], "sees": e.get("sees"), "blocked_on": e["blocked_on"]}
        for e in eyes if e["verdict"] == "silent"
    ]

    # Sensitivity: assumptions carried by more than one eye. If such an
    # assumption falls, every eye resting on it moves together, so their
    # apparent agreement is one observation, not several.
    shared = defaultdict(list)
    for e in eyes:
        for a in e.get("assumptions") or []:
            shared[a].append(e["eye_id"])
    rel["sensitivity"] = [{"assumption": a, "eyes": ids}
                          for a, ids in shared.items() if len(ids) > 1]

    # Persistence: has this eye said the same thing every time it looked?
    hist = defaultdict(list)
    for o in sorted(obs, key=lambda o: o["observed_utc"]):
        hist[o["eye_id"]].append(o["verdict"])
    rel["persistence"] = [
        {"eye": k, "looks": len(v), "verdicts": v,
         "stable": len(set(v)) == 1}
        for k, v in hist.items() if len(v) > 1
    ]

    # What to build next: the bridge that unblocks the most closed eyes at once.
    blockers = Counter()
    for e in eyes:
        if e.get("blocked_on"):
            blockers[e["blocked_on"]] += 1
    rel["next_eye_needed"] = [
        {"bridge": b, "unblocks": n,
         "eyes": [e["eye_id"] for e in eyes if e.get("blocked_on") == b]}
        for b, n in blockers.most_common()
    ]

    # The standing verdict is a shape, not a score.
    rel["standing"] = (
        "contradicted" if rel["contradiction"] else
        "obstructed" if rel["obstruction"] and not by_verdict.get("supports") else
        "supported" if by_verdict.get("supports") and not by_verdict.get("refutes") else
        "refuted" if by_verdict.get("refutes") and not by_verdict.get("supports") else
        "open")
    return rel


def render(claim, obs, sets, rel):
    cur = latest_per_eye(obs)
    w = []
    cid = claim["claim_id"] if claim else obs[0]["claim_id"]
    w.append("=" * 78)
    w.append(f"CLAIM  {cid}")
    if claim:
        w.append(f"       {claim['claim']}")
        if claim.get("handoff_id"):
            w.append(f"       claim sealed before the work as hand-off {claim['handoff_id']}")
    w.append("")

    w.append("LEVEL 1 — every eye, kept whole")
    w.append("-" * 78)
    for e in sorted(cur.values(), key=lambda e: (VERDICT_ORDER.index(e["verdict"]), e["eye_id"])):
        tail = "  [weight 0 — kept, contributes to no scalar]" if e["weight"] == 0 else ""
        w.append(f"  {e['eye_id']:<22} {e['verdict']:<11} {e['evidence']:<16}"
                 f" w={e['weight']:<4g}{tail}")
        if e.get("sees"):
            w.append(f"       sees        {e['sees']}")
        if e.get("output") is not None:
            out = json.dumps(e["output"], separators=(", ", ": "))
            w.append(f"       output      {out if len(out) < 300 else out[:297] + '...'}")
        if e.get("unit"):
            w.append(f"       unit        {e['unit']}")
        for a in e.get("assumptions") or []:
            w.append(f"       assumes     {a}")
        if e.get("failure_mode"):
            w.append(f"       wrong if    {e['failure_mode']}")
        if e.get("blocked_on"):
            w.append(f"       blocked on  {e['blocked_on']}")
        if e.get("reproduce"):
            w.append(f"       reproduce   {e['reproduce']}")
        w.append("")

    w.append("LEVEL 2 — set-level combination (declared commensurable sets only)")
    w.append("-" * 78)
    if not sets:
        w.append("  no eye on this claim declared a commensurable set.")
        w.append("  Nothing was added. That is the correct outcome, not a gap:")
        w.append("  these eyes measure different quantities and share no coordinate.")
    for s in sets:
        if not s.get("mixed"):
            w.append(f"  {s['set_id']}: {s.get('note')}")
            continue
        w.append(f"  {s['set_id']}  on \"{s['coordinate']}\" ({s['x_unit']}), "
                 f"{s['points']} points")
        w.append(f"       members      {', '.join(s['members'])}")
        if s.get("zero_weight"):
            w.append(f"       weight zero  {', '.join(s['zero_weight'])}  (kept in full)")
        w.append(f"       unit guard   "
                 + ("commensurable" if s["units_commensurable"]
                    else f"REFUSED — {s['unit_guard_message']}"))
        w.append(f"       replay       {'exact' if s['roundtrip_ok'] else 'FAILED'}"
                 f"   {s['recipe_path']}")
    w.append("")

    w.append("LEVEL 3 — the compound view")
    w.append("-" * 78)
    w.append(f"  standing: {rel['standing']}   "
             f"({len(cur)} eyes filed, {len(rel['blind_spots'])} never built, "
             f"{len(rel['silent'])} silent)")
    w.append("")

    def block(title, items, fmt):
        if not items:
            return
        w.append(f"  {title}")
        for it in items:
            w.append("      " + fmt(it))
        w.append("")

    if rel["agreement"]:
        w.append("  AGREEMENT")
        for v, ids in rel["agreement"].items():
            w.append(f"      {v}: {', '.join(ids)}")
        w.append("")
    block("CONTRADICTION", rel["contradiction"],
          lambda c: f"{c['supports']} supports while {c['refutes']} refutes — unresolved")
    block("OBSTRUCTION", rel["obstruction"],
          lambda o: f"{o['eye']}: {o['barrier']}")
    block("MISSING INFORMATION — no eye exists", rel["blind_spots"],
          lambda b: f"{b['eye']}: would see {b['should_see']}")
    block("MISSING INFORMATION — eye exists but cannot see", rel["silent"],
          lambda s: f"{s['eye']}: blocked on {s['blocked_on']}")
    block("SENSITIVITY — shared assumptions, correlated failure", rel["sensitivity"],
          lambda s: f"{', '.join(s['eyes'])} all rest on: {s['assumption']}")
    block("PERSISTENCE", rel["persistence"],
          lambda p: f"{p['eye']}: {' -> '.join(p['verdicts'])}"
                    f"{'' if p['stable'] else '   UNSTABLE'}")
    if rel["next_eye_needed"]:
        w.append("  WHAT TO BUILD NEXT")
        for n in rel["next_eye_needed"]:
            w.append(f"      {n['bridge']}")
            w.append(f"          unblocks {n['unblocks']} eye(s): {', '.join(n['eyes'])}")
        w.append("")
    w.append("=" * 78)
    return "\n".join(w)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("claim_id", nargs="?")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--claims", action="store_true")
    a = ap.parse_args(argv)

    if a.claims or not a.claim_id:
        claims, obs, _ = load()
        for c in claims:
            n = len({o["eye_id"] for o in obs if o["claim_id"] == c["claim_id"]})
            print(f"{c['claim_id']:<34} {n} of {len(c['eyes_wanted'])} eyes filed"
                  f"   {c['claim'][:60]}")
        if not claims:
            print("no claims recorded")
        return 0

    claims, obs, sets = load(a.claim_id)
    if not obs and not claims:
        print(f"no claim or observation matching {a.claim_id!r}")
        return 1
    claim = claims[-1] if claims else None
    rel = relationships(claim, obs)
    if a.json:
        print(json.dumps({"claim": claim, "observations": obs, "sets": sets,
                          "compound": rel}, indent=1))
        return 0
    print(render(claim, obs, sets, rel))
    return 0


if __name__ == "__main__":
    sys.exit(main())
