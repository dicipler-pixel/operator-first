// meet_chain: exact meet between radius-RA balls around SOURCE states and the union of radius-RB balls around
// every state of a known road (TARGET chain). Any meet gives source -> chain state j; the rest of the road finishes.
// usage: meet_yx WORKDIR RA RB nT [T: l0 w.. l1 w..]... SOURCEFILE   (one source state per line: l0 w.. l1 w..)
// prints per source:  MEET s dS dT j  and  PATH m1 m2 ...  (source -> chain state j), or NOMEET s |ball|
#define ACC_NO_MAIN
#include "../acc_opt.c"
static St T[4096], *S; static int nT, nS;
static Tab TU, SB; static int bdS, bdT; static St bmeet; static int found;
static void cb(const St*s,int d){ uint64_t h1,h2; fp(s,&h1,&h2); int dt=tab_find(&TU,h1,h2);
    if(dt>=0 && (!found || d+dt<bdS+bdT)){ found=1; bdS=d; bdT=dt; bmeet=*s; } }
int main(int argc,char**argv){
    const char*dir=argv[1]; int RA=atoi(argv[2]), RB=atoi(argv[3]); int ai=4;
    nT=atoi(argv[ai++]); for(int i=0;i<nT;i++) ai=parse_state(argv,ai,&T[i]);
    { FILE*sf=fopen(argv[ai++],"r"); int cap=1024; S=malloc(sizeof(St)*cap); nS=0; int l0;
      while(fscanf(sf,"%d",&l0)==1){ if(nS==cap){ cap*=2; S=realloc(S,sizeof(St)*cap); } St*x=&S[nS]; x->l[0]=l0;
        for(int i=0;i<l0;i++){ int v; fscanf(sf,"%d",&v); x->w[0][i]=(uint8_t)v; } fscanf(sf,"%d",&x->l[1]);
        for(int i=0;i<x->l[1];i++){ int v; fscanf(sf,"%d",&v); x->w[1][i]=(uint8_t)v; } nS++; } fclose(sf); }
    // multi-source BFS around the whole chain
    tab_init(&TU,1u<<24); uint64_t h1,h2; FILE*o=openf(dir,"U",0,"wb");
    for(int i=0;i<nT;i++){ fp(&T[i],&h1,&h2); if(tab_ins(&TU,h1,h2,0,1)<0) wr_state(o,&T[i]); } fclose(o);
    for(int d=1;d<=RB;d++){ FILE*in=openf(dir,"U",d-1,"rb"); FILE*out=d<RB?openf(dir,"U",d,"wb"):NULL; uint64_t c=0;
        while(rd_state(in,&cur)) for(int m=0;m<14;m++){ apply(&cur,m,&nx); fp(&nx,&h1,&h2);
            if(tab_ins(&TU,h1,h2,d,1)<0){ c++; if(out) wr_state(out,&nx); } }
        fclose(in); if(out) fclose(out); if(d>=2) rmf(dir,"U",d-2);
        fprintf(stderr,"chain ball layer %d: +%llu total %llu\n",d,(unsigned long long)c,(unsigned long long)TU.n); }
    printf("CHAIN %d states, union ball %llu\n",nT,(unsigned long long)TU.n); fflush(stdout);
    for(int s=0;s<nS;s++){ found=0; tab_init(&SB,1u<<18);
        bfs(&SB,&S[s],RA,dir,"S",1,0,cb);
        if(!found){  munmap(SB.t,(size_t)16*SB.N); continue; }
        int path[64],L=0,rev[64]; St c=bmeet,n;
        for(int k=bdS;k>0;k--){ int ok=0; for(int m=0;m<14;m++){ apply(&c,m,&n); fp(&n,&h1,&h2); if(tab_find(&SB,h1,h2)==k-1){ rev[bdS-k]=INV[m]; c=n; ok=1; break; } } if(!ok) die("rebuild S"); }
        if(!st_eq(&c,&S[s])) die("rebuild S end");
        for(int i=bdS-1;i>=0;i--) path[L++]=rev[i];
        c=bmeet; for(int k=bdT;k>0;k--){ int ok=0; for(int m=0;m<14;m++){ apply(&c,m,&n); fp(&n,&h1,&h2); if(tab_find(&TU,h1,h2)==k-1){ path[L++]=m; c=n; ok=1; break; } } if(!ok) die("rebuild T"); }
        int j=-1; for(int i=0;i<nT;i++) if(st_eq(&c,&T[i])){ j=i; break; }
        printf("MEET %d %d %d %d\nPATH",s,bdS,bdT,j); for(int i=0;i<L;i++) printf(" %d",path[i]); printf("\n"); fflush(stdout);
        munmap(SB.t,(size_t)16*SB.N); }
    return 0; }
