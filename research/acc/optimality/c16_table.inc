// ---- ceiling finish table ("C16"), shared by acc_c16.c (builder) and acc_beam.c (BEAM_C16) ----
// Contents: every state reachable from (x,y) through states of total relator length <= CEIL, with its BFS distance
// inside that ceiling graph. Moves are reversible (INV[] in acc_opt.c), so this is the distance *to* (x,y) inside the
// ceiling, an upper bound on the true AC distance (a shortest path may need to climb above CEIL). Idea: rival method
// nahom §2.1 (research/acc/live/RIVAL_METHODS_20260928.md).
// Keys are EXACT, not fingerprints: a state with l0+l1 <= CEIL <= 22 packs into 54 bits,
//   bits 0..4 = l0, bits 5..9 = l1, bits 10.. = the letters of r0 then r1, 2 bits each (0=x 1=x^-1 2=y 3=y^-1).
// Slot word (8 bytes): bit 63 = occupied, bits 55..62 = distance (8 bits, 0..255), bits 0..54 = key.
// So unlike the Tab layout (16-byte slots, 123 fingerprint bits, 4-bit distance) no fingerprint bits are spent and
// there are no collisions; the price is the CEIL <= 22 limit. Home slot = mulhi(fmix_a(key), N), linear probing.
// File: a 64-byte header (C16Hdr) followed by N slot words.
#define C16_OCC (1ULL<<63)
#define C16_KEY ((1ULL<<55)-1)
#define C16_DSH 55
#define C16_MAXCEIL 22
typedef struct { char magic[8]; uint32_t ver,ceil; uint64_t N,n; uint32_t maxd,complete; uint8_t pad[24]; } C16Hdr;
typedef struct { uint64_t*t; uint64_t N,n; int ceil; void*map; size_t maplen; } C16;
static inline uint64_t c16_pack(const St*s){ uint64_t k=(uint64_t)s->l[0]|((uint64_t)s->l[1]<<5); int b=10;
  for(int j=0;j<2;j++) for(int i=0;i<s->l[j];i++,b+=2) k|=(uint64_t)s->w[j][i]<<b; return k; }
static inline void c16_unpack(uint64_t k,St*s){ s->l[0]=(int)(k&31); s->l[1]=(int)((k>>5)&31); int b=10;
  for(int j=0;j<2;j++) for(int i=0;i<s->l[j];i++,b+=2) s->w[j][i]=(uint8_t)((k>>b)&3); }
static inline uint64_t c16_home(const C16*T,uint64_t k){ return (uint64_t)(((unsigned __int128)fmix_a(k*0x9E3779B97F4A7C15ULL+0x632BE59BD9B4E019ULL)*T->N)>>64); }
static inline int c16_find(const C16*T,uint64_t k){ uint64_t i=c16_home(T,k);
  for(;;){ uint64_t a=T->t[i]; if(!a) return -1; if((a&C16_KEY)==k) return (int)((a>>C16_DSH)&255); if(++i==T->N) i=0; } }
static inline int c16_ins(C16*T,uint64_t k,int d){ uint64_t i=c16_home(T,k);   // existing distance, or -1 if inserted
  for(;;){ uint64_t a=T->t[i]; if(!a){ T->t[i]=C16_OCC|((uint64_t)d<<C16_DSH)|k; T->n++; return -1; }
    if((a&C16_KEY)==k) return (int)((a>>C16_DSH)&255); if(++i==T->N) i=0; } }
static inline int c16_lookup(const C16*T,const St*s){ if(s->l[0]+s->l[1]>T->ceil) return -1; return c16_find(T,c16_pack(s)); }
static void c16_alloc(C16*T,uint64_t N,int ceil){ T->N=N; T->n=0; T->ceil=ceil; T->maplen=(size_t)8*N;
  T->t=mmap(0,T->maplen,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS,-1,0); if(T->t==MAP_FAILED) die("mmap c16");
  madvise(T->t,T->maplen,MADV_HUGEPAGE); T->map=T->t; }
static void c16_free(C16*T){ munmap(T->map,T->maplen); T->t=NULL; T->map=NULL; }
static void c16_save(const C16*T,const char*fn,int maxd,int complete){ C16Hdr h; memset(&h,0,sizeof h); memcpy(h.magic,"ACCC16\0",8);
  h.ver=1; h.ceil=(uint32_t)T->ceil; h.N=T->N; h.n=T->n; h.maxd=(uint32_t)maxd; h.complete=(uint32_t)complete;
  FILE*f=fopen(fn,"wb"); if(!f) die("c16 out"); setvbuf(f,NULL,_IOFBF,1<<24);
  if(fwrite(&h,sizeof h,1,f)!=1||fwrite(T->t,8,T->N,f)!=T->N) die("c16 write"); if(fclose(f)) die("c16 close"); }
static void c16_load(C16*T,const char*fn,C16Hdr*ho){ struct stat st; int fd=open(fn,O_RDONLY); if(fd<0||fstat(fd,&st)) die("c16 file");
  if((size_t)st.st_size<sizeof(C16Hdr)) die("c16 short");
  void*p=mmap(0,st.st_size,PROT_READ,MAP_SHARED|MAP_POPULATE,fd,0); if(p==MAP_FAILED) die("mmap c16 file"); close(fd);
  C16Hdr h; memcpy(&h,p,sizeof h); if(memcmp(h.magic,"ACCC16\0",8)||h.ver!=1) die("c16 magic");
  if((uint64_t)st.st_size!=sizeof(C16Hdr)+8*h.N||h.ceil>C16_MAXCEIL) die("c16 size");
  T->map=p; T->maplen=st.st_size; T->t=(uint64_t*)((char*)p+sizeof(C16Hdr)); T->N=h.N; T->n=h.n; T->ceil=(int)h.ceil; if(ho) *ho=h; }
// greedy descent from s (C16 distance k): each step takes the first move (0..13) to an in-ceiling neighbour at k-1.
// Writes the k moves to path; returns 0, or -1 if no neighbour at k-1 exists (cannot happen for a BFS table).
static int c16_descend(const C16*T,const St*s,int k,int*path){ static St c,n; c=*s;
  for(int j=k;j>0;j--){ int ok=0; for(int m=0;m<14;m++){ apply(&c,m,&n); if(c16_lookup(T,&n)==j-1){ path[k-j]=m; c=n; ok=1; break; } }
    if(!ok) return -1; }
  return (c.l[0]==1&&c.l[1]==1&&c.w[0][0]==0&&c.w[1][0]==2)?0:-2; }
// ---- C16 end ----
