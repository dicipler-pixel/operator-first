# The Atlas console

Published screen: the ten controls over the event ledger.

  `console_v1.html`   the page as published
  `snapshot_v1.json`  the ledger export it reads (generated, not authored)

The snapshot is a DERIVED VIEW. `ledger/events/stream_v1.jsonl` is the record;
this file is regenerated from it and may be deleted and rebuilt at any time.
Regenerate with the exporter in the session notes, then republish the page to
the same artifact URL.

## What the screen can and cannot do

It reads a snapshot. It is not live, so an item recorded in the repository
after the last export does not appear until the snapshot is regenerated.

`Record Move` and `Attach Evidence` write to the artifact's own shared store,
not to `stream_v1.jsonl`. Those writes are real and durable, and they are NOT
in the hash chain until they are read back and appended. Until that sync runs,
the two records disagree, and the screen says so rather than implying one
record.

`Start Mixer Run` and `Replay Run` deliberately do nothing. Runs execute
against the frozen `mixer_core.js` and the official SAIR verifier, which live
in the repository. A button here that claimed to start a run would be claiming
a computation that never happened.

`Find Prior Work` searches what has been indexed into the ledger by
`tools/acc/index_sources_v1.py`. Entries carry `seen`: `full` means this
process opened it, `listing-only` means it was seen in a listing and is a
pointer, not a reading.

`Ask What Comes Next` sends this item's chain to Claude and requires seq
citations. Its output is labelled PREDICTION on the page and in the prompt.
