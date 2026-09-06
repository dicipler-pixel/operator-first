#!/usr/bin/env python3
"""Independent scalar-Hankel verification on the equal-hopping line."""
import argparse,json
from pathlib import Path
from mpmath import mp
from endpoint_probe import family,evaluate

def run(tstr,vstr,nmax,dps):
 mp.dps=dps;t=mp.mpf(tstr);e=abs(mp.mpf(vstr));M=mp.sqrt(4*t*t+e*e)
 assert t>0 and e>0
 moments={}
 for s in [-1,1]:
  for k in range(2*nmax+3):
   def f(th):
    E=(M+e)/2+(M-e)*mp.cos(th)/2
    return E**k*(E+s*e)/mp.sqrt((E+e)*(E+M))
   moments[s,k]=mp.quad(f,[0,mp.pi/2,mp.pi])
 def H(n,s,extra=False):
  if n==0:return mp.mpf(1)
  return mp.det(mp.matrix([[M*M*moments[s,i+j]-moments[s,i+j+2] if extra else moments[s,i+j] for j in range(n)] for i in range(n)]))
 block,g,r=family([tstr,tstr,str(e)],2*nmax+1,dps);rows=[]
 for n in range(nmax+1):
  ratio=H(n+1,1)*H(n,-1,True)/(H(n+1,-1)*H(n,1,True));b=(ratio-1)/(ratio+1)
  direct=evaluate(block(2*n+1),g,n)
  rows.append({'n':n,'L':2*n+1,'hankel_b':str(b),'direct_b':direct['b'],'difference':str(b-mp.mpf(direct['b']))})
  print(tstr,vstr,n,'difference',mp.nstr(b-mp.mpf(direct['b']),8),flush=True)
 c=(M+e)/2;d=(M-e)/2
 ce=(c+e+mp.sqrt((e+e)*(M+e)))/2
 cM=(c+M+mp.sqrt((e+M)*(M+M)))/2
 predicted=mp.sqrt(ce*cM)*(1-d*d/(4*ce*cM))/d
 target=(mp.sqrt(M)+mp.sqrt(e))/(mp.sqrt(M)-mp.sqrt(e))
 return {'t':tstr,'v_magnitude':str(e),'dps':dps,'rows':rows,'asymptotic_ratio':str(predicted),'target_ratio':str(target),'prefactor_identity_error':str(predicted-target)}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='hankel.json');ap.add_argument('--dps',type=int,default=90);ap.add_argument('--n-max',type=int,default=5);args=ap.parse_args()
 result=[run('1','.4',args.n_max,args.dps),run('.7','.1',args.n_max,args.dps)]
 Path(args.out).write_text(json.dumps(result,indent=2)+'\n')
