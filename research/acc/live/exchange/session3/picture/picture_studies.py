# /tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpadIPT: ACC_FULL_PICTURE_STUDIES  Mixer 5.2 studies from all 1,746 verified paths.
# (1) one study per eye: mean reading of each group (at record / above 1-3 / above 4+, record band 25-50) at every
#     'moves still to go', aligned at the finish; a sample count channel is kept per group.
# (2) the same-row pair with the largest gap: record path vs our path, all six eyes, aligned at the finish.
import json,statistics
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'; D=json.load(open(S+'/picture/all_paths_eyes.json')); P=D['paths']; EN=D['eye_names']
LAB={'total':'Total relator length','kappa':'RELATION log|kappa-18|','scale':'SCALE Sanov stretch','ledger':'Exponent ledger distance','grams2':'Cyclic 2-letter patterns','down':'Moves that shorten from here'}
grp={'at_record':[p for p in P if p['status']=='at_record' and 25<=p['record']<=50],
     'above_1_3':[p for p in P if p['status']=='above' and p['gap']<=3 and 25<=p['record']<=50],
     'above_4up':[p for p in P if p['status']=='above' and p['gap']>=4 and 25<=p['record']<=50]}
COL={'at_record':'#58c4dd','above_1_3':'#f2a65a','above_4up':'#e0605e'}
H=60; x=list(range(-H,1))
for j,e in enumerate(EN):
    tr=[]
    for g,G in grp.items():
        vals=[];cnt=[]
        for k in range(H,-1,-1):
            v=[p['eyes'][-1-k][j] for p in G if len(p['eyes'])>k]
            vals.append(statistics.mean(v) if len(v)>=5 else None); cnt.append(float(len(v)))
        tr.append(dict(id=g,label=f'{g.replace("_"," ")} mean ({len(G)} paths)',unit=LAB[e],source='all verified paths, Git 2026-09-29',values=vals,color=COL[g],defaultRoute='y'))
    json.dump(dict(schema='compound-eye-traces-v1',id='picture_'+e,title=f'Every path we hold, by group: {LAB[e]}',
        description='Means over all verified paths in the record band 25-50; blue = at record, orange = 1-3 over, red = 4+ over. Aligned at the finish.',
        context=dict(object_id='acc_all_verified_paths',model_id='ac-r2-v1',coordinate='moves still to go',x_unit='moves',source_stage='evaluated'),
        x=x,traces=tr),open(S+'/picture/picture_'+e+'.traces.json','w'))
by={}
for p in P: by.setdefault(p['id'],[]).append(p)
best=None
for cid,ps in by.items():
    R=[p for p in ps if p['status']=='at_record']; O=[p for p in ps if p['status']=='above' and p['gap']<=10]
    if R and O:
        r=min(R,key=lambda p:p['n']); o=max(O,key=lambda p:p['gap'])
        if best is None or o['gap']>best[1]['gap']: best=(r,o)
r,o=best; Hn=len(o['eyes'])-1; x=list(range(-Hn,1)); tr=[]
for j,e in enumerate(EN):
    for kind,p,col in (('record',r,'#58c4dd'),('ours',o,'#f2a65a')):
        v=[None]*(Hn+1-len(p['eyes']))+[float(z[j]) for z in p['eyes']]
        tr.append(dict(id=f'{e}_{kind}',label=f'{LAB[e]} - {kind} ({p["n"]} moves)',unit=LAB[e],source=p['source'],values=v,color=col,defaultRoute='y',defaultEnabled=e in ('total','kappa','scale')))
json.dump(dict(schema='compound-eye-traces-v1',id='pair_'+r['id'].replace('-','_'),title=f'{r["id"]}: record path ({r["n"]}) vs our path ({o["n"]}), same row',
    description='Same start, same eyes, aligned at the finish.',context=dict(object_id=r['id'],model_id='ac-r2-v1',coordinate='moves still to go',x_unit='moves',source_stage='evaluated'),
    x=x,traces=tr),open(S+'/picture/pair_study.traces.json','w'))
print('pair row',r['id'],r['n'],'vs',o['n'])
