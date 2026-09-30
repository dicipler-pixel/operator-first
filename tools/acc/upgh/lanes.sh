#!/usr/bin/env bash
# Run N parallel code-runner lanes. Each task runs in a fresh process, so code fixes apply from the
# next task on. A lane ends when nothing is runnable or the harness is stopped. T9 is mmap-shared.
# usage: bash tools/acc/upgh/lanes.sh [N=3] [TASKS_PER_LANE=40]
set -u
N=${1:-3}; T=${2:-40}
cd "$(dirname "$0")/../../.." || exit 1
mkdir -p research/acc/upgh/cache
lane() {
  local i=$1 n=0
  while [ "$n" -lt "$T" ] && [ ! -f research/acc/upgh/STOP ]; do
    out=$(python3 tools/acc/upgh/upgh.py --json run --max-tasks 1 2>&1)
    echo "$(date -u +%FT%TZ) $out" | tr '\n' ' ' >> "research/acc/upgh/cache/lane$i.log"
    echo >> "research/acc/upgh/cache/lane$i.log"
    case "$out" in
      "[]"*) sleep 300 ;;
      *Refused*|*refused*) sleep 300 ;;
      *) bash tools/acc/upgh/commit_state.sh "UPG-H lane $i: $(echo "$out" | tr -d '\n' | grep -o '"task": "t[0-9]*"' | head -1) $(echo "$out" | tr -d '\n' | grep -o '"outcome": "[a-z]*"' | head -1)" >/dev/null 2>&1 ;;
    esac
    n=$((n + 1))
  done
}
for i in $(seq 1 "$N"); do lane "$i" & sleep 3; done
wait
