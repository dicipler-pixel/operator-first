
(function(){
'use strict';
const root=document.getElementById('atlas-demo');
const get=id=>root.querySelector('#'+id);
let reduced=false, forgotten=false;
const matrix=[[4,-1,0],[-1,5,-2],[0,-2,3]];
function det(M){
 if(M.length===0)return 1;
 if(M.length===1)return M[0][0];
 if(M.length===2)return M[0][0]*M[1][1]-M[0][1]*M[1][0];
 return M[0].reduce((sum,x,j)=>sum+(j%2?-1:1)*x*det(M.slice(1).map(row=>row.filter((_,k)=>k!==j))),0);
}
function eliminate(M,i){
 const keep=M.map((_,j)=>j).filter(j=>j!==i),pivot=M[i][i];
 if(pivot===0)throw new Error('A singular pivot cannot be eliminated.');
 return {response:keep.map(a=>keep.map(b=>M[a][b]-M[a][i]*M[i][b]/pivot)),weight:pivot};
}
const smaller=eliminate(matrix,1);
const fmt=x=>Number(x.toFixed(8)).toLocaleString('en-US',{maximumFractionDigits:8});
function draw(){
 const svg=get('network'),w=Math.max(280,Math.round(svg.getBoundingClientRect().width||850));
 const compact=w<500,h=compact?230:225;
 svg.setAttribute('viewBox','0 0 '+w+' '+h);
 const left=42,right=w-72,mid=(left+right)/2,y=105,lam=Number(get('load').value);
 const line=(a,b,c,d,color,width=2)=>`<line x1="${a}" y1="${b}" x2="${c}" y2="${d}" stroke="${color}" stroke-width="${width}"/>`;
 const text=(x,y,s,color='#DCE6E8',size=14)=>`<text x="${x}" y="${y}" text-anchor="middle" fill="${color}" font-size="${size}">${s}</text>`;
 const node=(x,y,r,c,fill='#0C161C')=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${fill}" stroke="${c}" stroke-width="2"/>`;
 let body=`<title id="network-title">${reduced?'Reduced chain with retained scalar weight':'Full three-coordinate chain'}</title><desc id="network-desc">${reduced?'Two exposed ends, effective coupling minus two fifths, and retained determinant factor five.':'Two exposed ends and one internal coordinate, with couplings minus one and minus two.'} Attached right load ${lam}.</desc>`;
 body+=line(right,y,w-24,y,'#E0C16C')+line(w-24,y,w-24,y+35,'#E0C16C')+line(w-34,y+35,w-14,y+35,'#E0C16C');
 body+=text(right,y+72,'load '+fmt(lam),'#E0C16C',14);
 if(reduced){
  body+=line(left,y,right,y,'#7BC9E5',2.5)+text(mid,y-13,'−2/5','#7BC9E5',16);
  body+=node(mid,y+86,23,'#E0C16C','#18252A')+text(mid,y+91,'× 5','#E0C16C',17);
  body+=text(left,y-42,'19/5','#DCE6E8',16)+text(right,y-42,'11/5','#DCE6E8',16);
 }else{
  body+=line(left,y,mid,y,'#7BC9E5')+line(mid,y,right,y,'#7BC9E5');
  body+=text((left+mid)/2,y-13,'−1','#7BC9E5',16)+text((mid+right)/2,y-13,'−2','#7BC9E5',16);
  body+=node(mid,y,12,'#99D5AD','#1E332B')+text(mid,y-42,'5','#99D5AD',16)+text(mid,y+40,'inside','#99D5AD',14);
  body+=text(left,y-42,'4','#DCE6E8',16)+text(right,y-42,'3','#DCE6E8',16);
 }
 body+=node(left,y,9,'#DCE6E8')+node(right,y,9,'#DCE6E8')+text(left,y+40,'left')+text(right,y+40,'right');
 svg.innerHTML=body;
}
function update(){
 const lam=Number(get('load').value),full=matrix.map(row=>row.slice());full[2][2]+=lam;
 const current=(reduced?smaller.response:matrix).map(row=>row.slice());current[current.length-1][current.length-1]+=lam;
 const direct=det(full),reading=det(current)*(reduced?smaller.weight:1);
 get('load-value').textContent=lam.toFixed(2);
 get('full-result').textContent=fmt(direct);get('diagram-result').textContent=fmt(reading);
 get('registers').hidden=!reduced;
 get('simplify').textContent=reduced?'Restore the full chain':'Eliminate the interior';
 get('simplify').setAttribute('aria-pressed',String(reduced));
 get('diagram-caption').textContent=reduced?'The interior is gone. Its response is in the new connection; its determinant contribution survives as × 5.':'The load touches an exposed end. It has no access to the internal coordinate.';
 get('agreement').textContent=Math.abs(direct-reading)<1e-9?'Agreement holds for every nonnegative load: 41 + 19λ.':'The two readouts differ.';
 draw();
}
function updateCounter(){
 get('forget').setAttribute('aria-pressed',String(forgotten));get('forget').textContent=forgotten?'Restore the retained weights':'Try discarding the weights';
 get('x-result').textContent=forgotten?'Incomplete reading: 1.5':'Determinant: 3';
 get('y-result').textContent=forgotten?'Incomplete reading: 1.5':'Determinant: 12';
 get('counter-message').textContent=forgotten?'False agreement: discarding the weights erases the determinant distinction.':'The response agrees; the determinant distinguishes the pieces.';
 get('counter-message').style.color=forgotten?'#F29C97':'#99D5AD';
}
get('simplify').addEventListener('click',()=>{reduced=!reduced;update();});
get('load').addEventListener('input',update);
get('forget').addEventListener('click',()=>{forgotten=!forgotten;updateCounter();});
if(typeof ResizeObserver!=='undefined')new ResizeObserver(draw).observe(get('network'));
else window.addEventListener('resize',draw);
update();
})();
