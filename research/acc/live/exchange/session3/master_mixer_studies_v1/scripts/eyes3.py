# SCRIPT: ACC_THREE_EYES  Snell, planar (Mazur height) and Smith, each computed alone from the pooled recordings; exports Mixer traces
# Scalable: every constant is re-learned from whatever recordings are in RECS; add a recording and rerun.
import sys,json,math
sys.path.insert(0,'../solve')
from trace import mv
E={'x':1,'X':-1,'y':2,'Y':-2}
def enc(w): return tuple(E[c] for c in w)
def r1(n): return 'Y'*(n+1)+'X'+'y'*n+'x'
P=json.load(open('paths.json')); n3=json.load(open('../playback/n3_path.json'))['moves']; n5=json.load(open('../playback/n5_path.json'))['moves']
g=lambda f,k: [l for l in open(f)][0].split(' ',8)[-1]
import ast
mb=ast.literal_eval(open('mb30.out').read().split('->')[1].split(' ',2)[2])
RECS=[('MS(3,YYXXYx) solved 50','YYXXYx',r1(3),n3,True),
      ('MS(5,YYXXYx) descent, unsolved','YYXXYx',r1(5),n5,False),
      ('ac-07790 greedy 132','YYXYYXyyx',r1(5),json.load(open('../solve/mcsc5_paths.json'))['ac-07790'],True),
      ('ac-07790 tube 97','YYXYYXyyx',r1(5),P['ac-07790'],True),
      ('ac-07790 beam 59','YYXYYXyyx',r1(5),P['A5beam'],True),
      ('ac-07790 macro beam 58','YYXYYXyyx',r1(5),mb,True),
      ('ac-09762 greedy 188','YYXYYXyyx',r1(6),P['ac-09762'],True),
      ('ac-09762 beam 78','YYXYYXyyx',r1(6),P['A6beam'],True),
      ('ac-06005 greedy 132','YYXYYxyyX',r1(5),P['ac-06005'],True),
      ('ac-06005 beam 67','YYXYYxyyX',r1(5),P['C5beam'],True),
      ('ac-05564 greedy 203','YYXYYxyyX',r1(6),P['ac-05564'],True)]
def states(w0,w1,moves):
    st=(enc(w0),enc(w1)); S=[st]
    for m in moves: st=mv(*st,m); S.append(st)
    return S
SS=[states(a,b,m) for _,a,b,m,_ in RECS]
tot=lambda s:len(s[0])+len(s[1])
# ---- SNELL alone: speed of the medium by total length, learned from all pooled moves (band width 5)
band={}
for S in SS:
    for i in range(1,len(S)):
        b=tot(S[i-1])//5; x=band.setdefault(b,[0,0]); x[0]+=1; x[1]+=tot(S[i-1])-tot(S[i])
speed=lambda L:(lambda x: x[1]/x[0] if x else None)(band.get(L//5))
# ---- PLANAR alone: pooled integer height = fewest known moves to trivial; unknown states use a radius-2 lookup (+1/+2)
H={}
for (_,_,_,_,solved),S in zip(RECS,SS):
    if not solved: continue
    T=len(S)-1
    for i,s in enumerate(S): H[s]=min(H.get(s,10**9),T-i)
def height(s):
    if s in H: return H[s],0
    best=None
    for m in range(14):
        t=mv(*s,m)
        if t in H and (best is None or H[t]+1<best): best=H[t]+1
    if best is not None: return best,1
    for m in range(14):
        t=mv(*s,m)
        for m2 in range(14):
            u=mv(*t,m2)
            if u in H and (best is None or H[u]+2<best): best=H[u]+2
    return (best,2) if best is not None else (None,None)
# ---- SMITH alone: ledger point on the chart
def led(r): return sum((c==1)-(c==-1) for c in r), sum((c==2)-(c==-2) for c in r)
def smith(s):
    (a,b),(c,d)=led(s[0]),led(s[1]); tau=(a*1j+b)/(c*1j+d)
    if tau.imag<0: tau=tau.conjugate()
    G=(tau-1j)/(tau+1j); return 2*math.atanh(min(abs(G),0.999999)), math.degrees(math.atan2(G.imag,G.real))
out=[]
for (name,a,b,moves,solved),S in zip(RECS,SS):
    hs=[height(s) for s in S]; Tm=max([h for h,_ in hs if h is not None],default=1) or 1
    ch={'total':[tot(s) for s in S],
        'snell':[speed(tot(s)) for s in S],
        'height':[h for h,_ in hs],
        'height_gap':[r for _,r in hs],
        'mazurX':[None if h is None else h*(Tm-h)/Tm**2 for h,_ in hs],
        'dM':[round(smith(s)[0],3) for s in S],
        'smith_angle':[round(smith(s)[1],1) for s in S],
        'move':[None]+moves}
    lab={'total':'Total relator length','snell':'SNELL: medium speed at this height (letters/move, pooled)','height':'PLANAR: pooled height (fewest known moves to trivial)','height_gap':'PLANAR: lookup radius (0 on a known route, 1-2 near one)','mazurX':'PLANAR: Mazur X = h(T-h)/T^2','dM':'SMITH: distance from chart centre (hyperbolic)','smith_angle':'SMITH: angle round the chart (degrees)','move':'Move taken to arrive (0-13)'}
    out.append(dict(schema='compound-eye-traces-v1',id=name,title=name,description='Three eyes computed alone: Snell, planar height, Smith. Pooled and re-learned from all loaded recordings.',
        context=dict(object_id=name,model_id='ac-r2-v1 official move grammar',coordinate='move number',x_unit='moves',source_stage='evaluated'),
        x=list(range(len(S))),traces=[dict(id=k,label=lab[k],unit='',source='ACC_THREE_EYES',values=[None if v is None else float(v) for v in vals]) for k,vals in ch.items()]))
json.dump(out,open('three_eyes_traces.json','w'))
print('bands:',{b*5:round(x[1]/x[0],2) for b,x in sorted(band.items())})
print('pooled height table:',len(H),'states')
for o in out:
    h=o['traces'][2]['values']; print(f"{o['id']:34s} start height {h[0]}  known {sum(v is not None for v in h)}/{len(h)}")
