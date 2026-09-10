#!/usr/bin/env python3
from __future__ import annotations
import collections, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parents[1]
OUT = ROOT / "lean_corpus_ledger.json"

# Only source files explicitly compiled/audited by the successful proof verifier for
# each bundle. This intentionally excludes copied sources, false controls, candidate
# files and Lean files merely present on the branch.
CERTIFIED = {
  1: ["OperatorFirst.lean"],
  2: ["OperatorFirst/Offset.lean", "OperatorFirst/OffsetFock.lean"],
  3: ["MixedIntake/FCS_original.lean", "MixedIntake/AK_original.lean", "MixedIntake/Review.lean"],
  4: [
    "OperatorFirst/RestrictionBridge.lean", "OperatorFirst/KakeyaExtension.lean",
    "OperatorFirst/EarthMoon.lean", "OperatorFirst/FCSMoments.lean",
    "OperatorFirst/KakeyaSeedingControl.lean", "OperatorFirst/KakeyaCut.lean",
    "OperatorFirst/KakeyaForcingLinear.lean", "OperatorFirst/KakeyaAtlasFamily.lean",
    "OperatorFirst/KakeyaAtlasProjector.lean"],
  5: ["OperatorFirst/OffsetEndpoint.lean"],
  6: [
    "OperatorFirst/EndpointProgress.lean", "OperatorFirst/EndpointTransfer.lean",
    "OperatorFirst/FiniteCovariance.lean", "OperatorFirst/BandObstruction.lean",
    "OperatorFirst/LaurentBoundary.lean"],
  7: [
    "LightBridges/Algebra.lean", "LightBridges/Gram.lean", "LightBridges/Census.lean",
    "LightBridges/Coherence.lean", "LightBridges/Boundary.lean", "LightBridges/Ledger.lean",
    "LightBridges/ScalarOptics.lean", "LightBridges/Examples.lean", "OpticalMetric.lean",
    "Rigidity.lean", "LightCompletion.lean"],
  8: ["Gravity.lean"],
  9: ["GravityOverlap.lean"],
  11: ["proofs/peel_constitutive/OpticalMetric.lean"],
  13: ["research/diophantine/formal/Certificates.lean"],
  17: ["research/elemental_foundations/formal/ElementalFoundations.lean"],
  18: [
    "research/yang_mills_2026_09_09/lean/GaugeCertificates.lean",
    "research/yang_mills_2026_09_09/cross_theorem/lean/CrossTheorem.lean"],
  20: ["research/compound_eye_cortex_2026_09_10/formal_transport_memory/TransportMemory.lean"],
}

# Expected named theorem declarations from the actual successful verifier reports.
EXPECTED_THEOREMS = {
  1:14, 2:53, 3:39, 4:95, 5:30, 6:56, 7:91,
  8:23, 9:7, 11:16, 13:7, 17:16, 18:33, 20:15,
}

DECL_RE = re.compile(r"^\s*(?:(?:private|protected|noncomputable)\s+)*(theorem|lemma|def|abbrev|structure|inductive|class)\s+([^\s(:{]+)")
EXAMPLE_RE = re.compile(r"^\s*example\b")
SCOPE_RE = re.compile(r"^\s*(namespace|section)\s*([^\s]*)")
END_RE = re.compile(r"^\s*end(?:\s+([^\s]+))?\s*$")

def sh(*args: str) -> str:
    return subprocess.check_output(args, cwd=REPO, text=True, stderr=subprocess.DEVNULL)

def text_at(ref: str, path: str) -> str:
    return sh("git", "show", f"{ref}:{path}")

def parse_source(ref: str, path: str) -> tuple[list[dict], int]:
    text = text_at(ref, path)
    scopes: list[tuple[str,str]] = []
    decls: list[dict] = []
    examples = 0
    for lineno, line in enumerate(text.splitlines(), 1):
        if EXAMPLE_RE.match(line):
            examples += 1
        sm = SCOPE_RE.match(line)
        if sm:
            kind, name = sm.groups()
            scopes.append((kind, name))
            continue
        if END_RE.match(line):
            if scopes:
                scopes.pop()
            continue
        m = DECL_RE.match(line)
        if not m:
            continue
        kind, name = m.groups()
        namespaces = [n for k,n in scopes if k == "namespace" and n]
        qualified = ".".join(namespaces + [name]) if namespaces else name
        decls.append({"path":path,"kind":kind,"name":name,"qualified":qualified,"line":lineno})
    return decls, examples

def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: lean_corpus_audit.py PR_REFS_TSV")
    rows = {}
    for raw in pathlib.Path(sys.argv[1]).read_text().splitlines():
        if not raw.strip(): continue
        pr, base, head, title = raw.split("\t", 3)
        rows[int(pr)] = {"base":base,"head":head,"title":title.strip()}

    missing = sorted(set(CERTIFIED)-set(rows))
    if missing:
        raise RuntimeError(f"missing PR refs: {missing}")

    theorem_instances = []
    lemma_instances = []
    support_instances = []
    example_instances = 0
    per_bundle = []
    for pr in CERTIFIED:
        row = rows[pr]
        all_decls = []
        examples = 0
        for path in CERTIFIED[pr]:
            ds, ex = parse_source(row["head"], path)
            all_decls.extend(ds); examples += ex
        by_kind = collections.Counter(d["kind"] for d in all_decls)
        theorem_count = by_kind.get("theorem",0)
        if theorem_count != EXPECTED_THEOREMS[pr]:
            raise RuntimeError(f"PR #{pr}: parsed {theorem_count} theorems, expected {EXPECTED_THEOREMS[pr]}")
        theorem_instances += [d for d in all_decls if d["kind"] == "theorem"]
        lemma_instances += [d for d in all_decls if d["kind"] == "lemma"]
        support_instances += [d for d in all_decls if d["kind"] not in {"theorem","lemma"}]
        example_instances += examples
        per_bundle.append({
            "pr":pr,"title":row["title"],"head":row["head"],"certified_sources":CERTIFIED[pr],
            "named_by_kind":dict(sorted(by_kind.items())),"anonymous_examples_in_certified_sources":examples,
        })

    # A fully-qualified theorem name is the durable logical identity used for corpus
    # de-duplication. This removes re-certifications such as the 12 LightConstitutive
    # statements later rechecked in the peel-constitutive bundle.
    unique_theorems = {}
    repeats = collections.defaultdict(list)
    for d, bundle in ((d,b) for b in per_bundle for d in []):
        pass
    for b in per_bundle:
        pr=b["pr"]
        for path in b["certified_sources"]:
            ds,_=parse_source(b["head"],path)
            for d in ds:
                if d["kind"] != "theorem": continue
                repeats[d["qualified"]].append({"pr":pr,"path":path,"line":d["line"]})
                unique_theorems.setdefault(d["qualified"], {"qualified":d["qualified"],"first_pr":pr,"path":path,"line":d["line"]})
    repeated_names = {k:v for k,v in repeats.items() if len(v)>1}

    support_by_kind = collections.Counter(d["kind"] for d in support_instances)
    report = {
      "status":"PASS",
      "method":"Counts only source files explicitly covered by successful verifier inventories. 'Certified theorem instances' counts re-certification in separate bundles; 'unique theorem names' de-duplicates identical fully-qualified Lean theorem names. Anonymous examples and false controls are not theorem counts.",
      "verified_prs":list(CERTIFIED),
      "certified_theorem_instances":len(theorem_instances),
      "unique_fully_qualified_theorem_names":len(unique_theorems),
      "certified_named_lemma_instances":len(lemma_instances),
      "support_declaration_instances_by_kind":dict(sorted(support_by_kind.items())),
      "anonymous_examples_in_certified_sources":example_instances,
      "repeated_certified_theorem_names":repeated_names,
      "per_bundle":per_bundle,
      "unique_theorems":sorted(unique_theorems.values(), key=lambda x:x["qualified"]),
    }
    OUT.write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps({k:report[k] for k in ["status","certified_theorem_instances","unique_fully_qualified_theorem_names","certified_named_lemma_instances","support_declaration_instances_by_kind","anonymous_examples_in_certified_sources"]},indent=2))

if __name__ == "__main__": main()
