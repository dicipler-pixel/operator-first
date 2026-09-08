#!/usr/bin/env python3
"""Check source preservation, both histories, runtime hashes and portal inventory."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / 'tools/compound-eye'
sys.path.insert(0, str(TOOL))
import machine


def main():
    registry = machine.Registry(TOOL)
    source_inventories = TOOL / 'preserved/synchronization_3_2'
    checked = 0
    for name in ['universal_2_2', 'universal_3_1']:
        inv = json.loads((source_inventories / (name + '_inventory.json')).read_text())
        for rel, sha in inv.items():
            if rel.startswith(('catalog/eyes/', 'catalog/sets/', 'plugins/installed/')):
                assert hashlib.sha256((TOOL / rel).read_bytes()).hexdigest() == sha, (name, rel)
                checked += 1
    counts = json.loads((TOOL / 'release_counts.json').read_text())
    assert counts['eye_versions'] == len(registry.eyes) == 198
    assert counts['sets'] == len(registry.sets) == 30
    assert counts['statuses'] == dict(Counter(v['status'] for v in registry.eyes.values()))
    page = (TOOL / 'START_HERE.html').read_text()
    embedded = json.loads(re.search(r'const eyes=(.*?);const \$=', page, re.S)[1])
    assert {machine.reference(v): v for v in embedded} == registry.eyes
    for element in ['mixer', 'horizon', 'integration', 'arithmetic', 'catalog', 'elemental']:
        assert f'id="{element}"' in page and f'data-tab="{element}"' in page
    assert 'Universal 3.2' in page and '<b>198</b>eye versions' in page
    before = hashlib.sha256(page.encode()).hexdigest()
    subprocess.run([sys.executable, str(TOOL / 'build_portal.py')], check=True, stdout=subprocess.DEVNULL)
    assert hashlib.sha256((TOOL / 'START_HERE.html').read_bytes()).hexdigest() == before, 'Non-deterministic portal'
    assert (TOOL / 'projects/master_sync/MASTER_STATUS.md').is_file()
    assert (TOOL / 'projects/eye_mixer/Eye_Mixer_Guide.html').is_file()
    print(json.dumps({'status': 'PASS', 'source_manifest_checks': checked,
                      'eye_versions': 198, 'sets': 30,
                      'portal_registry_matches_runtime': True,
                      'deterministic_portal': True,
                      'scope': 'Release integrity, histories and presentation inventory; scientific checks run separately.'}))


if __name__ == '__main__':
    main()
