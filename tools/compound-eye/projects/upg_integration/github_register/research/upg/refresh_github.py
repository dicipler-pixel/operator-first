"""Read-only public GitHub snapshot; never updates branches or proof grades.

python refresh_github.py --output github_live.json [--compare older_snapshot.json]
Uses GitHub REST without credentials. The public API may rate-limit requests.
"""
import argparse,datetime,json,urllib.request,urllib.error
from pathlib import Path

REPO='dicipler-pixel/operator-first'
def get(path):
    req=urllib.request.Request('https://api.github.com/repos/'+REPO+('/'+path if path else ''),headers={'Accept':'application/vnd.github+json','User-Agent':'Compound-Eye-Source-Register'})
    with urllib.request.urlopen(req,timeout=40) as r:return json.load(r)
def pages(path):
    data=[]
    for page in range(1,101):
        part=get(path+('&' if '?' in path else '?')+'per_page=100&page='+str(page));data.extend(part)
        if len(part)<100:return data
    raise RuntimeError('Pagination limit reached; snapshot incomplete.')
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('github_live.json'));p.add_argument('--compare',type=Path);a=p.parse_args()
    old=json.loads(a.compare.read_text()) if a.compare else None
    repo=get('');main=get('commits/'+repo['default_branch']);prs=pages('pulls?state=all&sort=updated&direction=desc')
    rows=[]
    for pr in prs:
        row={'number':pr['number'],'title':pr['title'],'state':pr['state'],'draft':pr['draft'],'url':pr['html_url'],
            'head_ref':pr['head']['ref'],'head_sha':pr['head']['sha'],'base_ref':pr['base']['ref'],'base_sha':pr['base']['sha']}
        try:
            runs=get('actions/runs?head_sha='+row['head_sha']+'&per_page=100')['workflow_runs']
            row['workflows']=[{'id':x['id'],'name':x['name'],'status':x['status'],'conclusion':x['conclusion'],'url':x['html_url']} for x in runs]
            row['workflow_scope']='Up to 100 runs matching source head; inspect tested merge revision and job logs before certifying a theorem.'
        except (urllib.error.URLError,TimeoutError) as e:row['workflow_error']=str(e)
        rows.append(row)
    out={'repository':REPO,'retrieved_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'main':main['sha'],'pull_requests':rows,
         'scope':'Read-only current metadata. No proof reruns or automatic grade changes.'}
    if old:
        prior={x['number']:x for x in old['pull_requests']}
        out['changed_heads']=[{'number':x['number'],'before':prior.get(x['number'],{}).get('head_sha'),'after':x['head_sha']} for x in rows if prior.get(x['number'],{}).get('head_sha')!=x['head_sha']]
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({'output':str(a.output),'pull_requests':len(rows),'changed_heads':out.get('changed_heads'),'workflow_errors':sum('workflow_error' in x for x in rows)},indent=2))
if __name__=='__main__':main()
