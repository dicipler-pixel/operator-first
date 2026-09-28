import subprocess,sys,re,os,time
S='/tmp/claude-0/-home-user-operator-first/3cb9951d-8cab-51bf-a791-90f0d5bac4db/scratchpad'
E={'x':0,'X':1,'y':2,'Y':3}
def enc(a,b): return [str(len(a)),*[str(E[c]) for c in a],str(len(b)),*[str(E[c]) for c in b]]
env=dict(os.environ,BEAM_H='1',BEAM_DIV='0.8',BEAM_P2='2',BEAM_QUOTA='16',BEAM_ELITE='5000')
W=sys.argv[1]; D=sys.argv[2]
for spec in sys.argv[3:]:
    a,b=spec.split(',')
    t=time.time()
    p=subprocess.run([S+'/acc_beam_x',S+'/p2beam/T8.tab',W,D,*enc(a,b)],capture_output=True,text=True,env=env)
    m=re.search(r'^AC (\d+) PATH ([\d ]+)',p.stdout,re.M)
    print(spec, 'AC', m.group(1) if m else None, '%.0fs'%(time.time()-t), (m.group(2)[:200] if m else p.stdout[-200:]), flush=True)
