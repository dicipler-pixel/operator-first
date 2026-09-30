"""Smith-chart reading of an AC path: each move is ROT (conjugation, length unchanged), CUT (length down),
CLIMB (length up), or INV. Also the 'phase table' of a state: for every rotation of each relator (and inverse),
how much a single multiplication cancels, and the rotation cost to get there."""
import sys, json
S='/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad'
sys.path.insert(0,S+'/sair/competition/tools'); from verifier import core
L={1:'x',-1:'X',2:'y',-2:'Y'}; w=lambda r:''.join(L[a] for a in r)
def kind(s,m,t):
    d=len(t[0])+len(t[1])-len(s[0])-len(s[1])
    if m in (0,1): return 'INV'
    if m>=6: return 'ROT' if d==0 else ('CUT' if d<0 else 'CLIMB')
    return 'CUT' if d<0 else ('CLIMB' if d>0 else 'FLAT')
def read(start,path,show=True):
    s=start; seq=[]
    for k,m in enumerate(path):
        t=core.apply_move(s,m); kd=kind(s,m,t); seq.append((kd,len(t[0])+len(t[1])-len(s[0])-len(s[1])))
        if show: print(f'{k+1:3d} m{m:2d} {kd:5s} {len(t[0])+len(t[1]):3d}  {w(t[0])[:40]:40s} {w(t[1])[:40]}')
        s=t
    return seq
def red(a):
    out=[]
    for x in a:
        if out and out[-1]==-x: out.pop()
        else: out.append(x)
    return out
def phase_table(s):
    """best single-cut gain for r_i <- rot(r_i)*rot(r_j)^e, with rotation costs (min steps each way)."""
    best=[]
    for i in (0,1):
        j=1-i; a,b=list(s[i]),list(s[j])
        for e in (1,-1):
            bb=b if e==1 else [-x for x in reversed(b)]
            for ra in range(len(a)):
                A=a[ra:]+a[:ra]
                for rb in range(len(bb)):
                    B=bb[rb:]+bb[:rb]
                    gain=len(A)+len(B)-len(red(A+B))
                    cost=min(ra,len(a)-ra)+min(rb,len(bb)-rb)
                    best.append((gain-len(B),cost,i,e,ra,rb))  # net change in r_i length is len(B)-gain
    best.sort(key=lambda x:(-x[0],x[1]))
    return best[:5]
if __name__=='__main__':
    m=json.load(open(S+'/sair/competition/tools/verifier/data/manifest.json')); C={c['challenge_id']:c for c in m['challenges']}
    cid=sys.argv[1]; path=json.loads(sys.argv[2])
    st=tuple(tuple(r) for r in C[cid]['initial_relators'])
    print(cid,'start',len(st[0])+len(st[1]),w(st[0]),w(st[1]))
    seq=read(st,path)
    from collections import Counter; print(Counter(k for k,_ in seq))
    print('phase table at start (net shrink, rot cost, target relator, sign, rotA, rotB):',phase_table(st))
