#!/bin/bash
# Rebuild the results map: fresh dashboard data -> results_data.json -> results_map.html (publish this file).
cd /home/user/operator-first
python3 tools/acc/dashboard_data.py >/dev/null 2>&1
python3 tools/acc/dashboard/build_results.py >/dev/null
python3 - <<'PY'
import json
t=open("tools/acc/dashboard/idea_map.html").read()
d=json.load(open("tools/acc/dashboard/results_data.json"))
open("tools/acc/dashboard/results_map.html","w").write(t.replace("/*RESULTS*/null",json.dumps(d,separators=(",",":"))))
PY
