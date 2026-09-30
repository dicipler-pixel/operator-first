"""Opposite approach for first solves: deep two-eyes beams from the three twins of each unsolved row (relators swapped,
x<->y, letters inverted); paths mapped back by exact move permutations and replayed with the official core."""
import sys, json, subprocess, os, random
S='/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad'
sys.path.insert(0,S+'/sair/competition/tools'); from verifier import core
m=json.load(open(S+'/sair/competition/tools/verifier/data/manifest.json')); C={c['challenge_id']:c for c in m['challenges']}
def tw(s,v):
    r0,r1=s
    if v=='swap-relators': return (r1,r0)
    f={1:2,-1:-2,2:1,-2:-1} if v=='swap-xy' else {1:-1,-1:1,2:-2,-2:2}
    return (tuple(f[t] for t in r0),tuple(f[t] for t in r1))
rng=random.Random(1)
def rs():
    def w():
        o=[]
        while len(o)<rng.randint(3,9):
            t=rng.choice((1,-1,2,-2))
            if o and o[-1]==-t: continue
            o.append(t)
        return tuple(o)
    return (w(),w())
V=['swap-relators','swap-xy','invert-letters']; PERM={}
for v in V:
    p={}
    for mv in range(14):
        c=set(range(14))
        for _ in range(40):
            s=rs(); want=tw(core.apply_move(s,mv),v); c={x for x in c if core.apply_move(tw(s,v),x)==want}
        p[min(c)]=mv
    PERM[v]=p
E={1:0,-1:1,2:2,-2:3}; ENV={'BEAM_H':'1','BEAM_DIV':'0.8','BEAM_P2':'2','BEAM_QUOTA':'16','BEAM_ELITE':'5000','BEAM_DUAL':'0.75'}
out=S+'/work/firstsolve_twins.jsonl'; done=set()
if os.path.exists(out): done={json.loads(l)['id'] for l in open(out)}
for t in json.load(open(S+'/work/firstsolve_targets.json')):
    cid=t['id']
    if cid in done: continue
    st=tuple(tuple(r) for r in C[cid]['initial_relators']); rec={'id':cid,'tries':[]}
    for v in V:
        s=tw(st,v); enc=[str(len(s[0]))]+[str(E[x]) for x in s[0]]+[str(len(s[1]))]+[str(E[x]) for x in s[1]]
        try: o=subprocess.run([S+'/dualbin/acc_beam',S+'/work/T9.tab','20000','250']+enc,capture_output=True,text=True,timeout=200,env={**os.environ,**ENV}).stdout
        except subprocess.TimeoutExpired: o=''
        path=None
        for line in o.splitlines():
            if line.startswith('AC ') and 'PATH' in line:
                q=[PERM[v][int(x)] for x in line.split('PATH')[1].split()]; z=st
                for mv in q: z=core.apply_move(z,mv)
                if z==((1,),(2,)): path=q
        rec['tries'].append({'twin':v,'ac':len(path) if path else None})
        if path: rec['ac']=path; break
    with open(out,'a') as f: f.write(json.dumps(rec)+'\n')
    print(cid,'SOLVED' if 'ac' in rec else 'none',len(rec.get('ac',[])),flush=True)
