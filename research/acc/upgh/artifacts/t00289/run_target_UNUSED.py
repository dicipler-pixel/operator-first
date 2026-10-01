"""Bounded target run of sol61_ida on one manifest row; mirrors run_control.py's control logic.

No network calls. Reads the row by challenge_id from the exact pinned manifest only.
Saves raw stdout/stderr and exact settings. A lines file is written only after the
pinned official verifier (core.verify) accepts the candidate on the official challenge.
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
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--challenge', required=True)
    parser.add_argument('--depth', type=int, required=True)
    parser.add_argument('--cap', type=int, default=36)
    parser.add_argument('--ball', type=int, default=8)
    parser.add_argument('--ball-cap', type=int, default=None)
    parser.add_argument('--ball-states', type=int, default=4_000_000)
    parser.add_argument('--tt-states', type=int, default=2_000_000)
    parser.add_argument('--seconds', type=int, default=600)
    args = parser.parse_args()
    raw = args.manifest.read_bytes()
    git_hash = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    if git_hash != PINNED_BLOB:
        raise ValueError(f'manifest is not the pinned official Git blob: {git_hash}')
    manifest = json.loads(raw)
    index = submission.build_challenge_index(manifest)
    cid = args.challenge
    challenge = index[cid]
    if challenge['move_spec_version'] != 'ac-r2-v1' or challenge['target_relators'] != [[1], [2]]:
        raise ValueError('unexpected target specification')
    ball_cap = args.ball_cap if args.ball_cap is not None else args.cap
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = args.output_dir / stamp
    out.mkdir(parents=True, exist_ok=False)
    enc = {1: 'x', -1: 'X', 2: 'y', -2: 'Y'}
    words = [''.join(enc[c] for c in w) or '-' for w in challenge['initial_relators']]
    word_path = out / 'target_words.txt'
    word_path.write_text(' '.join(words + ['x', 'y']) + '\n')
    command = [str(ROOT / 'sol61' / 'sol61_ida'), '--input', str(word_path), '--depth', str(args.depth),
               '--cap', str(args.cap), '--ball', str(args.ball), '--ball-cap', str(ball_cap),
               '--ball-states', str(args.ball_states), '--tt-states', str(args.tt_states),
               '--seconds', str(args.seconds)]
    settings = {'official_commit': PINNED_COMMIT, 'manifest_git_blob': git_hash,
                'challenge_id': cid, 'initial_relators': challenge['initial_relators'],
                'command': command, 'known_route_used_as_input': False, 'started_utc': stamp}
    (out / 'settings.json').write_text(json.dumps(settings, indent=2) + '\n')
    with (out / 'stdout.txt').open('w') as stdout, (out / 'stderr.txt').open('w') as stderr:
        result = subprocess.run(command, stdout=stdout, stderr=stderr)
    output = (out / 'stdout.txt').read_text()
    search_status = ('incomplete' if 'STOP status=incomplete' in output
                     else 'complete_no_path' if 'STOP status=complete_no_path' in output
                     else 'found_candidate' if result.returncode == 0 and 'MOVES [' in output
                     else 'failed')
    receipt = {'process_exit_code': result.returncode, 'verified_line_written': False,
               'search_status': search_status, 'challenge_id': cid,
               'SAIR_API_calls': 0, 'submissions': 0,
               'ended_utc': datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}
    match = re.search(r'^MOVES (\[.*\])$', output, re.MULTILINE)
    if match:
        receipt['search_status'] = 'found_candidate'
        moves = json.loads(match.group(1))
        verdict = core.verify(challenge, moves, challenge['move_spec_version'], manifest['limits'])
        receipt['official_verifier'] = verdict
        receipt['candidate_length'] = len(moves)
        if verdict['ok']:
            # Only verifier-accepted lines are ever written.
            lines = [f'{cid}: ' + json.dumps(moves)]
            sac_id = 's' + cid
            if sac_id in index:
                sac = index[sac_id]
                sac_moves = moves + [16, 15]
                sac_verdict = core.verify(sac, sac_moves, sac['move_spec_version'], manifest['limits'])
                receipt['sac_official_verifier'] = sac_verdict
                if sac_verdict['ok']:
                    lines.append(f'{sac_id}: ' + json.dumps(sac_moves))
            (out / f'SOL61_lines_{stamp}.txt').write_text('\n'.join(lines) + '\n')
            receipt['verified_line_written'] = True
    (out / 'receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    report = f'SOL61 target {cid}, UTC {stamp}\n' + json.dumps(settings, indent=2) + '\n' + json.dumps(receipt, indent=2) + '\n'
    (out / f'SOL61_target_{stamp}.txt').write_text(report)
    print(json.dumps({'output_dir': str(out), **receipt}))
    return 0 if receipt['verified_line_written'] else 2

if __name__ == '__main__':
    raise SystemExit(main())
