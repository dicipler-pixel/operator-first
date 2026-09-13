const fs=require('fs'),path=require('path');
const E=require('/home/user/operator-first/tools/compound-eye/projects/eye_mixer/mixer_core.js');
const OUT=process.env.OUT_DIR||__dirname;
const rms=a=>{const v=a.filter(Number.isFinite);return Math.sqrt(v.reduce((s,x)=>s+x*x,0)/v.length)};
const ledger={schema:'compound-eye-intervention-ledger-v1',trials:[]};
function loadRun(id){const r=E.read(fs.readFileSync(`/home/user/operator-first/tools/acc/decoded_v2/${id}__training__recipe.json`,'utf8'));return {d:r.dataset,s:r.settings}}
const V={confirmed:'matched',refuted:'failed',blocked:'ambiguous'}; // map to the 5.1 page's verdict vocabulary
const snap=(m)=>m?{activeCount:m.activeCount,rmsOriginal:m.rmsOriginal,rmsCombined:m.rmsCombined,rmsResidual:m.rmsResidual}:null;
function trial(name,prediction,run,setup,observe,norm='source',expectRefusal=false){
  const {d}=loadRun(run); const s=E.defaults(d); s.normalization=norm;
  for(const c of Object.values(s.channels)){c.enabled=false;c.weight=1;c.route='both'}
  // "before" = the dataset with every channel muted, exactly as the page would snapshot it before the intervention
  const before={settings:E.copy(s),mix:null};
  setup(s); let m=null,obs;
  try{m=E.mix(d,s)}catch(e){obs={text:`mixer refused: ${e.message}`,verdict:expectRefusal?'confirmed':'blocked'}}
  if(!obs)obs=observe(m,d,s);
  const t={createdUTC:new Date().toISOString(),dataset:d.id,datasetTitle:d.title,prediction,before,
    observation:obs.text,verdict:V[obs.verdict],closedUTC:new Date().toISOString(),after:{settings:E.copy(s),mix:snap(m)},
    trial_name:name,harness_verdict:obs.verdict,recipe_file:!m?null:`${name}_recipe.json`};
  ledger.trials.push(t);
  if(m)fs.writeFileSync(path.join(OUT,`${name}_recipe.json`),JSON.stringify(E.recipe(d,s),null,1));
  console.log(`\n[${name}] ${run}\n  predict: ${prediction}\n  observe: ${obs.text}\n  verdict: ${obs.verdict} (${V[obs.verdict]})`);
}
const step=(d,id)=>d.traces.find(t=>t.id===id).values;
// T1: exact bookkeeping identity — delta_total + cancellations should equal the operand letters added (|r_j| for multiply, 2 for conjugate, 0 for invert)
trial('T1_delta_plus_canc','delta_total(w=+1) + cancellations(w=+1) equals 2 on every conjugate step, |other relator| on every multiply step, 0 on invert/step0',
 'ms-train-0160',s=>{s.channels.delta_total.enabled=true;s.channels.cancellations.enabled=true},
 (m,d)=>{const code=step(d,'move_class_code'),mv=step(d,'move_id'),r0=step(d,'len_r0'),r1=step(d,'len_r1');
  let bad=[];m.combined.forEach((v,k)=>{if(k===0)return;const c=code[k];let want=c===3?2:c===1?0:(mv[k]===2||mv[k]===3?r1[k-1]:r0[k-1]);if(v!==want)bad.push([k,v,want])});
  return {text:`combined=${JSON.stringify(m.combined)}; mismatches=${JSON.stringify(bad)}`,verdict:bad.length?'refuted':'confirmed'}});
// T2: the same identity on the longest training run (159 moves)
trial('T2_identity_0384','same identity holds on every step of ms-train-0384 (I guessed this was the 159-move run; the ledger records the real step count)','ms-train-0384',
 s=>{s.channels.delta_total.enabled=true;s.channels.cancellations.enabled=true},
 (m,d)=>{const code=step(d,'move_class_code'),mv=step(d,'move_id'),r0=step(d,'len_r0'),r1=step(d,'len_r1');let bad=0;
  m.combined.forEach((v,k)=>{if(!k)return;const c=code[k];const want=c===3?2:c===1?0:(mv[k]===2||mv[k]===3?r1[k-1]:r0[k-1]);if(v!==want)bad++});
  return {text:`steps=${m.combined.length-1}, mismatches=${bad}`,verdict:bad?'refuted':'confirmed'}});
// T2b: the actual longest decoded training run (ms-train-0066, 159 moves, found by scanning decoded_runs.jsonl)
trial('T2b_identity_longest','same identity holds on all 159 steps of ms-train-0066, the true longest run','ms-train-0066',
 s=>{s.channels.delta_total.enabled=true;s.channels.cancellations.enabled=true},
 (m,d)=>{const code=step(d,'move_class_code'),mv=step(d,'move_id'),r0=step(d,'len_r0'),r1=step(d,'len_r1');let bad=0;
  m.combined.forEach((v,k)=>{if(!k)return;const c=code[k];const want=c===3?2:c===1?0:(mv[k]===2||mv[k]===3?r1[k-1]:r0[k-1]);if(v!==want)bad++});
  return {text:`steps=${m.combined.length-1}, mismatches=${bad}`,verdict:(bad||m.combined.length-1!==159)?'refuted':'confirmed'}});
// T3a: mixed units under source normalization — predict the mixer's unit guard refuses (letters vs 'letters (proxy)')
trial('T3a_unit_guard','total_length (letters) with dist_to_target (letters (proxy)) under source normalization is REFUSED by the unit guard; no mix is produced','ms-train-0160',
 s=>{s.channels.total_length.enabled=true;s.channels.dist_to_target.enabled=true;s.channels.dist_to_target.weight=-1},
 (m)=>({text:`mixer produced a mix: combined=${JSON.stringify(m.combined)}`,verdict:'refuted'}),'source',true);
// T3b: same pair under RMS normalization — combined is NOT zero (each channel is divided by its own RMS), but de-normalizing each trace (y*scale/weight) must recover the raw identity total-dist = 0 everywhere except the last step, where it equals the final total length (2)
trial('T3b_proxy_rms','under rms: combined != 0 on interior steps (scales differ), but y*scale/weight recovers raw values so total-dist = 0 except last step = 2','ms-train-0160',
 s=>{s.channels.total_length.enabled=true;s.channels.dist_to_target.enabled=true;s.channels.dist_to_target.weight=-1},
 (m)=>{const T=m.traces.find(t=>t.id==='total_length'),D=m.traces.find(t=>t.id==='dist_to_target');
  const raw=k=>T.y[k]*T.transforms.y.scale/T.weight-D.y[k]*D.transforms.y.scale/D.weight;
  const rawDiff=m.combined.map((_,k)=>+raw(k).toFixed(9));const interiorNonzero=m.combined.slice(0,-1).some(v=>Math.abs(v)>1e-9);
  const ok=interiorNonzero&&rawDiff.slice(0,-1).every(v=>v===0)&&rawDiff[rawDiff.length-1]===2;
  return {text:`combined=${JSON.stringify(m.combined.map(v=>+v.toFixed(4)))}; scales T=${T.transforms.y.scale.toFixed(4)} D=${D.transforms.y.scale.toFixed(4)}; de-normalized total-dist=${JSON.stringify(rawDiff)}`,verdict:ok?'confirmed':'refuted'}},'rms');
// T4: smoothing — predict that a 5-sample moving average of total_length on the longest run leaves a residual whose RMS is under 1 letter (plateaus dominate)
trial('T4_smoothing_residual','smoothing=5 on total_length of the longest run: residual RMS < 1.0 letter, because the path is mostly plateaus and 1-2 letter steps','ms-train-0384',
 s=>{s.channels.total_length.enabled=true;s.smoothing=5},
 (m)=>{const r=rms(m.residual);return {text:`rms(original)=${rms(m.original).toFixed(3)} rms(smoothed)=${rms(m.combined).toFixed(3)} rms(residual)=${r.toFixed(3)}`,verdict:r<1?'confirmed':'refuted'}});
// T5: shape view — route cancellations to X and delta_total to Y; predict every point lies on or above the line y = -x (no step loses more letters than it cancels)
trial('T5_shape_x_canc_y_delta','X=cancellations, Y=delta_total: every point satisfies y >= -x (a step cannot shrink by more than it cancelled)','ms-train-0384',
 s=>{s.channels.cancellations.enabled=true;s.channels.cancellations.route='x';s.channels.delta_total.enabled=true;s.channels.delta_total.route='y'},
 (m)=>{let viol=0;m.X.forEach((x,k)=>{if(m.Y[k]< -x)viol++});return {text:`points=${m.X.length}, y<-x violations=${viol}, max x=${Math.max(...m.X)}, min y=${Math.min(...m.Y)}`,verdict:viol?'refuted':'confirmed'}});
// T6: deliberately wrong prediction — carry source-unit arithmetic (1 - 2 = -1) into an RMS mix; RMS divides each constant channel by itself so both become 1 and the sum is 0
trial('T6_wrong_on_purpose','abelian_ok(+1) + n_generators(-1) under rms is -1 at every step (source-unit arithmetic: 1 - 2)','ms-train-0160',
 s=>{s.channels.abelian_ok.enabled=true;s.channels.n_generators.enabled=true;s.channels.n_generators.weight=-1},
 (m)=>{const ok=m.combined.every(v=>Math.abs(v+1)<1e-9);return {text:`combined=${JSON.stringify(m.combined)}; per-channel scales=${JSON.stringify(m.traces.map(t=>[t.id,t.transforms.y.scale]))}`,verdict:ok?'confirmed':'refuted'}},'rms');
fs.writeFileSync(path.join(OUT,'Compound_Eye_Intervention_Ledger_acc_decoder.json'),JSON.stringify(ledger,null,1));
console.log(`\nledger: ${ledger.trials.length} trials -> ${OUT}/Compound_Eye_Intervention_Ledger_acc_decoder.json`);
