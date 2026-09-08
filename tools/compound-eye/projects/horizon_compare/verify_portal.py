"""Static portal checks plus independent JavaScript/Python formula comparisons.

This is not a screenshot or full browser interaction test.
"""
from pathlib import Path
from html.parser import HTMLParser
from collections import Counter
import re,json,subprocess,sys
import numpy as np
from scipy.linalg import expm
ROOT=Path(__file__).resolve().parents[2];P=Path(__file__).parent
class Inspect(HTMLParser):
    def __init__(self):super().__init__();self.ids=[];self.tabs=[];self.scripts=[];self.current=None;self.external=[];self.math=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if 'data-tab' in a:self.tabs.append(a['data-tab'])
        if tag=='script':
            self.current=''
            if 'src' in a:self.external.append(a['src'])
        if tag=='math':self.math+=1
    def handle_data(self,data):
        if self.current is not None:self.current+=data
    def handle_endtag(self,tag):
        if tag=='script':self.scripts.append(self.current);self.current=None
s=Inspect();html=(ROOT/'START_HERE.html').read_text();s.feed(html)
assert len(s.ids)==len(set(s.ids)),[k for k,v in Counter(s.ids).items() if v>1]
assert all(t in s.ids for t in s.tabs) and len(s.tabs)==6
assert not s.external and len(s.scripts)==2 and s.math>=10
assert '__OBS_SCAN__' not in html and '__FINDINGS__' not in html
assert '<span class="math display">\\' not in html,'An equation fell back to raw TeX.'
out=ROOT/'runs/horizon'
for k,script in enumerate(s.scripts):
    path=out/('portal_script_'+str(k)+'.js');path.write_text(script)
    subprocess.run(['node','--check',str(path)],check=True)
# Compare browser trajectory model to SciPy expm on all UI parameter choices.
source="const m=require(process.argv[1]);const rows=[];for(const f of [0,.000001,.001,.05,.2])for(const [b,h] of [[2,0],[3,1]])for(const t of [0,.01,.5,2,4])rows.push({f,b,h,t,value:m.state(t,b,h,f)});console.log(JSON.stringify({rows,shape:[-.55,0,.1,.55].map(q=>m.shape(q)),rays:[1,2,4].map(r=>m.ray(r))}));"
data=json.loads(subprocess.check_output(['node','-e',source,str(P/'horizon_models.js')],text=True))
maxerr=0
for x in data['rows']:
    y=expm(x['t']*np.array([[-1,x['f']],[.3,-x['b']]]))@np.array([1,x['h']])
    maxerr=max(maxerr,float(np.linalg.norm(y-x['value'])))
assert maxerr<1e-12
for v in data['shape']:
    assert abs(v['length']-np.arcsin(abs(v['q'])))<1e-14
    if v['q']!=0:
        A=np.array(v['A']);ev,V=np.linalg.eig(A);proj=np.outer(V[:,0],np.linalg.inv(V)[0]);assert abs(np.linalg.norm(proj,2)-v['norm'])<1e-10
assert [v['type'] for v in data['rays']]==['spacelike','null','timelike']
result={'status':'pass','tab_targets':s.tabs,'unique_ids':len(s.ids),'offline_mathml_elements':s.math,'external_scripts':s.external,'javascript_syntax_checks':len(s.scripts),'trajectory_comparisons':len(data['rows']),'maximum_expm_difference':maxerr,'shape_and_causal_controls':True,'visual_status':'Scientific PNG inspected. No full browser rendering or interaction verification.'}
(out/'portal_verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
