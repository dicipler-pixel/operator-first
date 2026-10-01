"""t00285 helper: pinned verifier access, replay traces, training->challenge mapping for the
MS family w = x^-1 y^-3 x y^2 (twin of y^3 x y^-2 x^-1).  Credit: Bob's interpolation idea."""
import json, os, sys
SAIR = os.path.expanduser('~/.cache/upgh/sair')
sys.path.insert(0, SAIR + '/competition/tools')
from verifier import core  # noqa: E402

MAN = json.load(open(SAIR + '/competition/tools/verifier/data/manifest.json'))
LIM = MAN['limits']
CH = {c['challenge_id']: c for c in MAN['challenges']}
TR = json.load(open(SAIR + '/competition/examples/training_424.json'))['instances']
TRID = {t['training_id']: t for t in TR}

# training rows in this family (twin form w = x^-1 y^-3 x y^2, start (T0,T1) = (x^-1 y^n x y^-(n+1), x y^-2 x^-1 y^3 x))
TWIN = {1: 'ms-train-0341', 2: 'ms-train-0342', 3: 'ms-train-0343', 6: 'ms-train-0344'}
# direct form w = y^3 x y^-2 x^-1, start (x^-1 y^n x y^-(n+1), x x y y x^-1 y^-3)
DIRECT = {1: 'ms-train-0249', 3: 'ms-train-0250', 6: 'ms-train-0251'}
# board rows of this family (challenge start = (y^-3 x y^2 x^-2, y^-(n+1) x^-1 y^n x))
BOARD = {4: 'ac-09632', 5: 'ac-05538', 7: 'ac-09090', 8: 'ac-06811', 9: 'ac-02630', 10: 'ac-01923'}

LET = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}
def w(word): return ''.join(LET[t] for t in word) or '1'
def tot(s): return len(s[0]) + len(s[1])

def challenge_start(n):
    """official-shaped start for MS(n, x^-1 y^-3 x y^2) as the board encodes it."""
    return [[-2, -2, -2, 1, 2, 2, -1, -1], [-2] * (n + 1) + [-1] + [2] * n + [1]]

def synth(n):
    cid = BOARD.get(n)
    if cid: return CH[cid]
    return {'challenge_id': f'synth-n{n}', 'generators': ['x', 'y'], 'initial_relators': challenge_start(n),
            'target_relators': [[1], [2]], 'move_spec_version': 'ac-r2-v1'}

def states(start, moves):
    s = [tuple(tuple(r) for r in start)]
    for m in moves: s.append(core.apply_move(s[-1], m))
    return s

def trace(start, moves, out=sys.stdout):
    st = states(start, moves)
    out.write(f'  {"i":>3} {"mv":>3} {"tot":>4}  r0 | r1\n')
    out.write(f'  {0:>3} {"-":>3} {tot(st[0]):>4}  {w(st[0][0])} | {w(st[0][1])}\n')
    for i, (m, s) in enumerate(zip(moves, st[1:]), 1):
        out.write(f'  {i:>3} {m:>3} {tot(s):>4}  {w(s[0])} | {w(s[1])}\n')
    return st

SWAP = {0: 1, 1: 0, 2: 4, 3: 5, 4: 2, 5: 3, 6: 10, 7: 11, 8: 12, 9: 13, 10: 6, 11: 7, 12: 8, 13: 9}
def swap(moves): return [SWAP[m] for m in moves]

def prefix(n):
    """challenge start -> swapped training start (T1, T0): r0 <- x^-1 r0 x, invert r0, r1 <- y r1 y^-1 (n+1 times)."""
    return [7, 0] + [12] * (n + 1)
SUFFIX_21 = [0, 2, 5, 2, 8]  # canonicalization table: ([y],[x]) -> ([x],[y])

def mapped(n, train_moves):
    return prefix(n) + swap(train_moves) + SUFFIX_21

def verify(ch, moves):
    return core.verify(ch, list(moves), 'ac-r2-v1', LIM)

def trim(moves):
    """drop adjacent inverse pairs (exact: m then inverse(m) is identity on states)."""
    INV = {0: 0, 1: 1, 2: 3, 3: 2, 4: 5, 5: 4, 6: 7, 7: 6, 8: 9, 9: 8, 10: 11, 11: 10, 12: 13, 13: 12}
    out = []
    for m in moves:
        if out and INV[out[-1]] == m: out.pop()
        else: out.append(m)
    return out
