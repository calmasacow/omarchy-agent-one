# Agent One project instructions

Read `HANDOFF.md` and `TODO.md` before changing this project.

## Project conventions

- Keep the implementation compatible with Omarchy's agents usage-record format and the local Omarchy plugin manifest.
- Separate local session statistics from account quota data. Only display a quota or billing figure when its source and meaning are known.
- Open provider history, logs, and databases read-only. Never include account credentials, prompt text, or private usage records in the repository.
- Preserve last-known-good usage when refreshes return empty, incomplete, or temporarily unavailable data.
- Keep the nine selector IDs and labels documented in `README.md`; do not add unrelated providers to the selector.
- Work in the repository root, validate `manifest.json` with `omarchy plugin validate .`, and update `TODO.md` as work is completed.

## Current provider IDs

`claude`, `codex`, `grok`, `google`, `cursor`, `deepseek`, `opencode`, `pi`, and `qwen`.

The Google button may be labeled Google or Gemini. The active Google coding agent on the original machine is Antigravity, whose executable is `agy`; `agy` is the CLI name, not the agent name.
