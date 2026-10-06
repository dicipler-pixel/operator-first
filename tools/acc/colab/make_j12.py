#!/usr/bin/env python3
"""Build the self-contained Colab bundle colab_j12_rival.py: embeds our C engines (acc_opt, acc_beam with P2/dual,
acc_window, acc_capped) and the target list (records from the latest board snapshot). usage: make_j12.py OUT TARGETS.json"""
import base64, json, sys
R = "/home/user/operator-first/"
O = R + "research/acc/optimality/"
src = {n: base64.b64encode(open(O + n, "rb").read()).decode() for n in ("acc_opt.c", "acc_beam.c", "c16_table.inc", "acc_window.c", "acc_capped.c")}
tg = json.load(open(sys.argv[2]))
head = '#!/usr/bin/env python3\n"""J12 (Mad Hatters ACC): rival-rows search for Colab. Self-contained: clones the official SAIR repo at the pinned commit,\n' \
       'compiles our engines, builds the T8 finish table, runs a dual-P2 beam (3 orientations) and an exact capped BFS lane,\n' \
       'replays every line on the official verifier, and writes a report file every ~35 min (and at once on a tie/beat).\n' \
       'Colab:  !python3 colab_j12_rival.py --hours 11 --outdir /content/drive/MyDrive/J12\n"""\n'
body = open(R + "tools/acc/colab/j12_body.py").read()
out = head + "PIN = 'a0fd6e6f52d82c93ccc06ab91d81e8fa3678256e'\nSRC = %s\nTARGETS = %s\n" % (json.dumps(src), json.dumps(tg)) + body
open(sys.argv[1], "w").write(out)
print("wrote", sys.argv[1], len(out), "bytes,", len(tg), "targets")
