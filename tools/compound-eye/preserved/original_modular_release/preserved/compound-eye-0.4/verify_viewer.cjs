// Node >=18. No packages required. This checks real event logic with a minimal
// DOM adapter; it does not claim to check full browser layout.
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const here=__dirname,html=fs.readFileSync(path.join(here,'compound_eye.html'),'utf8');
const els={};
function make(id){
 if(els[id])return els[id];
 const el={id,textContent:'',attrs:{},events:{},width:736,setAttribute(k,v){this.attrs[k]=v},addEventListener(k,f){this.events[k]=f},getBoundingClientRect(){return {width:this.width}}};
 let content='';Object.defineProperty(el,'innerHTML',{get(){return content},set(v){content=v;for(const m of v.matchAll(/\bid="([^"]+)"/g))make(m[1]);}});
 return els[id]=el;
}
const markup=html.replace(/(<script\b[^>]*>)[\s\S]*?<\/script>/g,'$1</script>');
for(const m of markup.matchAll(/\bid="([^"]+)"/g))make(m[1]);
const scripts=[...html.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/g)];
for(const [_,attr,body] of scripts){const id=/\bid="([^"]+)"/.exec(attr);if(id)els[id[1]].textContent=body;}
els['compound-eye'].querySelector=q=>{assert(els[q.slice(1)],'Missing element '+q);return els[q.slice(1)]};
let callback=null,now=0,exported=null,downloaded=false;
const ctx={document:{getElementById:id=>els[id],createElement:()=>({click(){downloaded=true;assert.equal(this.download,'compound-eye-trace.json')}})},window:{addEventListener(){}},Math,Number,JSON,Error,performance:{now:()=>now},requestAnimationFrame:f=>{callback=f;return 1},cancelAnimationFrame:()=>{callback=null},Blob:class{constructor(parts){exported=JSON.parse(parts[0])}},URL:{createObjectURL:()=>'blob:local-test',revokeObjectURL(){}},setTimeout:f=>f()};
for(const script of scripts.filter(s=>!s[1].includes('type="application/json"')))vm.runInNewContext(script[2],ctx);
assert.equal(Object.keys(els).filter(k=>k.startsWith('read-')).length,16);
assert.equal(els.clock.textContent,'t = 0.00');assert(els['read-phase'].innerHTML.includes('undefined'));
for(const width of [320,360,736,1024]){
 els.network.width=width;
 els.restart.events.click();els.run.events.click();
 now+=1000;const step=callback;assert(step);step(now);
 assert.equal(els.clock.textContent,'t = 1.00');
 assert(els.status.textContent.includes('Frame 100 / 800'));
 assert(!/NaN|undefined/.test(els.network.innerHTML));
 for(const k of Object.keys(els).filter(k=>k.startsWith('read-'))){assert(els[k].innerHTML.length>0,k);assert(!els[k].innerHTML.includes('NaN'),k);}
 els.run.events.click();assert.equal(callback,null);
 els.next.events.click();assert.equal(els.clock.textContent,'t = 1.01');
 els.run.events.click();now+=10000;callback(now);assert.equal(els.clock.textContent,'t = 8.00');assert.equal(callback,null);
}
els.export.events.click();assert(downloaded);assert.equal(exported.trace.length,801);assert.equal(exported.registry.implemented.length,16);assert.equal(exported.registry.extensions.length,9);
els.network.width=736;els.restart.events.click();els.run.events.click();now+=1000;callback(now);els.run.events.click();
const preview='<svg xmlns="http://www.w3.org/2000/svg" viewBox="'+els.network.attrs.viewBox+'"><style>text{font-family:Arial,sans-serif;fill:#dce6e8;font-size:14px}</style><rect width="100%" height="100%" fill="#0c161c"/>'+els.network.innerHTML+'</svg>';
fs.writeFileSync(path.join(here,'network_preview.svg'),preview);
for(let k=0;k<=16;k++){
 els['earth-step'].value=String(k);els['earth-step'].events.input();
 assert.equal(els['earth-count'].textContent,(96+k)+' / 104');
 assert.equal(els['earth-planar'].textContent,k>=9?'Two layers impossible':'Two layers unresolved');
 assert.equal(els['earth-color'].textContent,k===16?'χ = 10':'χ ≤ 9');
}
for(const [name,n,score] of [['kt_7_4',4,'7/4'],['kt_11_6',6,'11/6'],['kt_11_6_minus_generator',0,'5/3']]){
 els['ak-case'].value=name;els['ak-case'].events.change();assert.equal(els['ak-cost'].textContent,score);
 assert.equal(els['ak-step'].max,String(n));assert.equal(els['ak-step'].disabled,n===0);
 for(let k=0;k<=n;k++){
  els['ak-step'].value=String(k);els['ak-step'].events.input();
  assert.equal(els['ak-known'].textContent,k+' / '+(name==='kt_7_4'?4:6));
  assert(!/undefined|NaN/.test(els['ak-witness'].textContent));
 }
 if(n===0){assert.equal(els['ak-cuts'].textContent,'All 63 cuts pass');assert.equal(els['ak-verdict'].textContent,'Stalled; target unmet');}
}
const result={event_logic:'passed',readouts:16,frames:801,extensions:9,checked_diagram_widths:[320,360,736,1024],controls:['run','pause','next frame','restart','export','earth closure slider','arithmetic candidate selector','forcing-step slider'],all_share_one_frame:true,frontier_replays:{earth_steps:17,arithmetic_cases:3,all_checked:true},full_browser_layout:'not checked: browser unavailable in this session',method:'Minimal Node DOM adapter; actual application scripts and datasets executed.'};
fs.writeFileSync(path.join(here,'viewer_verification.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
