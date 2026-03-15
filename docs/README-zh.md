<h1 align="center"><img src="../assets/logo.png" alt="" width="64" style="vertical-align: middle;">&nbsp; CLAM — CLI on Mac</h1>


<p align="center">
  中文 | <a href="../README.md">English</a>
</p>

<p align="center">
  <strong>给任何 AI Agent 装上控制 Mac 的手。</strong><br>
  自动发现应用、生成 CLI 接口、返回结构化 JSON。
</p>

<p align="center">
  <a href="https://pypi.org/project/clam-mac/"><img src="https://img.shields.io/pypi/v/clam-mac" alt="PyPI"></a>
  <img src="https://img.shields.io/badge/platform-macOS-lightgrey" alt="macOS">
  <img src="https://img.shields.io/badge/python-3.10%2B-blue" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT">
</p>

<br>

你的 Mac 上有几十个应用，但 AI 一个都碰不到。CLAM 自动扫描已安装的应用，即时生成类型化的 CLI 工具，所有命令都返回结构化 JSON。无需 API、无需手写适配、不用折腾 AppleScript。

## 眼见为实

<table>
<tr>
<td width="45%">
<a href="https://youtu.be/LBmZHGgEl9I">
<img src="../assets/demo-getting-started-zh.png" width="100%">
</a>
</td>
<td valign="middle" width="55%">
<strong>🚀 三条命令，10 秒上手</strong><br><br>
<code>pip install</code> → <code>clam scan</code> → <code>clam install</code>，任何 Mac 应用立刻变成 AI 可调用的 CLI 工具。
</td>
</tr>
<tr><td colspan="2"><br></td></tr>
<tr>
<td width="45%">
<a href="https://youtu.be/G1IOv1YUPQU">
<img src="../assets/demo-email-zh.png" width="100%">
</a>
</td>
<td valign="middle" width="55%">
<strong>📧 AI 直接读邮件，无需 API Key</strong><br><br>
问"我有哪些未读邮件？"—— AI 实时读取 Apple Mail。无 OAuth，无 Gmail API，零折腾。
</td>
</tr>
<tr><td colspan="2"><br></td></tr>
<tr>
<td width="45%">
<a href="https://youtu.be/3WD85V0U4eo">
<img src="../assets/demo-calendar-zh.png" width="100%">
</a>
</td>
<td valign="middle" width="55%">
<strong>📅 一句话生成今日待办</strong><br><br>
"今天有什么安排？"—— AI 读取日历和备忘录，直接给你每日清单。零复制粘贴。
</td>
</tr>
<tr><td colspan="2"><br></td></tr>
<tr>
<td width="45%">
<a href="https://youtu.be/P95UukSavsI">
<img src="../assets/demo-spotify-zh.png" width="100%">
</a>
</td>
<td valign="middle" width="55%">
<strong>🎵 用 AI 对话控制 Spotify</strong><br><br>
说"我想听稻香"—— 就这么简单。AI 控制播放、暂停、切歌，零配置。
</td>
</tr>
</table>

## 安装

```bash
pip install clam-mac
```

> **找不到 `pip` 或报 `externally-managed-environment`？**
> macOS 自带的是 `pip3` 而非 `pip`，且 Python 3.12+ 禁止直接安装。请使用虚拟环境：
> ```bash
> python3 -m venv ~/clam-env
> source ~/clam-env/bin/activate
> pip install clam-mac
> ```
> 把 `source ~/clam-env/bin/activate` 加入 `~/.zshrc` 即可永久生效。

## 快速上手

```bash
clam scan                              # 发现可控应用
clam install music                     # 生成 CLI（约 10 秒）
clam-music play                        # 播放音乐
clam-music --json get-current-track    # → 结构化 JSON
clam-music set-sound-volume 50         # 设置音量
clam-mail list-inbox-messages --unread # 列出未读邮件
```

支持模糊匹配：`chrome` → `google-chrome`，`word` → `microsoft-word`。

## 接入 AI Agent

### Claude Code（MCP）

```bash
pip install clam-mac
clam mcp-setup
```

`clam mcp-setup` 会自动找到 `clam-mcp` 二进制并注册到 Claude Code，无需手动配置路径。重启 Claude Code 后直接说：

> "帮我把音量调到 50，告诉我现在在放什么歌"
> "列出我的未读邮件"
> "用 Finder 打开 Downloads 文件夹"

Claude 会自动调用 `clam_find_app` → `clam_install` → `clam_execute`，每个应用无需单独配置。

**MCP 工具一览：**

| 工具 | 说明 |
|------|------|
| `clam_find_app(query)` | 即时查找应用——始终从这里开始 |
| `clam_install(app_id)` | 生成并安装 CLI wrapper（约 10 秒） |
| `clam_info(app_id)` | 列出所有可用命令和属性 |
| `clam_execute(app_id, command, args?)` | 执行命令，返回 JSON |
| `clam_scan()` | 扫描所有可控应用 |
| `clam_doctor(app_id)` | 检查命令可靠性 |

### OpenClaw

从 [ClawHub](https://clawhub.ai) 安装：

```bash
clawhub install clam-mac
```

安装后，AI 自动通过 `clam_find_app` 发现能力、安装 wrapper、执行命令。

### 其他 Agent 框架

CLAM 生成的是标准 CLI 工具，任何能调用 shell 命令的 Agent 都可以直接使用：

```python
import subprocess, json
result = subprocess.run(
    ["clam-music", "--json", "get-current-track"],
    capture_output=True, text=True
)
track = json.loads(result.stdout)
```

## 工作原理

CLAM 自动为每个应用选择最佳自动化模式：

| 模式 | 原理 | 典型应用 | 命令数 |
|------|------|---------|--------|
| **完整模式** | 解析 `.sdef` 脚本定义 | Music、Finder、Mail、Chrome、Safari、Word | 几十到几百 |
| **UI Scripting** | 通过辅助功能点击菜单 | Figma、Slack、VS Code、Spotify | 所有菜单项 |
| **基础模式** | macOS 标准套件 | 钉钉、微信、WPS | 前置、退出、打开、版本 |

无需配置 — `clam install` 自动选择最佳模式。

## 命令参考

```bash
clam scan              # 扫描可控应用
clam install <app>     # 生成并安装 CLI
clam info <app>        # 查看可用命令
clam doctor <app>      # 检查命令可靠性
clam list              # 查看已安装
clam remove <app>      # 卸载
```

## v0.2.0 更新

- **集合查询** — 支持脚本定义的应用新增 `list-<容器>-<元素>` 命令（如 `clam-mail list-inbox-messages --unread`）
- **中文应用支持** — QQ 音乐、微信等名称含非 ASCII 字符的应用现可正常安装
- **MCP PATH 修复** — `clam_execute` 在 MCP 服务器上下文中可靠定位 wrapper 二进制
- **更好的 `clam_info`** — 基础模式和完整模式均可正确显示命令列表

## 常见问题

| 问题 | 解决 |
|------|------|
| 找不到 `clam-xxx` | `source ~/clam-env/bin/activate` 或检查 `PATH` |
| Permission denied | 系统设置 > 隐私与安全性 > 自动化 |
| UI Scripting 报错 | 系统设置 > 隐私与安全性 > 辅助功能 |
| 只有基础命令 | 应用无脚本化接口，基础模式已是上限 |
| MCP 工具找不到 | `claude mcp add` 后重启 Claude Code |

## 许可

[MIT](../LICENSE)
