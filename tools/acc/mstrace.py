import sys,re
import os; sys.path.insert(0,os.environ.get('SAIR','SAIR')+'/competition/tools'); from verifier import core
E={'x':1,'X':-1,'y':2,'Y':-2}; L={1:'x',-1:'X',2:'y',-2:'Y'}
def rle(r):
    s=''.join(L[a] for a in r); return re.sub(r'(([xXyY])\2{3,})',lambda m:f'{m.group(2)}^{len(m.group(1))}',s)
def run(r0,r1,p,show=True):
    s=(tuple(E[c] for c in r0),tuple(E[c] for c in r1))
    if show: print('    ',rle(s[0]),rle(s[1]))
    for k,m in enumerate(p):
        s=core.apply_move(s,m)
        if show: print(f'{k+1:3d} m{m:2d} {rle(s[0]):22s} {rle(s[1])}')
    return s
if __name__=='__main__':
    n=int(sys.argv[1]); p=list(map(int,sys.argv[2:]))
    run('YXXyx','Y'*(n+1)+'X'+'y'*n+'x',p)
