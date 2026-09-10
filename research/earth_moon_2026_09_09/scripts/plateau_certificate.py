#!/usr/bin/env python3
"""Exact connected-component certificate below an independent-triple ceiling.

Default ceiling five, from the original EM19 checkpoint. The generator uses the
original flip engine. Verification reconstructs every move from face incidence,
recounts all triples, and checks reachability and closure independently. No claim
about moves other than single diagonal flips or another component is made.
"""
from __future__ import annotations
import argparse,collections,hashlib,itertools,json,time
from pathlib import Path
import graph_core as engine

def key(layers):return tuple(sorted(tuple(sorted(tuple(sorted(f)) for f in fs)) for fs in layers))
def edges(fs):return {e for f in fs for e in itertools.combinations(f,2)}
def score(k):
    union=edges(k[0])|edges(k[1])
    return tuple(t for t in itertools.combinations(range(19),3)
                 if not any(e in union for e in itertools.combinations(t,2)))
def raw_neighbors(k):
    for side,fs in enumerate(k):
        inc=collections.defaultdict(list)
        for f in fs:
            for e in itertools.combinations(f,2):inc[e].append(f)
        for uv,ff in sorted(inc.items()):
            if len(ff)!=2:raise ValueError('Invalid face incidence')
            ab=tuple(sorted(set(ff[0]+ff[1])-set(uv)))
            if len(ab)!=2 or ab in inc:continue
            new=set(fs)-set(ff)
            new|={tuple(sorted((u,)+ab)) for u in uv}
            other=[tuple(x) for x in k];other[side]=tuple(sorted(new))
            yield key(other),(side,uv,ab)

def generate(source,ceiling):
    initial=json.loads(source.read_text());engine.verify(initial)
    start=key([x['faces'] for x in initial['layers']]);seen={start:None};todo=collections.deque([start])
    parent={};transitions=0
    while todo:
        k=todo.popleft();ls=[engine.Triangulation(19,list(fs)) for fs in k]
        for side,t in enumerate(ls):
            for idx in range(51):
                move=t.proposal(idx)
                if move is None:continue
                t.apply(move);nxt=key([x.faces for x in ls]);t.undo(move);transitions+=1
                if len(score(nxt))<=ceiling and nxt not in seen:
                    seen[nxt]=None;parent[nxt]=(k,(side,move[1],move[2]));todo.append(nxt)
    order=sorted(seen);ids={x:i for i,x in enumerate(order)}
    return {'format':'EM19_PLATEAU_V1','n':19,'ceiling':ceiling,
            'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'start':ids[start], 'states':order,
            'parents':{str(ids[x]):{'parent':ids[v[0]],'move':v[1]} for x,v in parent.items()},
            'generator_transitions':transitions,
            'scope':'single diagonal flips; exact face equality; layer swap only'}

def verify(cert,source):
    assert cert['format']=='EM19_PLATEAU_V1' and cert['n']==19
    assert cert['source_sha256']==hashlib.sha256(source.read_bytes()).hexdigest()
    states=[key(k) for k in cert['states']];assert len(set(states))==len(states)
    assert all([list(map(list,fs)) for fs in k]==raw for k,raw in zip(states,json.loads(json.dumps(cert['states']))))
    original=json.loads(source.read_text());initial=key([t['faces'] for t in original['layers']])
    assert states[cert['start']]==initial
    present=set(states);links={k:set() for k in states};counts=collections.Counter();same_triples=True
    for k in states:
        for fs in k:
            engine.verify_layer(19,{'edges':sorted(edges(fs)),'faces':list(fs)})
        ts=score(k);assert len(ts)<=cert['ceiling'];same_triples&=ts==score(initial)
        for nxt,move in raw_neighbors(k):
            v=len(score(nxt));counts[v]+=1
            if v<=cert['ceiling']:
                assert nxt in present,'Missing reachable state';links[k].add(nxt)
    seen={initial};todo=[initial]
    while todo:
        k=todo.pop()
        for nxt in links[k]-seen:seen.add(nxt);todo.append(nxt)
    assert seen==present,'Unreachable extraneous state'
    assert sum(counts.values())==cert['generator_transitions']
    for child,row in cert['parents'].items():
        p=states[row['parent']];dest=states[int(child)];wanted=json.loads(json.dumps(row['move']))
        assert any(nxt==dest and json.loads(json.dumps(mv))==wanted for nxt,mv in raw_neighbors(p))
    assert len(cert['parents'])==len(states)-1
    return {'verified':True,'states':len(states),'legal_transitions':sum(counts.values()),
            'score_histogram':dict(sorted(counts.items())),'all_states_same_bad_triples':same_triples,
            'minimum_exit_score':min(v for v in counts if v>cert['ceiling']),
            'minimum_inside_score':min(len(score(k)) for k in states),
            'no_Lean_claim':True}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--input',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--ceiling',type=int,default=5)
    p.add_argument('--verify',type=Path);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    t=time.monotonic();c=json.loads(a.verify.read_text()) if a.verify else generate(a.input,a.ceiling)
    r=verify(c,a.input)
    bad=json.loads(json.dumps(c));bad['states'].pop()
    try:verify(bad,a.input)
    except (AssertionError,IndexError,KeyError):r['omitted_state_negative_control']='rejected'
    else:raise AssertionError('Incomplete component accepted')
    (a.out/'certificate.json').write_text(json.dumps(c,separators=(',',':'))+'\n')
    r['seconds']=time.monotonic()-t;(a.out/'report.json').write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps(r,indent=2))
if __name__=='__main__':main()
