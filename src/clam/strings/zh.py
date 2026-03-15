"""中文字符串 for CLAM CLI."""

STRINGS: dict[str, str] = {
    # ── CLI group ───────────────────────────────────────────────────────────────
    "cli.help_json": "输出 JSON 格式，供 AI 工具解析",
    "cli.description": "扫描你的 Mac，发现可被 AI 操控的应用，一键生成 CLI 接口。",

    # ── scan ────────────────────────────────────────────────────────────────────
    "scan.help": "扫描本地可脚本化应用",
    "scan.scanning": "正在扫描本地应用…",
    "scan.no_apps": "未发现可脚本化应用",
    "scan.done": "扫描完成",
    "scan.found": "发现 {count} 个可脚本化应用",
    "scan.hint": "试一试: clam install music  |  详情: clam info music",

    # ── install ─────────────────────────────────────────────────────────────────
    "install.help": "安装应用的 CLI wrapper",
    "install.probing_menus": "正在探测 {name} 的菜单结构…",
    "install.mode.full": "",
    "install.mode.ui": "（UI Scripting 模式）",
    "install.mode.basic": "（基础模式）",
    "install.generating": "正在为 {name} 生成 CLI wrapper{mode}…",
    "install.gen_failed": "生成 wrapper 失败: {error}",
    "install.installing": "正在安装 clam-{app_id}…",
    "install.pip_failed": "pip install 失败",
    "install.sdef_failed": "解析 sdef 失败: {error}",
    "install.success_full": "{name} 已安装 → [bold]{ep}[/bold]",
    "install.success_basic": "{name} 已安装 → [bold]{ep}[/bold]  [dim]（基础模式）[/dim]",
    "install.success_ui": "{name} 已安装 → [bold]{ep}[/bold]  [dim]（UI Scripting 模式）[/dim]",
    "install.cmd_prop": "命令: {cmds} 个  |  属性: {props} 个",
    "install.menu_cmd": "菜单命令: {menus} 个  |  基础命令: 6 个",
    "install.quickstart": "快速上手:",
    "install.activate_hint": "前置窗口",
    "install.version_hint": "查看版本",
    "install.quit_hint": "退出应用",
    "install.view_summary": "查看能力概括",
    "install.view_api": "查看完整 API",
    "install.nested_count": "  |  嵌套对象: {count} 个",
    "install.ai_title": "AI 工具集成:",
    "install.ai_configured": "已配置完成，AI 可直接在终端调用 [cyan]{ep}[/cyan] 的所有命令。",
    "install.ai_guide": "查看 AI 集成指南: [dim]clam --json info {app_id}[/dim]",

    # ── list ────────────────────────────────────────────────────────────────────
    "list.help": "查看已安装的 wrapper",
    "list.empty": "尚未安装任何 wrapper，运行 [bold]clam scan[/bold] 查看可用应用",
    "list.title": "已安装的 wrapper",
    "list.col.app": "应用",
    "list.col.entry": "入口命令",
    "list.col.commands": "命令",
    "list.col.properties": "属性",
    "list.col.installed_at": "安装时间",

    # ── info ────────────────────────────────────────────────────────────────────
    "info.help": "查看应用的命令和属性清单",
    "info.help_detail": "对 AI agent 集成最关键 — agent 先 clam info <app> --json\n获取能力清单，再调 clam-<app> <command>。",
    "info.installed": "已安装",
    "info.not_installed": "未安装",
    "info.entry": "入口:",
    "info.cmd_prop": "命令: {cmds} 个  |  属性: {props} 个",
    "info.nested": "  |  嵌套对象: {count} 个",
    "info.tbl.commands": "命令",
    "info.tbl.name": "命令名",
    "info.tbl.description": "说明",
    "info.tbl.params": "参数",
    "info.tbl.properties": "属性 (get/set)",
    "info.tbl.prop_name": "属性名",
    "info.tbl.access": "访问",
    "info.tbl.type": "类型",
    "info.tbl.prop_desc": "说明",
    "info.nested_title": "{name} ({class_name}) 属性",
    "info.tbl.command": "命令",
    "info.compound_cmd": "复合命令: get-{name} → JSON",

    # ── doctor ──────────────────────────────────────────────────────────────────
    "doctor.help": "检查应用命令的可靠性（参数类型分析）",
    "doctor.title": "{name} 命令可靠性检查",
    "doctor.supported": "✓ {n} / {total} 个命令完全支持",
    "doctor.unsupported": "⚠ {n} 个命令含复杂参数类型（可能不可用）",

    # ── remove ──────────────────────────────────────────────────────────────────
    "remove.help": "卸载应用的 CLI wrapper",
    "remove.not_found": "未找到已安装的 wrapper: {name}",
    "remove.removing": "正在卸载 clam-{app_id}…",
    "remove.success": "已卸载 clam-{app_id}",

    # ── lang ────────────────────────────────────────────────────────────────────
    "lang.current": "当前语言: {lang}",
    "lang.switched": "语言已设置为: {lang}",

    # ── mcp-setup ─────────────────────────────────────────────────────────────
    "mcp.checking": "检查 Claude Code 安装状态…",
    "mcp.no_claude": "未找到 Claude Code (claude)。\n请先安装: https://claude.ai/download",
    "mcp.registering": "注册 clam MCP 服务器（全局）…",
    "mcp.success": "clam MCP 服务器已全局注册。\n重启 Claude Code 即可使用，AI 现在可以调用所有 clam 命令。",
    "mcp.already": "clam MCP 服务器已注册。",
    "mcp.failed": "注册失败: {error}",
    "mcp.removed": "clam MCP 服务器已注销。",
    "mcp.not_registered": "clam MCP 服务器未注册。",

    # ── errors ──────────────────────────────────────────────────────────────────
    "err.app_not_found": "未找到应用: {name}，你是不是想找: {suggestions}",
    "err.app_not_found_generic": "未找到应用: {name}，运行 clam scan 查看可用应用",

    # ── output ──────────────────────────────────────────────────────────────────
    "output.error": "错误:",
    "output.none": "(无)",

    # ── categories ──────────────────────────────────────────────────────────────
    "cat.office": "办公",
    "cat.design": "设计",
    "cat.media": "媒体",
    "cat.browser": "浏览器",
    "cat.communication": "通信",
    "cat.productivity": "效率",
    "cat.development": "开发",
    "cat.system": "系统",
    "cat.tools": "工具",
    "cat.other": "其他",

    # ── auto-describe capabilities ──────────────────────────────────────────────
    "cap.playback": "播放控制",
    "cap.track_switch": "切歌",
    "cap.navigation": "页面导航",
    "cap.messaging": "消息收发",
    "cap.search": "搜索",
    "cap.import_export": "导入导出",
    "cap.build_run": "构建运行",
    "cap.start_stop": "启停控制",
    "cap.scriptable": "脚本化操作",
    "join.comma": "、",

    # ── app descriptions ────────────────────────────────────────────────────────
    # 媒体
    "app.desc.music": "控制播放、切歌、音量调节、曲目查询",
    "app.desc.tv": "视频播放、切集、音量调节、播放列表管理",
    "app.desc.quicktime-player": "视频播放、录屏、录音、导出裁剪",
    "app.desc.garageband": "音乐制作预览",
    "app.desc.photos": "照片导入导出、相册管理、幻灯片放映",
    "app.desc.spotify": "播放控制、切歌、播放列表、音量调节",
    "app.desc.qqmusic": "播放控制、切歌、歌单管理",
    # 浏览器
    "app.desc.google-chrome": "打开网页、管理标签页、页面导航",
    "app.desc.safari": "打开网页、管理标签页、书签、阅读列表",
    "app.desc.arc": "打开网页、管理标签页、页面导航",
    "app.desc.doubao": "打开网页、管理标签页、书签操作",
    # 办公
    "app.desc.microsoft-word": "文档编辑、格式设置、表格、批量排版",
    "app.desc.microsoft-excel": "电子表格、图表、公式计算、数据处理",
    "app.desc.microsoft-powerpoint": "幻灯片制作、动画设置、演示控制",
    "app.desc.microsoft-outlook": "邮件收发、日程管理、联系人",
    "app.desc.keynote": "幻灯片制作、导出、演示控制",
    "app.desc.pages": "文档编辑、排版、表格、导出",
    "app.desc.numbers": "电子表格、行列操作、排序、导出",
    "app.desc.notion": "文档编辑、知识库、项目管理",
    "app.desc.obsidian": "笔记编辑、双向链接、知识图谱",
    # 效率
    "app.desc.mail": "发送邮件、搜索、管理邮箱",
    "app.desc.calendar": "创建/查询日程、视图切换",
    "app.desc.contacts": "联系人管理、搜索查询",
    "app.desc.messages": "发送消息",
    "app.desc.notes": "创建/搜索/编辑备忘录",
    "app.desc.reminders": "查看提醒事项、待办管理",
    "app.desc.ticktick": "任务查询、添加待办、番茄钟",
    # 通信
    "app.desc.telegram": "消息收发、群组管理",
    "app.desc.wechat": "消息收发、文件传输",
    "app.desc.qq": "消息收发、文件传输",
    "app.desc.dingtalk": "消息收发、审批、考勤",
    "app.desc.lark": "消息收发、文档协作、日程",
    "app.desc.discord": "消息收发、语音频道",
    "app.desc.slack": "消息收发、频道管理、集成",
    "app.desc.zoom": "视频会议、屏幕共享",
    # 设计
    "app.desc.figma": "对象操作、文本排版、矢量编辑、图层管理",
    # 开发
    "app.desc.xcode": "项目构建、运行、测试、调试",
    "app.desc.visual-studio-code": "代码编辑、终端、扩展、调试",
    "app.desc.cursor": "AI 代码编辑、终端、调试",
    # 系统
    "app.desc.finder": "文件管理、窗口视图、前往目录、标签",
    "app.desc.terminal": "执行脚本、窗口设置",
    "app.desc.system-settings": "系统设置查看与修改",
    "app.desc.shortcuts": "运行快捷指令",
    # 工具
    "app.desc.amphetamine": "防休眠控制、会话管理",
    "app.desc.flow": "专注计时、番茄钟、阶段控制",
    "app.desc.the-unarchiver": "文件解压",
    "app.desc.bluetooth-file-exchange": "蓝牙文件收发",
    "app.desc.screen-sharing": "远程屏幕共享",
    "app.desc.console": "系统日志查看",
    "app.desc.clashx-pro": "网络代理、规则切换",
    "app.desc.chatgpt-atlas": "AI 对话",

    # ── template strings (baked at install time) ────────────────────────────────
    # Shared
    "tpl.capabilities": "核心能力:",
    "tpl.quickstart": "快速上手:",
    "tpl.view_api": "查看完整 API（供 AI 工具使用）:",
    "tpl.view_api_basic": "查看完整 API:",
    "tpl.api_docstring": "查看完整 API 列表（供 AI 工具使用）",
    "tpl.api_docstring_basic": "查看完整 API 列表",
    "tpl.basic_controls_label": "基础控制:",
    "tpl.basic_info_label": "基本信息:",
    "tpl.action_commands": "操作命令:",
    "tpl.properties_getset": "属性 (get/set):",
    "tpl.prop_suffix": "属性:",
    "tpl.get_all_json": "获取全部属性 (JSON)",
    "tpl.writable_prefix": "可写: set-",
    "tpl.writable_label": "可写",

    # Full mode summary
    "tpl.summary_full": "clam-{app_id} — {app_name} 的命令行控制工具",
    "tpl.cap_execute": "执行操作",
    "tpl.cap_rw": "读写状态",
    "tpl.unit_commands": "个命令",
    "tpl.unit_properties": "个属性",
    "tpl.unit_writable": "个可写",
    "tpl.deep_access": "个属性可深层访问",
    "tpl.colon_sep": "：",
    "tpl.join_sep": "、",
    "tpl.read_prefix": "读取",
    "tpl.set_prefix": "设置",
    "tpl.get_all_info": "获取{name}的全部信息",

    # Basic mode
    "tpl.summary_basic": "clam-{app_id} — {app_name} 的命令行控制工具（基础模式）",
    "tpl.basic_controls_desc": "基础控制    前置窗口、退出应用、打开文件",
    "tpl.basic_info_desc": "基本信息    应用名称、版本号、窗口状态",
    "tpl.no_sdef_basic": "该应用未提供脚本化接口，仅支持 macOS 标准命令。",

    # UI mode
    "tpl.summary_ui": "clam-{app_id} — {app_name} 的命令行控制工具（UI Scripting 模式）",
    "tpl.basic_controls_ui": "基础控制    前置窗口、退出应用、打开文件",
    "tpl.basic_info_ui": "基本信息    应用名称、版本号、窗口状态",
    "tpl.no_sdef_ui": "该应用未提供脚本化接口，通过菜单点击实现控制。",
    "tpl.accessibility_warning": "需要辅助功能权限（System Settings > Accessibility）。",
    "tpl.unit_ops": "个操作",

    # Command docstrings (baked into generated wrappers)
    "tpl.activate_doc": "前置窗口",
    "tpl.quit_doc": "退出应用",
    "tpl.open_doc": "用该应用打开文件",
    "tpl.get_name_doc": "获取应用名称",
    "tpl.get_version_doc": "获取版本号",
    "tpl.get_frontmost_doc": "是否为当前活跃窗口",
    # Command output messages
    "tpl.activated_msg": "{app_name} 已前置",
    "tpl.quit_msg": "{app_name} 已退出",
    "tpl.opened_msg": "已用 {app_name} 打开 {filepath}",
    # API list labels
    "tpl.activate_api": "前置窗口",
    "tpl.quit_api": "退出应用",
    "tpl.open_api": "用该应用打开文件",
    "tpl.name_api": "应用名称",
    "tpl.version_api": "版本号",
    "tpl.frontmost_api": "是否为当前活跃窗口",
    "tpl.path_arg": "<路径>",
}
