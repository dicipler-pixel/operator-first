// mixer trials v4 — original training path vs finisher output, same run, on the frozen Eye Mixer
const fs=require('fs'),path=require('path');const ROOT=path.resolve(__dirname,'..','..','..');
const E=require(path.join(ROOT,'tools/compound-eye/projects/eye_mixer/mixer_core.js'));const OUT=process.env.OUT_DIR||__dirname;
const ledger={schema:'compound-eye-intervention-ledger-v1',trials:[]};const V={confirmed:'matched',refuted:'failed',blocked:'ambiguous'};
const snap=m=>m?{activeCount:m.activeCount,rmsOriginal:m.rmsOriginal,rmsCombined:m.rmsCombined,rmsResidual:m.rmsResidual}:null;
const orig=id=>E.read(fs.readFileSync(path.join(ROOT,`tools/acc/decoded_v2/${id}__training__recipe.json`),'utf8')).dataset;
const fin=id=>E.read(fs.readFileSync(path.join(ROOT,`tools/acc/decoded_finished_v1/${id}__submission_training_424_finished.txt__recipe.json`),'utf8')).dataset;
const val=(d,id)=>d.traces.find(t=>t.id===id).values;
function mixWith(d,setup){const s=E.defaults(d);s.normalization='source';for(const c of Object.values(s.channels)){c.enabled=false;c.weight=1;c.route='both'}setup(s);return {s,m:E.mix(d,s)}}
function trial(name,prediction,run,setup,observe){
  const dO=orig(run),dF=fin(run);const o=mixWith(dO,setup),f=mixWith(dF,setup);const obs=observe(o.m,f.m,dO,dF);
  ledger.trials.push({createdUTC:new Date().toISOString(),dataset:`${dO.id} vs ${dF.id}`,datasetTitle:`${dO.title} | ${dF.title}`,prediction,before:{settings:E.copy(o.s),mix:snap(o.m)},
    observation:obs.text,verdict:V[obs.verdict],closedUTC:new Date().toISOString(),after:{settings:E.copy(f.s),mix:snap(f.m)},trial_name:name,harness_verdict:obs.verdict,recipe_file:`${name}_finished_recipe.json`,baseline_recipe_file:`${name}_original_recipe.json`});
  fs.writeFileSync(path.join(OUT,`${name}_original_recipe.json`),JSON.stringify(E.recipe(dO,o.s)));fs.writeFileSync(path.join(OUT,`${name}_finished_recipe.json`),JSON.stringify(E.recipe(dF,f.s)));
  console.log(`\n[${name}] ${run}\n  predict: ${prediction}\n  observe: ${obs.text}\n  verdict: ${obs.verdict} (${V[obs.verdict]})`);}
const entryOf=d=>{const r0=val(d,'len_r0'),r1=val(d,'len_r1');return r0.findIndex((a,k)=>(a===1)!==(r1[k]===1))};
// F1: length trace — finished 0333 is 8 moves shorter, never exceeds L_entry+2 after entry, and has fewer plateau steps
trial('F1_length_trace','ms-train-0333 finished: 15 moves (was 23), max length after corridor entry <= L_entry+2, fewer plateau steps than the original','ms-train-0333',
 s=>{s.channels.total_length.enabled=true},(mo,mf,dO,dF)=>{const e=entryOf(dF);const L=mf.combined[e];const mx=Math.max(...mf.combined.slice(e));
  const plat=c=>c.slice(1).filter((v,k)=>v===c[k]).length;const po=plat(mo.combined),pf=plat(mf.combined);
  return {text:`orig steps=${mo.combined.length-1} fin steps=${mf.combined.length-1}; entry=${e} L_entry=${L} max after entry=${mx}; plateaus orig=${po} fin=${pf}`,verdict:(mf.combined.length-1===15&&mx<=L+2&&pf<po)?'confirmed':'refuted'}});
// F2: churn — delta_total + cancellations (= operand letters added per step) summed over the tail is smaller in the finished path
trial('F2_less_churn','operand letters added over the corridor tail (sum of delta_total + cancellations after entry) is smaller in the finished path than in the original','ms-train-0333',
 s=>{s.channels.delta_total.enabled=true;s.channels.cancellations.enabled=true},(mo,mf,dO,dF)=>{const eo=entryOf(dO),ef=entryOf(dF);const so=mo.combined.slice(eo+1).reduce((a,b)=>a+b,0),sf=mf.combined.slice(ef+1).reduce((a,b)=>a+b,0);
  return {text:`operand letters over tail: orig=${so} (${mo.combined.length-1-eo} moves) fin=${sf} (${mf.combined.length-1-ef} moves)`,verdict:sf<so?'confirmed':'refuted'}});
// F3: shape — X=cancellations Y=delta_total: finished tail has fewer points at the origin (steps that neither cancel nor change length)
trial('F3_fewer_origin_points','in the shape view X=cancellations, Y=delta_total, the finished tail has fewer (0,0) points than the original tail','ms-train-0333',
 s=>{s.channels.cancellations.enabled=true;s.channels.cancellations.route='x';s.channels.delta_total.enabled=true;s.channels.delta_total.route='y'},
 (mo,mf,dO,dF)=>{const eo=entryOf(dO),ef=entryOf(dF);const z=(m,e)=>m.X.slice(e+1).filter((x,k)=>x===0&&m.Y[e+1+k]===0).length;const zo=z(mo,eo),zf=z(mf,ef);
  return {text:`(0,0) points in tail: orig=${zo} fin=${zf}`,verdict:zf<zo?'confirmed':'refuted'}});
// F4: genuine unknown — the finished tail of 0333 contains at most one inversion move
trial('F4_tail_inversions','the finished tail of ms-train-0333 contains at most one inversion (move_class_code 1)','ms-train-0333',
 s=>{s.channels.move_class_code.enabled=true},(mo,mf,dO,dF)=>{const eo=entryOf(dO),ef=entryOf(dF);const inv=(m,e)=>m.combined.slice(e+1).filter(v=>v===1).length;const io=inv(mo,eo),iff=inv(mf,ef);
  return {text:`inversions in tail: orig=${io} fin=${iff}; finished tail classes=${JSON.stringify(mf.combined.slice(ef+1))}`,verdict:iff<=1?'confirmed':'refuted'}});
fs.writeFileSync(path.join(OUT,'Compound_Eye_Intervention_Ledger_finished_vs_original.json'),JSON.stringify(ledger,null,1));console.log(`\nledger: ${ledger.trials.length} trials`);
