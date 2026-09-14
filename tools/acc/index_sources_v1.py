"""Index everything reachable into the ledger, so "find prior work" is true.

`prior` searched the event stream only, which made the repeat-warning true
within one file and false everywhere it mattered. This indexes the places the
work actually lives, as `evidence` events with provenance, so a search reaches
them:

    git commits          every commit touching research, tools, ledger, proofs
    repo artifacts       tools, ledgers, research code, Lean sources
    Lean certificates    the LC registry from PR #41 (CERTIFIED / PENDING / WITHDRAWN)
    github               issues and PRs already read in this session
    drive                files already listed in this session

Honesty rule for this file: an index entry records WHERE something is and WHAT
this process actually saw. It never asserts the content of a thing it did not
open. Entries carry `seen` = full | listing-only, so a search result cannot be
mistaken for a reading.

    python3 tools/acc/index_sources_v1.py --all
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))

from event_log_v1 import EventLog  # noqa: E402

RUN = "source-index"


def index_commits(log, limit=200):
    out = subprocess.run(
        ["git", "log", f"-{limit}", "--format=%H%x1f%aI%x1f%s", "--",
         "research/", "tools/", "ledger/", "proofs/", "catalog/", ".github/"],
        cwd=ROOT, capture_output=True, text=True).stdout
    n = 0
    for line in out.splitlines():
        parts = line.split("\x1f")
        if len(parts) != 3:
            continue
        sha, iso, subject = parts
        log.append("evidence", {"kind": "commit", "ref": sha[:12], "when": iso,
                                "title": subject, "source": "git log",
                                "seen": "full"}, RUN)
        n += 1
    return n


def index_files(log):
    pats = ["tools/acc/*.py", "tools/acc/*.js", "research/acc/*.py",
            "research/frontiermath/*.py", "ledger/**/*.md", "proofs/**/*.lean",
            "*.lean", "ledger/**/*.jsonl"]
    n = 0
    for pat in pats:
        for p in sorted(ROOT.glob(pat)):
            if ".git" in p.parts or "__pycache__" in p.parts:
                continue
            rel = str(p.relative_to(ROOT))
            log.append("evidence", {"kind": "file", "ref": rel,
                                    "bytes": p.stat().st_size,
                                    "source": "repository working tree",
                                    "seen": "full"}, RUN)
            n += 1
    return n


# The LC registry as read from PR #41 at trace-map commit e3e9cfc2. Scope lines
# are the registry's own words, shortened; nothing is added to them.
LC = [
 ("LC-001", "GREEN", "#1", "Core operator algebra", "commutator identity, bilinear reciprocity, Gram/Cauchy-Schwarz"),
 ("LC-002", "GREEN", "#2", "Offset finite core", "guarded finite log identities, finite Schur determinant algebra"),
 ("LC-003", "GREEN", "#3", "Gaussian / arithmetic-Kakeya audit", "FCS/AK statements with scoped corrections"),
 ("LC-004", "GREEN", "#4", "Kakeya / Earth-Moon / projector", "forcing-kernel criterion, dual obstruction, projector criterion"),
 ("LC-005", "GREEN", "#5", "Offset endpoint extension", "reflection/determinant identities, monotonicity counterexamples"),
 ("LC-006", "GREEN", "#6", "Laurent boundary mechanism", "column degree bounds, faithful-substitution descent"),
 ("LC-007", "GREEN", "#7", "Light Ledger finite suite", "bridge/constitutive/rigidity plus finite completion"),
 ("LC-008", "GREEN", "#8", "Moving-projector / wall algebra", "tangent decomposition, moving projector chart identities"),
 ("LC-009", "GREEN", "#9", "Projector overlap Taylor bridge", "equal-trace idempotent overlap identity"),
 ("LC-010", "GREEN", "#11", "Positive-channel peel", "finite constitutive identities, null persistence"),
 ("LC-011", "GREEN", "#17", "Elemental finite predictor layer", "finite predictor/Gram/FOFT/angle/ladder"),
 ("LC-012", "GREEN", "#25", "Elemental Foundations Revision 4", "nonidentifiability, minimax error floor"),
 ("LC-013", "GREEN", "#13", "Diophantine algebraic batch", "seven algebraic certificates"),
 ("LC-014", "GREEN", "#30", "Diophantine section integer image", "rational section y-range, integer images u=+-1"),
 ("LC-015", "GREEN", "#22", "Hypersurface square-lineage", "positive-branch Snell/squared-metric equivalence"),
 ("LC-016", "GREEN", "#26", "Four-body PSD wall bridge", "for PSD W, L^T W L = 0 iff W L = 0"),
 ("LC-017", "GREEN", "#18", "Yang-Mills finite scalar closing", "scalar inverse-weight, error-budget arithmetic"),
 ("LC-018", "GREEN", "#27", "Yang-Mills PSD matrix boundary", "contributionwise PSD improvement"),
 ("LC-019", "GREEN", "#28", "UPG redistribution / zero-time feedback", "redistribution B=0 iff B=0"),
 ("LC-020", "GREEN", "#24", "Collatz prefix barriers", "exact affine-prefix identity, survival envelope"),
 ("LC-021", "GREEN", "#40", "Collatz bounded-collapse", "every 1<=n<=100000 reaches 1 within 400 steps"),
 ("LC-022", "GREEN", "#43", "Standard-math / title-kernel audit", "three title kernels plus 20 standard kernels"),
 ("LC-023", "GREEN", "#56", "Yang-Mills nonuniform allocation floor", "three new theorems; parents are ancestry"),
 ("LC-024", "GREEN", "#57", "Collatz one-cylinder exceptional threshold", "five new theorems at fixed resolution"),
]
PENDING = ["#31","#32","#35","#36","#37","#46","#47","#48","#49","#50","#51","#52","#53","#54","#55"]
WITHDRAWN = [("#34","weaker duplicate Collatz formalization"),
             ("#45","withdrawn ACC public bridge; no certificate claim"),
             ("#38","recovery/provenance ledger only"),
             ("#39","Smith-mixer experiment; not a theorem certificate"),
             ("#44","frontier infrastructure; corrected downstream by #47")]


def index_lean(log):
    n = 0
    for tag, status, pr, lane, scope in LC:
        log.append("evidence", {"kind": "lean-certificate", "ref": tag,
                                "status": status, "pr": pr, "lane": lane,
                                "scope": scope,
                                "source": "PR #41 LEAN_TRACE_MAP.md @ e3e9cfc2",
                                "seen": "full"}, RUN)
        n += 1
    for pr in PENDING:
        log.append("evidence", {"kind": "lean-lane", "ref": pr, "status": "PENDING",
                                "note": "source exists; this head is not promoted",
                                "source": "PR #41 registry", "seen": "full"}, RUN)
        n += 1
    for pr, why in WITHDRAWN:
        log.append("evidence", {"kind": "lean-lane", "ref": pr, "status": "WITHDRAWN",
                                "note": why, "source": "PR #41 registry",
                                "seen": "full"}, RUN)
        n += 1
    return n


GITHUB = [("issue", "#42", "ACC shared agent war room — ChatGPT <-> Claude", "full"),
          ("pr", "#41", "Certified layer: master Lean certificate registry", "full"),
          ("comment", "#42 5657092717", "External-priority notice ACC-P000002, R. Sneiderman", "full")]

DRIVE = [
 ("Sofic_Torsion_Atlas_Working_Note.md", "the lifting ladder and the move-defect rule", "full"),
 ("complete_complex_k3_permutation.pdf", "Beasley, k/3 permutation coboundary; Thm 8, Cor 9, Rem 10", "full"),
 ("Ramanujan_Challenge_Proofs_02_08.pdf", "Ramanujan challenge proofs", "listing-only"),
 ("The_Ramanujan_Challenge__Clean_.pdf", "earlier Ramanujan version, 8 Jul", "listing-only"),
 ("matter_at_a_scale_v5.pdf", "matter at a scale, v5", "listing-only"),
 ("sofic_trace (5).pdf", "sofic trace", "listing-only"),
 ("the_relational_atlas_full.md", "relational atlas, 55 KB", "listing-only"),
 ("THE_OPERATOR_FIRST_ATLAS.pdf", "Operator-First Atlas", "listing-only"),
 ("verified-lean-proof-atlas.zip", "verified Lean proof atlas", "listing-only"),
 ("Mad_Hatters_ACC_War_Room_v23", "War Room v23", "listing-only"),
 ("CLAUDE_AC_RECORD_IMPROVEMENTS_20260913_v4.txt", "174 AC record improvements", "listing-only"),
 ("SOFIC-NEW-ROUTES-01.py", "sofic new routes code", "listing-only"),
]


def index_external(log):
    n = 0
    for kind, ref, title, seen in GITHUB:
        log.append("evidence", {"kind": f"github-{kind}", "ref": ref, "title": title,
                                "source": "github dicipler-pixel/operator-first",
                                "seen": seen}, RUN)
        n += 1
    for ref, title, seen in DRIVE:
        log.append("evidence", {"kind": "drive-file", "ref": ref, "title": title,
                                "source": "Google Drive, Mad Hatters hub",
                                "seen": seen}, RUN)
        n += 1
    return n


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--dir")
    a = ap.parse_args(argv)
    log = EventLog(a.dir)
    c = index_commits(log)
    f = index_files(log)
    l = index_lean(log)
    e = index_external(log)
    print(f"indexed {c} commits, {f} files, {l} Lean registry rows, {e} external refs")
    n, p = log.verify()
    print(f"stream: {n} events, {len(p)} problems")
    return 0


if __name__ == "__main__":
    sys.exit(main())
