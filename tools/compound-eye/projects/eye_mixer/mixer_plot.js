/* One SVG renderer powers the live view and vector/image exports. */
const EyeMixerPlot=(()=>{
 const E=typeof EyeMixer!=='undefined'?EyeMixer:require('./mixer_core.js');
 const esc=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const num=v=>Number.isFinite(v)?Number(v.toPrecision(4)).toString():'—';
 const extent=a=>a.reduce((m,v)=>E.finite(v)?Math.max(m,Math.abs(v)):m,0);
 function path(x,y,X,Y){let s='',open=false;for(let k=0;k<x.length;k++){if(!E.finite(x[k])||!E.finite(y[k])){open=false;continue}s+=(open?'L':'M')+X(x[k]).toFixed(2)+','+Y(y[k]).toFixed(2);open=true}return s}
 function svg(d,s,m,baseline=null){
  const W=1100,H=620,L=74,R=1058,T=100,B=458,idx=Math.max(0,Math.min(d.x.length-1,Math.round(s.cursor||0))),shape=s.view==='shape';
  let lines=[],max=1e-9,xmin=0,xmax=1,ymin=0,ymax=1;
  const add=(p,color,width=2,opacity=1,dash='')=>{if(p)lines.push(`<path d="${p}" fill="none" stroke="${color}" stroke-width="${width}" opacity="${opacity}" ${dash?'stroke-dasharray="'+dash+'"':''}/>`)};
  const text=(v,x,y,col='#a9bfd4',size=13,anchor='start')=>lines.push(`<text x="${x}" y="${y}" fill="${col}" font-family="system-ui,sans-serif" font-size="${size}" text-anchor="${anchor}">${esc(v)}</text>`);
  const dot=(x,y,col,r=5)=>lines.push(`<circle cx="${x}" cy="${y}" r="${r}" fill="${col}"/>`);
  if(shape){
   let vx=m.X.concat(m.rawX),vy=m.Y.concat(m.rawY);if(baseline){vx=vx.concat(baseline.X);vy=vy.concat(baseline.Y)}
   if(s.showComponents){let xx=0,yy=0;for(const c of m.traces){if(c.route!=='y')xx+=c.x[idx]||0;if(c.route!=='x')yy+=c.y[idx]||0;vx.push(xx);vy.push(yy)}}
   max=Math.max(.2,extent(vx),extent(vy))*1.13/(s.scale||1);
   const ratio=(R-L)/(B-T);ymin=-max;ymax=max;xmin=-max*ratio;xmax=max*ratio;
  }else{
   let vals=m.combined.concat(s.showOriginal?m.original:[]);if(s.showComponents)vals=vals.concat(...m.traces.map(t=>t.y));if(baseline)vals=vals.concat(baseline.combined);
   max=Math.max(.05,extent(vals))*1.16/(s.scale||1);xmin=d.x[0];xmax=d.x[d.x.length-1];ymin=-max;ymax=max;
  }
  const X=x=>L+(x-xmin)/(xmax-xmin)*(R-L),Y=y=>B-(y-ymin)/(ymax-ymin)*(B-T);
  lines.push(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(d.title)} combined ${shape?'X/Y shape':'signal'}"><defs><clipPath id="mixClip"><rect x="${L}" y="${T}" width="${R-L}" height="${B-T}"/></clipPath></defs><rect width="${W}" height="${H}" rx="16" fill="#081321"/>`);
  text(d.title+' · '+(shape?'combined X / Y shape':'combined signal'),36,37,'#f4dfba',22);
  text(m.activeCount+' active channels · '+m.unit,36,66,'#8fa8c2',13);
  text('COMPOUND EYE  /  MIXER',W-35,34,'#68e2d0',12,'end');
  for(let k=0;k<=4;k++){let xx=xmin+k*(xmax-xmin)/4,yy=ymin+k*(ymax-ymin)/4;add(`M${X(xx)},${T}V${B}`,'#1d3146',1);add(`M${L},${Y(yy)}H${R}`,'#1d3146',1);text(num(xx),X(xx),B+23,'#8199b1',11,'middle');text(num(yy),L-12,Y(yy)+4,'#8199b1',11,'end')}
  if(ymin<0&&ymax>0)add(`M${L},${Y(0)}H${R}`,'#36506a',1);
  if(xmin<0&&xmax>0)add(`M${X(0)},${T}V${B}`,'#36506a',1);
  lines.push('<g clip-path="url(#mixClip)">');
  if(baseline)add(shape?path(baseline.X,baseline.Y,X,Y):path(d.x,baseline.combined,X,Y),'#bda0ff',2,.85,'7 6');
  if(s.showOriginal&&m.smoothing>1)add(shape?path(m.rawX,m.rawY,X,Y):path(d.x,m.original,X,Y),'#87a2bc',1,.5);
  if(!shape&&s.showComponents)for(const c of m.traces)add(path(d.x,c.y,X,Y),c.color,1.5,.55);
  let combined=shape?path(m.X,m.Y,X,Y):path(d.x,m.combined,X,Y);add(combined,'#ffce78',9,.06);add(combined,'#ffce78',4,.12);add(combined,'#ffce78',2.2,.98);
  if(shape&&s.showComponents){let xx=0,yy=0;for(const c of m.traces){let dx=c.route==='y'?0:c.x[idx],dy=c.route==='x'?0:c.y[idx];if(dx===null||dy===null)continue;let nx=xx+dx,ny=yy+dy;add(`M${X(xx)},${Y(yy)}L${X(nx)},${Y(ny)}`,c.color,2,.85);dot(X(nx),Y(ny),c.color,3.5);xx=nx;yy=ny}}
  const px=shape?m.X[idx]:d.x[idx],py=shape?m.Y[idx]:m.combined[idx];if(E.finite(px)&&E.finite(py)){if(!shape)add(`M${X(px)},${T}V${B}`,'#68e2d0',1,.4);dot(X(px),Y(py),'#ffce78',6);dot(X(px),Y(py),'#fff2d7',2)}
  lines.push('</g>');
  text(shape?'X route · equal scale on both axes':d.context.coordinate+' ['+d.context.x_unit+']',(L+R)/2,B+49,'#a9bfd4',12,'middle');
  const ry=552,rmax=Math.max(.001,extent(m.residual));
  text('REMOVED DETAIL',L,523,'#ad9ace',10);text('RMS '+num(m.rmsResidual)+' · residual is not automatically noise',R,523,'#ad9ace',11,'end');
  add(`M${L},${ry}H${R}`,'#23364b',1);add(path(d.x,m.residual,x=>L+(x-d.x[0])/(d.x.at(-1)-d.x[0])*(R-L),y=>ry-y/rmax*18),'#bda0ff',1.2,.8);
  text((s.center?'Centered · ':'')+(s.normalization==='rms'?'Per-channel RMS scaling':'Source-unit sum')+' · smoothing '+m.smoothing+' samples · '+d.context.source_stage,36,596,'#829db8',11);
  text('x = '+num(d.x[idx])+(baseline?' · baseline dashed':''),R,596,'#68e2d0',11,'end');
  lines.push('</svg>');return lines.join('');
 }
 return {svg,esc,num};
})();
if(typeof module!=='undefined')module.exports=EyeMixerPlot;
