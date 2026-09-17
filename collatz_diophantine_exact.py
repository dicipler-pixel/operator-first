#!/usr/bin/env python3
"""Exact saturated Collatz barrier scanner.

No floating point and no numerical logarithms are used.

Let lambda = log_2(3).  For m >= 1,

    p_m = ceil(m lambda) = bit_length(3**m),
    u_i = floor(i lambda) = bit_length(3**i) - 1.

If

    C_m = sum_{i < m} 3**(m-1-i) * 2**u_i,
    G_m = 2**p_m - 3**m,

then the saturated first-contraction barrier is exactly the rational number

    H*_m = C_m / G_m.

The recurrence C_{m+1} = 3 C_m + 2**u_m lets us scan record barriers using
integer arithmetic only.  Rational comparisons are done by cross products.

A second exact scan tracks strict record minima of the upper approximation
p_m/m to log_2(3).  Because every p_m is computed from bit length, this scan
also uses no real logarithm.  Through m=10,000 its record pairs coincide
exactly with the saturated-barrier record pairs; CI treats that as a finite
regression fact, not as an infinite theorem.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from math import gcd


KNOWN_RECORDS_THROUGH_10000 = [
    1, 3, 5, 17, 29, 41, 94, 147, 200, 253, 306,
    971, 1636, 2301, 2966, 3631, 4296, 4961, 5626,
    6291, 6956, 7621, 8286, 8951, 9616,
]


@dataclass(frozen=True)
class BarrierRecord:
    m: int
    p: int
    correction: int
    gap: int

    @property
    def reduced_upper_approximation(self) -> tuple[int, int]:
        g = gcd(self.p, self.m)
        return self.p // g, self.m // g


def scan_exact_barrier_records(limit: int) -> list[BarrierRecord]:
    if limit < 1:
        return []

    # At the start of the m-loop, pow3 = 3**(m-1) and correction = C_{m-1}.
    pow3 = 1
    correction = 0
    records: list[BarrierRecord] = []
    best_c = 0
    best_g = 1

    for m in range(1, limit + 1):
        # u_{m-1} = floor((m-1) log_2 3), exactly from the integer 3**(m-1).
        u = pow3.bit_length() - 1
        assert (1 << u) <= pow3 < (1 << (u + 1))

        correction = 3 * correction + (1 << u)
        pow3 *= 3  # now exactly 3**m

        # 3**m is never a power of two for m>0, so bit_length is ceil(log_2(3**m)).
        p = pow3.bit_length()
        assert (1 << (p - 1)) < pow3 < (1 << p)

        gap = (1 << p) - pow3
        assert gap > 0

        # C_m / G_m > best_c / best_g iff C_m*best_g > best_c*G_m.
        if not records or correction * best_g > best_c * gap:
            record = BarrierRecord(m=m, p=p, correction=correction, gap=gap)
            records.append(record)
            best_c, best_g = correction, gap

    return records


def scan_exact_upper_approximation_records(limit: int) -> list[tuple[int, int]]:
    """Strict record minima of p_m/m, where p_m=ceil(m log_2 3).

    The comparison p/m < p0/m0 is performed as p*m0 < p0*m, so neither
    log_2(3) nor floating-point arithmetic occurs in this scan.
    """
    if limit < 1:
        return []

    pow3 = 1
    records: list[tuple[int, int]] = []
    best_m = 0
    best_p = 0

    for m in range(1, limit + 1):
        pow3 *= 3
        p = pow3.bit_length()
        assert (1 << (p - 1)) < pow3 < (1 << p)

        if not records or p * best_m < best_p * m:
            records.append((m, p))
            best_m, best_p = m, p

    return records


def check_known(records: list[BarrierRecord], limit: int) -> None:
    checked_limit = min(limit, 10_000)
    expected = [m for m in KNOWN_RECORDS_THROUGH_10000 if m <= checked_limit]
    checked = [r for r in records if r.m <= checked_limit]
    actual = [r.m for r in checked]
    if actual != expected:
        raise AssertionError(
            f"record mismatch through {checked_limit}: expected {expected}, got {actual}"
        )

    # The barrier-record pairs coincide exactly with strict record minima of
    # the upper approximants p_m/m on this finite range.
    upper_records = scan_exact_upper_approximation_records(checked_limit)
    barrier_pairs = [(r.m, r.p) for r in checked]
    if barrier_pairs != upper_records:
        raise AssertionError(
            "barrier records and exact upper-approximation records differ "
            f"through {checked_limit}: barrier={barrier_pairs}, upper={upper_records}"
        )

    # The observed record upper approximants p_m/m are reduced, and consecutive
    # records through 10,000 are Farey neighbours with determinant +1.
    for r in checked:
        if gcd(r.p, r.m) != 1:
            raise AssertionError(f"record p/m is not reduced at m={r.m}")

    for left, right in zip(checked, checked[1:]):
        det = left.p * right.m - right.p * left.m
        if det != 1:
            raise AssertionError(
                f"unexpected consecutive-record determinant {det} at "
                f"m={left.m},{right.m}"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--limit", type=int, default=10_000)
    parser.add_argument(
        "--check-known",
        action="store_true",
        help="assert the exact record ledger through min(limit, 10000)",
    )
    args = parser.parse_args()

    records = scan_exact_barrier_records(args.limit)
    upper_records = scan_exact_upper_approximation_records(args.limit)
    if args.check_known:
        check_known(records, args.limit)

    print(f"exact saturated Collatz barrier scan: m <= {args.limit}")
    print(f"barrier record count: {len(records)}")
    print(f"upper-approximation record count: {len(upper_records)}")
    print("m\tp\tgap_bits\tcorrection_bits\tp/m")
    for r in records:
        num, den = r.reduced_upper_approximation
        print(
            f"{r.m}\t{r.p}\t{r.gap.bit_length()}\t"
            f"{r.correction.bit_length()}\t{num}/{den}"
        )

    if args.check_known:
        print("known-record regression: PASS")
        print("barrier = exact upper-approximation records through checked range: PASS")


if __name__ == "__main__":
    main()
