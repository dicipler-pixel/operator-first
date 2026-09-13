// mixer trials v3 — touch / taste / smell channels on the frozen Eye Mixer; predict -> intervene -> observe -> record -> replay
const fs=require('fs'),path=require('path');const ROOT=path.resolve(__dirname,'..','..','..');
const E=require(path.join(ROOT,'tools/compound-eye/projects/eye_mixer/mixer_core.js'));const OUT=process.env.OUT_DIR||__dirname;
const ledger={schema:'compound-eye-intervention-ledger-v1',trials:[]};const V={confirmed:'matched',refuted:'failed',blocked:'ambiguous'};
const snap=m=>m?{activeCount:m.activeCount,rmsOriginal:m.rmsOriginal,rmsCombined:m.rmsCombined,rmsResidual:m.rmsResidual}:null;
const load=id=>E.read(fs.readFileSync(path.join(ROOT,`tools/acc/senses_v1/recipes/${id}__training__senses_recipe.json`),'utf8'));
const step=(d,id)=>d.traces.find(t=>t.id===id).values;
function trial(name,prediction,run,setup,observe,norm='source',expectRefusal=false){
  const {dataset:d}=load(run);const s=E.defaults(d);s.normalization=norm;for(const c of Object.values(s.channels)){c.enabled=false;c.weight=1;c.route='both'}
  const before={settings:E.copy(s),mix:null};setup(s);let m=null,obs;
  try{m=E.mix(d,s)}catch(e){obs={text:`mixer refused: ${e.message}`,verdict:expectRefusal?'confirmed':'blocked'}}
  if(!obs)obs=observe(m,d,s);
  ledger.trials.push({createdUTC:new Date().toISOString(),dataset:d.id,datasetTitle:d.title,prediction,before,observation:obs.text,verdict:V[obs.verdict],closedUTC:new Date().toISOString(),after:{settings:E.copy(s),mix:snap(m)},trial_name:name,harness_verdict:obs.verdict,recipe_file:m?`${name}_recipe.json`:null});
  if(m)fs.writeFileSync(path.join(OUT,`${name}_recipe.json`),JSON.stringify(E.recipe(d,s)));
  console.log(`\n[${name}] ${run}\n  predict: ${prediction}\n  observe: ${obs.text}\n  verdict: ${obs.verdict} (${V[obs.verdict]})`);}
const thirds=(c)=>{const n=c.length-1,t=[[0,0],[0,0],[0,0]];c.forEach((v,k)=>{if(!k)return;const i=Math.min(2,Math.floor(3*k/n));t[i][0]+=v;t[i][1]++});return t.map(([s,c])=>+(s/c).toFixed(3))};
// SMELL: what lingers — the leaky cancellation trace peaks in the last third of the 159-move run (multiplies dominate the end)
trial('M1_smell_canc_last_third','smell_linger_canc (decay 0.7) mean is highest in the last third of ms-train-0066','ms-train-0066',
 s=>{s.channels.smell_linger_canc.enabled=true},m=>{const t=thirds(m.combined);return {text:`mean linger by third=${JSON.stringify(t)}, peak step=${m.combined.indexOf(Math.max(...m.combined))}`,verdict:(t[2]>t[0]&&t[2]>t[1])?'confirmed':'refuted'}});
// SMELL vs SIGHT: smoothing=5 on cancellations is NOT the same as the leaky smell trace: residual of (smell - 5-avg) has RMS > 1 letter
trial('M2_smell_is_not_smoothing','smell_linger_canc(+1) with cancellations(-1) under source normalization is refused (units differ: lingering units vs letters)','ms-train-0066',
 s=>{s.channels.smell_linger_canc.enabled=true;s.channels.cancellations.enabled=true;s.channels.cancellations.weight=-1},m=>({text:`mixed ok: ${m.combined.length}`,verdict:'refuted'}),'source',true);
// TOUCH: growth happens only when nothing descends — predict touch_pressure == 0 before EVERY growth step of ms-train-0342 (pooled: 765/809 growth steps had zero pressure; 0342 step 45 is one of the 44 exceptions)
trial('T1_touch_forced_growth','on ms-train-0342, touch_pressure is 0 on the state before every growth step (growth only happens when no move descends); step 45 is the pooled Snell disagreement, where a flat move 13 existed but the +2 move 12 was taken','ms-train-0342',
 s=>{s.channels.touch_pressure.enabled=true},(m,d)=>{const dl=step(d,'delta_total');const bad=[];dl.forEach((v,k)=>{if(k&&v>0&&m.combined[k-1]>0)bad.push([k,m.combined[k-1]])});
  return {text:`growth steps=${dl.filter((v,k)=>k&&v>0).length}, growth with a descending move available=${JSON.stringify(bad)}`,verdict:bad.length===0?'confirmed':'refuted'}});
// TASTE: chemistry stays balanced — x_fraction of all letters within [0.3,0.7] on >= 90% of steps of the longest run
trial('S1_taste_balanced','taste_x_fraction in [0.3,0.7] on >= 90% of steps of ms-train-0066','ms-train-0066',
 s=>{s.channels.taste_x_fraction.enabled=true},m=>{const ok=m.combined.filter(v=>v>=0.3&&v<=0.7).length;return {text:`in-band ${ok}/${m.combined.length} (${(100*ok/m.combined.length).toFixed(1)}%), min=${Math.min(...m.combined).toFixed(3)} max=${Math.max(...m.combined).toFixed(3)}`,verdict:ok/m.combined.length>=0.9?'confirmed':'refuted'}});
// TASTE shape: X = alternation of r0, Y = alternation of r1 — predict the final state sits at (0,0) and the start at (>0,>0)
trial('S2_taste_alternation_shape','X=taste_alt_r0, Y=taste_alt_r1 on ms-train-0066: last point (0,0), first point both > 0.5','ms-train-0066',
 s=>{s.channels.taste_alt_r0.enabled=true;s.channels.taste_alt_r0.route='x';s.channels.taste_alt_r1.enabled=true;s.channels.taste_alt_r1.route='y'},
 m=>{const n=m.X.length-1;return {text:`first=(${m.X[0].toFixed(3)},${m.Y[0].toFixed(3)}) last=(${m.X[n]},${m.Y[n]})`,verdict:(m.X[n]===0&&m.Y[n]===0&&m.X[0]>0.5&&m.Y[0]>0.5)?'confirmed':'refuted'}});
fs.writeFileSync(path.join(OUT,'Compound_Eye_Intervention_Ledger_senses.json'),JSON.stringify(ledger,null,1));console.log(`\nledger: ${ledger.trials.length} trials`);
