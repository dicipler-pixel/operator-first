# Second brain starter

A ready-to-use version of the "Claude second brain" setup: plain Markdown files in a few folders, with a `CLAUDE.md` map that Claude Code loads automatically.

```
second-brain/
├── CLAUDE.md        ← the map Claude reads at startup (also imports MEMORY.md)
├── MEMORY.md        ← core facts, always in context
├── LEARNINGS.md     ← lessons learned
├── decisions.md     ← dated decision log
├── notes/           ← one file per topic
├── people/          ← one file per person or company
└── projects/        ← one file per project
```

## Use it

1. Copy this folder somewhere of its own, for example `~/second-brain`, or make it a separate private repo.
   Keep it out of other projects: Claude Code also loads `CLAUDE.md` / `AGENTS.md` from parent folders, so another project's instructions would mix in.
2. Open a terminal in the folder and run `claude`.
3. Talk to it:
   - "Remember that Ivan Petrov is the tax accountant I met at the meetup on Oct 3." → creates `people/ivan-petrov.md`
   - "What's the next step on the second brain project?" → reads `projects/`, answers, cites the file
   - "Log a decision: I'm using a private GitHub repo for backups because…" → adds an entry to `decisions.md`

Any text editor works for editing the files yourself. Nothing to install.

## Starter files

`people/example-person.md` is a format example. Delete it once you've added someone real.
The other files are real starting content you can keep or edit.
