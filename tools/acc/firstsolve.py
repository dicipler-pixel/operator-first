"""First solves on unsolved MS rows: replay our path for the solved MS(n-1,w) on MS(n,w), pick prefix states where the
pair is shortest, and run deep beams from them (any length scores). Plain deep beam from the start is the control.
Paths are replayed with the official core. Out: work/firstsolve.jsonl (resumes by id)."""
import sys, json, subprocess, os
S='/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad'
sys.path.insert(0,S+'/sair/competition/tools'); from verifier import core
m=json.load(open(S+'/sair/competition/tools/verifier/data/manifest.json')); C={c['challenge_id']:c for c in m['challenges']}
d=json.load(open(S+'/work/ms_by_w.json'))
roads={}
for l in open(S+'/work/all_roads.jsonl'):
    r=json.loads(l)
    if r['id'] not in roads or len(r['ac'])<len(roads[r['id']]): roads[r['id']]=r['ac']
out=S+'/work/firstsolve.jsonl'; done=set()
if os.path.exists(out): done={json.loads(l)['id'] for l in open(out)}
E={1:0,-1:1,2:2,-2:3}
def beam(s,depth,env,W='20000',T=180):
    enc=[str(len(s[0]))]+[str(E[x]) for x in s[0]]+[str(len(s[1]))]+[str(E[x]) for x in s[1]]
    try: o=subprocess.run([S+'/dualbin/acc_beam',S+'/work/T9.tab',W,str(depth)]+enc,capture_output=True,text=True,timeout=T,env={**os.environ,**env}).stdout
    except subprocess.TimeoutExpired: return None,None
    ac=sac=None
    for line in o.splitlines():
        if line.startswith('AC ') and 'PATH' in line: ac=[int(x) for x in line.split('PATH')[1].split()]
        if line.startswith('SAC ') and 'PATH' in line: sac=[int(x) for x in line.split('PATH')[1].split()]
    return ac,sac
H={'BEAM_H':'1','BEAM_DIV':'1.0'}; P2={'BEAM_P2':'2','BEAM_H':'1','BEAM_DIV':'0.8'}
for t in json.load(open(S+'/work/firstsolve_targets.json')):
    cid=t['id']
    if cid in done: continue
    st=tuple(tuple(r) for r in C[cid]['initial_relators'])
    lower_id=d[t['w']][str(t['solved_n'])][2]; seeds=[([],st)]
    P=roads.get(lower_id)
    if P:
        s=st; pre=[]; cand=[]
        for mv in P:
            s=core.apply_move(s,mv); pre=pre+[mv]; cand.append((len(s[0])+len(s[1]),len(pre),list(pre),s))
        cand.sort(key=lambda c:(c[0],-c[1])); seeds+= [(c[2],c[3]) for c in cand[:1]]
    rec={'id':cid,'w':t['w'],'n':t['n'],'tries':[]}
    for pre,s in seeds:
        for name,env in (('H',H),('P2',P2)):
            ac,sac=beam(s,250,env)
            ok=None
            if ac is not None:
                z=st
                for mv in pre+ac: z=core.apply_move(z,mv)
                if z==((1,),(2,)): ok=pre+ac
            rec['tries'].append({'prefix':len(pre),'cfg':name,'ac_len':len(ok) if ok else None})
            if ok:
                rec['ac']=ok; break
        if 'ac' in rec: break
    with open(out,'a') as f: f.write(json.dumps(rec)+'\n')
    print(cid,'SOLVED' if 'ac' in rec else 'none',len(rec.get('ac',[])),flush=True)
