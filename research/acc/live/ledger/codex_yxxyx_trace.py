#!/usr/bin/env python3
"""Replay the YXXyx Miller–Schupp chain with the pinned SAIR AC kernel.

This probes uniform prefixes and verifies the two concrete n=3,4 paths.
It does not claim that the prefixes extend to a full family certificate.
Run with a checkout of SAIRcompetition/Andrews-Curtis at a0fd6e6f52d8:

  python3 codex_yxxyx_trace.py --sair-root SAIR-AC
"""

import argparse
import json
import sys
from pathlib import Path


# x=1, X=-1, y=2, Y=-2.  The first relator is BS(1,2).
BS = [-2, -1, -1, 2, 1]
NINE = [5, 1, 12, 4, 1, 10, 5, 12, 10]
# A different 18-move prefix found by beam. Its first seven moves already
# reduce the y-level by one, and all 18 reduce it by two.
EIGHTEEN = [5, 7, 12, 5, 6, 5, 12, 1, 4, 10, 4, 10, 4, 10, 1, 5, 12, 10]
N3 = [0, 4, 12, 2, 5, 6, 3, 8, 6, 3, 7, 3, 7, 3, 7, 3, 8, 10, 4,
      1, 11, 2, 4, 4, 4, 4, 4, 4, 8]
N4 = EIGHTEEN + [5, 11, 5, 11, 5, 11, 5, 11, 5, 11, 5, 11, 5, 11,
                  5, 12, 6, 2, 10, 10, 5] + [3] * 13 + [5, 11, 2]


def start(n):
    return (tuple(BS), tuple([-2] * (n + 1) + [-1] + [2] * n + [1]))


def replay(apply_move, state, moves):
    for m in moves:
        state = apply_move(state, m)
    return state


def letters(word):
    return ''.join({1: 'x', -1: 'X', 2: 'y', -2: 'Y'}[x] for x in word)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--sair-root', default='SAIR-AC')
    p.add_argument('--json-out', type=Path)
    args = p.parse_args()
    sys.path.insert(0, str(Path(args.sair_root) / 'competition' / 'tools'))
    from verifier.core import apply_move, free_reduce, verify

    manifest = json.loads((Path(args.sair_root) / 'competition' / 'tools' /
                            'verifier' / 'data' / 'manifest.json').read_text())
    out = {'source_commit': 'a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e',
           'prefixes': [], 'certificates': []}
    for n in range(3, 11):
        a = replay(apply_move, start(n), NINE)
        b = replay(apply_move, start(n), EIGHTEEN)
        expected_a = tuple([1] * 3 + [-2] * (n - 1) + [-1] + [2] * (n - 2) + [1])
        expected_b = free_reduce([1] * 7 + [-2] * (n - 2) + [-1] + [2] * (n - 3) + [1])
        assert a == (tuple(BS), expected_a), (n, a)
        assert b == (tuple(BS), expected_b), (n, b)
        out['prefixes'].append({'n': n, 'nine': letters(a[1]),
                                'eighteen': letters(b[1])})

    for n, path in ((3, N3), (4, N4)):
        challenge = {'challenge_id': f'synthetic-ms-{n}',
                     'move_spec_version': 'ac-r2-v1',
                     'initial_relators': [list(w) for w in start(n)],
                     'target_relators': [[1], [2]]}
        result = verify(challenge, path, 'ac-r2-v1', manifest['limits'])
        assert result['ok'], (n, result)
        out['certificates'].append({'n': n, 'moves': path, 'verifier': result})
    if args.json_out:
        args.json_out.write_text(json.dumps(out, indent=2) + '\n')
    else:
        print(json.dumps(out, indent=2))


if __name__ == '__main__':
    main()
