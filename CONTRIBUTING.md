# Contributing to CLAM

Thanks for your interest in CLAM! This guide will get you from zero to your first PR in under 10 minutes.

## The Easiest Way to Contribute: Add an App

CLAM's app catalog lives in `src/clam/mcp_server.py` inside `_APP_CATALOG`. Adding a new app means adding ~8 lines of Python.

### Step 1: Fork & Clone

```bash
git clone https://github.com/<your-username>/cli-on-mac.git
cd cli-on-mac
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

### Step 2: Find Your App's Info

```bash
# Check if the app has scripting definitions (sdef = full automation support)
ls /Applications/YourApp.app/Contents/Resources/*.sdef

# Get the exact bundle path
ls /Applications/ | grep -i "yourapp"
```

### Step 3: Add the Entry

Open `src/clam/mcp_server.py`, find `_APP_CATALOG`, and add your app:

```python
"your-app": {
    "display_name": "Your App",
    "names": ["your-app", "yourapp", "别名"],
    "keywords": ["what", "it", "does", "关键词"],
    "category": "one of: 媒体/浏览器/办公/效率/通信/系统/设计/开发",
    "description": "Brief description of what CLAM can do with this app",
    "bundle_hints": ["/Applications/Your App.app"]
},
```

**Field guide:**

| Field | What to put |
|-------|-------------|
| key | Lowercase, kebab-case (e.g. `google-chrome`) |
| `display_name` | Human-readable name |
| `names` | All names users might type — English, Chinese, abbreviations |
| `keywords` | What the app does, in both languages |
| `category` | Pick from: 媒体, 浏览器, 办公, 效率, 通信, 系统, 设计, 开发 |
| `description` | One line — what CLAM can automate |
| `bundle_hints` | Full path(s) to the `.app` bundle |

### Step 4: Test It

```bash
pytest tests/test_mcp_server.py -v
```

### Step 5: Submit a PR

```bash
git checkout -b add-your-app
git add src/clam/mcp_server.py
git commit -m "Add YourApp to app catalog"
git push origin add-your-app
```

Then open a PR on GitHub. That's it!

## Other Ways to Contribute

### Report a Bug

Open an issue with:
- What you ran (command or MCP tool call)
- What you expected
- What actually happened
- Your macOS version and Python version

### Improve Tests

```bash
# Run full test suite
pytest tests/ -v

# Run a specific test file
pytest tests/test_mcp_server.py -v

# Run with coverage (if installed)
pytest tests/ --cov=clam
```

We especially need tests for:
- UI Scripting mode apps (Spotify, Figma, VS Code)
- Error scenarios (app not installed, permission denied, timeout)
- Non-ASCII app names (WeChat, DingTalk)

### Improve Documentation

- Fix typos or unclear wording in README.md
- Add examples to docs/
- Translate docs to other languages

## Development Setup

```bash
git clone https://github.com/mileszhang001-boom/cli-on-mac.git
cd cli-on-mac
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest tests/ -v
```

**Requirements:** Python 3.10+, macOS (for sdef parsing and AppleScript execution)

## Code Style

- Follow existing patterns in the codebase
- Use type hints where possible
- Keep functions focused and under 50 lines when practical
- Bilingual comments are welcome (English + Chinese)

## Questions?

Open an issue or start a discussion on GitHub. We're happy to help!
