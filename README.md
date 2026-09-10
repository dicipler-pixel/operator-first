# Compound Eye Companion 1.1 — Clean Share Build

This branch is the **shareable clean edition** of Compound Eye Companion. It contains no Jeromie Beasley research datasets, private theorem corpus, saved runs, API keys, account connections, or owner-method pack.

## Download

Use GitHub's branch download, extract it, then run `START_WINDOWS.bat` on Windows or `python3 START.py` on macOS/Linux.

Python 3.10+ is required. The base workbench uses only the Python standard library.

## What it does

- keeps theorem, note, matrix, sample, and custom-eye records in a local workspace;
- runs several eyes on the same identified object and returns a combined whole-view report;
- offers a chat-style request box that produces **proposed actions** for review before execution;
- has an optional OpenAI Responses API connector using the recipient's own `OPENAI_API_KEY` environment variable and chosen model;
- contains a bounded three-bundle phase/coupling laboratory for exploring exchange, directional bias, loss, and phase winding;
- exports the user's own workspace as JSON.

The assistant does not execute arbitrary Python, shell commands, or downloaded plugins. Uploaded theorem prose is `user_supplied_unverified`; a numerical pass is not a proof.

## Privacy

The default workspace is stored on the recipient's own computer. The OpenAI connector sends only the current chat request plus the compact workspace summary shown by the app. No API key is stored in the project file. Leave provider set to `offline` for no model-network calls.

## Creator

Compound Eye / Operator-First research programme — Jeromie N. Beasley. This clean distribution is intended as a reusable research instrument for other users with their own theorems and data.
