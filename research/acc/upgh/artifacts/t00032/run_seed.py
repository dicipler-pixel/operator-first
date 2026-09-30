import sys, json, os, re, subprocess, time, shutil, glob
sys.path.insert(0,'/root/.cache/upgh/sair/competition/tools')
from verifier import core, specs
S='/root/.cache/upgh'; W=S+'/work/t00032'; A='/home/user/operator-first/research/acc/upgh/artifacts/t00032'
man=json.load(open(S+'/sair/competition/tools/verifier/data/manifest.json')); C={c['challenge_id']:c for c in man['challenges']}; LIM=man['limits']
L={1:'x',-1:'X',2:'y',-2:'Y'}
st0=tuple(tuple(r) for r in C['ac-06045']['initial_relators'])
def replay(p):
    s=st0
    for mv in p: s=core.apply_move(s,mv)
    return tuple(''.join(L[t] for t in r) for r in s)
BACK={0:1,1:0,2:4,3:5,4:2,5:3,6:10,7:11,8:12,9:13,10:6,11:7,12:8,13:9}
seeds={
 'b12':([5,12,12,12,12,0,2,6,1,13,11,5],'9 3 3 0 2 2 2 2 2 0 7 1 3 1 1 3 3 3'),
 'c12':([5,12,12,12,12,0,2,6,6,8,1,5],'9 2 0 3 3 0 2 2 2 2 7 1 1 3 3 3 1 3'),
 'd12':([5,12,12,12,12,0,2,6,6,8,2,5],'7 2 0 2 2 2 0 0 9 3 3 3 3 1 2 2 1 3'),
}
A12=[1,2,5,8,8,8,8,5,10,9,7,3]
seed=sys.argv[1]; cap=sys.argv[2]; tmo=int(sys.argv[3]); pre,enc=seeds[seed]
if os.path.exists('/home/user/operator-first/research/acc/upgh/STOP'): print('STOP'); sys.exit(3)
tag=f'{seed}c{cap}'
env=dict(os.environ,MAXD='15',INIT_LOG2='28')
cmd=['timeout',str(tmo),S+'/bin/acc_capped',S+'/T9.tab',cap,'210000000',W,tag]+enc.split()
t=time.time()
p=subprocess.run(cmd,capture_output=True,text=True,env=env)
wall=time.time()-t
open(f'{A}/raw_{tag}.stdout.txt','w').write(p.stdout); open(f'{A}/raw_{tag}.stderr.txt','w').write(p.stderr)
open(f'{A}/raw_{tag}.cmd.txt','w').write('MAXD=15 INIT_LOG2=28 '+' '.join(cmd)+f'\nrc={p.returncode} wall_s={wall:.1f}\n')
# cleanup this task's layer files for this tag only
for f in glob.glob(f'{W}/*{tag}*'): os.remove(f)
dl=[l for l in p.stderr.splitlines() if 'cap=' in l and ' d=' in l]
last=dl[-1] if dl else None
depth=int(re.search(r' d=(\d+)',last).group(1)) if last else 0
ended='timeout' if p.returncode==124 else ('finished' if re.search(r'depth=\d+ (CLOSED|STOPPED)',p.stdout) else f'rc{p.returncode}')
m0=re.search(r'depth=(\d+) (CLOSED|STOPPED)',p.stdout)
if m0 and ended=='finished':
    ended = 'closed_or_bfs_exhausted' if m0.group(2)=='CLOSED' else ('maxd_reached' if depth>=15 else 'budget_stopped')
recs=[]; out=[]
res={'seed':seed,'cap':int(cap),'maxd':15,'depth_reached':depth,'last_stderr':last,'bestAC':None,'bestSAC':None,'ended':ended,'wall_s':round(wall,1),'stdout_head':p.stdout.splitlines()[:2],'checks':[]}
mm=re.search(r'\] AC (\d+) PATH ([\d ]+)',p.stdout); ms=re.search(r'\] SAC (\d+) PATH ([\d ]+)',p.stdout)
acc=C['ac-06045']; sacc=C['sac-06045']
def vfy(cid,path,spec):
    return specs.verify_challenge(C[cid],path,spec,LIM)
if mm:
    tail=list(map(int,mm.group(2).split())); full=pre+tail
    v=vfy('ac-06045',full,'ac-r2-v1'); res['bestAC']={'tail_len':int(mm.group(1)),'full_len':len(full),'verified':bool(v.get('ok')),'v':{k:v[k] for k in v if k in('ok','code','length')}}
    out.append({'id':'ac-06045','ac':full})
    f2=full+[16,15]; v2=vfy('sac-06045',f2,'sac-r8-v1'); res['checks'].append({'kind':'AC+[16,15] as sac','len':len(f2),'ok':bool(v2.get('ok')),'code':v2.get('code')})
    out.append({'id':'sac-06045','sac':f2})
if ms:
    tail=list(map(int,ms.group(2).split())); full=pre+tail
    v=vfy('sac-06045',full,'sac-r8-v1'); res['bestSAC']={'tail_len':int(ms.group(1)),'full_len':len(full),'verified':bool(v.get('ok')),'v':{k:v[k] for k in v if k in('ok','code','length')}}
    out.append({'id':'sac-06045','sac':full})
    if seed=='b12':
        t2=[BACK[x] for x in tail[:-2]]; ac12=A12+t2
        end=replay(ac12); ok=end==('x','y')
        v=vfy('ac-06045',ac12,'ac-r2-v1')
        res['a12_twin']={'ac_len':len(ac12),'ends_xy':ok,'verified':bool(v.get('ok')),'v':{k:v[k] for k in v if k in('ok','code','length')}}
        out.append({'id':'ac-06045','ac':ac12})
        f2=ac12+[16,15]; v2=vfy('sac-06045',f2,'sac-r8-v1'); res['a12_twin']['plus_16_15_as_sac']={'len':len(f2),'ok':bool(v2.get('ok')),'code':v2.get('code')}
        out.append({'id':'sac-06045','sac':f2})
with open(f'{A}/out.jsonl','a') as f:
    for o in out: f.write(json.dumps(o)+'\n')
    f.write(json.dumps({'record':True,**res})+'\n')
print(json.dumps(res,indent=1))
