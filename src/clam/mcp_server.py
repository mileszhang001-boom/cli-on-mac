"""CLAM MCP Server — 让 AI 通过 MCP 协议直接控制 macOS 应用。

Usage:
    clam-mcp              # 启动 MCP server (stdio 模式)

Claude Code 配置 (~/.claude.json):
    {
      "mcpServers": {
        "clam": { "command": "clam-mcp" }
      }
    }
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP

from clam.generator.applescript_gen import (
    check_command_support,
    generate_basic_wrapper,
    generate_ui_wrapper,
    generate_wrapper,
    get_ui_wrapper_info,
    get_wrapper_info,
)
from clam.generator.installer import install_wrapper
from clam.registry import registry
from clam.registry.registry import GENERATOR_VERSION
from clam.scanner.app_scanner import find_app, find_basic_app, scan_applications
from clam.scanner.menu_scanner import scan_menus
from clam.scanner.sdef_parser import parse_sdef

mcp = FastMCP(
    "clam",
    instructions=(
        "CLAM 是 macOS 所有应用的通用控制桥梁。"
        "当用户提到任何 Mac 应用时，不要说'没有该应用的 MCP'，不要直接写 AppleScript。"
        "正确工作流：clam_find_app(应用名) → clam_install(app_id) → clam_execute(app_id, 命令)。"
        "支持所有 Mac 应用：Music/音乐、Finder/访达、Mail/邮件、微信、QQ音乐、Chrome、Spotify 等。"
    ),
)

# ── App catalog for clam_find_app (static, no filesystem access) ─────────────
_APP_CATALOG: dict[str, dict] = {
    "music":                {"display_name": "Apple 音乐",   "names": ["music", "apple music", "苹果音乐", "itunes"],           "keywords": ["音乐", "播放", "歌曲", "play", "song", "听歌"],    "category": "媒体",  "description": "播放控制、切歌、音量调节、曲目查询",   "bundle_hints": ["/System/Applications/Music.app"]},
    "spotify":              {"display_name": "Spotify",      "names": ["spotify"],                                               "keywords": ["音乐", "播放", "podcast", "music", "play"],         "category": "媒体",  "description": "播放控制、切歌、播放列表、音量调节",   "bundle_hints": ["/Applications/Spotify.app"]},
    "qqmusic":              {"display_name": "QQ音乐",       "names": ["qqmusic", "qq音乐", "qq music", "腾讯音乐"],            "keywords": ["音乐", "播放", "歌曲", "music", "qq音乐"],          "category": "媒体",  "description": "播放控制、切歌、歌单管理",             "bundle_hints": ["/Applications/QQMusic.app"]},
    "neteasemusic":         {"display_name": "网易云音乐",   "names": ["neteasemusic", "网易云音乐", "网易云", "netease"],       "keywords": ["音乐", "播放", "网易", "music", "网易云"],          "category": "媒体",  "description": "播放控制、切歌、歌单管理",             "bundle_hints": ["/Applications/NeteaseMusic.app"]},
    "tv":                   {"display_name": "Apple TV",     "names": ["tv", "apple tv"],                                       "keywords": ["视频", "电影", "video", "movie"],                   "category": "媒体",  "description": "视频播放、切集、音量调节",             "bundle_hints": ["/System/Applications/TV.app"]},
    "quicktime-player":     {"display_name": "QuickTime",    "names": ["quicktime-player", "quicktime"],                        "keywords": ["视频", "录屏", "录音", "video", "screen"],          "category": "媒体",  "description": "视频播放、录屏、录音、导出裁剪",       "bundle_hints": ["/System/Applications/QuickTime Player.app"]},
    "photos":               {"display_name": "照片",         "names": ["photos", "照片"],                                       "keywords": ["照片", "相册", "photo", "album"],                   "category": "媒体",  "description": "照片导入导出、相册管理",               "bundle_hints": ["/System/Applications/Photos.app"]},
    "google-chrome":        {"display_name": "Chrome",       "names": ["google-chrome", "chrome", "谷歌浏览器", "谷歌"],        "keywords": ["浏览器", "网页", "标签", "browser", "web", "tab"],  "category": "浏览器","description": "打开网页、管理标签页、页面导航",       "bundle_hints": ["/Applications/Google Chrome.app"]},
    "safari":               {"display_name": "Safari",       "names": ["safari"],                                               "keywords": ["浏览器", "网页", "书签", "browser", "tab"],         "category": "浏览器","description": "打开网页、管理标签页、书签",           "bundle_hints": ["/Applications/Safari.app", "/System/Applications/Safari.app"]},
    "arc":                  {"display_name": "Arc",          "names": ["arc", "arc browser"],                                   "keywords": ["浏览器", "网页", "browser", "tab"],                 "category": "浏览器","description": "打开网页、管理标签页",                 "bundle_hints": ["/Applications/Arc.app"]},
    "microsoft-word":       {"display_name": "Word",         "names": ["microsoft-word", "word", "ms word"],                    "keywords": ["文档", "编辑", "排版", "document", "word"],         "category": "办公",  "description": "文档编辑、格式设置、表格",             "bundle_hints": ["/Applications/Microsoft Word.app"]},
    "microsoft-excel":      {"display_name": "Excel",        "names": ["microsoft-excel", "excel", "表格", "电子表格"],         "keywords": ["表格", "数据", "公式", "spreadsheet", "excel"],     "category": "办公",  "description": "电子表格、图表、公式计算",             "bundle_hints": ["/Applications/Microsoft Excel.app"]},
    "microsoft-powerpoint": {"display_name": "PowerPoint",  "names": ["microsoft-powerpoint", "powerpoint", "ppt", "幻灯片"], "keywords": ["幻灯片", "演示", "ppt", "presentation"],            "category": "办公",  "description": "幻灯片制作、动画设置",                 "bundle_hints": ["/Applications/Microsoft PowerPoint.app"]},
    "keynote":              {"display_name": "Keynote",      "names": ["keynote"],                                              "keywords": ["幻灯片", "演示", "presentation"],                   "category": "办公",  "description": "幻灯片制作、导出、演示控制",           "bundle_hints": ["/Applications/Keynote.app"]},
    "pages":                {"display_name": "Pages",        "names": ["pages"],                                                "keywords": ["文档", "编辑", "document"],                         "category": "办公",  "description": "文档编辑、排版、导出",                 "bundle_hints": ["/Applications/Pages.app"]},
    "numbers":              {"display_name": "Numbers",      "names": ["numbers"],                                              "keywords": ["表格", "数据", "spreadsheet"],                      "category": "办公",  "description": "电子表格、行列操作",                   "bundle_hints": ["/Applications/Numbers.app"]},
    "mail":                 {"display_name": "邮件",         "names": ["mail", "邮件", "apple mail"],                           "keywords": ["邮件", "收件箱", "发送", "email", "inbox"],         "category": "效率",  "description": "发送邮件、搜索、管理邮箱",             "bundle_hints": ["/System/Applications/Mail.app"]},
    "calendar":             {"display_name": "日历",         "names": ["calendar", "日历"],                                     "keywords": ["日历", "日程", "事件", "event", "schedule", "安排"],"category": "效率",  "description": "创建/查询日程、视图切换",              "bundle_hints": ["/System/Applications/Calendar.app"]},
    "reminders":            {"display_name": "提醒事项",     "names": ["reminders", "提醒事项", "提醒", "待办"],                "keywords": ["提醒", "待办", "任务", "todo", "reminder"],         "category": "效率",  "description": "查看提醒事项、待办管理",               "bundle_hints": ["/System/Applications/Reminders.app"]},
    "notes":                {"display_name": "备忘录",       "names": ["notes", "备忘录", "备忘"],                              "keywords": ["备忘录", "笔记", "note", "memo"],                   "category": "效率",  "description": "创建/搜索/编辑备忘录",                 "bundle_hints": ["/System/Applications/Notes.app"]},
    "contacts":             {"display_name": "通讯录",       "names": ["contacts", "通讯录", "联系人"],                         "keywords": ["联系人", "通讯录", "contact"],                      "category": "效率",  "description": "联系人管理、搜索查询",                 "bundle_hints": ["/System/Applications/Contacts.app"]},
    "messages":             {"display_name": "信息",         "names": ["messages", "信息", "短信", "imessage"],                 "keywords": ["短信", "消息", "信息", "sms", "imessage"],          "category": "效率",  "description": "发送消息",                             "bundle_hints": ["/System/Applications/Messages.app"]},
    "wechat":               {"display_name": "微信",         "names": ["wechat", "微信", "wei xin"],                            "keywords": ["微信", "消息", "聊天", "wechat", "chat"],           "category": "通信",  "description": "消息收发、文件传输",                   "bundle_hints": ["/Applications/WeChat.app"]},
    "qq":                   {"display_name": "QQ",           "names": ["qq"],                                                   "keywords": ["qq", "消息", "聊天", "chat"],                       "category": "通信",  "description": "消息收发、文件传输",                   "bundle_hints": ["/Applications/QQ.app"]},
    "dingtalk":             {"display_name": "钉钉",         "names": ["dingtalk", "钉钉", "dingding"],                         "keywords": ["钉钉", "消息", "审批", "dingtalk"],                 "category": "通信",  "description": "消息收发、审批、考勤",                 "bundle_hints": ["/Applications/DingTalk.app"]},
    "lark":                 {"display_name": "飞书",         "names": ["lark", "飞书", "feishu"],                               "keywords": ["飞书", "消息", "文档", "lark", "feishu"],           "category": "通信",  "description": "消息收发、文档协作、日程",             "bundle_hints": ["/Applications/Lark.app"]},
    "telegram":             {"display_name": "Telegram",     "names": ["telegram", "tg"],                                       "keywords": ["消息", "聊天", "telegram", "chat"],                 "category": "通信",  "description": "消息收发、群组管理",                   "bundle_hints": ["/Applications/Telegram.app"]},
    "slack":                {"display_name": "Slack",        "names": ["slack"],                                                "keywords": ["slack", "消息", "频道", "channel"],                 "category": "通信",  "description": "消息收发、频道管理",                   "bundle_hints": ["/Applications/Slack.app"]},
    "discord":              {"display_name": "Discord",      "names": ["discord"],                                              "keywords": ["discord", "消息", "语音", "voice"],                 "category": "通信",  "description": "消息收发、语音频道",                   "bundle_hints": ["/Applications/Discord.app"]},
    "zoom":                 {"display_name": "Zoom",         "names": ["zoom", "腾讯会议"],                                     "keywords": ["会议", "视频", "zoom", "meeting"],                  "category": "通信",  "description": "视频会议、屏幕共享",                   "bundle_hints": ["/Applications/zoom.us.app"]},
    "finder":               {"display_name": "Finder",       "names": ["finder", "访达"],                                       "keywords": ["文件", "文件夹", "访达", "file", "folder", "下载"],  "category": "系统",  "description": "文件管理、窗口视图、前往目录",         "bundle_hints": ["/System/Library/CoreServices/Finder.app"]},
    "terminal":             {"display_name": "终端",         "names": ["terminal", "终端"],                                     "keywords": ["终端", "命令行", "脚本", "shell", "script"],         "category": "系统",  "description": "执行脚本、窗口设置",                   "bundle_hints": ["/System/Applications/Utilities/Terminal.app"]},
    "system-settings":      {"display_name": "系统设置",     "names": ["system-settings", "系统设置", "system preferences"],   "keywords": ["设置", "偏好", "系统", "settings"],                  "category": "系统",  "description": "系统设置查看与修改",                   "bundle_hints": ["/System/Applications/System Settings.app"]},
    "shortcuts":            {"display_name": "快捷指令",     "names": ["shortcuts", "快捷指令"],                                "keywords": ["快捷指令", "自动化", "shortcut"],                    "category": "系统",  "description": "运行快捷指令",                         "bundle_hints": ["/System/Applications/Shortcuts.app"]},
    "figma":                {"display_name": "Figma",        "names": ["figma"],                                                "keywords": ["设计", "原型", "图层", "design", "ui"],              "category": "设计",  "description": "对象操作、文本排版、矢量编辑",         "bundle_hints": ["/Applications/Figma.app"]},
    "xcode":                {"display_name": "Xcode",        "names": ["xcode"],                                                "keywords": ["开发", "构建", "运行", "build", "run", "xcode"],    "category": "开发",  "description": "项目构建、运行、测试、调试",           "bundle_hints": ["/Applications/Xcode.app"]},
    "visual-studio-code":   {"display_name": "VS Code",      "names": ["visual-studio-code", "vscode", "vs code", "code"],     "keywords": ["代码", "编辑器", "code", "editor", "ide"],          "category": "开发",  "description": "代码编辑、终端、扩展、调试",           "bundle_hints": ["/Applications/Visual Studio Code.app"]},
    "cursor":               {"display_name": "Cursor",       "names": ["cursor"],                                               "keywords": ["代码", "ai", "编辑器", "code", "editor"],          "category": "开发",  "description": "AI 代码编辑、终端、调试",              "bundle_hints": ["/Applications/Cursor.app"]},
    "notion":               {"display_name": "Notion",       "names": ["notion"],                                               "keywords": ["笔记", "文档", "知识库", "note", "wiki"],           "category": "效率",  "description": "文档编辑、知识库、项目管理",           "bundle_hints": ["/Applications/Notion.app"]},
    "obsidian":             {"display_name": "Obsidian",     "names": ["obsidian"],                                             "keywords": ["笔记", "双链", "知识图谱", "note", "md"],           "category": "效率",  "description": "笔记编辑、双向链接、知识图谱",         "bundle_hints": ["/Applications/Obsidian.app"]},
}


def _score_catalog_match(query: str, app_id: str, entry: dict) -> int:
    """Score how well a catalog entry matches the query. Higher = better."""
    q = query.lower().strip()
    for name in entry["names"]:
        if q == name.lower():
            return 100
    if app_id == q or app_id.startswith(q) or q.startswith(app_id):
        return 90
    for name in entry["names"]:
        if q in name.lower() or name.lower() in q:
            return 70
    for kw in entry["keywords"]:
        if kw in q or q in kw:
            return 50
    return 0


def _check_bundle_present(bundle_hints: list[str]) -> bool:
    """Check if any of the app bundle paths exist on disk (single stat per path)."""
    return any(Path(p).is_dir() for p in bundle_hints)


@mcp.tool()
def clam_find_app(query: str) -> str:
    """当用户提到任何 Mac 应用名称时，第一步调用此工具。

    【何时调用】用户说到任何 Mac 应用时立即调用，无论是否已安装：
      "QQ音乐"、"微信"、"日历"、"chrome"、"Finder"、"Spotify" ...
      也支持功能描述："play music" → music/spotify，"发邮件" → mail

    【优势】即时返回（<10ms），不扫描文件系统，不解析 sdef 文件。
    比 clam_scan 快 100x，适合作为第一步查找。

    query 支持中文名、英文名、功能描述：
      "QQ音乐" → qqmusic，"play music" → music/spotify，"微信" → wechat
      "日历" → calendar，"访达" → finder，"谷歌浏览器" → google-chrome

    返回匹配的应用列表，含安装状态和下一步操作建议。
    未找到时返回 found=false，并建议用 clam_install 直接尝试。
    """
    installed_ids = set(registry.list_all().keys())
    q = query.lower().strip()

    scored: list[tuple[int, str, dict]] = []
    for app_id, entry in _APP_CATALOG.items():
        score = _score_catalog_match(q, app_id, entry)
        if score > 0:
            scored.append((score, app_id, entry))

    scored.sort(key=lambda x: x[0], reverse=True)
    top3 = scored[:3]

    if not top3:
        return json.dumps({
            "found": False,
            "query": query,
            "message": "未在内置目录中找到匹配应用。该应用可能仍可通过 CLAM 控制。",
            "suggestions": [
                f"尝试 clam_install('{query}') 直接安装（支持模糊匹配）",
                "或用 clam_scan() 扫描所有可用应用（较慢，约 10-30s）",
            ],
        }, ensure_ascii=False)

    matches = []
    for _, app_id, entry in top3:
        is_installed = app_id in installed_ids
        present = _check_bundle_present(entry["bundle_hints"])
        matches.append({
            "app_id": app_id,
            "name": entry["display_name"],
            "category": entry["category"],
            "description": entry["description"],
            "installed": is_installed,
            "present_on_mac": present,
            "next_step": "clam_execute" if is_installed else "clam_install",
        })

    best = matches[0]
    best_id = best["app_id"]
    step1 = "已安装，可直接执行" if best["installed"] else f"clam_install('{best_id}')"
    workflow = (
        f"1. {step1}"
        f"  2. clam_info('{best_id}') 查看可用命令"
        f"  3. clam_execute('{best_id}', 命令名, 参数)"
    )

    return json.dumps({
        "found": True,
        "query": query,
        "best_match": best,
        "other_matches": matches[1:],
        "workflow": workflow,
    }, ensure_ascii=False, indent=2)


@mcp.tool()
def clam_scan() -> str:
    """扫描 macOS 上可被脚本化控制的应用。

    返回所有可控应用的列表，包含名称、ID、命令数、属性数、模式等信息。
    mode: "full" = 完整 AppleScript 支持, "ui" = UI Scripting (菜单点击), "basic" = 基础模式。
    """
    apps = scan_applications()
    results = []
    for app in apps:
        if app.sdef_path:
            try:
                sdef_info = parse_sdef(app.sdef_path, app.name)
                wi = get_wrapper_info(sdef_info, app.app_id)
                results.append({
                    "name": app.name,
                    "app_id": app.app_id,
                    "commands": len(wi["commands"]),
                    "properties": len(wi["properties"]),
                    "nested_groups": len(wi["nested_groups"]),
                    "installed": app.installed,
                    "mode": "full",
                })
            except Exception:
                continue
        else:
            results.append({
                "name": app.name,
                "app_id": app.app_id,
                "commands": 0,
                "properties": 0,
                "installed": app.installed,
                "mode": "ui",
            })
    return json.dumps(results, ensure_ascii=False, indent=2)


@mcp.tool()
def clam_info(app_id: str) -> str:
    """查看某个应用的完整能力清单（命令、属性、嵌套对象）。

    每个命令都有 supported 字段标记是否可靠。调用前先用此工具了解有哪些命令可用。
    app_id 支持模糊匹配：chrome → google-chrome, word → microsoft-word。
    """
    app = find_app(app_id) or find_basic_app(app_id)
    if not app:
        return json.dumps({"error": f"未找到应用: {app_id}"})

    if not app.sdef_path:
        if app.basic_mode:
            basic_cmds = [
                {"name": "activate",     "description": "将应用窗口前置", "supported": True, "params": []},
                {"name": "quit-app",     "description": "退出应用",       "supported": True, "params": []},
                {"name": "open-file",    "description": "用此应用打开文件", "supported": True, "params": [{"name": "--filepath", "description": "文件路径"}]},
                {"name": "get-name",     "description": "获取应用名称",   "supported": True, "params": []},
                {"name": "get-version",  "description": "获取版本号",     "supported": True, "params": []},
                {"name": "get-frontmost","description": "是否为前台应用", "supported": True, "params": []},
            ]
        else:
            # UI mode — scan menus to get current commands
            menu_scan = scan_menus(app.name, app.process_name or None)
            if menu_scan and menu_scan.total_items > 0:
                ui_info = get_ui_wrapper_info(menu_scan)
                basic_cmds = [
                    {
                        "name": item.cli_name,
                        "description": item.name,
                        "supported": True,
                        "params": [],
                    }
                    for group in ui_info["menu_groups"]
                    for item in group.items
                ]
            else:
                basic_cmds = []

        return json.dumps({
            "app_id": app.app_id,
            "app_name": app.name,
            "mode": "basic" if app.basic_mode else "ui",
            "commands": basic_cmds,
            "properties": [],
            "nested_groups": [],
        }, ensure_ascii=False)

    try:
        sdef_info = parse_sdef(app.sdef_path, app.name)
    except Exception as e:
        return json.dumps({"error": f"解析 sdef 失败: {e}"})

    wi = get_wrapper_info(sdef_info, app.app_id)
    support = check_command_support(sdef_info, app.app_id)
    support_map = {r["name"]: r["supported"] for r in support}

    from clam.generator.applescript_gen import _build_list_commands
    list_cmds = _build_list_commands(sdef_info)

    # Check if installed wrapper is up-to-date
    installed = registry.get(app.app_id)
    needs_update = installed and installed.get("generator_version", 0) < GENERATOR_VERSION

    def _list_cmd_name(lc) -> str:
        if lc.is_element_of_element:
            return f"list-{lc.element_plural.replace(' ', '-')}"
        if lc.prop_name:
            return f"list-{lc.prop_cli_name}-{lc.element_plural.replace(' ', '-')}"
        return f"list-{lc.prop_cli_name}"

    def _list_cmd_params(lc) -> list:
        params = []
        if lc.is_element_of_element:
            params.append({"name": f"--{lc.parent_cli_name}", "description": f"Filter by {lc.parent_type} name (optional)"})
        if lc.filter_label:
            params.append({"name": f"--{lc.filter_label}", "description": f"Only show {lc.filter_label} {lc.element_plural}."})
        return params

    result = {
        "app_id": app.app_id,
        "app_name": app.name,
        "entry_point": f"clam-{app.app_id}",
        "commands": [
            {
                "name": cmd.cli_name,
                "description": cmd.description,
                "has_direct_param": cmd.direct_param,
                "supported": support_map.get(cmd.cli_name, True),
                "params": [
                    {"name": f"--{p.cli_name}", "description": p.description}
                    for p in cmd.params
                ],
            }
            for cmd in wi["commands"]
        ] + ([
            {
                "name": _list_cmd_name(lc),
                "description": (
                    f"List {lc.element_plural} (use --{lc.parent_cli_name} to filter by {lc.parent_type})"
                    if lc.is_element_of_element
                    else f"List {lc.element_plural}" + (f" in {lc.prop_name}" if lc.prop_name else "")
                ),
                "supported": True,
                "params": _list_cmd_params(lc),
            }
            for lc in list_cmds
        ] if not needs_update else []),
        "properties": [
            {
                "name": prop.cli_name,
                "access": prop.access,
                "type": prop.value_type,
                "get_command": f"get-{prop.cli_name}",
                "set_command": f"set-{prop.cli_name}" if prop.access == "rw" else None,
            }
            for prop in wi["properties"]
        ],
        "nested_groups": [
            {
                "name": group.cli_name,
                "compound_command": f"get-{group.cli_name}",
                "properties": [
                    {
                        "name": prop.cli_name,
                        "access": prop.access,
                        "get_command": f"get-{group.cli_name}-{prop.cli_name}",
                        "set_command": (
                            f"set-{group.cli_name}-{prop.cli_name}"
                            if prop.access == "rw" else None
                        ),
                    }
                    for prop in group.properties
                ],
            }
            for group in wi["nested_groups"]
        ],
    }
    if needs_update:
        result["warning"] = (
            f"Wrapper was installed with an older generator (v{installed.get('generator_version', 0)}, "
            f"current v{GENERATOR_VERSION}). Run clam_install('{app.app_id}') to regenerate "
            f"and unlock list-* collection commands."
        )
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def clam_install(app_id: str) -> str:
    """为任意 macOS 应用安装 CLI wrapper，安装后可通过 clam_execute 执行命令。

    【何时调用】clam_find_app 确认 app_id 后立即调用。或已知 app_id 时直接调用。
    不要在调用此工具前自己写 AppleScript。

    常见 app_id 映射（支持模糊匹配）：
      音乐类: music / spotify / qqmusic / neteasemusic
      通信类: wechat / qq / dingtalk / lark / slack / messages / telegram
      效率类: calendar / mail / reminders / notes / contacts
      文件管理: finder
      浏览器: google-chrome / safari / arc
      办公: microsoft-word / microsoft-excel / microsoft-powerpoint / keynote / pages
      系统: terminal / shortcuts / system-settings
      开发: visual-studio-code / cursor / xcode

    安装过程自动选择最佳模式：full (sdef) → ui (菜单点击) → basic (标准套件)。
    任何 .app 都可以尝试，即使不在上面列表中。
    """
    app = find_app(app_id)
    if not app:
        app = find_basic_app(app_id)
    if not app:
        return json.dumps({"error": f"未找到应用: {app_id}"})

    wrapper_dir = registry.REGISTRY_DIR / "wrappers" / app.app_id

    mode = "full"
    menu_scan = None

    if not app.sdef_path:
        menu_scan = scan_menus(app.name, app.process_name or None)
        if menu_scan and menu_scan.total_items > 0:
            mode = "ui"
        else:
            mode = "basic"

    try:
        if mode == "basic":
            generate_basic_wrapper(app.name, wrapper_dir, app_id=app.app_id)
            cmd_count, prop_count = 3, 3
        elif mode == "ui":
            generate_ui_wrapper(app.name, menu_scan.process_name, menu_scan, wrapper_dir, app_id=app.app_id)
            ui_info = get_ui_wrapper_info(menu_scan)
            cmd_count = ui_info["menu_cmd_count"] + 3
            prop_count = 3
        else:
            sdef_info = parse_sdef(app.sdef_path, app.name)
            generate_wrapper(sdef_info, wrapper_dir, app_id=app.app_id)
            wi = get_wrapper_info(sdef_info)
            cmd_count = len(wi["commands"])
            prop_count = len(wi["properties"])
    except Exception as e:
        return json.dumps({"error": f"生成 wrapper 失败: {e}"})

    if not install_wrapper(app.app_id, wrapper_dir):
        return json.dumps({"error": "pip install 失败"})

    registry.register(
        app_id=app.app_id,
        app_name=app.name,
        sdef_path=app.sdef_path,
        wrapper_dir=str(wrapper_dir),
        command_count=cmd_count,
        property_count=prop_count,
    )

    return json.dumps({
        "app_id": app.app_id,
        "entry_point": f"clam-{app.app_id}",
        "commands": cmd_count,
        "properties": prop_count,
        "mode": mode,
    }, ensure_ascii=False)


@mcp.tool()
def clam_execute(app_id: str, command: str, args: dict | None = None) -> str:
    """在已安装的应用 wrapper 上执行命令。使用此工具替代直接写 AppleScript。

    必须先用 clam_install 安装 wrapper。先用 clam_info 查看可用命令。
    command 是命令名（如 "play", "get-sound-volume", "set-sound-volume"）。
    args 是命名参数字典（如 {"once": true}），位置参数用 "_direct" 键传递。

    示例：
      clam_execute("music", "play")
      clam_execute("music", "set-sound-volume", {"_direct": "50"})
      clam_execute("music", "get-current-track")
      clam_execute("calendar", "get-...")       # 读取日历事件
      clam_execute("mail", "get-...")           # 读取未读邮件
      clam_execute("reminders", "get-...")      # 读取待办提醒
      clam_execute("finder", "move", {...})     # 移动文件

    常见场景：用户说"今天有什么" → 依次读取 calendar/mail/reminders 数据，汇总成简报。
    用户说"帮我整理邮件" → 读取邮件列表，分类后展示给用户确认，再执行归档。
    用户说"整理 Downloads" → 用 finder 列出文件，分类后展示计划，确认后移动。

    重要：执行写入/移动/删除操作前，务必先展示计划并获得用户确认。
    """
    # 检查是否已安装
    wrapper = registry.get(app_id)
    if not wrapper:
        return json.dumps({"error": f"未安装 wrapper: {app_id}，请先调用 clam_install"})

    # Check for stale wrapper: list-* commands require generator v2+
    if command.startswith("list-") and wrapper.get("generator_version", 0) < GENERATOR_VERSION:
        return json.dumps({
            "error": (
                f"命令 '{command}' 需要重新安装 wrapper（当前版本 v{wrapper.get('generator_version', 0)}，"
                f"需要 v{GENERATOR_VERSION}）。请调用 clam_install('{app_id}') 后重试。"
            )
        })

    # Resolve full path: try registry name in venv bin first, then clam-{app_id}
    import sys as _sys
    _venv_bin = Path(_sys.executable).parent
    _ep_name = wrapper["entry_point"]
    _full = _venv_bin / _ep_name
    if not _full.exists():
        _full = _venv_bin / f"clam-{app_id}"
    entry_point = str(_full) if _full.exists() else _ep_name
    cmd = [entry_point, "--json", command]

    if args:
        direct = args.pop("_direct", None)
        if direct is not None:
            cmd.append(str(direct))
        for key, value in args.items():
            if isinstance(value, bool):
                if value:
                    cmd.append(f"--{key}")
            else:
                cmd.extend([f"--{key}", str(value)])

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=35,
        )
    except FileNotFoundError:
        return json.dumps({"error": f"找不到命令 {entry_point}，可能需要重新安装"})
    except subprocess.TimeoutExpired:
        return json.dumps({"error": "命令执行超时 (35s)"})

    if result.returncode != 0:
        return json.dumps({
            "error": result.stderr.strip() or "命令执行失败",
            "exit_code": result.returncode,
        })

    return result.stdout.strip() or '{"result": "ok"}'


@mcp.tool()
def clam_doctor(app_id: str) -> str:
    """检查应用命令的可靠性，分析哪些命令的参数类型完全支持、哪些可能不可用。

    返回每个命令的 supported 状态和具体问题描述。
    """
    app = find_app(app_id) or find_basic_app(app_id)
    if not app:
        return json.dumps({"error": f"未找到应用: {app_id}"})

    if not app.sdef_path:
        return json.dumps({"error": f"{app.name} 无 AppleScript 脚本定义，doctor 仅适用于 full 模式应用"})

    try:
        sdef_info = parse_sdef(app.sdef_path, app.name)
    except Exception as e:
        return json.dumps({"error": f"解析 sdef 失败: {e}"})

    results = check_command_support(sdef_info, app.app_id)
    supported = [r for r in results if r["supported"]]
    unsupported = [r for r in results if not r["supported"]]

    return json.dumps({
        "app_id": app.app_id,
        "total": len(results),
        "supported": len(supported),
        "unsupported": len(unsupported),
        "commands": results,
    }, ensure_ascii=False, indent=2)


def main():
    """启动 CLAM MCP Server (stdio 模式)。"""
    mcp.run()


if __name__ == "__main__":
    main()
