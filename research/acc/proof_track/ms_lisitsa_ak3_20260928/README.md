# Lisitsa MS audit and AK(3) P-route replay (helper, 2026-09-28)

- `MS_Lisitsa_audit.md`: independent replay of Lisitsa's MS(3)-MS(9) fixed-word sequences (Zenodo 10.5281/zenodo.14647749,
  v2, MD5 345a7a0d3ddfffe395a52f8b0474c4f2): 16,232 labelled moves pass; an 11-move common finish; MS(9) = 8,634 moves.
- `ms_lisitsa_replay.py`: the checker (needs the Zenodo zip, not stored here).
- `ak3_p_to_ak3_replay.py`: replays the 53 h_i moves P -> AK(3) (Shehper et al. 3.5). Ordinary AC equivalence only;
  **not** a stable trivialization, **not** a submission. Replayed here: PASS.
- `AK3Audit.lean`: self-contained Lean 4 (imports only Init). Checks the P <-> AK(3) leg and a *conditional* stable transfer;
  proves no stable trivialization. SHA-256 659dad3229b9b83483740cf97a5481d95283b2122482cdbc9d8ef9de77b92161 (matches the
  helper). Not compiled here: no Lean toolchain in this container.
- `MS_supplement_v2.zip`: Lisitsa's Zenodo v2 archive, MD5 345a7a0d3ddfffe395a52f8b0474c4f2 (matches Zenodo).
  `python3 ms_lisitsa_replay.py MS_supplement_v2.zip` here: **ALL PASS, 16,232 labelled moves**, common 11-move tail
  verified; shared tails 35 / 134 / 369 / 893 / 1,590 / 4,063 moves (n=4..9 vs n-1); no file passes through a conjugate
  of the previous start.
- Source: Drive handoff folder "ACC replay" (1XF_fUNOgurSR3YaRnoH3iCGgKJkMExh1), copied 2026-09-28 12:47Z.
- The early AK(3) PDF in that folder is historical: its stable-triviality premise was later corrected.

Scoring relevance: the fixed-word family MS_n(w*) is our YXXyx chain (ac-01950 n5 ... ac-00106 n10; all k = 1).
Lisitsa's routes are far longer than the records (n=9: 8,634 vs 1,046), but they keep the BS relator fixed and the
working word short (peak 11-28 letters), unlike our beam routes that grow an x-run of length 2^n.
