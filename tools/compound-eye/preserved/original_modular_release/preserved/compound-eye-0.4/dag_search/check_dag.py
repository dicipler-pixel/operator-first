#!/usr/bin/env python3
"""Independent DAG certificate checker: Python standard library only.

Reconstructs public tower relations by scanning vertices. Uses Fraction-based
Gauss-Jordan elimination, independently of the producer's integer elimination.
Checks every branch, merge, obstruction, context and complete terminal.
"""
from fractions import Fraction
from itertools import product
from math import comb, gcd, lcm, prod
from functools import reduce
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time

from check_ak_certificate import check as check_primal


def need(condition, message):
    if not condition:
        raise ValueError(message)


def digest(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def rref(rows):
    A = [list(map(Fraction, r)) for r in rows if any(r)]
    if not A:
        return ()
    k = 0
    for j in range(len(A[0])):
        p = next((i for i in range(k, len(A)) if A[i][j]), None)
        if p is None:
            continue
        A[k], A[p] = A[p], A[k]
        d = A[k][j]
        A[k] = [x/d for x in A[k]]
        for i in range(len(A)):
            if i != k and A[i][j]:
                d = A[i][j]
                A[i] = [x-d*y for x, y in zip(A[i], A[k])]
        k += 1
        if k == len(A):
            break
    return tuple(tuple(r) for r in A[:k])


def primitive(row):
    d = lcm(*(x.denominator for x in row)) if row else 1
    out = [int(x*d) for x in row]
    g = reduce(gcd, out, 0)
    if not g:
        return tuple(out)
    if next(x for x in out if x) < 0:
        g = -abs(g)
    return tuple(x//g for x in out)


def canonical(rows):
    return tuple(primitive(row) for row in rref(rows))


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def reconstruct(problem, pool):
    p = problem
    need(p.get('schema') == 'arithmetic-kakeya-tower-v1', 'Wrong problem schema.')
    d = p['dims']
    need(isinstance(d, list) and d and all(type(a) is int and a > 0 for a in d), 'Bad dimensions.')
    n = prod(d)
    need(n <= 128, 'Vertex limit exceeded.')
    X = p['X']
    need(all(isinstance(x, list) and len(x) == 2 and all(type(a) is int for a in x)
             and (x == [0, 0] or sum(x) != 0) for x in X), 'Invalid X.')
    Xset = {tuple(x) for x in X}
    need(len(Xset) == len(X) and (0, 0) in Xset, 'Duplicate labels or missing zero.')
    V = list(product(*(range(1, a+1) for a in d)))
    ids = {v: i for i, v in enumerate(V)}
    T = p['initial_known']
    need(all(isinstance(v, list) and all(type(a) is int for a in v) and tuple(v) in ids for v in T), 'Invalid T.')
    initial = {ids[tuple(v)] for v in T}
    need(len(initial) == len(T) and len(T) < n, 'Duplicate or full T.')
    need(p['generators'] == [], 'Base generators must be empty.')
    need(len(p['levels']) == len(d), 'Wrong level count.')
    edges = []
    for level, entries in enumerate(p['levels']):
        seen = set()
        for entry in entries:
            key, x = entry['prefix'], entry['label']
            need(isinstance(key, list) and len(key) == level+1 and all(type(a) is int for a in key), 'Bad prefix.')
            need(all(1 <= key[j] <= d[j] for j in range(level)) and 1 <= key[-1] < d[level], 'Prefix range.')
            need(tuple(key) not in seen, 'Duplicate prefix.')
            seen.add(tuple(key))
            need(isinstance(x, list) and len(x) == 2 and all(type(a) is int for a in x) and tuple(x) in Xset, 'Bad edge label.')
            if x == [0, 0]:
                continue
            for v in V:
                if list(v[:level+1]) != key:
                    continue
                w = list(v)
                w[level] += 1
                row = [0]*(2*n)
                a, b = ids[v], ids[tuple(w)]
                row[2*a:2*a+2] = x
                row[2*b:2*b+2] = [-z for z in x]
                edges.append(row)
    need(isinstance(pool, list) and pool and all(isinstance(x, list) and len(x) == 2
         and all(type(a) is int for a in x) and tuple(x) in Xset and x != [0, 0] for x in pool), 'Bad pool.')
    need(len({tuple(x) for x in pool}) == len(pool), 'Duplicate pool option.')
    options = []
    for v in range(n):
        for label in pool:
            row = [0]*(2*n)
            row[2*v:2*v+2] = label
            options.append(row)
    identity = {'rule': 'epoch-public-nonzero-multiple-forcing-v1',
                'base_problem': {k: p[k] for k in ('schema', 'dims', 'X', 'levels', 'initial_known')},
                'ordered_vertices': [list(v) for v in V], 'ordered_pool': pool,
                'target': [1, -1], 'arithmetic': 'rational-span-with-integer-certificates'}
    return V, initial, edges, options, identity


def check(artifact):
    started = time.perf_counter()
    a = artifact
    need(a.get('schema') == 'compound-eye-decision-dag-v1', 'Wrong DAG schema.')
    V, initial, edges, options, identity = reconstruct(a['problem'], a['pool'])
    n, N = len(V), len(options)
    need(a['context'] == identity and a['context_sha256'] == digest(identity), 'Forged or stale context.')
    E = rref(edges)
    pivots = [next(j for j, x in enumerate(row) if x) for row in E]
    free = [j for j in range(2*n) if j not in pivots]
    need(a['free_coordinates'] == free, 'Wrong quotient coordinates.')
    projections = []
    for row in options:
        v = list(map(Fraction, row))
        for p, basisrow in zip(pivots, E):
            d = v[p]
            v = [x-d*y for x, y in zip(v, basisrow)]
        projections.append(primitive([v[j] for j in free]))
    def lift(row):
        out = [0]*(2*n)
        for j, x in zip(free, row):
            out[j] = x
        return out
    masks = []
    vectors = []
    for record in a['obstructions']:
        need(record['schema'] == 'compound-eye-ak-obstruction-v2' and record['context_sha256'] == a['context_sha256'], 'Wrong obstruction context.')
        need(record['record_sha256'] == digest({k: v for k, v in record.items() if k != 'record_sha256'}), 'Obstruction hash mismatch.')
        Klist = record['known_container']
        need(all(type(v) is int and 0 <= v < n for v in Klist), 'Bad known container.')
        K = set(Klist)
        need(len(K) == len(Klist) and initial <= K and len(K) < n, 'Container misses T or is not proper.')
        fs = record['functionals']
        need(len(fs) == n-len(K) and {f['vertex'] for f in fs} == set(range(n))-K, 'Missing functional.')
        for f in fs:
            e, z = f['vertex'], f['vector']
            need(type(e) is int and len(z) == 2*n and all(type(x) is int for x in z), 'Malformed functional.')
            need(all(z[2*v] == z[2*v+1] == 0 for v in K), 'Functional has support on K.')
            need(z[2*e] != z[2*e+1], 'Functional fails to separate target.')
            need(all(dot(z, row) == 0 for row in edges), 'Functional violates edge annihilation.')
        zs = [f['vector'] for f in fs]
        mask = sum(1 << j for j, row in enumerate(options) if all(dot(z, row) == 0 for z in zs))
        need(record['inside_options_mask'] == mask, 'Incorrect family mask.')
        masks.append(mask)
        vectors.append(zs)
    budget = a['budget']
    need(type(budget) is int and 0 <= budget <= N, 'Invalid budget.')
    nodes = a['nodes']
    root = a['root']
    need(type(root) is int and 0 <= root < len(nodes), 'Invalid root.')
    states = []
    seen_keys = set()
    for node in nodes:
        pos, left = node['pos'], node['left']
        need(type(pos) is int and type(left) is int and 0 <= pos <= N and 0 <= left <= min(budget, N-pos), 'Node range.')
        need(left != 0 or pos == N, 'Noncanonical terminal position.')
        state = tuple(tuple(row) for row in node['state'])
        need(all(len(row) == len(free) and all(type(x) is int for x in row) for row in state), 'Invalid state coefficients.')
        key = pos, left, state
        need(key not in seen_keys, 'Unmerged duplicate decision state.')
        seen_keys.add(key)
        states.append(state)
    need(states[root] == () and nodes[root]['left'] == budget and nodes[root]['pos'] == (0 if budget else N), 'Wrong root state.')
    transition_cache = {}
    reached = set()
    totals = {}
    complete_nodes = 0
    def visit(i):
        nonlocal complete_nodes
        if i in totals:
            return totals[i]
        reached.add(i)
        node = nodes[i]
        pos, left, state = node['pos'], node['left'], states[i]
        count = comb(N-pos, left)
        if node['kind'] == 'excluded':
            b = node['obstruction']
            need(type(b) is int and 0 <= b < len(masks), 'Unknown obstruction.')
            need(all(dot(z, lift(row)) == 0 for z in vectors[b] for row in state), 'Obstruction does not cover node state.')
            if left:
                suffix = ((1 << N)-1) ^ ((1 << pos)-1)
                need(suffix & ~masks[b] == 0, 'Obstruction misses a future extension.')
            answer = count, 0
        elif node['kind'] == 'complete':
            need(left == 0, 'Premature positive terminal.')
            cert = node.get('positive_certificate')
            need(cert is not None, 'Positive terminal lacks integer certificate.')
            result = check_primal(cert)
            need(result['forcing_complete'], 'Positive certificate is incomplete.')
            p = cert['problem']
            for key in ('schema', 'dims', 'X', 'levels', 'initial_known'):
                need(p[key] == a['problem'][key], 'Positive certificate context changed.')
            indices = node['representative']
            need(len(indices) == budget and len(set(indices)) == budget and all(type(j) is int and 0 <= j < N for j in indices), 'Bad positive representative.')
            expected = [{'vertex': list(V[j//len(a['pool'])]), 'label': a['pool'][j%len(a['pool'])]} for j in indices]
            need(p['generators'] == expected and canonical([projections[j] for j in indices]) == state, 'Positive representative does not match state.')
            answer = 1, 1
            complete_nodes += 1
        else:
            need(node['kind'] == 'decision' and left > 0, 'Invalid decision node.')
            branch_totals = []
            for take, field in ((True, 'include'), (False, 'exclude')):
                j = node[field]
                nextleft = left-int(take)
                impossible = nextleft > N-pos-1
                if impossible:
                    need(j == -1, 'Impossible branch should be absent.')
                    branch_totals.append((0, 0))
                    continue
                need(type(j) is int and 0 <= j < len(nodes), 'Missing feasible branch.')
                child = nodes[j]
                expectedpos = N if nextleft == 0 else pos+1
                need(child['pos'] == expectedpos and child['left'] == nextleft, 'Branch chronology or cost changed.')
                expectedstate = state
                if take:
                    tkey = state, pos
                    if tkey not in transition_cache:
                        transition_cache[tkey] = canonical(list(state)+[projections[pos]])
                    expectedstate = transition_cache[tkey]
                need(states[j] == expectedstate, 'Unsound state merge or transition.')
                branch_totals.append(visit(j))
            answer = tuple(sum(v[k] for v in branch_totals) for k in (0, 1))
            need(answer[0] == count, 'Branch coverage count mismatch.')
        totals[i] = answer
        return answer
    coverage, complete = visit(root)
    need(len(reached) == len(nodes), 'Unreachable certificate nodes.')
    need(coverage == comb(N, budget), 'Incomplete root coverage.')
    need(a['statistics']['configurations'] == coverage and a['statistics']['complete_configurations'] == complete, 'Reported totals disagree.')
    return {'all_passed': True, 'context_sha256': a['context_sha256'],
            'nodes_checked': len(nodes), 'obstructions_checked': len(masks),
            'rational_transitions_checked': len(transition_cache),
            'configurations_certified': coverage, 'complete_configurations': complete,
            'positive_certificates_checked': complete_nodes,
            'seconds': time.perf_counter()-started,
            'arithmetic': 'standard-library integers and independent Fraction Gauss-Jordan',
            'official_epoch_verifier_run': False, 'lean_formalized': False}


if __name__ == '__main__':
    path = Path(sys.argv[1])
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'rt') as f:
        data = json.load(f)
    try:
        print(json.dumps(check(data), indent=2))
    except (ValueError, KeyError, IndexError, TypeError) as error:
        print(json.dumps({'all_passed': False, 'error': str(error)}))
        sys.exit(2)
