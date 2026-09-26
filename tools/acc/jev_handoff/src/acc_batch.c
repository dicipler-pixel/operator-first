// Batch meet: load T_B once, then for each start line "tag l0 w.. l1 w.." compute
// min dS+dT over S_A ∩ T_B (exact distance if <= A+B), rebuild and print the path.
// Same kernel/fingerprint/table as acc_opt.c (included verbatim). No length cap.
// usage: acc_batch TFILE B A WORKDIR < starts.txt
#define ACC_NO_MAIN
#include "acc_opt.c"
int main(int argc,char**argv){
    const char*tf=argv[1]; gB=atoi(argv[2]); gA=atoi(argv[3]); const char*dir=argv[4];
    struct stat stt; int fd=open(tf,O_RDONLY); if(fd<0||fstat(fd,&stt)) die("tfile");
    TT.t=mmap(0,stt.st_size,PROT_READ,MAP_SHARED|MAP_POPULATE,fd,0); if(TT.t==MAP_FAILED) die("mmap T");
    TT.N=stt.st_size/16; TT.n=0;
    char tag[64]; static St s0; double t0=now(); long nrow=0;
    while(scanf("%63s",tag)==1){
        for(int j=0;j<2;j++){ if(scanf("%d",&s0.l[j])!=1) die("in"); for(int i=0;i<s0.l[j];i++){ int x; if(scanf("%d",&x)!=1) die("in"); s0.w[j][i]=(uint8_t)x; } }
        tab_init(&SS,1u<<20); best=99; meets=0;
        bfs(&SS,&s0,gA,dir,"batch",1,0,on_new);
        rmf(dir,"batch",gA-1); rmf(dir,"batch",gA);
        printf("%s S=%llu meets=%llu",tag,(unsigned long long)SS.n,(unsigned long long)meets);
        if(best<99){ int path[128]; int L=rebuild(&s0,path); printf(" dist=%d rebuild=%d path",best,L); for(int i=0;i<L;i++) printf(" %d",path[i]); }
        else printf(" dist>%d",gA+gB);
        printf("\n"); fflush(stdout);
        munmap(SS.t,(size_t)16*SS.N); nrow++;
    }
    fprintf(stderr,"batch done rows=%ld wall=%.1fs\n",nrow,now()-t0); return 0;
}
