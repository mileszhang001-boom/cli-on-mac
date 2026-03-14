<h1 align="center"><img src="../assets/logo.png" alt="" width="64" style="vertical-align: middle;">&nbsp; CLAM — CLI on Mac</h1>


<p align="center">
  中文 | <a href="../README.md">English</a>
</p>

<p align="center">
  <strong>给任何 AI Agent 装上控制 Mac 的手。</strong><br>
  自动发现应用、生成 CLI 接口、返回结构化 JSON。
</p>

<br>

你的 Mac 上有几十个应用，但 AI 一个都碰不到。CLAM 自动扫描已安装的应用，即时生成类型化的 CLI 工具，所有命令都返回结构化 JSON。无需 API、无需手写适配、不用折腾 AppleScript。

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
clam scan                       # 发现可控应用
clam install music              # 生成 CLI（约 10 秒）
clam-music play                 # 播放音乐
clam-music --json get-current-track   # → 结构化 JSON
clam-music set-sound-volume 50  # 设置音量
```

支持模糊匹配：`chrome` → `google-chrome`，`word` → `microsoft-word`。

## 接入 AI Agent

### OpenClaw

从 [ClawHub](https://clawhub.ai) 安装：

```bash
clawhub install clam-mac
```

或在 Lobster pipeline 中使用：

```yaml
steps:
  - run: clam-music set-sound-volume 20
  - run: clam-music play
  - run: clam-finder open ~/Projects/current
```

安装后，AI 自动通过 `clam scan` 发现能力、安装 wrapper、执行命令。

### Claude Code (MCP)

```bash
pip install clam-mac
claude mcp add clam -- clam-mcp
```

然后直接说：

> "帮我把音量调到 50，告诉我现在在放什么歌"

### 其他 Agent 框架

CLAM 生成的是标准 CLI 工具，任何能调用 shell 命令的 Agent 都可以直接使用：

```python
import subprocess, json
result = subprocess.run(["clam-music", "--json", "get-current-track"], capture_output=True, text=True)
track = json.loads(result.stdout)
```

## 工作原理

CLAM 自动为每个应用选择最佳自动化模式：

| 模式 | 原理 | 典型应用 | 命令数 |
|------|------|---------|--------|
| **完整模式** | 解析 `.sdef` 脚本定义 | Music、Finder、Chrome、Safari、Word | 几十到几百 |
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

## 常见问题

| 问题 | 解决 |
|------|------|
| 找不到 `clam-xxx` | `source .venv/bin/activate` 或检查 `PATH` |
| Permission denied | 系统设置 > 隐私与安全性 > 自动化 |
| UI Scripting 报错 | 系统设置 > 隐私与安全性 > 辅助功能 |
| 只有基础命令 | 应用无脚本化接口，基础模式已是上限 |

## 许可

[MIT](../LICENSE)
