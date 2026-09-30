ACC Master Mixer Studies v1 (private) - Jeromie Beasley, 2026-09-28
Open Compound_Eye_Matrix_Mixer_5_2_All_Eyes.html -> Eye mixer -> Import traces / recipe -> pick one *.traces.json.
Set Scale convention to "Display RMS normalization" (channels have different units).
Each file is one recorded, officially replayed AC path (12 recordings). 20 channels each:
  known eyes: harness v2 (lengths, Magnus 2/3, runs, down, collapse), image distance (p=5,7,11), Whitehead
  new eyes, each computed alone: SNELL speed, PLANAR pooled height + Mazur X, SMITH abelian (distance, angle),
  SMITH per line (r0 from vacuum x, r1 from vacuum y, via rho into SL2(Z); sees word order).
Pooled eyes (Snell, planar) re-learn from every recording when master_studies.py is rerun.
