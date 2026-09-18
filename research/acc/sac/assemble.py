"""Merge every SAC path we hold, keep the shortest per row, verify, emit."""
import json, re, sys, glob, os
sys.path.insert(0, "tools/acc/eyes")
import replay_sac as S

LET = {"x": 1, "x^-1": -1, "y": 2, "y^-1": -2}
def load_board(p):
    out = {}
    for line in open(p, errors="replace"):
        line = line.strip()
        if not line:
            continue
        d = json.loads(line)
        b = re.search(r"<x, y \|(.*?)>\.", d["description"]).group(1)
        out[d["challenge_id"]] = tuple(
            tuple(LET[t] for t in q.replace("= 1", "").strip().split())
            for q in b.split(";"))
    return out

board = load_board("research/acc/sac/stable_ac.jsonl")

baseline = {}   # what is already submitted, for scoring the delta
for line in open("/root/.claude/uploads/134a87db-34f4-5773-8170-2c301f6ca866/"
                 "54442fc9-acc-247-submission.txt"):
    line = line.strip()
    if line:
        c, r = line.split(":", 1)
        baseline[c.strip()] = json.loads(r.strip())

best = {}
def offer(cid, moves, src):
    if cid not in board:
        return
    if cid not in best or len(moves) < len(best[cid][0]):
        best[cid] = (list(moves), src)

for line in open("research/acc/sac/SAC_SUBMISSION_20260918.txt"):
    line = line.strip()
    if line:
        c, r = line.split(":", 1)
        offer(c.strip(), json.loads(r.strip()), "ac-cert")

if os.path.exists("research/acc/sac/COMPRESSED_276.jsonl"):
    for line in open("research/acc/sac/COMPRESSED_276.jsonl"):
        d = json.loads(line)
        offer(d["id"], d["moves"], "compress")

for f in glob.glob("research/acc/sac/shards/*.jsonl") + ["research/acc/sac/SWEEP_FULL.jsonl"]:
    if not os.path.exists(f):
        continue
    for line in open(f):
        line = line.strip()
        if line:
            d = json.loads(line)
            offer(d["id"], d["moves"], "sweep")

rows, rejected = [], []
for cid, (moves, src) in sorted(best.items()):
    ok, why = S.verify(board[cid], moves)
    if not ok:
        rejected.append((cid, why))
        continue
    prev = baseline.get(cid)
    if prev is None:
        kind, delta = "NEW", None
    elif len(moves) < len(prev):
        kind, delta = "IMPROVE", len(prev) - len(moves)
    else:
        continue                      # no gain over what is already submitted
    rows.append((cid, len(moves), kind, delta, src, moves))

with open("research/acc/sac/SAC_SUBMIT_FINAL.txt", "w") as f:
    f.write("# Stable AC submission. Verified against sac-r8-v1: every path\n")
    f.write("# replays to the empty presentation.\n")
    for cid, n, kind, delta, src, moves in rows:
        note = f"{kind}" + (f" -{delta}" if delta else "")
        f.write(f"{cid}: [{','.join(map(str,moves))}] # {note}, {src}\n")

imp = [r for r in rows if r[2] == "IMPROVE"]
new = [r for r in rows if r[2] == "NEW"]
print(f"SUBMITTABLE {len(rows)}   NEW {len(new)}   IMPROVE {len(imp)}   rejected {len(rejected)}")
if imp:
    print(f"  total moves saved on improved rows: {sum(r[3] for r in imp)}")
    print("  biggest gains:")
    for r in sorted(imp, key=lambda z: -z[3])[:10]:
        print(f"    {r[0]}  {len(baseline[r[0]])} -> {r[1]}  (-{r[3]})")
if new:
    print("  new rows:", ", ".join(r[0] for r in new[:20]))
if rejected:
    print("  REJECTED:", rejected[:5])
