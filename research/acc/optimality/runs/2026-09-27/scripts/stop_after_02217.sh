#!/bin/bash
until grep -q '"ac-02217"' /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/beam_unsolved.jsonl 2>/dev/null; do sleep 15; done
for p in $(ps aux | grep -E '[d]river_unsolved|[r]un_beam.py.*unsolved|[a]cc_beam' | awk '{print $2}'); do kill $p; done
echo "$(date -u +%FT%TZ) stopped unsolved queue after 02217 (rest handed to Colab)" >> /tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad/work/watchdog.log
