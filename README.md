<h1 align="center"><img src="assets/logo.png" alt="" width="64" style="vertical-align: middle;">&nbsp; CLAM — CLI on Mac</h1>


<p align="center">
  <a href="docs/README-zh.md">中文</a> | English
</p>

<p align="center">
  <strong>Give any AI Agent hands to control your Mac.</strong><br>
  Auto-discover apps. Generate CLI wrappers. Return structured JSON.
</p>

<br>

Your Mac has dozens of apps, but AI can't touch any of them. CLAM fixes that — it scans installed apps, generates typed CLI wrappers on the fly, and gives every command structured JSON output. No APIs, no manual adapters, no AppleScript headaches.

## Install

```bash
pip install clam-mac
```

> **`pip` not found or `externally-managed-environment` error?**
> macOS ships with `pip3` (not `pip`), and Python 3.12+ blocks direct installs. Use a virtual environment:
> ```bash
> python3 -m venv ~/clam-env
> source ~/clam-env/bin/activate
> pip install clam-mac
> ```
> Add `source ~/clam-env/bin/activate` to your `~/.zshrc` to make it permanent.

## Quick Start

```bash
clam scan                       # discover controllable apps
clam install music              # generate CLI wrapper (~10s)
clam-music play                 # play music
clam-music --json get-current-track   # → structured JSON
clam-music set-sound-volume 50  # set volume
```

Fuzzy matching built in: `chrome` → `google-chrome`, `word` → `microsoft-word`.

## Use with AI Agents

### OpenClaw

Install from [ClawHub](https://clawhub.ai):

```bash
clawhub install clam-mac
```

Or add to your Lobster pipeline:

```yaml
steps:
  - run: clam-music set-sound-volume 20
  - run: clam-music play
  - run: clam-finder open ~/Projects/current
```

Once installed, the AI auto-discovers apps via `clam scan`, installs wrappers, and executes commands.

### Claude Code (MCP)

```bash
pip install clam-mac
claude mcp add clam -- clam-mcp
```

Then just ask:

> "Set volume to 50 and tell me what song is playing"

### Any Other Agent

CLAM generates standard CLI tools. Anything that can call shell commands works:

```python
import subprocess, json
result = subprocess.run(["clam-music", "--json", "get-current-track"], capture_output=True, text=True)
track = json.loads(result.stdout)
```

## How It Works

CLAM auto-selects the best automation mode for each app:

| Mode | Mechanism | Apps | Commands |
|------|-----------|------|----------|
| **Full** | `.sdef` scripting definitions | Music, Finder, Chrome, Safari, Word | Dozens to hundreds |
| **UI Scripting** | Menu clicks via Accessibility | Figma, Slack, VS Code, Spotify | All menu items |
| **Basic** | macOS standard suite | DingTalk, WeChat, WPS | Activate, quit, open, version |

No configuration needed — `clam install` picks the right mode automatically.

## Commands

```bash
clam scan              # list controllable apps
clam install <app>     # generate + install CLI wrapper
clam info <app>        # show available commands
clam doctor <app>      # check command reliability
clam list              # list installed wrappers
clam remove <app>      # uninstall wrapper
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `clam-xxx` not found | `source .venv/bin/activate` or check your `PATH` |
| Permission denied | System Settings > Privacy & Security > Automation |
| UI Scripting error | System Settings > Privacy & Security > Accessibility |
| Only basic commands | App has no scripting support — basic mode is the max |

## License

[MIT](LICENSE)
