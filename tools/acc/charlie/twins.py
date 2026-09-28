# SCRIPT: CHARLIE_TWINS -- carry a verified path to every pool row that is an exact image of its row
# under a letter automorphism (signed permutation of x, y: 8 maps) and/or relator swap (x2).
# The moves transform exactly: swap exchanges moves 0<->1, 2<->4, 3<->5, 6..9<->10..13;
# a letter map sends a conjugation by g to the conjugation by the image of g; inversion and
# multiplication moves are unchanged by a letter map. Every carried path is replayed by the
# official verifier; only accepted lines are printed.
import json, os, sys, itertools
SAIR_TOOLS = os.environ.get('SAIR_TOOLS', os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SAIR/competition/tools')))
sys.path.insert(0, SAIR_TOOLS)
from verifier import core
M=json.load(open(os.path.join(SAIR_TOOLS, 'verifier/data/manifest.json')))
POOL={c['challenge_id']:c for c in M['challenges']}; LIM=M['limits']
KEY={}
for cid,c in POOL.items(): KEY.setdefault((tuple(c['initial_relators'][0]),tuple(c['initial_relators'][1])),[]).append(cid)
GENS=[1,-1,2,-2]
def maps():
    for perm in ((1,2),(2,1)):
        for sx in (1,-1):
            for sy in (1,-1):
                yield {1:sx*perm[0],-1:-sx*perm[0],2:sy*perm[1],-2:-sy*perm[1]}
def carry(cid,path):
    c=POOL[cid]; r0,r1=map(tuple,c['initial_relators']); out=[]
    for f in maps():
        for swap in (False,True):
            a=tuple(f[x] for x in r0); b=tuple(f[x] for x in r1)
            if swap: a,b=b,a
            for tid in KEY.get((a,b),[]):
                if tid==cid: continue
                p=[]
                for m in path:
                    if m>=6:
                        rel=0 if m<=9 else 1; g=GENS[(m-6)%4]; g2=f[g]; rel2=rel^1 if swap else rel
                        m2=(6 if rel2==0 else 10)+GENS.index(g2)
                    else:
                        m2={0:1,1:0,2:4,4:2,3:5,5:3}[m] if swap else m
                    p.append(m2)
                v=core.verify(POOL[tid],p,'ac-r2-v1',LIM)
                out.append((tid,swap,f,v.get('ok'),len(p),p))
    return out
if __name__=='__main__':
    src=sys.argv[1]; path=json.loads(sys.argv[2])
    for tid,swap,f,ok,n,p in carry(src,path):
        print(tid,'swap' if swap else '', f, 'ok' if ok else 'FAIL', n)
        if ok: print('%s: %s'%(tid,json.dumps(p)))
    print('done')
