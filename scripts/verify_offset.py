#!/usr/bin/env python3
"""Run actual Lean checks; never substitute source scans for compilation."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from source_revision import source_revision
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "verification" / "offset"
OUT.mkdir(parents=True, exist_ok=True)
ALLOWED = {"propext", "Classical.choice", "Quot.sound"}
report: dict = {"status": "RUNNING", "checks": {}, "allowlist": sorted(ALLOWED)}

def run(name: str, argv: list[str], expected_failure: bool = False) -> str:
    proc = subprocess.run(argv, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, timeout=240)
    text = proc.stdout
    (OUT / (name + ".log")).write_text(text, encoding="utf-8")
    print(f"=== {name}: exit={proc.returncode} ===\n{text}", flush=True)
    report["checks"][name] = {"argv": argv, "exit_code": proc.returncode,
                              "expected_failure": expected_failure}
    if not expected_failure and proc.returncode != 0:
        raise RuntimeError(name + " failed")
    if expected_failure:
        if proc.returncode == 0:
            raise RuntimeError(name + ": false control was accepted")
        if re.search(r"unknown (?:module|identifier|constant)|unexpected token|invalid field|not found", text, re.I):
            raise RuntimeError(name + ": infrastructure/syntax failure is not a mathematical rejection")
        if not re.search(r"unsolved goals|proved that the proposition.*false|tactic.*failed", text, re.I | re.S):
            raise RuntimeError(name + ": no recognized mathematical rejection")
    return text

try:
    report["git_commit"] = source_revision(ROOT)
    report["toolchain"] = (ROOT / "lean-toolchain").read_text().strip()
    modules = [ROOT / "OperatorFirst" / "Offset.lean"]
    fock = ROOT / "OperatorFirst" / "OffsetFock.lean"
    if fock.exists():
        modules.append(fock)
    report["sources"] = {}
    total = 0
    for source in modules:
        data = source.read_bytes()
        text = data.decode("utf-8")
        names = re.findall(r"^theorem\s+([\w]+)", text, re.M)
        total += len(names)
        report["sources"][str(source.relative_to(ROOT))] = {
            "sha256": hashlib.sha256(data).hexdigest(), "theorems": names}
        log = run(source.stem + "_elaboration", ["lake", "env", "lean", str(source.relative_to(ROOT))])
        if re.search(r"declaration uses 'sorry'|depends on axioms:.*sorryAx", log):
            raise RuntimeError("unfinished proof in " + source.name)
        found = re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]", log)
        no_axioms = re.findall(r"'([^']+)' does not depend on any axioms", log)
        fullnames = {n for n, _ in found} | set(no_axioms)
        for short in names:
            if not any(n.endswith("." + short) for n in fullnames):
                raise RuntimeError("missing explicit axiom report: " + short)
        for name, axioms in found:
            used = {a.strip() for a in axioms.split(",") if a.strip()}
            if used - ALLOWED:
                raise RuntimeError("unapproved dependencies in " + name + ": " + str(used))
        module = ".".join(source.relative_to(ROOT).with_suffix("").parts)
        run(source.stem + "_kernel_recheck", ["lake", "env", "leanchecker", module])
    report["named_theorems"] = total
    negatives = {
      "false_arithmetic": "import Mathlib\nexample : (1 : Nat) = 2 := by decide\n",
      "false_shear_sector": "import OperatorFirst.Offset\nopen Matrix OperatorFirst.Offset\nexample : (shear (1/3)).mulVec ![1, 1] = (2/3 : Real) • ![1, 1] := by\n  ext i\n  fin_cases i <;> norm_num [shear, Matrix.mulVec, dotProduct, Fin.sum_univ_two]\n",
      "false_linear_response": "import Mathlib\nexample : (1 : Real)*1 + 1*(-1) ≠ 0 := by norm_num\n"
    }
    for name, text in negatives.items():
        path = OUT / (name + ".lean")
        path.write_text(text, encoding="utf-8")
        run(name, ["lake", "env", "lean", str(path.relative_to(ROOT))], True)
    report["status"] = "PASS"
except Exception as exc:
    report["status"] = "FAIL"
    report["error"] = str(exc)
finally:
    (OUT / "verification_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2), flush=True)
sys.exit(0 if report["status"] == "PASS" else 1)

