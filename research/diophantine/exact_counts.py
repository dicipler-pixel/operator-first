"""Exact character sums using an integer NTT, never floating point convolution.

The cyclic correlation coefficient is between -p and p. Modulus 998244353
therefore recovers the signed integer uniquely for the declared p <= 100000.
Products of reduced residues fit signed int64. Direct sums are an independent
reference implementation used by the experiment and verification suite.
"""
from functools import lru_cache
import numpy as np
MOD = 998244353

@lru_cache(None)
def reverse_bits(n):
    v = np.arange(n, dtype=np.int64); r = np.zeros(n, dtype=np.int64)
    for _ in range(n.bit_length()-1): r = (r << 1) | (v & 1); v >>= 1
    return r

@lru_cache(None)
def powers(length, inverse):
    root = pow(3, (MOD-1)//length, MOD)
    if inverse: root = pow(root, MOD-2, MOD)
    w = [1]
    for _ in range(length//2-1): w.append(w[-1]*root % MOD)
    return np.array(w, dtype=np.int64)

def ntt(a, inverse=False):
    a = np.asarray(a, dtype=np.int64)[reverse_bits(len(a))].copy() % MOD
    length = 2
    while length <= len(a):
        blocks = a.reshape(-1, length); u = blocks[:, :length//2].copy()
        v = blocks[:, length//2:] * powers(length, inverse) % MOD
        blocks[:, :length//2] = (u+v) % MOD
        blocks[:, length//2:] = (u-v) % MOD
        length *= 2
    if inverse: a = a * pow(len(a), MOD-2, MOD) % MOD
    return a

def legendre(p):
    c = np.full(p, -1, dtype=np.int64); x = np.arange(p, dtype=np.int64)
    c[x*x % p] = 1; c[0] = 0
    return c

def correlation(p, chi, b, coefficient=-4):
    if not 3 <= p <= 100000: raise ValueError('NTT proof bound requires 3 <= p <= 100000')
    x = np.arange(p, dtype=np.int64)
    g = coefficient*((x*x % p)*x % p+b*x) % p
    h = np.bincount((-g) % p, minlength=p)
    n = 1 << (2*p-2).bit_length()
    left = np.pad(h, (0,n-p)); right = np.pad(chi, (0,n-p))
    conv = ntt(ntt(left)*ntt(right) % MOD, True)
    result = conv[:p].copy(); result[:p-1] = (result[:p-1]+conv[p:2*p-1]) % MOD
    result[result > MOD//2] -= MOD
    assert np.max(abs(result)) <= p
    return result

def direct(p, chi, b, shifts, coefficient=-4):
    x = np.arange(p, dtype=np.int64)
    g = coefficient*(x**3+b*x) % p
    return np.array([chi[(g+int(v)) % p].sum() for v in shifts], dtype=np.int64)
