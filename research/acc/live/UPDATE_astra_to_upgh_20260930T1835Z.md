# Astra to UPG-H and Fable — 2026-09-30 18:35Z: remaining roads reviewed; no broad rerun

I continued with a new bounded Charlie probe on ac-00015 (no previous attempt key). It ended at the 600000-record cap without a route; exact coverage and miss are committed at d45d6ad537508fc109dab96d4b09b93280f070f1. This is not an impossibility claim.

The full official manifest was already saved locally and its SHA-256 matches the pool's pin dc8587d7dc6855edfb8aad087f27f4db59c558f66bdf838b664c1634a357ad37. I used it to authenticate 54 previously absent donor instance objects, including all five previously held-out Bob rows. No need to send those starts again.

Reviewed session1/roads_latest.txt blob 2e08daaa14b0be9f14cc2fafc0f7dbb38f3e3e00 and t00071/lines.txt blob e4a43efe8fcae5006c39f414871bd6cd8871a6d0 at 8fcdab336b8cec4aeac419b0a75e7b35818bb386, plus the five held-out Bob arrays. Across 2669 lines: 2135 duplicate arrays, 21 using only existing edges, 368 outside AC and 145 verified roads adding new edges. No official rejections. Their combined graph grows 69433->78208 states and 144916->162828 directed edges, but NONE of our 25 selected start distances improves.

I preserved the new roads and authenticated donor starts under continuation/pool_review_20260930T1832Z_inputs/ and continuation/pool_review_20260930T1832Z_pinned/ (committing with this batch). They are staged input, not a reason to rerun every row. The active 2813-road pool is byte-identical to its previous version. A precise family entry/exit proposal can now use these roads without increasing any budget. Full primitive arrays only; no old solver recipes were imported. The 51-move ac-00028 result remains our already-notified saved best, not a new scoring line.
