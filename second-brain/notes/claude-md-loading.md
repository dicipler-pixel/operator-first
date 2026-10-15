# How Claude Code loads CLAUDE.md

When Claude Code starts, it reads `CLAUDE.md` from the folder it was opened in and from each parent folder above it. Their contents go into the session's instructions before the first message, so there's no need to tell it to "read the map".

## Details

- Inside `CLAUDE.md`, a line like `@MEMORY.md` imports that file's contents too. Imports always cost context, so keep them to a few small files.
- A `CLAUDE.md` in a subfolder loads only when Claude works with files in that subfolder.
- Because parent folders also load, a brain kept inside another project inherits that project's `CLAUDE.md` / `AGENTS.md`. Give the brain its own folder or repo so the instructions don't mix.
- Other agents don't read `CLAUDE.md` automatically. Point them at it, or copy it to `README.md` / `AGENTS.md`.

## Sources

- Claude Code memory docs: https://code.claude.com/docs/en/memory
- Tested in this repo on 2026-10-14 (see `projects/second-brain-setup.md`).

Updated: 2026-10-14
