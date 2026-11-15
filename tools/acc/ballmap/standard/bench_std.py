import json,subprocess,os,sys
from multiprocessing import Pool
S=sys.argv[1]; cid=sys.argv[2]; W=sys.argv[3]
sys.path.insert(0,'/home/user/operator-first/tools/acc/upgh'); import symmetry_recog as SR; from verifier import core
road=json.load(open(S+'/mine3/%s.road'%cid))
st=[tuple(tuple(x) for x in SR.CH[cid]['initial_relators'])]
for m in road: st.append(core.apply_move(st[-1],m))
E={1:0,-1:1,2:2,-2:3}
CFG={'reach2':{'BEAM_REACH':'2'}, 'loopx2':{'BEAM_LOOPX':'2'}, 'peel0.25+loopx1':{'BEAM_PEEL':'0.25','BEAM_LOOPX':'1'},
     'rel0.5(base O)+loopx0.5':{'BEAM_REL':'0.5','BEAM_RELB':'0','BEAM_LOOPX':'0.5'}, 'reach2+loopx0.5':{'BEAM_REACH':'2','BEAM_LOOPX':'0.5'}}
def run(j):
    c,name=j; a,b=st[c]
    env=dict(os.environ,BEAM_H='1',BEAM_DIV='0.8',BEAM_QUOTA='16',BEAM_ELITE='5000',BEAM_DUAL='0.75',BEAM_P2='2',BEAM_REACHZ='5'); env.update(CFG[name])
    p=subprocess.run([S+'/cstd/bin/acc_beam',S+'/cstd/bin/T8.tab',W,str(len(road)-c),str(len(a)),*[str(E[x]) for x in a],str(len(b)),*[str(E[x]) for x in b]],capture_output=True,text=True,env=env)
    r={l.split()[0]:l.split()[1] for l in p.stdout.splitlines() if l.startswith(('AC ','SAC '))}
    return c,name,r.get('AC')
jobs=[(c,n) for c in range(1,len(road)-14,2) for n in CFG]
res={}
with Pool(4) as P:
    for c,n,ac in P.imap_unordered(run,jobs): res[(c,n)]=ac
for n in CFG:
    ok=[c for c in range(1,len(road)-14,2) if res[(c,n)] not in (None,'NONE')]
    print(cid,'W',W,n,'recovers from cuts:',ok)
