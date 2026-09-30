"""Relator-substitution (Dehn-style) solver for first solves.

Macro move: r_i <- r_i . (u r_j^e u^-1), chosen so the conjugated relator cancels against r_i (u = a suffix of r_i
matched against a cyclic rotation of r_j^e). Every macro is compiled into official ac-r2-v1 moves by applying
conjugations to r_j (letter by letter), one multiplication, then the inverse conjugations; the state is always the
exact official state (verifier core), so compiled paths are valid by construction and re-verified at the end.
Also: rotations of r_i (conjugation by a letter), inversions, and the classic primitive endgame via acc_beam.
Search: beam over states keyed by cyclically reduced canonical pair, score = total cyclic length (+ small tie terms).
Out: JSONL {id, ok, moves, len, macros, t}. Any length counts for a first solve (limit 100000 moves).

Usage: subst_solver.py IDS_FILE OUT [W=400] [ROUNDS=300] [SLACK=2]
"""
import sys, json, os, time
S = os.environ.get('ACC_S', '/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad')
sys.path.insert(0, S + '/sair/competition/tools')
from verifier import core

MAXL = int(os.environ.get('SUB_MAXL', '400'))
MINC = int(os.environ.get('SUB_MINC', '1'))
INV = {1: 1, -1: 0, 2: 3, -2: 2}          # letter g -> index into GENS for conj by g  (GENS = 1,-1,2,-2)
def conj_move(i, g):                      # move making r_i <- g r_i g^-1
    return (6 if i == 0 else 10) + {1: 0, -1: 1, 2: 2, -2: 3}[g]
def mul_move(i, inv):                     # r_i <- r_i r_j^(+/-1)
    return {(0, False): 2, (0, True): 3, (1, False): 4, (1, True): 5}[(i, inv)]

def cyc(w):
    w = list(w)
    while len(w) > 1 and w[0] == -w[-1]: w = w[1:-1]
    return tuple(w)
def canon1(w):
    w = cyc(w)
    if not w: return ()
    best = None
    for v in (w, core.invert(w)):
        for k in range(len(v)):
            r = v[k:] + v[:k]
            if best is None or r < best: best = r
    return best
def key(s): return tuple(sorted((canon1(s[0]), canon1(s[1]))))
def clen(s): return len(cyc(s[0])) + len(cyc(s[1]))
SCORE = os.environ.get('SUB_SCORE', 'len')
def xcount(s): return sum(1 for w in s for g in cyc(w) if abs(g) == 1)
def ycount(s): return sum(1 for w in s for g in cyc(w) if abs(g) == 2)
def score(s):
    if SCORE == 'x': return (xcount(s), clen(s))
    if SCORE == 'y': return (ycount(s), clen(s))
    return (clen(s), 0)

class Node:
    __slots__ = ('s', 'mv')
    def __init__(self, s, mv): self.s, self.mv = s, mv
    def apply(self, ms):
        s = self.s
        for m in ms: s = core.apply_move(s, m)
        return Node(s, self.mv + ms)

def conj_seq(i, u):
    """moves making r_i <- u r_i u^-1 (apply innermost letter first)."""
    return [conj_move(i, g) for g in reversed(u)]

def cycnorm(node):
    """cyclically reduce both relators with exact conjugation moves."""
    ms = []; st = node.s
    for i in (0, 1):
        while len(st[i]) > 1 and st[i][0] == -st[i][-1]:
            m = conj_move(i, -st[i][0]); ms.append(m); st = core.apply_move(st, m)
    return Node(st, node.mv + ms) if ms else node

def rot_seq(i, w, t):
    """moves turning r_i = w into w[t:]+w[:t] (cyclically reduced w): conj by a^-1 (a=w[:t]) or by b (b=w[t:])."""
    a, b = w[:t], w[t:]
    return conj_seq(i, core.invert(a)) if len(a) <= len(b) else conj_seq(i, b)

def macros(node, maxu):
    """Compiled move lists: rotate r_i, then r_i <- r_i . (rotation of r_j^e) cancelling >= half of r_j."""
    s = node.s
    for i in (0, 1):
        j = 1 - i
        ri, rj = s[i], s[j]
        if not ri or not rj: continue
        n = len(rj)
        for e in (False, True):
            base = core.invert(rj) if e else rj
            for k in range(n):
                rot = base[k:] + base[:k]
                p = base[:k]
                u = core.invert(p) if k <= n - k else base[k:]
                if len(u) > maxu: continue
                for t in range(len(ri)):
                    w = ri[t:] + ri[:t]
                    c = 0
                    while c < len(w) and c < n and w[len(w) - 1 - c] == -rot[c]: c += 1
                    if c < MINC: continue
                    seq = rot_seq(i, ri, t) + conj_seq(j, u) + [mul_move(i, e)] + conj_seq(j, core.invert(u))
                    yield seq

def solve(st, W=400, rounds=300, slack=2, tlimit=int(os.environ.get('SUB_T', '600'))):
    t0 = time.time()
    beam = [cycnorm(Node(st, []))]; seen = {key(st): 0}
    best = clen(st)
    for r in range(rounds):
        if time.time() - t0 > tlimit: break
        kids = []
        for nd in beam:
            for seq in macros(nd, maxu=40):
                ch = cycnorm(nd.apply(seq))
                L = clen(ch.s)
                if L > best + slack or L > MAXL: continue
                kk = key(ch.s)
                if kk in seen and seen[kk] <= r + 1: continue
                seen[kk] = r + 1
                if L <= 2 and ch.s[0] and ch.s[1]:
                    return ch, r
                kids.append((score(ch.s), len(ch.mv), ch, L))
        if not kids: break
        kids.sort(key=lambda t: (t[0], t[1]))
        beam = [t[2] for t in kids[:W]]
        best = min(best, min(t[3] for t in kids)) if SCORE == 'len' else best
        if os.environ.get('SUB_DBG'): print('round', r, 'best', best, 'kids', len(kids), file=sys.stderr)
    return None, best

def finish(node):
    """From a pair of cyclic length 2 (each relator a conjugate of a letter), reach the exact target (x, y)."""
    import itertools
    from collections import deque
    # small BFS on exact states limited depth
    target = ((1,), (2,))
    start = node.s
    q = deque([(start, [])]); seen = {start}
    while q:
        s, mv = q.popleft()
        if s == target: return node.mv + mv
        if len(mv) >= 14: continue
        for m in range(14):
            t = core.apply_move(s, m)
            if len(t[0]) + len(t[1]) > len(start[0]) + len(start[1]) + 2: continue
            if t in seen: continue
            seen.add(t); q.append((t, mv + [m]))
    return None

if __name__ == '__main__':
    ids = [l.split()[0] for l in open(sys.argv[1]) if l.strip()]
    out = sys.argv[2]
    W = int(sys.argv[3]) if len(sys.argv) > 3 else 400
    R = int(sys.argv[4]) if len(sys.argv) > 4 else 300
    SL = int(sys.argv[5]) if len(sys.argv) > 5 else 2
    m = json.load(open(S + '/sair/competition/tools/verifier/data/manifest.json'))
    C = {c['challenge_id']: c for c in m['challenges']}
    done = set()
    if os.path.exists(out): done = {json.loads(l)['id'] for l in open(out)}
    for cid in ids:
        if cid in done: continue
        c = C[cid]; st = tuple(tuple(r) for r in c['initial_relators'])
        t0 = time.time()
        nd, info = solve(st, W, R, SL)
        rec = {'id': cid, 'ok': False, 't': round(time.time() - t0, 1)}
        if nd is not None:
            mv = finish(nd)
            if mv is not None:
                lim = {"max_path_length": 100000, "max_total_relator_length": 10000, "max_intermediate_relator_length": 10000}
                s = st
                for x in mv: s = core.apply_move(s, x)
                if s == tuple(tuple(r) for r in c['target_relators']):
                    rec.update(ok=True, len=len(mv), moves=mv)
                else: rec['end'] = str(s)
            else: rec['stuck2'] = str(nd.s)
        else: rec['best'] = info
        print(json.dumps({k: v for k, v in rec.items() if k != 'moves'}), flush=True)
        with open(out, 'a') as f: f.write(json.dumps(rec) + '\n')
