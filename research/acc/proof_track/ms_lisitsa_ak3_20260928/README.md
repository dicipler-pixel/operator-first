# Lisitsa MS audit and AK(3) P-route replay (helper, 2026-09-28)

- `MS_Lisitsa_audit.md`: independent replay of Lisitsa's MS(3)-MS(9) fixed-word sequences (Zenodo 10.5281/zenodo.14647749,
  v2, MD5 345a7a0d3ddfffe395a52f8b0474c4f2): 16,232 labelled moves pass; an 11-move common finish; MS(9) = 8,634 moves.
- `ms_lisitsa_replay.py`: the checker (needs the Zenodo zip, not stored here).
- `ak3_p_to_ak3_replay.py`: replays the 53 h_i moves P -> AK(3) (Shehper et al. 3.5). Ordinary AC equivalence only;
  **not** a stable trivialization, **not** a submission. Replayed here: PASS.
- `AK3Audit.lean` (added 12:50Z from the user's Drive handoff folder, file 1qW1ROB-A5kRmQvATnlMxM9-rrjrJt96D; SHA-256
  `659dad3229b9b83483740cf97a5481d95283b2122482cdbc9d8ef9de77b92161`, matches the user's hash). Lean 4, self-contained
  (`import Init`, `by decide`). Proves `p_to_ak3` and `ak3_to_p` (67 elementary AC moves each way) and the *conditional*
  `ak3_stable_if_p_stable` (AK(3) is stably trivial **if** P is). It proves no stable trivialization. Not compiled here
  (no Lean toolchain); the 67-move certificate was replayed independently in Python: reaches AK(3).
- The Zenodo zip `MS_supplement_v2.zip`, Lisitsa's early AK(3) PDF (historical; its stable-triviality premise was
  withdrawn) and the MS preprint PDF are in the user's Drive folder "ACC replay Drive handoff"
  (1XF_fUNOgurSR3YaRnoH3iCGgKJkMExh1); not copied here.

Scoring relevance: the fixed-word family MS_n(w*) is our YXXyx chain (ac-01950 n5 ... ac-00106 n10; all k = 1).
Lisitsa's routes are far longer than the records (n=9: 8,634 vs 1,046), but they keep the BS relator fixed and the
working word short (peak 11-28 letters), unlike our beam routes that grow an x-run of length 2^n.
