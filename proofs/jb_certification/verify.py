#!/usr/bin/env python3
"""Compile, axiom-audit, leancheck, and run false controls for JBCertCore and JBCertMatrix."""
import hashlib, json, pathlib, re, shutil, subprocess
ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "evidence"
OUT.mkdir(exist_ok=True)
MODULES = ["JBCertCore", "JBCertMatrix"]
report = {"status": "RUNNING", "commands": [], "modules": {}}

def run(name, args, negative=False):
    p = subprocess.run(args, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=1500)
    (OUT / f"{name}.log").write_text(p.stdout)
    print(p.stdout, flush=True)
    report["commands"].append({"name": name, "args": args, "returncode": p.returncode})
    if negative:
        if p.returncode == 0 or not re.search(r"proved that the proposition.*false|unsolved goals|no goals to be solved|failed", p.stdout, re.S):
            raise RuntimeError("False control did not fail mathematically: " + name)
        if re.search(r"unknown (?:module|identifier|constant)|unexpected token", p.stdout):
            raise RuntimeError("False control failed for infrastructure reason: " + name)
    elif p.returncode:
        raise RuntimeError(name + " failed")
    return p.stdout

try:
    for filename in ["lake-manifest.json", "lean-toolchain"]:
        if (ROOT / filename).exists():
            shutil.copyfile(ROOT / filename, OUT / filename)
    run("toolchain", ["lake", "env", "lean", "--version"])
    for mod in MODULES:
        src = ROOT / f"{mod}.lean"
        names = ["JBCert." + x for x in re.findall(r"^theorem\s+(\w+)", src.read_text(), re.M)]
        report["modules"][mod] = {"sha256": hashlib.sha256(src.read_bytes()).hexdigest(), "theorems": names}
        run(f"build_{mod}", ["lake", "build", mod])
        audit = OUT / f"axioms_{mod}.lean"
        audit.write_text(f"import {mod}\n" + "\n".join("#print axioms " + n for n in names) + "\n")
        log = run(f"axioms_{mod}", ["lake", "env", "lean", str(audit)])
        for name in names:
            m = re.search(re.escape("'" + name + "'") + r"\s+(does not depend on any axioms|depends on axioms:\s*\[([^\]]*)\])", log, re.S)
            if not m:
                raise RuntimeError("Missing axiom audit: " + name)
            if m.group(2) and set(x.strip() for x in m.group(2).split(",")) - {"propext", "Classical.choice", "Quot.sound"}:
                raise RuntimeError("Forbidden axiom: " + name)
        run(f"leanchecker_{mod}", ["lake", "env", "leanchecker", mod])
    false_controls = {
        # pairing is NOT conserved without the inverse relation: a concrete counterexample must not be provable as an identity
        "false_pairing_no_inverse": "import JBCertCore\nexample : ((2:ℤ) * 3) * (3 * 5) = 2 * 5 := by norm_num",
        "false_coboundary_no_endpoint": "import JBCertCore\nexample : (2:ℚ) * 3 * (1/3) = 3 := by norm_num",
        "false_kronecker_not_idempotent": "import JBCertMatrix\nexample : (2:ℕ) * 2 = 2 := by norm_num",
        "false_inverse_order": "import JBCertMatrix\nexample : ((1:ℚ)/2) * 3 * 2 = 1 := by norm_num",
    }
    for name, text in false_controls.items():
        f = OUT / f"{name}.lean"
        f.write_text(text + "\n")
        run(name, ["lake", "env", "lean", str(f)], negative=True)
    report["status"] = "PASS"
except Exception as e:
    report["status"] = "FAIL"
    report["error"] = str(e)
finally:
    report["named_theorems"] = sum(len(v["theorems"]) for v in report["modules"].values())
    (OUT / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2), flush=True)
