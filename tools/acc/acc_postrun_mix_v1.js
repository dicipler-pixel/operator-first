// acc_postrun_mix v1 — mix after every run. Usage: node tools/acc/acc_postrun_mix_v1.js <recipes dir> <ledger jsonl (append)> [label]
// For every recipe: read() through the frozen mixer core, run the recipe's own settings, run the mixer defaults,
// run three fixed "trail" mixes (bookkeeping identity, plateau count, shape cancellations vs delta), and append one
// JSON line per run. Also confirms recipe() -> read() -> mix() round-trips to the same combined array.
const fs=require('fs'),path=require('path');const ROOT=path.resolve(__dirname,'..','..');
const E=require(path.join(ROOT,'tools/compound-eye/projects/eye_mixer/mixer_core.js'));
const [dir,ledger,label='postrun']=process.argv.slice(2);if(!dir||!ledger){console.error('usage: dir ledger [label]');process.exit(2)}
const files=fs.readdirSync(dir).filter(f=>f.endsWith('.json')).sort();const val=(d,id)=>d.traces.find(t=>t.id===id).values;
let n=0,bad=[],lines=[];const tot={default_refused:0,runs:0,identity_mismatch_runs:0,roundtrip_fail:0,plateau_total:0,steps:0,rms_default:0};
for(const f of files){
  let r;try{r=E.read(fs.readFileSync(path.join(dir,f),'utf8'))}catch(e){bad.push([f,'read: '+e.message]);continue}
  const d=r.dataset;const s0=r.settings||E.defaults(d);let m0;try{m0=E.mix(d,s0)}catch(e){bad.push([f,'mix(settings): '+e.message]);continue}
  const sd=E.defaults(d);let md,default_refused=null;try{md=E.mix(d,sd)}catch(e){default_refused=e.message;sd.normalization='rms';md=E.mix(d,sd)}
  // trail mix 1: bookkeeping identity delta_total + cancellations = operand letters (source units, letters)
  const s1=E.copy(sd);s1.normalization='source';for(const c of Object.values(s1.channels)){c.enabled=false;c.weight=1;c.route='both'}
  s1.channels.delta_total.enabled=true;s1.channels.cancellations.enabled=true;const m1=E.mix(d,s1);
  const code=val(d,'move_class_code'),mv=val(d,'move_id'),r0=val(d,'len_r0'),r1=val(d,'len_r1');let mism=0;
  m1.combined.forEach((v,k)=>{if(!k)return;const c=code[k];const want=c===3?2:c===1?0:(mv[k]===2||mv[k]===3?r1[k-1]:r0[k-1]);if(v!==want)mism++});
  // trail mix 2: plateaus — total_length alone, count zero-delta steps
  const s2=E.copy(s1);for(const c of Object.values(s2.channels))c.enabled=false;s2.channels.total_length.enabled=true;const m2=E.mix(d,s2);
  let plateau=0;for(let k=1;k<m2.combined.length;k++)if(m2.combined[k]===m2.combined[k-1])plateau++;
  // trail mix 3: shape X=cancellations Y=delta_total, y >= -x violations
  const s3=E.copy(s1);for(const c of Object.values(s3.channels))c.enabled=false;s3.channels.cancellations.enabled=true;s3.channels.cancellations.route='x';s3.channels.delta_total.enabled=true;s3.channels.delta_total.route='y';const m3=E.mix(d,s3);
  let viol=0;m3.X.forEach((x,k)=>{if(m3.Y[k]<-x)viol++});
  // round trip: recipe() -> read() -> mix()
  const rt=E.read(JSON.stringify(E.recipe(d,s0)));const mrt=E.mix(rt.dataset,rt.settings);const roundtrip=JSON.stringify(mrt.combined)===JSON.stringify(m0.combined);
  const steps=d.x.length-1;const line={label,file:f,dataset:d.id,steps,rms_settings:m0.rmsCombined,rms_default:md.rmsCombined,active_default:md.activeCount,default_refused,
    identity_mismatches:mism,plateau_steps:plateau,shape_violations:viol,final_length:val(d,'total_length')[steps],max_length:Math.max(...val(d,'total_length')),roundtrip,at:new Date().toISOString()};
  lines.push(JSON.stringify(line));n++;tot.runs++;tot.steps+=steps;tot.plateau_total+=plateau;tot.rms_default+=md.rmsCombined;if(mism)tot.identity_mismatch_runs++;if(default_refused)tot.default_refused++;if(!roundtrip)tot.roundtrip_fail++;
}
fs.appendFileSync(ledger,lines.join('\n')+'\n');
console.log(JSON.stringify({label,dir,runs:tot.runs,steps:tot.steps,plateau_steps:tot.plateau_total,plateau_fraction:+(tot.plateau_total/tot.steps).toFixed(4),mean_rms_default:+(tot.rms_default/tot.runs).toFixed(4),identity_mismatch_runs:tot.identity_mismatch_runs,defaults_refused_mixed_units:tot.default_refused,roundtrip_fail:tot.roundtrip_fail,unreadable:bad.length,ledger},null,1));
if(bad.length)console.log('bad:',bad.slice(0,5));
