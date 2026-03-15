"""English strings for CLAM CLI."""

STRINGS: dict[str, str] = {
    # ── CLI group ───────────────────────────────────────────────────────────────
    "cli.help_json": "Output as JSON for AI tools",
    "cli.description": "Scan your Mac, discover AI-controllable apps, generate CLI interfaces.",

    # ── scan ────────────────────────────────────────────────────────────────────
    "scan.help": "Scan local scriptable apps",
    "scan.scanning": "Scanning local apps…",
    "scan.no_apps": "No scriptable apps found",
    "scan.done": "Scan complete",
    "scan.found": "Found {count} controllable apps",
    "scan.hint": "Try: clam install music  |  Details: clam info music",

    # ── install ─────────────────────────────────────────────────────────────────
    "install.help": "Install CLI wrapper for an app",
    "install.probing_menus": "Probing {name} menu structure…",
    "install.mode.full": "",
    "install.mode.ui": " (UI Scripting mode)",
    "install.mode.basic": " (basic mode)",
    "install.generating": "Generating CLI wrapper for {name}{mode}…",
    "install.gen_failed": "Failed to generate wrapper: {error}",
    "install.installing": "Installing clam-{app_id}…",
    "install.pip_failed": "pip install failed",
    "install.sdef_failed": "Failed to parse sdef: {error}",
    "install.success_full": "{name} installed → [bold]{ep}[/bold]",
    "install.success_basic": "{name} installed → [bold]{ep}[/bold]  [dim](basic mode)[/dim]",
    "install.success_ui": "{name} installed → [bold]{ep}[/bold]  [dim](UI Scripting mode)[/dim]",
    "install.cmd_prop": "Commands: {cmds}  |  Properties: {props}",
    "install.menu_cmd": "Menu commands: {menus}  |  Basic commands: 6",
    "install.quickstart": "Quick start:",
    "install.activate_hint": "Activate window",
    "install.version_hint": "View version",
    "install.quit_hint": "Quit app",
    "install.view_summary": "View capability summary",
    "install.view_api": "View full API",
    "install.nested_count": "  |  Nested objects: {count}",
    "install.ai_title": "AI tool integration:",
    "install.ai_configured": "Configured. AI can directly invoke all [cyan]{ep}[/cyan] commands in terminal.",
    "install.ai_guide": "View AI integration guide: [dim]clam --json info {app_id}[/dim]",

    # ── list ────────────────────────────────────────────────────────────────────
    "list.help": "List installed wrappers",
    "list.empty": "No wrappers installed, run [bold]clam scan[/bold] to see available apps",
    "list.title": "Installed Wrappers",
    "list.col.app": "App",
    "list.col.entry": "Entry Command",
    "list.col.commands": "Commands",
    "list.col.properties": "Properties",
    "list.col.installed_at": "Installed At",

    # ── info ────────────────────────────────────────────────────────────────────
    "info.help": "View an app's command and property list",
    "info.help_detail": "Most critical for AI agent integration — agent calls clam info <app> --json\nto get the capability list, then calls clam-<app> <command>.",
    "info.installed": "Installed",
    "info.not_installed": "Not installed",
    "info.entry": "Entry:",
    "info.cmd_prop": "Commands: {cmds}  |  Properties: {props}",
    "info.nested": "  |  Nested objects: {count}",
    "info.tbl.commands": "Commands",
    "info.tbl.name": "Name",
    "info.tbl.description": "Description",
    "info.tbl.params": "Params",
    "info.tbl.properties": "Properties (get/set)",
    "info.tbl.prop_name": "Property",
    "info.tbl.access": "Access",
    "info.tbl.type": "Type",
    "info.tbl.prop_desc": "Description",
    "info.nested_title": "{name} ({class_name}) properties",
    "info.tbl.command": "Command",
    "info.compound_cmd": "Compound command: get-{name} → JSON",

    # ── doctor ──────────────────────────────────────────────────────────────────
    "doctor.help": "Check command reliability (parameter type analysis)",
    "doctor.title": "{name} command reliability check",
    "doctor.supported": "✓ {n} / {total} commands fully supported",
    "doctor.unsupported": "⚠ {n} commands have complex parameter types (may not work)",

    # ── remove ──────────────────────────────────────────────────────────────────
    "remove.help": "Uninstall an app's CLI wrapper",
    "remove.not_found": "Installed wrapper not found: {name}",
    "remove.removing": "Uninstalling clam-{app_id}…",
    "remove.success": "Uninstalled clam-{app_id}",

    # ── lang ────────────────────────────────────────────────────────────────────
    "lang.current": "Current language: {lang}",
    "lang.switched": "Language set to: {lang}",

    # ── mcp-setup ─────────────────────────────────────────────────────────────
    "mcp.checking": "Checking Claude Code installation…",
    "mcp.no_claude": "Claude Code (claude) not found on PATH.\nInstall it first: https://claude.ai/download",
    "mcp.registering": "Registering clam MCP server (user scope)…",
    "mcp.success": "clam MCP server registered globally.\nRestart Claude Code to activate. All clam commands are now available to AI.",
    "mcp.already": "clam MCP server is already registered.",
    "mcp.failed": "Registration failed: {error}",
    "mcp.removed": "clam MCP server unregistered.",
    "mcp.not_registered": "clam MCP server is not registered.",

    # ── errors ──────────────────────────────────────────────────────────────────
    "err.app_not_found": "App not found: {name}, did you mean: {suggestions}",
    "err.app_not_found_generic": "App not found: {name}, run clam scan to see available apps",

    # ── output ──────────────────────────────────────────────────────────────────
    "output.error": "Error:",
    "output.none": "(none)",

    # ── categories ──────────────────────────────────────────────────────────────
    "cat.office": "Office",
    "cat.design": "Design",
    "cat.media": "Media",
    "cat.browser": "Browser",
    "cat.communication": "Communication",
    "cat.productivity": "Productivity",
    "cat.development": "Development",
    "cat.system": "System",
    "cat.tools": "Tools",
    "cat.other": "Other",

    # ── auto-describe capabilities ──────────────────────────────────────────────
    "cap.playback": "Playback control",
    "cap.track_switch": "Track switching",
    "cap.navigation": "Page navigation",
    "cap.messaging": "Messaging",
    "cap.search": "Search",
    "cap.import_export": "Import/export",
    "cap.build_run": "Build & run",
    "cap.start_stop": "Start/stop control",
    "cap.scriptable": "Scriptable operations",
    "join.comma": ", ",

    # ── app descriptions ────────────────────────────────────────────────────────
    # Media
    "app.desc.music": "Play/pause, track switching, volume, track info",
    "app.desc.tv": "Video playback, episode switching, volume, playlists",
    "app.desc.quicktime-player": "Video playback, screen recording, audio recording, export",
    "app.desc.garageband": "Music production preview",
    "app.desc.photos": "Photo import/export, album management, slideshows",
    "app.desc.spotify": "Playback control, track switching, playlists, volume",
    "app.desc.qqmusic": "Playback control, track switching, playlist management",
    # Browser
    "app.desc.google-chrome": "Open pages, manage tabs, page navigation",
    "app.desc.safari": "Open pages, manage tabs, bookmarks, reading list",
    "app.desc.arc": "Open pages, manage tabs, page navigation",
    "app.desc.doubao": "Open pages, manage tabs, bookmark operations",
    # Office
    "app.desc.microsoft-word": "Document editing, formatting, tables, batch layout",
    "app.desc.microsoft-excel": "Spreadsheets, charts, formulas, data processing",
    "app.desc.microsoft-powerpoint": "Slide creation, animations, presentation control",
    "app.desc.microsoft-outlook": "Email, calendar, contacts",
    "app.desc.keynote": "Slide creation, export, presentation control",
    "app.desc.pages": "Document editing, layout, tables, export",
    "app.desc.numbers": "Spreadsheets, row/column operations, sorting, export",
    "app.desc.notion": "Document editing, knowledge base, project management",
    "app.desc.obsidian": "Note editing, bidirectional links, knowledge graph",
    # Productivity
    "app.desc.mail": "Send email, search, mailbox management",
    "app.desc.calendar": "Create/query events, view switching",
    "app.desc.contacts": "Contact management, search",
    "app.desc.messages": "Send messages",
    "app.desc.notes": "Create/search/edit notes",
    "app.desc.reminders": "View reminders, to-do management",
    "app.desc.ticktick": "Task queries, add to-dos, Pomodoro timer",
    # Communication
    "app.desc.telegram": "Send/receive messages, group management",
    "app.desc.wechat": "Send/receive messages, file transfer",
    "app.desc.qq": "Send/receive messages, file transfer",
    "app.desc.dingtalk": "Send/receive messages, approvals, attendance",
    "app.desc.lark": "Send/receive messages, document collaboration, calendar",
    "app.desc.discord": "Send/receive messages, voice channels",
    "app.desc.slack": "Send/receive messages, channel management, integrations",
    "app.desc.zoom": "Video conferencing, screen sharing",
    # Design
    "app.desc.figma": "Object operations, text layout, vector editing, layer management",
    # Development
    "app.desc.xcode": "Project building, running, testing, debugging",
    "app.desc.visual-studio-code": "Code editing, terminal, extensions, debugging",
    "app.desc.cursor": "AI code editing, terminal, debugging",
    # System
    "app.desc.finder": "File management, window views, Go to folder, tags",
    "app.desc.terminal": "Run scripts, window settings",
    "app.desc.system-settings": "View and modify system settings",
    "app.desc.shortcuts": "Run shortcuts",
    # Tools
    "app.desc.amphetamine": "Anti-sleep control, session management",
    "app.desc.flow": "Focus timer, Pomodoro, phase control",
    "app.desc.the-unarchiver": "File decompression",
    "app.desc.bluetooth-file-exchange": "Bluetooth file transfer",
    "app.desc.screen-sharing": "Remote screen sharing",
    "app.desc.console": "System log viewer",
    "app.desc.clashx-pro": "Network proxy, rule switching",
    "app.desc.chatgpt-atlas": "AI conversations",

    # ── template strings (baked at install time) ────────────────────────────────
    # Shared
    "tpl.capabilities": "Core capabilities:",
    "tpl.quickstart": "Quick start:",
    "tpl.view_api": "View full API (for AI tools):",
    "tpl.view_api_basic": "View full API:",
    "tpl.api_docstring": "View full API list (for AI tools)",
    "tpl.api_docstring_basic": "View full API list",
    "tpl.basic_controls_label": "Basic controls:",
    "tpl.basic_info_label": "Basic info:",
    "tpl.action_commands": "Action commands:",
    "tpl.properties_getset": "Properties (get/set):",
    "tpl.prop_suffix": "properties:",
    "tpl.get_all_json": "Get all properties (JSON)",
    "tpl.writable_prefix": "writable: set-",
    "tpl.writable_label": "writable",

    # Full mode summary
    "tpl.summary_full": "clam-{app_id} — CLI control for {app_name}",
    "tpl.cap_execute": "Execute",
    "tpl.cap_rw": "Read/write state",
    "tpl.unit_commands": "commands",
    "tpl.unit_properties": "properties",
    "tpl.unit_writable": "writable",
    "tpl.deep_access": "deep properties accessible",
    "tpl.colon_sep": ": ",
    "tpl.join_sep": ", ",
    "tpl.read_prefix": "Read ",
    "tpl.set_prefix": "Set ",
    "tpl.get_all_info": "Get all {name} info",

    # Basic mode
    "tpl.summary_basic": "clam-{app_id} — CLI control for {app_name} (basic mode)",
    "tpl.basic_controls_desc": "Basic controls    Activate window, quit app, open file",
    "tpl.basic_info_desc": "Basic info    App name, version, window state",
    "tpl.no_sdef_basic": "This app has no scripting interface, only standard macOS commands available.",

    # UI mode
    "tpl.summary_ui": "clam-{app_id} — CLI control for {app_name} (UI Scripting mode)",
    "tpl.basic_controls_ui": "Basic controls    Activate window, quit app, open file",
    "tpl.basic_info_ui": "Basic info    App name, version, window state",
    "tpl.no_sdef_ui": "This app has no scripting interface, controlled via menu clicks.",
    "tpl.accessibility_warning": "Requires Accessibility permission (System Settings > Accessibility).",
    "tpl.unit_ops": "operations",

    # Command docstrings (baked into generated wrappers)
    "tpl.activate_doc": "Activate window",
    "tpl.quit_doc": "Quit app",
    "tpl.open_doc": "Open file with this app",
    "tpl.get_name_doc": "Get app name",
    "tpl.get_version_doc": "Get version",
    "tpl.get_frontmost_doc": "Check if frontmost",
    # Command output messages
    "tpl.activated_msg": "{app_name} activated",
    "tpl.quit_msg": "{app_name} quit",
    "tpl.opened_msg": "Opened {filepath} with {app_name}",
    # API list labels
    "tpl.activate_api": "Activate window",
    "tpl.quit_api": "Quit app",
    "tpl.open_api": "Open file with this app",
    "tpl.name_api": "App name",
    "tpl.version_api": "Version",
    "tpl.frontmost_api": "Is frontmost window",
    "tpl.path_arg": "<path>",
}
