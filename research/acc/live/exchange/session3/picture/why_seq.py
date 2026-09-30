# SCRIPT: ACC_WHY_SEQ  Same-row pairs (record path vs our shortest path over record): do the two use the same
# multiplication sequence (moves 2-5 plus inversions 0-1, conjugations removed)? If yes, the whole miss is alignment.
import json,statistics as st,collections,difflib
A=json.load(open('all_paths.json')); by=collections.defaultdict(list)
for p in A: by[p['id']].append(p)
rows=[]
for cid,ps in by.items():
    R=[p for p in ps if p['status']=='at_record']; O=[p for p in ps if p['status']=='above']
    if not R or not O: continue
    o=min(O,key=lambda p:p['n']); sk=lambda p:[m for m in p['path'] if m<6]
    best=max(R,key=lambda r:difflib.SequenceMatcher(None,sk(r),sk(o)).ratio()); r=best
    same=sk(r)==sk(o); ratio=difflib.SequenceMatcher(None,sk(r),sk(o)).ratio()
    rows.append((cid,o['gap'],same,ratio,len(sk(r)),len(sk(o))))
print('rows with a record path and a path of ours above record:',len(rows))
for lo,hi in ((1,1),(2,3),(4,10),(11,999)):
    Z=[z for z in rows if lo<=z[1]<=hi]
    if Z: print(f'gap {lo}-{hi}: rows {len(Z)} | identical skeleton {sum(z[2] for z in Z)} ({100*sum(z[2] for z in Z)/len(Z):.0f}%) | skeleton similarity median {st.median(z[3] for z in Z):.2f}')
json.dump(rows,open('why_seq_rows.json','w'))
