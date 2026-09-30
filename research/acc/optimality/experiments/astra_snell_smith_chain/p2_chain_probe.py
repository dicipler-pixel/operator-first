"""Fixed follow-up: test the chain behind the actual production P2/H key."""
import hashlib
import json
import subprocess
import numpy as np
import run_chain_probe as p

rows = []
states = {}
manifest = json.loads((p.ROOT/'SAIR/competition/tools/verifier/data/manifest.json').read_text())
ch = {c['challenge_id']:c for c in manifest['challenges']}
for label, fn in [('primary','routes.json'), ('external','heldout_routes.json')]:
    for r in json.loads((p.HERE/fn).read_text()):
        assert p.core.verify(ch[r['id']],r['ac'],'ac-r2-v1',manifest['limits'])['ok']
        s = tuple(map(tuple,ch[r['id']]['initial_relators']))
        for i,m in enumerate(r['ac']):
            kids = [p.core.apply_move(s,j) for j in range(14)]
            for k in kids:
                if k not in states:
                    states[k] = len(states)
            rows.append(dict(group=label,id=r['id'],step=i,left=len(r['ac'])-i,
                             climb=sum(map(len,kids[m]))>sum(map(len,s)),
                             children=[states[k] for k in kids],move=m))
            s = kids[m]
enc = {1:0,-1:1,2:2,-2:3}
src = p.HERE/'score_kernel.c'
exe = p.ROOT/'work/astra_chain_scores'
subprocess.run(['gcc','-O3','-march=native','-o',str(exe),str(src),'-lm'],check=True)
stdin = ''.join(' '.join(str(x) for w in s for x in [len(w),*[enc[a] for a in w]])+'\n' for s in states)
ret = subprocess.run([str(exe)],input=stdin,text=True,capture_output=True,check=True)
sc = [tuple(map(int,l.split())) for l in ret.stdout.splitlines()]
assert len(sc) == len(states)
chain = []
for (s,i),(p2,h) in zip(states.items(),sc):
    assert p.hpriority(s) == h, (s,p.hpriority(s),h)
    chain.append(p.features(s)['chain'])
out = dict(production_acc_beam_sha256=hashlib.sha256((p.ROOT/'research/acc/optimality/acc_beam.c').read_bytes()).hexdigest(),
           unique_states=len(states),H_crosschecks=len(states),groups={})
detail = []
for r in rows:
    keys = [sc[i] for i in r['children']]
    ck = [(*sc[i],chain[i]) for i in r['children']]
    rec = {k:v for k,v in r.items() if k not in ('children','move')}
    for name,ks in [('P2_H',keys),('P2_H_chain',ck)]:
        chosen = ks[r['move']]
        rec[name] = (sum(x<chosen for x in ks)+.5*(sum(x==chosen for x in ks)-1))/13
    detail.append(rec)
for label in ('primary','external'):
    out['groups'][label] = {}
    for subset,pred in [('all',lambda r:True),('far',lambda r:r['left']>=10),('climb',lambda r:r['climb'])]:
        rr=[r for r in detail if r['group']==label and pred(r)]
        ids=sorted(set(r['id'] for r in rr))
        diffs=[np.mean([r['P2_H_chain']-r['P2_H'] for r in rr if r['id']==cid]) for cid in ids]
        rng=np.random.default_rng(20260929)
        bs=np.mean(rng.choice(diffs,(2000,len(diffs)),replace=True),axis=1)
        out['groups'][label][subset]=dict(steps=len(rr),path_count=len(ids),
            mean_rank={key:float(np.mean([r[key] for r in rr])) for key in ('P2_H','P2_H_chain')},
            path_mean_delta=float(np.mean(diffs)),path_bootstrap95=np.quantile(bs,[.025,.975]).tolist())
(p.HERE/'p2_results.json').write_text(json.dumps(out,indent=2)+'\n')
(p.HERE/'p2_step_scores.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in detail))
print(json.dumps(out,indent=2),flush=True)
