#!/usr/bin/env python3
"""Two paid commutator insertions with held-relator Dehn simplification only."""
import hashlib,json,resource,sys,time
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(192*1024**2,192*1024**2))
resource.setrlimit(resource.RLIMIT_CPU,(10,10))
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT))
from official_checker import load_kernel,render
c,_,pins,_=load_kernel()
mp=ROOT/'integration/repo/official_manifest.json'
assert hashlib.sha256(mp.read_bytes()).hexdigest()==pins['source_manifest_sha256']
manifest=json.loads(mp.read_text())
row=next(x for x in manifest['challenges']if x['challenge_id']=='ac-07824')
start=tuple(tuple(w)for w in row['initial_relators'])
deadline=time.monotonic()+10;began=time.monotonic();admitted=0;MAX=100000
def determinant(s):
    a=[[sum(x for x in w if abs(x)==g)//g for g in(1,2)]for w in s]
    return a[0][0]*a[1][1]-a[0][1]*a[1][0]
def replay(s,moves):
    peak=sum(map(len,s));ds=[]
    for m in moves:
        s=c.apply_move(s,m);peak=max(peak,sum(map(len,s)))
        d=determinant(s);assert abs(d)==1;ds.append(d)
    return s,peak
def source_frames(a):
    result=[]
    for inv in(False,True):
        z=c.invert(a)if inv else a
        for k in range(len(z)):
            if k<=len(z)-k:gs=tuple(-v for v in z[:k])
            else:gs=tuple(reversed(z[k:]))
            moves=([0]if inv else[])+[6+c.GENS.index(g)for g in gs]
            result.append((z[k:]+z[:k],moves))
    return result
frames=source_frames(start[0])
results=[]
for exponent in(4,16):
    if time.monotonic()>=deadline:break
    prefix=[6]*exponent+[4]+[7]*exponent+[5]
    s,peak=replay(start,prefix)
    g=(1,)*exponent
    expected=(start[0],c.free_reduce(start[1]+g+start[0]+c.invert(g)+c.invert(start[0])))
    assert s==expected and s[0]==start[0]
    inserted=render(s);moves=list(prefix);simplifications=[];status='held_relator_dehn_fixed_point'
    while time.monotonic()<deadline and admitted<MAX:
        proposals=[]
        for framed,frame_moves in frames:
            for n in range(len(framed)//2+1,len(framed)+1):
                left=framed[-n:];replacement=c.invert(framed[:-n])
                for pos in range(len(s[1])-n+1):
                    if time.monotonic()>=deadline or admitted>=MAX:break
                    if s[1][pos:pos+n]!=left:continue
                    before=s[1][:pos];after=s[1][pos+n:]
                    new=c.free_reduce(before+replacement+after)
                    if len(new)>=len(s[1]):continue
                    # r1 difference = after^-1 * framed^-1 * after.
                    conj=[6+c.GENS.index(-a)for a in after]
                    prepare=frame_moves+conj+[0]
                    macro=prepare+[4]+[c.INVERSE_MOVE[m]for m in reversed(prepare)]
                    if admitted>=MAX:break
                    admitted+=1
                    reached,tmp_peak=replay(s,macro)
                    assert reached==(start[0],new)
                    proposals.append((len(new),len(macro),tuple(macro),pos,n,reached,tmp_peak))
                if time.monotonic()>=deadline or admitted>=MAX:break
            if time.monotonic()>=deadline or admitted>=MAX:break
        if time.monotonic()>=deadline:status='wall_time_cap';break
        if admitted>=MAX:status='admission_cap';break
        if not proposals:break
        proposal=min(proposals,key=lambda p:p[:3])
        _,_,macro,pos,n,s,p=proposal;peak=max(peak,p);moves.extend(macro)
        simplifications.append({'matched_position':pos,'matched_length':n,'paid_moves':list(macro),'endpoint':render(s)})
    independently,ind_peak=replay(start,moves)
    assert independently==s and ind_peak==peak
    results.append({'conjugator':'x^'+str(exponent),'insertion_moves':prefix,
        'insertion_endpoint':inserted,'simplifications':simplifications,
        'complete_paid_moves':moves,'endpoint':render(s),
        'paid_length':len(moves),'peak_total_relator_length':peak,
        'same_as_original_start':s==start,'held_r0_unchanged':s[0]==start[0],
        'determinant':determinant(s),'status':status,
        'official_verdict':c.verify(row,moves,row['move_spec_version'],manifest['limits'])})
out={'method':'proof_critical_pair_paid_commutator_and_held_relator_dehn_v1',
     'row':'ac-07824','instance_hash':row['instance_hash'],
     'bounds':{'wall_seconds':10,'memory_mib':192,'admissions':MAX,'conjugator_exponents':[4,16]},
     'elapsed_seconds':time.monotonic()-began,'admitted_macro_candidates':admitted,'cases':results,
     'group_certificate_used_as_search_hint_only':True,
     'negative_scope':'Only these two exact inserted states followed by the deterministic strict held-r0 Dehn policy. No arbitrary search or global impossibility claim.',
     'execution_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'core_sha256':hashlib.sha256((ROOT/'vendor/verifier/core.py').read_bytes()).hexdigest()}
Path(__file__).with_name('receipt.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'admitted':admitted,'seconds':out['elapsed_seconds'],
    'cases':[{k:v for k,v in r.items()if k not in('simplifications','complete_paid_moves')}for r in results]},indent=2))
