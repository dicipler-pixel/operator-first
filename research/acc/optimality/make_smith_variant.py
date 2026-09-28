from pathlib import Path

source = Path('research/acc/optimality/acc_beam.c').read_text()
anchor = 'static int QUOTA=0,WHM=0; static uint64_t ELITE=0; static double DUALF=0;'
addition = r'''
static double SMITHF=0;
static int SMITHZ0=1;
// Exploratory impedance chart: Z = total relator length + i*cyclic commutator length.
// Gamma=(Z-Z0)/(Z+Z0); radial/phase sectors are a diversity view, not an AC invariant.
static int smith_bin(const St*s){
  double L=s->l[0]+s->l[1], C=comm_len(s), R=SMITHZ0;
  double den=(L+R)*(L+R)+C*C;
  double re=(L*L-R*R+C*C)/den, im=2*R*C/den;
  double mag=sqrt(re*re+im*im), ph=atan2(im,re);
  int rb=(int)(mag*4), pb=(int)(ph*(4.0/3.141592653589793));
  if(rb>3) rb=3; if(pb>3) pb=3; if(pb<0) pb=0;
  return rb*4+pb;
}
'''
assert source.count(anchor) == 1
source = source.replace(anchor, anchor + addition)

anchor = 'DUALF=getenv("BEAM_DUAL")?atof(getenv("BEAM_DUAL")):0;'
replacement = 'SMITHF=getenv("BEAM_SMITH")?atof(getenv("BEAM_SMITH")):0; SMITHZ0=s0.l[0]+s0.l[1]; if(SMITHF<0||SMITHF>1||(SMITHF>0&&!getenv("BEAM_DUAL"))) die("BEAM_SMITH needs BEAM_DUAL and a fraction in [0,1]");\n  ' + anchor
assert source.count(anchor) == 1
source = source.replace(anchor, replacement)

start = '''        uint64_t k2=(uint64_t)(W2*DIV); if(k2>W2) k2=W2; if(k2>nh) k2=nh;'''
end = '''        if(d%10==0) fprintf(stderr,"dual d=%d first=%llu second=%llu of %llu left\\n",d,(unsigned long long)WS,(unsigned long long)(keep-WS),(unsigned long long)nh);
        free(H); free(taken);'''
assert source.count(start) == 1 and source.count(end) == 1
i, j = source.index(start), source.index(end)
old = source[i:j]
sm = r'''
        if(SMITHF>0){
          uint64_t want=(uint64_t)(W2*SMITHF), got=0, cap=(want+15)/16;
          uint32_t counts[16]={0}; uint8_t*sm_taken=calloc(nt,1);
          if(!sm_taken) die("smith alloc");
          for(uint64_t q=0;q<nh&&got<want;q++){
            Node x=tmpN[H[q].idx]; uint8_t*z=SA+x.off; St t2;
            t2.l[0]=z[0]|(z[1]<<8); t2.l[1]=z[2]|(z[3]<<8);
            memcpy(t2.w[0],z+4,t2.l[0]); memcpy(t2.w[1],z+4+t2.l[0],t2.l[1]);
            int bin=smith_bin(&t2);
            if(counts[bin]<cap){ counts[bin]++; C[WS+got++]=H[q]; sm_taken[H[q].idx]=1; }
          }
          // Remaining slots use the original plain eye, including its tail sampling.
          uint64_t nU=0, need=W2-got; Cand*U=malloc(sizeof(Cand)*nh); if(!U) die("smith plain alloc");
          for(uint64_t q=0;q<nh;q++) if(!sm_taken[H[q].idx]) U[nU++]=H[q];
          uint64_t k2=(uint64_t)(need*DIV); if(k2>need) k2=need; if(k2>nU) k2=nU;
          for(uint64_t q=0;q<k2;q++) C[WS+got+q]=U[q];
          uint64_t kk=k2;
          if(k2<need&&nU>k2){ uint64_t rest=nU-k2,nwant=need-k2;
            if(nwant>rest) nwant=rest;
            for(uint64_t q=0;q<nwant;q++) C[WS+got+kk++]=U[k2+(uint64_t)((double)q*rest/nwant)]; }
          keep=WS+got+kk;
          if(d%10==0) fprintf(stderr,"smith d=%d reserved=%llu requested=%llu second=%llu\\n",d,(unsigned long long)got,(unsigned long long)want,(unsigned long long)(keep-WS));
          free(U); free(sm_taken);
        } else {
'''
source = source[:i] + sm + old + '''        }
''' + source[j:]
Path('work/acc_beam_smith.c').write_text(source)
print('Wrote work/acc_beam_smith.c')
