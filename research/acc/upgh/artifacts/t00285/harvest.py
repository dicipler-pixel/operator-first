"""t00285: rebuild full paths from beam/capped outputs (prefix + reported moves), verify with the pinned core,
write lines.txt (ac-XXXXX: [...] and sac-XXXXX: [... + [16, 15]]) and verify_log.txt.  Prefixes are the
challenge-frame move lists used to reach each restart state (see intermediate_states.txt)."""
import glob, json, os, re, sys
from fam import *
A = os.path.dirname(os.path.abspath(__file__))
PREFIX = {  # beam tag -> (row, prefix moves in the official challenge frame)
    '09632_w20000_div0.6': ('ac-09632', []),
    '09632_tot15_div0.6': ('ac-09632', [7, 0, 12, 12, 12, 12, 12, 13, 7, 0, 8, 1, 0, 4, 13]),
    '05538_tot17_div0.6': ('ac-05538', [7, 0, 12, 12, 12, 12, 12, 12, 13, 7, 0, 8, 1, 0, 4, 13]),
    '05538_start_div0.6': ('ac-05538', []),
    '09632_start_H1': ('ac-09632', []),
}
found = []; log = []
for f in sorted(glob.glob(A + '/beam_*.out')):
    tag = os.path.basename(f)[5:-4]
    if tag not in PREFIX: log.append(f'{f}: no prefix registered, skipped'); continue
    row, pre = PREFIX[tag]
    for m in re.finditer(r'^(AC|SAC) (\d+) PATH ([\d ]+)$', open(f).read(), re.M):
        kind, d, mv = m.group(1), int(m.group(2)), list(map(int, m.group(3).split()))
        full = pre + mv
        if kind == 'AC':
            v = verify(CH[row], full); log.append(f'{tag} {kind} {d}: full len {len(full)} verify={v}')
            if v['ok']: found.append((row, full))
        else:
            log.append(f'{tag} {kind} {d}: raw moves recorded (SAC candidates not rebuilt here): {full}')
for f in sorted(glob.glob(A + '/capped_*.out')):
    txt = open(f).read(); log.append(f'{f}: {txt.strip()[:400]}')
    for m in re.finditer(r'^AC (\d+) PATH ([\d ]+)$', txt, re.M):
        row = 'ac-' + re.search(r'capped_(\d+)_', f).group(1)
        full = list(map(int, m.group(2).split())); v = verify(CH[row], full)
        log.append(f'{f} AC {m.group(1)}: verify={v}')
        if v['ok']: found.append((row, full))
with open(A + '/verify_log.txt', 'w') as g: g.write('\n'.join(log) + '\n')
if found:
    with open(A + '/lines.txt', 'w') as g:
        for row, p in found:
            g.write(f'{row}: {json.dumps(p)}\n'); g.write(f's{row}: {json.dumps(p + [16, 15])}\n')
print(len(found), 'verified paths;', len(log), 'log lines ->', A + '/verify_log.txt')
