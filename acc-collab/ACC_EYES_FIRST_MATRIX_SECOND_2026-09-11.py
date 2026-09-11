#!/usr/bin/env python3
import json, csv, statistics, time, importlib.util, sys
from pathlib import Path

def load_engine(path):
    spec=importlib.util.spec_from_file_location('eng', path)
    eng=importlib.util.module_from_spec(spec); sys.modules['eng']=eng; spec.loader.exec_module(eng)
    return eng

eng=None

def eye_record(cid, desc, p):
    E=eng.exponent_matrix(p)
    lens=[len(r) for r in p.relators]
    cyc_lens=[eng.cyclic_reduced_length(r) for r in p.relators]
    det=E[0][0]*E[1][1]-E[0][1]*E[1][0]
    neigh=[]
    for mid in range(14):
        q=eng.apply_move(p, eng.sair_id_to_move(mid), False)
        neigh.append({'move':mid,'L':q.total_length,'abel_l1':eng.exponent_l1_distance(q,False),'cyc_excess':eng.cyclic_excess(q),'cancel_gain':eng.cancellation_gain(q)})
    return {'challenge_id':cid,'description':desc,'eyes':{
        'word_length':{'r0':lens[0],'r1':lens[1],'total':sum(lens),'balance':abs(lens[0]-lens[1])},
        'cyclic':{'r0':cyc_lens[0],'r1':cyc_lens[1],'excess':eng.cyclic_excess(p)},
        'abelian':{'matrix':[list(E[0]),list(E[1])],'det':det,'l1_to_identity':eng.exponent_l1_distance(p,False)},
        'cancellation':{'best_gain':eng.cancellation_gain(p)},'one_step':neigh}}

def zrank(vals, reverse=False):
    n=len(vals); order=sorted(range(n), key=lambda i: vals[i], reverse=reverse)
    rank=[0.0]*n
    for k,i in enumerate(order): rank[i]=k/(n-1 if n>1 else 1)
    return rank

def main(inp, outdir, engine=None):
    global eng
    engine=Path(engine) if engine else Path(__file__).with_name('ACC_Cosmic_Matrix_Mixer_LIVE_2026-09-11.py')
    eng=load_engine(engine)
    outdir=Path(outdir); outdir.mkdir(parents=True, exist_ok=True)
    rows=eng.load_sair_jsonl(inp)
    allrecs=[]; t=time.time()
    with (outdir/'EYES_ALL_RAW.jsonl').open('w',encoding='utf-8') as f:
      for i,(cid,desc,p) in enumerate(rows,1):
        r=eye_record(cid,desc,p); allrecs.append(r); f.write(json.dumps(r,separators=(',',':'))+'\n')
        if i%1000==0: print('eyes',i,'/',len(rows),flush=True)
    L=[r['eyes']['word_length']['total'] for r in allrecs]; bal=[r['eyes']['word_length']['balance'] for r in allrecs]
    cyc=[r['eyes']['cyclic']['excess'] for r in allrecs]; ab=[r['eyes']['abelian']['l1_to_identity'] for r in allrecs]
    cg=[r['eyes']['cancellation']['best_gain'] for r in allrecs]
    stepL=[min(x['L'] for x in r['eyes']['one_step']) for r in allrecs]; stepAb=[min(x['abel_l1'] for x in r['eyes']['one_step']) for r in allrecs]
    pL=zrank(L); pbal=zrank(bal); pcyc=zrank(cyc); pab=zrank(ab); pcg=zrank(cg,reverse=True); psL=zrank(stepL); psA=zrank(stepAb)
    matrix=[]
    for i,r in enumerate(allrecs):
      sets={'compression_set':0.55*pL[i]+0.30*psL[i]+0.15*pcg[i],'abelian_set':0.55*pab[i]+0.30*psA[i]+0.15*pL[i],'cyclic_set':0.55*pcyc[i]+0.25*pL[i]+0.20*pcg[i],'balance_set':0.50*pbal[i]+0.30*pL[i]+0.20*pcyc[i]}
      combined=min(sets.values())*0.55 + statistics.mean(sets.values())*0.45
      matrix.append({'challenge_id':r['challenge_id'],'sets':sets,'matrix_score':combined,'eyes_summary':{'L':L[i],'balance':bal[i],'cyc':cyc[i],'abel_l1':ab[i],'cancel_gain':cg[i],'best_1step_L':stepL[i],'best_1step_abel':stepAb[i]}})
    matrix.sort(key=lambda x:(x['matrix_score'],x['challenge_id']))
    for k,m in enumerate(matrix,1): m['matrix_rank']=k
    (outdir/'MATRIX_AFTER_EYES.json').write_text(json.dumps(matrix,indent=2),encoding='utf-8')
    with (outdir/'MATRIX_RANKING.csv').open('w',newline='',encoding='utf-8') as f:
      w=csv.writer(f); w.writerow(['rank','challenge_id','matrix_score','L','balance','cyc','abel_l1','cancel_gain','best_1step_L','best_1step_abel','best_set'])
      for m in matrix:
        s=m['eyes_summary']; best=min(m['sets'],key=m['sets'].get)
        w.writerow([m['matrix_rank'],m['challenge_id'],m['matrix_score'],s['L'],s['balance'],s['cyc'],s['abel_l1'],s['cancel_gain'],s['best_1step_L'],s['best_1step_abel'],best])
    manifest={'problems':len(rows),'order':'ALL EYES RAW FIRST; SET OUTPUTS SECOND; MATRIX COMBINATION THIRD; SEARCH LAST','seconds':time.time()-t,'files':['EYES_ALL_RAW.jsonl','MATRIX_AFTER_EYES.json','MATRIX_RANKING.csv']}
    (outdir/'SCAN_MANIFEST.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print(json.dumps(manifest,indent=2))

if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser(); ap.add_argument('input'); ap.add_argument('outdir'); ap.add_argument('--engine'); a=ap.parse_args(); main(a.input,a.outdir,a.engine)
