import json,gzip,glob
S='/tmp/claude-0/-home-user-operator-first/211fc7c6-f60e-5702-90d7-e59337b51555/scratchpad'; B='/home/user/operator-first/research/acc/live/boards/'
for pat,out in (('ac_*.json.gz','live_all_ac.txt'),('stable_ac_*.json.gz','live_all_sac.txt')):
    f=sorted(glob.glob(B+pat))[-1]; d=json.load(gzip.open(f))['data']['items']
    with open(S+'/'+out+'.tmp','w') as o:
        for x in d: o.write(f"{x['challengeId']} {x.get('currentBestLength') or 0} {x.get('kTeams') or 0}\n")
    import os; os.replace(S+'/'+out+'.tmp',S+'/'+out); print('REFRESH',out,f.split('/')[-1])
