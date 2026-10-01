"""Read-only audit of both completed, immutable geometry experiments."""
import gzip,hashlib,json,sys
from pathlib import Path
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[2];sys.path.insert(0,str(ROOT))
from official_checker import load_kernel
core,_,doc,starts=load_kernel();start=tuple(tuple(w) for w in starts['ac-00009']['initial_relators']);goal=((1,),(2,))
paths=['runs/geometry_revival/code_c3456c8439b8dadc','runs/geometry_simple_revival/code_9ab0757b75c40721']
audits=[]
for idx,path in enumerate(paths):
 r=ROOT/path;coverage=json.loads((r/'coverage.json').read_text());graph=json.loads(gzip.decompress((r/'exact_graph.json.gz').read_bytes()))
 states=[tuple(tuple(w) for w in s) for s in graph['states']]
 for i,j,m in graph['edges']:assert core.apply_move(states[i],m)==states[j]
 labels=0;cycles=0;by_arm={}
 for name in [a['arm'] for a in coverage['arms']]:
  initial=goal if name=='reverse_toward' else start;memo={(): (initial,frozenset([initial]),False)};distinct=set();n=bad=0
  with gzip.open(r/(name+'_layers.jsonl.gz'),'rt') as f:
   for line in f:
    for label in json.loads(line)['beam']:
     p=tuple(label['path'])
     for k in range(1,len(p)+1):
      q=p[:k]
      if q not in memo:
       s,seen,loop=memo[q[:-1]];u=core.apply_move(s,q[-1]);memo[q]=(u,seen|{u},loop or u in seen)
     s,seen,loop=memo[p];assert s==tuple(tuple(w) for w in label['state']);distinct.add(s);n+=1;bad+=loop
  if idx:assert bad==0
  labels+=n;cycles+=bad;by_arm[name]={'retained_labels':n,'cyclic_labels':bad,'distinct_states':len(distinct)}
 audits.append({'path':path,'coverage_sha256':hashlib.sha256((r/'coverage.json').read_bytes()).hexdigest(),
                'checked_graph_edges':len(graph['edges']),'distinct_graph_states':len(states),'labels_checked':labels,'cyclic_labels':cycles,
                'by_arm':by_arm,'elapsed_seconds':coverage['elapsed_seconds'],'peak_rss_mib':coverage['peak_rss_mib'],
                'records':coverage['records'],'best_length':coverage['best_length']})
result={'type':'independent_readonly_graph_and_cycle_audit','row':'ac-00009','official_commit':doc['source_commit'],
        'audits':audits,'distinct_state_count_increase_pct':100*(audits[1]['distinct_graph_states']/audits[0]['distinct_graph_states']-1),
        'decision':'No shorter route. Preserve both negatives. Reject these score variants as demonstrated improvements; retain exact loop prevention and diagnostics. No automatic unchanged-input rerun.'}
(OUT/'comparison.json').write_text(json.dumps(result,indent=2)+'\n')
lines=['# Eight-way geometry and clock comparison: ac-00009','',
       '**Outcome: the independently verified saved best remains 78 paid moves.** Both eight-arm batches completed their declared record ceilings normally. There was no crash, kill, wall-time timeout or candidate to send. No live scoring claim.', '',
       '| Arm | First retained states | Cycle-free retained states | Best paid length |','|---|---:|---:|---:|']
for arm,a in audits[0]['by_arm'].items():lines.append(f"| {arm} | {a['distinct_states']} | {audits[1]['by_arm'][arm]['distinct_states']} | 78 |")
lines+=['','The first experiment retained removable exact-state cycles in 69–87% of its beam labels. The complete successor forbids revisiting an exact state on the current prefix and keeps that ancestor set in the history identity. All other scores, ceilings and beam settings are unchanged. Exact loop deletion preserves endpoints and lowers paid cost; no global optimality follows from either beam.', '',
        f"The pooled graphs contain {audits[0]['distinct_graph_states']} and {audits[1]['distinct_graph_states']} exact states, a {result['distinct_state_count_increase_pct']:.1f}% increase in count. Their shortest witnessed paths are both 78. Pool-only discoveries would have been attributed to the pool, rather than a single score.", '',
        f"Code execution: {audits[0]['elapsed_seconds']:.3f}s and {audits[1]['elapsed_seconds']:.3f}s; peak RSS {max(a['peak_rss_mib'] for a in audits):.2f} MiB. These are computation times, excluding implementation, audit and GitHub persistence. Records charged: {audits[0]['records']} and {audits[1]['records']}, each below 600,000.",'',
        f"Independent audit replayed {sum(a['checked_graph_edges'] for a in audits)} pooled primitive edges and {sum(a['labels_checked'] for a in audits)} retained labels using pinned official moves. The second batch has zero exact-state cycles in retained prefixes.",'',
        'The tested feature map is an explicit Sanov matrix/Cayley representation. It does not instantiate a physical Maxwell/gravity law. Fixed versus moving chart heading, shared versus relator clock, reverse heading and reverse search are separate hypotheses. Every comparison uses exact states for junctions and the official paid metric.', '',
        'Decision: retain the improved trace and loop controls; no score wins on route length. Park both keys. A next experiment needs fresh useful path data or a separately justified bridge mechanism; increasing width or renaming a score is not justified by this miss.', '',
        'All inputs, source snapshots, per-layer states/paths/history, budgets, exact graphs and result hashes are preserved in the two run directories listed in comparison.json. Both experimental registry entries are disabled after this explicit comparison; other continuation lanes remain unchanged.']
(OUT/'REVIEW.md').write_text('\n'.join(lines)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='audits'}));print(json.dumps(audits))
