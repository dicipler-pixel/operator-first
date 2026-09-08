from pathlib import Path
import concurrent.futures, urllib.request, json, hashlib
ROOT=Path(__file__).resolve().parent
BASE='https://raw.githubusercontent.com/polyanskiy/refractiveindex.info-database/master/database/data/main'
tasks=[]
for el in ['Au','Ag','Cu','Pt']:
 tasks.append((f'{el}_Rakic-LD.yml',f'{BASE}/{el}/nk/Rakic-LD.yml'))
 if el!='Pt':tasks.append((f'{el}_Johnson.yml',f'{BASE}/{el}/nk/Johnson.yml'))
 u='https://physics.nist.gov/cgi-bin/ASD/ie.pl?spectra='+el+'&units=1&format=2&order=0&at_num_out=on&sp_name_out=on&ion_charge_out=on&el_name_out=on&seq_out=on&shells_out=on&level_out=on&e_out=0&unc_out=on&biblio=on'
 tasks.append((f'{el}_NIST.csv',u))
def one(item):
 name,url=item
 try:
  data=urllib.request.urlopen(url,timeout=25).read()
  (ROOT/'data'/name).write_bytes(data)
  return dict(file=name,url=url,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),status='downloaded')
 except Exception as e:return dict(file=name,url=url,status='failed',error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:results=list(ex.map(one,tasks))
(ROOT/'data'/'manifest.json').write_text(json.dumps({'retrieved':'2026-09-08','sources':results},indent=2))
for x in results:print(x['file'],x['status'],x.get('bytes'),x.get('error',''))
