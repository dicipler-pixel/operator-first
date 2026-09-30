# SCRIPT: GOOD_RUNS_STUDIES  Every good run (all 433 verified paths at record) into Mixer 5.2, one trace per run,
# aligned at the finish. Mixer takes <= 64 traces per study, so runs go in batches of 64 ordered by record length.
# One set of studies per eye (total, kappa, scale, ledger, grams2, down).
import json
E=json.load(open('all_paths_eyes.json')); EN=E['eye_names']
G=sorted([p for p in E['paths'] if p['status']=='at_record'],key=lambda p:(p['record'],p['id']))
LAB={'total':'Total relator length','kappa':'RELATION log|kappa-18|','scale':'SCALE Sanov stretch','ledger':'Exponent ledger distance','grams2':'Cyclic 2-letter patterns','down':'Moves that shorten from here'}
made=[]
for b in range(0,len(G),64):
    B=G[b:b+64]; H=max(len(p['eyes']) for p in B)-1; x=list(range(-H,1))
    for j,e in enumerate(EN):
        tr=[dict(id=f"{p['id']}_{i}",label=f"{p['id']} record {p['record']}",unit=LAB[e],source=p['source'],
                 values=[None]*(H+1-len(p['eyes']))+[float(z[j]) for z in p['eyes']],defaultRoute='y') for i,p in enumerate(B)]
        sid=f"good_{e}_b{b//64+1}"
        json.dump(dict(schema='compound-eye-traces-v1',id=sid,title=f"Good runs {b+1}-{b+len(B)} (records {B[0]['record']}-{B[-1]['record']}): {LAB[e]}",
            description='Every verified path at record, one trace per run, aligned at the finish.',
            context=dict(object_id='acc_good_runs',model_id='ac-r2-v1',coordinate='moves still to go',x_unit='moves',source_stage='evaluated'),
            x=x,traces=tr),open(f'studies_good/{sid}.traces.json','w'))
        made.append(sid)
print(len(G),'good runs,',len(made),'studies')
