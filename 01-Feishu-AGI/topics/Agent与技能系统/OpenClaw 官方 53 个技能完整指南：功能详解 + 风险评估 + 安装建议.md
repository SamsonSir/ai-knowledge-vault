# Agent与技能系统

## 66. [2026-02-19]

## 📘 文章 3


> 文档 ID: `AphawozhlimpPgksAV9ce7Qrnjf`

**来源**: OpenClaw 官方 53 个技能完整指南：功能详解 + 风险评估 + 安装建议 | **时间**: 2026-02-18 | **原文链接**: `https://mp.weixin.qq.com/s/f3im9z__..`

---

### 📋 核心分析

**战略价值**: ClawHub 5700+ 技能中仅 53 个官方内置，本文逐一拆解功能/平台/风险，给出最小安全配置路径，帮你在 ClawHavoc 事件（341 个恶意技能，占比 12%）背景下做出最安全的选择。

**核心逻辑**:

- **Tool vs Skill 本质区别**：Tool 是「器官」（read/write/exec 决定能不能做），Skill 是「教科书」（教怎么组合 Tool 完成任务）。安装 Skill 不赋予新权限，只是说明书。
- **默认全加载是风险源**：53 个官方技能默认全部自动加载，必须用 `skills.allowBundled` 白名单模式主动限制，只启用你真正需要的。
- **最小安全配置只需 9 个技能**：`gog, github, tmux, session-logs, weather, summarize, clawhub, healthcheck, skill-creator`，其余按需追加。
- **VM 部署有平台限制**：obsidian/apple-notes/bear-notes/things-mac/apple-reminders 均依赖本地 Mac 文件系统，OpenClaw 跑在 VM 上时这些技能无法使用，云端 Notion 是 VM 环境唯一无限制的笔记方案。
- **消息类技能的不可逆风险**：wacli/imsg/bird 等技能让 AI 以你名义发出的消息无法撤回，且提供完整历史消息访问权，与仅发送的 `message` 工具有本质区别。
- **1password 是全库或全无**：一旦授权，AI 可访问整个密码库所有条目，无法限制单条目。若必须用，建议创建「AI 专用密码库」隔离。
- **gog 是性价比最高的单个技能**：一个技能覆盖 Gmail + Calendar + Tasks + Drive + Docs + Sheets，支持自然语言指令（「今天有什么会议」「给 Sarah 发跟进邮件」），权限可随时在 Google 账户设置撤销。
- **summarize 是时间杠杆最高的技能**：40 分钟播客 20 秒出摘要，15 页 PDF 一段话总结，有用户报告每周节省 5 小时以上。
- **coding-agent 实现「AI 调度 AI」**：通过 Telegram 发指令「克隆这个仓库，研究它，做个 demo 网站」，它自动调用 Codex/Claude Code 等在后台执行，无需手动介入。
- **ClawHavoc 安全背景**：2026 年 2 月安全研究团队在 ClawHub 发现 341 个恶意技能（约占总数 12%），安装任何第三方技能前必须审查源码。

---

### 📦 配置/工具详表

#### 最小安全配置（推荐直接复制）

```json
"skills": {
  "allowBundled": [
    "gog", "github", "tmux",
    "session-logs", "weather", "summarize",
    "clawhub", "healthcheck", "skill-creator"
  ]
}
```

#### 全部 53 个官方技能详表

**一、笔记类（4 个）**

| 技能 | 平台 | 风险 | 说明 | 注意事项 |
|------|------|------|------|---------|
| obsidian | Obsidian | 低 | 创建/编辑/搜索本地笔记库 | 需要 read/write 工具；VM 环境无法访问本地 Mac 笔记库 |
| notion | Notion | 中 | 管理笔记、数据库、页面 | 需要 Notion API token；云端服务，VM 无限制，VM 首选 |
| apple-notes | Apple 备忘录 | 低 | 集成 Apple 备忘录 | 仅限 Mac 本地运行 |
| bear-notes | Bear | 低 | 集成 Bear 笔记应用 | 仅限 Mac 本地运行 |

**二、任务管理类（3 个）**

| 技能 | 平台 | 风险 | 说明 | 注意事项 |
|------|------|------|------|---------|
| things-mac | Things 3 | 低 | 集成 Things 3 任务管理 | 仅限 Mac 本地运行 |
| apple-reminders | Apple 提醒事项 | 低 | 集成 Apple 提醒事项 | 仅限 Mac 本地 |
| trello | Trello | 中 | 管理看板、卡片、列表、团队协作 | 需要 Trello API key；已装 gog 则 Google Tasks 已覆盖，可不装 |

**三、办公/邮件类（2 个）**

| 技能 | 平台 | 风险 | 说明 | 注意事项 |
|------|------|------|------|---------|
| gog | Google Workspace | 中 | 覆盖 Gmail/Calendar/Tasks/Drive/Docs/Sheets，支持自然语言指令 | 通过 gog CLI 集成；权限可在 Google 账户设置随时撤销；多评测者评为「只装一个就装这个」 |
| himalaya | IMAP/SMTP 邮件 | 高 | 通用邮件客户端，收发邮件 | 需存储邮箱密码，风险较高；适合非 Google 邮箱用户 |

**四、消息/社交类（7 个）**

| 技能 | 平台 | 风险 | 说明 | 注意事项 |
|------|------|------|------|---------|
| wacli | WhatsApp | 极高 | 读取消息历史、发送消息，完整访问 WhatsApp 数据 | AI 发出消息不可撤回 |
| imsg | iMessage | 极高 | 读取和发送 iMessage | 仅限 Mac；AI 发出消息不可撤回 |
| bluebubbles | iMessage（外部） | 高 | 通过 BlueBubbles 服务器访问 iMessage | 不限于本地 Mac |
| slack | Slack | 中 | 发布更新、回复线程、管理频道，支持富文本和 Block Kit | — |
| discord | Discord | 中 | 管理频道、发送消息、自动化社区管理 | — |
| bird | X (Twitter) | 极高 | 发布、搜索、互动 | AI 发布内容不可撤回，且以你名义发布 |
| （第7个技能原文未单独列出，消息类共7个，原文表格实际列出6个） | — | — | — | — |

**五、开发工具类（4 个）**

| 技能 | 平台 | 风险 | 说明 | 注意事项 |
|------|------|------|------|---------|
| github | GitHub | 中 | 通过 gh CLI 管理 Issue/PR/仓库，支持 OAuth | 权限可控；可远程检查 CI/CD 故障，拉取 GitHub Actions 错误日志 |
| coding-agent | AI 编码助手 | 中 | 调用 Codex/Claude Code 等在后台执行任务，实现「AI 调度 AI」 | 可通过 Telegram 远程触发复杂编码任务 |
| tmux | 终端会话 | 低 | 管理多个终端会话，并行执行任务 | — |
| session-logs | 日志搜索 | 低 | 搜索和分析过去的对话日志 | — |

**六、音乐类（4 个）**

| 技能 | 平台 | 风险 | 说明 |
|------|------|------|------|
| spotify-player | Spotify | 低 | 控制播放、搜索音乐、管理播放列表 |
| sonoscli | Sonos | 低 | 控制 Sonos 智能音箱系统 |
| blucli | BluOS | 低 | 控制 BluOS 音频设备 |
| songsee | 音频可视化 | 低 | 生成音频波形图等可视化内容 |

**七、智能家居类（2 个）**

| 技能 | 平台 | 风险 | 说明 |
|------|------|------|------|
| openhue | Philips Hue | 低 | 控制智能灯光，调整亮度/颜色/场景 |
| eightctl | Eight Sleep | 低 | 控制 Eight Sleep 智能床垫温度 |

**八、外卖/食品类（2 个）**

| 技能 | 平台 | 风险 | 说明 | 注意事项 |
|------|------|------|------|---------|
| food-order | 多平台外卖 | 高 | 多平台订餐 | 涉及支付操作，风险较高 |
| ordercli | Foodora | 中 | 通过 Foodora 平台订餐 | — |

**九、创意/图像类（5 个）**

| 技能 | 平台 | 风险 | 说明 | 注意事项 |
|------|------|------|------|---------|
| openai-image-gen | OpenAI DALL-E | 低 | 使用 DALL-E API 生成图片 | 需要 OpenAI API key |
| nano-banana-pro | Google Gemini | 低 | 使用 Gemini 生成图像 | — |
| video-frames | 视频帧提取 | 低 | 从视频中提取关键帧 | — |
| gifgrep | GIF 搜索 | 低 | 搜索和发送 GIF 动图 | — |
| canvas | Canvas 画布 | 低 | 可视化画布，用于图表和流程图 | — |

**十、语音类（5 个）**

| 技能 | 平台 | 风险 | 说明 | 注意事项 |
|------|------|------|------|---------|
| sag | ElevenLabs TTS | 低 | 生成高质量语音 | 需要 ElevenLabs API key |
| openai-whisper | Whisper 本地 STT | 低 | 本地运行语音识别，无需网络 | — |
| openai-whisper-api | Whisper 云端 STT | 低 | 云端语音识别 | 需要 OpenAI API key |
| sherpa-onnx-tts | 离线 TTS | 低 | 完全离线文字转语音 | — |
| voice-call | 语音通话 | 高 | 让 OpenClaw 进行语音通话 | 涉及实时通信，风险较高 |

**十一、密码管理类（1 个）**

| 技能 | 平台 | 风险 | 说明 | 注意事项 |
|------|------|------|------|---------|
| 1password | 1Password | 极高 | 查找密码、自动登录、填充表单 | 权限模型全部或无，一旦授权可访问整个密码库所有条目；建议创建「AI 专用密码库」隔离 |

**十二、AI 模型类（3 个）**

| 技能 | 平台 | 风险 | 说明 | 注意事项 |
|------|------|------|------|---------|
| gemini | Google Gemini | 低 | 集成 Gemini，用于实时搜索研究任务 | 作为补充 AI，适合需要最新新闻/产品评测/最新法规等实时信息场景 |
| oracle | Oracle CLI | 低 | Oracle 命令行工具集成 | — |
| mcporter | MCP 集成 | 中 | Model Context Protocol，连接其他 MCP 服务 | — |

**十三、系统/工具类（6 个）**

| 技能 | 平台 | 风险 | 说明 | 注意事项 |
|------|------|------|------|---------|
| summarize | 内容摘要 | 低 | 对网页/PDF/播客/长文智能摘要；40 分钟播客 20 秒出摘要，15 页 PDF 一段话总结 | 用户报告每周节省 5 小时以上 |
| weather | 天气预报 | 低 | 获取本地天气预报 | 免费、无需 API key、即装即用 |
| clawhub | 技能管理 | 低 | 管理技能的安装/更新/删除 | — |
| skill-creator | 技能创建 | 低 | 创建自定义技能 | — |
| healthcheck | 健康检查 | 低 | 检查 OpenClaw 运行状态和配置 | — |
| peekaboo | macOS UI 控制 | 高 | 捕获和自动化 macOS 用户界面 | 仅限 Mac |

**十四、地点/导航类（2 个）**

| 技能 | 平台 | 风险 | 说明 |
|------|------|------|------|
| goplaces | Google Places | 低 | 搜索附近餐厅/商店/景点 |
| local-places | 本地代理 | 低 | 本地地点代理服务 |

**十五、媒体/监控类（3 个）**

| 技能 | 平台 | 风险 | 说明 | 注意事项 |
|------|------|------|------|---------|
| camsnap | RTSP 摄像头 | 中 | 访问 RTSP 协议监控摄像头，截图和监控 | — |
| blogwatcher | RSS 监控 | 低 | 监控 RSS 源，跟踪博客和新闻更新 | — |
| model-usage | 用量跟踪 | 低 | 跟踪 AI 模型使用量和费用 | — |

**十六、文档类（1 个）**

| 技能 | 平台 | 风险 | 说明 |
|------|------|------|------|
| nano-pdf | PDF 编辑 | 低 | 编辑和处理 PDF 文件 |

#### 风险等级汇总

| 风险等级 | 数量 | 代表技能 |
|---------|------|---------|
| 低风险 | 30 个 | summarize, weather, tmux, spotify-player 等 |
| 中风险 | 12 个 | gog, github, notion, slack, discord, trello, mcporter 等 |
| 高风险 | 6 个 | himalaya, food-order, voice-call, peekaboo, bluebubbles, wacli（部分） |
| 极高风险 | 5 个 | wacli, imsg, bird, 1password，及消息类完整访问技能 |

---

### 🛠️ 操作流程

**第一周：必装 Top 3**

1. 安装 `gog`（Google 全套件：邮件 + 日历 + 文档）
2. 安装 `summarize`（内容摘要，每周节省 5+ 小时）
3. 安装 `weather`（免费、无需 API key、即装即用）

配置白名单（先用最小集）：
```json
"skills": {
  "allowBundled": ["gog", "summarize", "weather"]
}
```

**第二周：按角色追加**

| 角色 | 追加技能 |
|------|---------|
| 开发者 | `github` + `tmux` + `session-logs` + `coding-agent` |
| 笔记用户（云端/VM） | `notion` |
| 笔记用户（本地 Mac） | `obsidian` |
| 自动化用户 | 配合 `cron` + `message` 工具做每日简报 |

**验证与优化**

- 用 `healthcheck` 技能检查运行状态
- 用 `session-logs` 回顾历史操作，确认权限范围符合预期
- 定期用 `clawhub` 检查技能更新

---

### 💡 具体案例/数据

- **github 实战场景**：在外面时通过手机问「检查为什么这个 PR 构建失败了」，它拉取 GitHub Actions 错误日志并返回原因。
- **coding-agent 实战场景**：通过 Telegram 发「克隆这个仓库，研究它，做个 demo 网站」，自动调度 Codex/Claude Code 在后台完成。
- **summarize 效率数据**：40 分钟播客 → 20 秒出摘要；15 页 PDF → 一段话总结关键点；用户报告每周节省 5 小时以上。
- **ClawHavoc 事件**：2026 年 2 月，安全研究团队在 ClawHub 发现 341 个恶意技能，约占总数 5700+ 的 12%。
- **gog 自然语言指令示例**：「今天有什么会议」「给 Sarah 发一封跟进邮件」。

---

### 📝 避坑指南

- ⚠️ **默认全加载陷阱**：53 个技能默认全部自动加载，不主动配置 `allowBundled` 白名单就等于全开放，必须手动限制。
- ⚠️ **VM 环境本地技能失效**：obsidian/apple-notes/bear-notes/things-mac/apple-reminders 在 VM 中均无法使用，VM 用户直接选 notion。
- ⚠️ **消息不可撤回**：wacli/imsg/bird 让 AI 以你名义发出的内容无法撤回，且提供完整历史消息访问权，与仅发送的 `message` 工具有本质区别，谨慎安装。
- ⚠️ **1password 全库暴露**：权限模型是全部或无，无法限制单条目访问。若必须用，创建「AI 专用密码库」只放愿意让 AI 看到的密码。
- ⚠️ **food-order 涉及支付**：外卖类技能涉及真实支付操作，结账步骤建议保留手动确认。
- ⚠️ **第三方技能安全风险**：ClawHavoc 事件证明 ClawHub 上约 12% 技能为恶意技能，安装任何非官方技能前必须审查源码。
- ⚠️ **三条安全原则**：① 想不到用途就不开；② 能力越大管控越严（给 `exec` 开启审批，`message` 只发给自己）；③ 最后一步永远手动（结账、对外发消息、公开发布等不可逆操作由你亲手完成）。

---

### 🏷️ 行业标签

#OpenClaw #ClawHub #AI助手 #技能管理 #安全配置 #自动化工作流 #GoogleWorkspace #开发工具 #白名单配置

---

---
