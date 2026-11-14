#!/usr/bin/env python3
"""Ball map: Jeromie Beasley's "Balls in One Ball" mixer (v3) applied to Andrews-Curtis states.

The mixer's picture: one ball (hyperbolic space); a peel step of ratio z moves a ball ln z along an arm; the ball at depth
L straight out sits at Gamma_L = (z^L - 1)/(z^L + 1); for two arms crossing at the centre, g = sinh(ln z1/2) sinh(ln z2/2)
decides the square a, b, back a, back b: g < 1 a TURN by 4 arccos g about a fixed point (the walk is held), g > 1 a RUN of
length 4 arccosh g (nothing returns).

Here the two arms are the generators: x = peel step of ratio zx along one axis, y = peel step of ratio zy along the
perpendicular axis through the centre (SL(2,R) acting on the hyperbolic plane). A word w is then one hyperbolic motion:
  size(w)  = its translation length 2 arccosh(|tr w|/2)   (0 for a turn) : a conjugation move never changes it
  reach(w) = how far it carries the centre (the ball's distance from the centre)
A relator pair (r0, r1) gets the mixer's PAIR reading: the square r0, r1, back r0, back r1 is a turn (held) or a run.
The goal (x, y) has sizes ln zx, ln zy. usage: ballmap.py R0 R1 [moves...]  -> the map of a road, one line per step."""
import math, sys
sys.path.insert(0, __file__.rsplit("/", 2)[0] + "/../../ACC_ROUNDUP_20261020/tools/core")

def mats(zx=5.0, zy=5.0):
    a, b = math.log(zx) / 2, math.log(zy) / 2
    X = ((math.exp(a), 0.0), (0.0, math.exp(-a)))
    Y = ((math.cosh(b), math.sinh(b)), (math.sinh(b), math.cosh(b)))
    inv = lambda M: ((M[1][1], -M[0][1]), (-M[1][0], M[0][0]))
    return {"x": X, "X": inv(X), "y": Y, "Y": inv(Y)}

def mul(A, B):
    return ((A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]),
            (A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]))

def word(w, G):
    M = ((1.0, 0.0), (0.0, 1.0))
    for c in w: M = mul(M, G[c])
    return M

def size(M):
    t = abs(M[0][0] + M[1][1]) / 2
    return 2 * math.acosh(t) if t > 1 else 0.0

def reach(M):  # distance from i to M(i) in the upper half plane
    a, b, c, d = M[0][0], M[0][1], M[1][0], M[1][1]
    return math.acosh(max(1.0, (a * a + b * b + c * c + d * d) / 2))

def pair(A, B):
    """mixer PAIR reading of the square A, B, back A, back B: ('turn', angle in degrees) or ('run', length)"""
    inv = lambda M: ((M[1][1], -M[0][1]), (-M[1][0], M[0][0]))
    C = mul(mul(A, B), mul(inv(A), inv(B))); t = (C[0][0] + C[1][1]) / 2
    return ("turn", 360 - math.degrees(2 * math.acos(max(-1, min(1, t))))) if abs(t) < 1 else ("run", 2 * math.acosh(abs(t)))

def ballmap(r0, r1, G):
    A, B = word(r0, G), word(r1, G)
    k, v = pair(A, B)
    return {"size0": size(A), "size1": size(B), "reach0": reach(A), "reach1": reach(B), "pair": k, "pairval": v}

if __name__ == "__main__":
    import mini_ac
    G = mats()
    r = (mini_ac.red(sys.argv[1]), mini_ac.red(sys.argv[2])); mv = [int(t) for t in " ".join(sys.argv[3:]).replace("[", "").replace("]", "").replace(",", " ").split()]
    for i in range(len(mv) + 1):
        m = ballmap(r[0], r[1], G)
        print("%3d %-4s |r|=%2d+%2d  size %6.2f + %6.2f  %s %.1f" % (i, mv[i - 1] if i else "", len(r[0]), len(r[1]), m["size0"], m["size1"], m["pair"], m["pairval"]))
        if i < len(mv): r = mini_ac.move(r, mv[i])
