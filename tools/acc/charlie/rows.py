# SCRIPT: ACC_ROWS -- official initial relators for a challenge id, as acc_disk state strings
import json, os, sys
SAIR_TOOLS = os.environ.get('SAIR_TOOLS', os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../SAIR/competition/tools')))
M=json.load(open(os.path.join(SAIR_TOOLS, 'verifier/data/manifest.json')))
L={1:'x',-1:'X',2:'y',-2:'Y'}
def find(cid):
    def walk(o):
        if isinstance(o,dict):
            if o.get('challenge_id')==cid: return o
            for v in o.values():
                r=walk(v)
                if r: return r
        elif isinstance(o,list):
            for v in o:
                r=walk(v)
                if r: return r
    return walk(M)
def state(cid):
    c=find(cid); r0,r1=c['initial_relators']; return ''.join(L[a] for a in r0)+','+''.join(L[a] for a in r1)
if __name__=='__main__':
    for cid in sys.argv[1:]:
        c=find(cid); print(cid, state(cid), 'limits', {k:v for k,v in c.items() if k not in ('initial_relators','target_relators','description')})
