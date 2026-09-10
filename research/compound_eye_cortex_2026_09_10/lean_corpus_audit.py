#!/usr/bin/env python3
from __future__ import annotations
import collections, json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "lean_corpus_ledger.json"

DECL_RE = re.compile(r"^\s*(?:(?:private|protected|noncomputable)\s+)*(theorem|lemma|def|abbrev|structure|inductive|class)\s+([A-Za-z_][A-Za-z0-9_'.]*)\b")
EXAMPLE_RE = re.compile(r"^\s*example\b")
EXCLUDE_PARTS = {"evidence", ".lake", "build", "backups", "preserved"}

def sh(*args: str) -> str:
    return subprocess.check_output(args, cwd=ROOT.parents[1], text=True, stderr=subprocess.DEVNULL)

def lean_files(ref: str) -> list[str]:
    names = sh("git", "ls-tree", "-r", "--name-only", ref).splitlines()
    return [p for p in names if p.endswith(".lean") and not any(part in EXCLUDE_PARTS for part in pathlib.PurePosixPath(p).parts)]

def text_at(ref: str, path: str) -> str | None:
    try:
        return sh("git", "show", f"{ref}:{path}")
    except subprocess.CalledProcessError:
        return None

def parse_named(ref: str) -> dict[tuple[str,str,str], dict]:
    out = {}
    for path in lean_files(ref):
        text = text_at(ref, path)
        if text is None:
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            m = DECL_RE.match(line)
            if m:
                kind, name = m.groups()
                out[(path, kind, name)] = {"path": path, "kind": kind, "name": name, "line": lineno}
    return out

def count_examples(ref: str, paths: set[str] | None = None) -> int:
    total = 0
    for path in lean_files(ref):
        if paths is not None and path not in paths:
            continue
        text = text_at(ref, path)
        if text:
            total += sum(bool(EXAMPLE_RE.match(line)) for line in text.splitlines())
    return total

def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: lean_corpus_audit.py PR_REFS_TSV")
    rows = []
    for raw in pathlib.Path(sys.argv[1]).read_text().splitlines():
        if not raw.strip():
            continue
        pr, base, head, title = raw.split("\t", 3)
        rows.append((int(pr), base, head, title))

    union_new = {}
    per_pr = []
    all_source_paths = set()
    for pr, base, head, title in rows:
        b = parse_named(base)
        h = parse_named(head)
        new_keys = set(h) - set(b)
        new = [h[k] for k in sorted(new_keys)]
        kinds = collections.Counter(x["kind"] for x in new)
        changed_source_paths = {x["path"] for x in new}
        all_source_paths |= changed_source_paths
        # Anonymous examples are reported only as context, not included in named-proof totals.
        examples = count_examples(head, changed_source_paths)
        per_pr.append({
            "pr": pr, "title": title, "base": base, "head": head,
            "new_named_declarations": len(new), "new_by_kind": dict(sorted(kinds.items())),
            "examples_in_files_with_new_named_declarations": examples,
            "new_declarations": new,
        })
        for k in new_keys:
            union_new[k] = h[k]

    union_counts = collections.Counter(x["kind"] for x in union_new.values())
    proof_kinds = {"theorem", "lemma"}
    named_proofs = sum(v for k, v in union_counts.items() if k in proof_kinds)
    report = {
        "method": "For each Lean-verified PR, compare named declarations at its head against its current base commit; union by (path, kind, name). Evidence/.lake/build/backups/preserved are excluded. Anonymous examples are not counted as reusable named proofs.",
        "verified_prs": [r[0] for r in rows],
        "unique_new_named_declarations": len(union_new),
        "unique_new_named_proofs_theorem_plus_lemma": named_proofs,
        "unique_new_by_kind": dict(sorted(union_counts.items())),
        "source_paths_with_new_declarations": sorted(all_source_paths),
        "per_pr": per_pr,
    }
    OUT.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ["verified_prs","unique_new_named_declarations","unique_new_named_proofs_theorem_plus_lemma","unique_new_by_kind"]}, indent=2))

if __name__ == "__main__":
    main()
