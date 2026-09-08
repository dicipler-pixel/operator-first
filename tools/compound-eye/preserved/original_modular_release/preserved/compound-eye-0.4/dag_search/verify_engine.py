#!/usr/bin/env python3
"""Meaningful regression, independent algebra, and adversarial proof checks."""
from copy import deepcopy
from itertools import combinations
from pathlib import Path
import json
import random
import time

from decision_dag import Context, DecisionDAG, Registry, basis_of, digest
from check_dag import check, canonical
from exact_ak import controls
from check_ak_certificate import check as check_primal
from run_searches import baseline, load, save, attach_positive_certificates, RESULTS
if not __debug__:
    raise RuntimeError('Run this test suite without Python -O.')


def run():
    started = time.perf_counter()
    passed = []
    _, ctx = baseline()
    a = load(RESULTS/'dag_with_obstructions.json.gz')
    rng = random.Random(20260907)
    for _ in range(120):
        width = rng.randint(1, 8)
        rows = [[rng.randint(-8, 8) for _ in range(width)] for _ in range(rng.randint(0, 8))]
        assert basis_of(rows) == canonical(rows)
        scaled = [row[:] for row in rows]
        rng.shuffle(scaled)
        scaled = [[factor*x for x in row] for row in scaled
                  for factor in [rng.choice([-9, -3, 2, 7])]]
        assert basis_of(scaled) == basis_of(rows)
    passed.append('120 independent rational-space checks, including row permutation and nonzero rescaling')
    registry = Registry(ctx)
    for record in a['obstructions']:
        registry.add({k: v for k, v in record.items() if k != 'record_sha256'})
    for _ in range(300):
        pos = rng.randrange(len(ctx.options)+1)
        selection = rng.sample(range(pos), min(pos, rng.randrange(4)))
        left = rng.randrange(2)
        mask = sum(1 << j for j in selection)
        suffix = ((1 << len(ctx.options))-1) ^ ((1 << pos)-1)
        required = mask | (suffix if left else 0)
        brute = next((i for i, r in enumerate(registry.records) if required & ~r['inside_options_mask'] == 0), None)
        assert registry.match(mask, pos, left) == brute
    passed.append('300 indexed-family queries agree with direct membership checks')
    for name, p in controls().items():
        generators = p['generators']
        base = deepcopy(p)
        base['generators'] = []
        c = Context(base, [x for x in p['X'] if x != [0, 0]])
        selection = [c.options.index((c.ids[tuple(g['vertex'])], tuple(g['label']))) for g in generators]
        known, _ = c.closure(c.state(selection))
        assert len(known) == c.n
        passed.append(name+' complete calibration survives the quotient-space engine')
    random_dir = Path(__file__).resolve().parent.parent/'frontier/certificates/random'
    random_checked = 0
    if random_dir.exists():
        for path in sorted(random_dir.glob('*.json')):
            cert = json.loads(path.read_text())
            check_primal(cert)
            p = deepcopy(cert['problem'])
            generators = p['generators']
            p['generators'] = []
            c = Context(p, [x for x in p['X'] if x != [0, 0]])
            selection = [c.options.index((c.ids[tuple(g['vertex'])], tuple(g['label']))) for g in generators]
            known, _ = c.closure(c.state(selection))
            assert known == [c.ids[tuple(v)] for v in cert['forced_vertices']]
            random_checked += 1
        passed.append(f'{random_checked} prior arbitrary-initial-T certificates agree with new exact closures')
    p = {'schema': 'arithmetic-kakeya-tower-v1', 'name': 'positive DAG control',
         'dims': [1], 'X': [[0, 0], [1, 0], [0, 1]], 'levels': [[]],
         'initial_known': [], 'generators': []}
    positive = DecisionDAG(Context(p, [[1, 0], [0, 1]]), 2)
    positive.run()
    attach_positive_certificates(positive)
    assert check(positive.artifact())['complete_configurations'] == 1
    save(RESULTS/'positive_control.json.gz', positive.artifact())
    passed.append('complete DAG terminal has an independently checked integer forcing certificate')
    negative = DecisionDAG(Context(p, [[1, 0], [0, 1]]), 1)
    negative.run()
    assert check(negative.artifact())['complete_configurations'] == 0
    passed.append('one-generator negative control is excluded with full coverage')
    bad_controls = []
    def reject(name, mutation):
        b = deepcopy(a)
        mutation(b)
        try:
            check(b)
        except (ValueError, KeyError, IndexError, TypeError):
            bad_controls.append(name)
        else:
            raise AssertionError('Checker accepted '+name)
    reject('changed initial-T scope', lambda b: b['problem']['initial_known'].append([1, 1]))
    reject('missing feasible branch', lambda b: b['nodes'][b['root']].__setitem__('exclude', -1))
    reject('cyclic proof edge', lambda b: b['nodes'][b['root']].__setitem__('include', b['root']))
    reject('incorrect generator cost', lambda b: b.__setitem__('budget', 4))
    reject('inflated coverage', lambda b: b['statistics'].__setitem__('configurations', 11481))
    reject('wrong coordinate basis', lambda b: b['free_coordinates'].reverse())
    def rank_only(b):
        child = b['nodes'][b['nodes'][b['root']]['include']]
        row = child['state'][0]
        row[-1] += 17
        child['state'] = [list(x) for x in canonical(child['state'])]
    reject('equal-rank but unequal-row-space merge', rank_only)
    def corrupt_functional(b):
        record = b['obstructions'][0]
        record['functionals'][0]['vector'] = [0]*(2*ctx.n)
        record['record_sha256'] = digest({k: v for k, v in record.items() if k != 'record_sha256'})
    reject('zero separator with recomputed hash', corrupt_functional)
    def corrupt_mask(b):
        record = b['obstructions'][0]
        record['inside_options_mask'] ^= 1
        record['record_sha256'] = digest({k: v for k, v in record.items() if k != 'record_sha256'})
    reject('false family membership with recomputed hash', corrupt_mask)
    badp = deepcopy(p)
    badp['X'].append([1, -1])
    try:
        Context(badp, [[1, -1]])
    except ValueError:
        bad_controls.append('forbidden target direction admitted as a generator')
    else:
        raise AssertionError('Forbidden direction was admitted.')
    changed = deepcopy(ctx.problem)
    changed['levels'][0][0]['label'] = [0, 1]
    try:
        Registry(Context(changed, ctx.pool)).add(a['obstructions'][0])
    except ValueError:
        bad_controls.append('stale obstruction reused after changing edge labels')
    else:
        raise AssertionError('Stale scope was accepted.')
    result = {'all_passed': True, 'checks': passed, 'rejected_false_controls': bad_controls,
              'random_existing_certificates_checked': random_checked,
              'seconds': time.perf_counter()-started, 'lean_formalized': False}
    save(RESULTS/'engine_verification.json', result)
    print(json.dumps(result, indent=2), flush=True)
    return result


if __name__ == '__main__':
    run()
