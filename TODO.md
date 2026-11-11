# Agent One TODO

## Provider support

- [x] Google Gemini via the installed Antigravity CLI (`agy`): aggregate local transcript token/prompt counters without reading content and refresh Gemini quota windows from `/usage` every five minutes.
- [ ] Cursor Agent: collect local usage and determine whether Cursor exposes account quota data through a supported local interface.
- [x] Read DeepSeek Harness session token-usage projections and show all-time local token/turn totals without reading prompts.
- [x] Poll DeepSeek balance every five minutes, selecting Harness OAuth or API-key auth according to the active model route; preserve the last good balance on failure and never sync credentials.
- [ ] Reconstruct per-day activity for DeepSeek sessions that span multiple dates; current projections expose all-time totals without per-turn timestamps.
- [ ] OpenCode: collect local session and token usage; keep upstream provider billing separate from OpenCode activity.
- [ ] Pi: collect local session and token usage; keep upstream provider billing separate from Pi activity.
- [ ] Qwen Code: collect local session and token usage and investigate first-party account quota availability.

## Panel and integration

- [x] Present the requested agents in balanced selector rows of up to three buttons.
- [ ] Give each provider an accurate source/status label for local stats and account limits.
- [x] Preserve last good Google token and quota data when a scan or quota refresh has no data.
- [x] Integrate Google collector with Omarchy refresh, settings, and synchronized snapshots.
- [ ] Add broader regression coverage for every collector and panel behavior.
- [ ] Replace the Grok-specific preview with an Agent One panel preview.
- [x] Create the private GitHub repository and document how to clone it.
