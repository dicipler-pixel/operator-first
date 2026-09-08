const fs=require('fs'),vm=require('vm'),assert=require('assert');
const html=fs.readFileSync(require('path').join(__dirname,'Diophantine_Evolution.html'),'utf8');
const script=html.match(/<script>([\s\S]*)<\/script>/)[1];
for(const width of [360,736,1024]){
 const ids=[...html.matchAll(/id="([^"]+)"/g)].map(x=>x[1]);const elements={};let timer;
 const ctx=new Proxy({}, {get:(o,k)=>k in o?o[k]:(...args)=>{assert(args.every(x=>typeof x!=='number'||Number.isFinite(x)),k)},set:(o,k,v)=>(o[k]=v,true)});
 for(const id of ids)elements[id]={value:id==='cutoff'?'160':id==='metric'?'mean':id==='parameter'?'20':'',textContent:'',innerHTML:'',getBoundingClientRect:()=>({width,height:width<650?300:360}),getContext:()=>ctx};
 const sandbox={document:{getElementById:id=>{assert(id in elements,id);return elements[id]}},window:{devicePixelRatio:1,addEventListener(){},matchMedia:()=>({matches:false})},setInterval:f=>(timer=f,1),clearInterval:()=>{timer=null}};
 vm.createContext(sandbox);vm.runInContext(script,sandbox);
 assert(elements.sectionState.textContent.includes('Exact integer point'));
 const before=elements.values.textContent;elements.cutoff.value='590';elements.cutoff.oninput();assert.notEqual(before,elements.values.textContent);
 elements.metric.value='weighted';elements.metric.onchange();assert(elements.values.textContent.includes('Persistent twist'));
 elements.parameter.value='0';elements.parameter.oninput();assert(elements.sectionState.textContent.includes('Nonintegral'));
 elements.play.onclick();for(let i=0;i<300&&timer;i++)timer();assert.equal(elements.play.textContent,'Play validation');
 assert(elements.winners.innerHTML.match(/<tr>/g).length===9);
}
console.log('Viewer logic PASS at three modeled widths; this is not a browser screenshot test.');
