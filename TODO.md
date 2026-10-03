# Agent One TODO

## Provider support

- [ ] Google Gemini via the installed Antigravity CLI (`agy`): discover token statistics and account quota data without invoking agent work.
- [ ] Cursor Agent: collect local usage and determine whether Cursor exposes account quota data through a supported local interface.
- [ ] DeepSeek: identify a first-party coding agent or account usage interface; avoid treating arbitrary API-key billing as subscription quota.
- [ ] OpenCode: collect local session and token usage; keep upstream provider billing separate from OpenCode activity.
- [ ] Pi: collect local session and token usage; keep upstream provider billing separate from Pi activity.
- [ ] Qwen Code: collect local session and token usage and investigate first-party account quota availability.

## Panel and integration

- [x] Present the nine requested agents in a stable 3-column selector grid.
- [ ] Give each provider an accurate source/status label for local stats and account limits.
- [ ] Preserve last good cached usage when a scan or quota refresh has no data.
- [ ] Integrate the provider collectors with Omarchy refresh, settings, and synchronized snapshots.
- [ ] Add focused collector and panel regression coverage.
- [ ] Replace the Grok-specific preview with an Agent One panel preview.
- [x] Create the private GitHub repository and document how to clone it.
