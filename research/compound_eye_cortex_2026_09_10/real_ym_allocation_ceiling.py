#!/usr/bin/env python3
"""Exact Cortex stress test for the two-cube lambda/alpha=1 bottleneck.

Input is the exact double-cube matrix JSON produced by Yang-Mills native run
34412059750. This script does not rebuild Haar integrals. It verifies the pinned
canonical matrix digest, an exact six-character one-plaquette variational trial,
the common-s single-plaquette allocation ceiling, and exact rational LDL inertia
of the 95-state retained compression at the ceiling and a rational bracket.

The conclusion is deliberately narrow: it rules out the present retained-space
variational route inside the stated allocation family. It does not prove
Gaplessness or rule out a better full-space trial, cluster floor, nonuniform
retained electric weights, different compression, or another hidden-sector
inequality.
"""
from __future__ import annotations
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path
import argparse, hashlib, json

EXPECTED_MATRIX_DIGEST = 'f907870d090be604baf4ba5e8ae1da0e89f4dbee6a088d325e4d177b1bdd575d'
TAIL = F(28, 3)
R = F(16022321, 500000)
TRIAL = (13, 6, 6, 1, 2, 1)


def canonical(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(x):
    return hashlib.sha256(canonical(x).encode()).hexdigest()


def states(n):
    return [(p, s-p) for s in range(n+1) for p in range(s+1)]


def neighbors(p, q):
    return [(a, b) for a, b in ((p+1,q),(p-1,q+1),(p,q-1),
             (p,q+1),(p+1,q-1),(p-1,q)) if min(a,b) >= 0]


def casimir(p, q):
    return F(p*p + q*q + p*q + 3*p + 3*q, 3)


def exact_inertia(a):
    """Exact no-pivot LDL congruence; zero pivots are refused."""
    if not a or any(len(row) != len(a) for row in a):
        raise ValueError('Expected square matrix')
    if any(a[i][j] != a[j][i] for i in range(len(a)) for j in range(i)):
        raise ValueError('Expected symmetric matrix')
    m = [row[:] for row in a]
    pivots = []
    negative = 0
    for k in range(len(m)):
        pivot = m[k][k]
        if pivot == 0:
            raise ArithmeticError('Zero LDL pivot at ' + str(k))
        pivots.append(pivot)
        negative += int(pivot < 0)
        for i in range(k+1, len(m)):
            if m[k][i] == 0:
                continue
            aik = m[k][i]
            for j in range(i, len(m)):
                if m[k][j]:
                    m[i][j] -= aik*m[k][j]/pivot
                    m[j][i] = m[i][j]
    return negative, pivots


def shifted(a, x):
    return [[v - (x if i == j else F(0)) for j, v in enumerate(row)]
            for i, row in enumerate(a)]


def trial_coefficients():
    ss = states(2)
    index = {s:i for i,s in enumerate(ss)}
    norm = sum(F(x*x) for x in TRIAL)
    cform = sum(F(TRIAL[i]*TRIAL[i])*casimir(*s)
                for i,s in enumerate(ss))
    edges = []
    for i,s in enumerate(ss):
        for target in neighbors(*s):
            j = index.get(target)
            if j is not None and i < j:
                edges.append((i,j))
    # V = 3 I - (chi_10 + chi_01)/2.  In the character basis the internal
    # undirected neighbor entries are -1/2, hence each pair contributes -vi*vj.
    vform = 3*norm - sum(F(TRIAL[i]*TRIAL[j]) for i,j in edges)
    if norm != 247 or cform != F(344,3) or vform != 509:
        raise AssertionError('One-plaquette trial arithmetic changed')
    return norm, cform/norm, vform/norm, edges


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--matrix-json', type=Path, required=True)
    parser.add_argument('--out', type=Path,
                        default=Path('real_ym_allocation_ceiling.json'))
    args = parser.parse_args()

    raw = json.loads(args.matrix_json.read_text())
    pinned = deepcopy(raw)
    pinned.pop('seconds', None)
    matrix_digest = digest(pinned)
    if matrix_digest != EXPECTED_MATRIX_DIGEST:
        raise AssertionError('Double-cube matrix canonical digest changed: ' + matrix_digest)

    model = raw['model']
    n = len(model['energies'])
    if (model['name'] != 'double_cube' or len(model['edges']) != 20 or
        len(model['faces']) != 11 or n != 95 or F(model['tail']) != TAIL):
        raise AssertionError('Pinned double-cube model contract changed')

    gram = [[F(x) for x in row] for row in raw['matrices']['gram']]
    if any(gram[i][j] != F(int(i == j)) for i in range(n) for j in range(n)):
        raise AssertionError('Expected orthonormal retained Gram')

    S = [[F(x) for x in row] for row in raw['matrices']['S']]
    energies = list(map(F, model['energies']))
    # spatial_certificates.retained at alpha=lambda=1:
    # A_ij = delta_ij(E_i + 3 * number_of_plaquettes) - S_ij.
    A = [[(energies[i] + 3*len(model['faces']) if i == j else F(0)) - S[i][j]
          for j in range(n)] for i in range(n)]

    norm, qa, qb, trial_edges = trial_coefficients()
    # Let E(kappa) be the exact one-plaquette ground energy of kappa*C+V.
    # Variational principle gives E(kappa) <= qa*kappa+qb. The written report
    # supplies the concavity/monotonicity and incidence-budget steps.
    ceiling_constant = 20*qa + 11*qb
    ceiling_slope = TAIL - 20*qa
    if ceiling_constant != F(23677,741) or ceiling_slope != F(12,247):
        raise AssertionError('Allocation ceiling simplification changed')
    ceiling_at_one = ceiling_constant + ceiling_slope
    if ceiling_at_one != F(23713,741):
        raise AssertionError('Ceiling endpoint changed')

    negative_at_ceiling, pivots_at_ceiling = exact_inertia(shifted(A, ceiling_at_one))
    negative_at_r, pivots_at_r = exact_inertia(shifted(A, R))
    if negative_at_ceiling != 0 or negative_at_r != 1:
        raise AssertionError('Compression-ground bracket failed')

    margin = R - ceiling_at_one
    if margin != F(16039861,370500000) or margin <= 0:
        raise AssertionError('Expected positive structural margin')

    out = {
      'schema':'compound-eye-cortex-real-ym-test/1',
      'status':'PASS',
      'matrix_record_without_timing_sha256':matrix_digest,
      'model':{
        'name':'double_cube','links':20,'plaquettes':11,
        'retained_dimension':95,'tail':str(TAIL),'lambda_over_alpha':'1'
      },
      'one_plaquette_trial':{
        'state_order':states(2),'vector':list(TRIAL),'norm_squared':str(norm),
        'C_rayleigh_coefficient':str(qa),'V_rayleigh_intercept':str(qb),
        'internal_potential_edges':trial_edges,
        'variational_upper':'E(kappa) <= (344/741) kappa + 509/247'
      },
      'allocation_ceiling':{
        'scope':'common retained coefficient beta_e=s; arbitrary positive incidence allocations satisfying beta_e+sum_p a_pe<=1; sum of 11 single-plaquette absolute ground floors; total-electric C<=8 hidden floor',
        'formula':'d <= 23677/741 + (12/247) s',
        's_range':'0<=s<=1 (s=1 handled as bare endpoint)',
        'global_upper':str(ceiling_at_one),
        'global_upper_display':float(ceiling_at_one)
      },
      'retained_compression_exact_inertia':{
        'negative_directions_at_ceiling':negative_at_ceiling,
        'negative_directions_at_r':negative_at_r,
        'r':str(R),'r_display':float(R),
        'ceiling_to_r_margin':str(margin),
        'ceiling_to_r_margin_display':float(margin),
        'pivots_at_ceiling':len(pivots_at_ceiling),
        'pivots_at_r':len(pivots_at_r),
        'conclusion':'The lowest eigenvalue of the 95-state retained compression lies strictly above the allocation ceiling and strictly below r.'
      },
      'licensed_diagnosis':'Within this common-s/single-plaquette-floor family, no ground-energy upper bound obtained from a trial vector restricted to the current 95-state retained compression can satisfy r<d at lambda/alpha=1.',
      'not_ruled_out':[
        'a lower full-space trial upper bound not restricted to the 95-state compression',
        'cluster or overlapping-cell lower floors',
        'nonuniform retained beta_e with a weighted hidden-sector bound',
        'a different/larger retained compression with its tail recomputed',
        'another rigorous hidden-sector inequality'
      ],
      'not_claimed':['gaplessness','failure of every allocation architecture',
                     'volume-uniform gap','continuum Yang-Mills mass gap'],
      'checks':{
        'exact_ldl_pivots':len(pivots_at_ceiling)+len(pivots_at_r),
        'one_plaquette_trial_edges':len(trial_edges)
      }
    }
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(out,indent=2)+'\n')
    print('PASS')
    print('ceiling', float(ceiling_at_one), 'r', float(R),
          'margin', float(margin), 'inertia', negative_at_ceiling, negative_at_r)


if __name__ == '__main__':
    main()
