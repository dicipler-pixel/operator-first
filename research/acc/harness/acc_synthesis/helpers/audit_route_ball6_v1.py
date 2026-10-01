#!/usr/bin/env python3
"""Check a saved radius certificate independently, without running the search."""
from collections import defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import resource
import sys
import time
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import official_checker

def main():
    out = Path(sys.argv[1]).resolve()
    out.relative_to(ROOT/'runs/route_ball6_revival')
    resource.setrlimit(resource.RLIMIT_AS,(1024*1048576,1024*1048576))
    start_time = time.monotonic()
    operations = 0
    def tick():
        nonlocal operations
        operations += 1
        if operations > 600000 or time.monotonic()-start_time > 180:
            raise RuntimeError('independent validation bound reached; no proof claim')
    frozen = json.loads((out/'captured_input.json').read_text())
    core,specs,doc,selected = official_checker.load_kernel()
    ch=selected[frozen['row_id']]
    verified=core.verify(ch,frozen['moves'],ch['move_spec_version'],doc['limits'])
    assert verified['ok']
    states=[tuple(tuple(w) for w in ch['initial_relators'])]
    for m in frozen['moves']:
        states.append(core.apply_move(states[-1],m))
    raw=gzip.decompress((out/'balls.json.gz').read_bytes())
    records=json.loads(raw)
    assert len(records)==len(states)==43
    witnessed=defaultdict(list)
    balls=[]
    for i,(seed,ball) in enumerate(zip(states,records)):
        distance={}
        for encoded,moves in ball:
            tick()
            state=tuple(tuple(w) for w in encoded)
            assert state not in distance and len(moves)<=3
            s=seed
            for m in moves:
                tick()
                s=core.apply_move(s,m)
            assert s==state
            distance[state]=len(moves)
            witnessed[state].append((i,len(moves)))
        assert distance[seed]==0
        for state,d in distance.items():
            if d==3: continue
            for m in range(core.NUM_MOVES):
                tick()
                t=core.apply_move(state,m)
                if sum(map(len,t))<=doc['limits']['max_total_relator_length']:
                    assert t in distance and distance[t]<=d+1
        balls.append(distance)
    cheaper=[]
    comparisons=0
    for entries in witnessed.values():
        for k,(i,di) in enumerate(entries):
            for j,dj in entries[k+1:]:
                tick();comparisons+=1
                if di+dj<j-i:
                    cheaper.append((i,j,di+dj))
    assert not cheaper
    receipt={'valid':True,'row_id':frozen['row_id'],'input_length':len(frozen['moves']),
      'complete_radius3_balls':len(balls),'admitted_labels':sum(map(len,balls)),
      'pair_comparisons':comparisons,'checks':operations,'cheaper_fixed_endpoint_replacements':0,
      'scope':'No <=6-primitive replacement shortens any interval between the 43 fixed states of this exact 42-move route, under the official relator-length limit. Not a global optimality claim.',
      'balls_sha256':hashlib.sha256((out/'balls.json.gz').read_bytes()).hexdigest(),
      'input_sha256':hashlib.sha256((out/'captured_input.json').read_bytes()).hexdigest(),
      'audit_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'official_input_receipt':verified,'elapsed_seconds':time.monotonic()-start_time,
      'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024}
    (out/'independent_radius_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))
if __name__=='__main__':main()
