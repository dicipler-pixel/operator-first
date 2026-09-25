#!/usr/bin/env python3
"""Mad Hatters ACC toolkit for Gemini/Colab — pure Python, no dependencies.

WHAT: official SAIR Andrews-Curtis rules (ac-r2-v1), our target rows with their starting relators,
      a replay checker that mirrors the official verifier, Stable AC finishing, and the official CLI call.

LETTERS  (official ints):  x=1  X=x^-1=-1  y=2  Y=y^-1=-2
MOVES 0..13 (each result freely reduced; NOT cyclically reduced):
   0: r0 <- r0^-1            1: r1 <- r1^-1
   2: r0 <- r0 r1            3: r0 <- r0 r1^-1
   4: r1 <- r1 r0            5: r1 <- r1 r0^-1
   6: r0 <- x r0 X   7: r0 <- X r0 x   8: r0 <- y r0 Y   9: r0 <- Y r0 y
  10: r1 <- x r1 X  11: r1 <- X r1 x  12: r1 <- y r1 Y  13: r1 <- Y r1 y
  inverse pairs: 0<->0, 1<->1, 2<->3, 4<->5, 6<->7, 8<->9, 10<->11, 12<->13
GOAL: exactly r0=[1] (x), r1=[2] (y).  Score = number of moves; shorter is better.
LIMITS: path <= 100000 moves, total relator length <= 10000 at every step.

STABLE AC (sac-XXXXX, same starting relators, spec sac-r8-v1):
   any AC path P gives  P + [16,15]  (length len(P)+2).
   also: solve the SWAPPED start (x<->y in both relators) with AC path Q,
         map Q's moves 6<->8, 7<->9, 10<->12, 11<->13, then append [15,15].
   Always confirm SAC lines with the official CLI (below) - this file only replays AC.

USAGE
   from acc_toolkit import TARGETS, replay, check, render
   check('ac-00005', [8,7,4,12,12,12,1,4,6,4,13,13,11,3,13,10,12,6,4,7,8,3,3,5,5,5,2])   -> True
   python3 acc_toolkit.py list          # print targets with relator strings
   python3 acc_toolkit.py check FILE    # check every 'ac-XXXXX: [..]' line in FILE

OFFICIAL CHECK (authoritative; run before reporting anything):
   git clone https://github.com/SAIRcompetition/Andrews-Curtis sair
   cd sair && git checkout a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e
   PYTHONPATH=competition/tools python3 -m verifier --manifest competition/tools/verifier/data/manifest.json --submission FILE
"""
import json, re, sys
TARGETS = [{"id": "ac-00003", "record": 40, "k": 2, "r0": [-2, -2, -2, -2, -1, 2, 2, 2, 1], "r1": [-2, -2, -2, -2, -2, 1, -2, -2, -1, -1], "r0_str": "YYYYXyyyx", "r1_str": "YYYYYxYYXX"}, {"id": "ac-00009", "record": 34, "k": 3, "r0": [-2, -2, 1, 2, 1, 2, -1], "r1": [-2, -2, 1, 2, 1, 2, 1, 2, -1, -2, -1, -1, -1, -2, -1], "r0_str": "YYxyxyX", "r1_str": "YYxyxyxyXYXXXYX"}, {"id": "ac-00028", "record": 48, "k": 2, "r0": [-2, -2, -2, -1, -1, -2, 1], "r1": [-2, -2, -2, -2, -1, 2, 2, 2, 1], "r0_str": "YYYXXYx", "r1_str": "YYYYXyyyx"}, {"id": "ac-00042", "record": 47, "k": 2, "r0": [-2, -2, -2, -2, -1, 2, 2, 2, 1], "r1": [-2, -2, -2, -2, -2, 1, 2, 2, 2, -1, -1], "r0_str": "YYYYXyyyx", "r1_str": "YYYYYxyyyXX"}, {"id": "ac-00052", "record": 49, "k": 2, "r0": [-2, -2, -1, -1, -2, 1, 1, 1, 1, 1, 1], "r1": [-2, -2, -1, -1, -2, 1, 1, 2, -1, -2, -2, 1, 1, 1, 1, 1, 1], "r0_str": "YYXXYxxxxxx", "r1_str": "YYXXYxxyXYYxxxxxx"}, {"id": "ac-00048", "record": 98, "k": 1, "r0": [-2, -2, -2, -1, 2, 2, 2, -1, 2, -1, 2, 2, -1, -1, 2, 2, -1], "r1": [-2, -2, -2, 1, 2, 2, 1, -2, 1, -2, 1, 1, -2, -2, 1, -2, 1], "r0_str": "YYYXyyyXyXyyXXyyX", "r1_str": "YYYxyyxYxYxxYYxYx"}, {"id": "ac-00046", "record": 117, "k": 1, "r0": [-2, -2, -2, -2, -1, -2, -2, -1, -2, 1], "r1": [-2, -2, -2, -2, -2, -2, -1, 2, 2, 2, 2, 2, 1], "r0_str": "YYYYXYYXYx", "r1_str": "YYYYYYXyyyyyx"}, {"id": "ac-00016", "record": 79, "k": 2, "r0": [-2, -2, -1, 2, 1, -2, -2, 1], "r1": [-2, -2, -2, -2, -2, -2, -1, 2, 2, 2, 2, 2, 1], "r0_str": "YYXyxYYx", "r1_str": "YYYYYYXyyyyyx"}, {"id": "ac-00031", "record": 93, "k": 2, "r0": [-2, -2, -1, 2, -1, 2, 2, 1], "r1": [-2, -2, -2, -2, 1, 1, -2, -1, -2, 1, 2, 1, 2, 1, -2, -2, -2, 1, -2, 1, 2, 2, -1, 2, -1], "r0_str": "YYXyXyyx", "r1_str": "YYYYxxYXYxyxyxYYYxYxyyXyX"}, {"id": "ac-03467", "record": None, "k": 0, "r0": [-2, -2, -2, -1, 2, 2, 1], "r1": [-2, -1, -1, -2, 1, 1, 1], "r0_str": "YYYXyyx", "r1_str": "YXXYxxx"}, {"id": "ac-08126", "record": None, "k": 0, "r0": [-2, -2, -2, -1, 2, 2, 1], "r1": [-2, -1, -1, -1, -2, 1, 1], "r0_str": "YYYXyyx", "r1_str": "YXXXYxx"}, {"id": "ac-02923", "record": None, "k": 0, "r0": [-2, -1, 2, 1, 1, 2, -1], "r1": [-2, -2, -1, 2, 2, 1, -2, 1], "r0_str": "YXyxxyX", "r1_str": "YYXyyxYx"}]
GENS = (1, -1, 2, -2)
def free_reduce(w):
    out = []
    for a in w:
        if out and out[-1] == -a: out.pop()
        else: out.append(a)
    return tuple(out)
def invert(w): return tuple(-a for a in reversed(w))
def apply_move(s, m):
    r0, r1 = s
    if m == 0: return (invert(r0), r1)
    if m == 1: return (r0, invert(r1))
    if m == 2: return (free_reduce(r0 + r1), r1)
    if m == 3: return (free_reduce(r0 + invert(r1)), r1)
    if m == 4: return (r0, free_reduce(r1 + r0))
    if m == 5: return (r0, free_reduce(r1 + invert(r0)))
    if 6 <= m <= 9: g = GENS[m - 6]; return (free_reduce((g,) + r0 + (-g,)), r1)
    if 10 <= m <= 13: g = GENS[m - 10]; return (r0, free_reduce((g,) + r1 + (-g,)))
    raise ValueError(m)
def start(cid):
    t = next(t for t in TARGETS if t['id'] == cid); return (tuple(t['r0']), tuple(t['r1']))
def replay(cid, moves, s=None):
    s = s or start(cid)
    for m in moves:
        s = apply_move(s, m)
        if len(s[0]) + len(s[1]) > 10000: raise ValueError('total relator length > 10000')
    return s
def check(cid, moves): return replay(cid, moves) == ((1,), (2,))
L = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}
def render(s): return ''.join(L[a] for a in s[0]) + ' , ' + ''.join(L[a] for a in s[1])
def swap(s): SW = {1: 2, -1: -2, 2: 1, -2: -1}; return (tuple(SW[a] for a in s[0]), tuple(SW[a] for a in s[1]))
if __name__ == '__main__':
    if sys.argv[1:2] == ['list']:
        for t in TARGETS: print(t['id'], 'record', t['record'], 'k', t['k'], '|', t['r0_str'], ',', t['r1_str'])
    elif sys.argv[1:2] == ['check']:
        for line in open(sys.argv[2]):
            m = re.match(r'^(ac-\d+): (\[.*\])', line.strip())
            if m and any(t['id'] == m[1] for t in TARGETS):
                p = json.loads(m[2]); print(m[1], len(p), 'OK' if check(m[1], p) else 'FAIL')
