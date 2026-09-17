"""Restore a complete backup using only Python's standard library.
python restore_work.py --output /path/to/new/restored-work
Run from any directory. Parts and manifests are resolved beside this script.
"""
from pathlib import Path
import argparse,hashlib,json,tarfile,tempfile

def restore(root,dest):
    parts=json.loads((root/'PARTS.json').read_text());raw=(root/'FILES.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==parts['files_manifest_sha256'],'File inventory hash mismatch'
    inventory=json.loads(raw);expected={r['path']:r for r in inventory['files']}
    if dest.exists() and any(dest.iterdir()):raise ValueError('Choose an empty output directory to preserve existing work.')
    dest.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryFile() as archive:
        whole=hashlib.sha256();size=0
        for part in parts['parts']:
            path=root/'parts'/part['name'];b=path.read_bytes()
            assert len(b)==part['bytes'] and hashlib.sha256(b).hexdigest()==part['sha256'],str(path)+' failed verification'
            whole.update(b);size+=len(b);archive.write(b)
        assert size==parts['archive_bytes'] and whole.hexdigest()==parts['archive_sha256'],'Reassembled archive hash mismatch'
        archive.seek(0);seen=set()
        with tarfile.open(fileobj=archive,mode='r|xz') as tar:
            for item in tar:
                if not item.isfile() or item.name not in expected or item.name in seen:raise ValueError('Unexpected archive entry '+item.name)
                target=(dest/item.name).resolve()
                if not target.is_relative_to(dest.resolve()):raise ValueError('Unsafe archive path')
                row=expected[item.name];b=tar.extractfile(item).read()
                assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'Restored file mismatch '+item.name
                target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b);target.chmod(row['mode']);seen.add(item.name)
        assert seen==set(expected),'Missing archived files'
    result={'restored_files':len(seen),'verified_bytes':inventory['total_bytes'],'archive_sha256':parts['archive_sha256'],'all_file_hashes_match':True}
    (dest/'RESTORE_RESULT.json').write_text(json.dumps(result,indent=2));return result

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    print(json.dumps(restore(Path(__file__).resolve().parent,a.output.resolve()),indent=2))
