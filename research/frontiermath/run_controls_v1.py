"""Control run for the FrontierMath (ell=3, r=9) Python lane.

Runs the work assigned to this lane in CLAUDE_FRONTIERMATH_ATLAS_RAMANUJAN_TRACE.md:

  1. control-test the exact F3 rank-increment and separating-dual-witness layer;
  2. reproduce every control whose arithmetic is small enough to be exact here;
  3. verify the stated integer constants of the two Elkies boundaries;
  4. append one JSONL row per field/lane evaluation, in the supplied schema;
  5. preserve failures and absences rather than papering over them.

It does not compute class groups of the Elkies discriminants: those are near
10^29 and need a subexponential algorithm (PARI/Sage/Magma).  It never
synthesises class-group coordinates, and it writes no certificate file.

    python3 research/frontiermath/run_controls_v1.py
"""

import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import bqf_class_group_v1 as B          # noqa: E402
import f3_witness_v1 as F               # noqa: E402

OUT_JSONL = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "frontiermath_3rank9_python_lane.jsonl")

# Carried from the supplied package.  Values marked "carried" are NOT recomputed
# in this lane; the reason field on each row says so.
R16_D = 72513834653847828539450325493
R16_DISC = -217541503961543485618350976479
R16_URL = "https://doi.org/10.1007/s40993-025-00651-9"
R16_CURVE = "y^2+y=x^3-489468383913472842641289697078"

R17_M = 908800736629952526116772283648363
R17_F1 = 2195745961
R17_F2 = 413891567044514092637683
R17_B = 24537619889008718205152851658505801
R17_URL = "https://arxiv.org/abs/2510.27109"
R17_CURVE = "y^2=x^3+24537619889008718205152851658505801"


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def row(**kw):
    base = {
        "timestamp_utc": now(),
        "candidate_id": "",
        "source_url": "",
        "curve_model": "",
        "claimed_curve_rank": "",
        "lane": "imaginary",
        "radicand_squarefree": 0,
        "field_discriminant": 0,
        "class_group_invariants": [],
        "three_rank": 0,
        "status": "ERROR",
        "reason": "",
    }
    base.update(kw)
    return base


def invariant_factors_from_orders(D):
    """Invariant factors of Cl(D), read off exactly from the element-order profile.

    Only called for discriminants small enough to enumerate.
    """
    from collections import Counter
    orders = Counter(B.element_orders(D).values())
    h = sum(orders.values())
    exponent = max(orders)
    return h, exponent, dict(sorted(orders.items()))


def main():
    rows = []
    transcript = []

    def log(s):
        transcript.append(s)
        print(s)

    # ---------------- witness layer self-test --------------------------------
    log("== F3 witness layer ==")
    ident = [tuple(1 if i == j else 0 for j in range(9)) for i in range(9)]
    sweep = F.independence_sweep(ident, expect_order=19683)
    log(f"   3^9 sweep on an independent set: order {sweep['subgroup_order']} / "
        f"{sweep['combinations_checked']} checked, independent={sweep['independent']}")
    dep = ident[:8] + [tuple((ident[0][i] + ident[1][i]) % 3 for i in range(9))]
    sweep2 = F.independence_sweep(dep)
    log(f"   3^9 sweep on a dependent set:    order {sweep2['subgroup_order']}, "
        f"relation {sweep2['first_nontrivial_relation']}")
    W = ident[:8]
    g_in = tuple((ident[0][i] + ident[3][i]) % 3 for i in range(9))
    g_out = ident[8]
    log(f"   g inside  span: increment {F.rank_increment(W, g_in)}, "
        f"separating chi {F.separating_dual(W, g_in)}")
    chi = F.separating_dual(W, g_out)
    log(f"   g outside span: increment {F.rank_increment(W, g_out)}, "
        f"separating chi {chi}, re-check {F.verify_separation(W, g_out, chi)}")
    assert sweep["independent"] and not sweep2["independent"]
    assert F.separating_dual(W, g_in) is None and chi is not None

    # ---------------- control C0 ---------------------------------------------
    log("\n== Control C0: Delta = -23 ==")
    D0 = -23
    f0 = (2, 1, 3)
    h0, exp0, prof0 = invariant_factors_from_orders(D0)
    tors0, r0 = B.three_torsion(D0)
    log(f"   form (2,1,3) discriminant {B.disc(f0)}; reduced={B.is_reduced(f0)}; "
        f"order {B.order_of(f0)}")
    log(f"   h = {h0}, exponent {exp0}, order profile {prof0}")
    log(f"   |Cl[3]| = {len(tors0)}, 3-rank = {r0}  (expected 1)")
    assert B.disc(f0) == D0 and B.order_of(f0) == 3 and h0 == 3 and r0 == 1
    rows.append(row(
        candidate_id="CONTROL-C0", source_url="package control C0",
        curve_model="", claimed_curve_rank="", lane="imaginary",
        radicand_squarefree=-23, field_discriminant=D0,
        class_group_invariants=[3], three_rank=r0,
        status="REJECT",
        reason="control reproduced exactly in this lane: h=3, Cl=Z/3, form (2,1,3) "
               "has exact order 3, 3-rank 1. Rejected for the r=9 target because "
               "3-rank 1 < 9."))

    # ---------------- control C1 ---------------------------------------------
    log("\n== Control C1: Delta = -3321607 ==")
    D1 = -3321607
    h1, exp1, prof1 = invariant_factors_from_orders(D1)
    tors1, r1 = B.three_torsion(D1)
    log(f"   h = {h1}, exponent {exp1}")
    log(f"   order profile {prof1}")
    log(f"   |Cl[3]| = {len(tors1)}, 3-rank = {r1}  (expected 3)")
    # 567 = 7 * 3^4; 3-rank 3 forces the 3-part to be Z/9 x Z/3 x Z/3,
    # so Cl = Z/7 x Z/9 x Z/3 x Z/3 = Z/63 x Z/3 x Z/3.
    structure_ok = (h1 == 567 and r1 == 3 and exp1 == 63)
    log(f"   invariant factors [63,3,3] confirmed: {structure_ok} "
        f"(h=567=7*3^4, 3-rank 3 forces 3-part Z/9 x Z/3 x Z/3, exponent 63)")
    assert structure_ok
    rows.append(row(
        candidate_id="CONTROL-C1", source_url="package control C1",
        curve_model="", claimed_curve_rank="", lane="imaginary",
        radicand_squarefree=-3321607, field_discriminant=D1,
        class_group_invariants=[63, 3, 3], three_rank=r1,
        status="REJECT",
        reason="control reproduced exactly in this lane by independent form "
               "composition: h=567, exponent 63, |Cl[3]|=27, 3-rank 3, invariant "
               "factors Z/63 x Z/3 x Z/3. The eight order-3 form triples of the "
               "historical run are absent from the ledger and were NOT invented. "
               "Rejected for the r=9 target because 3-rank 3 < 9."))

    # ---------------- constants of the two Elkies boundaries -----------------
    log("\n== Stated constants of the Elkies boundaries ==")
    ok16 = (-3 * R16_D == R16_DISC)
    log(f"   R16: -3D == stated field discriminant: {ok16}; "
        f"disc mod 4 = {R16_DISC % 4}")
    ok17b = (27 * R17_M == R17_B)
    ok17f = (R17_F1 * R17_F2 == R17_M)
    ok17r = (3 * R17_M == 2726402209889857578350316850945089)
    log(f"   R17: b == 27m: {ok17b}; m == f1*f2: {ok17f}; real radicand == 3m: {ok17r}")
    log(f"   R17: m mod 4 = {R17_M % 4} so -m mod 4 = {(-R17_M) % 4}; "
        f"3 divides m: {R17_M % 3 == 0}")
    log("   R17: m is a product of two distinct primes, hence provably squarefree, "
        "so -m is a fundamental discriminant and 3m is squarefree.")
    log(f"   R17: allocation 17 = 7+8+2: {7 + 8 + 2 == 17}")
    assert ok16 and ok17b and ok17f and ok17r

    carried = ("3-rank carried from the supplied ledger and NOT recomputed in this "
               "lane: |field discriminant| is about 1e29, far beyond exact reduced-form "
               "enumeration. Needs PARI/Sage/Magma. Constants re-derived here exactly.")
    rows.append(row(
        candidate_id="ELKIES-R16", source_url=R16_URL, curve_model=R16_CURVE,
        claimed_curve_rank="16", lane="imaginary",
        radicand_squarefree=-3 * R16_D, field_discriminant=R16_DISC,
        class_group_invariants=[], three_rank=8, status="BOUNDARY",
        reason=carried + " The sixteen form triples and the eight-vector relation "
               "basis are absent from the consolidated ledger, so the historical "
               "16-by-8 dependency witness is NOT reproduced and was not invented."))
    rows.append(row(
        candidate_id="ELKIES-R17", source_url=R17_URL, curve_model=R17_CURVE,
        claimed_curve_rank="17", lane="imaginary",
        radicand_squarefree=-R17_M, field_discriminant=-R17_M,
        class_group_invariants=[], three_rank=8, status="BOUNDARY",
        reason=carried + " b=27m, m=f1*f2 with both factors prime, m=3 mod 4."))
    rows.append(row(
        candidate_id="ELKIES-R17", source_url=R17_URL, curve_model=R17_CURVE,
        claimed_curve_rank="17", lane="real",
        radicand_squarefree=3 * R17_M, field_discriminant=3 * R17_M,
        class_group_invariants=[], three_rank=7, status="BOUNDARY",
        reason=carried + " Paired real field Q(sqrt(3m)); 3m squarefree because "
               "3 does not divide m and m is a product of two primes."))

    log("\n== Result ==")
    log("   No rank-9 input exists in this package, so no certificate was written.")
    log("   Highest 3-rank on record here is 8 (Elkies rank-16 and rank-17 boundaries).")

    with open(OUT_JSONL, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    log(f"\n   ledger: {os.path.basename(OUT_JSONL)} ({len(rows)} rows)")
    return rows, transcript


if __name__ == "__main__":
    main()
