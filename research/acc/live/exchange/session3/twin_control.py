# SCRIPT: TWIN_CONTROL  Same twin test on SOLVED rows (their own good run excluded as twin), to learn whether the readings
# that rank unsolved rows (steps staying with the twin, length drop) actually separate solvable starts. 300 solved rows,
# fixed seed, same width and depth cap as the unsolved run.
import json,sys,random,multiprocessing as mp,statistics as st
sys.argv=[sys.argv[0],'300','0']
import twin_all as TA
TB=TA.TB; E=TA.E; good=TA.good; EN=TA.EN
starts=[(cid,p['eyes'][0]) for cid,p in good.items()]
sd=[st.pstdev(c) or 1 for c in zip(*[e for _,e in starts])]
random.seed(7); pick=random.sample(sorted(good),300)
def rowfor(cid):
    e0=good[cid]['eyes'][0]
    near=min((sum(((a-b)/c)**2 for a,b,c in zip(e0,e,sd))**.5,oid) for oid,e in starts if oid!=cid)
    return dict(id=cid,nearest=[(near[0],near[1],good[near[1]]['record'])])
if __name__=='__main__':
    f=open('twin_control_W300.jsonl','w')
    with mp.Pool(mp.cpu_count()) as P:
        for o in P.imap_unordered(TA.one,[rowfor(c) for c in pick],chunksize=2): f.write(json.dumps(o)+'\n'); f.flush()
    print('done')
