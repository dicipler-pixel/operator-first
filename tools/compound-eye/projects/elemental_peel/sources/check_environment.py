"""Enforce the pinned verification dependencies before producing results."""
from pathlib import Path
from importlib.metadata import version

def enforce_versions(include_plotting=False):
    checked={}
    for line in (Path(__file__).parent/'requirements.txt').read_text().splitlines():
        if not line.strip() or line.startswith('#'):continue
        name,wanted=line.strip().split('==')
        if name=='matplotlib' and not include_plotting:continue
        actual=version(name)
        if actual!=wanted:
            raise RuntimeError(f'{name}=={wanted} required; found {actual}. Install requirements.txt before reproducing.')
        checked[name]=actual
    return checked

if __name__=='__main__':
    print('PASS pinned dependency versions',enforce_versions(include_plotting=True))
