# Omarchy Agent One

Usage dashboard for coding agents in Omarchy. It extends the Omarchy Agents panel with provider-specific usage and account limits where those can be read reliably.

**Plugin ID:** `calmasacow.agent-one`  
**Repository:** `omarchy-agent-one`  
**Author:** James Barnette  
**License:** MIT

## Supported agent roadmap

The target selector is a 3×3 grid for these nine agents:

1. Codex
2. Claude
3. Grok
4. Google Gemini (Antigravity CLI)
5. Cursor Agent
6. DeepSeek
7. OpenCode
8. Pi
9. Qwen Code

The existing Codex, Claude, and Grok usage panels are carried forward. Google Gemini support uses the installed Antigravity CLI (`agy`): token and prompt totals come from local transcript counters, while remaining Gemini weekly and five-hour quota comes from `agy /usage`. The collector reads timestamps and numeric counters only; prompt and response content is discarded. Quota is cached for five minutes. DeepSeek Harness contributes all-time local token and turn totals from its session usage projections. The collector reads aggregate counters only, never prompt text. Today's totals include sessions created today; the projections do not timestamp turns in older sessions, so their usage cannot be split by day. DeepSeek's balance is queried every five minutes through the credential route selected by the active Harness model configuration: the Harness OAuth grant uses DeepSeek Platform's account summary, and an API-key route uses DeepSeek's documented `/user/balance` endpoint. Credentials stay local and are never written to usage records or synced snapshots. Local token totals remain separate from account balance.

The provider selector balances rows with at most three buttons each. Four providers use two rows of two; seven use rows of three, two, and two; eight use rows of three, three, and two.

## Install

The GitHub repository is private while development continues. Clone it with GitHub SSH access:

```sh
git clone git@github.com:calmasacow/omarchy-agent-one.git
```

The plugin is still under development and is not yet a marketplace release.

## Usage

| Control | Action |
|---|---|
| Left-click | Open or close the usage panel |
| Right-click | Launch the default coding agent |
| Middle-click | Next agent |
| `h` / `l` | Switch agent |
| `r` or Enter | Refresh |
| Esc | Close |

## Development

Run the existing collector and panel checks with `test/run` when requested. The shared helper bounds local file reads and handles usage-record discovery; provider-specific collectors write JSON records to Omarchy's standard agents usage directory.

## License

MIT. Panel QML is adapted from Omarchy's first-party Agents plugin.
