# Agent One handoff

## Goal

Continue the Grok-focused Omarchy usage plugin as **Omarchy Agent One**, expanding it to a nine-agent usage panel. Source repository: `git@github.com:calmasacow/omarchy-agent-one.git` (private). Plugin ID: `calmasacow.agent-one`.

## Requested agents

The target is a 3×3 selector for Codex, Claude, Grok, Google/Gemini, Cursor Agent, DeepSeek, OpenCode, Pi, and Qwen Code. Existing Codex, Claude, and Grok implementations are carried forward. The selector already uses three columns and intentionally excludes Fireworks so the target remains these nine agents.

Google/Gemini here means Google's Antigravity coding agent. Its installed executable is `agy`, but the button should be labeled Google or Gemini, not `agy`.

OpenCode and Pi can use many upstream model providers. Their local session/token statistics should be attributed to the OpenCode or Pi app; do not imply that those stats or any subscription limits are billed by OpenCode or Pi. Keep account quota and token usage as distinct sources.

## Current state

- The repository is a clean `main` branch and tracks `origin/main`.
- `README.md` and `TODO.md` describe the project and outstanding work.
- The local machine has the new plugin enabled as `calmasacow.agent-one`; the older `calmasacow.grok-usage` plugin is disabled and retained locally.
- `Main.qml`, `Agent.qml`, and `Panel.qml` contain the carried-forward UI and last-known-good Codex usage handling.
- `scripts/omarchy-agent-one-helper` handles the Grok collector, bounded JSON/text reads, safe usage-record discovery, snapshot loading, Codex limits-cache repair, DeepSeek Harness session projection totals and five-minute balance polling, plus Antigravity transcript counters and Gemini quota polling through `agy --print /usage`. Antigravity collection reads transcript timestamps and numeric usage counters only; no prompt/response content is retained. DeepSeek balance auth follows the active profile route and reads only the relevant local API key or account grant into memory; credentials never enter usage records, and requests are restricted to DeepSeek's HTTPS API or Platform origins. Session collection reads aggregate counters only and omits seeded fork projections to avoid counting inherited model calls twice.
- The manifest validates with `omarchy plugin validate .`.
- The Agent One preview image still shows the old Grok-only panel; replace it after the new selector/provider UI settles.

## Immediate work

Implement and integrate collectors for Cursor Agent (`cursor`), OpenCode (`opencode`), Pi (`pi`), and Qwen Code (`qwen`). Antigravity (`google`) now reads local token and prompt counters and Gemini quota windows via `agy`. DeepSeek (`deepseek`) reports all-time local session token totals, creation-day totals where known, and polls the account balance through its selected Harness OAuth or API-key route. Harness projections do not timestamp turns in older sessions, so their per-day token totals cannot currently be reconstructed.

Preserve cached values through empty/transient refreshes. Wire settings, normal/limits refresh, sync snapshots, display labels, and source/status explanations. Update `TODO.md` as each piece lands. After a coherent change, copy the project to the installed plugin directory and restart the Omarchy shell so the user can see the current iteration.
