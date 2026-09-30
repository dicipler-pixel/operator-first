#!/usr/bin/env python3
"""JSON-lines boundary example, intentionally no invented model API bindings.

Replace the function call in a COPY with your authenticated host's supported
model client. The client must enforce allowed paths/tool policy, run the role's
tools, and return one structured result. stdout is protocol-only; logs stderr.
"""
import json
import sys

def main():
    request=json.load(sys.stdin)
    print(json.dumps({'kind':'blocked','summary':f"No authenticated adapter bound for {request['model']}",
                      'evidence':[],'reopen_when':{'event':'adapter_connected','role':request['role']}}))

if __name__=='__main__': main()
