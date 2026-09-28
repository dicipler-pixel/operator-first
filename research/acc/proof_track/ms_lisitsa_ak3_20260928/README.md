# Lisitsa MS audit and AK(3) P-route replay (helper, 2026-09-28)

- `MS_Lisitsa_audit.md`: independent replay of Lisitsa's MS(3)-MS(9) fixed-word sequences (Zenodo 10.5281/zenodo.14647749,
  v2, MD5 345a7a0d3ddfffe395a52f8b0474c4f2): 16,232 labelled moves pass; an 11-move common finish; MS(9) = 8,634 moves.
- `ms_lisitsa_replay.py`: the checker (needs the Zenodo zip, not stored here).
- `ak3_p_to_ak3_replay.py`: replays the 53 h_i moves P -> AK(3) (Shehper et al. 3.5). Ordinary AC equivalence only;
  **not** a stable trivialization, **not** a submission. Replayed here: PASS.
- **Missing:** `AK3Audit.lean` (proves the P -> AK(3) route and a *conditional* stable transfer; not recompiled) and the
  Zenodo zip were sandbox links on the helper's side and did not arrive. Ask the helper to push them directly.

Scoring relevance: the fixed-word family MS_n(w*) is our YXXyx chain (ac-01950 n5 ... ac-00106 n10; all k = 1).
Lisitsa's routes are far longer than the records (n=9: 8,634 vs 1,046), but they keep the BS relator fixed and the
working word short (peak 11-28 letters), unlike our beam routes that grow an x-run of length 2^n.
