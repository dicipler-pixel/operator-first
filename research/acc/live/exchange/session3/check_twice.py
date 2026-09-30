# SCRIPT: CHECK_TWICE  Check the unsolved twin list before it goes out, and run it backwards.
# 1. Replay: for 60 listed rows, rerun the twin beam, keep the path to the shortest state, replay it with the official core,
#    and confirm the drop is real (length after replay == reported min).
# 2. Twin-specific or not: same rows, same beam, but following (a) a RANDOM good run, (b) the FARTHEST good run (opposite),
#    (c) no twin at all (plain length beam). If they drop just as often, the signal is "a short beam finds a descent",
#    not the twin.
# 3. Control fairness: solved vs unsolved drop rate within the same start-length band.
import json,sys,random,statistics as st,collections,multiprocessing as mp
sys.argv=[sys.argv[0],'300','0']; import twin_all as TA
TB=TA.TB; good=TA.good; core=TB.core; T=TB.T
L=json.load(open('/home/claude/rally/research/acc/live/targets_git_unsolved_twin_20260929T2030Z.json')) if False else None
U={json.loads(l)['id']:json.loads(l) for l in open('twin_all_W300.jsonl')}
C=[json.loads(l) for l in open('twin_control_W300.jsonl')]
P=json.load(open('unknown_placed.json'))['rows']; near={r['id']:r for r in P}
starts=[(cid,p['eyes'][0]) for cid,p in good.items()]; sd=[st.pstdev(c) or 1 for c in zip(*[e for _,e in starts])]
dropped=sorted([u for u in U.values() if 'error' not in u and u['drop']>0],key=lambda u:-u['drop'])
random.seed(11); sample=dropped[:30]+random.sample(dropped[30:],30)
flat=random.sample([u for u in U.values() if 'error' not in u and u['drop']==0],30)
def cap(t): c=dict(t); c['eyes']=t['eyes'][:21]; return c
def run_one(args):
    cid,mode=args; r=near[cid]; e0=r['eyes']
    if mode=='twin': tw=good[r['nearest'][0][1]]
    elif mode=='random': tw=good[random.Random(hash(cid)%9999).choice(sorted(good))]
    elif mode=='farthest': tw=good[max(starts,key=lambda s:sum(((a-b)/c)**2 for a,b,c in zip(e0,s[1],sd)))[0]]
    if mode=='plain':
        tw=dict(good[r['nearest'][0][1]]); tw['eyes']=[[0,0,0,0,0,0]]*21   # every step's target = all-zero: pure closeness to the finish
    x=TB.beam(cid,cap(tw),300,False,extra=0)
    s=tuple(map(tuple,T[cid]['initial_relators'])); L0=sum(map(len,s))
    for m in x.get('path',[]): s=core.apply_move(s,m)
    return dict(id=cid,mode=mode,start=L0,min_total=x.get('min_total'),replayed=sum(map(len,s)),path_len=len(x.get('path',[])))
if __name__=='__main__':
    jobs=[(u['id'],m) for u in sample for m in ('twin','random','farthest','plain')]+[(u['id'],m) for u in flat for m in ('twin','random')]
    out=[]
    with mp.Pool(2) as Pl:
        for o in Pl.imap_unordered(run_one,jobs): out.append(o)
    json.dump(out,open('check_twice.json','w'))
    rep=[o for o in out if o['mode']=='twin' and o['id'] in {u['id'] for u in sample}]
    print('1. replay: twin drops reproduced and replay length == reported min on',sum(o['replayed']==o['min_total'] for o in rep),'of',len(rep),
          '| reproduced drop>0:',sum(o['start']-o['replayed']>0 for o in rep),'| same drop as the first run:',sum(U[o['id']]['drop']==o['start']-o['replayed'] for o in rep))
    for m in ('twin','random','farthest','plain'):
        X=[o for o in out if o['mode']==m and o['id'] in {u['id'] for u in sample}]
        print(f'2. listed rows, follow {m:8s}: drop>0 on {sum(o["start"]-o["replayed"]>0 for o in X)}/{len(X)}, mean drop {st.mean(o["start"]-o["replayed"] for o in X):.2f}')
    for m in ('twin','random'):
        X=[o for o in out if o['mode']==m and o['id'] in {u['id'] for u in flat}]
        print(f'2b. rows that did NOT drop, rerun follow {m:6s}: drop>0 on {sum(o["start"]-o["replayed"]>0 for o in X)}/{len(X)}')
    band=lambda n:min(n//4,8)
    cu=collections.defaultdict(list); cc=collections.defaultdict(list)
    for u in U.values():
        if 'error' not in u: cu[band(u['start_total'])].append(u['drop']>0)
    for c in C:
        if 'error' not in c: cc[band(c['start_total'])].append(c['drop']>0)
    print('3. drop rate by start length band (solved control | unsolved):')
    for b in sorted(set(cu)|set(cc)):
        if cc[b] and cu[b]: print(f'   start {4*b}-{4*b+3}: solved {100*st.mean(cc[b]):.0f}% (n={len(cc[b])}) | unsolved {100*st.mean(cu[b]):.0f}% (n={len(cu[b])})')
