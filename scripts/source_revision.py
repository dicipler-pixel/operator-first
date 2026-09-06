"""Record provenance in either a Git checkout or an extracted supplement."""
import shutil
import subprocess
from pathlib import Path


def source_revision(root):
    root = Path(root).resolve()
    if shutil.which('git'):
        top = subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=root,
                             capture_output=True, text=True)
        if top.returncode == 0 and Path(top.stdout.strip()).resolve() == root:
            commit = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=root,
                                    capture_output=True, text=True)
            if commit.returncode == 0:
                return commit.stdout.strip()
    revision_file = root / 'SOURCE_REVISION.txt'
    if revision_file.exists():
        return 'standalone archive: ' + revision_file.read_text().strip()
    return 'unversioned local sources; use recorded source SHA-256 values'
