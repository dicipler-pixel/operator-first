#!/usr/bin/env python3
"""Construct ordinary AC certificates for the YXXyx Miller–Schupp chain.

The presentation at level n is

    (YXXyx, Y^(n+1) X y^n x),  with X=x^-1 and Y=y^-1.

For a=1,2,4,...,2^(n-1), the level block transforms

    (YXXyx, Y^k X y^(k-1) x^a)
      -> (YXXyx, Y^(k-1) X y^(k-2) x^(2a)).

The block is 10^(a-1), 5, (11,5)^(a-1), 12.  It rotates a-1
trailing x's to the front, crosses the yx boundary with the inverse
Baumslag–Solitar relator, then crosses the remaining x's as they rotate
back.  The last move removes one outer Y/y pair.  At the end the second
relator is Y x^(2^n-1).  The n-independent finish shape is derived from
an officially verified n=4 route.

This is a VALID generator, not a record-length one.  The block spends
3a-1 moves per level and the full route has 4*2^n+2-n moves.  A better
chain would avoid rotating a-1 x's to the front at each level.

Usage:
  python3 yxxyx_chain.py --sair-root SAIR-AC --n 5
  python3 yxxyx_chain.py --sair-root SAIR-AC --all
"""

import argparse
import json
import sys
from pathlib import Path

BS = [-2, -1, -1, 2, 1]
CHAR = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}


def word(w):
    return ''.join(CHAR[a] for a in w)


def initial(n):
    return (tuple(BS), tuple([-2] * (n + 1) + [-1] + [2] * n + [1]))


def generate(n, apply_move):
    if n < 2:
        raise ValueError('the finish block below requires n >= 2')
    state = initial(n)
    path = []
    checkpoints = []

    def push(block):
        nonlocal state
        for m in block:
            state = apply_move(state, m)
            path.append(m)

    for j in range(n):
        a = 1 << j
        k = n + 1 - j
        expected = (tuple(BS), tuple([-2] * k + [-1] + [2] * (k - 1) + [1] * a))
        assert state == expected, (n, j, state, expected)
        push([10] * (a - 1) + [5] + [11, 5] * (a - 1) + [12])
        checkpoints.append({'level': j + 1, 'moves_so_far': len(path),
                            'second_relator': word(state[1]) if n <= 5 else None})

    M = (1 << n) - 1
    assert state == (tuple(BS), tuple([-2] + [1] * M)), (n, state)
    push([6, 2, 10, 10, 5] + [3] * (M - 2) + [5, 11, 2])
    assert state == ((1,), (2,)), (n, state)
    assert len(path) == 4 * (1 << n) + 2 - n
    return path, checkpoints


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--sair-root', default='SAIR-AC')
    which = p.add_mutually_exclusive_group(required=True)
    which.add_argument('--n', type=int)
    which.add_argument('--all', action='store_true')
    p.add_argument('--json-out', type=Path)
    args = p.parse_args()
    root = Path(args.sair_root)
    sys.path.insert(0, str(root / 'competition' / 'tools'))
    from verifier.core import apply_move, verify

    manifest = json.loads((root / 'competition' / 'tools' / 'verifier' /
                            'data' / 'manifest.json').read_text())
    rows = {c['challenge_id']: c for c in manifest['challenges']}
    ns = range(2, 11) if args.all else (args.n,)
    output = {'source_commit': 'a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e',
              'formula': '4*2^n+2-n', 'rows': []}
    scored = {5: 'ac-01950', 6: 'ac-02033', 7: 'ac-06796',
              8: 'ac-03079', 9: 'ac-06727', 10: 'ac-00106'}
    for n in ns:
        path, checkpoints = generate(n, apply_move)
        if n in scored:
            challenge = rows[scored[n]]
            assert tuple(tuple(w) for w in challenge['initial_relators']) == initial(n)
        else:
            challenge = {'challenge_id': f'synthetic-ms-{n}',
                         'move_spec_version': 'ac-r2-v1',
                         'initial_relators': [list(w) for w in initial(n)],
                         'target_relators': [[1], [2]]}
        result = verify(challenge, path, 'ac-r2-v1', manifest['limits'])
        output['rows'].append({'n': n, 'challenge_id': challenge['challenge_id'],
                               'moves': path, 'checkpoints': checkpoints,
                               'verifier': result})
        if not result['ok']:
            raise RuntimeError(f'n={n}: {result}')
    if args.json_out:
        args.json_out.write_text(json.dumps(output, indent=2) + '\n')
    else:
        print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
