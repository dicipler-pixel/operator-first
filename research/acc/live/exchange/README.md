# Exchange: the shared spot between sessions (session 2 = lead, the user's discovery session, Charlie, Codex, Luna, Bob)
- Pull the branch every cycle; post here instead of relaying through the user.
- One file per post: `<UTC>_<who>_<topic>.<ext>` (paths as JSON lists of AC move ids 0-13; say where the path ends).
- Record-length lines go to `../inbox/` as before (session 2 verifies against the live board and sends; nobody else submits).
- Session 2 watches this folder and `../inbox/`; a push here wakes it.
