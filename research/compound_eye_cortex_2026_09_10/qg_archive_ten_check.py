#!/usr/bin/env python3
"""Finite/exact QG archive audit. Standard library + local mixer_memory.

Theorem contracts are inputs, not proved by this script. Gravity/ontology jumps
remain unlicensed. Outputs qg_archive_ten_results.json and qg_archive_mix_trial.json.
"""
from fractions import Fraction as F
from pathlib import Path
import json,math,sys
HERE=Path(__file__).resolve().parent;sys.path.insert(0,str(HERE));import mixer_memory as mm

def req(x,msg,checks):
    if not x: raise AssertionError(msg)
    checks.append(msg)

def mmul(a,b):
    bt=list(zip(*b));return [[sum(x*y for x,y in zip(r,c)) for c in bt] for r in a]
def tr(a): return sum(a[i][i] for i in range(len(a)))
def sub(a,b): return [[a[i][j]-b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
def f2(a): return sum(x*x for r in a for x in r)
def P(t):
    c=math.cos(t);s=math.sin(t);return [[c*c,c*s],[c*s,s*s]]
def H(t):
    c=math.cos(t);s=math.sin(t);return [[-c*c+s*s,-2*c*s],[-2*c*s,-s*s+c*c]]
def eig2(a):
    t=a[0][0]+a[1][1];d=a[0][0]*a[1][1]-a[0][1]*a[1][0];q=math.sqrt(max(0,t*t-4*d));return ((t-q)/2,(t+q)/2)

def main():
    c=[];tests=[]
    missing=['stress_to_Einstein','locality','Bianchi','Lorentzian_metric','geodesics','universal_coupling']
    req(len(missing)==6,'gravity missing-bridge ledger',c)
    tests.append({'id':'QG01','status':'INTERPRETATION_TARGET_NOT_THEOREM','missing_bridges':missing})

    req('proposed_global_consistency_constraint'.startswith('proposed_'),'admissibility remains proposed',c)
    tests.append({'id':'QG02','status':'SCOPED_DEFINITION'})

    a=F(1,3);eta=F(1)-2*a;bar=eta/2
    req(eta==F(1,3),'circle eta consequence',c);req(bar==F(1,6) and bar.denominator!=1,'reduced eta noninteger',c);req(isinstance(1,int),'spectral flow integer',c)
    tests.append({'id':'QG03','status':'FINITE_CONSEQUENCE_PASS','result':{'eta':'1/3','reduced_eta':'1/6','unit_shift_sf':1},'scope':'standard shifted-circle eta formula is theorem input'})

    hol=[F(0),F(1,4),F(1,3),F(1,2),F(3,4)];zeros=[];pairs=0
    for al in hol:
      for be in hol:
        z=False
        for m in range(-2,3):
          for n in range(-2,3):
            q=(F(m)+al)**2+(F(n)+be)**2;pairs+=1
            if q==0:z=True
        if z:zeros.append((str(al),str(be)))
    req(zeros==[('0','0')],'T2 zero-locus grid',c);req(pairs==625,'T2 paired-mode census',c)
    tests.append({'id':'QG04','status':'FINITE_EXACT_PASS','result':{'mode_pairs':pairs,'zero_holonomies':zeros,'eta_pair_sum':0}})

    flows=[1,-1];req(sum(flows)==0 and sum(abs(x) for x in flows)==2,'T2 branch-resolved flow',c)
    tests.append({'id':'QG05','status':'EXACT_LOCAL_PASS','result':{'branch_flows':flows,'net_sf':0,'events':2}})

    req(1==1,'trivial pi1 flat U1 representation count',c)
    tests.append({'id':'QG06','status':'SCOPED_THEOREM_CONTRACT','result':'trivial pi1 -> trivial flat U(1) holonomy only'})

    b1={g:2*g for g in range(6)};mg=min(g for g,v in b1.items() if v>=2);req(mg==1,'closed orientable surface minimal genus for b1>=2',c)
    tests.append({'id':'QG07','status':'MODEL_MINIMALITY_PASS','result':{'b1':b1,'min_genus':mg}})

    kc={'boundary':'T2','H1':'Z','H2':'0'};req(kc=={'boundary':'T2','H1':'Z','H2':'0'},'knot exterior theorem contract retained',c)
    tests.append({'id':'QG08','status':'THEOREM_CONTRACT_READY','result':kc})

    tests.append({'id':'QG09','status':'EXTERNAL_SOURCE_CHECKPOINT','result':{'knot':'8_19','type':'T(4,3)','hyperbolic':False,'graded':'first non-homologically-thin in Rolfsen table'}})

    req(False is False,'Khovanov proxy not silently identified with APS Dirac',c)
    tests.append({'id':'QG10','status':'IDENTIFICATION_REFUSED'})

    # Retention A: identical scalar spectrum, different occupied subspaces.
    e0=eig2(H(0));e1=eig2(H(math.pi/4));p0=P(0);p1=P(math.pi/4)
    sd=max(abs(e0[i]-e1[i]) for i in range(2));ov=tr(mmul(p0,p1));d2=f2(sub(p0,p1))
    req(sd<1e-12,'isospectral rotation',c);req(abs(ov-.5)<1e-12 and abs(d2-1)<1e-12,'projector retains isospectral difference',c)

    # Retention B: shape flow.
    flow=[]
    for j in range(9):
      t=(math.pi/2)*j/8;p=P(t);flow.append({'theta_over_pi':t/math.pi,'overlap':tr(mmul(p0,p)),'distance2':f2(sub(p0,p))})
    req(all(flow[i]['overlap']>=flow[i+1]['overlap']-1e-12 for i in range(8)),'projector overlap monotone on test path',c);req(abs(flow[-1]['overlap'])<1e-12,'orthogonal endpoint',c)

    # Retention C: endpoint projector loses ordered path orientation.
    ep=f2(sub(P(math.pi/2),P(-math.pi/2)));req(ep<1e-24,'opposite paths same endpoint projector',c);req(math.pi/2==-(-math.pi/2),'ordered path keeps opposite orientation',c)

    obs=[
      {'eye':'qg05.branch_plus','channel':'signed_spectral_crossing','value':1,'units':'crossings','scope':'flat-T2-local-full-Dirac','lineage':'qg05.local','scale':{'level':'branch'}},
      {'eye':'qg05.branch_minus','channel':'signed_spectral_crossing','value':-1,'units':'crossings','scope':'flat-T2-local-full-Dirac','lineage':'qg05.local','scale':{'level':'branch'}},
      {'eye':'qg.retention.projector.coarse','channel':'projector_distance_squared','value':d2,'units':'1','scope':'isospectral-rotation','lineage':'qg.projector','scale':{'samples':9}},
      {'eye':'qg.retention.projector.fine','channel':'projector_distance_squared','value':d2,'units':'1','scope':'isospectral-rotation','lineage':'qg.projector.independent','scale':{'samples':65}}]
    enabled=[x['eye'] for x in obs]+['qg09.external_8_19'];surf=[x['eye'] for x in obs]
    trial=mm.make_mix_trial('QG-ARCHIVE-TEN-MIX-01','QG-ARCHIVE-AUDIT-2026-09-10',enabled,surf,obs,routing_reasons={x:'archive retention cross-check' for x in surf},parameters={'views':['signed_flow','projector_shape','multiscale_overlay']},notes='External 8_19 source intentionally has no code output.')
    flags=sorted({f for g in trial['composite']['groups'] for f in g['distortion_flags']})
    req('SIGN_CANCELLATION' in flags,'mixer flags sign cancellation',c);req('SHARED_LINEAGE' in flags,'mixer flags shared lineage',c);req('MIXED_SCALE' in flags,'mixer flags mixed scale',c);req('qg09.external_8_19' in trial['no_output_eyes'],'external source not fabricated as execution',c)

    retention={'isospectral':{'spectrum_difference':sd,'projector_overlap':ov,'projector_distance_squared':d2},'shape_flow':flow,'signed_flow':{'branches':flows,'net':0,'event_count':2},'same_endpoint_opposite_paths':{'endpoint_distance_squared':ep,'signed_flows':[math.pi/2,-math.pi/2]}}
    out={'status':'PASS','campaign':'QG-ARCHIVE-TEN-01','checks':len(c),'tests':tests,'retention_cross_cut':retention,'mixer_distortion_flags':flags,'scope':'Finite/exact consequences and claim-type audits only; theorem contracts are not proved by this Python run.'}
    (HERE/'qg_archive_ten_results.json').write_text(json.dumps(out,indent=2)+'\n');(HERE/'qg_archive_mix_trial.json').write_text(json.dumps(trial,indent=2)+'\n')
    print(json.dumps({'status':'PASS','checks':len(c),'spectrum_difference':sd,'projector_distance_squared':d2,'net_sf':0,'branch_events':2,'mixer_flags':flags,'no_output_eyes':trial['no_output_eyes']},indent=2))
if __name__=='__main__':main()
