/* Pure model functions shared by the offline portal and its numerical checks. */
const HorizonModels = (()=>{
  function shape(q,a=.7){
    if(!(a>0&&a<1&&Math.abs(q)<1))throw Error('Outside signed path domain');
    const w=[a*(1-q*q),(1-a)*(1-q*q),q*q],d=w[0]-w[1];
    const A=[[3-d,(1-.4*d)/Math.sqrt(3)],[Math.sqrt(3)*q*q,2.6+.4*q*q]];
    const gap=Math.sqrt((A[0][0]-A[1][1])**2+4*A[0][1]*A[1][0]);
    const low=(A[0][0]+A[1][1]-gap)/2;
    const norm=gap>1e-12?Math.hypot(A[0][0]-low,A[0][1],A[1][0],A[1][1]-low)/gap:null;
    return {q,w,A,det:Math.sqrt(a*(1-a))*(1-q*q)*q,metric:1/(1-q*q),length:Math.asin(Math.abs(q)),norm,metricNorm:q===0?null:1};
  }
  function ray(r,M=1){
    if(!(r>0&&M>0))throw Error('Positive r and M required');
    return {out:1-Math.sqrt(2*M/r),in:-1-Math.sqrt(2*M/r),K:48*M*M/r**6,type:Math.abs(r-2*M)<1e-10?'null':r>2*M?'timelike':'spacelike'};
  }
  function state(t,b,h,feedback=0){
    // Analytic exponential of the real two-by-two generator [-1, feedback; .3, -b].
    const m=-(1+b)/2,d=(b-1)/2,k=Math.sqrt(d*d+.3*feedback),E=Math.exp(m*t),c=Math.cosh(k*t),s=k===0?t:Math.sinh(k*t)/k;
    return [E*(c+s*(d+feedback*h)),E*(h*c+s*(.3-d*h))];
  }
  return {shape,ray,state};
})();
if(typeof module!=='undefined')module.exports=HorizonModels;
