# ACC run decoder — summary (submission:training_424_finished.txt)

Decoder: acc_run_decoder v2 · replay kernel: official SAIR verifier · schema: compound-eye-traces-v1

| quantity | value |
|---|---|
| runs decoded | 424 |
| verifier ok | 424/424 |
| abelian_ok == 1 at every step | 424/424 |
| n_moves | min 6 · q1 15 · median 23 · q3 40 · max 156 · mean 31.4 |
| initial_length | min 7 · q1 13 · median 14 · q3 16 · max 25 · mean 14.6 |
| max_length_reached − initial_length (growth before shrinking) | min 0 · q1 0 · median 0 · q3 0 · max 2 · mean 0.1 |
| step_of_max | min 0 · q1 0 · median 0 · q3 0 · max 13 · mean 0.4 |
| longest_plateau (consecutive delta_total == 0) | min 1 · q1 3 · median 5 · q3 7 · max 29 · mean 5.8 |

## Move class frequency by position in run

| class | first third | middle third | last third |
|---|---:|---:|---:|
| conjugate | 2667 | 2238 | 1216 |
| invert | 1048 | 947 | 903 |
| multiply | 862 | 1243 | 2183 |

Runs whose total length rose above the initial length at some step: 23/424.
dist_to_target is a proxy (0 only at the exact target); it is not a distance.
