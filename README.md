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

The existing Codex, Claude, and Grok usage panels are carried forward. Provider collectors will report local usage independently of account quota data; quota bars are shown only when an official or otherwise reliable account source is available.

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
