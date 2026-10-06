# SCRIPT: NEWTARGET_WORKER  runs rows from a list one at a time (free-depth P2 dual beam W 100000, DMAX record+20), then:
# replays the AC route on the official core, runs the tight road DP on it, writes the shortest checked AC line and its SAC twin
# (+[16,15]) to sweeps/git (all roads) and to queue/ if it ties/beats the board record. Results appended to nt_results.jsonl.
import json,sys,subprocess,time,os,gzip,glob
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'; H='/home/claude/rally/research/acc/live'
sys.path.insert(0,S+'/upgh'); import skel_dp_fixed as SD
core=SD.core; T=SD.T
def board(pref):
    d=json.load(gzip.open(sorted(glob.glob(H+'/boards/'+pref+'_2026*.json.gz'))[-1]))['data']['items']
    return {x['challengeId']:(x.get('currentBestLength'),x.get('kTeams'),x.get('status')) for x in d}
rows=sys.argv[1].split(',')
for cid in rows:
    B=board('ac'); SB=board('stable_ac'); rec,k,st=B[cid]
    dmax=int(os.environ['NT_DMAX']) if (rec is None or os.environ.get('NT_DMAX')) else rec+int(os.environ.get('NT_EXTRA','20'))
    subprocess.run([S+'/upgh/nt_run.sh',cid,str(dmax)])
    o=open(S+f'/upgh/nt_{cid}.out').read(); ac=None
    for l in o.splitlines():
        if l.startswith('AC ') and 'PATH' in l: ac=[int(x) for x in l.split('PATH')[1].split()]
    res=dict(id=cid,record=rec,k=k,beam=len(ac) if ac else None)
    if ac and core.verify(T[cid],ac,'ac-r2-v1',SD.rl.LIMITS)['ok']:
        import commute_clean as CC; q=CC.clean(ac)
        if len(q)<len(ac) and core.verify(T[cid],q,'ac-r2-v1',SD.rl.LIMITS)['ok']: ac=q   # UPG-H song-4 commute cleanup
        x=SD.run(cid,ac,secs=120); best=x if isinstance(x,list) and len(x)<len(ac) and core.verify(T[cid],x,'ac-r2-v1',SD.rl.LIMITS)['ok'] else ac
        res.update(dp=len(best)); sac=best+[16,15]; srec,sk,_=SB.get('s'+cid,(None,None,None))
        os.makedirs(H+'/sweeps/git',exist_ok=True)
        with open(H+'/sweeps/git/newtarget_roads_20260930.txt','a') as f:
            f.write(f"# git new-target lane (free-depth P2 dual W100k + DP), official core ok, AC {len(best)} vs record {rec} k{k}\n{cid}: {json.dumps(best)}\n")
            f.write(f"# SAC twin (+[16,15]) {len(sac)} vs record {srec} k{sk}\ns{cid}: {json.dumps(sac)}\n")
        q=[]
        if rec is None or len(best)<=rec: q.append((cid,best,rec,k))   # unsolved row: any verified route is a first solve
        if (srec is None and rec is None) or (srec and len(sac)<=srec): q.append(('s'+cid,sac,srec,sk))
        for c,p,r,kk in q:
            open(H+'/queue/'+time.strftime('%Y%m%dT%H%M%SZ',time.gmtime())+'_git_'+c+'.txt','w').write(f"# git new target, len {len(p)} record {r} k{kk}, official core ok\n{c}: {json.dumps(p)}\n")
        res.update(queued=[c for c,*_ in q])
    open(S+'/upgh/nt_results.jsonl','a').write(json.dumps(res)+'\n'); print(res,flush=True)
