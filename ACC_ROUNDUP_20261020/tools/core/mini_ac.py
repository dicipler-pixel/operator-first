#!/usr/bin/env python3
"""Reference replay of the 14 SAIR AC moves (ac-r2-v1) for self-checks. The official SAIR verifier is still the judge:
Mad Hatters replays every route on it before anything is sent.
Words: strings over x, X (= x^-1), y, Y (= y^-1). After every move each relator is freely reduced (no cyclic reduction).
usage: python3 mini_ac.py R0 R1 "1, 6, 5, ..."     -> prints each state and whether the route ends at (x, y) or (y, x)"""
import sys
INV = {"x": "X", "X": "x", "y": "Y", "Y": "y"}
def red(w):
    out = []
    for c in w:
        if out and out[-1] == INV[c]: out.pop()
        else: out.append(c)
    return "".join(out)
def inv(w): return "".join(INV[c] for c in reversed(w))
def move(r, m):
    r0, r1 = r
    if m == 0: r0 = inv(r0)
    elif m == 1: r1 = inv(r1)
    elif m == 2: r0 = r0 + r1
    elif m == 3: r0 = r0 + inv(r1)
    elif m == 4: r1 = r1 + r0
    elif m == 5: r1 = r1 + inv(r0)
    elif 6 <= m <= 13:
        g = "xXyY"[(m - 6) % 4]          # 6/10: x, 7/11: X, 8/12: y, 9/13: Y
        if m < 10: r0 = g + r0 + INV[g]
        else: r1 = g + r1 + INV[g]
    else: raise ValueError("AC moves are 0..13 (Stable finish [16, 15] is appended after reaching (x,y) or (y,x))")
    return red(r0), red(r1)
if __name__ == "__main__":
    r = (red(sys.argv[1]), red(sys.argv[2])); route = [int(t) for t in sys.argv[3].replace("[", "").replace("]", "").split(",") if t.strip()]
    print(0, "start", r, len(r[0]) + len(r[1]))
    for i, m in enumerate(route, 1):
        r = move(r, m); print(i, m, r, len(r[0]) + len(r[1]))
    print("ENDS AT (x, y): AC route ok" if r == ("x", "y") else "ENDS AT (y, x): AC NOT ok, Stable ok with [16, 15]" if r == ("y", "x") else "NOT FINISHED")
