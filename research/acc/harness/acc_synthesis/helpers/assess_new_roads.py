#!/usr/bin/env python3
"""Offline, bounded review of new saved AC roads against pinned donor starts.

No search, submission, networking, recipe import, or checkpoint reset occurs.
The output is evidence for an explicitly reviewed pool merge, not a candidate.
"""
import argparse
import hashlib
import json
from pathlib import Path
import resource
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import official_checker
from helpers.kernel_lane_v1 import add_trace,bfs,dump,replay,state_of,stopped


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--events',required=True)
    p.add_argument('--pool',default='helpers/kernel_sources/roads_input.json')
    p.add_argument('--output',required=True)
    a=p.parse_args()
    cap=1024*1024*1024;hard=resource.getrlimit(resource.RLIMIT_AS)[1]
    resource.setrlimit(resource.RLIMIT_AS,(cap if hard<0 else min(cap,hard),hard))
    started=time.monotonic();deadline=started+180
    def control():
        if stopped():raise RuntimeError('controller_stop')
        if time.monotonic()>=deadline:raise RuntimeError('review_deadline')
    events_path=(ROOT/a.events).resolve();pool_path=(ROOT/a.pool).resolve()
    out=(ROOT/a.output).resolve();out.relative_to(ROOT/'continuation')
    out.mkdir(parents=True,exist_ok=True)
    if (out/'review.json').exists():raise ValueError('Preserve old review; choose fresh output')
    source=json.loads(events_path.read_text());pool=json.loads(pool_path.read_text())
    core,specs,doc,selected=official_checker.load_kernel()
    from verifier.canon import instance_hash
    def verified_trace(row,moves):
        ch=pool['challenges'][row]
        pin=instance_hash(ch['challenge_id'],ch['generators'],ch['initial_relators'],ch['target_relators'],ch['move_spec_version'],specs.get(ch['move_spec_version']).move_spec_hash)
        if pin!=ch['instance_hash']:raise ValueError('donor_instance_hash')
        if ch['move_spec_version']!='ac-r2-v1':raise ValueError('foreign_ruleset')
        verdict=core.verify(ch,moves,ch['move_spec_version'],pool['limits'])
        if not verdict['ok']:return None,verdict
        states=replay(core,state_of(ch['initial_relators']),moves)
        if states[-1]!=((1,),(2,)):raise ValueError('foreign_endpoint')
        return states,verdict
    graph={((1,),(2,)):set()};known=set()
    for road in pool['routes']:
        control();row,moves=road['row_id'],road['moves']
        states,verdict=verified_trace(row,moves)
        if states is None:raise ValueError('existing_pool_failed_official_replay')
        add_trace(core,graph,states,moves);known.add((row,tuple(moves)))
        if len(graph)>600000:raise ValueError('review_state_cap')
    before_states=len(graph);before_edges=sum(map(len,graph.values()))
    before,_,done=bfs(graph,((1,),(2,)),deadline)
    if not done:raise RuntimeError('review_deadline')
    accepted=[];decisions=[]
    for event in source['events']:
        control();data=event['data'];row,moves=data['cid'],data['moves']
        item={'line':event['line'],'row_id':row,'length':len(moves)}
        if data.get('track')!='AC':item['status']='outside_AC_donors'
        elif (row,tuple(moves)) in known:item['status']='duplicate_move_array'
        elif row not in pool['challenges']:item['status']='missing_pinned_start'
        else:
            states,verdict=verified_trace(row,moves);item['official_verdict']=verdict
            if states is None:item['status']='official_rejected'
            else:
                novel=sum((t,m) not in graph.get(s,set()) for s,m,t in zip(states,moves,states[1:]))
                item['novel_forward_edges']=novel
                if not novel:item['status']='existing_edges_only'
                else:
                    add_trace(core,graph,states,moves)
                    if len(graph)>600000:raise ValueError('review_state_cap')
                    item['status']='verified_new_edges'
                    accepted.append({'row_id':row,'moves':moves,'sources':[{'archive':a.events,'source_blob':source['source_blob'],'line':event['line'],'independent_official_verdict':verdict}]})
                known.add((row,tuple(moves)))
        decisions.append(item)
    after,_,done=bfs(graph,((1,),(2,)),deadline)
    if not done:raise RuntimeError('review_deadline')
    starts=[]
    for row,ch in selected.items():
        start=state_of(ch['initial_relators'])
        starts.append({'row_id':row,'old_graph_distance':before.get(start),'new_graph_distance':after.get(start)})
    report={'schema':'acc-new-road-review/1','scope':'offline replay and graph comparison; not a new search or scoring claim','source_head':source['source_head'],'source_blob':source['source_blob'],'pool_sha256':official_checker.sha(pool_path),'events_sha256':official_checker.sha(events_path),'script_sha256':official_checker.sha(Path(__file__)),'bounds':{'wall_seconds':180,'memory_mib':1024,'graph_states':600000},'elapsed_seconds':time.monotonic()-started,'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,'before':{'states':before_states,'directed_edges':before_edges},'after':{'states':len(graph),'directed_edges':sum(map(len,graph.values()))},'decisions':decisions,'selected_graph_distances':starts,'accepted_roads':accepted}
    dump(out/'review.json',report)
    print(json.dumps({k:report[k] for k in ['scope','elapsed_seconds','peak_rss_mib','before','after']}))
    print(json.dumps({'accepted_roads':len(accepted),'statuses':{s:sum(x['status']==s for x in decisions) for s in sorted({x['status'] for x in decisions})},'selected_changes':[x for x in starts if x['old_graph_distance']!=x['new_graph_distance']]}))


if __name__=='__main__':main()
