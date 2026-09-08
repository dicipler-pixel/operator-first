"""Exact, context-scoped arithmetic Kakeya decision DAG.

Arithmetic uses arbitrary-precision integers. Primitive reduced rows identify
rational subspaces, not integral lattices. This is valid ONLY for forcing a
nonzero multiple of the target, as in Epoch's public verifiable setup.
"""
from copy import deepcopy
from functools import reduce
from itertools import combinations
from math import comb, gcd, lcm
import hashlib
import json
import time

from exact_ak import build

RULE = 'epoch-public-nonzero-multiple-forcing-v1'


def digest(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def primitive(row):
    g = reduce(gcd, row, 0)
    if not g:
        return tuple(row)
    first = next(x for x in row if x)
    g = abs(g) if first > 0 else -abs(g)
    return tuple(x // g for x in row)


def pivot(row):
    return next(i for i, x in enumerate(row) if x)


def remainder(basis, row):
    """A primitive representative proportional to the quotient remainder."""
    v = tuple(row)
    for b in basis:
        p = pivot(b)
        if v[p]:
            a, d = v[p], b[p]
            v = primitive(tuple(d*x - a*y for x, y in zip(v, b)))
    return v


def insert(basis, row):
    v = remainder(basis, row)
    if not any(v):
        return basis
    v = primitive(v)
    p = pivot(v)
    result = []
    for b in basis:
        if b[p]:
            b = primitive(tuple(v[p]*x - b[p]*y for x, y in zip(b, v)))
        result.append(b)
    result.append(v)
    return tuple(sorted(result, key=pivot))


def basis_of(rows):
    basis = ()
    for row in rows:
        basis = insert(basis, row)
    return basis


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def rank2(labels):
    nonzero = [x for x in labels if any(x)]
    if not nonzero:
        return 0
    a, b = nonzero[0]
    return 2 if any(a*y != b*x for x, y in nonzero[1:]) else 1


class Context:
    def __init__(self, problem, pool):
        self.problem = deepcopy(problem)
        if self.problem['generators']:
            raise ValueError('Search base must have no selected generators.')
        self.V, self.erows, self.edges = build(self.problem)
        self.ids = {v: i for i, v in enumerate(self.V)}
        self.n = len(self.V)
        self.width = 2*self.n
        self.initial = {self.ids[tuple(v)] for v in self.problem['initial_known']}
        self.pool = [tuple(x) for x in pool]
        if len(self.pool) != len(set(self.pool)) or not self.pool:
            raise ValueError('Generator pool must be nonempty and distinct.')
        X = {tuple(x) for x in self.problem['X']}
        if any(len(x) != 2 or any(type(a) is not int for a in x) or not any(x)
               or x not in X for x in self.pool):
            raise ValueError('Generator option outside X or malformed.')
        self.options = [(v, label) for v in range(self.n) for label in self.pool]
        self.raw_options = [self.genrow(v, label) for v, label in self.options]
        self.E = basis_of(self.erows)
        pivots = {pivot(b) for b in self.E}
        self.free = [j for j in range(self.width) if j not in pivots]
        self.projected = [tuple(remainder(self.E, row)[j] for j in self.free)
                          for row in self.raw_options]
        base = {k: self.problem[k] for k in ('schema', 'dims', 'X', 'levels', 'initial_known')}
        self.identity = {'rule': RULE, 'base_problem': base,
                         'ordered_vertices': [list(v) for v in self.V],
                         'ordered_pool': [list(x) for x in self.pool],
                         'target': [1, -1], 'arithmetic': 'rational-span-with-integer-certificates'}
        self.hash = digest(self.identity)
        self.cut_specs = []
        # This is only an optional cheap screen; large n still has an exact solver.
        if self.n <= 16:
            unknown = [v for v in range(self.n) if v not in self.initial]
            for bits in range(1, 1 << len(unknown)):
                S = {unknown[i] for i in range(len(unknown)) if bits >> i & 1}
                labels = [x for a, b, x in self.edges if (a in S) != (b in S)]
                if rank2(labels) < 2:
                    self.cut_specs.append((S, labels))

    def genrow(self, v, label):
        row = [0]*self.width
        row[2*v:2*v+2] = label
        return tuple(row)

    def lift(self, qrow):
        v = [0]*self.width
        for j, x in zip(self.free, qrow):
            v[j] = x
        return tuple(v)

    def state(self, selection):
        return basis_of(self.projected[j] for j in selection)

    def full_basis(self, state):
        result = self.E
        for row in state:
            result = insert(result, self.lift(row))
        return result

    def candidate(self, selection):
        p = deepcopy(self.problem)
        p['generators'] = [{'vertex': list(self.V[self.options[j][0]]),
                            'label': list(self.options[j][1])} for j in selection]
        return p

    def cut_reject(self, selection):
        for S, labs in self.cut_specs:
            if rank2(labs + [self.options[j][1] for j in selection if self.options[j][0] in S]) < 2:
                return True
        return False

    def closure(self, state):
        C = self.full_basis(state)
        known = set(self.initial)
        for v in known:
            C = insert(insert(C, self.genrow(v, (1, 0))), self.genrow(v, (0, 1)))
        while True:
            changed = False
            for v in range(self.n):
                if v in known:
                    continue
                if not any(remainder(C, self.genrow(v, (1, -1)))):
                    known.add(v)
                    C = insert(insert(C, self.genrow(v, (1, 0))), self.genrow(v, (0, 1)))
                    changed = True
            if not changed:
                return sorted(known), C

    def barrier(self, known, C, source):
        pairs = []
        den = lcm(*(row[pivot(row)] for row in C)) if C else 1
        for e in range(self.n):
            if e in known:
                continue
            rem = remainder(C, self.genrow(e, (1, -1)))
            if not any(rem):
                raise ValueError('Requested separating vector for a forceable vertex.')
            j = next(j for j, a in enumerate(rem) if a)
            z = [0]*self.width
            z[j] = den
            for row in C:
                p = pivot(row)
                z[p] = -(den // row[p])*row[j]
            pairs.append({'vertex': e, 'vector': list(primitive(z))})
        return {'schema': 'compound-eye-ak-obstruction-v2', 'context_sha256': self.hash,
                'known_container': list(known), 'functionals': pairs,
                'source': source,
                'claim': 'Forcing cannot leave the proper known_container when all selected generators annihilate these functionals.'}


def validate_record(ctx, record):
    if record.get('schema') != 'compound-eye-ak-obstruction-v2' or record.get('context_sha256') != ctx.hash:
        raise ValueError('Obstruction scope does not match this context.')
    K = record['known_container']
    if len(K) != len(set(K)) or any(type(v) is not int or not 0 <= v < ctx.n for v in K):
        raise ValueError('Invalid known container.')
    K = set(K)
    if not ctx.initial <= K or len(K) == ctx.n:
        raise ValueError('Container must include initial T and omit a vertex.')
    records = record['functionals']
    if len(records) != ctx.n-len(K) or {r['vertex'] for r in records} != set(range(ctx.n))-K:
        raise ValueError('Missing or duplicate separating functional.')
    for row in records:
        e, z = row['vertex'], row['vector']
        if len(z) != ctx.width or any(type(a) is not int for a in z):
            raise ValueError('Invalid integer vector.')
        if any(z[2*v] or z[2*v+1] for v in K) or z[2*e] == z[2*e+1]:
            raise ValueError('Functional does not separate the required target.')
        if any(dot(z, r) for r in ctx.erows):
            raise ValueError('Functional does not annihilate the fixed edge relations.')
    mask = sum(1 << j for j, option in enumerate(ctx.raw_options)
               if all(dot(r['vector'], option) == 0 for r in records))
    if 'inside_options_mask' in record and record['inside_options_mask'] != mask:
        raise ValueError('Forged family membership.')
    return mask


class Registry:
    def __init__(self, ctx):
        self.ctx = ctx
        self.records = []
        self.by_mask = {}
        self.match_calls = 0
        self.option_records = [0]*len(ctx.options)

    def add(self, record):
        mask = validate_record(self.ctx, record)
        if mask in self.by_mask:
            return self.by_mask[mask]
        record = deepcopy(record)
        record['inside_options_mask'] = mask
        record['record_sha256'] = digest(record)
        i = len(self.records)
        self.by_mask[mask] = i
        self.records.append(record)
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            self.option_records[bit.bit_length()-1] |= 1 << i
            remaining -= bit
        return i

    def seed_cuts(self):
        ctx = self.ctx
        for S, labels in ctx.cut_specs:
            directions = [next(x for x in labels if any(x))] if any(any(x) for x in labels) else ctx.pool
            for a, b in directions:
                z = [0]*ctx.width
                for v in S:
                    z[2*v], z[2*v+1] = b, -a
                self.add({'schema': 'compound-eye-ak-obstruction-v2', 'context_sha256': ctx.hash,
                          'known_container': sorted(set(range(ctx.n))-S),
                          'functionals': [{'vertex': v, 'vector': z} for v in sorted(S)],
                          'source': {'kind': 'exact_subset_cut', 'subset': sorted(S), 'direction': [a, b]},
                          'claim': 'Selected generators stay within a rank-one cut direction.'})

    def match(self, selection_mask, pos, left):
        self.match_calls += 1
        suffix = ((1 << len(self.ctx.options))-1) ^ ((1 << pos)-1)
        required = selection_mask | (suffix if left else 0)
        possible = (1 << len(self.records))-1
        while required and possible:
            bit = required & -required
            possible &= self.option_records[bit.bit_length()-1]
            required -= bit
        return (possible & -possible).bit_length()-1 if possible else None


class DecisionDAG:
    def __init__(self, ctx, budget, learning=True, seed_cuts=True):
        if type(budget) is not int or not 0 <= budget <= len(ctx.options):
            raise ValueError('Budget outside finite option domain.')
        self.ctx, self.budget, self.learning = ctx, budget, learning
        self.registry = Registry(ctx)
        self.seed_cuts = seed_cuts and learning
        self.nodes, self.memo = [], {}
        self.transitions = {}
        self.merge_hits = self.transition_hits = self.closure_calls = 0
        self.complete_representatives = []

    def run(self):
        started = time.perf_counter()
        if self.seed_cuts:
            self.registry.seed_cuts()
        self.root = self.visit(0, self.budget, (), ())
        elapsed = time.perf_counter()-started
        self.statistics = {'seconds': elapsed, 'nodes': len(self.nodes), 'merged_visits': self.merge_hits,
                           'transition_cache_hits': self.transition_hits, 'distinct_insertions': len(self.transitions),
                           'closure_calls': self.closure_calls, 'obstructions': len(self.registry.records),
                           'obstruction_queries': self.registry.match_calls,
                           'configurations': comb(len(self.ctx.options), self.budget),
                           'complete_configurations': self.count_complete(self.root),
                           'mode': 'dag_with_obstructions' if self.learning else 'dag_only'}
        return self.statistics

    def visit(self, pos, left, state, selection):
        N = len(self.ctx.options)
        if left > N-pos:
            return -1
        if not left:
            pos = N  # Future options are irrelevant once the exact budget is spent.
        key = pos, left, state
        if key in self.memo:
            self.merge_hits += 1
            return self.memo[key]
        i = len(self.nodes)
        self.memo[key] = i
        node = {'pos': pos, 'left': left, 'state': [list(row) for row in state],
                'representative': list(selection)}
        self.nodes.append(node)
        mask = sum(1 << j for j in selection)
        match = self.registry.match(mask, pos, left) if self.learning else None
        if match is not None:
            node.update(kind='excluded', obstruction=match)
            return i
        if not left:
            self.closure_calls += 1
            known, C = self.ctx.closure(state)
            node['closure'] = known
            if len(known) == self.ctx.n:
                node['kind'] = 'complete'
                self.complete_representatives.append(list(selection))
            else:
                rec = self.ctx.barrier(known, C, {'kind': 'terminal_dual', 'selection': list(selection)})
                blocker = self.registry.add(rec)
                if mask & ~self.registry.records[blocker]['inside_options_mask']:
                    raise ValueError('Computed barrier does not cover its source selection.')
                node.update(kind='excluded', obstruction=blocker)
            return i
        transition_key = state, pos
        if transition_key in self.transitions:
            child_state = self.transitions[transition_key]
            self.transition_hits += 1
        else:
            child_state = insert(state, self.ctx.projected[pos])
            self.transitions[transition_key] = child_state
        yes = self.visit(pos+1, left-1, child_state, selection+(pos,))
        no = self.visit(pos+1, left, state, selection)
        node.update(kind='decision', include=yes, exclude=no)
        return i

    def count_complete(self, node_id, cache=None):
        if cache is None:
            cache = {}
        if node_id == -1:
            return 0
        if node_id in cache:
            return cache[node_id]
        node = self.nodes[node_id]
        if node['kind'] == 'decision':
            result = self.count_complete(node['include'], cache)+self.count_complete(node['exclude'], cache)
        else:
            result = int(node['kind'] == 'complete')
        cache[node_id] = result
        return result

    def trace_selection(self, selection):
        chosen = set(selection)
        i = self.root
        while self.nodes[i]['kind'] == 'decision':
            node = self.nodes[i]
            i = node['include'] if node['pos'] in chosen else node['exclude']
            if i < 0:
                raise ValueError('Selection left the declared domain.')
        return self.nodes[i]

    def artifact(self):
        return {'schema': 'compound-eye-decision-dag-v1', 'context': self.ctx.identity,
                'context_sha256': self.ctx.hash, 'problem': self.ctx.problem,
                'pool': [list(x) for x in self.ctx.pool], 'budget': self.budget,
                'free_coordinates': self.ctx.free, 'root': self.root,
                'nodes': self.nodes, 'obstructions': self.registry.records,
                'statistics': self.statistics,
                'scope': 'All distinct-generator subsets of exactly this budget, at this fixed tower, initial T, and ordered pool. No graph isomorphism or coordinate normalization is used.',
                'official_epoch_verifier_run': False, 'lean_formalized': False}
