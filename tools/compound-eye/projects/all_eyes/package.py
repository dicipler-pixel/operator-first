"""Make a complete small runtime for this observation session, including evidence."""
from pathlib import Path
import argparse,hashlib,json,shutil,zipfile
from records import load,seal
HERE=Path(__file__).parent;ROOT=HERE.parents[1]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True)
    seal(HERE/'results');findings=load(HERE/'results/findings.json')
    text='# All Eyes — coordinated observation findings\n\n'
    text+=f"{findings['frames']} frames; {findings['sweep_evaluations']} coordinated evaluations; {findings['coverage_evaluations']} registry-coverage evaluations; {findings['checks_passed']} mathematical and consistency checks.\n\n"
    text+='All 191 versions are accounted for. 171 implementations returned fresh results; the nuclear-data gate, 17 specified methods and two archives retain their actual status. 58 distinct versions participate in the coordinated sweeps.\n\n'
    for f in findings['findings']:text+='## '+f['title']+'\n\n'+f['text']+'\n\n'
    text+='## Current limits\n\nNo new Lean theorem, general Earth–Moon solution, improved Kakeya exponent or solution to the six remaining Diophantine targets is claimed. The QHE panel uses existing classified counts, not a fresh raw-IQ fit. The local server provides live mathematical recomputation; no laboratory feed is connected. UI handlers and live HTTP calls were checked; a fresh full-browser screenshot was not obtained.\n'
    (HERE/'FINDINGS.md').write_text(text)
    include=set()
    def add(rel):
        p=ROOT/rel
        for f in ([p] if p.is_file() else p.rglob('*')):
            if f.is_file() and '__pycache__' not in f.parts and f.suffix!='.pyc':include.add(f)
    for path in ['machine.py','requirements.txt','catalog','plugins','extensions','projects/all_eyes','preserved/original_modular_release/requests','preserved/original_modular_release/preserved/compound-eye-0.4','research/raw_population_replay.json','research/source_eye_cases.json','research/readout_calibration.json','runs/qhe/results.json','projects/peeling_cascade/cascade_runs.json','projects/upg_integration/verification.json','projects/diophantine/verification.json','projects/diophantine/evolution.json','runs/horizon/results.json']:add(path)
    include={f for f in include if not(f.parent==HERE/'results' and f.suffix=='.json')}
    files={str(f.relative_to(ROOT)):f.read_bytes() for f in sorted(include)}
    files['START_HERE.md']=(HERE/'README.md').read_bytes();files['All_Eyes_Observatory.html']=(HERE/'All_Eyes_Observatory.html').read_bytes()
    manifest={p:hashlib.sha256(b).hexdigest() for p,b in files.items()};files['MANIFEST.json']=(json.dumps(manifest,indent=2)+'\n').encode()
    dest=a.output/'All_Eyes_Observatory_Complete.zip'
    with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p,b in files.items():
            info=zipfile.ZipInfo('compound_eye_observatory/'+p,date_time=(2026,9,8,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,b)
    with zipfile.ZipFile(dest) as z:
        for p,sha in manifest.items():assert hashlib.sha256(z.read('compound_eye_observatory/'+p)).hexdigest()==sha
    for name in ['All_Eyes_Observatory.html','FINDINGS.md']:shutil.copy2(HERE/name,a.output/('All_Eyes_Findings.md' if name=='FINDINGS.md' else name))
    print(json.dumps({'zip':str(dest),'bytes':dest.stat().st_size,'files':len(files),'sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'all_manifest_hashes_verified':True}))
if __name__=='__main__':main()
