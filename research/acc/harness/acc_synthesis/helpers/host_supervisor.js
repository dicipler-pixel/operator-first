async function runSupervisor(maxJobs=25) {
 // Tool-host adapter. The owner-authorized GitHub connector remains outside workers.
 if(!Number.isInteger(maxJobs)||maxJobs<1||maxJobs>25)throw Error('At most 25 existing bounded jobs per activation');
 const repo='dicipler-pixel/operator-first',branch='claude/gallant-bardeen-0pgpae';
 const quote=s=>"'"+String(s).replaceAll("'","'\\''")+"'";
 const driver=eval('('+load('work_driver')+')');
 async function shell(cmd){
  let r=await tools.exec_command({cmd,workdir:load('work_parent'),yield_time_ms:1000,max_output_tokens:5000});
  while(r.session_id)r=await tools.write_stdin({session_id:r.session_id,chars:'',yield_time_ms:1000,max_output_tokens:5000});
  if(r.exit_code!==0)throw Error('Supervisor stage failed: '+r.output);
  return r.output;
 }
 async function intake(){
  const policy=JSON.parse(await shell('cat acc_synthesis/helpers/auto_intake_policy.json'));
  const ref=await tools.mcp__codex_apps__github_fetch({url:'https://api.github.com/repos/'+repo+'/git/refs/heads/'+branch});
  if(ref.isError)throw Error('Source head unavailable');
  const head=JSON.parse(ref.structuredContent.content).object.sha;
  const replies=await Promise.allSettled(policy.source_paths.map(path=>tools.mcp__codex_apps__github_fetch_file({repository_full_name:repo,ref:head,path})));
  const files=replies.map((r,i)=>{
   if(r.status!=='fulfilled'||r.value.isError||typeof r.value.structuredContent?.content!=='string')throw Error('Allowed route feed unavailable: '+policy.source_paths[i]);
   return {path:policy.source_paths[i],content:r.value.structuredContent.content};
  });
  const payload=JSON.stringify({head,files});
  // Quote the entire Python expression for the shell; never interpolate route text as shell code.
  const chunks=[];for(let i=0;i<payload.length;i+=20000)chunks.push(payload.slice(i,i+20000));
  for(let base=0;base<chunks.length;base+=8){
   const written=await Promise.allSettled(chunks.slice(base,base+8).map((s,n)=>shell('python -c '+quote('from pathlib import Path;Path('+JSON.stringify('/tmp/acc_auto_feed_'+(base+n))+').write_text('+JSON.stringify(s)+')'))));
   for(const r of written)if(r.status!=='fulfilled')throw r.reason;
  }
  await shell('python -c '+quote('from pathlib import Path;p=Path("/tmp/acc_auto_feed.json");p.write_text("".join(Path("/tmp/acc_auto_feed_"+str(i)).read_text() for i in range('+chunks.length+')))'));
  const prepared=JSON.parse(await shell('python acc_synthesis/helpers/auto_intake.py prepare --feed /tmp/acc_auto_feed.json'));
  if(!['reserved_intake','no_new_known_routes','closed_intake_key'].includes(prepared.status))return prepared;
  await driver(0); // Atomic private checkpoint BEFORE any verification work.
  if(prepared.status!=='reserved_intake')return prepared;
  if((load('work_new_messages')||[]).length)return {status:'review_new_messages',reserved_intake:prepared.lease};
  const reservation=load('work_last_commit'),key=prepared.lease.key;
  let r=await tools.exec_command({cmd:'python acc_synthesis/helpers/auto_intake.py run --key '+key+' --reservation-commit '+reservation+' > /tmp/acc_auto_intake_result.json 2>&1',workdir:load('work_parent'),yield_time_ms:30000,max_output_tokens:1000});
  while(r.session_id)r=await tools.write_stdin({session_id:r.session_id,chars:'',yield_time_ms:1000,max_output_tokens:1000});
  const resultText=await shell('tail -15 /tmp/acc_auto_intake_result.json');
  await driver(0); // Preserve both completed receipts and interrupted failures.
  if(r.exit_code!==0)throw Error('Intake interrupted, preserved without retry: '+resultText);
  const result=JSON.parse(resultText);text({automatic_intake:result});return result;
 }
 let remaining=maxJobs,intakeChecked=false;const all=[];
 while(remaining>0){
  const result=await driver(remaining);all.push(result);
  remaining-=result?.summaries?.length||0;
  if(result?.status!=='exhausted')return {status:result?.status||'completed',job_allowance_remaining:remaining,results:all};
  if(intakeChecked)return {status:'waiting_for_new_evidence',results:all};
  intakeChecked=true;
  const fresh=await intake();all.push({intake:fresh});
  if(fresh.status!=='verified_new_graph')return {status:fresh.status==='no_new_known_routes'?'waiting_for_new_evidence':fresh.status,results:all};
 }
 return {status:'activation_job_allowance_complete',results:all};
}
