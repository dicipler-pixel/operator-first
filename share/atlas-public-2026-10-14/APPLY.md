# Publish the Atlas to `dicipler-pixel/relational-atlas-lean`

Prepared 14 October 2026. **Applied the same day:** pushed to `relational-atlas-lean` main at commit `9357538` (209 files, the whole card edition including PNG renders). The instructions below remain for re-application. The automated session was not permitted to write private-repository
content into the public repository, so the payload is staged here. Everything below is the
author's own work (CC BY 4.0 text, MIT code); the live-competition section of the candidates file
is withheld in the public copy.

From a clone of `operator-first` on branch `claude/gallant-bardeen-0pgpae` (or `main` after
PR #71 merges) and a clone of `relational-atlas-lean`, with `$PRIV` and `$PUB` set to their paths:

    mkdir -p "$PUB/atlas"
    cp -r "$PRIV/tools/compound-eye/preserved/original_modular_release/preserved/atlas-cards/cards" "$PUB/atlas/cards"
    cp "$PRIV/atlas/ORIGINAL_ATLAS_METHOD_PLATES.md" "$PUB/atlas/"
    cp "$PRIV/atlas/ATLAS_VERSION_AUDIT_2026-10-14.md" "$PUB/atlas/"
    cp "$PRIV/share/atlas-public-2026-10-14/ATLAS_CANDIDATES_2026-10-14.public.md" "$PUB/atlas/ATLAS_CANDIDATES_2026-10-14.md"
    cp "$PRIV/share/atlas-public-2026-10-14/atlas_README.md" "$PUB/atlas/README.md"

Then paste `README_section_to_add.md` into `$PUB/README.md` before the "## How it is checked"
heading, append `PROVENANCE_section_to_add.md` to `$PUB/PROVENANCE.md`, and:

    cd "$PUB" && git add -A && git commit -m "Add the Atlas itself: 93-card edition, the moves, the version audit and candidates" && git push origin main

Size: the card edition is about 19 MB, of which 17 MB is the 90 PNG renders (`cards/png/`). Drop
that directory if the public repository should stay small; the HTML cards are complete without it.

The public workflow builds only the two Lean modules named in `scripts/config.json`, so adding
this folder does not change the proof check.
