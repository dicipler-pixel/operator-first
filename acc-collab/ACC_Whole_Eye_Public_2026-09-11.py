#!/usr/bin/env python3
"""ACC Whole Eye public collaboration router — 2026-09-11.

Public-safe version of Team Dicipler's live Compound Eye / Cosmic Matrix routing.
It contains no Discovery solution certificate and no private move sequence.

Order: official pool -> all-eyes matrix -> independent routing lanes -> two-step
next-space eye -> shared reverse target ball -> exact replay -> local private
ledger/output.
"""
from __future__ import annotations
import argparse, importlib.util, json, statistics, sys, time
from pathlib import Path


def load_engine(path: Path):
    spec=importlib.util.spec_from_file_location('acc_eng', path)
    eng=importlib.util.module_from_spec(spec)
    sys.modules['acc_eng']=eng
    spec.loader.exec_module(eng)
    return eng


def two_step_eye(eng,p):
    L0=p.total_length
    branch=[]; best2=10**9; bestA2=10**9; unique2=set(); enabling=0; first_improve=0
    for mid in range(14):
        q=eng.apply_move(p,eng.sair_id_to_move(mid),False)
        if q.total_length<L0: first_improve+=1
        useful=0
        for mid2 in range(14):
            z=eng.apply_move(q,eng.sair_id_to_move(mid2),False)
            unique2.add(z)
            best2=min(best2,z.total_length)
            bestA2=min(bestA2,eng.exponent_l1_distance(z,False))
            if (z.total_length<q.total_length or eng.exponent_l1_distance(z,False)<eng.exponent_l1_distance(q,False)):
                useful+=1
        branch.append(useful)
        if useful>=5: enabling+=1
    return {'unique_grandchildren':len(unique2),'best_2step_L':best2,'best_2step_abel':bestA2,'enabling_first_moves':enabling,'first_step_L_improvers':first_improve,'useful_branch_mean':sum(branch)/14,'useful_branch_max':max(branch),'useful_branch_var':statistics.pvariance(branch)}


def add_unique(dst,seen,seq,route,n):
    k=0
    for m in seq:
        cid=m['challenge_id']
        if cid in seen: continue
        dst.append({'m':m,'route':route}); seen.add(cid); k+=1
        if k>=n: return


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('pool_jsonl', type=Path)
    ap.add_argument('matrix_json', type=Path)
    ap.add_argument('outdir', type=Path)
    ap.add_argument('--engine', type=Path, default=Path(__file__).with_name('ACC_Cosmic_Matrix_Mixer_LIVE_2026-09-11.py'))
    ap.add_argument('--budget', type=int, default=18000)
    ap.add_argument('--select', type=int, default=64)
    ap.add_argument('--max-length', type=int)
    ap.add_argument('--exclude-ids', type=Path)
    a=ap.parse_args(); a.outdir.mkdir(parents=True,exist_ok=True)
    eng=load_engine(a.engine)
    rows={cid:p for cid,_,p in eng.load_sair_jsonl(a.pool_jsonl)}
    rank=json.loads(a.matrix_json.read_text(encoding='utf-8'))
    excluded=set()
    if a.exclude_ids and a.exclude_ids.exists():
        txt=a.exclude_ids.read_text(encoding='utf-8').strip()
        try:
            obj=json.loads(txt)
            if isinstance(obj,list):
                for x in obj: excluded.add(x if isinstance(x,str) else x.get('challenge_id'))
            elif isinstance(obj,dict): excluded.update(obj)
        except Exception:
            excluded.update(x.strip() for x in txt.splitlines() if x.strip())
    cands=[m for m in rank if m['challenge_id'] in rows and m['challenge_id'] not in excluded]
    if not cands: raise SystemExit('no candidates')

    # Route, don't vote: keep independent set frontiers plus matrix/diversity lanes.
    pool=[]; seen=set()
    add_unique(pool,seen,sorted(cands,key=lambda m:m['matrix_rank']),'matrix-frontier',90)
    setnames=list(cands[0]['sets'])
    for s in setnames:
        add_unique(pool,seen,sorted(cands,key=lambda m:(m['sets'][s],m['matrix_rank'])),f'set:{s}',45)
    maxrank=max(m['matrix_rank'] for m in cands)
    for lo,hi in [(1,500),(501,1500),(1501,3500),(3501,7000),(7001,maxrank)]:
        band=[m for m in cands if lo<=m['matrix_rank']<=hi]
        add_unique(pool,seen,sorted(band,key=lambda m:m['matrix_rank']),f'diversity:{lo}-{hi}',12)

    # Record the retina before selection.
    for r in pool: r['next_space_eye']=two_step_eye(eng,rows[r['m']['challenge_id']])
    retina=[{'challenge_id':r['m']['challenge_id'],'route':r['route'],'matrix_rank':r['m']['matrix_rank'],'old_eyes':r['m']['eyes_summary'],'sets':r['m']['sets'],'next_space_eye':r['next_space_eye']} for r in pool]
    (a.outdir/'ROUTED_RETINA_ALL.json').write_text(json.dumps(retina,indent=2),encoding='utf-8')

    lanes={
      'matrix-frontier':sorted(pool,key=lambda r:r['m']['matrix_rank']),
      'deep-enabling':sorted(pool,key=lambda r:(-r['next_space_eye']['enabling_first_moves'],-r['next_space_eye']['useful_branch_var'],r['m']['matrix_rank'])),
      'two-step-compression':sorted(pool,key=lambda r:(r['next_space_eye']['best_2step_L'],r['next_space_eye']['best_2step_abel'],r['m']['matrix_rank'])),
      'novel-mobility':sorted(pool,key=lambda r:(-r['next_space_eye']['unique_grandchildren'],-r['next_space_eye']['useful_branch_max'],r['m']['matrix_rank']))}
    selected=[]; sseen=set(); j=0
    while len(selected)<min(a.select,len(pool)):
        progressed=False
        for lname,seq in lanes.items():
            if j>=len(seq): continue
            r=seq[j]; cid=r['m']['challenge_id']
            if cid not in sseen:
                rr=dict(r); rr['selection_lane']=lname; selected.append(rr); sseen.add(cid); progressed=True
                if len(selected)>=a.select: break
        if not progressed and all(j>=len(v)-1 for v in lanes.values()): break
        j+=1
    (a.outdir/'SELECTED.json').write_text(json.dumps([{'challenge_id':r['m']['challenge_id'],'selection_lane':r['selection_lane'],'source_route':r['route'],'matrix_rank':r['m']['matrix_rank'],'next_space_eye':r['next_space_eye']} for r in selected],indent=2),encoding='utf-8')

    # One shared exact target memory, reused across selected cases.
    t=time.time(); rev=eng.OrdinaryReverseBall(6); shadow=eng.AbelianShadow2(12)
    print('reverse states',len(rev.depth),'built in',round(time.time()-t,3),'s')
    ledger=[]; sols=[]
    for i,r in enumerate(selected,1):
        cid=r['m']['challenge_id']; p=rows[cid]; t=time.time()
        path,stats=eng.routed_search(p,False,budget=a.budget,max_length=a.max_length,baseline_only=False,reverse_ball=rev,shadow=shadow,exact_forward_depth=2,shorten=True)
        rec={'set_index':i,'challenge_id':cid,'selection_lane':r['selection_lane'],'source_route':r['route'],'matrix_rank':r['m']['matrix_rank'],'next_space_eye':r['next_space_eye'],'solved':path is not None,'seconds':time.time()-t,'stats':stats}
        if path:
            ids=[eng.move_to_sair_id(x) for x in path]; ok,*_=eng.verify_sair_ids(p,ids)
            rec.update({'moves':ids,'length':len(ids),'verified':ok})
            if ok: sols.append(rec)
        rec['miss_trace']='SURFACED_VERIFIED' if rec.get('verified') else 'SEEN_BUT_NOT_SOLVED'
        ledger.append(rec)
        # Generated files below may contain live certificates: keep them local.
        (a.outdir/'LEDGER.private.json').write_text(json.dumps(ledger,indent=2),encoding='utf-8')
        (a.outdir/'SOLUTIONS.private.json').write_text(json.dumps(sols,indent=2),encoding='utf-8')
        print(i,cid,rec['miss_trace'],rec.get('length'),round(rec['seconds'],2))

if __name__=='__main__': main()
