"""Rotation compressor (Smith-chart 'shortest arc'): between two moves that read or change relator i, the pure
rotations of r_i (length-preserving conjugations) only matter through their net cyclic shift. Replace each such
run by the shortest arc, placed just before the next move that touches r_i. Output is replayed with the official core."""
import sys, json
S='/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad'
sys.path.insert(0,S+'/sair/competition/tools'); from verifier import core
def tl(s): return len(s[0])+len(s[1])
def classify(s,m):
    t=core.apply_move(s,m)
    changed=[i for i in (0,1) if t[i]!=s[i]]
    rot = m>=6 and tl(t)==tl(s) and len(changed)==1 and sorted(t[changed[0]])==sorted(s[changed[0]]) and is_rot(s[changed[0]],t[changed[0]])
    return t,changed,rot
def is_rot(a,b):
    return len(a)==len(b) and any(a[k:]+a[:k]==b for k in range(len(a)))
def reads(m):  # which relators a move reads (besides the one it writes): multiplications read the other
    return {2:(0,1),3:(0,1),4:(0,1),5:(0,1)}.get(m,())
def rot_moves(s,i):
    out={}
    for m in range(6,14):
        t=core.apply_move(s,m)
        if t[1-i]==s[1-i] and t[i]!=s[i] and is_rot(s[i],t[i]): out[t[i]]=m
    return out
def compress(start,path):
    # pass: walk path; keep pending target word per relator (after rotations); flush before any move touching it
    s=start; out=[]; pend=[None,None]; virt=start
    def flush(i):
        nonlocal s
        tgt=pend[i]
        if tgt is None or tgt==s[i]: pend[i]=None; return
        n=len(s[i]); k=next(k for k in range(n) if s[i][k:]+s[i][:k]==tgt)
        # step toward the target the short way: try each rotation move, take the one reducing cyclic distance
        while s[i]!=tgt:
            opts=rot_moves(s,i); best=None
            for w,m in opts.items():
                kk=next(k for k in range(n) if w[k:]+w[:k]==tgt); d=min(kk,n-kk)
                if best is None or d<best[0]: best=(d,m,w)
            out.append(best[1]); s=core.apply_move(s,best[1])
        pend[i]=None
    for m in path:
        t,changed,rot=classify(virt,m)
        if rot:
            i=changed[0]; pend[i]=t[i]; virt=t; continue
        for i in set(changed)|set(reads(m)): flush(i)
        # also flush any relator whose virtual differs (safety)
        for i in (0,1):
            if pend[i] is not None and i not in changed and i not in reads(m) and m in (0,1) and i==m: flush(i)
        assert s==virt or all((pend[i] is not None) or s[i]==virt[i] for i in (0,1))
        s=core.apply_move(s,m); out.append(m); virt=t
        for i in (0,1):
            if pend[i] is None and s[i]!=virt[i]: pass
    for i in (0,1): flush(i)
    return out,s
if __name__=='__main__':
    m=json.load(open(S+'/sair/competition/tools/verifier/data/manifest.json')); C={c['challenge_id']:c for c in m['challenges']}
    cid=sys.argv[1]; p=json.loads(sys.argv[2]); st=tuple(tuple(r) for r in C[cid]['initial_relators'])
    q,end=compress(st,p); print(len(p),'->',len(q),'valid',end==((1,),(2,))); print(q)
