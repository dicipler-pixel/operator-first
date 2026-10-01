"""SONG12 (session 1): every state on every known road (plus 8 symmetric images) -> sorted acc_disk .set.
A forward BFS from an open row with --meet on this set finds a state that some known road passes through,
which links the open row to that road (a first solve). Moves follow tools/acc/charlie/acc_disk.cpp exactly."""
import json, re, sys, struct, pickle
S = '/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad'
MAXL = 58
MAN = {c['challenge_id']: c for c in json.load(open(S + '/sair/competition/tools/verifier/data/manifest.json'))['challenges']}
CODE = {1: 0, -1: 1, 2: 2, -2: 3}
def red(w):
    o = []
    for c in w:
        if o and o[-1] == c ^ 1: o.pop()
        else: o.append(c)
    return o
def inv(w): return [c ^ 1 for c in reversed(w)]
def move(s, m):
    a, b = s
    if m == 0: return (tuple(inv(a)), b)
    if m == 1: return (a, tuple(inv(b)))
    if 2 <= m <= 5:
        to0 = m <= 3; invo = m in (3, 5)
        x, y = (a, b) if to0 else (b, a)
        if invo: y = inv(y)
        r = red(list(x) + list(y))
        if len(r) > MAXL: return None
        return (tuple(r), b) if to0 else (a, tuple(r))
    on0 = m <= 9; c = m - 6 if on0 else m - 10
    w = a if on0 else b
    r = red([c] + list(w) + [c ^ 1])
    if len(r) > MAXL: return None
    return (tuple(r), b) if on0 else (a, tuple(r))
# symmetries: letter maps (x->X, y->Y, swap x/y) combined with relator swap
LMAPS = []
for sw in (0, 1):
    for fx in (0, 1):
        for fy in (0, 1):
            mp = [0, 1, 2, 3]
            if sw: mp = [2, 3, 0, 1]
            mp = [(v ^ fx) if v < 2 else (v ^ fy) for v in mp]
            LMAPS.append(mp)
def sym(s, k):
    mp = LMAPS[k % 8]; a = tuple(mp[c] for c in s[0]); b = tuple(mp[c] for c in s[1])
    return (b, a) if k >= 8 else (a, b)
def pack(s):
    a, b = s
    if len(a) + len(b) > MAXL: return None
    v = len(a); v = (v << 6) | len(b)
    for c in a: v = (v << 2) | c
    for c in b: v = (v << 2) | c
    v <<= 2 * (MAXL - len(a) - len(b))
    return v
if __name__ == '__main__':
    src = sys.argv[1]; out = sys.argv[2]
    pat = re.compile(r'^(s?)(ac-\d{5}):\s*(\[[0-9,\s]*\])')
    keys = {}; nroads = 0
    for line in open(src):
        m = pat.match(line.strip())
        if not m or m.group(2) not in MAN: continue
        p = json.loads(m.group(3))
        if m.group(1):
            if p[-2:] != [16, 15]: continue
            p = p[:-2]
        if any(x > 13 for x in p): continue
        c = MAN[m.group(2)]['initial_relators']
        s = (tuple(CODE[x] for x in c[0]), tuple(CODE[x] for x in c[1]))
        st = [s]
        for mv in p:
            s = move(s, mv)
            if s is None: break
            st.append(s)
        if s is None or s != ((0,), (2,)): continue
        nroads += 1
        for i, t in enumerate(st):
            for k in range(16):
                v = pack(sym(t, k))
                if v is not None and v not in keys: keys[v] = (m.group(2), i, k)
    ks = sorted(keys)
    with open(out, 'wb') as f:
        for v in ks: f.write(struct.pack('<QQ', v & (2**64 - 1), v >> 64))
    pickle.dump({'keys': keys, 'src': src}, open(out + '.idx', 'wb'))
    print('roads', nroads, 'states', len(ks))
