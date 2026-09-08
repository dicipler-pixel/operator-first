"""Independent identities, coverage gates and exact finite-search checks."""
from pathlib import Path
import json,math,sys
import numpy as np
from scipy.linalg import expm
import sweeps
from records import load
HERE=Path(__file__).parent;ROOT=sweeps.ROOT;checks=[]
def read(name):return load(HERE/'results'/(name+'.json'))
def check(name,condition):
    if not bool(condition):raise AssertionError(name)
    checks.append(name)
def metric(rows,key):return np.array([x['metrics'][key] for x in rows])
def main():
    cov=read('coverage');check('All 191 definitions accounted for',not cov['summary']['uncovered']);check('171 successful implementations',cov['summary']['fresh_successful_implemented']==171)
    check('Only implemented refusal is missing nuclear acquisition',[x['eye'] for x in cov['summary']['blocked_implemented']]==['ce.data.nuclear_readiness@1.0.0']);check('17 specifications and two archive reads',cov['summary']['specified']==17 and cov['summary']['archives']==2);check('No execution errors',not cov['summary']['errors'])
    index=read('sweeps');check('All thirteen studies completed',len(index['data'])==13 and not index['errors'])
    data={k:read(k) for k in index['data']}
    for k,rows in data.items():check(k+' no unexplained execution failures',all(sum(f['status_counts'][s] for s in ['error','blocked','inapplicable'])==0 for f in rows))
    q=data['quantum'];H=np.array([[.5,1,0],[1,0,1],[0,1,-.5]])
    check('Quantum energy stays fixed',np.ptp(metric(q,'energy'))<1e-12);check('Quantum ergotropy stays fixed',np.ptp(metric(q,'ergotropy'))<1e-12);check('Quantum coherence changes substantially',np.ptp(metric(q,'coherence'))>1)
    check('Independent matrix exponential agrees with original quantum eyes',all(np.linalg.norm(abs(expm(-1j*f['parameter']*H)@np.array([1,0,0]))**2-[f['metrics'][k] for k in ['left probability','middle probability','right probability']])<1e-12 for f in q))
    req=q[13]['runs'][0]['request'];one=sweeps.machine.execute(req,['ce.set.quantum@1.0.0'],root=ROOT,workers=1);four=sweeps.machine.execute(req,['ce.set.quantum@1.0.0'],root=ROOT,workers=4)
    check('Original sixteen eyes agree in serial and parallel',one['result_sha256']==four['result_sha256']);check('Original sixteen share one source computation',four['statistics']['shared_kernel_calls']=={'quantum':1} and four['statistics']['shared_cache_hits']==15)
    b=data['boundary'];g=metric(b,'coupling');check('Feedback is g squared',np.max(abs(metric(b,'instantaneous feedback')-g*g))<1e-14);check('Redistribution norm is sqrt two times coupling',np.max(abs(metric(b,'redistribution norm')-2**.5*g))<1e-14);check('Retained response survives exact reduction',max(metric(b,'exact reduction residual'))<1e-12)
    check('Small nonzero feedback precedes noise resolution',any(f['metrics']['memory dimension']==1 and f['metrics']['resolvable directions']==1 for f in b));resolved=next(f['parameter'] for f in b if f['metrics']['resolvable directions']==2)
    o=data['optical'];null=min(o,key=lambda f:abs(f['metrics']['response']));check('Optical cancellation with fixed metric and rank',abs(null['metrics']['response'])<1e-12 and null['metrics']['metric']==2 and null['metrics']['channel rank']==1)
    check('Independent optical response formula',max(abs(f['metrics']['response']-(2/(1-f['parameter']**2)+16/(4-f['parameter']**2))) for f in o)<1e-12)
    w=data['weak'];meter_errors=[];prob_errors=[]
    for f in w:
        v=f['metrics'];a=v['weak value'];g=.01;den=math.cos(g)**2+a*a*math.sin(g)**2
        meter_errors.append(abs(v['exact meter estimate']-math.sin(2*g)*a/(2*g*den)))
        prob_errors.append(abs(v['finite-coupling success']-v['zero-coupling success']*den))
    check('Exact meter matches independent two-amplitude formula',max(meter_errors)<1e-9 and max(prob_errors)<1e-12)
    check('Selection-weighted weak value remains bounded',all(f['metrics']['weighted squared value']<=f['metrics']['second moment']+1e-12 for f in w))
    shape=data['shape'];check('Reflected lifts have same Gram but opposite orientation',all(abs(a['metrics']['small Gram value']-b['metrics']['small Gram value'])<1e-12 and a['metrics']['orientation']==-b['metrics']['orientation'] for a,b in zip(shape,shape[::-1])))
    check('Metric norm stays one away from the wall',all(f['metrics']['metric projector norm'] is None or abs(f['metrics']['metric projector norm']-1)<1e-10 for f in shape))
    k=data['knot'];r1=(3-math.sqrt(5))/2;r2=math.sqrt(3)-1
    check('Polynomial winding thresholds agree with exact roots',all(f['metrics']['ordinary winding']==int(f['parameter']>r1) and f['metrics']['twisted winding']==int(f['parameter']>r2) for f in k))
    for radius,channel in [(r1,'ordinary'),(r2,'twisted')]:
        wall=sweeps.compute('knot',radius);check(channel+' zero-crossing refusal remains explicit',wall['metrics'][channel+' winding'] is None and wall['status_counts']['blocked']==1)
    t=data['otto'];pc=1/(1+math.exp(2));check('Independent Otto work formula',all(abs(f['metrics']['work output']-(1/(1+math.exp(2/f['parameter']))-pc))<1e-12 for f in t));check('Thermal endpoint ergotropy stays zero',max(abs(metric(t,'endpoint ergotropy')))<1e-12);check('Engine transition at hot temperature one',all(f['metrics']['engine regime']==int(f['parameter']>1+1e-10) for f in t))
    original=sweeps.read('research/raw_population_replay.json');cal=sweeps.read('research/readout_calibration.json');C=np.array(cal['original_scale_selection_matrix']);narrow=np.array(cal['matched_narrow_selection_matrix']);r=data['qhe_data']
    check('Every acquired QHE setting present',len(r)==len(original)==539)
    for i,(frame,row) in enumerate(zip(r,original)):
        y=np.array(row['selected_counts']);multiply=C@y;multiply/=sum(multiply);inverse=np.linalg.solve(narrow.T,y);inverse/=sum(inverse)
        check('QHE forward convention and original replay '+str(i),np.max(abs(multiply-[frame['metrics']['notebook population '+str(j)] for j in range(4)]))<1e-12 and np.max(abs(inverse-[frame['metrics']['inverse diagnostic '+str(j)] for j in range(4)]))<1e-12)
    earth=data['earth'];check('All 112 distinct join-edge deletions replayed',len(earth)==113)
    for f in earth[1:]:
        p=f['runs'][0]['request']['inputs']['graph']['value'];color=p['coloring'];check('Independent nine-coloring check '+str(int(f['parameter'])),len(color)==28 and len(set(color))<=9 and all(color[a]!=color[b] for a,b in p['edges']))
    ak=data['kakeya'];check('Every fixed-geometry subtarget placement included',len(ak)==1+16+math.comb(16,2)+1)
    ids=[sweeps.machine.canonical(f['runs'][0]['request']['inputs']['tower']['value']['generators']) for f in ak[:-1]];check('No repeated Kakeya candidate',len(set(ids))==137)
    check('All 137 subtarget placements fail complete forcing',all(f['metrics']['score passes'] and not f['metrics']['complete forcing'] for f in ak[:-1]));check('Known 7/4 control completes forcing',ak[-1]['metrics']['score']==1.75 and ak[-1]['metrics']['complete forcing']==1)
    dio=data['dio'];check('Prime prefixes never claim rank proof',all(not f['metrics']['candidate 0 rank proven'] and not f['metrics']['candidate 1 rank proven'] for f in dio));check('Integer-cover obstruction unchanged',set(metric(dio,'reachable integer y count'))=={1})
    # An unseen parameter checks the actual computation endpoint, not interpolation.
    fresh=sweeps.compute('weak',.137);check('Unrecorded parameter actually evaluated',all(abs(fresh['parameter']-f['parameter'])>1e-9 for f in w) and fresh['status_counts']['ok']==3)
    sk=data['skew'];pe=data['peeling'];check('Stable non-normal propagator amplifies a Euclidean norm',max(metric(sk,'maximum amplitude gain'))>1.5);check('Weighted norm decreases while pairing stays fixed',np.max(np.diff(metric(sk,'Lyapunov state norm')))<1e-12 and np.ptp(metric(sk,'pairing'))<1e-12)
    check('Positive peel loses rank monotonically',np.all(np.diff(metric(pe,'remaining channel rank'))<=0) and pe[-1]['metrics']['remaining channel rank']==0)
    findings=[
      {'title':'A census can rise during actual removal.', 'text':'The positive-channel sweep tracks exact rank, silent directions, probe response and a fixed spectral window together. Rank cannot increase, while an eigenvalue entering the window can increase its census.'},
      {'title':'Skew evolution depends on the norm.', 'text':f'The fixed stable generator reaches sampled maximum amplitude gain {max(metric(sk,"maximum amplitude gain")):.4f}. Its Lyapunov norm decreases and the transported pairing stays fixed. The metric must be specified before amplitude is interpreted as physical energy.'},
      {'title':'Coordinated quantum motion.', 'text':f'Eighteen eye versions followed 81 states. Probabilities and coherence vary while energy and ergotropy stay constant within {max(np.ptp(metric(q,"energy")),np.ptp(metric(q,"ergotropy"))):.2g}. This is a finite closed-system control.'},
      {'title':'Feedback can exist before it is resolved.', 'text':f'For the fixed observer, sample times and noise used here, the first sampled two-direction readout occurs at coupling {resolved:.5g}. Smaller nonzero coupling already has exact nonzero feedback. The crossing is specific to this measurement design.'},
      {'title':'Optical silence can be cancellation.', 'text':f'At probe energy {null["parameter"]:.9g}, response is {null["metrics"]["response"]:.3g}, metric stays 2, and channel rank stays 1. The positive-weight assumption fails there.'},
      {'title':'A large weak value can mispredict the meter.', 'text':f'At offset .001 and meter coupling .01, the weak value is {w[0]["metrics"]["weak value"]:.0f}, but the exact meter estimate is {w[0]["metrics"]["exact meter estimate"]:.5g}; zero-coupling postselection probability is {w[0]["metrics"]["zero-coupling success"]:.3g}.'},
      {'title':'Knot readouts change at different radii.', 'text':f'The ordinary polynomial changes winding at radius {r1:.6f}, the twisted polynomial at {r2:.6f}. The same path produces different records between those values; neither observation alone is a physical-memory claim.'},
      {'title':'Heat-engine work belongs to the cycle.', 'text':'The ideal Otto cycle changes into an engine above hot temperature 1 (Tc=.5, gaps 1 and 2). Its thermal endpoint has zero ergotropy throughout. Endpoint work capacity does not replace cycle bookkeeping.'},
      {'title':'The QHE readout map matters.', 'text':f'All 539 acquired settings were reprocessed from existing classified counts. Maximum population L1 disagreement is {max(metric(r,"population disagreement L1")):.4g}. This compares the preserved notebook-width multiplication with matched-width inversion, not two equivalently calibrated estimators; no corrected efficiency is claimed.'},
      {'title':'Earth–Moon stays blocked in this family.', 'text':'The original 28-vertex candidate passes whole-graph density but fails the triangle-free subgraph bound. Every one of its 112 join-edge deletions has a checked nine-coloring, which also colors every further subgraph.'},
      {'title':'Kakeya cost and forcing disagree.', 'text':'All 137 placements of zero, one or two generators in the fixed four-vertex geometry meet the score threshold but fail complete forcing. The known three-generator control forces all four vertices at 7/4. This does not exclude other geometries.'},
      {'title':'Arithmetic structure still faces an integer obstruction.', 'text':f'Across 430 held-out primes, the frozen strongest signal ends at {dio[-1]["metrics"]["candidate 0 mean"]:.6f}; a competing signal ends at {dio[-1]["metrics"]["candidate 1 mean"]:.6f}. The original radius-3/2 cover still reaches only one integer y. No unresolved equation is solved.'}]
    result={'checks_passed':len(checks),'checks':checks,'frames':sum(len(x) for x in data.values()),'sweep_evaluations':sum(x['evaluations'] for x in index['data'].values()),'coverage_evaluations':cov['summary']['evaluations'],'distinct_sweep_eye_versions':len({e for x in index['data'].values() for e in x['eyes']}),'findings':findings,'formal_status':'No new Lean theorem is claimed; current results are scoped numerical, symbolic or finite exact checks.'}
    sweeps.machine.dump(HERE/'results/findings.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ['checks','findings']},indent=2))
if __name__=='__main__':main()
