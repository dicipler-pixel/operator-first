# SCRIPT: HELD  team held length per row id (ac-* and sac-* separately): min over accepted submissions (all mine_*.json) and the ledger snapshot.
# Rule (UPG-H 11:01Z): queue only if length < held AND <= live record.
import json,glob
H='/home/claude/rally/research/acc/'
def held():
    h={}
    for f in glob.glob(H+'live/mine_*.json'):
        try: it=json.load(open(f))['items']
        except Exception: continue
        for x in it:
            for r in x.get('results') or []:
                if r.get('ok') and r.get('length'): c=r['challenge_id']; h[c]=min(h.get(c,10**9),r['length'])
    for l in open(H+'upgh/ledger.jsonl'):
        e=json.loads(l)
        if e.get('kind')=='history.snapshot':
            for c,v in e['data'].get('best',{}).items(): h[c]=min(h.get(c,10**9),v)
    return h
def ok_to_queue(cid,length,record):
    return length<=record and length<held().get(cid,10**9)
if __name__=='__main__':
    h=held()
    for c in ('ac-02288','sac-02288','ac-04493','sac-04493','ac-06969','sac-06969','ac-00145','sac-00145'): print(c,h.get(c))
