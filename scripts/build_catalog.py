#!/usr/bin/env python3
"""Generate the human-readable register from its machine-readable records."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def render():
 data=json.loads((ROOT/'catalog/papers.json').read_text());cards=json.loads((ROOT/'atlas/cards.json').read_text())
 counts=json.loads((ROOT/'tools/compound-eye/release_counts.json').read_text())
 front=['# Operator-first research master','',f"Jeromie N. Beasley’s current research directory: **{len(data['projects'])} projects**, **{len(cards)} Atlas cards**, and **Compound Eye Universal 3.2**.",'','Start with [current project status](MASTER_STATUS.md), the [paper register](catalog/README.md), or the [reusable-results Atlas](atlas/README.md).','',f"The [complete instrument](tools/compound-eye/START_HERE.md) contains **{counts['eye_versions']} eye versions in {counts['sets']} sets**: {counts['statuses']['implemented']} implemented, {counts['statuses']['specified']} specified, and {counts['statuses']['archived_result']} archived results. It combines the independent Universal 2.2 and 3.1 lines with Eye Mixer 1.0.0.",'','## Use or share the tool','','Download this repository and open `tools/compound-eye/START_HERE.html`, or build the standalone package with `python scripts/package_compound_eye.py --output release-output`. The full scientific replay command is `python tools/compound-eye/run_all.py` after installing its requirements; Node.js is needed for the mixer checks. The HTML works offline. The package builder restores the large raw dataset automatically from checked repository pieces. For a raw-source audit directly in a clone, first run `python scripts/restore_large_files.py`.','','The [original 3.1 upload backup](backups/2026-09-08-universal-3-1/README.md) and [earlier complete backup](backups/2026-09-08/README.md) preserve both release lines. Every registered source definition and installed implementation is retained.','','## Research and proof scope','','The root build incorporates the repair from PR #1 and checks its finite core. The [source snapshot](catalog/source_snapshot.json) records exact heads and available workflow evidence for the other proof branches. Their independent status and mathematical limits remain explicit in the register. A successful instrument integration does not establish new physical calibration or solve the six Diophantine equations.','','## Keep the master current','','Read [AGENTS.md](AGENTS.md) and [catalog policy](catalog/POLICY.md). Fetch branches before importing another chat’s work; compare source inventories, then add missing versions without rewriting existing ones. Run `python scripts/build_catalog.py`, `python scripts/validate_catalog.py` and `python scripts/verify_compound_eye_release.py` after relevant changes.','','The register remains a partial inventory of the wider 20+ paper corpus. Unresolved publication identities and missing source material remain in the intake queue.']
 (ROOT/'README.md').write_text('\n'.join(front)+'\n')
 lines=['# Master paper register','','This is an initial source register, not a complete census of the 20+ paper corpus. The project coverage is listed below. Published titles, versions and DOIs require source reconciliation where marked.','', '| Project | Source state | Next concrete step |','|---|---|---|']
 for p in data['projects']:
  lines.append(f"| [{p['title']}](../papers/{p['id']}/README.md) | {p['state']} | {p['next_step']} |")
 lines+=['','## Intake queue','','These entries are leads supplied in the research conversation, not verified publication records. No missing code is assumed to exist in GitHub.','']
 lines += ['- '+p for p in data['intake_queue']]
 (ROOT/'catalog/README.md').write_text('\n'.join(lines)+'\n')
 for p in data['projects']:
  d=ROOT/'papers'/p['id'];d.mkdir(parents=True,exist_ok=True)
  ls=['# '+p['title'],'',p['scope'],'','## Source locations','']
  ls += [f"- [{s['label']}]({s['url']})" for s in p['sources']]
  ls+=['','## Reusable results','']+[f"- [{c['title']}](../../atlas/{c['id']}.md)" for c in cards if p['id'] in c['papers']]
  ls+=['','## Next step','',p['next_step'],'','## Release policy','','One self-contained proofs-and-code supplement per paper release, with pinned shared sources and dependency locks. Published manuscripts and images remain separate. Publication identity: '+p['publication_identity']+'.','','[Back to register](../../catalog/README.md)']
  (d/'README.md').write_text('\n'.join(ls)+'\n')
 index=['# Reusable results and tools Atlas','','Cards describe exact scope. Their presence here does not upgrade a written proof to a Lean proof or a computation to a theorem.','', '| Card | Evidence status | Used by |','|---|---|---|']
 for c in cards:
  index.append(f"| [{c['title']}]({c['id']}.md) | {c['evidence_status']} | {', '.join(c['papers'])} |")
  ls=['# '+c['title'],'','Stable ID: `'+c['id']+'`','']
  for key in ['statement','assumptions','failure_mode','evidence_status','verification_scope','credit','next_step']:
   ls+=['## '+key.replace('_',' ').capitalize(),'',c[key],'']
  ls+=['## Sources','']+[f"- [{s['label']}]({s['url']})" for s in c['sources']]
  ls+=['','## Paper applications','']+[f'- [{p}](../papers/{p}/README.md)' for p in c['papers']]
  (ROOT/'atlas'/f"{c['id']}.md").write_text('\n'.join(ls)+'\n')
 (ROOT/'atlas/README.md').write_text('\n'.join(index)+'\n')
if __name__=='__main__':render()
