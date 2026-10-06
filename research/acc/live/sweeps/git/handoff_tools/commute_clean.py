# SCRIPT: COMMUTE_CLEAN  UPG-H's song-4 rule, own implementation: two AC moves commute when neither writes a relator the other reads or writes.
# A move m and a later inverse(m) with only m-commuting moves between them cancel: delete both. Repeat until nothing changes.
# Every cleaned road is replayed on the official core (kept only if it still reaches (x,y)).
INV=(0,1,3,2,5,4,7,6,9,8,11,10,13,12)
def rw(m):   # (reads, writes) as sets of relator indices
    if m in (0,1): return {m},{m}
    if m in (2,3): return {0,1},{0}
    if m in (4,5): return {0,1},{1}
    return ({0},{0}) if m<=9 else ({1},{1})
def commute(a,b):
    ra,wa=rw(a); rb,wb=rw(b)
    return not (wa&(rb|wb)) and not (wb&(ra|wa))
def clean(p):
    p=list(p); changed=True
    while changed:
        changed=False
        for i in range(len(p)):
            for j in range(i+1,len(p)):
                if p[j]==INV[p[i]]: del p[j]; del p[i]; changed=True; break
                if not commute(p[i],p[j]): break
            if changed: break
    return p
if __name__=='__main__':
    import sys,json,re,glob
    sys.path.insert(0,'/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad/acc_private/pool/ACC_Replay_Idea_Pool')
    import replay_loop as rl; from verifier import core; T=rl.load_targets()
    n=0; out=[]
    for f in glob.glob('/home/claude/rally/research/acc/live/sweeps/git/*.txt'):
        for m in re.finditer(r'^(ac-\d{5}):\s*(\[[\d,\s]+\])',open(f).read(),re.M):
            c=m.group(1); p=json.loads(m.group(2)); q=clean(p); n+=1
            if len(q)<len(p) and core.verify(T[c],q,'ac-r2-v1',rl.LIMITS)['ok']: out.append((c,len(p),q))
    print(n,'roads scanned |',len(out),'shortened:',[(c,a,len(q)) for c,a,q in out])
    json.dump(out,open('commute_out.json','w'))
