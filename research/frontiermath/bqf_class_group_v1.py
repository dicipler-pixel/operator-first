"""Exact form-class-group arithmetic for small negative discriminants.

This is a real arithmetic engine, not a stand-in: reduction and composition
are exact integer operations, and composition is done by multiplying the
corresponding ideals in the order of discriminant D and reducing the
resulting rank-2 lattice to Hermite normal form.

Scope is deliberately fenced.  Enumerating reduced forms costs O(|D|) work,
so this engine refuses discriminants large enough to make that dishonest.
The Elkies boundary discriminants are around 10^29 and are firmly out of
reach here: they need a subexponential class-group algorithm (PARI, Sage,
Magma).  This module exists to control-test the small cases exactly.

A form is a tuple (a, b, c) with b*b - 4*a*c = D, a > 0.
"""

from math import isqrt, gcd

# Enumerating reduced forms is O(|D|); refuse anything where that would be a lie.
MAX_ABS_DISCRIMINANT = 10 ** 9


def is_discriminant(D):
    return D < 0 and D % 4 in (0, 1)


def disc(f):
    a, b, c = f
    return b * b - 4 * a * c


def reduce_form(f):
    """The unique reduced form in the proper equivalence class of f."""
    a, b, c = f
    if a <= 0:
        raise ValueError("positive definite forms only")
    while True:
        if c < a:
            a, b, c = c, -b, a
            continue
        # normalise b into (-a, a]
        if b > a or b <= -a:
            m = (a - b) // (2 * a)
            b_new = b + 2 * a * m
            c = (b_new * b_new - disc((a, b, c))) // (4 * a) if False else c
            # recompute c from the discriminant to stay exact
            D = b * b - 4 * a * c
            b = b_new
            c = (b * b - D) // (4 * a)
            continue
        break
    if a == c and b < 0:
        b = -b
    if b == -a:
        b = a
    D = b * b - 4 * a * c
    c = (b * b - D) // (4 * a)
    return (a, b, c)


def is_reduced(f):
    a, b, c = f
    if not (abs(b) <= a <= c):
        return False
    if (abs(b) == a or a == c) and b < 0:
        return False
    return True


def principal_form(D):
    if D % 4 == 0:
        return reduce_form((1, 0, -D // 4))
    return reduce_form((1, 1, (1 - D) // 4))


def reduced_forms(D):
    """Every reduced primitive positive definite form of discriminant D."""
    if not is_discriminant(D):
        raise ValueError("D must be negative and 0 or 1 mod 4")
    if abs(D) > MAX_ABS_DISCRIMINANT:
        raise ValueError(
            f"|D|={abs(D)} exceeds the honest enumeration limit "
            f"{MAX_ABS_DISCRIMINANT}; use PARI/Sage/Magma for this one")
    out = []
    amax = isqrt(abs(D) // 3)
    for a in range(1, amax + 1):
        for b in range(-a + 1, a + 1):
            if (b * b - D) % (4 * a):
                continue
            c = (b * b - D) // (4 * a)
            if c < a:
                continue
            if gcd(gcd(a, b), c) != 1:
                continue
            if (a == c or b == a) and b < 0:
                continue
            out.append((a, b, c))
    return out


def class_number(D):
    return len(reduced_forms(D))


# ----- composition via ideal multiplication --------------------------------
#
# The order of discriminant D has Z-basis [1, w] with w = (D + sqrt(D))/2 and
#     w^2 = D*w - (D*D - D)//4.
# The form (a, b, c) corresponds to the ideal  a*Z + (w - k)*Z  with
#     k = (b + D)//2   (integral because b == D mod 2).

def _k_of(b, D):
    return (b + D) // 2


def _hnf2(rows):
    """Hermite normal form of a rank-<=2 integer lattice given by rows (x, y).

    Returns (N, x, g): the lattice is N*Z x {0} plus (x, g)*Z, with g the gcd
    of all second coordinates and 0 <= x < N (when N > 0).
    """
    g = 0
    xg = 0
    for (x, y) in rows:
        if y == 0:
            continue
        if g == 0:
            g, xg = y, x
        else:
            # combine (xg, g) and (x, y)
            old_g = g
            new_g = gcd(g, y)
            # find s,t with s*g + t*y = new_g
            s, t = _bezout(old_g, y)
            xg = s * xg + t * x
            g = new_g
    if g < 0:
        g, xg = -g, -xg
    N = 0
    for (x, y) in rows:
        if g:
            # eliminate the second coordinate using (xg, g)
            q = y // g
            if y % g:
                raise ArithmeticError("second coordinates not divisible by their gcd")
            N = gcd(N, x - q * xg)
        else:
            N = gcd(N, x)
    N = abs(N)
    if N:
        xg %= N
    return N, xg, g


def _bezout(a, b):
    """s, t with s*a + t*b = gcd(a, b)."""
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    if old_r < 0:
        old_s, old_t = -old_s, -old_t
    return old_s, old_t


def compose(f1, f2):
    """Gauss composition, computed as ideal multiplication then reduction."""
    D = disc(f1)
    if disc(f2) != D:
        raise ValueError("composition needs a common discriminant")
    a1, b1, _ = f1
    a2, b2, _ = f2
    k1, k2 = _k_of(b1, D), _k_of(b2, D)
    w2_const = -(D * D - D) // 4          # w^2 = D*w + w2_const

    rows = [
        (a1 * a2, 0),
        (-a1 * k2, a1),
        (-a2 * k1, a2),
        (k1 * k2 + w2_const, D - k1 - k2),
    ]
    N, x, g = _hnf2(rows)
    if g == 0:
        raise ArithmeticError("degenerate ideal product")
    if N % g:
        raise ArithmeticError("ideal product is not g times a primitive ideal")
    A = N // g
    if x % g:
        raise ArithmeticError("ideal product basis is not divisible by its content")
    K = (-(x // g)) % A
    b3 = (2 * K - D) % (2 * A)
    if b3 > A:
        b3 -= 2 * A
    if (b3 * b3 - D) % (4 * A):
        raise ArithmeticError("composed form has non-integral third coefficient")
    c3 = (b3 * b3 - D) // (4 * A)
    return reduce_form((A, b3, c3))


def power(f, n):
    D = disc(f)
    result = principal_form(D)
    base = reduce_form(f)
    while n > 0:
        if n & 1:
            result = compose(result, base)
        base = compose(base, base)
        n >>= 1
    return result


def order_of(f):
    D = disc(f)
    e = principal_form(D)
    g = reduce_form(f)
    cur = g
    n = 1
    while cur != e:
        cur = compose(cur, g)
        n += 1
        if n > 10 ** 6:
            raise ArithmeticError("order search ran away")
    return n


def three_torsion(D):
    """Cl(D)[3] as a list of reduced forms, plus the 3-rank."""
    e = principal_form(D)
    tors = [f for f in reduced_forms(D) if power(f, 3) == e]
    size = len(tors)
    r = 0
    while 3 ** r < size:
        r += 1
    if 3 ** r != size:
        raise ArithmeticError(
            f"|Cl[3]|={size} is not a power of 3; composition is wrong")
    return tors, r


def element_orders(D):
    return {f: order_of(f) for f in reduced_forms(D)}
