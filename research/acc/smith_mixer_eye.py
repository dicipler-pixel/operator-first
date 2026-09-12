#!/usr/bin/env python3
"""Layered Smith-display eye for SAIR rank-2 Andrews--Curtis states.

This is a routing/visualization eye built on the exact `ac-r2-v1` move kernel
from `length_well_eye.py`. It is NOT an invariant, quotient, or reachability
proof. Exact move replay remains authoritative.

For each of the six natural inverse move-pairs we compute the two resulting
length changes, convert them to a bounded Smith/Cayley display coordinate, and
print the layers separately rather than collapsing them to one score.
"""
from __future__ import annotations

import argparse
import cmath
import math
from dataclasses import dataclass

from length_well_eye import AC00015, State, move, replay, total_length, AC00015_ESCAPE_PATH


PAIR_AXES = (
    ("mul-r0-by-r1", 2, 3),
    ("mul-r1-by-r0", 4, 5),
    ("conj-r0-x", 6, 7),
    ("conj-r0-y", 8, 9),
    ("conj-r1-x", 10, 11),
    ("conj-r1-y", 12, 13),
)


@dataclass(frozen=True)
class SmithLayer:
    name: str
    move_plus: int
    move_minus: int
    delta_plus: int
    delta_minus: int
    q: float
    p: float
    gamma: complex

    @property
    def radius(self) -> float:
        return abs(self.gamma)

    @property
    def angle(self) -> float:
        return cmath.phase(self.gamma)


def smith_layers(state: State, scale: float = 2.0) -> list[SmithLayer]:
    if scale <= 0:
        raise ValueError("scale must be positive")
    L0 = total_length(state)
    out: list[SmithLayer] = []
    for name, mp, mm in PAIR_AXES:
        dp = total_length(move(state, mp)) - L0
        dm = total_length(move(state, mm)) - L0
        q = (dp + dm) / (2.0 * scale)
        p = (dm - dp) / (2.0 * scale)
        Z = complex(math.exp(q), p)
        gamma = (Z - 1.0) / (Z + 1.0)
        # Re(Z)>0, so gamma must lie in the open unit disk up to roundoff.
        if abs(gamma) >= 1.0 + 1e-12:
            raise AssertionError("Smith map escaped unit disk")
        out.append(SmithLayer(name, mp, mm, dp, dm, q, p, gamma))
    return out


def inversion_flags(state: State) -> tuple[int, int]:
    """Length changes of inversion moves 0 and 1 (normally zero)."""
    L0 = total_length(state)
    return total_length(move(state, 0)) - L0, total_length(move(state, 1)) - L0


def print_layers(state: State, scale: float) -> None:
    print(f"total_length={total_length(state)} scale={scale}")
    inv0, inv1 = inversion_flags(state)
    print(f"inversion_delta=(r0:{inv0}, r1:{inv1})")
    print("layer move+ move- d+ d- q p radius angle_rad gamma")
    for x in smith_layers(state, scale):
        print(
            f"{x.name:14s} {x.move_plus:2d} {x.move_minus:2d} "
            f"{x.delta_plus:3d} {x.delta_minus:3d} "
            f"{x.q: .6f} {x.p: .6f} {x.radius: .6f} {x.angle: .6f} "
            f"({x.gamma.real: .6f},{x.gamma.imag: .6f})"
        )


def ac00015_demo(scale: float) -> None:
    print("== ac-00015 initial ==")
    print_layers(AC00015, scale)
    end, lengths = replay(AC00015, AC00015_ESCAPE_PATH)
    print("\n== ac-00015 first-well exit endpoint ==")
    print(f"escape_profile={lengths}")
    print_layers(end, scale)


def self_test() -> None:
    layers = smith_layers(AC00015)
    assert len(layers) == 6
    assert all(x.radius < 1.0 + 1e-12 for x in layers)
    # Inversion preserves freely reduced word length exactly.
    assert inversion_flags(AC00015) == (0, 0)
    # The known exact escape endpoint really is shorter than the start.
    end, _ = replay(AC00015, AC00015_ESCAPE_PATH)
    assert total_length(end) == 20
    assert total_length(AC00015) == 21
    print("smith_mixer_eye self-test: PASS")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--scale", type=float, default=2.0)
    ap.add_argument("--self-test", action="store_true")
    ap.add_argument("--ac00015-demo", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        self_test()
    if args.ac00015_demo or not args.self_test:
        ac00015_demo(args.scale)


if __name__ == "__main__":
    main()
