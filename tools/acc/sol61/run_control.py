"""Rediscover only ac-09409 from the exact pinned manifest, then verify locally.

No network calls. No supplied control route, target-row data, or submission logic.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
PINNED_BLOB = 'accdb626ee08a06beea3f88dc7f351514c99eb27'
PINNED_COMMIT = 'a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e'
sys.path.insert(0, str(ROOT / 'official' / 'competition' / 'tools'))
from verifier import core, submission

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'sol61' / 'runs')
    parser.add_argument('--cap', type=int, default=36)
    parser.add_argument('--ball', type=int, default=8)
    parser.add_argument('--ball-states', type=int, default=4_000_000)
    parser.add_argument('--tt-states', type=int, default=2_000_000)
    parser.add_argument('--seconds', type=int, default=600)
    args = parser.parse_args()
    raw = args.manifest.read_bytes()
    git_hash = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    if git_hash != PINNED_BLOB:
        raise ValueError(f'manifest is not the pinned official Git blob: {git_hash}')
    manifest = json.loads(raw)
    challenge = submission.build_challenge_index(manifest)['ac-09409']
    if challenge['move_spec_version'] != 'ac-r2-v1' or challenge['target_relators'] != [[1], [2]]:
        raise ValueError('unexpected control specification')
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = args.output_dir / stamp
    out.mkdir(parents=True, exist_ok=False)
    enc = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}
    words = [''.join(enc[c] for c in w) or '-' for w in challenge['initial_relators']]
    word_path = out / 'control_words.txt'
    word_path.write_text(' '.join(words + ['x', 'y']) + '\n')
    command = [str(ROOT / 'sol61' / 'sol61_ida'), '--input', str(word_path), '--depth', '23',
               '--cap', str(args.cap), '--ball', str(args.ball), '--ball-cap', str(args.cap),
               '--ball-states', str(args.ball_states), '--tt-states', str(args.tt_states),
               '--seconds', str(args.seconds)]
    settings = {'official_commit': PINNED_COMMIT, 'manifest_git_blob': git_hash,
                'challenge_id': 'ac-09409', 'command': command,
                'known_route_used_as_input': False, 'started_utc': stamp}
    (out / 'settings.json').write_text(json.dumps(settings, indent=2) + '\n')
    with (out / 'stdout.txt').open('w') as stdout, (out / 'stderr.txt').open('w') as stderr:
        result = subprocess.run(command, stdout=stdout, stderr=stderr)
    output = (out / 'stdout.txt').read_text()
    search_status = ('incomplete' if 'STOP status=incomplete' in output
                     else 'complete_no_path' if 'STOP status=complete_no_path' in output
                     else 'found_candidate' if result.returncode == 0 and 'MOVES [' in output
                     else 'failed')
    receipt = {'process_exit_code': result.returncode, 'control_passed': False,
               'search_status': search_status,
               'target_rows_searched': 0, 'SAIR_API_calls': 0, 'submissions': 0}
    match = re.search(r'^MOVES (\[.*\])$', output, re.MULTILINE)
    if match:
        receipt['search_status'] = 'found_candidate'
        moves = json.loads(match.group(1))
        verdict = core.verify(challenge, moves, challenge['move_spec_version'], manifest['limits'])
        receipt['official_verifier'] = verdict
        receipt['control_passed'] = bool(verdict['ok'] and len(moves) == 23)
        if verdict['ok']:
            # Only verifier-accepted lines are ever written to the handoff.
            (out / f'SOL61_lines_{stamp}.txt').write_text('ac-09409: ' + json.dumps(moves) + '\n')
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    report = f'SOL61 control ac-09409, UTC {stamp}\n' + json.dumps(settings, indent=2) + '\n' + json.dumps(receipt, indent=2) + '\n'
    (out / f'SOL61_control_{stamp}.txt').write_text(report)
    print(json.dumps({'output_dir': str(out), **receipt}))
    return 0 if receipt['control_passed'] else 2

if __name__ == '__main__':
    raise SystemExit(main())
