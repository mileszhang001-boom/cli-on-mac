<h1 align="center"><img src="assets/logo.png" alt="" width="64" style="vertical-align: middle;">&nbsp; CLAM: Give AI Hands to Control Your Mac</h1>

<p align="center">
  <a href="https://pypi.org/project/clam-mac/"><img src="https://img.shields.io/pypi/v/clam-mac?color=blue" alt="PyPI"></a>
  <a href="https://pypi.org/project/clam-mac/"><img src="https://img.shields.io/pypi/pyversions/clam-mac" alt="Python"></a>
  <a href="https://github.com/mileszhang001-boom/cli-on-mac/blob/main/LICENSE"><img src="https://img.shields.io/pypi/l/clam-mac" alt="License"></a>
</p>

<p align="center">
  <a href="docs/README-zh.md">中文</a> | English
</p>

<p align="center">
  <strong>Your Mac has dozens of apps, but AI can't touch any of them.<br>
  CLAM auto-discovers apps, generates CLI wrappers, and lets any AI Agent control everything natively.</strong>
</p>

<p align="center">
  <a href="#-openclaw--lobster">OpenClaw Skill</a> · <a href="#-claude-code--mcp">Claude Code MCP</a> · <a href="#-quick-start-for-humans">CLI</a> · <a href="#-why-clam">Why CLAM</a>
</p>

Once installed, AI Agents can play music, operate Word, send emails, control Finder — using native app capabilities, no APIs, no manual adapter code.

## Why CLAM?

Existing approaches to let AI control Mac apps are either **too narrow** or **don't work at all**:

| Approach | Problem |
|----------|---------|
| Hand-built integrations (MCP/Skill) | Someone has to build one per app — most apps have none |
| Browser automation | Web only — can't touch Music, Finder, Word, or any native app |
| Let AI write AppleScript directly | Arcane syntax, scripts often error out, unstructured output |

**CLAM solves all of these at once:**

| Capability | What it does |
|------------|-------------|
| `clam scan` | AI auto-discovers all controllable apps on your Mac |
| `clam install <app>` | Generates a full CLI in 10 seconds — zero config, no pre-built adapters needed |
| `--json` output | Every command returns structured JSON for AI reasoning |
| `clam doctor` | Tells AI which commands are reliable before calling them |

## Install

```bash
pip install clam-mac
```

Or from source:

```bash
git clone https://github.com/mileszhang001-boom/cli-on-mac.git
cd cli-on-mac
pip install -e .
```

Then choose your AI Agent integration:

### OpenClaw / Lobster

Every `clam-<app>` is a standard shell command, usable as a Lobster pipeline step:

```yaml
# focus-mode.lobster
steps:
  - run: clam-music set-sound-volume 20
  - run: clam-music play
  - run: clam-finder open ~/Projects/current
```

Also works as an OpenClaw Skill — AI auto-discovers capabilities via `clam scan`, installs wrappers, and executes commands.

### Claude Code / MCP

```bash
claude mcp add clam -- clam-mcp
```

Done. Tell Claude Code:

> "Set volume to 50 and tell me what song is playing"

AI auto-scans apps, installs wrappers, and executes commands — you don't need to type a single command.

### Other Agent Frameworks

CLAM generates standard CLI tools. Any agent that can call shell commands can use them:

```python
# LangChain / AutoGPT / any framework
import subprocess, json
result = subprocess.run(["clam-music", "--json", "get-current-track"], capture_output=True, text=True)
track = json.loads(result.stdout)  # structured JSON, ready to use
```

## Quick Start (for Humans)

```bash
clam scan                              # see what's available
clam install music                     # install a wrapper
clam-music play                        # play
clam-music next-track                  # next track
clam-music set-sound-volume 80         # volume 80
clam-music get-current-track           # full track info (JSON)
```

## Three Modes, Covering Nearly All Apps

| Mode | How it works | Typical apps | Capability |
|------|-------------|-------------|-----------|
| **Full** | Parses .sdef scripting definitions | Music, Finder, Chrome, Word | Dozens to hundreds of commands |
| **UI Scripting** | Controls via menu clicks | Figma, Slack, VS Code, Spotify | Anything clickable in menus |
| **Basic** | macOS standard suite | DingTalk, WPS, WeChat | Activate / quit / open file / version |

The best mode is auto-selected during install — no manual configuration needed.

## Commands

```bash
clam scan              # scan controllable apps
clam install <app>     # install CLI (fuzzy match: chrome → google-chrome)
clam info <app>        # view capability details
clam doctor <app>      # check command reliability
clam list              # list installed wrappers
clam remove <app>      # uninstall

clam-<app>             # capability overview
clam-<app> api         # full API list
```

## FAQ

**Can't find `clam-xxx`?** — Run `source .venv/bin/activate`

**"permission denied"?** — System Settings > Privacy & Security > Automation — allow terminal to control the target app

**UI Scripting permission error?** — System Settings > Privacy & Security > Accessibility — allow terminal

**Only basic commands?** — Depends on the app developer. Most apps without scripting definitions only support basic mode.
