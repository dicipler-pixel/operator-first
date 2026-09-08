#!/usr/bin/env python3
"""Run each declared object with its own eye sets and preserve every run."""
import argparse,json
from machine import ROOT,execute,save_run,dump
def main():
    p=argparse.ArgumentParser();p.add_argument('--only',nargs='*');a=p.parse_args()
    jobs=json.loads((ROOT/'requests/project_jobs.json').read_text())
    if a.only and not set(a.only)<=set(jobs):raise ValueError('Unknown project job.')
    latest=ROOT/'runs/latest_project_index.json'
    summaries=json.loads(latest.read_text()) if a.only and latest.exists() else {}
    for name,job in jobs.items():
        if a.only and name not in a.only:continue
        req=json.loads((ROOT/job['request']).read_text());out=execute(req,job['sets']);path=save_run(ROOT,out)
        summaries[name]={'run_file':str(path.relative_to(ROOT)),'request':job['request'],'sets':job['sets'],'statistics':out['statistics']}
        print(name,json.dumps(out['statistics']),flush=True)
    dump(ROOT/'runs/latest_project_index.json',summaries)
    return 2 if any(x['statistics']['status_counts']['error'] for x in summaries.values()) else 0
if __name__=='__main__':raise SystemExit(main())
