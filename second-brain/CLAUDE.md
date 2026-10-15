# Second brain — map

This folder is a personal knowledge base made of plain Markdown files.
You (Claude) are its librarian: find things, answer from them, and file new things in the right place.

Always-loaded context (keep this list short):

@MEMORY.md

## Where things live

| Path | What goes there | One file per |
|---|---|---|
| `notes/` | Facts, explanations, how-tos, things learned | topic |
| `people/` | Contacts and organisations: who they are, how we met, meeting summaries | person or company |
| `projects/` | What I'm working on: status, where I stopped, next steps | project |
| `MEMORY.md` | Core long-term facts about me and how I like to work (loaded every session) | — |
| `LEARNINGS.md` | Lessons learned, mistakes not to repeat | — (one bullet each) |
| `decisions.md` | Dated log of choices and why I made them | — (one entry each) |

If a topic grows too big for one file, give it its own folder (for example `notes/tax/`) and add a row to the table above.

## Naming rules

- One file = one topic. Never put unrelated things in the same file.
- Name the file after its topic: `tax-policy.md`, `ivan-petrov.md`, not `note-12.md`.
- Lowercase letters, digits and hyphens only, ending in `.md`.
- Before creating a file, check whether one already exists for that topic. If so, update it instead.

## When I ask a question

1. Use the table above to pick the folder, then list it and open the likely files. Search file contents if the name doesn't make it obvious.
2. Answer from what the files say and cite the path of every file you used, e.g. (`people/ivan-petrov.md`).
3. If the answer isn't in the brain, say "Not in the second brain" and stop there. You can add general knowledge afterwards, but label it clearly as not coming from my files.
4. If two files disagree, point that out. Don't silently pick one.

## When I tell you something to remember

- Put it in the right file, using the shapes below. Create the file if the topic is new.
- Add `Updated: YYYY-MM-DD` at the bottom of any file you change.
- Decisions go at the top of `decisions.md`, newest first. Lessons go in `LEARNINGS.md`.
- Change `MEMORY.md` only for durable, core facts. It loads every session, so keep it under about 50 lines.
- Afterwards, tell me which files you created or changed.

## File shapes

Note (`notes/<topic>.md`):

```markdown
# <Topic>
<Two or three sentence summary.>
## Details
- ...
## Sources
- <where this came from>
```

Person (`people/<first-last>.md` or `people/<company>.md`):

```markdown
# <Name>
- Who: <role, organisation>
- How we met: <...>
- Contact: <...>
## Meetings
### YYYY-MM-DD
- ...
```

Project (`projects/<project>.md`):

```markdown
# <Project>
- Status: active | paused | done
- Last stopped at: <...>
## Next steps
- [ ] ...
## Log
- YYYY-MM-DD: ...
```
