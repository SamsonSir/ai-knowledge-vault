# Agent与技能系统

## 88. [2026-02-27]

## 📔 文章 5


> 文档 ID: `YEHbw8FuOicyFSksMVicHW2Bn1e`

**来源**: OpenClaw从安装到实战：一位开发者的完整配置手册 | **时间**: 2026-02-27 | **原文链接**: https://mp.weixin.qq.com/s/EXv8o3A1...

---

### 📋 核心分析

**战略价值**: 通过同心圆架构拆解 OpenClaw 全部 25 个工具 + 53 个官方 Skill，给出一份「开什么、关什么、为什么」的可直接复用配置手册。

**核心逻辑**:

- **工具 vs Skill 本质区别**：工具是「能不能」的开关（read/write/exec 等），Skill 是「怎么做」的说明书（gog/github/obsidian 等）。安装 Skill 不会新增任何权限，权限完全由 `tools.allow` 控制。
- **三条件缺一不可**：以「读取 Gmail」为例，必须同时满足：① exec 工具已开启（能启动程序）、② gog 桥接工具已安装（能连上 Google）、③ Google 账号已授权（Google 放行）。
- **捆绑 Skill 默认全开**：53 个官方 Skill 中，只要系统上装了对应 CLI 工具，Skill 就自动激活。不是「不装就没有」，而是「不禁用就全开」。必须用 `skills.allowBundled` 白名单模式主动限制。
- **exec 是最高风险工具**：它可以执行任意 shell 命令，包括 `rm -rf`。必须开启审批模式（`"approvals": {"exec": {"enabled": true}}`），每条命令先展示确认再执行，防止 AI 判断失误或 Prompt Injection 攻击。
- **message 工具只给自己发**：message 可向 Discord/Slack/Telegram/WhatsApp/iMessage 发消息。AI 以你名义发出的消息无法撤回，一旦误解语境或被诱导，后果自负。原则：只用于给自己推送通知。
- **1Password Skill 是全有或全无**：一旦授权，整个保险库对 OpenClaw 开放，无法限制只访问特定条目。如需使用，建议创建「AI 专用保险库」，只放愿意共享的密码。
- **nodes 工具（硬件控制）默认关闭**：涵盖远程截图、GPS 定位、摄像头访问。想不出 AI 需要自动开摄像头的场景，关闭。截图需求通过 Telegram 手动发送替代。
- **自动化核心公式**：`cron（定时调度）+ message（推送通知）= 睡觉时也在工作的自动化引擎`。模式固定为：触发条件 + 执行动作 + 结果投递。
- **「最后一公里」永远手动**：结账、对外发消息、公开发言等不可撤销操作，永远亲自完成。browser 可以帮你加购物车，但结账这一步不交给 AI。
- **官方文档只列 18 个工具，实际有 25 个**：多出的包括 sessions 系列工具、agents_list、以及文档未提及的工作流引擎工具（llm_task、lobster），需阅读源码才能发现。
- **OpenClaw vs ChatGPT 核心差异**：ChatGPT 的「同步」= 手机和桌面看到同一段对话历史（可见）；OpenClaw 的「同步」= 对话变成电脑文件夹里的文件，其他工具可直接读取继续处理（可操作）。对话结束后 OpenClaw 还在工作。

---

### 🎯 关键洞察

**同心圆架构逻辑**：

- 第 1 层（8 个核心工具）= 被动响应模式：你问它答，能读文件、执行命令、搜索网页，但不跨会话记忆，不主动推送。
- 第 2 层（17 个高级工具）= 主动助手模式：记住偏好（memory）、控制浏览器（browser）、定时推送（cron + message）。没有第 1 层，第 2 层无法运转。
- 第 3 层（53 个 Skill）= 知识层：教 OpenClaw 如何组合工具完成特定领域任务。

**memory 工具的复利效应**：使用一周后，OpenClaw 知道你用 Astro 建博客、部署在 Azure、习惯用繁体中文，不需要每次重新解释。用得越久，越懂你。

**coding-agent Skill 的潜力**：在 OpenClaw 的 VM 上装 Claude Code，让 OpenClaw 调度编码任务在后台执行。通过 Telegram 说「克隆这个仓库，研究一下，搭个演示站」，它启动 Claude Code 自主执行，完成后推送通知。AI 编排 AI。

---

### 📦 配置/工具详表

#### 全部 25 个工具

| 层级 | 工具 | 功能 | 风险 | 推荐操作 |
|------|------|------|------|---------|
| 1 | read | 读取文件 | 低 | 开启 |
| 1 | write | 写入文件 | 中 | 开启 |
| 1 | edit | 结构化编辑 | 中 | 开启 |
| 1 | apply_patch | 应用补丁 | 中 | 开启 |
| 1 | exec | 执行任意 shell 命令 | 极高 | 开启 + 强制审批模式 |
| 1 | process | 管理后台进程 | 中 | 开启（配合 exec） |
| 1 | web_search | 关键词搜索 | 低 | 开启 |
| 1 | web_fetch | 读取网页内容 | 中 | 开启 |
| 2 | browser | 控制 Chrome（点击/填表/截图） | 高 | 开启，结账步骤手动 |
| 2 | canvas | 可视化工作区/图表 | 低 | 按需，不需要可关 |
| 2 | image | 图像理解分析 | 低 | 开启 |
| 2 | memory_search | 搜索跨会话记忆 | 中 | 开启 |
| 2 | memory_get | 获取跨会话记忆 | 中 | 开启 |
| 2 | sessions_list | 列出会话 | 低 | 开启 |
| 2 | sessions_history | 查看会话历史 | 中 | 开启 |
| 2 | sessions_send | 会话间发消息 | 高 | 开启 |
| 2 | sessions_spawn | 派生子代理 | 高 | 开启 |
| 2 | session_status | 检查会话状态 | 低 | 开启 |
| 2 | message | 向 Discord/Slack/Telegram/WhatsApp/iMessage 发消息 | 极高 | 开启，只给自己发 |
| 2 | nodes | 远程截图/GPS/摄像头 | 极高 | 关闭（想不出场景） |
| 2 | cron | 定时任务调度 | 高 | 开启 |
| 2 | gateway | 让 OpenClaw 重启自身 | 高 | 开启 |
| 2 | agents_list | 列出可用 Agent ID | 低 | 单实例可关，多代理架构开启 |
| 扩展 | llm_task | 工作流中插入 LLM 步骤 | 中 | 不用工作流引擎则关闭 |
| 扩展 | lobster | 工作流引擎 | 中 | 不用工作流引擎则关闭 |

#### 全部 53 个官方 Skill

| 类别 | Skill | 平台/功能 | 风险 | 备注 |
|------|-------|----------|------|------|
| 笔记 | obsidian | Obsidian 本地文件 | 低 | 仓库和 OpenClaw 需在同一机器 |
| 笔记 | notion | Notion 云端 | 中 | 无部署限制，VM 首选 |
| 笔记 | apple-notes | Apple Notes | 低 | 仅本地 Mac 有效 |
| 笔记 | bear-notes | Bear | 低 | 仅本地 Mac 有效 |
| 任务 | things-mac | Things 3 | 低 | Mac 本地 |
| 任务 | apple-reminders | 提醒事项 | 低 | Mac 本地 |
| 任务 | trello | Trello | 中 | 云端 |
| 工作 | gog | Gmail + 日历 + Tasks + Drive + Docs + Sheets | 中 | Google 账号可随时撤销授权 |
| 工作 | himalaya | IMAP/SMTP 收发邮件 | 高 | 只有邮件，无其他 Google 服务 |
| 聊天 | slack | Slack | 中 | 含完整数据访问权 |
| 聊天 | discord | Discord | 中 | 含完整数据访问权 |
| 聊天 | wacli | WhatsApp | 极高 | 含消息历史，作者未装 |
| 聊天 | imsg | iMessage | 极高 | 含消息历史，作者未装 |
| 聊天 | bluebubbles | iMessage（外部服务器） | 高 | — |
| 社交 | bird | X（Twitter） | 极高 | 作者未装 |
| 开发 | github | GitHub 仓库操作 | 中 | 作者已装，远程查 CI/CD 日志 |
| 开发 | coding-agent | 在 VM 上调度 Claude Code | 中 | 潜力大，AI 编排 AI |
| 开发 | tmux | 终端会话管理 | 低 | 作者已装 |
| 开发 | session-logs | 日志搜索 | 低 | 作者已装 |
| 音乐 | spotify-player | Spotify | 低 | — |
| 音乐 | sonoscli | Sonos | 低 | — |
| 音乐 | blucli | BluOS | 低 | — |
| 家居 | openhue | Philips Hue | 低 | — |
| 家居 | eightctl | Eight Sleep | 低 | — |
| 外卖 | food-order | 多平台外卖 | 高 | — |
| 外卖 | ordercli | Foodora | 中 | — |
| 创意 | openai-image-gen | OpenAI 图像生成 | 低 | — |
| 创意 | nano-banana-pro | Gemini 图像生成 | 低 | — |
| 创意 | video-frames | 视频帧提取 | 低 | — |
| 创意 | gifgrep | GIF 搜索 | 低 | — |
| 语音 | sag | ElevenLabs TTS | 低 | — |
| 语音 | openai-whisper | 语音转文字（本地） | 低 | — |
| 语音 | openai-whisper-api | 语音转文字（云端） | 低 | — |
| 语音 | sherpa-onnx-tts | 离线 TTS | 低 | — |
| 安全 | 1password | 1Password 保险库 | 极高 | 全有或全无，建议 AI 专用保险库 |
| AI | gemini | Gemini | 低 | — |
| AI | oracle | Oracle CLI | 低 | — |
| AI | mcporter | MCP 集成 | 中 | — |
| 系统 | clawhub | Skill 管理 | 低 | 作者已装 |
| 系统 | skill-creator | 创建自定义 Skill | 低 | 作者已装 |
| 系统 | healthcheck | 健康检查 | 低 | 作者已装 |
| 系统 | summarize | 摘要 | 低 | 作者已装 |
| 系统 | weather | 天气 | 低 | 作者已装（Daily Brief 用） |
| 地点 | goplaces | Google Places | 低 | — |
| 地点 | local-places | 本地代理 | 低 | — |
| 媒体 | camsnap | RTSP 摄像头 | 中 | — |
| 新闻 | blogwatcher | RSS 监控 | 低 | — |
| 文档 | nano-pdf | PDF 编辑 | 低 | — |
| 监控 | model-usage | 用量追踪 | 低 | — |
| 系统 | peekaboo | macOS UI 控制 | 高 | — |
| 通讯 | voice-call | 语音通话 | 高 | — |
| 创意 | canvas | Canvas 操作 | 低 | — |
| 音乐 | songsee | 音频可视化 | 低 | — |

#### 工具组快捷方式

| 组名 | 包含工具 |
|------|---------|
| group: fs | read、write、edit、apply_patch |
| group: web | web_search、web_fetch |
| group: ui | browser、canvas |
| group: memory | memory_search、memory_get |
| group: sessions | sessions_list、sessions_history、sessions_send、sessions_spawn、session_status |
| group: messaging | message |
| group: nodes | nodes |
| group: automation | cron、gateway |

---

### 🛠️ 操作流程

#### 1. 准备阶段：理解三条件

要让某个 Skill 实际生效，必须同时满足：
- `tools.allow` 中开启了对应工具（如 exec）
- 机器上安装了对应桥接 CLI（如 gog）
- 完成了对应平台的账号授权（如 Google OAuth）

#### 2. 核心执行：复制基础配置

打开 `openclaw.json`，粘贴以下配置作为起点：

```json
{
  "tools": {
    "allow": [
      "read", "write", "edit", "apply_patch",
      "exec", "process",
      "web_search", "web_fetch",
      "browser", "image",
      "memory_search", "memory_get",
      "sessions_list", "sessions_history", "sessions_send", "sessions_spawn", "session_status",
      "message", "cron", "gateway", "agents_list"
    ],
    "deny": ["nodes", "canvas", "llm_task", "lobster"]
  },
  "approvals": {
    "exec": { "enabled": true }
  },
  "skills": {
    "allowBundled": [
      "gog", "github", "tmux", "session-logs",
      "weather", "summarize", "clawhub",
      "healthcheck", "skill-creator"
    ]
  }
}
```

说明：
- 开启 21 个工具，关闭 4 个（nodes/canvas/llm_task/lobster）
- exec 强制审批模式
- Skill 白名单只保留 9 个，其余 44 个全部屏蔽

#### 3. 自动化配置：cron + message 组合

每个自动化 = 一个 cron 条目 + 一个 prompt。prompt 告诉 OpenClaw 用哪些工具、结果发到哪里。

**实际运行的 4 个自动化场景**：

| 场景 | 触发时间 | 执行动作 | 结果投递 |
|------|---------|---------|---------|
| 每日简报 | 每天 6:47 | 拉取今日日程 + 待回复邮件 + 天气 + 夜间 CI/CD 状态 | Telegram |
| 邮件分类 | 每天 2 次 | 扫描收件箱，按紧急程度分类，通讯邮件归档 | Telegram 摘要（含一行标注） |
| CI/CD 监控 | GitHub Actions 失败时 | 读取错误日志，判断可能原因，生成诊断结果 | Telegram |
| 内容调研 | 每天定时 | 收集热门 Reddit 讨论 + HN 线程 + RSS 源，整理写作选题 | Telegram 摘要 |

#### 4. 验证与优化

- 运行 `openclaw doctor` 检查第三方 Skill 的安全状态
- 撤销 Google 授权路径：Google 账号 → 安全性 → 具有账号访问权限的第三方应用 → 找到 gog → 移除访问权限
- 从「每天摩擦最大的那一个流程」开始自动化，跑通后再逐步添加

---

### 💡 具体案例/数据

- **每日简报效果**：每天 6:47 Telegram 收到简报，替代了喝咖啡前查看 5 个应用的习惯
- **邮件管理**：每天 30 分钟的收件箱管理压缩到 5 分钟
- **远程修复生产问题**：在排队买咖啡时，用手机问「查一下这个 PR 构建失败的原因」，OpenClaw 拉取 GitHub Actions 错误日志并给出诊断，当场修复
- **部署架构**：OpenClaw 跑在 Azure VM 上，通过 Telegram 操作；本地 Mac 用 Claude Code 写代码；形成「移动端讨论调研 + 桌面端执行」双轨工作流
- **memory 积累周期**：使用一周后，OpenClaw 已知晓：用 Astro 建博客、部署在 Azure、习惯繁体中文

---

### 📝 避坑指南

- ⚠️ **捆绑 Skill 默认全开**：不是「不装就没有」，是「不禁用就全开」。必须用 `allowBundled` 白名单，否则系统上装了对应 CLI 的 Skill 全部自动激活。
- ⚠️ **exec 不加审批等于交出 root**：开启 exec 但不设审批模式，AI 判断失误或遭遇 Prompt Injection 时，`rm -rf` 级别的命令会直接执行。
- ⚠️ **message 工具被诱导风险**：Prompt Injection 可能诱导 OpenClaw 以你名义向他人发送不当内容，且无法撤回。严格限制只给自己发消息。
- ⚠️ **1Password 全有或全无**：无法限制只访问特定条目。如需使用，创建「AI 专用保险库」隔离。
- ⚠️ **obsidian Skill 有部署限制**：仓库和 OpenClaw 必须在同一台机器。OpenClaw 在 VM、仓库在 Mac 本地，则 obsidian Skill 无效，改用 notion（云端，无限制）。
- ⚠️ **第三方 Skill 不要默认信任**：ClawHub 上 3000+ 第三方 Skill，安装前务必查看 GitHub 仓库源码，并用 `openclaw doctor` 检查。
- ⚠️ **官方文档工具数量不准确**：文档列 18 个，实际 25 个。sessions 系列、agents_list、llm_task、lobster 均未在文档中完整说明，需读源码确认。

---

### 🏷️ 行业标签

#OpenClaw #AI-Agent #自动化 #配置手册 #Prompt-Injection防护 #cron自动化 #工作流 #开发者工具 #Telegram机器人 #Claude-Code

---

**参考原教程**: https://yu-wenhao.com/en/blog/openclaw-tools-skills-tutorial/

---

---
