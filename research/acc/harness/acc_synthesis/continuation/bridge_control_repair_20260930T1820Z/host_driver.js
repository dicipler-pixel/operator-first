async function runWork(count,resumeReserved=false,focusRow=null){
 const repo="dicipler-pixel/operator-first",branch="claude/gallant-bardeen-0pgpae",prefix="research/acc/harness/acc_synthesis/";
 const parent=load("work_parent");if(!parent)throw Error("Initialize work_parent and reviewed work_head/claims first");
 const quote=s=>"'"+String(s).replaceAll("'","'\\''")+"'";
 async function api(path){const r=await tools.mcp__codex_apps__github_fetch({url:"https://api.github.com/repos/"+repo+path});if(r.isError)throw Error("GitHub read failed");return JSON.parse(r.structuredContent.content);}
 async function shell(cmd){const r=await tools.exec_command({cmd,workdir:parent,max_output_tokens:24000,yield_time_ms:1000});if(r.session_id||r.exit_code!==0)throw Error("Stage failed: "+r.output);return r.output;}
 async function refresh(){
  const head=(await api("/git/refs/heads/"+branch)).object.sha,old=load("work_head");
  if(!old)throw Error("Reviewed starting head required");
  if(head!==old){
   const d=await api("/compare/"+old+"..."+head);
   if(!["ahead","identical"].includes(d.status)||d.files.length>=300)throw Error("Reconcile branch divergence or oversized diff");
   if(d.files.some(x=>x.filename.startsWith(prefix)||x.filename==="research/acc/live/WORKING_harness.md"))throw Error("Concurrent harness write: reconcile before proceeding");
   const claims=load("work_claims")||{};
   for(const f of d.files.filter(x=>/^research\/acc\/live\/WORKING_/.test(x.filename))){
    if(!(f.filename in claims))throw Error("Changed claim needs interpretation: "+f.filename);
    const r=await tools.mcp__codex_apps__github_fetch_file({repository_full_name:repo,ref:head,path:f.filename});
    claims[f.filename]=r.structuredContent.content;
   }
   store("work_claims",claims);
   const messages=d.files.filter(x=>/^research\/acc\/live\/UPDATE_(?!astra_to_).*(?:astra|to_all).*\.md$/.test(x.filename));
   for(const m of messages){
    const r=await tools.mcp__codex_apps__github_fetch_file({repository_full_name:repo,ref:head,path:m.filename});
    const q=load("work_new_messages")||[];q.push({path:m.filename,head,...r.structuredContent});store("work_new_messages",q);
    text({new_message:m.filename,content:r.structuredContent.content});
   }
  }
  store("work_head",head);
  const textClaims=Object.values(load("work_claims")||{}).join("\n");
  const excluded=[...new Set([...textClaims.matchAll(/(?:sac|ac)-(\d{5})/g)].map(x=>"ac-"+x[1]))];
  if(focusRow){const selected=load("work_selected_rows");if(!selected?.includes(focusRow))throw Error("Focus outside pinned rows");excluded.push(...selected.filter(x=>x!==focusRow));}
  store("work_excluded",[...new Set(excluded)]);return head;
 }
 async function readFile(path,len){
  if(!/^\/tmp\/acc_work_(entries|blob_\d+)\.json$/.test(path))throw Error("Unexpected pack path");
  const chunks=[];for(let n=0;n<len;n+=32000)chunks.push({off:n,len:Math.min(32000,len-n)});
  const out=[];
  for(let i=0;i<chunks.length;i+=20){
   const got=await Promise.allSettled(chunks.slice(i,i+20).map(x=>tools.exec_command({cmd:"python -c "+quote("from pathlib import Path;import sys;sys.stdout.write(Path("+JSON.stringify(path)+").read_text()["+x.off+":"+(x.off+x.len)+"])"),workdir:parent,max_output_tokens:23000})));
   got.forEach((v,j)=>{if(v.status!=="fulfilled"||v.value.exit_code!==0||v.value.output.length!==chunks[i+j].len)throw Error("Artifact transfer failed");out.push(v.value.output);});
  }
  return JSON.parse(out.join(""));
 }
 async function persist(label,job){
  const pack=JSON.parse(await shell("PYTHONPATH=. python /tmp/acc_work_stage.py pack"));
  const entries=await readFile(pack.files[0].path,pack.files[0].length);
  for(const f of pack.files.slice(1)){
   const b=await readFile(f.path,f.length);
   const r=await tools.mcp__codex_apps__github_create_blob({repository_full_name:repo,content:b.content,encoding:b.encoding});
   if(r.structuredContent?.sha!==b.expected_sha)throw Error("Blob persistence failed");
  }
  for(let attempt=0;attempt<4;attempt++){
   const head=await refresh();
   if(pack.active&&load("work_excluded").includes(job.row_id))throw Error("Competing claim: reserved work not launched");
   const base=(await api("/git/commits/"+head)).tree.sha;
   const t=await tools.mcp__codex_apps__github_create_tree({repository_full_name:repo,base_tree_sha:base,tree_elements:entries});
   if(!t.structuredContent?.sha)throw Error("Git tree failed");
   const c=await tools.mcp__codex_apps__github_create_commit({repository_full_name:repo,parent_sha:head,tree_sha:t.structuredContent.sha,message:"ACC harness: "+label+" "+job.helper+" "+job.row_id});
   const sha=c.structuredContent?.sha;if(!sha)throw Error("Git commit failed");
   const u=await tools.mcp__codex_apps__github_update_ref({repository_full_name:repo,branch_name:branch,sha,force:false});
   if(!u.structuredContent?.success){if(attempt<3&&/Reference cannot be updated|fast.forward/i.test(String(u.structuredContent?.error)))continue;throw Error("Fast-forward update failed: "+JSON.stringify(u.structuredContent));}
   const check=(await api("/git/refs/heads/"+branch)).object.sha;
   if(check!==sha){const d=await api("/compare/"+sha+"..."+check);if(!["ahead","identical"].includes(d.status))throw Error("Published checkpoint not reachable");}
   store("work_head",sha);store("work_last_commit",sha);
   const updateMeta="import json,hashlib;from pathlib import Path;p=Path('/tmp/acc_work_meta.json');m=json.loads(p.read_text());d={x['path']:x['sha'] for x in m['files']};known=set(m['known']);es=json.loads(Path('/tmp/acc_work_entries.json').read_text());prefix="+JSON.stringify(prefix)+";[(d.update({e['path'][len(prefix):]:e.get('sha') or hashlib.sha1(b'blob '+str(len(e['content'].encode())).encode()+b'\\0'+e['content'].encode()).hexdigest()})) for e in es if e['path'].startswith(prefix)];known.update(d.values());m.update(files=[{'path':k,'sha':v} for k,v in d.items()],known=sorted(known));p.write_text(json.dumps(m))";
   await shell("python -c "+quote(updateMeta));return sha;
  }
  throw Error("Persistence retries exhausted");
 }
 if(count===0){
  const job=JSON.parse(await shell("python -c "+quote("import json;from pathlib import Path;c=json.loads(Path('acc_synthesis/continuation/checkpoint.json').read_text());assert c['active'] is None;print(json.dumps(c['attempts'][-1]['job']))")));
  const sha=await persist("checkpoint reviewed result",job);text({checkpoint_commit:sha});return;
 }
 const summaries=[];
 for(let n=0;n<count;n++){
  await refresh();let job;
  if(n===0&&resumeReserved){
   const p=JSON.parse(await shell("PYTHONPATH=. python /tmp/acc_work_stage.py pack"));
   if(!p.active||p.active.phase!=="reserved")throw Error("No unlaunched reservation");job=p.active.job;
  }else{
   const p=JSON.parse(await shell("PYTHONPATH=. python /tmp/acc_work_stage.py reserve --head "+load("work_head")+" --exclude "+quote(JSON.stringify(load("work_excluded")))));
   if(p.status!=="reserved"){text(p);return {status:p.status,summaries};}job=p.active.job;
  }
  const reservation=await persist("reserve code-only",job);
  text({started:job.helper,row:job.row_id,key:job.key,reservation});
  let run=await tools.exec_command({cmd:"python acc_synthesis/helper_batch.py run --key "+job.key+" --reservation-commit "+reservation+" > /tmp/acc_work_batch_run.json 2>&1",workdir:parent,yield_time_ms:30000,max_output_tokens:1500});
  while(run.session_id)run=await tools.write_stdin({session_id:run.session_id,chars:"",yield_time_ms:1000,max_output_tokens:1500});
  if(run.exit_code!==0){text(await shell("tail -35 /tmp/acc_work_batch_run.json"));throw Error("Search interrupted: preserve checkpoint and inspect");}
  await shell("python acc_synthesis/helpers/audit_artifacts.py --sync");
  const s=JSON.parse(await shell("python -c "+quote("import json;from pathlib import Path;c=json.loads(Path('acc_synthesis/continuation/checkpoint.json').read_text());a=c['attempts'][-1];print(json.dumps({'helper':a['job']['helper'],'row':a['job']['row_id'],'kind':a['kind'],'summary':a['summary'],'gate':a.get('gate'),'result_path':a['result_path']}))")));
  const sha=await persist("checkpoint completed",job);
  const small={helper:s.helper,row:s.row,kind:s.kind,summary:s.summary,commit:sha,result_path:s.result_path};
  summaries.push(small);text(small);
  if(s.gate?.exact_verified){store("work_candidate",s);return {status:"candidate",summaries};}
  if((load("work_new_messages")||[]).length)return {status:"review_new_messages",summaries};
 }
 return {status:"batch_group_completed",summaries};
}
