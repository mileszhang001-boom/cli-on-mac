<h1 align="center"><img src="assets/logo.png" alt="" width="64" style="vertical-align: middle;">&nbsp; CLAM: 给 AI 装上控制 Mac 的手</h1>

<p align="center">
  <strong>你的 Mac 上有几十个应用，但 AI 一个都碰不到。<br>
  CLAM 一键生成 CLI 接口，让 AI Agent 用原生方式操控一切。</strong>
</p>

安装后，Claude Code 能调用应用原生能力播放音乐、操作 Word、发邮件、绘制3D模型，无需依赖API

## 🦀 给你的 AI 装上虾钳

两步，不到一分钟：

```bash
pip install -e .                        # 装 CLAM
claude mcp add clam -- clam-mcp         # 注册 MCP Server
```

完成了。去 Claude Code 里说一句：

> "帮我把音量调到 50，然后告诉我现在在放什么歌"

AI 自动扫描应用、安装 wrapper、执行命令——你不需要输入任何命令

## 🖐 30 秒上手（人类版）

```bash
clam scan                              # 看看有什么
clam install music                     # 装一个试试
clam-music play                        # 播放
clam-music next-track                  # 下一首
clam-music set-sound-volume 80         # 音量 80
clam-music get-current-track           # 当前曲目全部信息
```

## 🔧 三种模式，覆盖几乎所有应用

| 模式 | 原理 | 典型应用 | 能力 |
|------|------|---------|------|
| **完整模式** | 解析 .sdef 脚本定义 | Music、Finder、Chrome、Word | 几十到几百个命令 |
| **UI Scripting** | 通过菜单点击控制 | Figma (151 命令)、QQ音乐 (10 命令) | 菜单里能点的都能控 |
| **基础模式** | macOS 标准套件 | 钉钉、WPS、微信 | 前置/退出/打开文件/查版本 |

安装时自动选择最佳模式，不需要手动指定

## 📖 完整命令

```bash
clam scan              # 扫描可控应用
clam install <app>     # 安装 CLI（模糊匹配：chrome → google-chrome）
clam info <app>        # 查看能力详情
clam doctor <app>      # 检查命令可靠性
clam list              # 查看已安装
clam remove <app>      # 卸载

clam-<app>             # 能力概览
clam-<app> api         # 完整 API 列表
```

## ❓ 常见问题

**找不到 `clam-xxx`？** — `source .venv/bin/activate`

**"permission denied"？** — 系统设置 > 隐私与安全性 > 自动化，允许终端控制目标应用

**UI Scripting 报权限错误？** — 系统设置 > 隐私与安全性 > 辅助功能，允许终端

**只有基础命令？** — 取决于应用开发者，国产应用大多没有脚本化接口，只能基础模式
