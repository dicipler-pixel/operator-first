#!/usr/bin/env python3
"""Validate catalog structure, pinned paths and deterministic generated pages."""
import json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 papers=json.loads((ROOT/'catalog/papers.json').read_text());cards=json.loads((ROOT/'atlas/cards.json').read_text());snap=json.loads((ROOT/'catalog/source_snapshot.json').read_text())
 ids=[p['id'] for p in papers['projects']];cids=[c['id'] for c in cards]
 assert len(ids)==len(set(ids)) and len(cids)==len(set(cids))
 assert papers['coverage']=='partial' and papers['intake_queue']
 prs={p['number']:p for p in snap['pull_requests']};sources=0
 for rec in papers['projects']+cards:
  assert rec['title'] and rec['sources'] is not None
  for source in rec['sources']:
   assert source['url'].startswith('https://github.com/')
   if 'pr' not in source:continue
   p=prs[source['pr']];assert source['sha']==p['head_sha']
   assert source['path'] in {f['path'] for f in snap['trees'][str(source['pr'])]}
   assert '/'+source['sha']+'/'+source['path'] in source['url'];sources+=1
 for c in cards:
  assert c['papers'] and set(c['papers'])<=set(ids)
  for k in ['statement','assumptions','failure_mode','evidence_status','verification_scope','credit','next_step']:assert c[k]
  assert c['sources'] or 'intake pending' in c['evidence_status']
 links=0
 for p in ROOT.rglob('*.md'):
  for target in re.findall(r'\]\(([^)]+)\)',p.read_text()):
   if target.startswith(('https://','http://','#')):continue
   assert (p.parent/target.split('#')[0]).exists(),(p,target);links+=1
 generated=[ROOT/'catalog/README.md',ROOT/'atlas/README.md']+list((ROOT/'papers').glob('*/README.md'))+[ROOT/'atlas'/f'{c}.md' for c in cids]
 before={str(p):p.read_bytes() for p in generated}
 subprocess.run([sys.executable,str(ROOT/'scripts/build_catalog.py')],check=True)
 assert all(Path(p).read_bytes()==b for p,b in before.items()),'Generated pages were stale'
 print(json.dumps({'status':'PASS','projects':len(ids),'cards':len(cids),'pinned_path_references':sources,'local_links':links,'generated_pages':len(generated),'scope':'catalog validation only; not proof recompilation'}))
if __name__=='__main__':main()
