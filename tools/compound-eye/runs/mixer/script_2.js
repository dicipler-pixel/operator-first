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

/* One SVG renderer powers the live view and vector/image exports. */
const EyeMixerPlot=(()=>{
 const E=typeof EyeMixer!=='undefined'?EyeMixer:require('./mixer_core.js');
 const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const num=v=>Number.isFinite(v)?Number(v.toPrecision(4)).toString():'—';
 const extent=a=>a.reduce((m,v)=>E.finite(v)?Math.max(m,Math.abs(v)):m,0);
 function path(x,y,X,Y){let s='',open=false;for(let k=0;k<x.length;k++){if(!E.finite(x[k])||!E.finite(y[k])){open=false;continue}s+=(open?'L':'M')+X(x[k]).toFixed(2)+','+Y(y[k]).toFixed(2);open=true}return s}
 function svg(d,s,m,baseline=null){
  const W=1100,H=620,L=74,R=1058,T=100,B=458,idx=Math.max(0,Math.min(d.x.length-1,Math.round(s.cursor||0))),shape=s.view==='shape';
  let lines=[],max=1e-9,xmin=0,xmax=1,ymin=0,ymax=1;
  const add=(p,color,width=2,opacity=1,dash='')=>{if(p)lines.push(`<path d="${p}" fill="none" stroke="${color}" stroke-width="${width}" opacity="${opacity}" ${dash?'stroke-dasharray="'+dash+'"':''}/>`)};
  const text=(v,x,y,col='#a9bfd4',size=13,anchor='start')=>lines.push(`<text x="${x}" y="${y}" fill="${col}" font-family="system-ui,sans-serif" font-size="${size}" text-anchor="${anchor}">${esc(v)}</text>`);
  const dot=(x,y,col,r=5)=>lines.push(`<circle cx="${x}" cy="${y}" r="${r}" fill="${col}"/>`);
  if(shape){
   let vx=m.X.concat(m.rawX),vy=m.Y.concat(m.rawY);if(baseline){vx=vx.concat(baseline.X);vy=vy.concat(baseline.Y)}
   if(s.showComponents){let xx=0,yy=0;for(const c of m.traces){if(c.route!=='y')xx+=c.x[idx]||0;if(c.route!=='x')yy+=c.y[idx]||0;vx.push(xx);vy.push(yy)}}
   max=Math.max(.2,extent(vx),extent(vy))*1.13/(s.scale||1);
   const ratio=(R-L)/(B-T);ymin=-max;ymax=max;xmin=-max*ratio;xmax=max*ratio;
  }else{
   let vals=m.combined.concat(s.showOriginal?m.original:[]);if(s.showComponents)vals=vals.concat(...m.traces.map(t=>t.y));if(baseline)vals=vals.concat(baseline.combined);
   max=Math.max(.05,extent(vals))*1.16/(s.scale||1);xmin=d.x[0];xmax=d.x[d.x.length-1];ymin=-max;ymax=max;
  }
  const X=x=>L+(x-xmin)/(xmax-xmin)*(R-L),Y=y=>B-(y-ymin)/(ymax-ymin)*(B-T);
  lines.push(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(d.title)} combined ${shape?'X/Y shape':'signal'}"><defs><clipPath id="mixClip"><rect x="${L}" y="${T}" width="${R-L}" height="${B-T}"/></clipPath></defs><rect width="${W}" height="${H}" rx="16" fill="#081321"/>`);
  text(d.title+' · '+(shape?'combined X / Y shape':'combined signal'),36,37,'#f4dfba',22);
  text(m.activeCount+' active channels · '+m.unit,36,66,'#8fa8c2',13);
  text('COMPOUND EYE  /  MIXER',W-35,34,'#68e2d0',12,'end');
  for(let k=0;k<=4;k++){let xx=xmin+k*(xmax-xmin)/4,yy=ymin+k*(ymax-ymin)/4;add(`M${X(xx)},${T}V${B}`,'#1d3146',1);add(`M${L},${Y(yy)}H${R}`,'#1d3146',1);text(num(xx),X(xx),B+23,'#8199b1',11,'middle');text(num(yy),L-12,Y(yy)+4,'#8199b1',11,'end')}
  if(ymin<0&&ymax>0)add(`M${L},${Y(0)}H${R}`,'#36506a',1);
  if(xmin<0&&xmax>0)add(`M${X(0)},${T}V${B}`,'#36506a',1);
  lines.push('<g clip-path="url(#mixClip)">');
  if(baseline)add(shape?path(baseline.X,baseline.Y,X,Y):path(d.x,baseline.combined,X,Y),'#bda0ff',2,.85,'7 6');
  if(s.showOriginal&&m.smoothing>1)add(shape?path(m.rawX,m.rawY,X,Y):path(d.x,m.original,X,Y),'#87a2bc',1,.5);
  if(!shape&&s.showComponents)for(const c of m.traces)add(path(d.x,c.y,X,Y),c.color,1.5,.55);
  let combined=shape?path(m.X,m.Y,X,Y):path(d.x,m.combined,X,Y);add(combined,'#ffce78',9,.06);add(combined,'#ffce78',4,.12);add(combined,'#ffce78',2.2,.98);
  if(shape&&s.showComponents){let xx=0,yy=0;for(const c of m.traces){let dx=c.route==='y'?0:c.x[idx],dy=c.route==='x'?0:c.y[idx];if(dx===null||dy===null)continue;let nx=xx+dx,ny=yy+dy;add(`M${X(xx)},${Y(yy)}L${X(nx)},${Y(ny)}`,c.color,2,.85);dot(X(nx),Y(ny),c.color,3.5);xx=nx;yy=ny}}
  const px=shape?m.X[idx]:d.x[idx],py=shape?m.Y[idx]:m.combined[idx];if(E.finite(px)&&E.finite(py)){if(!shape)add(`M${X(px)},${T}V${B}`,'#68e2d0',1,.4);dot(X(px),Y(py),'#ffce78',6);dot(X(px),Y(py),'#fff2d7',2)}
  lines.push('</g>');
  text(shape?'X route · equal scale on both axes':d.context.coordinate+' ['+d.context.x_unit+']',(L+R)/2,B+49,'#a9bfd4',12,'middle');
  const ry=552,rmax=Math.max(.001,extent(m.residual));
  text('REMOVED DETAIL',L,523,'#ad9ace',10);text('RMS '+num(m.rmsResidual)+' · residual is not automatically noise',R,523,'#ad9ace',11,'end');
  add(`M${L},${ry}H${R}`,'#23364b',1);add(path(d.x,m.residual,x=>L+(x-d.x[0])/(d.x.at(-1)-d.x[0])*(R-L),y=>ry-y/rmax*18),'#bda0ff',1.2,.8);
  text((s.center?'Centered · ':'')+(s.normalization==='rms'?'Per-channel RMS scaling':'Source-unit sum')+' · smoothing '+m.smoothing+' samples · '+d.context.source_stage,36,596,'#829db8',11);
  text('x = '+num(d.x[idx])+(baseline?' · baseline dashed':''),R,596,'#68e2d0',11,'end');
  lines.push('</svg>');return lines.join('');
 }
 return {svg,esc,num};
})();
if(typeof module!=='undefined')module.exports=EyeMixerPlot;

(()=>{
 'use strict';
 const E=EyeMixer,P=EyeMixerPlot,$=id=>document.getElementById(id),presets=E.presets(),saved=new Map();
 let d=E.copy(presets[0]),s=E.defaults(d),baseline=null,m=null,timer=null,solo=null;
 const fmt=P.num,esc=P.esc;
 for(const x of presets){const o=document.createElement('option');o.value=x.id;o.textContent=x.title;$('mixDataset').append(o)}
 function controls(){
  $('mixNormalization').value=s.normalization;$('mixView').value=s.view;$('mixSmoothing').value=s.smoothing;$('mixZoom').value=s.scale;
  $('mixComponents').checked=s.showComponents;$('mixOriginal').checked=s.showOriginal;$('mixCenter').checked=s.center;
  $('mixCursor').max=d.x.length-1;$('mixCursor').value=s.cursor||0;$('mixDescription').textContent=d.description;
  $('mixAdd').hidden=d.id!=='harmonic';$('mixClearPin').disabled=!baseline;
  $('mixChannels').innerHTML=d.traces.map(t=>{let c=s.channels[t.id];return `<div class="mixchannel ${c.enabled?'':'disabled'}" style="--channel-color:${t.color||E.colors[0]}" data-id="${esc(t.id)}"><div class="mixchannelhead"><label style="color:${t.color||E.colors[0]}"><input type="checkbox" data-control="enabled" ${c.enabled?'checked':''}>${esc(t.label)}</label><button data-control="solo">Solo</button></div><label>Weight <output>${fmt(c.weight)}</output><input type="range" data-control="weight" min="-3" max="3" step=".01" value="${c.weight}"></label><div class="mixroute">Shape route <select data-control="route"><option value="x" ${c.route==='x'?'selected':''}>X only</option><option value="y" ${c.route==='y'?'selected':''}>Y only</option><option value="both" ${c.route==='both'?'selected':''}>X + Y</option></select></div>${t.harmonic?`<div class="mixharmonic"><label>Cycles per x unit<input type="number" data-control="frequency" min="-20" max="20" step=".25" value="${c.frequency}"></label><label>Phase °<input type="number" data-control="phase" min="-360" max="360" step="5" value="${c.phase}"></label></div>`:''}</div>`}).join('');
 }
 function fail(error){$('mixError').hidden=false;$('mixError').textContent=error.message||String(error);m=null;$('mixGraphic').innerHTML='<p style="padding:35px;color:#ffd0ce">'+esc(error.message||error)+'</p>';['mixPNG','mixSVG','mixCSV','mixRecipe','mixPin'].forEach(id=>$(id).disabled=true)}
 function draw(recompute=true){
  try{
   if(recompute||!m)m=E.mix(d,s);
   let bm=baseline?E.mix(baseline.dataset,baseline.settings):null,mismatch=bm&&bm.unit!==m.unit;
   $('mixError').hidden=!mismatch;$('mixError').textContent=mismatch?'The pinned comparison uses another scale convention. It is hidden until the conventions match.':'';
   if(mismatch)bm=null;
   $('mixGraphic').innerHTML=P.svg(d,s,m,bm);$('mixCursorValue').textContent=fmt(d.x[s.cursor||0])+' '+d.context.x_unit;
   $('mixSmoothValue').textContent=s.smoothing+(s.smoothing===1?' sample':' samples');$('mixZoomValue').textContent=s.scale+'×';
   $('mixStats').innerHTML=`<span><b>${m.activeCount}</b> active / ${d.traces.length} available traces</span><span>Original RMS <b>${fmt(m.rmsOriginal)}</b></span><span>Displayed RMS <b>${fmt(m.rmsCombined)}</b></span><span>Gaps <b>${m.missing}</b></span>`;
   $('mixProvenance').innerHTML=`<p><b>${esc(d.context.object_id)}</b> · ${esc(d.context.model_id)}<br>${esc(d.context.source_stage)} · ${esc(d.context.coordinate)} [${esc(d.context.x_unit)}]</p><p>Signal = ${m.traces.map(t=>fmt(t.weight)+' × '+esc(t.label)).join(' + ')||'0 (no active channel)'}</p>`+m.traces.map(t=>{let original=d.traces.find(x=>x.id===t.id);return `<p style="border-left:2px solid ${t.color};padding-left:10px">${esc(t.label)} [${esc(t.unit)}] → ${esc(t.route)}<br>${esc(original.source)}<br>Y offset ${fmt(t.transforms.y.offset)} · Y scale ${fmt(t.transforms.y.scale)}</p>`}).join('');
   ['mixPNG','mixSVG','mixCSV','mixRecipe','mixPin'].forEach(id=>$(id).disabled=false);
  }catch(e){fail(e)}
 }
 function stop(){if(timer)cancelAnimationFrame(timer);timer=null;$('mixPlay').textContent='▶ Play'}
 function load(dataset,settings=null,pin=null){stop();d=E.copy(E.validate(dataset));s=settings?E.copy(settings):E.defaults(d);s.cursor=Math.max(0,Math.min(d.x.length-1,Math.round(s.cursor||0)));baseline=pin;solo=null;controls();draw()}
 $('mixDataset').onchange=()=>{saved.set(d.id,{dataset:E.copy(d),settings:E.copy(s),baseline:E.copy(baseline)});let v=saved.get($('mixDataset').value);if(v)load(v.dataset,v.settings,v.baseline);else load(presets.find(p=>p.id===$('mixDataset').value))};
 $('mixChannels').addEventListener('input',e=>{
  const box=e.target.closest('.mixchannel');if(!box)return;const id=box.dataset.id,c=s.channels[id],kind=e.target.dataset.control;
  if(kind==='enabled'){c.enabled=e.target.checked;box.classList.toggle('disabled',!c.enabled)}
  else if(kind==='route')c.route=e.target.value;
  else if(['weight','frequency','phase'].includes(kind)){c[kind]=Number(e.target.value);if(kind==='weight')box.querySelector('output').textContent=fmt(c.weight)}
  solo=null;draw();
 });
 $('mixChannels').addEventListener('click',e=>{if(e.target.dataset.control!=='solo')return;let id=e.target.closest('.mixchannel').dataset.id;if(solo&&solo.id===id){for(const [k,v]of Object.entries(solo.enabled))s.channels[k].enabled=v;solo=null}else{solo={id,enabled:Object.fromEntries(Object.entries(s.channels).map(([k,v])=>[k,v.enabled]))};Object.entries(s.channels).forEach(([k,v])=>v.enabled=k===id)}controls();draw()});
 for(const [id,key]of [['mixView','view'],['mixNormalization','normalization']])$(id).onchange=()=>{s[key]=$(id).value;draw()};
 for(const [id,key]of [['mixComponents','showComponents'],['mixOriginal','showOriginal'],['mixCenter','center']])$(id).onchange=()=>{s[key]=$(id).checked;draw()};
 for(const [id,key]of [['mixSmoothing','smoothing'],['mixZoom','scale']])$(id).oninput=()=>{s[key]=Number($(id).value);draw()};
 $('mixCursor').oninput=()=>{s.cursor=Number($('mixCursor').value);draw(false)};
 $('mixAll').onclick=()=>{Object.values(s.channels).forEach(c=>c.enabled=true);solo=null;controls();draw()};
 $('mixNone').onclick=()=>{Object.values(s.channels).forEach(c=>c.enabled=false);solo=null;controls();draw()};
 $('mixReset').onclick=()=>load(d);
 $('mixPin').onclick=()=>{baseline={dataset:E.copy(d),settings:E.copy(s)};$('mixClearPin').disabled=false;draw()};
 $('mixClearPin').onclick=()=>{baseline=null;$('mixClearPin').disabled=true;draw()};
 $('mixAdd').onclick=()=>{if(d.traces.length>=64)return fail(Error('This mixer supports 64 channels per study.'));let id='harmonic_added_'+d.traces.length,t=E.harmonicTrace(id,'Added rhythm '+d.traces.length,.1,d.traces.length+1,0,d.x,E.colors[d.traces.length%E.colors.length]);d.traces.push(t);s.channels[id]=E.defaults(d).channels[id];controls();draw()};
 $('mixPlay').onclick=()=>{if(timer)return stop();let last=0;const frame=t=>{if(!timer)return;if(t-last>40){s.cursor=(Number(s.cursor||0)+Math.max(1,Math.round(d.x.length/450)))%d.x.length;$('mixCursor').value=s.cursor;draw(false);last=t}timer=requestAnimationFrame(frame)};timer=requestAnimationFrame(frame);$('mixPlay').textContent='Ⅱ Pause'};
 // Pause hidden animation when another instrument panel is selected.
 document.querySelectorAll('[data-tab]').forEach(b=>b.addEventListener('click',()=>{if(b.dataset.tab!=='mixer')stop()}));
 $('mixFullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await $('mixer').requestFullscreen()}catch(e){$('mixError').hidden=false;$('mixError').textContent='Full screen is unavailable here. Open the standalone HTML in your browser.'}};
 function download(data,name,type){let blob=new Blob([data],{type}),u=URL.createObjectURL(blob),a=document.createElement('a');a.href=u;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),2000)}
 function exporting(fn){try{if(!m)throw Error('Resolve the current composition before exporting.');fn()}catch(e){$('mixError').hidden=false;$('mixError').textContent=e.message}}
 const name=()=>('Compound_Eye_'+d.id).replace(/[^a-zA-Z0-9_-]/g,'_');
 $('mixSVG').onclick=()=>exporting(()=>download($('mixGraphic').querySelector('svg').outerHTML,name()+'.svg','image/svg+xml'));
 $('mixPNG').onclick=()=>exporting(()=>{const svg=$('mixGraphic').querySelector('svg').outerHTML,blob=new Blob([svg],{type:'image/svg+xml'}),u=URL.createObjectURL(blob),im=new Image();im.onload=()=>{const c=document.createElement('canvas');c.width=2200;c.height=1240;c.getContext('2d').drawImage(im,0,0,c.width,c.height);c.toBlob(b=>{if(b)download(b,name()+'.png','image/png');URL.revokeObjectURL(u)},'image/png')};im.onerror=()=>{URL.revokeObjectURL(u);$('mixError').hidden=false;$('mixError').textContent='PNG export is unavailable in this preview. Use Save SVG or open the HTML in your browser.'};im.src=u});
 $('mixCSV').onclick=()=>exporting(()=>download(E.csv(d,s),name()+'_combined.csv','text/csv'));
 $('mixRecipe').onclick=()=>exporting(()=>download(JSON.stringify(E.recipe(d,s,baseline),null,2),name()+'_recipe.json','application/json'));
 function importText(text){const value=E.read(text);let ds=value.dataset;if(ds.id!=='harmonic'&&!presets.some(p=>p.id===ds.id))ds.id='imported';if(!Array.from($('mixDataset').options).some(o=>o.value===ds.id)){let o=document.createElement('option');o.value=ds.id;o.textContent='Imported · '+ds.title;$('mixDataset').append(o)}$('mixDataset').value=ds.id;load(ds,value.settings,value.baseline)}
 $('mixLoad').onclick=()=>$('mixFile').click();$('mixFile').onchange=async()=>{try{let file=$('mixFile').files[0];if(!file)return;if(file.size>16000000)throw Error('Import up to 16 MB per file; use a selected window for larger studies.');importText(await file.text())}catch(e){$('mixError').hidden=false;$('mixError').textContent=e.message}finally{$('mixFile').value=''}};
 $('mixApplyPaste').onclick=()=>{try{importText($('mixPaste').value)}catch(e){$('mixError').hidden=false;$('mixError').textContent=e.message}};
 $('mixExample').onclick=()=>download(JSON.stringify(presets[0],null,2),'compound_eye_trace_example.json','application/json');
 // Small inspection hook for automated UI checks; no external requests.
 window.CompoundEyeMixer={snapshot:()=>E.recipe(d,s,baseline),result:()=>E.copy(m),importText};
 controls();draw();
})();
