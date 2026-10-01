# Decode acc_disk layer keys (16-byte, MSB first: len0 6 bits, len1 6 bits, letters 2 bits x=0 X=1 y=2 Y=3) with total <= T.
import sys
fn, T = sys.argv[1], int(sys.argv[2]); L = 'xXyY'; out = []
with open(fn, 'rb') as f:
    while True:
        b = f.read(16)
        if len(b) < 16: break
        k = int.from_bytes(b, 'little'); l0 = k >> 122; l1 = (k >> 116) & 63
        if l0 + l1 > T:
            if l0 > T: break
            continue
        s = []; 
        for i in range(l0 + l1): s.append(L[(k >> (114 - 2 * i)) & 3])
        out.append(''.join(s[:l0]) + ',' + ''.join(s[l0:]))
print('\n'.join(out))
