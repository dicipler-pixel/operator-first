# Active recovered-helper lanes

Updated: 2026-09-30T14:48:00Z. User explicitly requested separate agents for Charlie, Bob and Kernel.

- Charlie revival: ac-00037, exact cap ladder from latest Charlie v11 orders (bounded adaptation, not a blanket cap certificate).
- Bob revival: ac-00012, cross-class generator transfer from latest Bob job3. Old reach2/3 block splice remains closed.
- Kernel revival: ac-00034, exact overlay of foreign verified known roads from Kernel's Sep30 06:00 handoff; closed doubling lead is not restarted.

Each first search: <=180 seconds, <=600000 admitted records, <=1024MiB. Sources/build/tests may proceed before search. No submissions or challenge API reads. Rows checked against all28 current WORKING files at3981da39 and changes throughc1c3f9d; the old sac-00034 lane explicitly released its rows. Current UPG-H lanes are disjoint.

Task contracts and leases: research/acc/harness/acc_synthesis/continuation/helper_handoffs.json and its local harness ledger. Model dispatch cap closes after these specifically authorized handoffs. Search claims expire at2026-09-30T15:05:00Z unless renewed. All output, including incomplete search bounds, is retained.

Charlie source-fit revision: ac-00028 deferred before any search because record-start=28. The same Sol worker now tests ac-00037 (record-start=0, start31 slightly above original30 slice). Previously completed route-local bridge does not cover this exact cap-ladder method. This is one worker continuation, not another model launch.
