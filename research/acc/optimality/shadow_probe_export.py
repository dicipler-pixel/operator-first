"""Export SL(2,p) shadow probes for acc_beam (BEAM_SHADOW / BEAM_SHADOW_FILE).
Binary layout (little-endian): b'SHDW', uint32 K; then per probe: uint32 n, uint16 one, uint16 img[4]
(images of the letter codes 0=x, 1=x^-1, 2=y, 3=y^-1), uint16 mul[n*n], uint8 dist[n*n]
(exact shadow distance of (a, b) to (phi(x), phi(y)); 255 = unreached).
usage: shadow_probe_export.py OUT.bin p:a,b,c,d:e,f,g,h [...]"""
import struct, sys
from collections import deque


def probe(p, X, Y):
    els = [(a, b, c, d) for a in range(p) for b in range(p) for c in range(p) for d in range(p)
           if (a * d - b * c) % p == 1]
    ix = {e: i for i, e in enumerate(els)}; n = len(els)
    mm = lambda u, v: ((u[0]*v[0]+u[1]*v[2]) % p, (u[0]*v[1]+u[1]*v[3]) % p,
                       (u[2]*v[0]+u[3]*v[2]) % p, (u[2]*v[1]+u[3]*v[3]) % p)
    inv = [ix[(e[3], -e[1] % p, -e[2] % p, e[0])] for e in els]
    mul = [[ix[mm(els[i], els[j])] for j in range(n)] for i in range(n)]
    gx, gy = ix[tuple(v % p for v in X)], ix[tuple(v % p for v in Y)]
    cons = [gx, inv[gx], gy, inv[gy]]
    conj = [[mul[mul[c][i]][inv[c]] for i in range(n)] for c in cons]
    dist = bytearray([255]) * (n * n); t = gx * n + gy; dist[t] = 0; q = deque([t])
    while q:
        s = q.popleft(); a, b = divmod(s, n); d = dist[s] + 1
        for u in ([inv[a]*n+b, a*n+inv[b], mul[a][b]*n+b, mul[a][inv[b]]*n+b, a*n+mul[b][a], a*n+mul[b][inv[a]]]
                  + [conj[k][a]*n+b for k in range(4)] + [a*n+conj[k][b] for k in range(4)]):
            if dist[u] == 255:
                dist[u] = d; q.append(u)
    one = ix[(1, 0, 0, 1)]
    blob = struct.pack('<IH4H', n, one, gx, inv[gx], gy, inv[gy])
    blob += struct.pack('<%dH' % (n * n), *[mul[i][j] for i in range(n) for j in range(n)])
    return blob + bytes(dist)


if __name__ == '__main__':
    out, specs = sys.argv[1], sys.argv[2:]
    data = b'SHDW' + struct.pack('<I', len(specs))
    for sp in specs:
        p, X, Y = sp.split(':')
        data += probe(int(p), tuple(map(int, X.split(','))), tuple(map(int, Y.split(','))))
    open(out, 'wb').write(data)
    print(out, len(specs), 'probes', len(data), 'bytes')
