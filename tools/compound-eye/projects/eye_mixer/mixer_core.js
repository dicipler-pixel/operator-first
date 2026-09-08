/* Compound Eye Mixer 1.0. Pure, dependency-free functions for browser and Node.
   Imported samples remain immutable. Display transformations are recipe data. */
const EyeMixer = (()=>{
 'use strict';
 const colors=['#68e2d0','#ffcd78','#bda0ff','#79baff','#ff8fbd','#b1dc87','#ed9d70','#a9dce7'];
 const copy=x=>JSON.parse(JSON.stringify(x));
 const finite=x=>typeof x==='number'&&Number.isFinite(x);
 const fail=s=>{throw Error(s)};
 const rms=a=>{let v=a.filter(finite);return v.length?Math.sqrt(v.reduce((s,x)=>s+x*x,0)/v.length):null};
 function validate(d){
  if(!d||d.schema!=='compound-eye-traces-v1')fail('Use compound-eye-traces-v1, or import a CSV with x in its first column.');
  if(!d.context||!d.context.object_id||!d.context.model_id||!d.context.coordinate||!d.context.x_unit||!d.context.source_stage)fail('Declare the object, model, coordinate, coordinate unit and source stage.');
  if(!Array.isArray(d.x)||d.x.length<2||d.x.length>100000||!d.x.every(finite)||d.x.some((x,k)=>k&&x<=d.x[k-1]))fail('The common x coordinate must contain 2–100,000 strictly increasing finite samples.');
  if(!Array.isArray(d.traces)||!d.traces.length||d.traces.length>64)fail('Provide 1–64 trace channels.');
  const ids=new Set();
  for(const t of d.traces){
   if(!t.id||ids.has(t.id)||!t.label||!t.unit||!t.source)fail('Each trace needs a unique ID, label, unit and source.');ids.add(t.id);
   for(const a of [t.values,...(t.xValues?[t.xValues]:[])])if(!Array.isArray(a)||a.length!==d.x.length||!a.every(v=>v===null||finite(v)))fail('Trace lengths must match x. Use null for missing values, never padded zeroes.');
   if(t.harmonic&&(!finite(t.harmonic.amplitude)||!finite(t.harmonic.frequency)||!finite(t.harmonic.phase)))fail('Harmonic metadata must be finite.');
   if(t.color&&!/^#[0-9a-fA-F]{6}$/.test(t.color))fail('Trace colors must be six-digit hex colors.');
  }
  return d;
 }
 function noise(n,seed){let v=seed>>>0;return Array.from({length:n},()=>{v=(Math.imul(1664525,v)+1013904223)>>>0;return (v/4294967296-.5)*2})}
 function harmonicTrace(id,label,a,f,p,x,color){return {id,label,unit:'illustration amplitude',source:'Synthetic harmonic; no tidal station calibration',color,harmonic:{amplitude:a,frequency:f,phase:p},values:x.map(t=>a*Math.sin(2*Math.PI*f*t+p*Math.PI/180)),xValues:x.map(t=>a*Math.cos(2*Math.PI*f*t+p*Math.PI/180))}}
 function presets(){
  const x=Array.from({length:721},(_,i)=>i/720);
  const harmonic={schema:'compound-eye-traces-v1',id:'harmonic',title:'Harmonic studio',description:'An illustrative harmonic combiner inspired by tide-prediction machines. These are invented components, not a calibrated tide forecast.',context:{object_id:'harmonic_studio',model_id:'synthetic_harmonics',coordinate:'cycle',x_unit:'cycles',source_stage:'synthetic'},x,traces:[[.75,1,0],[.30,2,40],[.18,3,-80],[.10,5,20]].map((h,i)=>harmonicTrace('harmonic_'+i,['Main rhythm','Second rhythm','Third rhythm','Fine structure'][i],...h,x,colors[i]))};
  harmonic.traces.push({id:'synthetic_noise',label:'Synthetic noise',unit:'illustration amplitude',source:'Seeded uniform noise, seed 260907; illustrative',color:colors[4],values:noise(x.length,260907).map(v=>v*.17),xValues:noise(x.length,260908).map(v=>v*.17),defaultEnabled:false});
  const q=Array.from({length:601},(_,i)=>(i-300)/500),a=.7;
  const shape={schema:'compound-eye-traces-v1',id:'shape',title:'Shape wall',description:'Compatible outputs on one signed Jacobi path. Display normalization allows a visual comparison of different quantities; it is not a physical addition law.',context:{object_id:'signed_jacobi_path',model_id:'audited_shape_geometry',coordinate:'q',x_unit:'dimensionless q',source_stage:'theoretical'},x:q,traces:[
   {id:'signed_q',label:'Signed coordinate',unit:'signed coordinate',source:'Declared path coordinate',values:q,defaultRoute:'x'},
   {id:'det_X',label:'Orientation / determinant',unit:'normalized determinant',source:'ce.horizon.orientation@1.0.0 formula',values:q.map(v=>Math.sqrt(a*(1-a))*(1-v*v)*v),defaultRoute:'y'},
   {id:'w3',label:'Gram depth w₃',unit:'Gram eigenvalue',source:'ce.horizon.wall_path@1.0.0 formula',values:q.map(v=>v*v),defaultRoute:'y'},
   {id:'length',label:'Length to the wall',unit:'quotient path length',source:'ce.horizon.wall_path@1.0.0 arcsine formula',values:q.map(v=>Math.asin(Math.abs(v))),defaultRoute:'y',defaultEnabled:false},
   {id:'metric',label:'Lift metric gqq',unit:'metric component',source:'ce.horizon.wall_path@1.0.0 formula',values:q.map(v=>1/(1-v*v)),defaultRoute:'y',defaultEnabled:false}]};
  const time=Array.from({length:401},(_,i)=>i/100);
  const hidden={schema:'compound-eye-traces-v1',id:'hidden',title:'Hidden interiors',description:'Two different hidden states and rates, with the same exterior signal. Opposite weights cancel the shared outside signal while exposing a local inside difference.',context:{object_id:'one_way_candidates',model_id:'finite_linear_candidates',coordinate:'time',x_unit:'dimensionless time',source_stage:'theoretical'},x:time,traces:[
   {id:'outside_a',label:'Outside · model A',unit:'state amplitude',source:'x₁(t)=exp(-t), hidden b=2, x₂(0)=0',values:time.map(t=>Math.exp(-t)),defaultRoute:'x'},
   {id:'outside_b',label:'Outside · model B',unit:'state amplitude',source:'x₁(t)=exp(-t), hidden b=3, x₂(0)=1',values:time.map(t=>Math.exp(-t)),defaultRoute:'x',defaultWeight:-1},
   {id:'inside_a',label:'Inside · model A',unit:'state amplitude',source:'Local x₂(t)=0.3(exp(-t)-exp(-2t)); not outside telemetry',values:time.map(t=>.3*(Math.exp(-t)-Math.exp(-2*t))),defaultRoute:'y'},
   {id:'inside_b',label:'Inside · model B',unit:'state amplitude',source:'Local x₂(t)=exp(-3t)+0.15(exp(-t)-exp(-3t)); not outside telemetry',values:time.map(t=>Math.exp(-3*t)+.15*(Math.exp(-t)-Math.exp(-3*t))),defaultRoute:'y',defaultWeight:-1}]};
  const sun={schema:'compound-eye-traces-v1',id:'sun',title:'Sun shear scan',description:'Seven source-script samples at the stated tilt angles. Connecting lines aid reading; they are not added observations. The resolvent values sample the positive real axis.',context:{object_id:'sun_shear_lane_scan',model_id:'shear_lane_01_fixed_k',coordinate:'field tilt',x_unit:'degrees',source_stage:'theoretical'},x:[35,40,45,50,60,75,90],traces:[
   {id:'gain',label:'Sampled energy gain',unit:'gain ratio',source:'SHEAR-LANE-01 source replay, rounded printed output',values:[8.8,5.0,3.9,3.2,2.6,2.4,2.3],defaultRoute:'y'},
   {id:'kreiss',label:'Sampled resolvent bound',unit:'resolvent diagnostic',source:'SHEAR-LANE-01: finite positive-real samples, not full supremum',values:[1.80,1.39,1.26,1.19,1.13,1.10,1.08],defaultRoute:'y'},
   {id:'phi',label:'Commutator magnitude',unit:'generator commutator',source:'SHEAR-LANE-01: unnormalized Frobenius norm',values:[.90,.99,1.08,1.16,1.30,1.44,1.48],defaultRoute:'x'}]};
  return [harmonic,shape,hidden,sun].map((d)=>{d.traces.forEach((t,i)=>{t.color=t.color||colors[i%colors.length]});return validate(d)});
 }
 function defaults(d){return {normalization:['shape','sun'].includes(d.id)?'rms':'source',center:false,smoothing:1,view:'shape',showComponents:true,showOriginal:true,scale:1,cursor:0,channels:Object.fromEntries(d.traces.map(t=>[t.id,{enabled:t.defaultEnabled!==false,weight:t.defaultWeight??1,route:t.defaultRoute||'both',frequency:t.harmonic?.frequency??0,phase:t.harmonic?.phase??0}]))}}
 function smooth(v,width){
  width=Math.max(1,Math.min(101,Math.round(width)));if(width%2===0)width++;const h=(width-1)/2;
  return v.map((x,i)=>{if(x===null)return null;let sum=x,n=1;for(const dir of [-1,1])for(let j=1;j<=h;j++){let k=i+dir*j;if(k<0||k>=v.length||v[k]===null)break;sum+=v[k];n++}return sum/n});
 }
 function mix(d,settings){
  validate(d);const s={...defaults(d),...settings},active=d.traces.filter(t=>s.channels[t.id]?.enabled);
  if(!['source','rms'].includes(s.normalization))fail('Unknown normalization.');
  if(!Number.isInteger(s.smoothing)||s.smoothing<1||s.smoothing>101||s.smoothing%2!==1||!finite(s.scale)||s.scale<=0||s.scale>20||!['shape','trace'].includes(s.view))fail('Use an odd 1–101 sample window, a positive zoom up to 20, and a shape/trace view.');
  const units=[...new Set(active.map(t=>t.unit))];
  if(s.normalization==='source'&&units.length>1)fail('These channels have different units. Choose display RMS normalization, or select matching units.');
  let traces=active.map(t=>{
   let c=s.channels[t.id];if(!finite(c.weight)||Math.abs(c.weight)>100||!['x','y','both'].includes(c.route))fail('Channel weights must be finite, within ±100, with an X/Y route.');
   let v=t.values.slice(),x=t.xValues?t.xValues.slice():v.slice();
   if(t.harmonic){if(!finite(c.frequency)||!finite(c.phase)||Math.abs(c.frequency)>10000||Math.abs(c.phase)>360000)fail('Invalid harmonic frequency or phase.');v=d.x.map(z=>t.harmonic.amplitude*Math.sin(2*Math.PI*c.frequency*z+c.phase*Math.PI/180));x=d.x.map(z=>t.harmonic.amplitude*Math.cos(2*Math.PI*c.frequency*z+c.phase*Math.PI/180));}
   function transform(a){let f=a.filter(finite),mean=s.center&&f.length?f.reduce((q,z)=>q+z,0)/f.length:0,shift=a.map(z=>z===null?null:z-mean),scale=s.normalization==='rms'?(rms(shift)||1):1;return {mean,scale,v:shift.map(z=>z===null?null:c.weight*z/scale)}}
   let ty=transform(v),tx=transform(x);
   return {id:t.id,label:t.label,color:t.color||colors[0],route:c.route,weight:c.weight,unit:t.unit,x:tx.v,y:ty.v,transforms:{x:{offset:tx.mean,scale:tx.scale},y:{offset:ty.mean,scale:ty.scale}}};
  });
  const sum=(axis,routeOnly)=>d.x.map((_,k)=>{let n=0;for(const t of traces){if(routeOnly&&t.route!==axis&&t.route!=='both')continue;let z=t[axis][k];if(z===null)return null;n+=z}return n});
  const original=sum('y',false),rawX=sum('x',true),rawY=sum('y',true),combined=smooth(original,s.smoothing),X=smooth(rawX,s.smoothing),Y=smooth(rawY,s.smoothing);
  const residual=original.map((v,k)=>v===null||combined[k]===null?null:v-combined[k]);
  return {coordinate:d.x.slice(),traces,original,combined,rawX,rawY,X,Y,residual,unit:s.normalization==='source'?(units[0]||d.traces[0].unit):'display units (per-channel RMS)',activeCount:traces.length,rmsOriginal:rms(original),rmsCombined:rms(combined),rmsResidual:rms(residual),missing:combined.filter(v=>v===null).length,normalization:s.normalization,smoothing:s.smoothing};
 }
 function csvRows(text){
  const rows=[];let row=[],field='',quote=false;
  for(let k=0;k<text.length;k++){const c=text[k];if(c==='"'){if(quote&&text[k+1]==='"'){field+='"';k++}else quote=!quote}else if(c===','&&!quote){row.push(field);field=''}else if((c==='\n'||c==='\r')&&!quote){if(c==='\r'&&text[k+1]==='\n')k++;row.push(field);if(row.some(x=>x.trim()))rows.push(row);row=[];field=''}else field+=c}
  if(quote)fail('Unclosed CSV quotation.');row.push(field);if(row.some(x=>x.trim()))rows.push(row);return rows;
 }
 function fromCSV(text,metadata={}){
  const rows=csvRows(text.replace(/^\uFEFF/,''));if(rows.length<3||rows[0].length<2)fail('CSV needs a header, an x column, at least one trace, and two sample rows.');
  const head=rows.shift();if(rows.some(r=>r.length!==head.length))fail('Every CSV row must have the same column count.');
  const number=s=>s.trim()===''?null:(Number.isFinite(Number(s))?Number(s):fail('Non-numeric CSV value: '+s.slice(0,50)));
  const parse=s=>{let m=s.trim().match(/^(.*?)\s*\[([^\]]+)\]\s*$/);return m?{label:m[1].trim(),unit:m[2]}:{label:s.trim(),unit:metadata.y_unit||'user-declared units'}};
  const xhead=parse(head[0]),cols=head.slice(1).map(parse),values=rows.map(r=>r.map(number));
  return validate({schema:'compound-eye-traces-v1',id:'imported',title:metadata.title||'Imported eye traces',description:'User-supplied common-coordinate traces. Imported numbers are preserved; missing entries remain gaps.',context:{object_id:metadata.object_id||'user_supplied_object',model_id:metadata.model_id||'user_supplied_model',coordinate:xhead.label,x_unit:/\[/.test(head[0])?xhead.unit:'user-declared coordinate units',source_stage:metadata.source_stage||'user_supplied_unclassified'},x:values.map(r=>r[0]),traces:cols.map((h,k)=>({id:'import_'+k,label:h.label,unit:h.unit,source:'User-imported CSV; provenance must be assessed separately',color:colors[k%colors.length],values:values.map(r=>r[k+1]),defaultRoute:k===0?'x':'y'}))});
 }
 function read(text){let x=text.trim();if(x.startsWith('{')){let o=JSON.parse(x);if(o.schema==='compound-eye-mixer-recipe-v1'){validate(o.dataset);mix(o.dataset,o.settings);if(o.baseline){validate(o.baseline.dataset);mix(o.baseline.dataset,o.baseline.settings);if(JSON.stringify(o.baseline.dataset.x)!==JSON.stringify(o.dataset.x)||JSON.stringify(o.baseline.dataset.context)!==JSON.stringify(o.dataset.context))fail('Baseline and current recipe must share the same declared context and coordinate.');}return {dataset:o.dataset,settings:o.settings,baseline:o.baseline||null}}return {dataset:validate(o)}}return {dataset:fromCSV(text)}}
 function recipe(d,s,baseline=null){mix(d,s);return {schema:'compound-eye-mixer-recipe-v1',engine_version:'1.0.0',dataset:copy(d),settings:copy(s),baseline:baseline?copy(baseline):null,meaning:'A reproducible visual composition; weights, centering and smoothing are chosen display operations, not automatically physical laws.'}}
 function csv(d,s){let m=mix(d,s);return 'x,original_sum,display_sum,x_shape,y_shape,removed_residual\n'+d.x.map((x,k)=>[x,m.original[k],m.combined[k],m.X[k],m.Y[k],m.residual[k]].map(v=>v===null?'':String(v)).join(',')).join('\n')+'\n'}
 return {copy,finite,rms,validate,presets,defaults,mix,smooth,fromCSV,read,recipe,csv,colors,harmonicTrace};
})();
if(typeof module!=='undefined')module.exports=EyeMixer;
