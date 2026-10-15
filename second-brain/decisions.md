# Decisions

Newest first. Each entry: date, what I chose, why, and what I rejected.

## 2026-10-14 — Plain Markdown folders instead of a notes app

- Chose: flat `.md` files in `notes/`, `people/`, `projects/`, with `CLAUDE.md` as the map.
- Why: Claude Code reads files on disk directly, and `CLAUDE.md` loads automatically at startup. No app format sits in between.
- Rejected: Obsidian or Notion as the primary store, because their formats add a layer between the agent and the text.
