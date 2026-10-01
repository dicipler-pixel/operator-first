#!/usr/bin/env python3
"""Low-read-budget send file: when the API read budget is near its floor, `upgh plan` cannot refresh boards (its stale-clock
gate is deliberate), so build the candidate file offline instead:
  - every SEND row in research/acc/upgh/cache/scout_latest.json (our checked road at or under the cached record, not held),
    with its path from the harness best;
  - every line waiting in research/acc/live/queue/*.txt (not in queue/sent/);
  minus every row we already hold at that length or shorter.
`python3 tools/acc/sair_api.py send FILE --lean --yes` then pulls fresh boards once (an essential read), drops every line that
no longer scores, and posts the rest. 0 API reads here.

usage: python3 tools/acc/upgh/offline_send_file.py OUT.txt   (prints the line count; writes nothing when there are none)"""
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE))
from harness import Harness  # noqa: E402

h = Harness(config_path=HERE / "config.json", state_dir=REPO / "research/acc/upgh", repo=REPO)
st = h.state()
lines = {}
scout = json.loads((REPO / "research/acc/upgh/cache/scout_latest.json").read_text())
for e in scout["sections"].get("SEND", []):
    b = st.best.get(e["row"])
    if b:
        lines[e["row"]] = b["moves"]
for f in sorted((REPO / "research/acc/live/queue").glob("*.txt")):
    for raw in f.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"\s*((?:s?ac)-\d{5})\s*:\s*(\[[^\]]*\])", raw)
        if m:
            p = json.loads(m.group(2))
            if m.group(1) not in lines or len(p) < len(lines[m.group(1)]):
                lines[m.group(1)] = p
held = h.held(st)                      # API history + the local send log (owner direct sends included)
lines = {c: p for c, p in lines.items() if held.get(c) is None or len(p) < held[c]}
print(len(lines))
if lines:
    Path(sys.argv[1]).write_text("".join("%s: [%s]\n" % (c, ", ".join(map(str, p))) for c, p in sorted(lines.items())))
