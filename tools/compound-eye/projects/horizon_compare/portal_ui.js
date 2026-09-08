(()=>{
 const h=id=>document.getElementById(id),M=HorizonModels,scans=__OBS_SCAN__,feedbacks=[0,.000001,.001,.05,.2];
 const colors={gold:'#ffcf76',cyan:'#68e2d0',purple:'#bb9cff',muted:'#abc1d8',axis:'#37536f'};
 function setup(id){let c=h(id),x=c.getContext('2d');x.clearRect(0,0,c.width,c.height);x.font='15px system-ui';return [x,c.width,c.height]}
 function line(x,pts,color,width=2){x.beginPath();x.strokeStyle=color;x.lineWidth=width;pts.forEach((p,i)=>i?x.lineTo(...p):x.moveTo(...p));x.stroke()}
 function dot(x,a,b,color,r=5){x.beginPath();x.fillStyle=color;x.arc(a,b,r,0,2*Math.PI);x.fill()}
 function text(x,s,a,b,color=colors.muted){x.fillStyle=color;x.fillText(s,a,b)}
 function shape(){let q=+h('hq').value,v=M.shape(q);h('hqv').textContent=q.toFixed(3);let[x,W,H]=setup('hshape'),X=z=>60+(z+.65)/1.3*(W-100),Y=z=>H-55-z*230;
  line(x,[[45,H-55],[W-30,H-55]],colors.axis);line(x,[[X(0),35],[X(0),H-35]],colors.axis);
  for(let sign of [-1,1]){let pts=[];for(let k=0;k<=80;k++){let t=sign*.6*k/80;pts.push([X(t),Y(t*t)])}line(x,pts,sign<0?colors.purple:colors.cyan,3)}
  dot(x,X(q),Y(q*q),colors.gold,7);dot(x,X(-q),Y(q*q),colors.muted,4);text(x,'w₃ = q²',45,22);text(x,'orientation −',65,H-16,colors.purple);text(x,'orientation +',W-175,H-16,colors.cyan);text(x,'coplanar wall',X(0)-55,50);text(x,'same Gram datum',65,68,colors.gold);
  h('hshapevalues').innerHTML=`<b>Path length to wall ${v.length.toFixed(4)}</b><br>Lift metric gqq ${v.metric.toFixed(4)} · det X ${v.det.toFixed(5)}<br>Projector norm: coordinate ${v.norm===null?'degenerate chart':v.norm.toFixed(3)} · metric ${v.metricNorm===null?'use regular lifted limit':'1.000'}`;
 }
 function rays(){let r=+h('hr').value,v=M.ray(r);h('hrv').textContent=r.toFixed(2);let[x,W,H]=setup('hrays'),X=z=>50+(z-.4)/4.8*(W-80);x.fillStyle='#211e37';x.fillRect(X(.4),35,X(2)-X(.4),H-78);line(x,[[X(2),35],[X(2),H-43]],colors.gold,2);text(x,'interior',65,24,colors.purple);text(x,'exterior',X(2)+30,24,colors.cyan);text(x,'horizon r = 2M',X(2)-65,H-15,colors.gold);
  for(let rr of [.75,1.25,1.75,2,2.5,3.25,4.25]){let u=M.ray(rr);line(x,[[X(rr),205],[X(rr)+55*u.out,105]],colors.cyan);line(x,[[X(rr),205],[X(rr)+55*u.in,105]],colors.purple);dot(x,X(rr),205,colors.muted,2)}
  let pos=X(r);dot(x,pos,205,colors.gold,7);line(x,[[pos,205],[pos+55*v.out,105]],colors.gold,4);text(x,'future ↑',W-105,66);text(x,'r →',W-65,H-40);
  h('hrayvalues').innerHTML=`<b>Constant-r surface: ${v.type}</b><br>Outgoing-directed dr/dt ${v.out.toFixed(4)}<br>Ingoing-directed dr/dt ${v.in.toFixed(4)} · curvature scalar ${v.K.toPrecision(4)}`;
 }
 function observation(){let k=+h('hb').value,f=feedbacks[k],inside=h('hobserver').value==='inside',j=inside?1:0,v=scans[k];h('hbv').textContent=f===0?'0 · one way':f.toString();let[x,W,H]=setup('hobs'),X=t=>50+t/4*(W-80),Y=z=>H-42-z*(H-90);
  line(x,[[50,35],[50,H-42],[W-30,H-42]],colors.axis);text(x,inside?'local inside signal x₂':'outside signal x₁',55,23);text(x,'time 0 → 4',W-150,H-10);
  for(let [b,ini,col,width] of [[2,0,colors.cyan,5],[3,1,colors.gold,2]]){let pts=[];for(let n=0;n<=160;n++){let t=n/40;pts.push([X(t),Y(M.state(t,b,ini,f)[j])])}line(x,pts,col,width)}
  text(x,'b = 2, hidden start 0',W-240,60,colors.cyan);text(x,'b = 3, hidden start 1',W-240,82,colors.gold);
  h('hobsvalues').innerHTML=`<b>${inside?'The local inside observer sees a difference':f===0?'Outside signals coincide exactly':'Return coupling exposes a difference'}</b><br>Outside reference model: algebraic rank ${v.algebraic_observability_rank_numeric}/2<br>Noise-resolved directions ${v.noise_resolved_directions}/2 · weakest SNR ${v.snr_per_unit_scaled_state[1].toPrecision(3)}`;
 }
 function drawAll(){shape();rays();observation()}
 ['hq','hr','hb','hobserver'].forEach(id=>h(id).addEventListener('input',drawAll));let timer=null,phase=0;
 h('hplay').onclick=()=>{if(timer){clearInterval(timer);timer=null;h('hplay').textContent='Run the views'}else{timer=setInterval(()=>{phase+=.022;h('hq').value=.55*Math.sin(phase);h('hr').value=2.7+2*Math.cos(phase*.7);h('hb').value=Math.min(4,Math.floor((phase%10)/2));drawAll()},45);h('hplay').textContent='Pause'}};
 h('hreset').onclick=()=>{if(timer)clearInterval(timer);timer=null;phase=0;h('hplay').textContent='Run the views';h('hq').value=.1;h('hr').value=3;h('hb').value=0;h('hobserver').value='outside';drawAll()};
 h('hfull').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await h('horizon').requestFullscreen()}catch(e){h('hrun').textContent='Full screen is unavailable here; open the standalone HTML in your browser.'}};
 h('hreadreport').onclick=()=>document.querySelector('[data-tab="hfindings"]').click();drawAll();
})();
