"""Self-contained evidence viewer: compact traces plus inspectable eye outputs."""
from pathlib import Path
import json
from records import load
HERE=Path(__file__).parent
def main():
    index=load(HERE/'results/sweeps.json');coverage=load(HERE/'results/coverage.json')
    studies={}
    for k,meta in index['studies'].items():
        rows=load(HERE/'results'/f'{k}.json');frames=[]
        for f in rows:
            frames.append({a:f[a] for a in ['parameter','metrics','notes','eyes','status_counts']})
        middle=rows[len(rows)//2]
        sample=[{'eye':x['eye'],'status':x['status'],'value':x.get('value'),'reason':x.get('reason'),'limits':x['limits'],'derivation':r['derivation']} for r in middle['runs'] for x in r['run']['results']]
        studies[k]={**meta,'frames':frames,'eye_count':len(index['data'][k]['eyes']),'sample_coordinate':middle['parameter'],'sample_eye_outputs':sample}
    payload={'studies':studies,'coverage':coverage,'index':index}
    findings=HERE/'results/findings.json'
    if findings.exists() or findings.with_suffix('.json.gz').exists():payload['findings']=load(findings)
    text=(HERE/'viewer.html').read_text().replace('__OBSERVATORY_DATA__',json.dumps(payload,separators=(',',':'),allow_nan=False).replace('<','\\u003c'))
    out=HERE/'All_Eyes_Observatory.html';out.write_text(text);print(out, out.stat().st_size)
if __name__=='__main__':main()
