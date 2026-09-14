#!/usr/bin/env python3
"""Reproduces every row of the verification table in NOTE.md.

Self-contained: nu2 is computed directly, so no claim rests on the algebra
being right. Run:  python3 verify.py
"""
import random, collections

def nu2(n):
    if n == 0: raise ValueError("nu2(0) undefined")
    v = 0
    while n % 2 == 0: n //= 2; v += 1
    return v

def count(a, m, K, j):
    return sum(1 for k in range(2**K) if a + m*k != 0 and nu2(a + m*k) == j)

fail = 0

# 1. the Lemma itself, j < K
random.seed(11); bad = n = 0
for _ in range(2000):
    K = random.randint(1, 11); j = random.randint(0, K-1)
    a = random.randint(0, 500); m = 2*random.randint(0, 250) + 1
    n += 1
    if count(a, m, K, j) != 2**(K-j-1): bad += 1
print(f"Lemma, j < K                                  trials={n:>5} mismatches={bad}"); fail += bad

# 2. general q in eoc's (B, C) parametrisation, 1 <= q <= K
random.seed(3); bad = n = 0
for _ in range(3000):
    K = random.randint(1, 11); q = random.randint(1, K)
    B = 2*random.randint(1, 300); C = 2*random.randint(0, 300) + 1
    n += 1
    if count(B, 2*C, K, q) != 2**(K-q): bad += 1
print(f"general q, 1 <= q <= K                        trials={n:>5} mismatches={bad}"); fail += bad

# 3. eoc's q = 1 claim, brute force
random.seed(11); bad = n = 0
for _ in range(4000):
    K = random.randint(1, 11)
    B = 2*random.randint(1, 200); C = 2*random.randint(0, 200) + 1
    n += 1
    if count(B, 2*C, K, 1) != 2**(K-1): bad += 1
print(f"eoc q=1 claim vs brute force                  trials={n:>5} mismatches={bad}"); fail += bad

# 4. the Lemma at j = 0 reproducing eoc's claim via B = 2B'
random.seed(11); bad = n = 0
for _ in range(4000):
    K = random.randint(1, 11)
    B = 2*random.randint(1, 200); C = 2*random.randint(0, 200) + 1
    n += 1
    if count(B//2, C, K, 0) != 2**(K-1): bad += 1
print(f"Lemma at j=0 reproducing eoc's claim          trials={n:>5} mismatches={bad}"); fail += bad

# 5. sweep across the whole j range, including the boundary
random.seed(5); bad = 0
for K in range(1, 10):
    for j in range(0, K+2):
        for _ in range(60):
            a = random.randint(0, 400); m = 2*random.randint(0, 200) + 1
            got = count(a, m, K, j)
            if j < K and got != 2**(K-j-1): bad += 1
print(f"sweep K in [1,9], j in [0,K+1]                            mismatches={bad} (j<K rows)"); fail += bad

# 6. the boundary: q > K must give 0 or 1, never more
random.seed(3); c = collections.Counter(); bad = 0
for _ in range(1500):
    K = random.randint(1, 9); q = random.randint(K+1, K+3)
    B = 2*random.randint(1, 300); C = 2*random.randint(0, 300) + 1
    g = count(B, 2*C, K, q); c[g] += 1
    if g > 1: bad += 1
print(f"boundary q > K, observed counts {dict(sorted(c.items()))}          violations={bad}"); fail += bad

print()
print("ALL CHECKS PASS" if fail == 0 else f"FAILURES: {fail}")
raise SystemExit(1 if fail else 0)
