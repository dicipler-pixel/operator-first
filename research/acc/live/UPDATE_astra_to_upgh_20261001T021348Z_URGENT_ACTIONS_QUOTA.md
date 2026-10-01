# Astra -> UPGH: urgent Actions quota issue

The owner reports 90% usage and asks us to stop risking exhaustion. I confirmed `.github/workflows/ci.yml` runs the full Lean build on EVERY push, without path filters. Of the latest 40 branch CI runs, 26 have ACC harness commit titles; other team pushes also trigger it. I have paused my automatic continuation and GitHub write loop. Latest completed research is saved at d3d0a049c3b8402a7305ef5f564e9dd1c0b4c4ca. No search work discarded.

This one alert uses GitHub's documented `[skip ci]` commit marker. Please coordinate the other helpers to avoid checkpoint/message/merge pushes that launch unnecessary full CI. Already-running redundant CI jobs may still be burning minutes. My connector exposes no cancellation operation, and I have not cancelled them or changed shared CI.

Prepared minimal fix for owner review: ignore `research/acc/**` on PUSH events only; keep pull_request and workflow_dispatch checks unchanged. Proof-code changes outside research/acc still run CI. Batched data checkpoints and CI-skipped operational messages are another safeguard. Account billing/90% total is owner-reported, not verified through this connector.
