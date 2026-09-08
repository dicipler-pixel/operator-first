const fs=require('fs'),vm=require('vm'),assert=require('assert'),path=require('path');
const here=__dirname;
const ids=JSON.parse(fs.readFileSync(path.join(here,'atlas_demo_dom.json'),'utf8'));
const elements={};
for(const id of ids)elements[id]={id,value:id==='load'?'0':'',textContent:'',innerHTML:'',hidden:id==='registers',style:{},attrs:{},events:{},setAttribute(k,v){this.attrs[k]=v},addEventListener(k,f){this.events[k]=f},getBoundingClientRect(){return {width:this.width||850}},width:850};
elements['atlas-demo'].querySelector=sel=>{assert(sel[0]==='#');assert(elements[sel.slice(1)],'Missing element '+sel);return elements[sel.slice(1)];};
const ctx={document:{getElementById:id=>elements[id]},window:{addEventListener(){}},Number,Math,Error};
vm.runInNewContext(fs.readFileSync(path.join(here,'atlas_demo_script.js'),'utf8'),ctx);
assert.equal(elements['full-result'].textContent,'41');
assert.equal(elements['diagram-result'].textContent,'41');
const checks=[];
for(const width of [320,360,736,1024]){
 elements.network.width=width;
 for(const load of [0,0.25,2,8]){
  elements.load.value=String(load);elements.load.events.input();
  const expected=String(41+19*load);
  assert.equal(elements['full-result'].textContent,expected);
  assert.equal(elements['diagram-result'].textContent,expected);
  const before=elements.registers.hidden;
  elements.simplify.events.click();
  assert.equal(elements.registers.hidden,!before);
  assert.equal(elements['diagram-result'].textContent,expected);
  assert(!elements.network.innerHTML.includes('undefined'));
  assert(!elements.network.innerHTML.includes('NaN'));
 }
 checks.push({width,loads:[0,0.25,2,8],passed:true});
}
elements.forget.events.click();assert.equal(elements['x-result'].textContent,'Incomplete reading: 1.5');assert.equal(elements['y-result'].textContent,'Incomplete reading: 1.5');assert(elements['counter-message'].textContent.startsWith('False agreement'));
elements.forget.events.click();assert.equal(elements['x-result'].textContent,'Determinant: 3');assert.equal(elements['y-result'].textContent,'Determinant: 12');
const report={method:'Node VM with a minimal DOM adapter; event handlers executed, not a browser layout test',script_syntax:'passed',controls:'passed',responsive_diagram_coordinates:checks,external_dependencies:false,full_browser_render:'not verified: Chromium unavailable and download timed out',status:'logic checks passed; browser layout remains unchecked'};
const folder=here;
fs.writeFileSync(folder+'/display_checks.json',JSON.stringify(report,null,2)+'\n');
elements.network.width=736;elements.load.value='2';elements.load.events.input();
function save(name){fs.writeFileSync(path.join(here,name+'.svg'),'<svg xmlns="http://www.w3.org/2000/svg" viewBox="'+elements.network.attrs.viewBox+'"><rect width="100%" height="100%" fill="#0C161C"/>'+elements.network.innerHTML+'</svg>');}
save('atlas-demo-full');elements.simplify.events.click();save('atlas-demo-reduced');
console.log(JSON.stringify(report,null,2));
