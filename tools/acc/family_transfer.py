"""Family transfer for tied/untied rows in MS families: replay our path for a same-family neighbour (n-1 or n+1) on
the target row, take the 2 shortest prefix states as seeds, and beam from them (plus the start) to record+2 with
three settings (H, P2, two-eyes). Official core replay. Out: work/family.jsonl (resumes by id)."""
import sys, json, subprocess, os
S='/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad'; R='/home/user/operator-first'
sys.path.insert(0,S+'/sair/competition/tools'); from verifier import core
m=json.load(open(S+'/sair/competition/tools/verifier/data/manifest.json')); C={c['challenge_id']:c for c in m['challenges']}
fam=json.load(open(S+'/work/ms_by_w.json')); where={}
for o,v in fam.items():
    for n,x in v.items(): where[x[2]]=(o,int(n))
roads={}
for l in open(S+'/work/all_roads.jsonl'):
    r=json.loads(l)
    if r['id'] not in roads or len(r['ac'])<len(roads[r['id']]): roads[r['id']]=r['ac']
XD=int(os.environ.get('FAM_EXTRA','2')); out=S+os.environ.get('FAM_OUT','/work/family.jsonl'); done=set()
if os.path.exists(out): done={json.loads(l)['id'] for l in open(out)}
E={1:0,-1:1,2:2,-2:3}
CFG=[('dual',{'BEAM_H':'1','BEAM_DIV':'0.8','BEAM_P2':'2','BEAM_QUOTA':'16','BEAM_ELITE':'5000','BEAM_DUAL':'0.75'}),('H',{'BEAM_H':'1','BEAM_DIV':'1.0'})]
def beam(s,depth,env,T=150):
    enc=[str(len(s[0]))]+[str(E[x]) for x in s[0]]+[str(len(s[1]))]+[str(E[x]) for x in s[1]]
    try: o=subprocess.run([S+'/dualbin/acc_beam',S+'/work/T9.tab','20000',str(depth)]+enc,capture_output=True,text=True,timeout=T,env={**os.environ,**env}).stdout
    except subprocess.TimeoutExpired: return None,None
    ac=sac=None
    for line in o.splitlines():
        if line.startswith('AC ') and 'PATH' in line: ac=[int(x) for x in line.split('PATH')[1].split()]
        if line.startswith('SAC ') and 'PATH' in line: sac=[int(x) for x in line.split('PATH')[1].split()]
    return ac,sac
SH=int(sys.argv[1]) if len(sys.argv)>1 else 0; NS=int(sys.argv[2]) if len(sys.argv)>2 else 1
for ti,t in enumerate(json.load(open(S+'/work/family_targets.json'))):
    if ti%NS!=SH: continue
    cid=t['id']
    if cid in done or cid not in where: continue
    o,n=where[cid]; st=tuple(tuple(r) for r in C[cid]['initial_relators']); rec=t['ac_record']; srec=t.get('sac_record') or 0
    seeds=[([],st)]; used=0
    for nn in (n-1,n+1):
        if used: break
        nb=fam[o].get(str(nn)); P=roads.get(nb[2]) if nb else None
        if not P: continue
        s=st; pre=[]; cand=[]
        for mv in P:
            s=core.apply_move(s,mv); pre=pre+[mv]; cand.append((len(s[0])+len(s[1]),len(pre),list(pre),s))
            if len(pre)>=rec: break
        cand.sort(key=lambda c:(c[0]+c[1],)); seeds+=[(c[2],c[3]) for c in cand[:1]]; used=1
    best={'id':cid,'family':o,'n':n,'record':rec,'sac_record':srec,'tries':[]}
    for pre,s in seeds:
        for name,env in CFG:
            if rec-len(pre)<4: continue
            ac,sac=beam(s,rec+XD-len(pre),env)
            for kind,p in (('ac',ac),('sac',sac)):
                if not p: continue
                full=pre+p
                if kind=='ac':
                    z=st
                    for mv in full: z=core.apply_move(z,mv)
                    if z!=((1,),(2,)): continue
                if kind not in best or len(full)<len(best[kind]): best[kind]=full
            best['tries'].append({'prefix':len(pre),'cfg':name,'ac':len(pre+ac) if ac else None})
        if 'ac' in best and len(best['ac'])<=rec: break
    a=len(best['ac']) if 'ac' in best else None; b=len(best['sac']) if 'sac' in best else None
    best['verdict']='TIE' if a and a<=rec else ('near' if a and a<=rec+2 else ('road' if a else 'miss'))
    with open(out,'a') as f: f.write(json.dumps(best)+'\n')
    print(cid,o,'ac',a,'rec',rec,'sac',b,'srec',srec,best['verdict'],flush=True)
