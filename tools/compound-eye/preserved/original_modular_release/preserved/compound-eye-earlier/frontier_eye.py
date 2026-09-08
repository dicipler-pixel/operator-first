#!/usr/bin/env python3
"""Compound Eye 0.3: exact finite mathematical-target interface.

Use ak to produce a certificate, check-ak to verify one, or earth to screen
a proposed graph. The original compound_lab.py retains its numerical model API.
"""
import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent/'frontier'))
from exact_ak import certify
from check_ak_certificate import check
from earth_moon import screen


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['ak','check-ak','earth'])
    p.add_argument('input',help='JSON path or - for standard input')
    a=p.parse_args()
    try:
        data=json.load(sys.stdin) if a.input=='-' else json.loads(Path(a.input).read_text())
        result={'ak':certify,'check-ak':check,'earth':screen}[a.command](data)
        print(json.dumps(result,indent=2))
        return 0
    except (ValueError,TypeError,KeyError,IndexError,AttributeError,OSError) as exc:
        print(json.dumps({'status':'invalid_input_or_certificate','error':str(exc)}))
        return 2


if __name__=='__main__':raise SystemExit(main())
