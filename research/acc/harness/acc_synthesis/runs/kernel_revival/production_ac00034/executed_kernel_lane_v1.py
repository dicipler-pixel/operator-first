#!/usr/bin/env python3
"""Kernel saved-road compressor adaptation: exact foreign graph and bounded bridges.

Historical Kernel transfer scripts are preserved as sources, never imported.
Only ordered freely reduced words are graph keys; there are no unpaid symmetries.
"""
from __future__ import annotations
import argparse
from collections import deque
import gzip
import hashlib
import heapq
import json
import math
from pathlib import Path
import resource
import sqlite3
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import official_checker

ALGORITHM = 'kernel-exact-foreign-road-overlay-v1'
RULE = 'e13f57d82b5db1a79c1bd9d5ee1f6665ac4d96a634a3656ea20c0ada82e07643'

def dump(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False)+'\n')

def state_of(words):
    return tuple(tuple(w) for w in words)

def stopped():
    db=ROOT/'state/ledger.sqlite3'
    if not db.exists(): return False
    with sqlite3.connect('file:'+str(db)+'?mode=ro', uri=True) as con:
        r=con.execute('SELECT stopped FROM control WHERE singleton=1').fetchone()
    return bool(r and r[0])

def replay(core, start, moves):
    states=[start]
    for m in moves:
        if type(m) is not int or not 0 <= m < core.NUM_MOVES:
            raise ValueError('bad saved primitive move')
        states.append(core.apply_move(states[-1],m))
    return states

def add_trace(core, graph, states, moves):
    for s,m,t in zip(states,moves,states[1:]):
        graph.setdefault(s,set()).add((t,m))
        graph.setdefault(t,set()).add((s,core.INVERSE_MOVE[m]))

def bfs(graph, origin, deadline=None):
    """Unit directed shortest distances and parent edges, exact states only."""
    dist={origin:0}; parents={}; q=deque([origin])
    while q:
        s=q.popleft()
        if deadline is not None and time.monotonic() >= deadline:
            return dist,parents,False
        for t,m in sorted(graph.get(s,()),key=lambda e:(e[1],e[0])):
            if t not in dist:
                dist[t]=dist[s]+1;parents[t]=(s,m);q.append(t)
    return dist,parents,True

def prefix_path(parents, state):
    out=[]
    while state in parents:
        state,m=parents[state];out.append(m)
    return list(reversed(out))

def suffix_path(core,parents,state):
    # parents were obtained by target-origin BFS on the explicit inverse graph.
    out=[]
    while state in parents:
        state,m=parents[state];out.append(core.INVERSE_MOVE[m])
    return out

def bridge_search(core, seeds, suffix_dist, suffix_parent, baseline, *, deadline,
                  node_cap, max_length, depth=8, stop_check=stopped):
    """Layered target-only bridge search; foreign roads are frozen saved data.

    Labels carry exact saved-prefix cost and immutable ancestry. Dominance is
    only within the same exact state and fresh depth. All admitted labels count.
    """
    best=list(baseline) if baseline is not None else None
    records=[];labels={};heap=[]
    counts={'admitted_records':0,'generated_moves':0,'expanded_by_depth':[0]*(depth+1),
            'dominated':0,'length_pruned':0,'cost_pruned':0,'exact_graph_collisions':0,
            'improvements':[],'max_fresh_depth':depth}
    reason='depth_exhausted';partial=None
    def path(rid):
        out=[]
        while records[rid][3] is not None:
            s,d,c,p,m,seed=records[rid];out.append(m);rid=p
        return records[rid][5]+list(reversed(out))
    def admit(s,d,c,parent,m,seed):
        old=labels.get((s,d))
        if old is not None and records[old][2] <= c:
            counts['dominated']+=1;return
        rid=len(records);records.append((s,d,c,parent,m,seed));labels[s,d]=rid
        heapq.heappush(heap,(d,c,rid));counts['admitted_records']+=1
    for s,p in sorted(seeds.items(),key=lambda x:(len(x[1]),x[0])):
        if counts['admitted_records'] >= node_cap:reason='node_cap';break
        if best is None or len(p)<len(best):admit(s,0,len(p),None,None,p)
    while heap and reason=='depth_exhausted':
        if time.monotonic()>=deadline:reason='wall_seconds';break
        if counts['admitted_records']>=node_cap:reason='node_cap';break
        if counts['generated_moves']%1024==0 and stop_check():reason='controller_stop';break
        d,c,rid=heapq.heappop(heap);s=records[rid][0]
        if labels.get((s,d))!=rid:continue
        partial={'fresh_depth':d,'cost':c}
        if s in suffix_dist:
            counts['exact_graph_collisions']+=1
            length=c+suffix_dist[s]
            if best is None or length<len(best):
                best=path(rid)+suffix_path(core,suffix_parent,s)
                counts['improvements'].append({'length':len(best),'fresh_depth':d,'meeting_state':[list(w) for w in s]})
        if d==depth or (best is not None and c+1>=len(best)):
            counts['cost_pruned']+=1;continue
        counts['expanded_by_depth'][d]+=1
        for m in range(core.NUM_MOVES):
            if time.monotonic()>=deadline:reason='wall_seconds';break
            if counts['admitted_records']>=node_cap:reason='node_cap';break
            t=core.apply_move(s,m);counts['generated_moves']+=1
            if sum(map(len,t))>max_length:counts['length_pruned']+=1;continue
            admit(t,d+1,c+1,rid,m,None)
    counts.update({'termination_reason':reason,'partial_layer':partial,
                  'unique_state_depth_labels':len(labels),'best_length':len(best) if best is not None else None})
    return best,counts

def candidate_for(row,start,moves):
    return {'row_id':row,'track':'AC','start':official_checker.render(start),'moves':moves,
            'ruleset_sha256':RULE,'evidence_grade':'V','family':'kernel-foreign-road-overlay'}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--row',required=True);p.add_argument('--output-dir',required=True)
    p.add_argument('--wall-seconds',type=float,default=180);p.add_argument('--node-cap',type=int,default=600000)
    p.add_argument('--target-length',type=int,default=41);p.add_argument('--memory-mib',type=int,default=1024)
    p.add_argument('--depth',type=int,default=8)
    p.add_argument('--source-pool',default='helpers/kernel_sources/roads_input.json')
    p.add_argument('--pool-route-cap',type=int,default=6000)
    a=p.parse_args(argv)
    if not math.isfinite(a.wall_seconds) or not 0<a.wall_seconds<=180 or not 1<=a.node_cap<=600000 or not 64<=a.memory_mib<=1024 or not 0<=a.depth<=8 or a.target_length<0 or not 1<=a.pool_route_cap<=6000:
        p.error('bounds: wall (0,180], nodes [1,600000], memory [64,1024], depth [0,8], pool [1,6000]')
    out=Path(a.output_dir).resolve()
    if not out.is_relative_to(ROOT/'runs/kernel_revival'):p.error('output must be under runs/kernel_revival')
    out.mkdir(parents=True,exist_ok=True)
    if (out/'worker_result.json').exists():p.error('use a fresh output directory')
    (out/'executed_kernel_lane_v1.py').write_bytes(Path(__file__).read_bytes())
    (out/'executed_test_kernel_lane.py').write_bytes((ROOT/'tests/test_kernel_lane.py').read_bytes())
    hard=resource.getrlimit(resource.RLIMIT_AS)[1];cap=a.memory_mib*1024*1024
    resource.setrlimit(resource.RLIMIT_AS,(cap if hard<0 else min(cap,hard),hard))
    started=time.monotonic();deadline=started+a.wall_seconds
    core,specs,doc,selected=official_checker.load_kernel()
    poolpath=(ROOT/a.source_pool).resolve();pool=json.loads(poolpath.read_text())
    challenge=selected[a.row];start=state_of(challenge['initial_relators']);target=state_of(challenge['target_relators'])
    ownpath=ROOT/'continuation/routes.json'
    if not ownpath.exists():ownpath=ROOT/'integration/recovered_routes.json'
    own=json.loads(ownpath.read_text())
    ownroutes=own.get('routes',[]) if isinstance(own,dict) else own
    known={(r['row_id'],tuple(r['moves'])) for r in pool['routes']}
    for r in ownroutes:
        if r['row_id']==a.row and (a.row,tuple(r['moves'])) not in known:
            pool['routes'].append({'row_id':a.row,'moves':r['moves'],'sources':[{'path':str(ownpath.relative_to(ROOT))}]})
            pool['challenges'][a.row]=challenge
            known.add((a.row,tuple(r['moves'])))
    graph={target:set()};traces=[];accepted=[];negative=[]
    coverage={'algorithm_id':ALGORITHM,'row_id':a.row,'sourcepool_fingerprint':official_checker.sha(poolpath),
              'source_routes_available':len(pool['routes']),'source_cursor_next':0,'source_verified':0,
              'foreign_verified':0,'donor_active_searches':0,'symmetry_moves':0,
              'limits':{'wall_seconds':a.wall_seconds,'node_cap':a.node_cap,'memory_mib':a.memory_mib,'fresh_depth':a.depth,'pool_route_cap':a.pool_route_cap},
              'ruleset_sha256':RULE,'representation':'ordered-freely-reduced-words','generator_map':{'1':'x','-1':'X','2':'y','-2':'Y'},
              'edge_direction':'each forward primitive and its explicit inverse; unit cost',
              'command':[sys.executable,'helpers/kernel_lane_v1.py']+(sys.argv[1:] if argv is None else list(argv)),
              'own_seed_source':str(ownpath.relative_to(ROOT)),'own_seed_source_sha256':official_checker.sha(ownpath),
              'python_version':sys.version,'live_score_claim':False}
    ingestion_reason='complete';reserve=bytearray(8*1024*1024)
    try:
        for i,r in enumerate(pool['routes']):
            if time.monotonic()>=deadline:ingestion_reason='wall_seconds';break
            if stopped():ingestion_reason='controller_stop';break
            if i>=a.pool_route_cap:ingestion_reason='pool_route_cap';break
            ch=pool['challenges'][r['row_id']]
            ih=__import__('verifier.canon',fromlist=['instance_hash']).instance_hash(ch['challenge_id'],ch['generators'],ch['initial_relators'],ch['target_relators'],ch['move_spec_version'],specs.get(ch['move_spec_version']).move_spec_hash)
            if ih!=ch['instance_hash']:raise ValueError('donor instance hash mismatch')
            verdict=core.verify(ch,r['moves'],ch['move_spec_version'],pool['limits'])
            coverage['source_cursor_next']=i+1
            if not verdict['ok']:
                negative.append({'source_record':i,'row_id':r['row_id'],'verdict':verdict});continue
            states=replay(core,state_of(ch['initial_relators']),r['moves'])
            if states[-1]!=target:raise ValueError('foreign endpoint mismatch')
            if len(graph)+len(set(states)-graph.keys())>a.node_cap:
                coverage['source_cursor_next']=i;ingestion_reason='node_cap';break
            add_trace(core,graph,states,r['moves']);accepted.append(i)
            coverage['source_verified']+=1
            if r['row_id']!=a.row:coverage['foreign_verified']+=1
            else:traces.append((r,states))
        coverage['ingestion_seconds']=time.monotonic()-started
        pref,pp,pcomplete=bfs(graph,start,deadline);suff,sp,scomplete=bfs(graph,target,deadline)
        baseline=prefix_path(pp,target) if target in pref else None
        seeds={s:prefix_path(pp,s) for r,states in traces for s in states if s in pref}
        best_saved=min((len(r['moves']) for r,states in traces),default=None)
        phase=time.monotonic()
        if pcomplete and scomplete and ingestion_reason=='complete':
            best,search=bridge_search(core,seeds,suff,sp,baseline,deadline=deadline,node_cap=max(1,a.node_cap-len(graph)),max_length=doc['limits']['max_total_relator_length'],depth=a.depth)
        else:
            best=baseline;search={'termination_reason':ingestion_reason if ingestion_reason!='complete' else 'graph_distance_wall','admitted_records':0,'generated_moves':0,'best_length':len(best) if best else None}
        coverage.update(search);coverage.update({'fresh_search_seconds':time.monotonic()-phase,'graph_distance_complete':pcomplete and scomplete,'pool_ingestion_termination':ingestion_reason,'pool_ingestion_complete':coverage['source_cursor_next']==len(pool['routes']),
            'source_rejected':negative,'graph_states':len(graph),'graph_directed_edges':sum(map(len,graph.values())),
            'target_saved_lengths':[len(r['moves']) for r,states in traces],'best_saved_length':best_saved,'saved_graph_shortest_length':len(baseline) if baseline else None,'target_length':a.target_length,'target_met':best is not None and len(best)<=a.target_length})
        coverage['total_admitted_state_records']=len(graph)+coverage['admitted_records']
    except MemoryError:
        del reserve;best=None;best_saved=None;coverage['termination_reason']='memory_cap'
    coverage['elapsed_seconds']=time.monotonic()-started
    coverage['peak_rss_mib']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
    # Captured inputs preserve every chosen path and exact donor initial object.
    chosen=[pool['routes'][i] for i in accepted]
    dump(out/'captured_input.json',{'sourcepool_fingerprint':coverage['sourcepool_fingerprint'],'manifest_sha256':pool['manifest_sha256'],'limits':pool['limits'],'challenges':{r['row_id']:pool['challenges'][r['row_id']] for r in chosen},'routes':chosen,'source_record_indices':accepted,'negative_coverage':negative})
    states=sorted(graph);ids={s:i for i,s in enumerate(states)}
    with gzip.open(out/'exact_graph.json.gz','wt') as f:
        json.dump({'states':[[list(w) for w in s] for s in states],'edges':[[ids[s],m,ids[t]] for s in states for t,m in sorted(graph[s],key=lambda e:(e[1],e[0]))],'cost':'unit official primitive','direction':'explicit forward and inverse'},f,separators=(',',':'))
    dump(out/'coverage.json',coverage)
    evidence=[out/'captured_input.json',out/'exact_graph.json.gz',out/'coverage.json',out/'executed_kernel_lane_v1.py',out/'executed_test_kernel_lane.py',ROOT/'helpers/kernel_protocol.json',ROOT/'helpers/kernel_sources/source_catalog.json']
    if best is not None and best_saved is not None and len(best)<best_saved:
        candidate=candidate_for(a.row,start,best);receipt=official_checker.check(candidate)
        if not receipt['valid']:raise ValueError('composed candidate fails official verification')
        dump(out/'candidate.json',candidate);dump(out/'receipt.json',receipt);evidence.extend([out/'candidate.json',out/'receipt.json'])
        result={'kind':'candidate','summary':f'Exact foreign-road overlay route {len(best)} improves saved {best_saved}; requested target {a.target_length}. No live score claim.','candidate':candidate}
    else:
        result={'kind':'bounded_miss','summary':f'No improvement under recorded foreign-road overlay scope; best {coverage.get("best_length")}, target {a.target_length}.','limits':coverage['limits'],'actual_coverage':{k:coverage[k] for k in ['source_verified','foreign_verified','source_cursor_next','graph_states','graph_directed_edges','admitted_records','generated_moves'] if k in coverage},'termination_reason':coverage['termination_reason'],'reopen_when':{'event':'new_verified_foreign_road','row_id':a.row}}
    result['evidence']=[{'path':str(x.relative_to(ROOT)),'sha256':official_checker.sha(x)} for x in evidence]
    dump(out/'worker_result.json',result)
    print(json.dumps({'result_path':str((out/'worker_result.json').relative_to(ROOT)),'kind':result['kind'],'best_length':coverage.get('best_length'),'termination_reason':coverage['termination_reason']}))

if __name__=='__main__':main()
