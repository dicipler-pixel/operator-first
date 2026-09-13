"""Backfill the Compound Eye run ledger from artifacts already in this repo.

Every run below is built from a file that exists, with channels read straight
out of it. Nothing is invented: where a piece of work produced no numeric
channels on a common coordinate it is recorded as a claim only, with no
fabricated coordinate.

    python3 tools/acc/mixer_backfill_v1.py          # write runs.json
    python3 tools/acc/mixer_backfill_v1.py --record # write and record it
"""

import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "ledger" / "mixer" / "backfill_runs_v1.json"


def commit():
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                              capture_output=True, text=True).stdout.strip()[:12]
    except Exception:
        return None


def jsonl(path):
    p = ROOT / path
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def acc_postrun():
    """848 post-run mixes; channels read straight out of the existing ledger."""
    rows = jsonl("tools/acc/postrun_mix_ledger_v1.jsonl")
    if not rows:
        return None
    rows = [r for r in rows if isinstance(r.get("steps"), (int, float))]
    return {
        "lane": "acc",
        "run_id": "postrun-mix-v1",
        "title": "ACC post-run mix over every decoded run",
        "claim": (f"Mixing after every run over {len(rows)} recipes produced "
                  f"{sum(1 for r in rows if r.get('identity_mismatches'))} identity "
                  f"mismatches and "
                  f"{sum(1 for r in rows if not r.get('roundtrip'))} round-trip failures."),
        "evidence": "computation",
        "status": "verified",
        "reproduce": ("node tools/acc/acc_postrun_mix_v1.js tools/acc/decoded "
                      "tools/acc/postrun_mix_ledger_v1.jsonl"),
        "object_id": "acc_decoded_runs",
        "model_id": "acc_postrun_mix_v1",
        "coordinate": "recipe index",
        "x_unit": "recipe ordinal",
        "x": list(range(len(rows))),
        "channels": [
            {"id": "steps", "label": "Steps in the run", "unit": "steps",
             "values": [r["steps"] for r in rows]},
            {"id": "plateau_steps", "label": "Plateau steps", "unit": "steps",
             "values": [r.get("plateau_steps", 0) for r in rows]},
            {"id": "final_length", "label": "Final presentation length", "unit": "letters",
             "values": [r.get("final_length", 0) for r in rows]},
            {"id": "max_length", "label": "Peak presentation length", "unit": "letters",
             "values": [r.get("max_length", 0) for r in rows]},
        ],
        "observed": {
            "recipes": len(rows),
            "identity_mismatch_runs": sum(1 for r in rows if r.get("identity_mismatches")),
            "roundtrip_failures": sum(1 for r in rows if not r.get("roundtrip")),
            "default_refusals": sum(1 for r in rows if r.get("default_refused")),
        },
        "caveat": ("Steps and lengths carry different units, so the mixer's unit "
                   "guard refuses to add them under source normalization. That "
                   "refusal is the correct reading, not a defect."),
        "source": {"repo": "operator-first", "commit": commit(),
                   "path": "tools/acc/postrun_mix_ledger_v1.jsonl"},
    }


def lean_ledger():
    """Lean certificate ledger: verified / failed / unverified per source file."""
    rows = jsonl("ledger/LEAN_CERTIFICATE_LEDGER_2026-09-13.jsonl")
    if not rows:
        return None
    per = defaultdict(Counter)
    for r in rows:
        per[r["file"]][r["status"]] += 1
    files = sorted(per, key=lambda f: -sum(per[f].values()))
    tally = Counter(r["status"] for r in rows)
    return {
        "lane": "lean",
        "run_id": "certificate-ledger-2026-09-13",
        "title": "Lean certificate ledger by source file",
        "claim": (f"{tally['VERIFIED']} of {len(rows)} unique Lean declarations are "
                  f"verified by a named CI run; {tally['FAILED-AT-HEAD']} fail at head "
                  f"and {tally.get('UNVERIFIED', 0)} are unverified."),
        "evidence": "repo-provenance",
        "status": "verified",
        "reproduce": "python3 ledger/tools/render.py <workdir> ledger/LEAN_CERTIFICATE_LEDGER_2026-09-13",
        "object_id": "lean_declarations",
        "model_id": "lean_certificate_ledger_v1",
        "coordinate": "source file rank",
        "x_unit": "file ordinal by declaration count",
        "x": list(range(len(files))),
        "channels": [
            {"id": "verified", "label": "Verified declarations", "unit": "declarations",
             "values": [per[f]["VERIFIED"] for f in files]},
            {"id": "failed_at_head", "label": "Failing at head", "unit": "declarations",
             "values": [per[f]["FAILED-AT-HEAD"] for f in files]},
            {"id": "unverified", "label": "Unverified", "unit": "declarations",
             "values": [per[f]["UNVERIFIED"] for f in files]},
        ],
        "observed": dict(tally),
        "caveat": ("A run verifies the whole file it built, not a theorem in "
                   "isolation. The eleven failing rows are repaired on the lane "
                   "branch but not yet carried to the branches holding them."),
        "source": {"repo": "operator-first", "commit": commit(),
                   "path": "ledger/LEAN_CERTIFICATE_LEDGER_2026-09-13.jsonl"},
    }


def frontiermath():
    rows = jsonl("research/frontiermath/frontiermath_3rank9_python_lane.jsonl")
    if not rows:
        return None
    return {
        "lane": "frontiermath",
        "run_id": "python-lane-controls-v1",
        "title": "FrontierMath ell=3 r=9 Python lane controls",
        "claim": (f"Across {len(rows)} field/lane evaluations the highest 3-rank is "
                  f"{max(r['three_rank'] for r in rows)}; no input reaches the rank-9 gate."),
        "evidence": "computation",
        "status": "verified",
        "reproduce": "python3 research/frontiermath/run_controls_v1.py",
        "object_id": "quadratic_class_groups",
        "model_id": "frontiermath_3rank9_python_lane_v1",
        "coordinate": "evaluation index",
        "x_unit": "row ordinal",
        "x": list(range(len(rows))),
        "channels": [
            {"id": "three_rank", "label": "3-rank of the class group", "unit": "3-rank",
             "values": [r["three_rank"] for r in rows]},
        ],
        "observed": {
            "rows": len(rows),
            "max_three_rank": max(r["three_rank"] for r in rows),
            "target_three_rank": 9,
            "certificate_written": False,
        },
        "caveat": ("The two Elkies 3-ranks are carried from the supplied ledger, not "
                   "recomputed: their discriminants are near 1e29 and need PARI, Sage "
                   "or Magma. Only the C0 and C1 controls were recomputed exactly here."),
        "source": {"repo": "operator-first", "commit": commit(),
                   "path": "research/frontiermath/frontiermath_3rank9_python_lane.jsonl"},
    }


def claim_only_runs():
    """Work that produced no numeric channels on a common coordinate."""
    c = commit()
    return [
        {
            "lane": "lean", "run_id": "hunt-2026-09-13-root-causes",
            "claim": ("Two proof-script defects, an induction that did not generalize "
                      "and a rewrite aimed at the wrong summation, accounted for the "
                      "bulk of the failing Lean declarations."),
            "evidence": "computation", "status": "verified",
            "reproduce": "see ledger/LEAN_HUNT_2026-09-13.md for the run ids",
            "caveat": "Neither defect was a false statement; both theorems are true as written.",
            "source": {"repo": "operator-first", "commit": c,
                       "path": "ledger/LEAN_HUNT_2026-09-13.md"},
        },
        {
            "lane": "lean", "run_id": "warmup-never-compiled",
            "claim": ("Warmup.lean did not parse: the postfix transpose is scoped to "
                      "the Matrix namespace and the file never opened it."),
            "evidence": "computation", "status": "verified",
            "reproduce": "lake env lean Warmup.lean",
            "caveat": ("Hidden because no workflow on any branch compiled the file. "
                       "The same four results in OperatorFirst.lean were green throughout."),
            "depends_on": ["lean/certificate-ledger-2026-09-13"],
            "source": {"repo": "operator-first", "commit": c, "path": "Warmup.lean"},
        },
        {
            "lane": "frontiermath", "run_id": "rank16-witness-absent",
            "claim": ("The sixteen form triples of the Elkies rank-16 boundary and "
                      "their eight-vector relation basis are absent from the ledger."),
            "evidence": "none", "status": "blocked",
            "caveat": ("Blocked on recovering the exact forms from the original Elkies "
                       "computation. The witness must not be reconstructed as a substitute."),
            "source": {"repo": "operator-first", "commit": c,
                       "path": "research/frontiermath/README_PYTHON_LANE_v1.md"},
        },
        {
            "lane": "frontiermath", "run_id": "class-group-engine-out-of-reach",
            "claim": ("Exact reduced-form enumeration is linear in |D| and cannot reach "
                      "the Elkies discriminants near 1e29."),
            "evidence": "computation", "status": "blocked",
            "reproduce": "python3 -m unittest discover -s research/frontiermath",
            "caveat": "Blocked on a subexponential class-group algorithm: PARI, Sage or Magma.",
            "source": {"repo": "operator-first", "commit": c,
                       "path": "research/frontiermath/bqf_class_group_v1.py"},
        },
    ]


def main():
    runs = [r for r in (acc_postrun(), lean_ledger(), frontiermath()) if r]
    runs += claim_only_runs()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(runs, indent=1))
    print(f"{len(runs)} runs -> {OUT.relative_to(ROOT)}")
    for r in runs:
        n = len(r.get("channels") or [])
        print(f"  {r['lane']}/{r['run_id']:<34} {r['status']:<9} "
              f"{'%d channels' % n if n else 'claim only'}")
    if "--record" in sys.argv:
        subprocess.run(["node", "tools/acc/mixer_log_v1.js", "record", str(OUT)],
                       cwd=ROOT, check=True)


if __name__ == "__main__":
    main()
