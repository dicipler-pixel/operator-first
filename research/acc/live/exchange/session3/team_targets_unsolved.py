# /tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpadIPT: TEAM_TARGETS_UNSOLVED  First-solve targets from the twin test (Mixer 5.2 good-run profile).
# Every unsolved AC row followed its closest good run for up to 20 steps (width 300). Control on 300 solved rows:
# the length drop separates solved from unsolved starts (AUC 0.938); staying with the twin does not (0.474).
# Target = unsolved row whose length DROPS while following its twin, ranked by drop, then opening matches (AUC 0.682).
import json,gzip,glob
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'
U=[json.loads(l) for l in open(S+'/unknown/twin_all_W300.jsonl')]; U=[u for u in U if 'error' not in u and u['drop']>0]
skip={r if isinstance(r,str) else (r.get('id') or r.get('challenge_id')) for r in json.load(open('research/acc/live/AK3_CLASS_ROWS.json'))['rows']}
skip|={'ac-09839','ac-09311','ac-06403','ac-04718','ac-05378','ac-02257'}
active=set()
for f in glob.glob('research/acc/live/targets_*2026092[89]*.json'):
    try:
        for r in json.load(open(f)): active.add(r['id'] if isinstance(r,dict) else r)
    except Exception: pass
out=[dict(id=u['id'],start_len=u['start_total'],len_reached=u['min_total'],drop=u['drop'],opening_matches=u['opening_matches'],
          twin=u['twin'],twin_len=u['twin_n'],first_eye_to_leave=u['first_leave'],on_active_list=u['id'] in active)
     for u in U if u['id'] not in skip]
out.sort(key=lambda x:(x['on_active_list'],-x['drop'],-x['opening_matches'],x['start_len']))
json.dump(out,open('research/acc/live/targets_git_unsolved_twin_20260929T2030Z.json','w'),indent=0)
import collections
print(len(out),'unsolved targets | not on active lists',sum(not x['on_active_list'] for x in out),'| drop sizes',sorted(collections.Counter(min(x['drop'],10) for x in out).items()))
