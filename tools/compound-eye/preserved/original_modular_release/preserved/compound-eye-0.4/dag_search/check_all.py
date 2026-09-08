#!/usr/bin/env python3
"""Independently check the complete delivered proof bundle; standard library only."""
from itertools import product
from math import comb
from pathlib import Path
import gzip
import hashlib
import json
import time

from check_dag import check, reconstruct
from earth_families import check as check_earth

ROOT = Path(__file__).resolve().parent/'results'
if not __debug__:
    raise RuntimeError('Run this checker without Python -O; its aggregate assertions are required.')


def load(name):
    p = ROOT/name
    return json.loads(gzip.decompress(p.read_bytes()) if p.suffix == '.gz' else p.read_bytes())


def main():
    start = time.perf_counter()
    summary = load('new_regions.json')
    cores = load('all_initial_sets.json')
    audits = {}
    objects = {}
    names = ['dag_with_obstructions.json.gz']+[r['artifact'] for r in summary['regions']]
    assert len(names) == len(set(names))
    for i, name in enumerate(names):
        a = load(name)
        result = check(a)
        assert result['complete_configurations'] == 0
        audits[name] = result
        objects[name] = a
        if i % 25 == 0:
            print('proof bundles checked', i+1, '/', len(names), flush=True)
    for row in summary['regions']:
        assert row['artifact_sha256'] == hashlib.sha256((ROOT/row['artifact']).read_bytes()).hexdigest()
        assert row['context_sha256'] == objects[row['artifact']]['context_sha256']
    for core in cores['core_families']:
        refs = core['certificates']
        assert len(refs) == 7
        empty = next(r for r in refs if not r['initial_T'])
        a = objects[empty['artifact']]
        V, _, edges, options, _ = reconstruct(a['problem'], a['pool'])
        assert len(V) == 6 and len(edges) == 7 and a['budget'] == 3
        seen = set()
        for ref in refs:
            b = objects[ref['artifact']]
            T = tuple(tuple(v) for v in ref['initial_T'])
            assert b['problem']['initial_known'] == ref['initial_T']
            assert T not in seen and len(T) <= 1
            seen.add(T)
            for key in ('dims', 'X', 'levels'):
                assert b['problem'][key] == a['problem'][key]
            assert b['pool'] == a['pool']
            assert b['budget'] == (67*(6-len(T)))//40-7
        assert seen == {()} | {(v,) for v in V}
        assert 40*7 > 67*(6-2)
        assert len(options) >= 3  # Allows monotone padding after deduplicating R.
    # Deduplicate overlapping generator pools for the same G, T and budget.
    groups = {}
    for a in objects.values():
        p = a['problem']
        key = json.dumps([p['dims'], p['levels'], p['initial_known'], a['budget']], sort_keys=True)
        option_set = {tuple(x) for x in a['pool']}
        n = 1
        for d in p['dims']:
            n *= d
        if key in groups:
            prev, previous_n, budget = groups[key]
            assert option_set <= prev or prev <= option_set, 'Non-nested pools require a more general overlap audit.'
            option_set |= prev
        groups[key] = option_set, n, a['budget']
    union_count = sum(comb(len(pool)*n, budget) for pool, n, budget in groups.values())
    new_distinct = union_count-audits['dag_with_obstructions.json.gz']['configurations_certified']
    assert new_distinct == summary['new_configurations_beyond_baseline']
    assert summary['configurations_certified'] == sum(audits[name]['configurations_certified'] for name in names[1:])
    earth = check_earth(load('earth_new_family.json.gz'))
    assert earth['unresolved'] == 0
    result = {'all_passed': True, 'ak_proof_bundles_checked': len(audits),
              'ak_new_regions_checked': len(summary['regions']), 'core_families_all_initial_sets_checked': len(cores['core_families']),
              'ak_unique_configurations_including_old_baseline': union_count,
              'ak_distinct_new_configurations': new_distinct,
              'earth_new_configurations': earth['configurations_certified'],
              'all_distinct_new_configurations': new_distinct+earth['configurations_certified'],
              'positive_epoch_candidates': 0, 'earth_audit': earth,
              'seconds': time.perf_counter()-start,
              'scope': 'Exactly the declared finite domains; equal generator selections in nested pools counted once.',
              'official_epoch_verifier_run': False, 'lean_formalized': False}
    (ROOT/'complete_bundle_audit.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
