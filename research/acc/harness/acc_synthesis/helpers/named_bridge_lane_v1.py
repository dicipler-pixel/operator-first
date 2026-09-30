#!/usr/bin/env python3
"""Exact named-state queries on a pinned saved graph; fresh radius at most two.

Distinct from diffuse depth-eight frontier search: only paid prefixes/suffixes
and explicitly named states are tested. No quotient or symmetry is free.
"""
from collections import deque
import argparse
import gzip
import hashlib
import json
import math
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import official_checker
from harness import atomic_json
from helpers import kernel_lane_v1 as saved

ALGORITHM = 'named-exact-state-neighborhood-v1'
HELPER_PIN = 'ca9bfee637f01768a622f51a0b01e130e0729baed91e01c0038952b57955d4ca'
GRAPH = 'runs/kernel_revival/code_a7e9bffde8b90533/exact_graph.json.gz'
CAPTURE = 'runs/kernel_revival/code_a7e9bffde8b90533/captured_input.json'
GRAPH_PIN = 'd6b28b5d8139402b18225c3fa404c831e75055a6195bdc6d3c720ebe0060f835'
CAPTURE_PIN = 'f89f5ff8f6484a2d3f3a1e690b3debcc31e7694b9c38ca726539f3e7c62e82ee'

def state(words):
    alphabet = {'x':1, 'X':-1, 'y':2, 'Y':-2}
    return tuple(tuple(alphabet[c] for c in w) for w in words)

def neighborhood(core, origin, direction, admit=lambda: None):
    """Exhaust all move strings length <=2. Paths point in the declared direction."""
    result = {origin: []}
    admit()
    layer = [(origin, [])]
    generated = 0
    for depth in range(2):
        following = []
        for current, path in layer:
            for move in range(core.NUM_MOVES):
                admit()
                generated += 1
                if direction == 'predecessor':
                    dest = core.apply_move(current, core.INVERSE_MOVE[move])
                    route = [move] + path
                elif direction == 'successor':
                    dest = core.apply_move(current, move)
                    route = path + [move]
                else:
                    raise ValueError('Unknown direction')
                following.append((dest, route))
                if dest not in result or len(route) < len(result[dest]):
                    result[dest] = route
        layer = following
    return result, generated

def distances(graph, origin, admit):
    dist, parents, queue = {origin:0}, {}, deque([origin])
    admit()
    while queue:
        current = queue.popleft()
        for dest, move in sorted(graph.get(current, ()), key=lambda e:(e[1], e[0])):
            if dest not in dist:
                admit()
                dist[dest] = dist[current] + 1
                parents[dest] = (current, move)
                queue.append(dest)
    return dist, parents

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--row', required=True)
    p.add_argument('--output-dir', required=True)
    p.add_argument('--wall-seconds', type=float, default=180)
    p.add_argument('--node-cap', type=int, default=600000)
    p.add_argument('--memory-mib', type=int, default=1024)
    p.add_argument('--target-length', type=int, required=True)
    a = p.parse_args()
    if not math.isfinite(a.wall_seconds) or not 0 < a.wall_seconds <= 180:
        p.error('wall-seconds must be positive and <=180')
    if not 1 <= a.node_cap <= 600000 or not 64 <= a.memory_mib <= 1024 or a.target_length < 0:
        p.error('record, memory or target limit invalid')
    out = Path(a.output_dir).resolve()
    out.relative_to(ROOT/'runs')
    out.mkdir(parents=True, exist_ok=True)
    if (out/'worker_result.json').exists():
        raise ValueError('Immutable result already exists')
    hard = resource.getrlimit(resource.RLIMIT_AS)[1]
    cap = a.memory_mib*1024*1024
    resource.setrlimit(resource.RLIMIT_AS, (cap if hard < 0 else min(cap,hard), hard))
    started = time.monotonic()
    deadline = started + a.wall_seconds
    counts = {'admitted_records':0, 'generated_neighborhood_moves':0,
              'verified_graph_edges':0}
    reason, complete = 'named_neighborhood_complete', False
    def admit():
        if saved.stopped():
            raise InterruptedError('controller_stop')
        if time.monotonic() >= deadline:
            raise InterruptedError('wall_time_cap')
        if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024 >= a.memory_mib-32:
            raise InterruptedError('memory_headroom_cap')
        if counts['admitted_records'] >= a.node_cap:
            raise InterruptedError('record_cap')
        counts['admitted_records'] += 1
    if official_checker.sha(saved.__file__) != HELPER_PIN:
        raise ValueError('Saved-graph helper dependency changed')
    if official_checker.sha(ROOT/GRAPH) != GRAPH_PIN or official_checker.sha(ROOT/CAPTURE) != CAPTURE_PIN:
        raise ValueError('Saved graph or provenance changed')
    core, specs, doc, challenges = official_checker.load_kernel()
    ch = challenges[a.row]
    start, goal = saved.state_of(ch['initial_relators']), saved.state_of(ch['target_relators'])
    query_file = ROOT/'helpers/named_queries.json'
    queries = json.loads(query_file.read_text())
    query = queries['rows'][a.row]
    own = [r for r in json.loads((ROOT/'continuation/routes.json').read_text())['routes'] if r['row_id']==a.row]
    baseline = min((len(r['moves']) for r in own), default=None)
    best = min((r['moves'] for r in own), key=lambda m:(len(m),m), default=None)
    raw = json.loads(gzip.decompress((ROOT/GRAPH).read_bytes()))
    graph = {}
    tested = []
    for name, source in [('executed_named_bridge_lane_v1.py',Path(__file__)),
                         ('executed_kernel_dependency.py',Path(saved.__file__)),
                         ('executed_named_queries.json',query_file),
                         ('executed_test_named_bridge.py',ROOT/'tests/test_named_bridge.py')]:
        (out/name).write_bytes(source.read_bytes())
    atomic_json(out/'own_input.json',{'row_id':a.row,'routes':own,'baseline':baseline})
    fixed = []
    def candidate(moves, origin):
        nonlocal best
        if best is not None and len(moves) >= len(best):
            return
        c = {'row_id':a.row,'track':'AC','start':official_checker.render(start),
             'moves':moves,'ruleset_sha256':specs.get(ch['move_spec_version']).move_spec_hash.removeprefix('sha256:'),
             'evidence_grade':'V','family':ALGORITHM}
        receipt = official_checker.check(c)
        if not receipt['valid']:
            raise ValueError('Proposed paid composition failed independent replay: '+origin)
        best = moves
        fixed.append({'origin':origin,'length':len(moves),'receipt':receipt})
    try:
        nodes = [saved.state_of(words) for words in raw['states']]
        for node in nodes:
            admit()
            if node in graph:
                raise ValueError('Duplicate exact graph node')
            graph[node] = set()
        for i, move, j in raw['edges']:
            admit()
            source, dest = nodes[i], nodes[j]
            if type(move) is not int or not 0 <= move < core.NUM_MOVES or core.apply_move(source,move)!=dest:
                raise ValueError('Saved graph primitive edge failed replay')
            graph[source].add((dest,move))
            counts['verified_graph_edges'] += 1
        for source, edges in graph.items():
            for dest, move in edges:
                if (source,core.INVERSE_MOVE[move]) not in graph[dest]:
                    raise ValueError('Saved graph missing paid inverse edge')
        pref, pp = distances(graph,start,admit)
        suff, sp = distances(graph,goal,admit)
        if goal in pref:
            candidate(saved.prefix_path(pp,goal),'saved_graph_only')
        def report(label, node, direction=None, prefix=None, suffix=None):
            if prefix is not None and saved.replay(core,start,prefix)[-1] != node:
                raise ValueError('Named prefix failed replay')
            if suffix is not None and saved.replay(core,node,suffix)[-1] != goal:
                raise ValueError('Named suffix failed replay')
            row = {'label':label,'state':official_checker.render(node),'saved_node':node in graph,
                   'saved_distance_from_start':pref.get(node),'saved_distance_to_goal':suff.get(node),
                   'paid_prefix':prefix,'paid_suffix':suffix,'direction':direction,'hits':[]}
            if direction:
                near, generated = neighborhood(core,node,direction,admit)
                counts['generated_neighborhood_moves'] += generated
                row.update(neighborhood_unique_states=len(near),neighborhood_move_strings=1+generated)
                for other, bridge in sorted(near.items(),key=lambda x:(len(x[1]),x[0])):
                    if other not in graph:
                        continue
                    hit = {'state':official_checker.render(other),'bridge':bridge,
                           'saved_distance_from_start':pref.get(other),'saved_distance_to_goal':suff.get(other)}
                    if direction=='predecessor' and suffix is not None and other in pref:
                        moves = saved.prefix_path(pp,other)+bridge+suffix
                        hit['complete_cost'] = len(moves)
                        candidate(moves,label)
                    if direction=='successor' and prefix is not None and other in suff:
                        moves = prefix+bridge+saved.suffix_path(core,sp,other)
                        hit['complete_cost'] = len(moves)
                        candidate(moves,label)
                    row['hits'].append(hit)
            tested.append(row)
            return row
        if query['type']=='road_exit':
            road = query.get('moves')
            if road is None:
                if not own:
                    raise ValueError('Named own-road probe needs a saved road')
                road = min((r['moves'] for r in own),key=lambda m:(len(m),m))
            trace = saved.replay(core,start,road)
            if trace[-1] != goal:
                raise ValueError('Named source road fails exact endpoint')
            if query.get('entry_index') is not None:
                i=query['entry_index'];report('entry',trace[i],prefix=road[:i])
            for i in query['exit_indices']:
                report('exit_'+str(i),trace[i],direction='predecessor',suffix=road[i:])
        elif query['type']=='paid_prefix':
            prefix = query['moves'];node = saved.replay(core,start,prefix)[-1]
            if official_checker.render(node) != query['expected_state']:
                raise ValueError('Named stripped-state assertion failed replay')
            report('paid_stripped_core',node,direction='successor',prefix=prefix)
        elif query['type']=='pure_y_states':
            ms = state(query['ms_state'])[0]
            for m in range(2,9):
                pure = (2,)*m+(1,)
                other = (1,)+(2,)*m
                for index, node in enumerate(((pure,ms),(other,ms),(ms,pure),(ms,other))):
                    admit()
                    row=report('pure_y_m'+str(m)+'_orientation'+str(index),node)
                    finish=[5,1,6,13,13,5]+[3]*m
                    row['proposed_finish_cost']=len(finish)
                    row['proposed_finish_endpoint']=official_checker.render(saved.replay(core,node,finish)[-1])
                    row['proposed_finish_valid']=saved.replay(core,node,finish)[-1]==goal
                    if row['proposed_finish_valid'] and node in pref:
                        candidate(saved.prefix_path(pp,node)+finish,row['label'])
        else:
            raise ValueError('Unsupported bounded query')
        complete=True
    except InterruptedError as exc:
        reason=str(exc)
    # Memory errors and malformed inputs escape to the parent's interrupted ledger.
    coverage={'algorithm_id':ALGORITHM,'row_id':a.row,'graph_input':GRAPH,
              'graph_sha256':GRAPH_PIN,'capture_sha256':CAPTURE_PIN,'helper_sha256':HELPER_PIN,
              'queries_sha256':official_checker.sha(query_file),'limits':{'wall_seconds':a.wall_seconds,
               'node_cap':a.node_cap,'memory_mib':a.memory_mib,'fresh_radius':2},
              **counts,'graph_states':len(graph),'graph_directed_edges':sum(map(len,graph.values())),
              'complete_named_neighborhoods':complete,'termination_reason':reason,
              'best_saved_length':baseline,'best_length':len(best) if best is not None else None,
              'target_length':a.target_length,'queries':tested,'verified_compositions':fixed,
              'elapsed_seconds':time.monotonic()-started,
              'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,
              'scope':'Only the pinned saved graph and declared exact 0..2-move neighborhoods; no global impossibility or live scoring claim.'}
    atomic_json(out/'coverage.json',coverage)
    evidence=[out/'coverage.json',out/'own_input.json',ROOT/GRAPH,ROOT/CAPTURE]+[out/name for name in [
        'executed_named_bridge_lane_v1.py','executed_kernel_dependency.py','executed_named_queries.json','executed_test_named_bridge.py']]
    if best is not None and (baseline is None or len(best)<baseline):
        c={'row_id':a.row,'track':'AC','start':official_checker.render(start),'moves':best,
           'ruleset_sha256':specs.get(ch['move_spec_version']).move_spec_hash.removeprefix('sha256:'),
           'evidence_grade':'V','family':ALGORITHM}
        receipt=official_checker.check(c)
        if not receipt['valid']:
            raise ValueError('Final named bridge candidate fails pinned checker')
        atomic_json(out/'candidate.json',c);atomic_json(out/'receipt.json',receipt)
        evidence += [out/'candidate.json',out/'receipt.json']
        result={'kind':'candidate','candidate':c,'summary':f'Paid named bridge route {len(best)}, saved baseline {baseline}, target {a.target_length}; no live scoring claim.'}
    else:
        result={'kind':'bounded_miss','summary':f'No improvement in named exact neighborhoods; best {len(best) if best is not None else None}, target {a.target_length}; {reason}.',
                'limits':coverage['limits'],'actual_coverage':{**counts,'complete_named_neighborhoods':complete,'queries_completed':len(tested)},
                'termination_reason':reason,'reopen_when':{'event':'new_exact_named_state_or_saved_edges','row_id':a.row}}
    if official_checker.sha(saved.__file__)!=HELPER_PIN:
        raise ValueError('Dependency changed during query')
    result['evidence']=[{'path':str(path.relative_to(ROOT)),'sha256':official_checker.sha(path)} for path in evidence]
    atomic_json(out/'worker_result.json',result)
    print(json.dumps({'kind':result['kind'],'result_path':str((out/'worker_result.json').relative_to(ROOT))}))

if __name__=='__main__':
    main()
