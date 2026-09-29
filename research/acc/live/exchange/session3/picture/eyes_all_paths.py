# /tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpadIPT: ACC_EYES_ALL_PATHS  every verified path through the same eyes, one reading per state: total length, relation
# (log|kappa-18|, Sanov), scale (Sanov stretch of both lines), exponent-ledger row distance (harness v2 table), cyclic
# 2-letter patterns and moves that shorten (harness v2 definitions, checked equal on 2,000 starts this morning).
import sys,json,math,importlib.util
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'
sys.path.insert(0,S+'/acc_private/ladder'); sys.path.insert(0,S+'/acc_private/solve'); sys.path.insert(0,S+'/acc_private/pool/ACC_Replay_Idea_Pool')
import splitbeam as SB; from sanov import rho; import replay_loop as rl; from verifier import core
sp=importlib.util.spec_from_file_location('hv','/home/claude/operator-first/tools/compound-eye/mixer_5_2_all_eyes/implementations/compound_eye_harness_acc_v2.py')
HV=importlib.util.module_from_spec(sp); sp.loader.exec_module(HV); ROWD=HV.row_distance_table(12)
T=rl.load_targets()
def cyc(w):
    w=list(w)
    while len(w)>1 and w[0]==-w[-1]: w=w[1:-1]
    return w
def g2(w):
    c=cyc(w); n=len(c); return len({(c[i],c[(i+1)%n]) for i in range(n)}) if n else 0
def eyes(s):
    A,B=rho(s[0]),rho(s[1]); x=A[0]+A[3]; y=B[0]+B[3]; L=len(s[0])+len(s[1])
    d=ROWD.get(HV.matrix_M(s))
    return [L, math.log1p(abs(SB.kap(A,B)-18)), math.log1p(abs(x*x-4))+math.log1p(abs(y*y-4)), 13 if d is None else d,
            g2(s[0])+g2(s[1]), sum(1 for m in range(14) if sum(map(len,core.apply_move(s,m)))<L)]
P=json.load(open(S+'/picture/all_paths.json')); out=[]
for i,p in enumerate(P):
    s=tuple(map(tuple,T[p['id']]['initial_relators'])); rows=[eyes(s)]
    for m in p['path']: s=core.apply_move(s,m); rows.append(eyes(s))
    q=dict(p); q['eyes']=rows; out.append(q)
json.dump(dict(eye_names=['total','kappa','scale','ledger','grams2','down'],paths=out),open(S+'/picture/all_paths_eyes.json','w'))
print('paths with eye traces:',len(out))
