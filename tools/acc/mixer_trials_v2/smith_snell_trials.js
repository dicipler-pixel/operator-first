// mixer trials v2 — Smith chart + Snell law, predict -> intervene -> observe -> record -> replay
// Instrument: frozen mixer_core.js (tools/compound-eye is not modified). Inputs: tools/acc/smith_snell_v1/recipes/*.json
const fs=require('fs'),path=require('path');
const ROOT=path.resolve(__dirname,'..','..','..');
const E=require(path.join(ROOT,'tools/compound-eye/projects/eye_mixer/mixer_core.js'));
const OUT=process.env.OUT_DIR||__dirname;
const ledger={schema:'compound-eye-intervention-ledger-v1',trials:[]};
const V={confirmed:'matched',refuted:'failed',blocked:'ambiguous',partial:'partial'};
const snap=m=>m?{activeCount:m.activeCount,rmsOriginal:m.rmsOriginal,rmsCombined:m.rmsCombined,rmsResidual:m.rmsResidual}:null;
const load=id=>E.read(fs.readFileSync(path.join(ROOT,`tools/acc/smith_snell_v1/recipes/${id}__training__smith_recipe.json`),'utf8'));
const step=(d,id)=>d.traces.find(t=>t.id===id).values;
function trial(name,prediction,run,setup,observe,norm='source',expectRefusal=false){
  const {dataset:d}=load(run); const s=E.defaults(d); s.normalization=norm;
  for(const c of Object.values(s.channels)){c.enabled=false;c.weight=1;c.route='both'}
  const before={settings:E.copy(s),mix:null}; setup(s); let m=null,obs;
  try{m=E.mix(d,s)}catch(e){obs={text:`mixer refused: ${e.message}`,verdict:expectRefusal?'confirmed':'blocked'}}
  if(!obs)obs=observe(m,d,s);
  ledger.trials.push({createdUTC:new Date().toISOString(),dataset:d.id,datasetTitle:d.title,prediction,before,observation:obs.text,verdict:V[obs.verdict],
    closedUTC:new Date().toISOString(),after:{settings:E.copy(s),mix:snap(m)},trial_name:name,harness_verdict:obs.verdict,recipe_file:m?`${name}_recipe.json`:null});
  if(m)fs.writeFileSync(path.join(OUT,`${name}_recipe.json`),JSON.stringify(E.recipe(d,s)));
  console.log(`\n[${name}] ${run}\n  predict: ${prediction}\n  observe: ${obs.text}\n  verdict: ${obs.verdict} (${V[obs.verdict]})`);
}
// S0 control: Grok's Map A table for ms-train-0160
trial('S0_mapA_control','gammaA on ms-train-0160 equals Grok Map A table: [0, 0, -5/19, -1/6, -1/4, 0, -1/5, 0]','ms-train-0160',
 s=>{s.channels.gammaA.enabled=true},
 m=>{const want=[0,0,-5/19,-1/6,-0.25,0,-0.2,0];const bad=m.combined.map((v,k)=>Math.abs(v-want[k])>1e-12?k:null).filter(x=>x!==null);
  return {text:`combined=${JSON.stringify(m.combined.map(v=>+v.toFixed(6)))}; mismatches=${JSON.stringify(bad)}`,verdict:bad.length?'refuted':'confirmed'}});
// S1: Smith disk, shape view X=Re Y=Im of the taken layer, longest run: every point inside the unit disk; Im=0 exactly when the pair is symmetric (d+ = d-)
trial('S1_smith_disk','X=smith_re, Y=smith_im on the 159-move run: max radius < 1, and Im==0 exactly on steps where the taken layer had p==0 (d+ == d-) or no layer','ms-train-0066',
 s=>{s.channels.smith_re.enabled=true;s.channels.smith_re.route='x';s.channels.smith_im.enabled=true;s.channels.smith_im.route='y'},
 (m,d)=>{const r=m.X.map((x,k)=>Math.hypot(x,m.Y[k]));const tl=step(d,'taken_layer');let bad=0;
  m.Y.forEach((y,k)=>{const li=tl[k];const p=li<0?0:step(d,`L${li}_p`)[k];if((y===0)!==(p===0))bad++});
  return {text:`points=${m.X.length}, max|Gamma|=${Math.max(...r).toFixed(4)}, Im==0<->p==0 mismatches=${bad}, Im==0 count=${m.Y.filter(y=>y===0).length}`,verdict:(Math.max(...r)<1&&!bad)?'confirmed':'refuted'}});
// S2: Grok's Map A finding — the real-axis embedding occupies almost nothing: distinct gammaA values on the longest run <= 12 (Grok: 12 cells of 40 pooled over 424 runs)
trial('S2_mapA_sparse','gammaA (X) with smith_im (Y): distinct rounded-to-0.05 gammaA values on the 159-move run <= 12, i.e. Map A is a sparse real-axis line','ms-train-0066',
 s=>{s.channels.gammaA.enabled=true;s.channels.gammaA.route='x';s.channels.smith_im.enabled=true;s.channels.smith_im.route='y'},
 m=>{const cells=new Set(m.X.map(x=>Math.floor((x+1)*20)));return {text:`distinct gammaA cells (width 0.05)=${cells.size}; gammaA range [${Math.min(...m.X).toFixed(3)}, ${Math.max(...m.X).toFixed(3)}]`,verdict:cells.size<=12?'confirmed':'refuted'}});
// S3: stacked disks over run fraction — predict taken-layer |Gamma| rises monotonically first third < middle < last third (moves get more decisive near the end)
trial('S3_radius_by_third','smith_radius mean rises monotonically across run thirds on the 159-move run (first < middle < last)','ms-train-0066',
 s=>{s.channels.smith_radius.enabled=true},
 m=>{const n=m.combined.length-1;const th=[[0,0],[0,0],[0,0]];m.combined.forEach((v,k)=>{if(!k)return;const t=Math.min(2,Math.floor(3*(k/n)));th[t][0]+=v;th[t][1]++});
  const mean=th.map(([s,c])=>+(s/c).toFixed(4));return {text:`mean |Gamma| by third=${JSON.stringify(mean)}`,verdict:(mean[0]<mean[1]&&mean[1]<mean[2])?'confirmed':'refuted'}});
// N1: strict Snell law with n = total length, theta = arg Gamma of the taken layer: snell_in(+1)+snell_out(-1) within 0.5 on >= 90% of layer steps. Prediction: it FAILS (pooled 602/11193 = 5.4%)
trial('N1_snell_strict','strict Snell (L_prev sin theta_in = L sin theta_out) holds within 0.5 on >= 90% of layer steps of the 159-move run — I predict this FAILS','ms-train-0066',
 s=>{s.channels.snell_in.enabled=true;s.channels.snell_out.enabled=true;s.channels.snell_out.weight=-1},
 (m,d)=>{const tl=step(d,'taken_layer');let n=0,ok=0;m.combined.forEach((v,k)=>{if(tl[k]<0)return;n++;if(Math.abs(v)<0.5)ok++});
  return {text:`layer steps=${n}, |L_prev sin(in) - L sin(out)|<0.5 on ${ok} (${(100*ok/n).toFixed(1)}%)`,verdict:ok/n>=0.9?'confirmed':'refuted'}});
// N2: Snell as direction selection — the move taken agrees with sign(p) of its layer before the step on every decided step of the run holding the one pooled disagreement (ms-train-0342, step 45)
trial('N2_snell_direction','snell_sign_agree on ms-train-0342: exactly one 0 (step 45), all other layer steps 1','ms-train-0342',
 s=>{s.channels.snell_sign_agree.enabled=true},
 m=>{const zeros=m.combined.map((v,k)=>v===0?k:null).filter(x=>x!==null);const ones=m.combined.filter(v=>v===1).length;const und=m.combined.filter(v=>v===-1).length;
  return {text:`zeros at ${JSON.stringify(zeros)}, ones=${ones}, undecided(p==0 or inversion)=${und}`,verdict:(zeros.length===1&&zeros[0]===45)?'confirmed':'refuted'}});
// N3: that disagreement is a growth-before-shrink step: total_length(+1) shows step 45 grows by 2 (13->15) and the run is below 13 within 5 more steps
trial('N3_growth_then_shrink','on ms-train-0342 total_length goes 13->15 at step 45 (against the one-move lookahead) and is < 13 by step 50','ms-train-0342',
 s=>{s.channels.total_length.enabled=true},
 m=>{const c=m.combined;return {text:`L[44..52]=${JSON.stringify(c.slice(44,53))}`,verdict:(c[44]===13&&c[45]===15&&c[50]<13)?'confirmed':'refuted'}});
// N4: mixed units guard on the Snell pair under source? both are 'letters*sin' so it should MIX (control that N1 was not blocked by units): pairing snell_in with smith_angle (radians) must be refused
trial('N4_units_guard','snell_in (letters*sin) with smith_angle (radians) under source normalization is refused by the unit guard','ms-train-0066',
 s=>{s.channels.snell_in.enabled=true;s.channels.smith_angle.enabled=true},
 m=>({text:`mixed: combined length ${m.combined.length}`,verdict:'refuted'}),'source',true);
fs.writeFileSync(path.join(OUT,'Compound_Eye_Intervention_Ledger_smith_snell.json'),JSON.stringify(ledger,null,1));
console.log(`\nledger: ${ledger.trials.length} trials -> ${OUT}/Compound_Eye_Intervention_Ledger_smith_snell.json`);
