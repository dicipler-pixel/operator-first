/* Execute the real UI handlers against a small DOM harness.
   This tests wiring and state transitions, not browser layout or PNG encoding. */
const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
class Element{
 constructor(id=''){this.id=id;this.value='';this.checked=false;this.hidden=false;this.disabled=false;this.innerHTML='';this.textContent='';this.options=[];this.listeners={};this.dataset={};this.classList={toggle(){}}}
 append(e){this.options.push(e)}addEventListener(t,f){(this.listeners[t]??=[]).push(f)}
 querySelector(q){if(q==='svg')return {outerHTML:this.innerHTML};return new Element()}
 click(){if(this.onclick)this.onclick();(this.listeners.click||[]).forEach(f=>f({target:this}))}remove(){}
 fire(t,target=this){(this.listeners[t]||[]).forEach(f=>f({target}));if(this['on'+t])this['on'+t]({target})}
}
const html=fs.readFileSync(path.join(__dirname,'panel.html'),'utf8'),nodes={};for(const match of html.matchAll(/id="([^"]+)"/g))nodes[match[1]]=new Element(match[1]);
const tabs=['mixer','horizon','catalog'].map(t=>{let e=new Element();e.dataset.tab=t;return e});const downloads=[];let frames=new Map(),next=1;
const doc={getElementById:id=>nodes[id]||(()=>{throw Error('Missing DOM ID '+id)})(),querySelectorAll:()=>tabs,createElement:tag=>{let e=new Element();if(tag==='a')e.click=()=>downloads.push(e.download);return e},body:new Element()};
const c={document:doc,window:{},console,Blob,URL,setTimeout:f=>f(),requestAnimationFrame:f=>{let id=next++;frames.set(id,f);return id},cancelAnimationFrame:id=>frames.delete(id)};vm.createContext(c);
for(const file of ['mixer_core.js','mixer_plot.js','mixer_ui.js'])vm.runInContext(fs.readFileSync(path.join(__dirname,file),'utf8'),c,{filename:file});
const app=c.window.CompoundEyeMixer;let tests=[];const test=(n,f)=>{f();tests.push(n)};
test('Initial state actually draws a combined SVG',()=>{assert(nodes.mixGraphic.innerHTML.startsWith('<svg'));assert.equal(app.result().activeCount,4)});
test('All off and all on change the real output',()=>{nodes.mixNone.click();assert(app.result().combined.every(x=>x===0));nodes.mixAll.click();assert.equal(app.result().activeCount,5)});
test('Weight handler changes composition',()=>{let target=new Element();target.dataset.control='weight';target.value='0';target.closest=()=>({dataset:{id:'harmonic_0'},querySelector:()=>new Element()});nodes.mixChannels.fire('input',target);assert.equal(app.snapshot().settings.channels.harmonic_0.weight,0)});
test('Pin holds the previous settings',()=>{nodes.mixPin.click();nodes.mixSmoothing.value='9';nodes.mixSmoothing.fire('input');assert.equal(app.snapshot().baseline.settings.smoothing,1);assert.equal(app.snapshot().settings.smoothing,9)});
test('Phase and frequency are wired',()=>{for(const [kind,val] of [['phase',75],['frequency',3]]){let target=new Element();target.dataset.control=kind;target.value=val;target.closest=()=>({dataset:{id:'harmonic_1'}});nodes.mixChannels.fire('input',target);assert.equal(app.snapshot().settings.channels.harmonic_1[kind],val)}});
test('Play advances the shared coordinate and pauses',()=>{nodes.mixPlay.click();let fn=Array.from(frames.values()).at(-1);fn(100);assert(app.snapshot().settings.cursor>0);nodes.mixPlay.click();assert.equal(nodes.mixPlay.textContent,'▶ Play')});
test('Adding then resetting retains the new channel',()=>{let n=app.snapshot().dataset.traces.length;nodes.mixAdd.click();nodes.mixReset.click();assert.equal(app.snapshot().dataset.traces.length,n+1)});
test('Study switching and restoring retains settings',()=>{nodes.mixSmoothing.value='11';nodes.mixSmoothing.fire('input');nodes.mixDataset.value='sun';nodes.mixDataset.fire('change');assert.equal(app.result().activeCount,3);assert.equal(app.snapshot().settings.normalization,'rms');nodes.mixDataset.value='harmonic';nodes.mixDataset.fire('change');assert.equal(app.snapshot().settings.smoothing,11)});
test('Mixed source units are visibly refused',()=>{nodes.mixDataset.value='sun';nodes.mixDataset.fire('change');nodes.mixNormalization.value='source';nodes.mixNormalization.fire('change');assert(!nodes.mixError.hidden);assert(nodes.mixSVG.disabled);nodes.mixNormalization.value='rms';nodes.mixNormalization.fire('change');assert(!nodes.mixSVG.disabled)});
test('Pasted import replaces the displayed case',()=>{nodes.mixPaste.value='time [s],a [V],b [V]\n0,1,2\n1,3,4';nodes.mixApplyPaste.click();assert.equal(app.snapshot().dataset.id,'imported');assert.deepEqual(Array.from(app.result().combined),[3,7])});
test('SVG, CSV and complete recipe export handlers execute',()=>{nodes.mixSVG.click();nodes.mixCSV.click();nodes.mixRecipe.click();assert(downloads.some(n=>n.endsWith('.svg')));assert(downloads.some(n=>n.endsWith('.csv')));assert(downloads.some(n=>n.endsWith('_recipe.json')))});
test('An invalid import does not discard current data',()=>{let before=JSON.stringify(app.snapshot());nodes.mixPaste.value='not a trace';nodes.mixApplyPaste.click();assert.equal(JSON.stringify(app.snapshot()),before);assert(!nodes.mixError.hidden)});
fs.writeFileSync(path.resolve(__dirname,'../../runs/mixer/ui_verification.json'),JSON.stringify({status:'pass',tests:tests.length,checks:tests,method:'Real UI JavaScript executed against a DOM harness',not_tested:['Full browser rendering','Browser file-picker interaction','PNG encoding in a browser','Fullscreen API availability']},null,2));
console.log(JSON.stringify({status:'pass',ui_handler_checks:tests.length}));
