# /tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpadIPT: TEAM_TARGETS_SHAPE  Target list from the good-run shape (Mixer 5.2, 433 good runs): AC rows we hold 1-5 over the
# record whose best path misses at least one good-run trait (ledger climbs > 1, scale climbs above start, ledger peaks after
# kappa clears). Value = 2^(1-k) AC plus 2^(1-k) SAC when AC record + 2 <= SAC record (tie comes free via +[16,15]).
# Excludes AK(3)-class rows, the owner's reserved rows; marks rows on active lists.
import json,gzip,glob
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'
R=json.load(open(S+'/unknown/behind_targets.json'))
SB={r['challengeId']:(r['currentBestLength'],r['kTeams']) for r in next(v for v in json.load(gzip.open(sorted(glob.glob('research/acc/live/boards/stable_ac_2026*.json.gz'))[-1]))['data'].values() if isinstance(v,list))}
skip={r if isinstance(r,str) else (r.get('id') or r.get('challenge_id')) for r in json.load(open('research/acc/live/AK3_CLASS_ROWS.json'))['rows']}
skip|={'ac-09839','ac-09311','ac-06403','ac-04718','ac-05378','ac-02257'}
active=set()
for f in glob.glob('research/acc/live/targets_*2026092[89]*.json'):
    try:
        for r in json.load(open(f)): active.add(r['id'] if isinstance(r,dict) else r)
    except Exception: pass
out=[]
for r in R:
    if r['gap']>5 or r['shape_misses']==0 or r['id'] in skip: continue
    sac=SB.get('s'+r['id']); sac_free=bool(sac and sac[0] is not None and r['record']+2<=sac[0])
    v=2**(1-(r['k'] or 1))+(2**(1-sac[1]) if sac_free else 0)
    out.append(dict(id=r['id'],ac_record=r['record'],k=r['k'],our_best_ac=r['ours'],gap_ac=r['gap'],sac_record=sac[0] if sac else None,
        sac_k=sac[1] if sac else None,sac_tie_free=sac_free,value=round(v,3),misses=dict(ledger_climb=r['ledger_climb'],scale_climb=r['scale_climb'],order_broken=r['order_broken']),
        shape_misses=r['shape_misses'],on_active_list=r['id'] in active,our_path_source=r['source']))
out.sort(key=lambda x:(x['on_active_list'],x['gap_ac'],-x['value'],-x['shape_misses']))
json.dump(out,open('research/acc/live/targets_git_shape_20260929T1830Z.json','w'),indent=0)
print(len(out),'targets | not on active lists',sum(not x['on_active_list'] for x in out),'| total value %.1f'%sum(x['value'] for x in out),
      '| by gap',{g:sum(x['gap_ac']==g for x in out) for g in range(1,6)})
