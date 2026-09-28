"""Build the ACC Field Record page from research/acc/live/record/{template.html,ideas.json,paths.json}
and the score history in research/acc/live/dashboard.json.  usage: build_record.py OUT.html"""
import json, os, sys, datetime
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'research', 'acc', 'live')
t = open(f'{R}/record/template.html').read()
scores = json.load(open(f'{R}/dashboard.json'))['scores']['points']
t = (t.replace('__PATHS__', json.dumps(json.load(open(f'{R}/record/paths.json'))))
      .replace('__IDEAS__', json.dumps(json.load(open(f'{R}/record/ideas.json'))))
      .replace('__SCORES__', json.dumps(scores))
      .replace('__PROOF__', json.dumps(json.load(open(f'{R}/record/proof.json'))))
      .replace('__UPDATED__', datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%MZ')))
open(sys.argv[1], 'w').write(t); print('wrote', sys.argv[1], len(t), 'bytes')
