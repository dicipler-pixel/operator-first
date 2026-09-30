"""Run the pinned official SAIR verifier on JSON lines from stdin.

usage: python3 official_driver.py SAIR_DIR < items.jsonl
input line:  {"cid": "ac-00001", "moves": [...]}
output line: the official verify_challenge verdict plus "cid".

This file only calls the official library API (the same function the official
CLI uses for each line). It never edits a verdict. upgh verifies the pinned
file hashes before it starts this process.
"""
import json
import sys
from pathlib import Path

sair = Path(sys.argv[1])
sys.path.insert(0, str(sair / "competition" / "tools"))
import verifier  # noqa: E402
from verifier import specs  # noqa: E402

manifest = json.loads((sair / "competition/tools/verifier/data/manifest.json").read_text(encoding="utf-8"))
problems = specs.check_move_specs(manifest.get("move_specs"))
if problems:
    print(json.dumps({"fatal": "manifest move_specs do not match the frozen tables",
                      "problems": problems}))
    sys.exit(3)
index = {c["challenge_id"]: c for c in manifest["challenges"]}
limits = manifest["limits"]
for line in sys.stdin:
    if not line.strip():
        continue
    item = json.loads(line)
    challenge = index.get(item["cid"])
    if challenge is None:
        verdict = {"ok": False, "code": "E_UNKNOWN_CHALLENGE"}
    else:
        verdict = dict(specs.verify_challenge(challenge, item["moves"],
                                              challenge["move_spec_version"], limits))
    verdict["cid"] = item["cid"]
    verdict["verifier_version"] = verifier.__version__
    print(json.dumps(verdict), flush=True)
