"""Exact fixed-frame trajectory and monotone clock diagnostic; no route search."""
import json,sys,math,time,resource,hashlib
from pathlib import Path
from fractions import Fraction as F
resource.setrlimit(resource.RLIMIT_AS,(1024*1024*1024,1024*1024*1024))
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];sys.path.insert(0,str(ROOT))
from official_checker import load_kernel
I=(1,0,0,1);X=(1,2,0,1);Y=(1,0,2,1)
def mul(u,v):
 a,b,c,d=u;e,f,g,h=v;return(a*e+b*g,a*f+b*h,c*e+d*g,c*f+d*h)
def inv(u):
 a,b,c,d=u;return(d,-b,-c,a)
G={1:X,-1:inv(X),2:Y,-2:inv(Y)}
def disk(w,target):
 m=I
 for v in w:m=mul(m,G[v])
 a,b,c,d=mul(inv(target),m);nr,ni=b+c,a-d;dr,di=b-c,a+d;den=dr*dr+di*di
 return(F(nr*dr+ni*di,den),F(ni*dr-nr*di,den))
def rle(xs):
 out=[]
 for x in xs:
  if not out or x!=out[-1]:out.append(x)
 return out
t=time.monotonic();before=(ROOT/'continuation/checkpoint.json').read_bytes();cp=json.loads(before)
assert cp['active'] is None and not cp['stopped']
core,spec,doc,challenges=load_kernel()
routes={len(r['moves']):r['moves'] for r in json.loads((OUT/'inputs.json').read_text())['routes']}
traces={};metrics={};rads={}
for count,moves in routes.items():
 states=[tuple(tuple(w) for w in challenges['ac-00009']['initial_relators'])]
 for m in moves:states.append(core.apply_move(states[-1],m))
 assert states[-1]==((1,),(2,))
 traces[count]=states;pts=[(disk(s[0],X),disk(s[1],Y)) for s in states]
 rads[count]=[[p[layer][0]**2+p[layer][1]**2 for p in pts] for layer in (0,1)]
 angles=[]
 for layer in (0,1):
  delta=[]
  for i in range(count):
   a,b=pts[i][layer],pts[i+1][layer]
   if a==(0,0) or b==(0,0):delta.append(None)
   else:delta.append(math.degrees(math.atan2(float(a[0]*b[1]-a[1]*b[0]),float(a[0]*b[0]+a[1]*b[1]))))
  angles.append({'principal_increments_degrees':delta,'signed_sum_of_principal_increments':sum(x for x in delta if x is not None),'undefined_zero_point_intervals':sum(x is None for x in delta)})
 lengths=[sum(map(len,s)) for s in states]
 metrics[count]={'paid_moves':count,'peak_total_word_length':max(lengths),'initial_total_word_length':lengths[0],'terminal_total_word_length':lengths[-1],'sum_pre_move_word_lengths':sum(lengths[:-1]),'layer_update_ticks':[sum(states[i][j]!=states[i+1][j] for i in range(count)) for j in (0,1)],'angle_readouts':angles,'initial_disk':[[str(v) for v in p] for p in pts[0]],'both_initial_points_nonzero':all(p!=(0,0) for p in pts[0])}
a,b=traces[112],traces[78];assert (len(a)+1)*(len(b)+1)<=12000
dp=[[0]*(len(b)+1) for _ in range(len(a)+1)]
for i in range(len(a)-1,-1,-1):
 for j in range(len(b)-1,-1,-1):
  dp[i][j]=1+dp[i+1][j+1] if a[i]==b[j] else max(dp[i+1][j],dp[i][j+1])
anchors=[];i=j=0
while i<len(a) and j<len(b):
 if a[i]==b[j]:anchors.append((i,j));i+=1;j+=1
 elif dp[i+1][j]>=dp[i][j+1]:i+=1
 else:j+=1
assert anchors[0]==(0,0) and anchors[-1]==(112,78)
segments=[]
for (i,j),(k,l) in zip(anchors,anchors[1:]):
 if (k-i)!=(l-j) or a[i:k+1]!=b[j:l+1]:
  segments.append({'old_interval':[i,k],'new_interval':[j,l],'old_cost':k-i,'new_cost':l-j,'saving':(k-i)-(l-j),'old_moves':routes[112][i:k],'new_moves':routes[78][j:l],'common_start':a[i],'common_finish':a[k]})
assert sum(s['saving'] for s in segments)==34
result={'kind':'completed_readonly_clock_diagnostic','row':'ac-00009','paid_clock_unit':'one official atomic move','same_whole_state_path_up_to_repetitions':rle(a)==rle(b),'same_individual_layer_paths_up_to_repetitions':[rle([s[layer] for s in a])==rle([s[layer] for s in b]) for layer in (0,1)],'same_individual_radius_sequences_up_to_repetitions':[rle(rads[112][layer])==rle(rads[78][layer]) for layer in (0,1)],'shared_exact_states':len(set(a)&set(b)),'monotone_shared_anchors':anchors,'new_states_absent_from_old':len(set(b)-set(a)),'old_states_absent_from_new':len(set(a)-set(b)),'changed_segments':segments,'total_saved_moves':34,'route_metrics':metrics,'source_hashes':{p:hashlib.sha256((OUT/p).read_bytes()).hexdigest() for p in ['inputs.json','protocol.json','clock_probe.py']},'official_commit':doc['source_commit'],'elapsed_seconds':time.monotonic()-t,'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'dp_cells':(len(a)+1)*(len(b)+1),'new_searches':0,'model_workers':0,'checkpoint_unchanged':before==(ROOT/'continuation/checkpoint.json').read_bytes(),'angle_limit':'Principal increments at sampled states; no continuous trajectory, physical seconds, angular velocity or proven winding inferred.'}
assert result['checkpoint_unchanged'];assert result['elapsed_seconds']<180
(OUT/'result.json').write_text(json.dumps(result,indent=2)+'\n')
summary={k:v for k,v in result.items() if k not in ['source_hashes','route_metrics','monotone_shared_anchors','changed_segments']}
summary['segments']=[{k:v for k,v in s.items() if k not in ['old_moves','new_moves','common_start','common_finish']} for s in segments]
summary['metrics']={k:{a:b for a,b in v.items() if a not in ['angle_readouts','initial_disk']} for k,v in metrics.items()}
print(json.dumps(summary))

