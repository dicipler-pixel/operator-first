"""Read plain working records or the losslessly compressed portable evidence."""
from pathlib import Path
import gzip,json
def load(path):
    p=Path(path)
    if p.exists():return json.loads(p.read_text())
    return json.loads(gzip.decompress(p.with_suffix(p.suffix+'.gz').read_bytes()))
def seal(directory):
    for p in sorted(Path(directory).glob('*.json')):
        raw=p.read_bytes();out=p.with_suffix('.json.gz');out.write_bytes(gzip.compress(raw,compresslevel=9,mtime=0))
        assert gzip.decompress(out.read_bytes())==raw
