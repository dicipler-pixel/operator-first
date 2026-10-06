// join_bidi: cheapest join of a start state S0 onto a known trajectory (ac-r2-v1 kernel of acc_opt.c, restricted move mask):
// minimise dist(S0, traj[k]) + off_k over trajectory states (off_k = remaining offset given by the caller), by a bidirectional
// BFS whose backward side starts from every trajectory state at distance off_k (a virtual sink). Exact under the total-length cap.
// Layers live on disk (WORKDIR); visited sets are exact-depth hash tables keyed by the 128-bit fingerprint.
// usage: join_bidi WORKDIR CAP MAXTOTAL MASK TRAJFILE l0 w.. l1 w..      TRAJFILE lines: "k off l0 w.. l1 w.."
// prints  JOIN total k PATH m1 m2 ...   (S0 -> traj[k])   or   NOJOIN
#define ACC_NO_MAIN
#include "../../../optimality/acc_opt.c"
typedef struct { uint64_t *a, *b; uint16_t *d; uint64_t N, n; } H;
static void h_init(H*t,uint64_t N){ t->N=N; t->n=0; t->a=calloc(N,8); t->b=calloc(N,8); t->d=calloc(N,2); if(!t->a||!t->b||!t->d) die("h alloc"); }
static int64_t h_get(const H*t,uint64_t x,uint64_t y){ uint64_t k=x&(t->N-1); while(t->a[k]){ if(t->a[k]==x&&t->b[k]==y) return t->d[k]; k=(k+1)&(t->N-1);} return -1; }
static void h_grow(H*t);
static int h_put(H*t,uint64_t x,uint64_t y,int d){ // returns 1 if inserted or lowered
    if(2*(t->n+1)>t->N) h_grow(t);
    uint64_t k=x&(t->N-1); while(t->a[k]){ if(t->a[k]==x&&t->b[k]==y){ if(d<t->d[k]){ t->d[k]=(uint16_t)d; return 1;} return 0; } k=(k+1)&(t->N-1);}
    t->a[k]=x; t->b[k]=y; t->d[k]=(uint16_t)d; t->n++; return 1; }
static void h_grow(H*t){ H g; h_init(&g,t->N*2); for(uint64_t i=0;i<t->N;i++) if(t->a[i]){ uint64_t k=t->a[i]&(g.N-1); while(g.a[k]) k=(k+1)&(g.N-1); g.a[k]=t->a[i]; g.b[k]=t->b[i]; g.d[k]=t->d[i]; g.n++; }
    free(t->a); free(t->b); free(t->d); *t=g; }
static H TF, TB; static unsigned MASK; static int CAP;
static St trj[4096]; static int trk[4096], troff[4096], nt;
static int jbest=1<<30; static St bmeet;
static void meet(const St*s,int tot){ if(tot<jbest){ jbest=tot; bmeet=*s; } }
int main(int argc,char**argv){
    const char*dir=argv[1]; CAP=atoi(argv[2]); int MAXT=atoi(argv[3]); MASK=(unsigned)strtoul(argv[4],0,0); const char*tf=argv[5];
    St S0; parse_state(argv,6,&S0);
    FILE*f=fopen(tf,"r"); if(!f) die("trajfile"); char line[1<<16];
    while(fgets(line,sizeof line,f)){ char*p=line; int k,off,o; if(sscanf(p,"%d %d%n",&k,&off,&o)!=2) continue; p+=o; St*s=&trj[nt];
        for(int r=0;r<2;r++){ int l; sscanf(p,"%d%n",&l,&o); p+=o; s->l[r]=l; for(int i=0;i<l;i++){ int v; sscanf(p,"%d%n",&v,&o); p+=o; s->w[r][i]=(uint8_t)v; } }
        trk[nt]=k; troff[nt]=off; nt++; } fclose(f);
    h_init(&TF,1ULL<<22); h_init(&TB,1ULL<<22); uint64_t h1,h2;
    int maxoff=0; for(int i=0;i<nt;i++) if(troff[i]>maxoff) maxoff=troff[i];
    // backward layer files: initial states at their offsets
    for(int i=0;i<nt;i++){ fp(&trj[i],&h1,&h2); if(h_put(&TB,h1,h2,troff[i])){ FILE*o=openf(dir,"B",troff[i],"ab"); wr_state(o,&trj[i]); fclose(o);} }
    fp(&S0,&h1,&h2); h_put(&TF,h1,h2,0); { int64_t db=h_get(&TB,h1,h2); if(db>=0) meet(&S0,(int)db); }
    FILE*o=openf(dir,"F",0,"wb"); wr_state(o,&S0); fclose(o);
    int fd=0, bd=-1; uint64_t fcount=1; uint64_t BUD=getenv("BUDGET")?strtoull(getenv("BUDGET"),0,10):150000000ULL;
    while(1){
        if(jbest<=fd+bd+1) break; if(fd+bd+1>=MAXT) break; if(TF.n+TB.n>BUD){ fprintf(stderr,"budget stop\n"); break; }
        // size of next backward layer (file size) vs current forward layer count
        char pth[4096]; snprintf(pth,sizeof pth,"%s/B_layer%02d.bin",dir,bd+1); struct stat sb; uint64_t bsz=(stat(pth,&sb)==0)?(uint64_t)sb.st_size:0;
        int dofwd = (bd+1>maxoff+60) || (fcount*20 <= bsz) || (bsz==0 && bd+1>maxoff);
        if(dofwd){
            FILE*in=openf(dir,"F",fd,"rb"); FILE*out=openf(dir,"F",fd+1,"wb"); uint64_t c=0;
            while(rd_state(in,&cur)) for(int m=0;m<14;m++){ if(!((MASK>>m)&1)) continue; apply(&cur,m,&nx); if(nx.l[0]+nx.l[1]>CAP) continue;
                fp(&nx,&h1,&h2); if(!h_put(&TF,h1,h2,fd+1)) continue; c++; wr_state(out,&nx);
                int64_t db=h_get(&TB,h1,h2); if(db>=0) meet(&nx,fd+1+(int)db); }
            fclose(in); fclose(out); fd++; fcount=c;
            fprintf(stderr,"F d=%d +%llu (TF %llu) best=%d\n",fd,(unsigned long long)c,(unsigned long long)TF.n,jbest<(1<<30)?jbest:-1);
            if(!c) break;
        } else {
            bd++; FILE*in=openf(dir,"B",bd,"rb"); if(!in){ continue; } FILE*out=openf(dir,"B",bd+1,"ab"); uint64_t c=0;
            while(rd_state(in,&cur)){ fp(&cur,&h1,&h2); if(h_get(&TB,h1,h2)!=bd) continue;
                for(int m=0;m<14;m++){ if(!((MASK>>m)&1)) continue; apply(&cur,m,&nx); if(nx.l[0]+nx.l[1]>CAP) continue;
                    fp(&nx,&h1,&h2); if(!h_put(&TB,h1,h2,bd+1)) continue; c++; wr_state(out,&nx);
                    int64_t df=h_get(&TF,h1,h2); if(df>=0) meet(&nx,(int)df+bd+1); } }
            fclose(in); fclose(out);
            fprintf(stderr,"B d=%d +%llu (TB %llu) best=%d\n",bd+1,(unsigned long long)c,(unsigned long long)TB.n,jbest<(1<<30)?jbest:-1);
        }
    }
    if(jbest>=(1<<30)){ printf("NOJOIN\n"); return 0; }
    // rebuild forward part
    static int path[1<<14]; int L=0; St u=bmeet; fp(&u,&h1,&h2); int df=(int)h_get(&TF,h1,h2); int rev[4096];
    for(int k=df;k>0;k--){ int ok=0; for(int m=0;m<14;m++){ if(!((MASK>>m)&1)) continue; apply(&u,m,&nx); fp(&nx,&h1,&h2);
            if(h_get(&TF,h1,h2)==k-1){ rev[k-1]=INV[m]; u=nx; ok=1; break; } } if(!ok) die("rebuild F"); }
    for(int k=0;k<df;k++) path[L++]=rev[k];
    u=bmeet; fp(&u,&h1,&h2); int db=(int)h_get(&TB,h1,h2); int kk=-1;
    while(1){ for(int i=0;i<nt;i++) if(st_eq(&u,&trj[i]) && troff[i]==db){ kk=trk[i]; break; } if(kk>=0) break;
        int ok=0; for(int m=0;m<14;m++){ if(!((MASK>>m)&1)) continue; apply(&u,m,&nx); fp(&nx,&h1,&h2);
            if(h_get(&TB,h1,h2)==db-1){ path[L++]=m; u=nx; db--; ok=1; break; } } if(!ok) die("rebuild B"); }
    printf("JOIN %d %d PATH",jbest,kk); for(int i=0;i<L;i++) printf(" %d",path[i]); printf("\n");
    return 0; }
