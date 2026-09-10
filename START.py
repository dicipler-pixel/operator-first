#!/usr/bin/env python3
"""Compound Eye Companion 1.1 clean GitHub share build. Python 3.10+ only."""
from __future__ import annotations
import sys
if sys.version_info < (3,10): raise SystemExit('Python 3.10 or later is required.')
import cmath, hashlib, json, math, os, secrets, threading, time, urllib.request, urllib.error, webbrowser
from fractions import Fraction
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlsplit

VERSION='1.1-share'
HOME=Path(os.getenv('LOCALAPPDATA',Path.home()))/'CompoundEyeCompanion' if os.name=='nt' else Path.home()/'.compound-eye-companion'
DATA=HOME/'workspace.json'
HOME.mkdir(parents=True,exist_ok=True)

def stamp(): return time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())
def fid(): return secrets.token_hex(6)
def F(x):
    if isinstance(x,bool): raise ValueError('Boolean is not a number.')
    return Fraction(str(x))
def clean_text(x,n=40000):
    if not isinstance(x,str): raise ValueError('Expected text.')
    x=x.strip()
    if len(x)>n or '\x00' in x: raise ValueError('Text is too long or invalid.')
    return x

def load():
    if DATA.exists():
        try:
            d=json.loads(DATA.read_text(encoding='utf-8'))
            if isinstance(d,dict) and isinstance(d.get('records'),list): return d
        except Exception: pass
    return {'schema':'compound-eye-share-v1','created':stamp(),'records':[],'rules':[],'settings':{'provider':'offline','model':''},'last':None}
STATE=load(); LOCK=threading.RLock(); PENDING={}
def save():
    tmp=DATA.with_suffix('.tmp'); tmp.write_text(json.dumps(STATE,indent=2,ensure_ascii=False),encoding='utf-8'); tmp.replace(DATA)
def rec(kind,title,data,source=''):
    r={'id':fid(),'kind':kind,'title':clean_text(title,160) or kind,'source':clean_text(source,1000),'created':stamp(),'data':data}; STATE['records'].append(r); return r

def matrix(v):
    if not isinstance(v,list) or not 1<=len(v)<=16 or not all(isinstance(r,list) and len(r)==len(v) for r in v): raise ValueError('Matrix must be square, size 1–16.')
    return [[F(x) for x in r] for r in v]
def rank(A):
    a=[r[:] for r in A]; m=len(a); n=len(a[0]) if a else 0; rr=0
    for c in range(n):
        p=next((i for i in range(rr,m) if a[i][c]),None)
        if p is None: continue
        a[rr],a[p]=a[p],a[rr]; q=a[rr][c]; a[rr]=[x/q for x in a[rr]]
        for i in range(m):
            if i!=rr and a[i][c]:
                q=a[i][c]; a[i]=[x-q*y for x,y in zip(a[i],a[rr])]
        rr+=1
        if rr==m: break
    return rr
def symmetric(A): return all(A[i][j]==A[j][i] for i in range(len(A)) for j in range(len(A)))
def psd_ldl(A):
    if not symmetric(A): return False
    n=len(A); L=[[Fraction(i==j) for j in range(n)] for i in range(n)]; D=[Fraction(0) for _ in range(n)]
    for i in range(n):
        D[i]=A[i][i]-sum(L[i][k]*L[i][k]*D[k] for k in range(i))
        if D[i] < 0: return False
        for j in range(i+1,n):
            num=A[j][i]-sum(L[j][k]*L[i][k]*D[k] for k in range(i))
            if D[i]==0:
                if num!=0: return False
                L[j][i]=0
            else: L[j][i]=num/D[i]
    return True

def record_eye(r):
    out={'id':r['id'],'kind':r['kind'],'title':r['title'],'source_present':bool(r.get('source'))}
    if r['kind']=='theorem':
        d=r['data']; out.update(status='user_supplied_unverified',assumption_count=len(d.get('assumptions',[])),dependencies=d.get('depends_on',[]),missing_statement=not bool(d.get('statement')))
    elif r['kind']=='matrix':
        A=[[F(x) for x in row] for row in r['data']['values']]; n=len(A); rk=rank(A)
        out.update(matrix_size=n,matrix_rank=rk,matrix_nullity=n-rk,matrix_symmetric=symmetric(A),matrix_psd=psd_ldl(A))
    elif r['kind']=='samples':
        xs=[F(x) for x in r['data']['values']]
        out.update(sample_count=len(xs),sample_min=str(min(xs)),sample_max=str(max(xs)),sample_mean=str(sum(xs,Fraction(0))/len(xs)))
    else: out['status']='recorded'
    return out

def metric_value(eye,m):
    if m not in eye: raise ValueError('Metric is unavailable for that record.')
    v=eye[m]
    if isinstance(v,bool): return Fraction(int(v))
    return F(v)
def compare(a,op,b): return {'eq':a==b,'ne':a!=b,'lt':a<b,'le':a<=b,'gt':a>b,'ge':a>=b}[op]
def run_scan():
    eyes=[record_eye(r) for r in STATE['records']]
    by={e['id']:e for e in eyes}; checks=[]
    for q in STATE['rules']:
        try:
            a=metric_value(by[q['record_id']],q['metric']); b=F(q['value']); ok=compare(a,q['comparison'],b); checks.append({'title':q['title'],'status':'pass' if ok else 'fail','actual':str(a),'comparison':q['comparison'],'target':str(b)})
        except Exception as exc: checks.append({'title':q.get('title','rule'),'status':'inapplicable','reason':str(exc)[:160]})
    missing=[]
    known={r['id'] for r in STATE['records']}
    for r in STATE['records']:
        if r['kind']=='theorem':
            for d in r['data'].get('depends_on',[]):
                if d not in known: missing.append({'theorem':r['id'],'missing_dependency':d})
    whole={'schema':'compound-eye-whole-v1','time':stamp(),'record_count':len(eyes),'eyes':eyes,'custom_checks':checks,'missing':missing,'summary':{'passes':sum(x['status']=='pass' for x in checks),'fails':sum(x['status']=='fail' for x in checks),'inapplicable':sum(x['status']=='inapplicable' for x in checks),'unverified_theorems':sum(r['kind']=='theorem' for r in STATE['records'])}}
    STATE['last']=whole; save(); return whole

PHASE_DEFAULT={'sites':12,'steps':360,'dt':0.03,'intra_forward':1.15,'intra_backward':0.72,'inter':0.22,'loss':0.035,'phase_twist':0.45}
def phase_run(cfg):
    c=PHASE_DEFAULT|{k:float(v) if k not in ('sites','steps') else int(v) for k,v in (cfg or {}).items() if k in PHASE_DEFAULT}
    N=c['sites']; steps=c['steps']; dt=c['dt']
    if not 4<=N<=32 or not 20<=steps<=2000 or not 0<dt<=0.2: raise ValueError('Phase-lab bounds exceeded.')
    psi=[0j]*(3*N); psi[N//3]=1+0j
    def deriv(x):
        y=[0j]*len(x)
        for b in range(3):
            for i in range(N):
                k=b*N+i; z=-(c['loss']+0j)*x[k]
                if i>0: z += -1j*c['intra_forward']*x[k-1]
                if i+1<N: z += -1j*c['intra_backward']*x[k+1]
                for bb in range(3):
                    if bb!=b: z += -1j*c['inter']*cmath.exp(1j*c['phase_twist']*(bb-b))*x[bb*N+i]
                y[k]=z
        return y
    frames=[]
    for s in range(steps+1):
        if s%(max(1,steps//90))==0 or s==steps:
            norms=[sum(abs(psi[b*N+i])**2 for i in range(N)) for b in range(3)]; tot=sum(norms)
            cents=[sum(i*abs(psi[b*N+i])**2 for i in range(N))/(max(norms[b],1e-30)*(N-1)) for b in range(3)]
            frames.append({'t':round(s*dt,9),'norm':tot,'fractions':[v/max(tot,1e-30) for v in norms],'centroids':cents})
        if s==steps: break
        k1=deriv(psi); k2=deriv([x+dt*y/2 for x,y in zip(psi,k1)]); k3=deriv([x+dt*y/2 for x,y in zip(psi,k2)]); k4=deriv([x+dt*y for x,y in zip(psi,k3)])
        psi=[x+dt*(a+2*b+2*c4+d)/6 for x,a,b,c4,d in zip(psi,k1,k2,k3,k4)]
    return {'schema':'compound-eye-phase-v1','config':c,'frames':frames,'final':frames[-1],'meaning':'Synthetic finite three-bundle complex-amplitude model; not a material measurement or Yang–Mills simulation.'}

def add_action(a):
    kind=a.get('action'); d=a.get('args',{})
    if kind=='add_theorem': return rec('theorem',d.get('title','Theorem'),{'statement':clean_text(d.get('statement','')),'domain':clean_text(d.get('domain',''),1000),'assumptions':[clean_text(x,1000) for x in d.get('assumptions',[])[:50]],'depends_on':[str(x) for x in d.get('depends_on',[])[:50]]},d.get('source',''))
    if kind=='add_note': return rec('note',d.get('title','Note'),{'text':clean_text(d.get('text',''))},d.get('source',''))
    if kind=='add_matrix':
        A=matrix(d.get('values')); return rec('matrix',d.get('title','Matrix'),{'values':[[str(x) for x in row] for row in A],'units':clean_text(d.get('units','not declared'),100)},d.get('source',''))
    if kind=='add_samples':
        xs=d.get('values');
        if not isinstance(xs,list) or not 1<=len(xs)<=2000: raise ValueError('Supply 1–2000 samples.')
        return rec('samples',d.get('title','Samples'),{'values':[str(F(x)) for x in xs],'units':clean_text(d.get('units','not declared'),100)},d.get('source',''))
    if kind=='add_rule':
        if d.get('comparison') not in ('eq','ne','lt','le','gt','ge'): raise ValueError('Bad comparison.')
        q={'id':fid(),'title':clean_text(d.get('title','Custom eye'),160),'record_id':str(d.get('record_id','')),'metric':str(d.get('metric','')),'comparison':d['comparison'],'value':str(F(d.get('value',0)))}; STATE['rules'].append(q); return q
    if kind=='run_scan': return run_scan()
    if kind=='run_phase': return phase_run(d)
    raise ValueError('Unsupported action.')

def offline_plan(msg):
    t=msg.lower(); actions=[]
    if 'run' in t and ('eye' in t or 'scan' in t): actions.append({'action':'run_scan','args':{}})
    if 'phase' in t or 'bundle' in t or 'skin' in t: actions.append({'action':'run_phase','args':{}})
    return {'assistant':'Offline helper prepared the actions it can infer. Add theorem/data records with the forms for exact fields.','actions':actions}

def workspace_summary():
    return {'records':[{'id':r['id'],'kind':r['kind'],'title':r['title']} for r in STATE['records'][-40:]],'rules':STATE['rules'][-20:],'last_summary':(STATE.get('last') or {}).get('summary')}
def openai_plan(msg):
    key=os.getenv('OPENAI_API_KEY','').strip(); model=STATE['settings'].get('model','').strip()
    if not key or not model: raise ValueError('Set OPENAI_API_KEY in the terminal environment and choose a model in Settings.')
    schema={'type':'object','properties':{'assistant':{'type':'string'},'actions':{'type':'array','maxItems':4,'items':{'type':'object','properties':{'action':{'type':'string','enum':['add_theorem','add_note','add_matrix','add_samples','add_rule','run_scan','run_phase']},'args':{'type':'object'}},'required':['action','args'],'additionalProperties':False}}},'required':['assistant','actions'],'additionalProperties':False}
    instructions='You are the planner inside Compound Eye Companion. Propose only actions in the schema. Never claim a theorem is proved merely because it was uploaded or a check passed. Never request secrets. The user must approve actions before local execution. If fields are missing, return no action and ask for them in assistant.'
    payload={'model':model,'instructions':instructions,'input':json.dumps({'user':msg,'workspace':workspace_summary()},ensure_ascii=False),'text':{'format':{'type':'json_schema','name':'compound_eye_plan','strict':True,'schema':schema}},'store':False,'max_output_tokens':1400}
    req=urllib.request.Request('https://api.openai.com/v1/responses',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'},method='POST')
    try:
        with urllib.request.urlopen(req,timeout=90) as r: ans=json.load(r)
    except urllib.error.HTTPError as e: raise ValueError('OpenAI request failed with HTTP '+str(e.code)) from None
    text=ans.get('output_text')
    if not text:
        parts=[]
        for item in ans.get('output',[]):
            for c in item.get('content',[]) if isinstance(item,dict) else []:
                if isinstance(c,dict) and isinstance(c.get('text'),str): parts.append(c['text'])
        text=''.join(parts)
    out=json.loads(text); return out

def propose(msg):
    provider=STATE['settings'].get('provider','offline'); plan=openai_plan(msg) if provider=='openai' else offline_plan(msg)
    pid=fid(); PENDING[pid]=plan; return {'plan_id':pid,**plan}
def approve(pid):
    plan=PENDING.pop(pid,None)
    if not plan: raise ValueError('Plan is missing or already used.')
    results=[]
    for a in plan.get('actions',[])[:4]: results.append(add_action(a))
    save(); return {'executed':len(results),'results':results}

HTML=r'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Compound Eye Companion</title><style>
:root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#07131a;color:#e8f0f2;font:15px/1.5 system-ui}header{padding:24px 5vw;border-bottom:1px solid #25414b;background:#0b1c24}h1{margin:0;font-size:28px}main{max-width:1180px;margin:auto;padding:24px;display:grid;grid-template-columns:1fr 1fr;gap:18px}.card{background:#0c2029;border:1px solid #294650;border-radius:14px;padding:18px}.wide{grid-column:1/-1}input,textarea,select,button{width:100%;margin:5px 0 9px;padding:10px;border-radius:8px;border:1px solid #34525d;background:#09171d;color:#eef}textarea{min-height:80px}button{cursor:pointer;background:#163a43}.row{display:flex;gap:8px}.row>*{flex:1}pre{white-space:pre-wrap;max-height:430px;overflow:auto;background:#071219;padding:12px;border-radius:8px}.small{color:#9fb8c0;font-size:12px}.ok{color:#8ee0ba}.warn{color:#ffd58a}@media(max-width:800px){main{grid-template-columns:1fr}.wide{grid-column:auto}}</style></head><body>
<header><h1>Compound Eye Companion 1.1</h1><div class="small">Clean share build · local workspace · reviewed actions before execution</div></header><main>
<section class="card wide"><h2>AI companion</h2><div class="row"><select id="provider"><option value="offline">Offline helper</option><option value="openai">OpenAI</option></select><input id="model" placeholder="Model name for OpenAI"></div><textarea id="chat" placeholder="Example: run all eyes on my current records; then run the phase bundle lab"></textarea><button onclick="ask()">Prepare proposal</button><pre id="proposal">No proposal yet.</pre><button id="approve" onclick="approvePlan()" disabled>Approve displayed actions</button></section>
<section class="card"><h2>Add theorem</h2><input id="tt" placeholder="Title"><textarea id="ts" placeholder="Statement"></textarea><input id="ta" placeholder="Assumptions, separated by ;"><input id="tso" placeholder="Source"><button onclick="addTheorem()">Add locally</button></section>
<section class="card"><h2>Add matrix</h2><input id="mt" placeholder="Title"><textarea id="mv" placeholder='JSON square matrix, e.g. [[1,0],[0,2]]'></textarea><button onclick="addMatrix()">Add locally</button></section>
<section class="card"><h2>Whole view</h2><button onclick="scan()">Run all eyes</button><pre id="whole">No run yet.</pre></section>
<section class="card"><h2>Phase & coupling lab</h2><div class="row"><input id="inter" value="0.22" title="inter-bundle coupling"><input id="loss" value="0.035" title="loss"></div><div class="row"><input id="fwd" value="1.15" title="forward"><input id="back" value="0.72" title="backward"></div><button onclick="phase()">Run bundle phase lab</button><pre id="phase">No phase run yet.</pre></section>
<section class="card wide"><h2>Workspace</h2><button onclick="state()">Refresh</button><pre id="state"></pre><div class="small">The clean edition contains no creator research archive. Theorems you add remain user-supplied and unverified until separately proved.</div></section>
</main><script>
let plan=null; const $=x=>document.getElementById(x); async function api(path,body={}){let r=await fetch(path,{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+TOKEN},body:JSON.stringify(body)});let j=await r.json();if(!r.ok)throw Error(j.error||'request failed');return j.result}
async function settings(){await api('/api/settings',{provider:$('provider').value,model:$('model').value})}
async function ask(){try{await settings();let r=await api('/api/propose',{message:$('chat').value});plan=r.plan_id;$('proposal').textContent=JSON.stringify(r,null,2);$('approve').disabled=false}catch(e){$('proposal').textContent=e.message}}
async function approvePlan(){try{let r=await api('/api/approve',{plan_id:plan});$('proposal').textContent=JSON.stringify(r,null,2);$('approve').disabled=true;plan=null;state()}catch(e){$('proposal').textContent=e.message}}
async function addTheorem(){let a=$('ta').value.split(';').map(x=>x.trim()).filter(Boolean);let r=await api('/api/direct',{action:'add_theorem',args:{title:$('tt').value,statement:$('ts').value,assumptions:a,source:$('tso').value}});$('whole').textContent=JSON.stringify(r,null,2);state()}
async function addMatrix(){try{let v=JSON.parse($('mv').value);let r=await api('/api/direct',{action:'add_matrix',args:{title:$('mt').value,values:v}});$('whole').textContent=JSON.stringify(r,null,2);state()}catch(e){$('whole').textContent=e.message}}
async function scan(){let r=await api('/api/direct',{action:'run_scan',args:{}});$('whole').textContent=JSON.stringify(r,null,2);state()}
async function phase(){let r=await api('/api/direct',{action:'run_phase',args:{inter:$('inter').value,loss:$('loss').value,intra_forward:$('fwd').value,intra_backward:$('back').value}});let f=r.final;$('phase').textContent=JSON.stringify({config:r.config,final:f,meaning:r.meaning},null,2)}
async function state(){let r=await fetch('/api/state',{headers:{'Authorization':'Bearer '+TOKEN}});$('state').textContent=JSON.stringify(await r.json(),null,2)}
const TOKEN='__TOKEN__';state();
</script></body></html>'''

class Server(ThreadingHTTPServer):
    daemon_threads=True
class H(BaseHTTPRequestHandler):
    def log_message(self,*a): pass
    def sendj(self,code,obj,ctype='application/json; charset=utf-8'):
        b=obj if isinstance(obj,bytes) else json.dumps(obj,ensure_ascii=False).encode(); self.send_response(code); self.send_header('Content-Type',ctype); self.send_header('Content-Length',str(len(b))); self.send_header('Cache-Control','no-store'); self.send_header('X-Content-Type-Options','nosniff'); self.end_headers(); self.wfile.write(b)
    def auth(self): return secrets.compare_digest(self.headers.get('Authorization',''),'Bearer '+self.server.token)
    def do_GET(self):
        p=urlsplit(self.path).path
        if p=='/': return self.sendj(200,HTML.replace('__TOKEN__',self.server.token).encode(),'text/html; charset=utf-8')
        if p=='/api/state':
            if not self.auth(): return self.sendj(403,{'error':'unauthorized'})
            with LOCK: return self.sendj(200,{'version':VERSION,'workspace':str(DATA),'records':STATE['records'],'rules':STATE['rules'],'settings':STATE['settings'],'last':STATE.get('last')})
        return self.sendj(404,{'error':'not found'})
    def do_POST(self):
        if not self.auth(): return self.sendj(403,{'error':'unauthorized'})
        try:
            n=int(self.headers.get('Content-Length','0'))
            if not 0<=n<=2_000_000: raise ValueError('Request too large.')
            d=json.loads(self.rfile.read(n) or b'{}'); p=urlsplit(self.path).path
            with LOCK:
                if p=='/api/settings':
                    provider=d.get('provider','offline');
                    if provider not in ('offline','openai'): raise ValueError('Unknown provider.')
                    STATE['settings']={'provider':provider,'model':clean_text(d.get('model',''),100)}; save(); out=STATE['settings']
                elif p=='/api/propose': out=propose(clean_text(d.get('message',''),12000))
                elif p=='/api/approve': out=approve(str(d.get('plan_id','')))
                elif p=='/api/direct': out=add_action({'action':d.get('action'),'args':d.get('args',{})}); save()
                else: return self.sendj(404,{'error':'unknown endpoint'})
            return self.sendj(200,{'ok':True,'result':out})
        except Exception as e: return self.sendj(400,{'error':str(e)[:500]})

def main():
    s=Server(('127.0.0.1',0),H); s.token=secrets.token_urlsafe(24); url=f'http://127.0.0.1:{s.server_address[1]}/'; print('Compound Eye Companion:',url); threading.Timer(.4,lambda:webbrowser.open(url)).start()
    try:s.serve_forever()
    except KeyboardInterrupt: pass
    finally:s.server_close()
if __name__=='__main__': main()
