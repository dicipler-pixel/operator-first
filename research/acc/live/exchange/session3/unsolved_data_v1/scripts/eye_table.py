# SCRIPT: ACC_EYE_TABLE  every eye read at the start state of all 10,115 rows (solved and unsolved), with board record
import sys,json,math,time
sys.path.insert(0,'.'); sys.path.insert(0,'/home/claude/operator-first/tools/compound-eye/mixer_5_2_all_eyes/implementations')
import acc_image_distance as IMG, whitehead as WH
from descend import ld
M={'x':1,'x^-1':-1,'y':2,'y^-1':-2}; C2P={1:0,-1:1,2:2,-2:3}
rows=[]
for l in open('../pool/ACC_Replay_Idea_Pool/inputs/official_ac.jsonl'):
    d=json.loads(l); s=d['description'].split('|')[1].rsplit('>',1)[0]
    rel=[tuple(M[t] for t in r.replace('= 1','').split()) for r in s.split(';')]
    rows.append((d['challenge_id'],rel[0],rel[1]))
B={i['challengeId']:i for i in json.load(open('../solve/board.json'))['data']['items']}
band=json.load(open('snell_bands.json')) if False else None
def led(r): return sum((c==1)-(c==-1) for c in r), sum((c==2)-(c==-2) for c in r)
def smith_ab(r0,r1):
    (a,b),(c,d)=led(r0),led(r1); den=(c*1j+d)
    if den==0: return None
    tau=(a*1j+b)/den
    if tau.imag<0: tau=tau.conjugate()
    G=(tau-1j)/(tau+1j); return 2*math.atanh(min(abs(G),0.999999))
def run(w):
    b=o=0
    for i,c in enumerate(w): o=o+1 if i and c==w[i-1] else 1; b=max(b,o)
    return b
t=time.time(); out=[]
for k,(cid,r0,r1) in enumerate(rows):
    img=IMG.run({'relator_0':[C2P[c] for c in r0],'relator_1':[C2P[c] for c in r1]},None,None,None,None)
    wh=WH.analyse([C2P[c] for c in r0],[C2P[c] for c in r1])
    i=B[cid]
    out.append(dict(id=cid,solved=i['status']=='solved',record=i['currentBestLength'],teams=i['kTeams'],
        len0=len(r0),len1=len(r1),total=len(r0)+len(r1),run0=run(r0),run1=run(r1),
        imgd=img['lower_bound_moves'],img_unreach=img['image_unreachable'],
        wh_comp=wh[2],wh_cut=len(wh[3]),smithAB=smith_ab(r0,r1),line0=ld(r0,1),line1=ld(r1,2)))
    if k%2000==0: print(k,round(time.time()-t),'s',flush=True)
json.dump(out,open('eye_table_all_rows.json','w')); print('done',len(out),round(time.time()-t),'s')
