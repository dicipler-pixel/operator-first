# SCRIPT: ACC_SCALE_TARGETS  high-value AC rows we do not hold whose start is STRETCHED (scale percentile >= 0.75 at its length)
# Excludes AK(3)-class rows, the owner's reserved rows, and rows already on an active lane list. Adds our best known length.
import json,gzip,glob,os
L='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad/acc_private/ladder'
rows=json.load(open(L+'/flat_team_rows.json'))
B={r['challengeId']:(r['currentBestLength'],r['kTeams']) for r in next(v for v in json.load(gzip.open(sorted(glob.glob('research/acc/live/boards/stable_ac_2026*.json.gz'))[-1]))['data'].values() if isinstance(v,list))}
skip={r if isinstance(r,str) else (r.get('id') or r.get('challenge_id')) for r in json.load(open('research/acc/live/AK3_CLASS_ROWS.json'))['rows']}
skip|={'ac-09839','ac-09311','ac-06403','ac-04718','ac-05378','ac-02257'}
active=set()
for f in glob.glob('research/acc/live/targets_*2026092[89]*.json'):
    try:
        for r in json.load(open(f)): active.add(r['id'] if isinstance(r,dict) else r)
    except Exception: pass
best={}
for f in glob.glob('research/acc/live/sweeps/*_cap.jsonl')+glob.glob('/tmp/claude-0/*/*/scratchpad/work/*_cap.jsonl'):
    for l in open(f):
        try: d=json.loads(l)
        except Exception: continue
        c=d.get('id'); a=d.get('ac_len')
        if isinstance(c,str) and a: best[c]=min(best.get(c,999),a)
out=[]
for r in rows:
    if r['held'] or r['ps']<0.75 or r['k']>2 or r['rec']<30 or r['id'] in skip: continue
    sac=B.get('s'+r['id'])
    v=2**(1-r['k'])+(2**(1-sac[1]) if sac else 0)
    out.append(dict(id=r['id'],ac_record=r['rec'],k=r['k'],sac_record=sac[0] if sac else None,sac_k=sac[1] if sac else None,
                    scale_pct=round(r['ps'],3),relation_pct=round(r['pr'],3),start_len=r['L'],our_best_ac=best.get(r['id']),
                    on_active_list=r['id'] in active,value=round(v,3)))
out.sort(key=lambda x:(x['on_active_list'],-x['value'],-x['scale_pct'],x['ac_record']))
json.dump(out,open(L+'/scale_targets.json','w'),indent=0)
print(len(out),'rows; not on an active list:',sum(not x['on_active_list'] for x in out))
for x in out[:25]: print(x)
