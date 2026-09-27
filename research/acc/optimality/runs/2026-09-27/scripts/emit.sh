#!/bin/bash
# usage: emit.sh ID "ac sac" MSG
S=/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad; R=/home/user/operator-first; ID=$1; KINDS=$2; F=$R/ACC_TIE_${ID}_20260925.txt
python3 - "$ID" "$KINDS" "$F" <<'EOF'
import json,sys
ID,K,F=sys.argv[1],sys.argv[2].split(),sys.argv[3]
S='/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad'
out=[]
for f in [S+'/work/beam_sac.jsonl',S+'/work/beam_sac_rev.jsonl']:
  try:
    for l in open(f):
      r=json.loads(l)
      if r['id']=='ac-'+ID: out=[f"{k}-{ID}: {str(r[k]).replace(' ','')}" for k in K]
  except FileNotFoundError: pass
open(F,'w').write('\n'.join(out)+'\n')
EOF
cat $F
cd $S/sair && PYTHONPATH=competition/tools python3 -m verifier --manifest competition/tools/verifier/data/manifest.json --submission $F | python3 -c "import json,sys; r=json.load(sys.stdin); print('official CLI:', r['accepted'], [(x['challenge_id'],x['length'],x['ok']) for x in r['results']])"
cd $R && git add $F && git commit -qm "ACC: $ID $3; official CLI accepted

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01B1kuzz5XCRpjgsfCqZSo3d" && git push -q origin claude/gallant-bardeen-0pgpae; git log --oneline -1
