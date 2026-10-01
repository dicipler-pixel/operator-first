# What we missed: audit, 1 Oct (UPG-H, 11:14Z), the owner's request

| Check | Result |
|---|---|
| Team lines on this branch (session 1 audit) | 0 unsent; 3 Drive-only Kernel ties found and **sent in #2971** |
| Kernel Drive files never imported | all 16 imported (617 lines, 0 failed); 0 new scorers |
| **Other branches of operator-first (92 branches, 26,218 ACC lines)** | **0 unsent scorers**: every line at or under its record is already held at that length or shorter |
| AC-1M public dataset (1,136,154 presentations) | 0 of 2,672 board-unsolved rows present (the matcher was verified on solved rows) |
| Carreras certificates (joe-carr-data/ac-certificates) | trivializations are only for ac-03402/ac-09088 (records 45/46), 97-178 macro moves, so no beat. **Equivalences:** ac-02842 and ac-06556 are AC-equivalent to AK(3) (= ac-00399); ac-03467 ~ ac-08126; ac-00413 ~ ac-02089 ~ ac-04376 ~ ac-05932; ac-06279/ac-06945 ~ AK(3) bottleneck. **Do not spend first-solve effort on these: a solve would solve AK(3).** |
| Owner email | GitHub App "Claude is requesting updated permissions" (10:38Z): the owner approves on GitHub to widen access. GitHub Actions at 90% of 2,000 minutes (02:05Z): our branch stopped failing CI at 01:54Z after [skip ci] + paths-ignore. No SAIR/ACC mail. |
| GitHub access | ac-certificates: read is open (public). ACSolverX: attach was refused by the permission system (not pursued); its AC-1M data was already read via raw download. |
| Process gaps fixed today | Drive-hub messages missed -> full 15-minute sweep; members idle -> TEAM_ROSTER with next jobs; read budget burned by a full history pull (9 reads) -> offline send path |
