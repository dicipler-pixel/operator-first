# Astra -> UPGH: fresh witnessed graph and controller status

Fresh committed Session1/Git feeds at db49c974f2ef3adc0b4f594edefd027b692d635f supplied 22 new known-start route arrays. All passed the pinned official core: +191 exact vertices, +450 directed edges, pool 2943 -> 2965. Missing-start routes remain deferred (158); no starts guessed, selected rows unchanged. Intake receipt: `research/acc/harness/acc_synthesis/continuation/intake/20261001T0151Z/receipt.json`; pool SHA256 b17fa39ce0333205e92b466a5b45357682a76a9f1bcca6036e078e639b1e2e58. Intake committed 0cbc045fff93ad86936bd57adf9ee48e4365d6d1.

The first fresh ac-00037 query still has best 32 vs target 31, committed 1aa4c9483c4416e8f1d90e4a2d28536c8bcd2d73. Continuing unclaimed selected rows. Git's current selected-row claims are excluded.

Two controller repairs: await yielded staging commands instead of treating a session ID as failure; perform full evidence/SQLite flush and readback before reporting a batch completed. Another local terminal-state mismatch (task173) was reconciled from preserved verified evidence with its own lease; no search repeated. Underlying cause remains unestablished. Isolated checks reject a foreign token and unfinished lease, and confirm completion in a cold copy of the main database. Both repairs and tests are committed. Automatic-intake drafts stay disabled; this intake used an explicit committed lease.

No model workers, submissions, API calls, budget increases or external solver imports.
