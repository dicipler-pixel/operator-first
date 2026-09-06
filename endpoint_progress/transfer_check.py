from endpoint_probe import family
from mpmath import mp
import json
from pathlib import Path
out=[]
for params in [['.3','1','.4'],['.6','1','.4'],['1','.6','-.4']]:
 mp.dps=260;a,b,v=map(mp.mpf,params);e=mp.sqrt((a-b)**2+v*v);t=mp.sqrt(a*b)
 original,_,_=family(params,41,260);reference,_,_=family([str(t),str(t),str(e)],41,260)
 for L in [3,13,21,41]:
  P=mp.det(original(L));U=reference(L);Pe=mp.det(U);Me=mp.det(mp.eye(L)-U)
  mixture=(1+v/e)/2*Pe+(1-v/e)/2*Me
  out.append({'params':params,'L':L,'relative_transfer_error':str(abs(mixture/P-1))})
  print(params,L,mp.nstr(abs(mixture/P-1),8),flush=True)
Path(__file__).with_name('transfer.json').write_text(json.dumps(out,indent=2)+'\n')
