"""Homomorphic shadows of the AC graph: certified lower bounds on AC distance.

A probe phi: F(x, y) -> G (a finite group) sends a state (r0, r1) to (phi(r0), phi(r1)) in G x G.
Each ac-r2-v1 move commutes with phi: inversion -> g^-1, multiplication -> g h^+-1, and conjugation by a
letter -> conjugation by its image. So every real path maps to a shadow path of the same length, and
the exact BFS distance in the finite shadow graph to (phi(x), phi(y)) is a lower bound on the real
distance ("exterior probe", "obstruction through a factorization"; atlas OBS-PROBE-SPAN,
ALG-FORCING-DUAL). Taking the max over several probes is still a lower bound.

G = SL(2, p), phi(x), phi(y) = two matrices. usage:
  shadow_bounds.py MANIFEST p a,b,c,d e,f,g,h OUT.json   (matrices row-major mod p)"""
import json, sys
from collections import deque


def main():
    man, p = sys.argv[1], int(sys.argv[2])
    X = tuple(int(v) % p for v in sys.argv[3].split(',')); Y = tuple(int(v) % p for v in sys.argv[4].split(','))
    out = sys.argv[5]
    els = [(a, b, c, d) for a in range(p) for b in range(p) for c in range(p) for d in range(p)
           if (a * d - b * c) % p == 1]
    ix = {e: i for i, e in enumerate(els)}; n = len(els)
    mm = lambda u, v: ((u[0]*v[0]+u[1]*v[2]) % p, (u[0]*v[1]+u[1]*v[3]) % p,
                       (u[2]*v[0]+u[3]*v[2]) % p, (u[2]*v[1]+u[3]*v[3]) % p)
    inv = [ix[(e[3], -e[1] % p, -e[2] % p, e[0])] for e in els]
    mul = [[ix[mm(els[i], els[j])] for j in range(n)] for i in range(n)]
    gx, gy = ix[X], ix[Y]
    cons = [gx, inv[gx], gy, inv[gy]]
    conj = [[mul[mul[c][i]][inv[c]] for i in range(n)] for c in cons]
    N = n * n
    dist = bytearray([255]) * N
    t = gx * n + gy
    dist[t] = 0; q = deque([t])
    while q:
        s = q.popleft(); a, b = divmod(s, n); d = dist[s] + 1
        nb = [inv[a]*n+b, a*n+inv[b], mul[a][b]*n+b, mul[a][inv[b]]*n+b, a*n+mul[b][a], a*n+mul[b][inv[a]]]
        nb += [conj[k][a]*n+b for k in range(4)] + [a*n+conj[k][b] for k in range(4)]
        for u in nb:
            if dist[u] == 255:
                dist[u] = d; q.append(u)
    img = {1: gx, -1: inv[gx], 2: gy, -2: inv[gy]}
    def word(w):
        g = ix[(1, 0, 0, 1)]
        for a in w: g = mul[g][img[a]]
        return g
    res = {}
    for c in json.load(open(man))['challenges']:
        if not c['challenge_id'].startswith('ac-'): continue
        r0, r1 = c['initial_relators']
        res[c['challenge_id']] = dist[word(r0) * n + word(r1)]
    reached = sum(1 for v in dist if v != 255)
    json.dump({'p': p, 'X': X, 'Y': Y, 'group_order': n, 'shadow_states': N, 'reached': reached,
               'diameter': max(v for v in dist if v != 255), 'h': res}, open(out, 'w'))
    print(f'SL(2,{p}) |G|={n}, shadow states {N}, reached {reached}, diameter {max(v for v in dist if v != 255)}')


if __name__ == '__main__':
    main()
