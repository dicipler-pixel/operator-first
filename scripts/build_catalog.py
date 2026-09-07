#!/usr/bin/env python3
"""Generate the human-readable register from its machine-readable records."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def render():
 data=json.loads((ROOT/'catalog/papers.json').read_text());cards=json.loads((ROOT/'atlas/cards.json').read_text())
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
