#!/usr/bin/env python3
"""Claude Code PreToolUse hook: while UPG-H is stopped, block search and submit commands.

settings.json runs this only when research/acc/upgh/STOP exists. It reads the
hook JSON from stdin. For a search, harness-dispatch or SAIR submit command it
exits 2 (blocked) and explains why on stderr. Everything else (reading,
harvesting, committing the ledger, `upgh resume` itself) passes.
"""
import json
import re
import sys

BLOCK = re.compile(r"acc_beam|acc_capped|acc_window|acc_opt|run_beam|run_window|run_meet|splice\.py"
                   r"|sair_api\.py\s+submit|upgh\.py\s+(run|execute|next|open|wake)\b")

try:
    event = json.load(sys.stdin)
except ValueError:
    sys.exit(0)
command = (event.get("tool_input") or {}).get("command") or ""
if BLOCK.search(command):
    print("UPG-H is stopped (research/acc/upgh/STOP). Search, dispatch and submit commands are blocked "
          "until a person runs `python3 tools/acc/upgh/upgh.py resume`.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
