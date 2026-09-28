"""Exact shortest AC path for a custom MS(n,w) start via acc_capped (cap, MAXD). usage: ms_exact.py WORD N CAP MAXD"""
import subprocess, sys, re, os
S=os.environ.get('ACC_SCRATCH', '.')  # folder holding acc_capped and work/T9.tab
w,n,cap,maxd=sys.argv[1],int(sys.argv[2]),sys.argv[3],sys.argv[4]
E={'x':0,'X':1,'y':2,'Y':3}
r0=w; r1='Y'*(n+1)+'X'+'y'*n+'x'
enc=[str(len(r0))]+[str(E[c]) for c in r0]+[str(len(r1))]+[str(E[c]) for c in r1]
W=f'{S}/work_ms_{w}_{n}'; os.makedirs(W,exist_ok=True)
env=dict(os.environ,MAXD=maxd,INIT_LOG2='24')
p=subprocess.run([S+'/acc_capped',S+'/work/T9.tab',cap,'150000000',W,f'm{n}',*enc],capture_output=True,text=True,env=env)
print(r0,r1); print('\n'.join(l for l in p.stdout.splitlines()))
subprocess.run(['rm','-rf',W])
