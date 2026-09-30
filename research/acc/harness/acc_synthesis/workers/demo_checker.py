#!/usr/bin/env python3
"""TOY CHECKER ONLY. One defined string transformation; not an ACC checker."""
import hashlib
import json
from pathlib import Path
import sys

path,receipt=map(Path,sys.argv[1:3]); candidate=json.loads(path.read_text())
valid=(candidate['row_id']=='DEMO-ONLY' and candidate['start']==['ab','b'] and
       candidate['moves']==['toy-remove-suffix-b'])
result={'candidate_sha256':hashlib.sha256(json.dumps(candidate,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest(),
        'checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'ruleset_sha256':candidate['ruleset_sha256'],'valid':valid,
        'exact_endpoint':['a','b'] if valid else candidate['start'],'cost':len(candidate['moves']),
        'peak_length':3}
receipt.write_text(json.dumps(result))
