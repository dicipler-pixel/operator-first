ACC Unsolved Data v1 (private) - Jeromie Beasley, 2026-09-28
eye_table_all_rows.csv : every eye at the start state of all 10,115 AC rows (solved + unsolved) with board record/teams.
   columns: lengths, longest runs, image distance (p=5,7,11 lower bound), Whitehead, Smith abelian,
   Smith per line (order-6 rho: has blind spots), Smith faithful (Sanov x->[[1,2],[0,1]], y->[[1,0],[2,1]]: no blind spots).
unsolved_ranked.json   : the 2,672 unsolved rows ranked by a model trained on solved rows (held-out Spearman 0.42,
   median error 20 moves). The short top of the list is Baumslag-Solitar-type pairs and AK(3)-class rows: not easy.
yyxxyx_descents.json   : recorded descents for MS(n, YYXXYx), n=4..10 (odd n drop by 2, even n do not).
studies/               : 18 Mixer 5.2 studies (Import traces / recipe, then Display RMS normalization), 22 channels.
