# Independent replay: reimplemented from the AC move definitions in Python,
# no shared code with the C engine. Letters 0=x 1=X 2=y 3=Y ; inverse = ^1.
import json
def red(w):
    o=[]
    for c in w:
        if o and o[-1]==(c^1): o.pop()
        else: o.append(c)
    return o
def inv(w): return [c^1 for c in reversed(w)]
def step(r0,r1,m):
    if m==0: return inv(r0),r1
    if m==1: return r0,inv(r1)
    if m==2: return red(r0+r1),r1
    if m==3: return red(r0+inv(r1)),r1
    if m==4: return r0,red(r1+r0)
    if m==5: return r0,red(r1+inv(r0))
    if 6<=m<=9:
        g=m-6; return red([g]+r0+[g^1]),r1
    if 10<=m<=13:
        g=m-10; return r0,red([g]+r1+[g^1])
    raise ValueError(m)
C2P={1:0,-1:1,2:2,-2:3}
TGT=([0],[2])   # (x, y)
recs=json.load(open("PRIVATE_ties_20260916.json"))
allok=True
for r in recs:
    r0=[C2P[c] for c in r["initialRelators"][0]]
    r1=[C2P[c] for c in r["initialRelators"][1]]
    for m in r["moves"]:
        r0,r1=step(r0,r1,m)
    ok = (r0,r1)==TGT or (r0,r1)==([2],[0])
    exact = (r0,r1)==TGT
    if not ok: allok=False
    print(f"{r['challengeId']:10} len={r['length']:3} board={r['boardRecord']:3} k={r['kTeams']:3} "
          f"endpoint=({''.join('xXyY'[c] for c in r0)},{''.join('xXyY'[c] for c in r1)}) "
          f"{'VERIFIED' if exact else ('VERIFIED(swapped)' if ok else '*** FAIL ***')}")
print("\nALL VERIFIED" if allok else "\n*** SOME FAILED ***")
