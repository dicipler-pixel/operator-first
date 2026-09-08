// Optional artifact check: node tests/check_offline_pages.js
// Runs the shipped controls against a small DOM harness; no browser layout claim.
const fs=require('fs'),path=require('path'),vm=require('vm'),assert=require('assert');
const root=path.join(__dirname,'..');
function script(name){return fs.readFileSync(path.join(root,name),'utf8').match(/<script>([\s\S]*?)<\/script>/)[1];}
function element(value=''){return {value,textContent:'',hidden:false,dataset:{},attrs:{},listeners:{},addEventListener(e,f){this.listeners[e]=f},setAttribute(k,v){this.attrs[k]=v}};}
const ids={};for(const id of ['coupling','energy','coupling-value','energy-value','gamma-value','channel-value','width-curve','sample-dot'])ids[id]=element();
ids.coupling.value='0.25';ids.energy.value='2';
const context={document:{getElementById(id){assert(ids[id],id);return ids[id]}},window:{}};
vm.runInNewContext(script('START_HERE.html'),context);
assert.equal(ids['gamma-value'].textContent,'0.12500');
ids.coupling.value='0.5';ids.coupling.listeners.input();assert.equal(ids['gamma-value'].textContent,'0.50000');
ids.energy.value='4.5';ids.energy.listeners.input();assert.equal(ids['gamma-value'].textContent,'0.00000');
assert.equal(ids['channel-value'].textContent,'Outside this channel band');
ids.energy.value='4';ids.energy.listeners.input();assert.equal(ids['channel-value'].textContent,'At a band edge');
ids.energy.value='2';ids.coupling.value='0';ids.coupling.listeners.input();assert.equal(ids['gamma-value'].textContent,'0.00000');
assert(!ids['width-curve'].attrs.d.includes('NaN'));
const eyes=fs.readdirSync(path.join(root,'catalog/eyes')).filter(f=>f.endsWith('.json')).map(f=>JSON.parse(fs.readFileSync(path.join(root,'catalog/eyes',f),'utf8'))).map(e=>({hidden:false,dataset:{status:e.status,search:[e.id+'@'+e.version,e.title,e.family,e.status,e.assumptions.join(' ')].join(' ').toLowerCase()}}));
const fields={'eye-search':element(''),'eye-status':element('all'),'eye-count':element()};
vm.runInNewContext(script('BUILD_MANUAL.html'),{document:{getElementById(id){assert(fields[id]);return fields[id]},querySelectorAll(sel){assert.equal(sel,'.eye');return eyes}}});
fields['eye-status'].value='specified';fields['eye-status'].listeners.change();assert.equal(eyes.filter(e=>!e.hidden).length,9);
fields['eye-status'].value='all';fields['eye-search'].value='polygon winding';fields['eye-search'].listeners.input();assert.equal(eyes.filter(e=>!e.hidden).length,1);
fields['eye-search'].value='NO_MATCH_EXPECTED';fields['eye-search'].listeners.input();assert.equal(eyes.filter(e=>!e.hidden).length,0);
fields['eye-search'].value='';fields['eye-search'].listeners.input();assert.equal(eyes.filter(e=>!e.hidden).length,eyes.length);
console.log(JSON.stringify({javascript_controls_passed:true,checks:['initial model value','coupling factor of four','closed channel','band edge','zero coupling','finite SVG coordinates','status filter','text search','empty search result','reset catalog'],browser_layout_checked:false},null,2));
