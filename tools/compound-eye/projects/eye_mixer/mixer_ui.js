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
   $('mixProvenance').innerHTML=`<p><b>${esc(d.context.object_id)}</b> · ${esc(d.context.model_id)}<br>${esc(d.context.source_stage)} · ${esc(d.context.coordinate)} [${esc(d.context.x_unit)}]</p><p>Signal = ${m.traces.map(t=>fmt(t.weight)+' × '+esc(t.label)).join(' + ')||'0 (no active channel)'}</p>`+m.traces.map(t=>{let original=d.traces.find(x=>x.id===t.id),k=s.cursor||0;return `<p style="border-left:2px solid ${t.color};padding-left:10px">${esc(t.label)} [${esc(t.unit)}] → ${esc(t.route)}<br>${esc(original.source)}<br>Stored source sample ${fmt(original.values[k])} · current Y contribution ${fmt(t.y[k])}<br>Y offset ${fmt(t.transforms.y.offset)} · Y scale ${fmt(t.transforms.y.scale)}</p>`}).join('');
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
