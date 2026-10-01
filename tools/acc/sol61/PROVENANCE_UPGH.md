# Sol 6.1 package (owner upload 1 Oct 2026, `SOL61_prepared_20261001T0217Z.zip`), imported by the UPG-H lead
Author: Sol 6.1 (the owner's outside model). Imported unchanged: source, scripts, validation evidence and docs. **Not imported:** the prebuilt binary
`sol61_ida` (UPG-H builds from source, portable flags) and the `official/` verifier copy (UPG-H uses its pinned copy at a0fd6e6; our manifest's Git blob is
`accdb626ee08a06beea3f88dc7f351514c99eb27`, the exact blob Sol 6.1 pinned). Build: `g++ -O3 -std=c++20 -march=x86-64-v2 tools/acc/sol61/sol61_ida.cpp -o <out>`.
Sol's rules carry over: the ac-09409 23-move control must pass before any target run; UPG-H is the only SAIR sender.
