#!/usr/bin/env python3
"""Reproduce the baseline benchmark and explicitly declared new AK regions."""
from copy import deepcopy
from itertools import combinations
from math import comb, gcd
from pathlib import Path
from statistics import median
import argparse
import gzip
import hashlib
import json
import time

from decision_dag import Context, DecisionDAG, digest
from check_dag import check as check_dag
from exact_ak import certify
from check_ak_certificate import check as check_primal

ROOT = Path(__file__).resolve().parent
RESULTS = ROOT/'results'
RESULTS.mkdir(exist_ok=True)


def save(path, value):
    raw = json.dumps(value, sort_keys=True, separators=(',', ':')).encode()
    if str(path).endswith('.gz'):
        Path(path).write_bytes(gzip.compress(raw, mtime=0))
    else:
        Path(path).write_text(json.dumps(value, indent=2)+'\n')


def load(path):
    path = Path(path)
    return json.loads(gzip.decompress(path.read_bytes()) if path.suffix == '.gz' else path.read_bytes())


def baseline():
    s = load(ROOT/'evidence/baseline_scope.json')
    return s, Context(s['fixed_problem_without_generators'], s['dilate_pool'])


def attach_positive_certificates(d):
    for node in d.nodes:
        if node['kind'] == 'complete':
            c = certify(d.ctx.candidate(node['representative']), include_cuts=False)
            if not check_primal(c)['forcing_complete']:
                raise ValueError('False positive from decision engine.')
            node['positive_certificate'] = c


def legacy_class():
    text = (ROOT/'evidence/legacy_verifier.py').read_text()
    env = {}
    exec(compile(text.split('print("CONTROL 1')[0], 'original_legacy_verifier', 'exec'), env)
    return env['AK']


def run_flat(ctx, budget, legacy=False):
    klass = legacy_class() if legacy else None
    tables = [{tuple(x['prefix']): tuple(x['label']) for x in level} for level in ctx.problem['levels']]
    start = time.perf_counter()
    trace = []
    calls = cuts = hits = 0
    for selection in combinations(range(len(ctx.options)), budget):
        if ctx.cut_reject(selection):
            cuts += 1
            trace.append([*selection, 'cut'])
            continue
        calls += 1
        if legacy:
            obj = klass(ctx.problem['X'], ctx.problem['dims'], tables, ctx.problem['initial_known'],
                        [{ctx.V[ctx.options[j][0]]: ctx.options[j][1]} for j in selection])
            known = sorted(ctx.ids[v] for v in obj.run())
        else:
            known, _ = ctx.closure(ctx.state(selection))
        hits += len(known) == ctx.n
        trace.append([*selection, 'closure', known])
    return {'seconds': time.perf_counter()-start, 'configurations': len(trace),
            'cut_rejections': cuts, 'closure_calls': calls, 'complete_configurations': hits}, trace


def benchmark(full_certificate_baseline=False):
    s, ctx = baseline()
    oldtrace = load(ROOT/'evidence/baseline_trace.json')
    if hashlib.sha256(json.dumps(oldtrace, separators=(',', ':')).encode()).hexdigest() != s['trace_sha256']:
        raise ValueError('Stored baseline trace changed.')
    modes = {'legacy_search': [], 'integer_flat_search': [], 'dag_only': [], 'dag_with_obstructions': []}
    # Rotate deterministic order to reduce a fixed warmup/order advantage.
    last_dags = {}
    for rep in range(3):
        names = list(modes)
        names = names[rep:] + names[:rep]
        for name in names:
            if name.endswith('_search'):
                stats, trace = run_flat(ctx, 3, legacy=name == 'legacy_search')
                if len(trace) != len(oldtrace):
                    raise ValueError('Enumeration cardinality changed.')
                for row, old in zip(trace, oldtrace):
                    if row[:3] != old[:3] or (row[3] == 'cut') != (old[3] == 'cut'):
                        raise ValueError('Baseline cut or enumeration mismatch.')
                    if row[3] != 'cut' and row[4] != old[4]:
                        raise ValueError('Exact baseline closure mismatch.')
            else:
                d = DecisionDAG(ctx, 3, learning=name == 'dag_with_obstructions')
                stats = d.run()
                for old in oldtrace:
                    leaf = d.trace_selection(old[:3])
                    if leaf['kind'] != 'excluded':
                        raise ValueError('DAG contradicts exhaustive baseline.')
                    if name == 'dag_only' and old[3] != 'cut' and leaf['closure'] != old[4]:
                        raise ValueError('DAG merged states with different closures.')
                last_dags[name] = d
            modes[name].append(stats)
            print('benchmark', rep+1, name, round(stats['seconds'], 4), flush=True)
    audits = {}
    for name, d in last_dags.items():
        artifact = d.artifact()
        audits[name] = check_dag(artifact)
        save(RESULTS/(name+'.json.gz'), artifact)
    original_certification = None
    if full_certificate_baseline:
        start = time.perf_counter()
        count = steps = duals = 0
        for row in oldtrace:
            if row[3] == 'cut':
                continue
            c = certify(ctx.candidate(row[:3]), include_cuts=False)
            result = check_primal(c)
            if result['forcing_complete'] or [ctx.ids[tuple(v)] for v in c['forced_vertices']] != row[4]:
                raise ValueError('Original certificate generation disagreed with baseline.')
            count += 1
            steps += len(c['steps'])
            duals += len(c['stalled_dual_certificates'])
            if count % 500 == 0:
                print('baseline exact certificates', count, '/ 4120', flush=True)
        original_certification = {'seconds': time.perf_counter()-start, 'certificates': count,
                                  'integer_steps': steps, 'integer_duals': duals,
                                  'scope': 'Fresh generation plus independent checking; no disk serialization.'}
    medians = {name: median(r['seconds'] for r in values) for name, values in modes.items()}
    report = {'all_baseline_outcomes_agree': True, 'all_4120_noncut_closures_agree': True,
              'repetitions': 3, 'mode_results': modes, 'median_seconds': medians,
              'independent_dag_audits': audits, 'fresh_original_certificate_baseline': original_certification,
              'closure_call_reduction_against_original': 1-modes['dag_with_obstructions'][-1]['closure_calls']/4120,
              'search_speed_ratio_original_over_dag': medians['legacy_search']/medians['dag_with_obstructions'],
              'scope': 'Same fixed 11480-case baseline. DAG times include obstruction and proof-graph production; flat search times do not produce certificates. Shared context construction and file I/O excluded. Proof production improvements cannot be attributed to state merging alone.'}
    if original_certification:
        old_total = medians['legacy_search']+original_certification['seconds']
        new_total = medians['dag_with_obstructions']+audits['dag_with_obstructions']['seconds']
        report['verified_pipeline_seconds'] = {'original': old_total, 'new': new_total, 'ratio': old_total/new_total}
    save(RESULTS/'benchmark.json', report)
    return report


def height_pool(h):
    return [(a, b) for a in range(-h, h+1) for b in range(-h, h+1)
            if a+b > 0 and gcd(abs(a), abs(b)) == 1]


def new_regions(use_cache=True):
    s, baseline_ctx = baseline()
    base = baseline_ctx.problem
    pool = baseline_ctx.pool
    declarations = []
    # Change exactly one nonzero level-table entry, not one expanded edge.
    # In level zero this changes three replicated edges simultaneously.
    for level, entries in enumerate(base['levels']):
        for j, entry in enumerate(entries):
            for lab in pool:
                if list(lab) == entry['label']:
                    continue
                p = deepcopy(base)
                p['levels'][level][j]['label'] = list(lab)
                ident = f'entry_{level}_{j}_{lab[0]}_{lab[1]}'
                declarations.append((ident, p, pool, 3,
                    {'kind': 'one_level_table_entry_changed', 'level': level, 'prefix': entry['prefix'],
                     'old_label': entry['label'], 'new_label': list(lab), 'new_configurations': comb(42, 3)}))
    # Six singleton initial known sets, each with every one-generator option.
    for v in baseline_ctx.V:
        p = deepcopy(base)
        p['initial_known'] = [list(v)]
        declarations.append(('initial_'+'_'.join(map(str, v)), p, pool, 1,
                             {'kind': 'nonempty_initial_T', 'new_configurations': 42}))
    # A second tower orientation with explicitly specified replicated relations.
    p = deepcopy(base)
    p['dims'] = [3, 2]
    p['levels'] = [[{'prefix': [1], 'label': [1, 0]}, {'prefix': [2], 'label': [1, 0]}],
                   [{'prefix': [1, 1], 'label': [0, 1]}, {'prefix': [2, 1], 'label': [1, 1]},
                    {'prefix': [3, 1], 'label': [0, 1]}]]
    declarations.append(('orientation_3_2', p, pool, 3,
                         {'kind': 'new_tower_and_replication', 'new_configurations': comb(42, 3)}))
    # Enlarge the old fixed tower's generator pool; count old overlap explicitly.
    pool3 = height_pool(3)
    p = deepcopy(base)
    p['X'] = [[0, 0]]+[list(x) for x in pool3]
    declarations.append(('generator_height_3', p, pool3, 3,
                         {'kind': 'expanded_generator_pool', 'known_overlap': comb(42, 3),
                          'new_configurations': comb(6*len(pool3), 3)-comb(42, 3)}))
    # Complete the singleton-T cases for every other declared six-vertex core.
    # Larger T cannot qualify: seven edges alone cost at least 7/4 > 67/40.
    for name, p, D, budget, change in list(declarations):
        if p['initial_known']:
            continue
        core_ctx = Context(p, D)
        for v in core_ctx.V:
            q = deepcopy(p)
            q['initial_known'] = [list(v)]
            overlap = 42 if name == 'generator_height_3' else 0
            declarations.append((name+'_initial_'+'_'.join(map(str, v)), q, D, 1,
                                 {'kind': 'singleton_T_for_new_core', 'parent_empty_T_region': name,
                                  'overlap_with_other_new_regions': overlap,
                                  'new_configurations': len(core_ctx.options)-overlap}))
    previous_file = RESULTS/'new_regions.json'
    previous = load(previous_file) if use_cache and previous_file.exists() else {}
    completed = {r['name']: r for r in previous.get('regions', previous.get('finished_regions', []))}
    output = []
    scopes = set()
    for k, (name, p, D, budget, change) in enumerate(declarations):
        started = time.perf_counter()
        ctx = Context(p, D)
        if ctx.hash in scopes or ctx.hash == baseline_ctx.hash:
            raise ValueError('New search repeated an exact old context.')
        scopes.add(ctx.hash)
        if 40*(len(ctx.edges)+budget) > 67*(ctx.n-len(ctx.initial)):
            raise ValueError('A declared new search cannot meet the score gate.')
        prior = completed.get(name)
        if (prior and prior['context_sha256'] == ctx.hash and prior['audit']['all_passed']
                and (RESULTS/prior['artifact']).exists()
                and prior.get('artifact_sha256') == hashlib.sha256((RESULTS/prior['artifact']).read_bytes()).hexdigest()):
            prior['change'] = change
            output.append(prior)
            continue
        dag = DecisionDAG(ctx, budget)
        imported = 0
        if name == 'generator_height_3':
            old = load(RESULTS/'dag_with_obstructions.json.gz')
            for record in old['obstructions']:
                adapted = {key: value for key, value in record.items()
                           if key not in ('record_sha256', 'inside_options_mask')}
                adapted['context_sha256'] = ctx.hash
                adapted['source'] = {'kind': 'explicit_revalidation_in_expanded_pool',
                                     'parent_record_sha256': record['record_sha256'],
                                     'parent_context_sha256': old['context_sha256']}
                dag.registry.add(adapted)  # Rechecks all edge identities and new option memberships.
                imported += 1
        stats = dag.run()
        attach_positive_certificates(dag)
        artifact = dag.artifact()
        artifact['change_from_baseline'] = change
        audit = check_dag(artifact)
        filename = name+'.json.gz'
        save(RESULTS/filename, artifact)
        row = {'name': name, 'artifact': filename, 'context_sha256': ctx.hash,
               'artifact_sha256': hashlib.sha256((RESULTS/filename).read_bytes()).hexdigest(),
               'change': change, 'statistics': stats, 'audit': audit,
               'revalidated_prior_obstructions': imported,
               'total_seconds': time.perf_counter()-started}
        output.append(row)
        save(RESULTS/'new_regions.json', {'status': 'running', 'finished_regions': output})
        print('new region', k+1, '/', len(declarations), name,
              'cases', stats['configurations'], 'complete', stats['complete_configurations'],
              'seconds', round(row['total_seconds'], 3), flush=True)
    report = {'status': 'exhausted_declared_regions', 'regions': output,
              'configurations_certified': sum(x['statistics']['configurations'] for x in output),
              'new_configurations_beyond_baseline': sum(x['change']['new_configurations'] for x in output),
              'overlap_with_original_baseline': sum(x['change'].get('known_overlap', 0) for x in output),
              'overlap_among_new_regions': sum(x['change'].get('overlap_with_other_new_regions', 0) for x in output),
              'complete_configurations': sum(x['statistics']['complete_configurations'] for x in output),
              'scope': 'Distinct exact public input contexts. Not claimed inequivalent under all possible graph relabellings or target-preserving coordinate changes. No other level tables or initial sets are covered.',
              'official_epoch_verifier_run': False, 'lean_formalized': False}
    save(RESULTS/'new_regions.json', report)
    cores = [('baseline_height_2', base, pool, 'dag_with_obstructions.json.gz')]
    cores += [(name, p, D, name+'.json.gz') for name, p, D, budget, change in declarations if not p['initial_known']]
    full_status = []
    core_index = []
    for name, p, D, budget, change in declarations:
        q = deepcopy(p)
        T = tuple(tuple(v) for v in q['initial_known'])
        q['initial_known'] = []
        core_index.append((name, Context(q, D).hash, T))
    by_name = {row['name']: row for row in output}
    for name, p, D, empty_file in cores:
        c = Context(p, D)
        refs = {(): empty_file}
        for region_name, core_hash, T in core_index:
            if T and core_hash == c.hash:
                refs[T] = by_name[region_name]['artifact']
        if len(refs) != 7 or any((v,) not in refs for v in c.V):
            raise ValueError('An initial-set case is missing.')
        if len(c.edges) != 7 or c.n != 6:
            raise ValueError('All-T budget argument needs this exact edge/vertex count.')
        full_status.append({'core': name, 'empty_T_context_sha256': c.hash,
                            'pool_size': len(D), 'n': c.n, 'm': len(c.edges),
                            'empty_T_max_generator_budget': 3, 'singleton_T_max_generator_budget': 1,
                            'certificates': [{'initial_T': [list(v) for v in T], 'artifact': file} for T, file in refs.items()]})
    save(RESULTS/'all_initial_sets.json', {
        'core_families': full_status, 'count': len(full_status),
        'all_T_covered_at_score_67_over_40': True,
        'proof': 'For n=6,m=7: |T|=0 permits at most 3 generators; |T|=1 permits at most 1; |T|>=2 fails because 7/(6-|T|)>=7/4>67/40. Smaller generator sets and lists with duplicates are covered by monotonic padding to the tested distinct-generator budget.',
        'scope': 'Only these fixed edge-labelled towers and their specified generator pools. No other edge labels or tower sizes.'})
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['benchmark', 'search', 'all'])
    parser.add_argument('--full-baseline-certificates', action='store_true')
    parser.add_argument('--fresh', action='store_true', help='Recompute the new regions instead of reusing matching certificates.')
    args = parser.parse_args()
    if args.action in ('benchmark', 'all'):
        benchmark(args.full_baseline_certificates)
    if args.action in ('search', 'all'):
        new_regions(use_cache=not args.fresh)
