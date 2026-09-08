"""Compare curvature components after declaring the geometric metric and speed."""
import numpy as np

def curvature_norm(i,*_):
    p=i['case'];g=np.asarray(p['metric'],float);K=np.asarray(p['curvature_form'],float);V=np.asarray(p['velocity'],float)
    def stop(s):return {'_status':'blocked','reason':s}
    if g.ndim!=2 or g.shape[0]!=g.shape[1] or K.shape!=g.shape or V.shape!=(len(g),):return stop('Compatible metric, curvature form and velocity required.')
    if not all(np.all(np.isfinite(x)) for x in [g,K,V]) or not np.allclose(g,g.T) or not np.allclose(K,K.T):return stop('Finite symmetric metric and curvature form required.')
    if np.linalg.eigvalsh(g).min()<=0:return stop('Positive-definite metric required; a singular coordinate limit needs a regular chart.')
    speed=float(V@g@V)
    if speed<=0:return stop('Nonzero velocity needed for a unit-speed curvature comparison.')
    F=np.linalg.cholesky(g).T;Fi=np.linalg.inv(F);B=Fi.T@K@Fi/speed
    return {'coordinate_form_max_abs':float(np.max(np.abs(K))),'metric_speed_squared':speed,
      'unit_speed_metric_curvature_eigenvalues':np.linalg.eigvalsh((B+B.T)/2).tolist(),
      'metric_condition':float(np.linalg.cond(g)),
      'scope':'Input K must represent R(.,V)V in the supplied basis. Metric whitening and speed normalization do not independently validate the curvature solver or imply a bound in every direction.'}
