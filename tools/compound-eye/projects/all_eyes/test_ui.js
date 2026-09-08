/* Real viewer handlers executed in a DOM/canvas harness; no screenshot claim. */
const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const page=fs.readFileSync(path.join(__dirname,'All_Eyes_Observatory.html'),'utf8');
let strokes=0,downloads=[],timers=new Map(),timerId=0;
class Element{
 constructor(tag='div',id=''){this.tag=tag;this.id=id;this.children=[];this.dataset={};this.style={};this._value='';this.textContent='';this.checked=false;this.disabled=false;this._selected=0;}
 set value(v){this._value=String(v)}get value(){return this._value}
 set selectedIndex(i){this._selected=i;this._value=this.children[i]?.value||''}get selectedIndex(){return this._selected}
 append(...es){this.children.push(...es);if(this.tag==='select'&&!this.value&&es.length)this.value=es[0].value}
 replaceChildren(...es){this.children=[];if(this.tag==='select')this._value='';this.append(...es)}
 getBoundingClientRect(){return {width:this.id==='mainPlot'?880:200,height:this.id==='mainPlot'?350:75}}
 getContext(){return new Proxy({},{get:(_,k)=>(...a)=>{if(k==='stroke')strokes++;if(['arc','moveTo','lineTo'].includes(k))assert(a.every(Number.isFinite),'Nonfinite plot coordinate')},set:()=>true})}
 querySelector(q){if(q==='.value')return this.children.find(x=>x.className==='value');return this.children.find(x=>x.tag===q)}
 click(){if(this.tag==='a')downloads.push(this.download);else this.onclick?.()}
}
const nodes={};for(const x of page.matchAll(/<(\w+)[^>]*id="([^"]+)"/g))nodes[x[2]]=new Element(x[1],x[2]);
nodes.data.textContent=page.match(/<script id="data" type="application\/json">([\s\S]*?)<\/script>/)[1];nodes.speed.value='180';nodes.plotMode.value='traces';
const doc={getElementById:id=>nodes[id]||(()=>{throw Error('Unknown ID '+id)})(),createElement:t=>new Element(t),createTextNode:t=>({textContent:t}),querySelectorAll:q=>q==='.trace'?nodes.traces.children:[]};
const sandbox={document:doc,window:{addEventListener(){}},location:{protocol:'file:'},console,Blob,URL,devicePixelRatio:1,setTimeout:f=>f(),setInterval:f=>{timers.set(++timerId,f);return timerId},clearInterval:id=>timers.delete(id),fetch:global.fetch};
vm.createContext(sandbox);const script=page.match(/<\/script><script>([\s\S]*?)<\/script>/)[1];vm.runInContext(script,sandbox);const tests=[];
function test(n,fn){fn();tests.push(n)}
async function main(){
test('Initial viewer draws traces and accounts for 191 eyes',()=>{assert(strokes>0);assert(nodes.totals.textContent.includes('191'));assert.equal(nodes.inventory.children.length,191)});
test('Every study loads and plots finite coordinates',()=>{for(const e of nodes.study.children){nodes.study.value=e.value;nodes.study.onchange();assert(nodes.traces.children.length>0)}});
test('All-off removes visible eye selection',()=>{nodes.none.click();assert(nodes.activeCount.textContent.startsWith('0 '));nodes.all.click();assert(!nodes.activeCount.textContent.startsWith('0 '))});
test('Scrubbing advances the real recorded coordinate',()=>{nodes.scrub.value='3';nodes.scrub.oninput();assert.equal(nodes.coordinate.textContent,'3')});
test('Play advances and pause stops the same cursor',()=>{nodes.play.click();[...timers.values()][0]();assert.equal(nodes.coordinate.textContent,'4');nodes.play.click();assert.equal(timers.size,0)});
test('Individual eye toggle changes selected views',()=>{let c=nodes.eyes.children[0].children[0];c.checked=false;c.onchange();assert(nodes.activeCount.textContent.startsWith('5 '))});
test('Portrait uses actual metric names and values',()=>{nodes.plotMode.value='portrait';nodes.plotMode.onchange();assert(nodes.plotNote.textContent.includes('raw readout scales'))});
test('Inventory search retains missing-data reasons',()=>{nodes.search.value='nuclear';nodes.search.oninput();assert.equal(nodes.inventory.children.length,1);assert(nodes.inventory.children[0].children[1].title.includes('detector_events'))});
test('Frame export uses an actual JSON download',()=>{nodes.export.click();assert(downloads[0].endsWith('_frame.json'))});
if(process.env.OBSERVATORY_TEST_URL){
 sandbox.fetch=(url)=>global.fetch(process.env.OBSERVATORY_TEST_URL+url);nodes.study.value='weak';nodes.study.onchange();
 await vm.runInContext('calculate(.137)',sandbox);
 test('Live HTTP handler returns an unrecorded Python frame',()=>{assert.equal(nodes.coordinate.textContent,'0.137');assert(nodes.liveNote.textContent.includes('Fresh registered Python output'))});
 // Delay an old response, switch studies, then release it: stale data must not land.
 let release;sandbox.fetch=()=>new Promise(r=>release=r);const pending=vm.runInContext('calculate(.2)',sandbox);nodes.study.value='quantum';nodes.study.onchange();release({ok:true,json:async()=>({frame:{parameter:.2},seconds:1})});await pending;
 test('A late response cannot overwrite a newly selected problem',()=>assert(nodes.title.textContent.includes('Quantum motion')));
}
const result={status:'PASS',checks:tests.length,tests,method:'Actual UI JavaScript in a DOM/canvas harness; optional real local HTTP computation',not_tested:['Full browser rendering and screenshot','Operating-system file dialog']};fs.writeFileSync(path.join(__dirname,'results/ui_checks.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result));
}
main().catch(e=>{console.error(e);process.exitCode=1});
