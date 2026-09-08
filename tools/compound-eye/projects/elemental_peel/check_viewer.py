"""Compare the shipped JavaScript calculation with Python at new coordinates.

Also exercise each UI input and animation handler with a minimal DOM harness.
This is numerical/handler verification, not a full-browser screenshot test.
"""
from pathlib import Path
import json, subprocess
import numpy as np
import elemental_eyes as ee

HERE=Path(__file__).resolve().parent
js=r'''
const fs=require('fs'),vm=require('vm');
const ctx={module:{exports:{}},DATA:JSON.parse(fs.readFileSync(process.argv[1]))};
vm.createContext(ctx);vm.runInContext(fs.readFileSync(process.argv[2],'utf8'),ctx);
let a=[];
for(let el of ['Au','Ag','Cu','Pt'])for(let source of ['measured','fit']){
 let s=ctx.module.exports.spectrum(el,37.3,1.73,source,.63,1.7);
 a.push({el,source,s,color:ctx.module.exports.color(s.map(v=>v.R))});
}
let nodes={},callbacks={},tick,cleared=false;
const drawing=new Proxy({},{get:()=>()=>{}});
const make=()=>({value:'',textContent:'',innerHTML:'',hidden:false,width:1000,height:330,
 addEventListener:(k,f)=>{},appendChild:()=>{},getContext:()=>drawing});
for(let id of ['depth','outside','source','ib','damping','angle','depthValue','outsideValue','ibValue','dampingValue','fitcontrols','cards','optics','ions','angleValue','joint','play']){
 nodes[id]=make();nodes[id].addEventListener=(k,f)=>callbacks[id]=f;
}
Object.assign(nodes.depth,{value:'50'});nodes.outside.value='1.5';nodes.source.value='measured';nodes.ib.value='1';nodes.damping.value='1';nodes.angle.value='45';
const ui={DATA:ctx.DATA,document:{getElementById:id=>nodes[id],createElement:make},setInterval:f=>{tick=f;return 1},clearInterval:()=>cleared=true};
vm.createContext(ui);vm.runInContext(fs.readFileSync(process.argv[2],'utf8'),ui);
if(!nodes.fitcontrols.hidden)throw Error('Measured mode shows fit controls');
for(let id of ['depth','outside','source','ib','damping','angle'])callbacks[id]();
nodes.source.value='fit';callbacks.source();if(nodes.fitcontrols.hidden)throw Error('Fit controls missing');
nodes.play.onclick();tick();if(+nodes.depth.value!==49)throw Error('Animation did not thin');
nodes.play.onclick();if(!cleared)throw Error('Animation did not stop');
process.stdout.write(JSON.stringify({cases:a,handler_checks:10}));
'''
out=json.loads(subprocess.check_output(['node','-e',js,str(HERE/'viewer_data.json'),str(HERE/'viewer.js')]))
d=json.loads((HERE/'viewer_data.json').read_text());w=np.array(d['wavelength_nm']);largest=0.
for q in out['cases']:
 el=q['el']
 if q['source']=='measured' and el in d['measured_nk']:
  nk=np.array(d['measured_nk'][el]);n=nk[:,0]+1j*nk[:,1]
 else:
  z=ee.components({'case':{'parameters':d['parameters'][el],'energy_eV':1239.8419843320026/w,'interband_scale':.63,'drude_gamma_scale':1.7}})
  n=np.array(z['n'])+1j*np.array(z['k'])
 py=ee.film_core(w,n,37.3,1.73)
 for name in ['R','T','A']:
  err=float(np.max(abs(np.array(py[name])-np.array([v[name] for v in q['s']]))));largest=max(largest,err);assert err<2e-12
 co=ee.color({'case':{'cmf':d['cmf'],'illuminant':d['illuminant']}},None,{'film':{'value':dict(py,wavelength_nm=w)}})
 assert max(abs(np.array(co['XYZ_D65'])-q['color']['XYZ']))<2e-12
 assert co['hex']==q['color']['hex']
r={'status':'PASS','off_grid_spectra':len(out['cases']),'wavelengths_per_spectrum':len(w),'largest_RTA_difference':largest,'handler_checks':out['handler_checks'],'scope':'Node numerical and DOM-handler checks; no fresh full-browser screenshot.'}
(HERE/'results/viewer_verification.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
