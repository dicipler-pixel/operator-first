#!/usr/bin/env python3
"""New Earth-Moon host extensions, reusable colorings, and a decision DAG.

The DAG shares the state of the certificate tests, not full graph isomorphism.
Standard library only. No failed coloring search is treated as a lower bound.
"""
from itertools import combinations
from math import comb
from pathlib import Path
import gzip
import hashlib
import json
import sys
import time

ROOT = Path(__file__).resolve().parent


def proper(edges, colors, n=28):
    return len(colors) == n and all(type(c) is int and 0 <= c < 9 for c in colors) and all(colors[a] != colors[b] for a, b in edges)


def triangle_free(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    return all(not (adj[a] & adj[b]) for a, b in edges)


def coloring9(n, edges, limit=200000):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    colors = [-1]*n
    calls = 0
    def dfs(used, remaining):
        nonlocal calls
        calls += 1
        if calls > limit:
            return False
        if not remaining:
            return True
        v = max(remaining, key=lambda a: (len({colors[b] for b in adj[a] if colors[b] >= 0}), len(adj[a]), -a))
        banned = {colors[b] for b in adj[v] if colors[b] >= 0}
        for c in range(min(used+1, 9)):
            if c in banned:
                continue
            colors[v] = c
            if dfs(max(used, c+1), remaining-{v}):
                return True
            colors[v] = -1
        return False
    success = dfs(0, set(range(n)))
    return colors if success else None, calls


def run():
    start = time.perf_counter()
    old = json.loads((ROOT/'evidence/earth_moon_c7k4.json').read_text())
    G = {tuple(e) for e in old['candidate']['edges']}
    J = {tuple(e) for e in old['candidate']['triangle_free_subgraph']}
    removed = {(a, b) for a in range(4) for b in (24, 25)}
    assert removed <= J and len(removed) == 8
    base = G-removed
    options = [e for e in combinations(range(28), 2) if e not in G]
    certificates = []
    for item in old['join_deletion_nine_colorings']:
        c = item['nine_coloring']
        missing = tuple(item['deleted_join_edge'])
        assert proper(G-{missing}, c)
        if proper(base, c):
            certificates.append(c)
    inherited = len(certificates)
    density = {}
    for i, e in enumerate(options):
        H = (J-removed) | {e}
        if len(H) > 4*28-8 and triangle_free(28, H):
            density[i] = [list(x) for x in sorted(H)]
    initial_density_count = initial_coloring_count = 0
    for pair in combinations(range(len(options)), 2):
        if any(j in density for j in pair):
            initial_density_count += 1
        elif any(all(c[options[j][0]] != c[options[j][1]] for j in pair) for c in certificates):
            initial_coloring_count += 1
    calls = solver_nodes = 0
    unresolved = []
    for pair in combinations(range(len(options)), 2):
        if any(j in density for j in pair):
            continue
        if any(all(c[options[j][0]] != c[options[j][1]] for j in pair) for c in certificates):
            continue
        colors, nodes = coloring9(28, base | {options[j] for j in pair})
        calls += 1
        solver_nodes += nodes
        if colors is None:
            unresolved.append(list(pair))
        else:
            assert proper(base | {options[j] for j in pair}, colors)
            certificates.append(colors)
    N = len(options)
    compat = [sum(1 << i for i, c in enumerate(certificates) if c[a] != c[b]) for a, b in options]
    full = (1 << len(certificates))-1
    nodes, memo = [], {}
    merges = 0
    def visit(pos, left, available):
        nonlocal merges
        if left > N-pos:
            return -1
        if not left:
            pos = N
        key = pos, left, available
        if key in memo:
            merges += 1
            return memo[key]
        i = len(nodes)
        memo[key] = i
        node = {'pos': pos, 'left': left, 'available_colorings': available}
        nodes.append(node)
        if not left:
            if available:
                node.update(kind='coloring', certificate=(available & -available).bit_length()-1)
            else:
                node['kind'] = 'unresolved'
            return i
        if pos in density:
            yes = len(nodes)
            nodes.append({'kind': 'density', 'pos': pos+1, 'left': left-1, 'option': pos})
        else:
            yes = visit(pos+1, left-1, available & compat[pos])
        no = visit(pos+1, left, available)
        node.update(kind='decision', include=yes, exclude=no)
        return i
    root = visit(0, 2, full)
    a = {'schema': 'compound-eye-earth-family-dag-v1', 'num_vertices': 28,
         'original_host': [list(e) for e in sorted(G)], 'removed_joins': [list(e) for e in sorted(removed)],
         'base_edges': [list(e) for e in sorted(base)], 'optional_edges': [list(e) for e in options], 'budget': 2,
         'nine_colorings': certificates, 'density_obstructions': {str(i): H for i, H in density.items()},
         'nodes': nodes, 'root': root,
         'statistics': {'configurations': comb(N, 2), 'initial_density_rejections': initial_density_count,
                        'initial_coloring_rejections_after_density': initial_coloring_count,
                        'inherited_colorings': inherited, 'learned_colorings': len(certificates)-inherited,
                        'coloring_solver_calls': calls, 'coloring_solver_nodes': solver_nodes,
                        'unresolved_pairs': unresolved, 'dag_nodes': len(nodes), 'merged_visits': merges,
                        'generation_seconds': time.perf_counter()-start},
         'scope': 'Remove the eight joins from vertices 24 and 25 to vertices 0..3 of the labelled C7[K4]. Add exactly two distinct edges absent from the original host. This certificate covers these 24976 graphs only.',
         'merge_semantics': 'Same remaining choices and same surviving certified nine-colorings. This preserves these rejection tests, not full graph equivalence.',
         'official_epoch_verifier_run': False, 'lean_formalized': False}
    audit = check(a)
    out = ROOT/'results'
    out.mkdir(exist_ok=True)
    (out/'earth_new_family.json.gz').write_bytes(gzip.compress(json.dumps(a, separators=(',', ':')).encode(), mtime=0))
    (out/'earth_new_family_audit.json').write_text(json.dumps(audit, indent=2)+'\n')
    print(json.dumps({'statistics': a['statistics'], 'audit': audit}, indent=2), flush=True)
    return a, audit


def check(a):
    started = time.perf_counter()
    def need(x, message):
        if not x:
            raise ValueError(message)
    need(a['schema'] == 'compound-eye-earth-family-dag-v1', 'Wrong schema.')
    n = a['num_vertices']
    need(type(n) is int and n == 28 and a['budget'] == 2, 'Wrong region dimensions.')
    def edges(values):
        need(all(isinstance(e, list) and len(e) == 2 and all(type(v) is int for v in e)
                 and 0 <= e[0] < e[1] < n for e in values), 'Invalid graph edge.')
        result = {tuple(e) for e in values}
        need(len(result) == len(values), 'Duplicate graph edge.')
        return result
    host = edges(a['original_host'])
    expected = {e for e in combinations(range(n), 2)
                if e[0]//4 == e[1]//4 or (e[1]//4-e[0]//4) % 7 in (1, 6)}
    need(host == expected, 'Original host changed.')
    removed = edges(a['removed_joins'])
    need(removed == {(x, y) for x in range(4) for y in (24, 25)}, 'Deletion region changed.')
    base = edges(a['base_edges'])
    need(base == host-removed, 'Base graph mismatch.')
    opts = [tuple(e) for e in a['optional_edges']]
    need(opts == [e for e in combinations(range(n), 2) if e not in host], 'Optional-edge universe incomplete or reordered.')
    colors = a['nine_colorings']
    for c in colors:
        need(proper(base, c, n), 'False nine-coloring certificate.')
    density = {}
    for index, values in a['density_obstructions'].items():
        i = int(index)
        need(0 <= i < len(opts), 'Invalid density trigger.')
        H = edges(values)
        need(H <= base | {opts[i]} and len(H) > 4*n-8, 'Density certificate has wrong support or count.')
        # Direct triple enumeration, different from producer's neighbor-intersection check.
        need(all(not ({(u, v), (u, w), (v, w)} <= H) for u, v, w in combinations(range(n), 3)), 'Density witness contains a triangle.')
        density[i] = H
    # Independent direct finite coverage, without using the DAG traversal.
    flat = {'density': 0, 'nine_coloring': 0, 'unresolved': 0}
    for pair in combinations(range(len(opts)), 2):
        if any(i in density for i in pair):
            flat['density'] += 1
        elif any(all(c[opts[i][0]] != c[opts[i][1]] for i in pair) for c in colors):
            flat['nine_coloring'] += 1
        else:
            flat['unresolved'] += 1
    nodes, N = a['nodes'], len(opts)
    visited, totals = set(), {}
    def verify(i, pos, left, available):
        if left == 0:
            pos = N
        need(type(i) is int and 0 <= i < len(nodes), 'Missing decision node.')
        node = nodes[i]
        need(node['pos'] == pos and node['left'] == left and node['available_colorings'] == available, 'Unsound certificate-state merge.')
        if i in totals:
            return totals[i]
        visited.add(i)
        if node['kind'] == 'coloring':
            need(left == 0 and available >> node['certificate'] & 1, 'False coloring terminal.')
            answer = (0, 1, 0)
        elif node['kind'] == 'unresolved':
            need(left == 0 and not available, 'Incorrect unresolved leaf.')
            answer = (0, 0, 1)
        else:
            need(node['kind'] == 'decision' and left > 0, 'Invalid decision.')
            yesid = node['include']
            if pos in density:
                yes = nodes[yesid]
                need(yes['kind'] == 'density' and yes['option'] == pos
                     and yes['pos'] == pos+1 and yes['left'] == left-1, 'Incorrect density branch.')
                visited.add(yesid)
                y = (comb(N-pos-1, left-1), 0, 0)
            else:
                u, v = opts[pos]
                mask = sum(1 << j for j, c in enumerate(colors) if c[u] != c[v])
                y = verify(yesid, pos+1, left-1, available & mask)
            if left > N-pos-1:
                need(node['exclude'] == -1, 'Impossible exclusion branch.')
                z = (0, 0, 0)
            else:
                z = verify(node['exclude'], pos+1, left, available)
            answer = tuple(x+y for x, y in zip(y, z))
            need(sum(answer) == comb(N-pos, left), 'Coverage sum mismatch.')
        totals[i] = answer
        return answer
    counts = verify(a['root'], 0, 2, (1 << len(colors))-1)
    need(tuple(flat.values()) == counts and len(visited) == len(nodes), 'DAG and direct audit disagree.')
    need(sum(counts) == a['statistics']['configurations'] == comb(N, 2), 'Region cardinality mismatch.')
    return {'all_passed': True, 'configurations_certified': sum(counts), 'density_rejections': counts[0],
            'nine_coloring_rejections': counts[1], 'unresolved': counts[2],
            'nodes_checked': len(nodes), 'nine_colorings_checked': len(colors),
            'density_witnesses_checked': len(density), 'seconds': time.perf_counter()-started,
            'scope': a['scope'], 'epoch_target_solved': False}


if __name__ == '__main__':
    if len(sys.argv) > 1:
        with gzip.open(sys.argv[1], 'rt') as f:
            print(json.dumps(check(json.load(f)), indent=2))
    else:
        run()
