"""Reconstruct the archived saved-road graph, not the search, to its original hash."""
import gzip,hashlib,io,json,os,resource,struct,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import official_checker
from helpers.kernel_lane_v1 import add_trace,replay,state_of
resource.setrlimit(resource.RLIMIT_AS,(1024*1024*1024,resource.getrlimit(resource.RLIMIT_AS)[1]))
began=time.monotonic()
r=ROOT/'runs/kernel_revival/code_82e71293e34d8e6f'
result=json.loads((r/'worker_result.json').read_text())
expected={Path(x['path']).name:x['sha256'] for x in result['evidence']}
input_path=r/'captured_input.json'
assert official_checker.sha(input_path)==expected['captured_input.json']
pool=json.loads(input_path.read_text());core,*_=official_checker.load_kernel()
graph={((1,),(2,)):set()}
for road in pool['routes']:
    assert time.monotonic()-began<180
    ch=pool['challenges'][road['row_id']]
    verdict=core.verify(ch,road['moves'],ch['move_spec_version'],pool['limits'])
    assert verdict['ok']
    add_trace(core,graph,replay(core,state_of(ch['initial_relators']),road['moves']),road['moves'])
    assert len(graph)<=600000
states=sorted(graph);ids={s:i for i,s in enumerate(states)}
data={'states':[[list(w) for w in s] for s in states],'edges':[[ids[s],m,ids[t]] for s in states for t,m in sorted(graph[s],key=lambda e:(e[1],e[0]))],'cost':'unit official primitive','direction':'explicit forward and inverse'}
p=r/'exact_graph.json.gz';original=p.read_bytes();mtime=struct.unpack('<I',original[4:8])[0]
out=Path(__file__).parent/'reconstructed_graph.gz'
with out.open('wb') as raw:
    with gzip.GzipFile(filename='exact_graph.json.gz',mode='wb',fileobj=raw,mtime=mtime) as zipped:
        with io.TextIOWrapper(zipped) as stream:json.dump(data,stream,separators=(',',':'))
    raw.flush();os.fsync(raw.fileno())
actual=official_checker.sha(out)
report={'run':r.name,'kind':'artifact_reconstruction_from_saved_inputs','search_repeated':False,'states':len(graph),'edges':len(data['edges']),'gzip_mtime':mtime,'expected_sha256':expected[p.name],'actual_sha256':actual,'exact_original_hash_match':actual==expected[p.name],'elapsed_seconds':time.monotonic()-began,'peak_rss_mib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024}
(Path(__file__).parent/'reconstructed_graph_receipt.json').write_text(json.dumps(report,indent=2)+'\n')
assert report['exact_original_hash_match'], 'Preserve reconstruction; do not replace a mismatching artifact'
os.replace(out,p)
print(json.dumps(report))
