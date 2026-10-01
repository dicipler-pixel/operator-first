import sys, json
from common import core
W={1:'x',-1:'X',2:'y',-2:'Y'}
def s(w): return ''.join(W[g] for g in w) or '1'
def parse(t): 
    M={'x':1,'X':-1,'y':2,'Y':-2}; return tuple(M[c] for c in t)
NAMES={0:'inv0',1:'inv1',2:'r0*=r1',3:'r0*=R1',4:'r1*=r0',5:'r1*=R0',6:'r0^x',7:'r0^X',8:'r0^y',9:'r0^Y',10:'r1^x',11:'r1^X',12:'r1^y',13:'r1^Y'}
def trace(start, path, out=sys.stdout):
    st=start; print('%3s %-8s %-7s %4s  %s' % ('i','move','total','', 'state'), file=out)
    print('%3s %-8s %3d       (%s, %s)' % ('', 'start', len(st[0])+len(st[1]), s(st[0]), s(st[1])), file=out)
    for i,m in enumerate(path):
        st=core.apply_move(st,m); print('%3d %-8s %3d       (%s, %s)' % (i, NAMES[m], len(st[0])+len(st[1]), s(st[0]), s(st[1])), file=out)
    return st
if __name__=='__main__':
    r0,r1=sys.argv[1].split(','); path=json.loads(sys.argv[2])
    trace((parse(r0),parse(r1)), path)
