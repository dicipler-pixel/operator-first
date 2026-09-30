# /tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpadIPT: ACC_WHY_JUNCTION  Every multiplication is a junction. Cost = conjugations spent right before it (alignment);
# gain = letters it cancels (|r_i|+|r_j| - |result|). Record vs our paths, band 25-50, plus same-row pairs.
import json,sys,statistics as st,collections
S='/tmp/claude-0/-home-claude/5be0c348-2b1b-5074-ba12-c1a1b9cc55c4/scratchpad'; sys.path.insert(0,S+'/acc_private/pool/ACC_Replay_Idea_Pool')
from verifier import core; import replay_loop as rl
T=rl.load_targets(); A=json.load(open(S+'/picture/all_paths.json'))
def junctions(p):
    s=tuple(tuple(r) for r in T[p['id']]['initial_relators']); out=[]; run=0
    for m in p['path']:
        if m>=6: run+=1
        elif m>=2:
            i,j=(0,1) if m in (2,3) else (1,0)
            t=core.apply_move(s,m); gain=len(s[i])+len(s[j])-len(t[i])
            out.append((run,gain)); run=0; s=t; continue
        s=core.apply_move(s,m)
    return out
G=collections.defaultdict(list); byrow=collections.defaultdict(dict)
for p in A:
    if not (25<=p['record']<=50): continue
    g='at_record' if p['status']=='at_record' else ('above_1_3' if p['gap']<=3 else 'above_4up')
    J=junctions(p); G[g].append(J)
    if g=='at_record' and ('r' not in byrow[p['id']] or p['n']<byrow[p['id']]['r'][0]): byrow[p['id']]['r']=(p['n'],J)
    if g!='at_record' and p['gap']<=10 and ('o' not in byrow[p['id']] or p['n']>byrow[p['id']]['o'][0]): byrow[p['id']]['o']=(p['n'],J)
for g,L in G.items():
    nj=[len(J) for J in L]; al=[a for J in L for a,_ in J]; ga=[b for J in L for _,b in J]
    zero=sum(1 for J in L for a,b in J if b<=0)/max(1,len(al))
    print(f'{g:10s} paths {len(L):4d} | mults/path {st.mean(nj):.1f} | align/junction mean {st.mean(al):.2f} median {st.median(al)} | '
          f'cancel/junction {st.mean(ga):.2f} | junctions cancelling nothing {100*zero:.0f}% | share with align>=4 {100*sum(a>=4 for a in al)/len(al):.0f}%')
P=[(v['r'],v['o']) for v in byrow.values() if 'r' in v and 'o' in v]
d_n=[len(o[1])-len(r[1]) for r,o in P]; d_a=[sum(a for a,_ in o[1])-sum(a for a,_ in r[1]) for r,o in P]
d_nog=[sum(1 for a,b in o[1] if b<=0)-sum(1 for a,b in r[1] if b<=0) for r,o in P]
print(f'pairs {len(P)} | extra mults mean {st.mean(d_n):.2f} | extra alignment conj mean {st.mean(d_a):.2f} | extra non-cancelling junctions mean {st.mean(d_nog):.2f}')
print('pairs where ours has MORE junctions',sum(x>0 for x in d_n),'same',sum(x==0 for x in d_n),'fewer',sum(x<0 for x in d_n))
same=[(r,o) for r,o in P if len(r[1])==len(o[1])]
if same:
    print('same junction count pairs',len(same),'| extra align mean %.2f | ours cancel total - record %.2f'%(
      st.mean(sum(a for a,_ in o[1])-sum(a for a,_ in r[1]) for r,o in same),st.mean(sum(b for _,b in o[1])-sum(b for _,b in r[1]) for r,o in same)))
