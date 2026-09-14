#!/usr/bin/env python3
"""Reproduces the n-step table in NOTE.md §4.  Exhaustive, not sampled.

Claim: #{odd N < 2^K : (a_0..a_{n-1}) = (q_1..q_n)} = 2^(K-1-S), S = sum q_i,
whenever S <= K-1; and the formula fails for every vector with S > K-1.
"""
import collections, sys
def nu2(n):
    v=0
    while n%2==0: n//=2; v+=1
    return v
def digits(N,n):
    out=[]
    for _ in range(n):
        m=3*N+1; v=nu2(m); out.append(v); N=m>>v
    return tuple(out)

print(f"{'K':>3} {'n':>2} {'S<=K-1':>8} {'exact':>7} {'off':>5} {'S>K-1':>7} {'match':>6}")
fail=0
for K,ns in ((8,(1,2,3)),(10,(1,2,3)),(12,(1,2,3)),(14,(4,5)),(16,(4,5)),(18,(4,5))):
    nmax=max(ns)
    c=collections.Counter()
    for N in range(1,2**K,2): c[digits(N,nmax)]+=1
    for n in ns:
        cc=collections.Counter()
        for vec,ct in c.items(): cc[vec[:n]]+=ct
        ins=insbad=out=outmatch=0
        for vec,got in cc.items():
            S=sum(vec)
            if S<=K-1:
                ins+=1
                if got!=2**(K-1-S): insbad+=1
            else:
                out+=1
                if got==2**(K-1)//(2**S): outmatch+=1
        print(f"{K:>3} {n:>2} {ins:>8} {ins-insbad:>7} {insbad:>5} {out:>7} {outmatch:>6}")
        fail+=insbad
print()
print("ALL EXACT INSIDE THE BUDGET" if fail==0 else f"FAILURES: {fail}")
sys.exit(1 if fail else 0)
