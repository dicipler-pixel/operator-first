# SCRIPT: ACC_DISK_XCHECK_MOVES -- every move of acc_disk against official verifier/core.py apply_move
import os, random, subprocess, sys
sys.path.insert(0,os.environ.get('SAIR_TOOLS', os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SAIR/competition/tools'))))
from verifier import core
L={1:'x',-1:'X',2:'y',-2:'Y'}; R={v:k for k,v in L.items()}
def s2(w): return ''.join(L[a] for a in w)
def rw(n):
    w=[]
    while len(w)<n:
        a=random.choice([1,-1,2,-2])
        if w and w[-1]==-a: continue
        w.append(a)
    return tuple(w)
random.seed(1); states=[]
for _ in range(4000):
    states.append((rw(random.randint(0,20)),rw(random.randint(0,20))))
states += [((1,),(2,)),((),()),((1,),(-1,)),((1,2),(-2,-1))]
args=[s2(a)+','+s2(b) for a,b in states]
bad=0; n=0
for i in range(0,len(args),500):
    out=subprocess.run([os.path.join(os.path.dirname(__file__), 'acc_disk'),'selftest']+args[i:i+500],capture_output=True,text=True).stdout.split('\n')
    for line in out:
        if not line: continue
        st,m,res=line.split(' ') if line.count(' ')==2 else (line.split(' ')+[''])[:3]
        a,b=st.split(','); s=(tuple(R[c] for c in a),tuple(R[c] for c in b))
        e=core.apply_move(s,int(m)); n+=1
        if s2(e[0])+','+s2(e[1])!=res: bad+=1
print('moves compared',n,'mismatches',bad)
