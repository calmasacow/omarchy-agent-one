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

- [x] Add OpenRouter selector and integrate Usage Plus balance, analytics, local rated spend, settings, refresh, and standard usage records.
- [x] Add Grok Bot's separate allowance and branded icon inside Grok and Overview using Omarchy's stock collector.
- [x] Add a permanent first Overview button, selected on every open, listing tracked providers without inventing missing quotas.
- [x] Let Overview grow to fit its contents, reserving 120 pixels above the screen bottom and scrolling only when needed.
- [x] Add regression checks for selector navigation, OpenRouter fallback preservation, account data exclusion from sync snapshots, and provider discovery on machines with more than 16 usage records.

- [x] Present the requested agents in balanced selector rows of up to three buttons.
- [x] Right-click a selector button to launch that agent through the stock `omarchy-agent`, even when it is not the default.
- [ ] Pass the agent with `omarchy-agent --agent` once Omarchy supports it, replacing the default-agent shim.
- [ ] Give each provider an accurate source/status label for local stats and account limits.
- [x] Preserve last good Google token and quota data when a scan or quota refresh has no data.
- [x] Integrate Google collector with Omarchy refresh, settings, and synchronized snapshots.
- [ ] Add broader regression coverage for every collector and panel behavior.
- [x] Replace the Grok-specific preview with the owner-provided Agent One overview screenshot.
- [x] Create the private GitHub repository and document how to clone it.
