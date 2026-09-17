#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import pathlib
import subprocess
import sys
from urllib.parse import quote

import lean_corpus_audit as audit

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parents[1]
OUTDIR = ROOT / "lean_proof_atlas"
HTML_OUT = OUTDIR / "lean_proof_atlas.html"
MANIFEST_OUT = OUTDIR / "SOURCE_MANIFEST.json"


def sh(*args: str) -> str:
    return subprocess.check_output(args, cwd=REPO, text=True)


def text_at(ref: str, path: str) -> str:
    return sh("git", "show", f"{ref}:{path}")


def read_refs(path: pathlib.Path) -> dict[int, dict]:
    rows: dict[int, dict] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if not raw.strip():
            continue
        pr, base, head, title = raw.split("\t", 3)
        rows[int(pr)] = {"base": base, "head": head, "title": title.strip()}
    missing = sorted(set(audit.CERTIFIED) - set(rows))
    if missing:
        raise RuntimeError(f"missing PR refs: {missing}")
    return rows


def gh_source_url(head: str, path: str) -> str:
    return "https://github.com/dicipler-pixel/operator-first/blob/" + head + "/" + quote(path, safe="/")


def esc(s: object) -> str:
    return html.escape(str(s), quote=True)


def project_hint(pr: int, title: str, paths: list[str]) -> str:
    joined = (title + " " + " ".join(paths)).lower()
    if "yang" in joined:
        return "Yang–Mills"
    if "elemental" in joined:
        return "Elemental / hypersurface"
    if "gravity" in joined:
        return "Gravity / overlap"
    if "light" in joined or "optical" in joined or "endpoint" in joined:
        return "Light / endpoint"
    if "kakeya" in joined or "earthmoon" in joined or "fcs" in joined or "mixed" in joined:
        return "Kakeya / Earth–Moon / mixed"
    if "diophantine" in joined:
        return "Diophantine"
    if "transport" in joined or "memory" in joined:
        return "Transport / memory"
    if "offset" in joined:
        return "Offset / boundary"
    return "Operator-first core"


def source_card(pr: int, row: dict, path: str, text: str) -> tuple[str, dict]:
    decls, examples = audit.parse_source(row["head"], path)
    kinds: dict[str, int] = {}
    for d in decls:
        kinds[d["kind"]] = kinds.get(d["kind"], 0) + 1
    theorem_names = [d["qualified"] for d in decls if d["kind"] == "theorem"]
    source_rel = pathlib.Path("sources") / f"pr{pr:02d}" / path
    source_path = OUTDIR / source_rel
    source_path.parent.mkdir(parents=True, exist_ok=True)
    source_path.write_text(text, encoding="utf-8")
    search_blob = " ".join([str(pr), row["title"], path, " ".join(theorem_names), text[:12000]])
    card = f"""
    <details class="source-card" data-search="{esc(search_blob.lower())}">
      <summary>
        <span class="pill formal">LEAN SOURCE</span>
        <strong>PR #{pr} · {esc(path)}</strong>
        <span class="meta">{kinds.get('theorem',0)} theorems · {kinds.get('lemma',0)} lemmas · {examples} examples</span>
      </summary>
      <div class="source-meta">
        <div><b>PR:</b> #{pr} — {esc(row['title'])}</div>
        <div><b>Exact head:</b> <code>{esc(row['head'])}</code></div>
        <div><b>Source snapshot:</b> <code>{esc(source_rel.as_posix())}</code></div>
        <div><a href="{esc(gh_source_url(row['head'], path))}">Open exact source on GitHub</a></div>
      </div>
      <div class="theorem-list"><b>Theorems in this source:</b> {esc(', '.join(theorem_names) if theorem_names else 'none')}</div>
      <pre><code>{esc(text)}</code></pre>
    </details>
    """
    manifest = {
        "pr": pr,
        "title": row["title"],
        "head": row["head"],
        "path": path,
        "snapshot_path": source_rel.as_posix(),
        "theorem_count": kinds.get("theorem", 0),
        "lemma_count": kinds.get("lemma", 0),
        "anonymous_examples": examples,
        "theorems": theorem_names,
        "github_url": gh_source_url(row["head"], path),
    }
    return card, manifest


def build(refs_tsv: pathlib.Path) -> None:
    rows = read_refs(refs_tsv)
    ledger_path = ROOT / "lean_corpus_ledger.json"
    if not ledger_path.exists():
        raise RuntimeError("lean_corpus_ledger.json must be generated first")
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    OUTDIR.mkdir(parents=True, exist_ok=True)

    bundles_html: list[str] = []
    cards: list[str] = []
    manifest_rows: list[dict] = []
    for pr, paths in audit.CERTIFIED.items():
        row = rows[pr]
        project = project_hint(pr, row["title"], paths)
        theorem_count = audit.EXPECTED_THEOREMS[pr]
        bundles_html.append(
            f"<tr><td>#{pr}</td><td>{esc(project)}</td><td>{esc(row['title'])}</td>"
            f"<td class='num'>{theorem_count}</td><td><code>{esc(row['head'][:12])}</code></td></tr>"
        )
        for path in paths:
            text = text_at(row["head"], path)
            card, item = source_card(pr, row, path, text)
            item["project"] = project
            cards.append(card)
            manifest_rows.append(item)

    manifest = {
        "schema": "operator-first-lean-proof-atlas-v1",
        "scope": "Exact source snapshots listed in the certified Lean proof inventory. Inclusion certifies source lineage to a successful proof-verifier bundle; it does not upgrade broader scientific interpretations into formal theorems.",
        "verified_prs": list(audit.CERTIFIED),
        "certified_theorem_instances": ledger["certified_theorem_instances"],
        "unique_fully_qualified_theorem_names": ledger["unique_fully_qualified_theorem_names"],
        "sources": manifest_rows,
    }
    MANIFEST_OUT.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    css = r"""
:root{--bg:#050b16;--panel:#0a1424;--panel2:#0d1b2e;--ink:#e8edf5;--muted:#93a4ba;--gold:#d7ad4a;--cyan:#60c7d8;--red:#ff8f8f;--line:#1c3048}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}a{color:var(--cyan)}code,pre{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}.wrap{max-width:1500px;margin:auto;padding:36px}.hero{border:1px solid var(--line);background:linear-gradient(135deg,#07101e,#0b1829);padding:28px;border-radius:18px}.hero h1{margin:0 0 8px;color:var(--gold);font-size:34px}.hero p{max-width:1050px;color:var(--muted)}.stats{display:flex;gap:12px;flex-wrap:wrap;margin:20px 0}.stat{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 16px}.stat b{display:block;font-size:24px;color:var(--gold)}.warning{border-left:4px solid var(--gold);background:#151509;padding:14px 18px;margin:22px 0}.grid{display:grid;grid-template-columns:1fr;gap:18px}h2{color:var(--gold);margin-top:34px}table{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line)}th,td{padding:10px;border-bottom:1px solid var(--line);text-align:left}th{color:var(--gold)}.num{text-align:right}.controls{position:sticky;top:0;background:rgba(5,11,22,.96);padding:12px 0;z-index:3}.controls input{width:100%;padding:13px 15px;border-radius:10px;border:1px solid var(--line);background:var(--panel);color:var(--ink);font-size:16px}.source-card{background:var(--panel);border:1px solid var(--line);border-radius:12px;overflow:hidden}.source-card summary{cursor:pointer;padding:14px 16px;background:var(--panel2);display:flex;gap:10px;align-items:center;flex-wrap:wrap}.meta{color:var(--muted);margin-left:auto}.pill{font-size:11px;letter-spacing:.06em;border:1px solid var(--cyan);color:var(--cyan);border-radius:999px;padding:2px 7px}.source-meta,.theorem-list{padding:12px 16px;border-top:1px solid var(--line);color:var(--muted)}pre{margin:0;padding:18px;overflow:auto;background:#030811;border-top:1px solid var(--line);white-space:pre;tab-size:2;font-size:12.5px}.hidden{display:none!important}.foot{color:var(--muted);margin:30px 0 10px}
"""
    js = r"""
const q=document.getElementById('q');const cards=[...document.querySelectorAll('.source-card')];const count=document.getElementById('visible-count');
function filter(){const x=q.value.trim().toLowerCase();let n=0;for(const c of cards){const ok=!x||c.dataset.search.includes(x);c.classList.toggle('hidden',!ok);if(ok)n++;}count.textContent=n;}q.addEventListener('input',filter);filter();
"""
    page = f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>Operator-First Lean Proof Atlas</title><style>{css}</style></head><body><div class='wrap'>
<div class='hero'><h1>Operator-First Lean Proof Atlas</h1><p>Versioned reading copy of the certified Lean proof corpus. Every displayed module is an exact snapshot from the PR head recorded by the corpus ledger. The bundled <code>.lean</code> snapshots and commit SHAs are the authority; this HTML is the searchable presentation layer.</p>
<div class='stats'><div class='stat'><b>{ledger['certified_theorem_instances']}</b>certified theorem instances</div><div class='stat'><b>{ledger['unique_fully_qualified_theorem_names']}</b>unique fully-qualified theorem names</div><div class='stat'><b>{len(audit.CERTIFIED)}</b>certified PR bundles</div><div class='stat'><b>{len(manifest_rows)}</b>certified source snapshots</div></div></div>
<div class='warning'><b>Formal means formal within the Lean statement and its assumptions.</b> It does not automatically prove the surrounding physical interpretation, continuum limit, analytic input, or conjectural bridge. Exact numerical certificates and scientific interpretations that are not Lean declarations are intentionally outside this atlas.</div>
<h2>Certified bundles</h2><table><thead><tr><th>PR</th><th>Program</th><th>Verifier bundle</th><th>Theorem instances</th><th>Head</th></tr></thead><tbody>{''.join(bundles_html)}</tbody></table>
<h2>All certified Lean sources</h2><div class='controls'><input id='q' placeholder='Search theorem, source, PR, project, or Lean text…'><div class='foot'><span id='visible-count'></span> source snapshots visible</div></div><div class='grid'>{''.join(cards)}</div>
<div class='foot'>Generated from <code>lean_corpus_audit.py</code> and exact PR heads. Companion files: <code>lean_corpus_ledger.json</code>, <code>SOURCE_MANIFEST.json</code>, and <code>sources/</code>.</div></div><script>{js}</script></body></html>"""
    HTML_OUT.write_text(page, encoding="utf-8")
    print(json.dumps({"status":"PASS","html":str(HTML_OUT),"sources":len(manifest_rows),"theorem_instances":ledger["certified_theorem_instances"],"unique_theorems":ledger["unique_fully_qualified_theorem_names"]}, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: lean_proof_atlas.py PR_REFS_TSV")
    build(pathlib.Path(sys.argv[1]))
