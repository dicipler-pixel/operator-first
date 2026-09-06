from endpoint_probe import family,evaluate
from mpmath import mp
import json
from pathlib import Path
out={'precision':[],'isospectral':[],'reflection':[]}
for params,L in [(['.3','1','.4'],61),(['.6','1','.4'],61),(['.9','1','.4'],41),(['1','1','.02'],61)]:
 vals=[]
 for dps in [240,360]:
  block,g,r=family(params,L,dps)
  vals.append(evaluate(block(L),g,(L-1)//2))
 err=abs(mp.mpf(vals[0]['b'])-mp.mpf(vals[1]['b']))
 out['precision'].append({'params':params,'L':L,'absolute_difference':str(err),'relative_to_remainder':str(err/abs(mp.mpf(vals[1]['R'])))})
 print(out['precision'][-1],flush=True)
mp.dps=160
A=mp.mpf('1.52');p=mp.mpf('.6');ref={}
for vstr in ['.1','.3','.4','.5']:
 v=mp.mpf(vstr);s=mp.sqrt(A-v*v+2*p);d=mp.sqrt(A-v*v-2*p);a=(s-d)/2;b=(s+d)/2
 block,g,r=family([str(a),str(b),vstr],21,160)
 for L in [3,7,13,21]:
  C=block(L);D=mp.det(C);M=mp.det(mp.eye(L)-C);pair=[M+D,(M-D)/v]
  if L not in ref:ref[L]=pair
  out['isospectral'].append({'v':vstr,'L':L,'relative_sum_error':str(abs(pair[0]/ref[L][0]-1)),'relative_difference_over_v_error':str(abs(pair[1]/ref[L][1]-1))})
for params in [['.6','1','.4'],['1','.6','.4'],['.6','1','-.4']]:
 block,g,r=family(params,13,160)
 for L in [3,7,13]:
  C=block(L);S=mp.diag([(-1)**i for i in range(L)])
  bm,_,_=family([params[0],params[1],str(-mp.mpf(params[2]))],L,160)
  err=max(abs(z) for z in bm(L)-S*(mp.eye(L)-C)*S)
  nu=mp.eigsy(C,eigvals_only=True)
  eig=mp.fsum(mp.log1p(-x)-mp.log(x) for x in nu)
  det=mp.log(mp.det(mp.eye(L)-C))-mp.log(mp.det(C))
  out['reflection'].append({'params':params,'L':L,'matrix_error':str(err),'spectral_logodds_error':str(abs(eig-det)),'min_nu':str(min(nu)),'min_hole':str(1-max(nu))})
Path(__file__).with_name('validation.json').write_text(json.dumps(out,indent=2)+'\n')
print('validation saved',flush=True)
