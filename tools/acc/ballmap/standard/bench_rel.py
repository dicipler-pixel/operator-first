import json,subprocess,os,sys
from multiprocessing import Pool
S=sys.argv[1]; cid=sys.argv[2]; W=sys.argv[3]
sys.path.insert(0,'/home/user/operator-first/tools/acc/upgh'); import symmetry_recog as SR; from verifier import core
road=json.load(open(S+'/mine3/%s.road'%cid))
st=[tuple(tuple(x) for x in SR.CH[cid]['initial_relators'])]
for m in road: st.append(core.apply_move(st[-1],m))
E={1:0,-1:1,2:2,-2:3}
def run(j):
    c,cfg=j; a,b=st[c]; p2,loop,reachw,relw=cfg
    env=dict(os.environ,BEAM_H='1',BEAM_DIV='0.8',BEAM_QUOTA='16',BEAM_ELITE='5000',BEAM_DUAL='0.75',BEAM_P2=p2,BEAM_LOOP=loop,BEAM_LOOPZ='5',BEAM_REACH=reachw,BEAM_REACHZ='5',BEAM_REL=relw,BEAM_RELB='0.5')
    p=subprocess.run([S+'/crel/bin/acc_beam',S+'/crel/bin/T8.tab',W,str(len(road)-c),str(len(a)),*[str(E[x]) for x in a],str(len(b)),*[str(E[x]) for x in b]],capture_output=True,text=True,env=env)
    r={l.split()[0]:l.split()[1] for l in p.stdout.splitlines() if l.startswith(('AC ','SAC '))}
    return c,cfg,r.get('AC')
cfgs=[('2','0','2','0'),('2','0','0','1'),('2','0','0','2'),('2','0','0','4'),('2','0','1','1')]
jobs=[(c,cfg) for c in range(1,len(road)-14,2) for cfg in cfgs]
res={}
with Pool(4) as P:
    for c,cfg,ac in P.imap_unordered(run,jobs): res[(c,cfg)]=ac
for cfg in cfgs:
    ok=[c for c in range(1,len(road)-14,2) if res[(c,cfg)] not in (None,'NONE')]
    print(cid,'W',W,'P2=%s loop=%s reach=%s rel=%s'%cfg,'recovers from cuts:',ok)
