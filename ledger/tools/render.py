import json, sys, collections, datetime
L=sys.argv[1]; OUT=sys.argv[2]
import subprocess, os
decls=json.load(open(f'{L}/declarations.json')); wf=json.load(open(f'{L}/wfmap.json')); runs=json.load(open(f'{L}/branch_runs.json'))
latest=json.load(open(f'{L}/branch_latest_runs.json')) if os.path.exists(f'{L}/branch_latest_runs.json') else {}
_anc={}
def is_ancestor(a,b):
    k=(a,b)
    if k not in _anc: _anc[k]=subprocess.run(['git','merge-base','--is-ancestor',a,b]).returncode==0
    return _anc[k]
def runs_for(branch,file,file_last_commit):
    br=runs.get(branch,{}); wfs=set(wf.get(branch,{}).get(file,[]))
    out=[r for r in br.get('runs',[]) if r['workflow'] in wfs]; have={r['workflow'] for r in out}
    # path-scoped workflows do not run on every push: accept the latest run of the workflow on this branch
    # if the file's last commit is an ancestor of (or equal to) the commit that run built.
    for w in wfs-have:
        r=latest.get(branch,{}).get(w)
        if r and file_last_commit and is_ancestor(file_last_commit,r['head_sha']):
            out.append({'workflow':w,'run_id':r['run_id'],'conclusion':r['conclusion'],'event':'earlier-commit','created_at':r['created_at'],'built_sha':r['head_sha'][:12]})
    return out, sorted(wfs)
status_count=collections.Counter(); recs=[]
for d in decls:
    occ=[]; best='UNVERIFIED'
    for o in d['branches']:
        rs,wfs=runs_for(o['branch'],d['file'],o['file_last_commit'])
        succ=[r for r in rs if r['conclusion']=='success']; fail=[r for r in rs if r['conclusion'] not in ('success',None)]
        st='VERIFIED' if succ else ('FAILED-AT-HEAD' if fail else ('NO-RUN-AT-HEAD' if wfs else 'NO-WORKFLOW'))
        occ.append({**o,'workflows':wfs,'runs':[{'run_id':r['run_id'],'workflow':r['workflow'].split('/')[-1],'conclusion':r['conclusion'],'built':r.get('built_sha','head')} for r in rs],'status':st})
        rank={'VERIFIED':3,'FAILED-AT-HEAD':2,'NO-RUN-AT-HEAD':1,'NO-WORKFLOW':0,'UNVERIFIED':0}
        if rank[st]>rank[best]: best=st
    if best=='NO-WORKFLOW': best='UNVERIFIED'
    if best=='NO-RUN-AT-HEAD': best='UNVERIFIED'
    status_count[best]+=1; recs.append({'name':d['name'],'kind':d['kind'],'file':d['file'],'statement':d['statement'],'status':best,'occurrences':occ})
with open(f'{OUT}.jsonl','w') as f:
    for r in recs: f.write(json.dumps(r)+'\n')
by_file=collections.defaultdict(list)
for r in recs: by_file[r['file']].append(r)
md=[f"# Lean certificate ledger — {datetime.date.today().isoformat()}\n",
"Authoritative format per the author's instruction: theorem name, exact Lean declaration, source file, verified commit, verification run. Extracted read-only from every branch of `dicipler-pixel/operator-first` (git objects) and the GitHub Actions run history; nothing was compiled here.\n",
"**Status meaning.** VERIFIED = at least one branch containing this exact statement has a completed workflow run with conclusion success on that branch's head commit, from a workflow that references the file (by path, module, directory, or as a root lake library under `ci.yml`). FAILED-AT-HEAD = only failing runs found at head. UNVERIFIED = no run at head could be tied to the file. A run verifies the whole file/library it built, not the theorem in isolation; a `sorry`-free build is what the workflow asserts (no `.lean` file on any branch contains `sorry`), and axiom audits exist only where the workflow performs them. Runs marked `built <sha>` come from path-scoped workflows that did not re-run on the branch head; they are accepted only when the file's last commit is an ancestor of the commit the run built, i.e. the file content the run compiled is the content listed.\n",
"| status | declarations |\n|---|---:|"]+[f"| {k} | {v} |" for k,v in sorted(status_count.items())]+[f"| **total** | **{len(recs)}** |\n",
f"Unique declarations {len(recs)} in {len(by_file)} files across {len(wf)} branches. The same theorem name appears more than once when its statement differs between branches; each variant is its own row.\n"]
for file in sorted(by_file):
    rs=by_file[file]; md.append(f"\n## `{file}` — {len(rs)} declarations\n")
    for r in rs:
        md.append(f"### `{r['name']}` — {r['status']}\n\n```lean\n{r['statement']}\n```\n")
        md.append("| branch | head | file last commit | workflow(s) | run(s) | status |\n|---|---|---|---|---|---|")
        for o in r['occurrences']:
            runs_s=', '.join(f"{x['run_id']} ({x['conclusion']}{'' if x['built']=='head' else ', built '+x['built']})" for x in o['runs']) or '—'
            md.append(f"| {o['branch']} | {o['head']} | {o['file_last_commit']} | {', '.join(w.split('/')[-1] for w in o['workflows']) or '—'} | {runs_s} | {o['status']} |")
        md.append("")
open(f'{OUT}.md','w').write('\n'.join(md))
print(dict(status_count), 'files',len(by_file), 'md bytes',len('\n'.join(md)))
