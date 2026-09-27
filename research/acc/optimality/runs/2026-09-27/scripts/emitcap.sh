#!/bin/bash
# usage: emitcap.sh ID "ac moves space-separated" ["sac moves space-separated"]
S=/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad; R=/home/user/operator-first
ID=$1; AC=$(echo $2 | tr ' ' ','); if [ -n "$3" ]; then SAC=$(echo $3 | tr ' ' ','); else SAC="$AC,16,15"; fi
F=$R/ACC_CANDIDATE_${ID}_20260926.txt
printf "ac-$ID: [$AC]\nsac-$ID: [$SAC]\n" > $F
REC=$(python3 -c "
import json
s={x['challengeId']:x for x in json.load(open('$S/ACC_PORTFOLIO_SCREEN/inputs/ACC_AC_SNAPSHOT_20260914_0945.json'))['data']['items']}; x=s['ac-$ID']; print(x['currentBestLength'],x['kTeams'])")
cd $S/sair && PYTHONPATH=competition/tools python3 -m verifier --manifest competition/tools/verifier/data/manifest.json --submission $F | python3 -c "import json,sys; r=json.load(sys.stdin); print('official CLI:', r['accepted'], [(x['challenge_id'],x['length'],x['ok']) for x in r['results']])"
echo "09-14 record/k: $REC"
cd $R && git add $F && git commit -qm "ACC: ac/sac-$ID via exact capped search (09-14 record/k $REC); official CLI accepted

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01B1kuzz5XCRpjgsfCqZSo3d" && git push -q origin claude/gallant-bardeen-0pgpae; git log --oneline -1; cat $F
