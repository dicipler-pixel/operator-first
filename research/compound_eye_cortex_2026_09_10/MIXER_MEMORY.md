# Mixer Memory and Epiphany Replay

## Why this exists

A scientific instrument should learn from its misses. When a later result makes an earlier clue obvious, Compound Eye should be able to replay the old pass and answer four different questions rather than saying only “we missed it”:

1. Was the later-relevant eye registered then?
2. Was it actually executed and did it produce a usable record?
3. If it produced a record, did Cortex surface it to the foreground?
4. If it was surfaced or combined, did the mixer hide it through cancellation, scale collapse, or repeated lineage?

The existing full-retina ledger already records every registered eye version on every pass, including `NOT_ATTEMPTED`, and already distinguishes `SEEN_BUT_NOT_SURFACED`, blocked, errored, inapplicable, and not-yet-registered cases. `mixer_memory.py` adds the missing combination history.

## Rule: source first, picture second

A composite never replaces the native eye rows. Every mixer trial stores:

- the enabled eye set;
- the surfaced/foreground eye set;
- explicit routing reasons when supplied;
- control parameters;
- every native scalar source row used in the composite;
- eyes that were enabled but produced no recorded output;
- the compatibility groups used to make the picture;
- source hashes and a trial hash;
- optional append-only-style hash-chained trial history.

The foreground is therefore only a view. It is never deletion.

## Compatibility contract

The generic finite mixer only summarizes scalar observations that match on:

`channel + units + scope`

Scale is intentionally kept visible rather than silently normalized away. A group spanning multiple scales is marked `MIXED_SCALE` and becomes `OVERLAY_ONLY`.

The generic layer currently detects three exact structural risks:

- `SIGN_CANCELLATION` — opposite-signed source contributions can disappear in an aggregate;
- `SHARED_LINEAGE` — repeated implementation/dependency lineage can look like independent confirmation;
- `MIXED_SCALE` — collapsing resolution levels can erase a scale-dependent effect.

The output also reports the largest leave-one-eye-out change in the descriptive mean. This is an influence diagnostic, not a truth weight.

## Epiphany replay

After a later discovery, supply the eye refs and/or channels now known to matter. The replay reports whether each older trial suffered from:

- `ATTENTION_MISS`;
- `ENABLED_BUT_NO_RECORDED_OUTPUT`;
- `SEEN_BUT_NOT_SURFACED`;
- `FUSION_SIGN_CANCELLATION`;
- `FUSION_SHARED_LINEAGE`;
- `FUSION_MIXED_SCALE`;
- or `VISIBLE_IN_REPLAY`.

This does not rewrite history. An eye that was not run is still not evidence. The later relevance relation is used only to diagnose the earlier sensing/routing/fusion process.

## How to combine many eyes without losing the whole picture

The default strategy should be hierarchical rather than one giant average:

1. preserve all native rows;
2. group only compatible channels;
3. overlay first;
4. summarize only when the overlay shows no structural distortion flag;
5. keep independent lineage counts visible;
6. run leave-one-eye-out views for influential channels;
7. keep scale layers separate until a cross-resolution test shows that reduction is safe;
8. store every mixer configuration as a replayable trial;
9. after a useful discovery, replay prior trials and update the routing/fusion policy from the diagnosed miss.

This turns the mixer itself into an object of experiment. We can learn which combinations expose structure and which combinations wash it out.

## Current finite control

`test_mixer_memory.py` includes a deliberately bad phase composite with opposite signs, shared lineage and mixed scales. The correct behavior is not to average it away: the mixer marks all three risks and requires overlay-first inspection. The same test verifies seen-but-not-surfaced replay, not-attempted replay, source-row hashing, mixer-history chaining, and refusal of malformed or tampered records.

These are meta-layer controls only. They do not certify any scientific theorem or physical identification.
