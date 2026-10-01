SOL61 prepared handoff, Mad Hatters ACC, 2026-10-01.

Read SOL61_status_20261001T0217Z.txt first. This is a prepared and synthetically checked worker tool, not a passed ac-09409 control or a target-search result.

Contents:
sol61_ida.cpp: complete independent C++20 solver source.
sol61_ida: compiled Linux binary.
run_control.py: offline control runner; requires the exact official manifest blob and contains no known control route.
check_moves.py and check_bounded_search.py: synthetic validation scripts.
move_conformance_raw.json, synthetic_exact_raw.txt and synthetic_exact_summary.json: recorded validation evidence.
SEARCH_SCOPE.md: negative-result scope and pruning rationale.
official_provenance.json: pinned Git source hashes.
official/: verifier source, golden data and upstream license. The scored manifest is intentionally absent because it could not be retrieved faithfully.
source_scout/source_receipt.json: archive-source discovery diagnostics.

Build from the extracted package root:
g++ -O3 -std=c++20 sol61/sol61_ida.cpp -o sol61/sol61_ida

When the exact manifest is available, run from that root:
python sol61/run_control.py --manifest official/competition/tools/verifier/data/manifest.json

The runner refuses a manifest whose Git blob differs from accdb626ee08a06beea3f88dc7f351514c99eb27. It saves raw stdout/stderr, settings, a verifier receipt and the control report in sol61/runs/<UTC>/. It makes no network calls. Only a verifier-accepted candidate gets a lines file; the required control passes only with an independently found 23-move accepted path. No target-run wrapper or submission sender is included.

Target assignments are proposals until UPG-H confirms. Only UPG-H submits to SAIR. No target search may begin before the specified control passes.
