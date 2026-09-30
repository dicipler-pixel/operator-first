#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
static int oldrot(const char*d,int n){int b=0;for(int i=1;i<n;i++)if(memcmp(d+i,d+b,n)<0)b=i;return b;}
static int newrot(const char*d,int n){int i=0,j=1,k=0;while(i<n&&j<n&&k<n){unsigned char a=d[i+k],b=d[j+k];if(a==b){k++;continue;}if(a>b)i+=k+1;else j+=k+1;if(i==j)j++;k=0;}return i<j?i:j;}
static uint64_t count;
static void check(char*d,int n){memcpy(d+n,d,n);int a=oldrot(d,n),b=newrot(d,n);count++;if(a!=b){fprintf(stderr,"mismatch n=%d a=%d b=%d\n",n,a,b);exit(1);}}
int main(void){char d[2048],a[]="aAbB";uint32_t seed=20260928;
 for(int n=0;n<=9;n++){uint32_t lim=1u<<(2*n);for(uint32_t w=0;w<lim;w++){for(int j=0;j<n;j++)d[j]=a[(w>>(2*j))&3];check(d,n);}}
 for(int n=1;n<=512;n++){for(int z=0;z<32;z++){for(int j=0;j<n;j++){seed=1664525u*seed+1013904223u;d[j]=a[seed>>30];}check(d,n);}for(int period=1;period<=16;period++){for(int j=0;j<n;j++)d[j]=a[(j%period)&3];check(d,n);}}
 printf("exact least-rotation index equality: %llu cases\n",(unsigned long long)count);return 0;}
