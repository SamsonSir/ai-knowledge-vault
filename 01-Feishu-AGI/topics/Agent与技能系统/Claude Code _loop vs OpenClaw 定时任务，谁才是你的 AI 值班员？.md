# Agent与技能系统

## 111. [2026-03-08]

## 📒 文章 7


> 文档 ID: `F6YGwh4tNifnhrkmj77cyHk9n8g`

**来源**: Claude Code /loop vs OpenClaw 定时任务，谁才是你的 AI 值班员？ | **时间**: 2026-03-07 | **原文链接**: `https://mp.weixin.qq.com/s/yq2Clkin...`

---

### 📋 核心分析

**战略价值**: Claude Code /loop（会话级临时闹钟）与 OpenClaw Cron（持久化调度器）定位互补，前者零配置即用，后者适合构建 7×24 自动化工作流，选型取决于任务是"临时盯活儿"还是"长期值守"。

**核心逻辑**:

- **发布背景**: 2026-03-07，Claude Code 更新至 v2.1.71，新增 `/loop` 命令，底层将自然语言指令转换为 cron 表达式执行，最小粒度 1 分钟（秒级输入会向上取整）
- **`/loop` 基本语法**: `/loop <间隔> <prompt>`，间隔单位支持 `s / m / h / d`；不写间隔默认 10 分钟；可嵌套其他 slash 命令（如 `/loop 20m /review-pr 1234`）
- **`/loop` 自然语言支持**: 无需 `/loop` 前缀也可触发，如 `remind me at 3pm to push the release branch`，Claude 自动判断是否创建定时任务
- **`/loop` 硬性限制**: 会话级（关终端即消失）、3 天自动过期、单会话上限 50 个任务、不补跑（休眠/断网期间错过的任务不会补执行）、重启后全部消失
- **`/loop` 防拥堵机制**: 内置 jitter（随机偏移），避免整点所有任务同时触发；时区按本地时区解释
- **OpenClaw Cron 持久化机制**: 任务存储于 `~/.openclaw/cron/jobs.json`，重启不丢、断电不丢，只要 Gateway 在运行任务就持续执行，无时间上限
- **OpenClaw 三种调度方式**: `--at`（ISO 8601 单次执行）、`--every`（毫秒精度固定间隔，比 `/loop` 精度高三个数量级）、`--cron`（标准 5 字段 cron 表达式 + IANA 时区）
- **OpenClaw 隔离执行模式**: `--session isolated` 每次执行创建全新专用会话，不污染聊天记录；隔离模式可单独指定模型（如 Opus）和思考级别（如 `xhigh`）
- **OpenClaw 多渠道投递**: 结果可推送至 Slack、Discord、Telegram、WhatsApp、Signal；三种模式：`announce`（发频道）、`webhook`（POST 到 URL）、`none`（仅内部记录）；`/loop` 结果只能显示在当前终端
- **OpenClaw 错误重试**: 单次任务最多重试 3 次（临时错误）；周期任务指数退避重试（30s → 1m → 5m → 15m → 60m）；`/loop` 无任何重试机制

---

### 🎯 关键洞察

**为什么两者不是竞品而是搭档**：

`/loop` 解决的是开发过程中的"即时轮询"需求——你在写代码，顺手设一个，活儿干完关终端，任务自动消失，零配置零成本。OpenClaw Cron 解决的是"基础设施级自动化"需求——配好一次，永远在线，结果推到 IM，异常告警，无需人值守。两者的核心差异不是功能强弱，而是**生命周期**：一个是临时闹钟，一个是排班值班员。

**精度差异的实际影响**：`/loop` 最小 1 分钟，OpenClaw 支持毫秒级 `--every`，对于需要秒级心跳检查的监控场景，`/loop` 天然不适用。

---

### 📦 配置/工具详表

| 维度 | `/loop` | OpenClaw Cron |
|------|---------|---------------|
| 持久化 | 否，会话级 | 是，`~/.openclaw/cron/jobs.json` |
| 重启后保留 | 否 | 是 |
| 最长存活 | 3 天自动过期 | 无限制 |
| 精度 | 分钟级（秒级向上取整） | 毫秒级 |
| 单会话上限 | 50 个任务 | 无明确限制 |
| 投递渠道 | 仅当前终端 | Slack / Discord / Telegram / WhatsApp / Signal |
| 隔离执行 | 否 | 支持，`--session isolated` |
| 错误重试 | 无 | 指数退避（30s→1m→5m→15m→60m） |
| 上手门槛 | 极低，一行命令 | 需部署 Gateway |
| 时区支持 | 本地时区 | IANA 时区（`--tz "America/Los_Angeles"`） |
| 适合场景 | 临时盯活儿 | 长期自动化工作流 |

---

### 🛠️ 操作流程

**1. 使用 Claude Code `/loop`**

```bash
# 每 5 分钟检查部署状态
/loop 5m check if the deployment finished

# 每 2 小时检查构建（不写间隔默认 10 分钟）
/loop check the build every 2 hours

# 嵌套执行其他 slash 命令，每 20 分钟 review PR
/loop 20m /review-pr 1234

# 自然语言一次性提醒（无需 /loop 前缀）
remind me at 3pm to push the release branch

# 查看所有在跑的任务（直接用自然语言问 Claude）
# 取消任务
cancel the deployment check
```

底层工具：`CronCreate`、`CronList`、`CronDelete`

**2. 使用 OpenClaw Cron**

```bash
# 单次执行（--at，ISO 8601 时间戳）
openclaw cron add --name "Reminder" \
  --at "2026-03-08T16:00:00Z" \
  --session main --wake now --delete-after-run

# Cron 表达式 + 时区 + 推送到 Slack
openclaw cron add --name "Morning brief" \
  --cron "0 7 * * *" --tz "America/Los_Angeles" \
  --session isolated \
  --message "Summarize overnight updates" \
  --channel slack --to "channel:C1234567890"
```

**3. 持久化替代方案（不想上 OpenClaw）**

- **Claude Desktop 桌面端**：Cowork 模式支持 `/schedule` 命令，任务绑定桌面端而非终端会话，桌面端开着就不丢，适合个人场景
- **GitHub Actions `schedule` 触发器**：将 prompt 写成 workflow，用 `schedule` + cron 表达式触发，每次拉起 Claude Code 执行，适合团队协作场景

---

### 💡 具体案例/数据

**`/loop` 典型场景**：
- 跑了个部署，`/loop 5m check if the deployment finished`，部署完关终端走人
- PR 提上去，`/loop 20m /review-pr 1234`，盯 CI 状态

**OpenClaw Cron 典型场景**：
- 每天早上 7 点（LA 时区）生成 GitHub 活动日报推送到 Slack：`--cron "0 7 * * *" --tz "America/Los_Angeles"`
- 每周五下午自动 review 所有 open PR
- 每小时检查服务器状态，异常时发 Telegram 告警

**隔离模式高级用法**：`--session isolated` + 指定 Opus 模型 + 思考级别 `xhigh`，适合跑长任务、生成高质量报告，不污染主聊天记录

---

### 📝 避坑指南

- ⚠️ `/loop` 秒级间隔会被静默向上取整到分钟，底层是 cron，别指望秒级精度
- ⚠️ `/loop` 关终端即失效，不要用它做任何需要持久化的任务，否则任务静默消失不会有任何提示
- ⚠️ `/loop` 无错误重试，任务失败即失败，不适合网络不稳定或有限流风险的场景
- ⚠️ OpenClaw 需要先部署 Gateway，上手有一定门槛，临时需求用它反而是杀鸡用牛刀
- ⚠️ OpenClaw 隔离模式（`--session isolated`）不会污染主聊天记录，长任务务必用隔离模式，否则会把主会话上下文搞乱

---

### 🏷️ 行业标签

#ClaudeCode #OpenClaw #AI调度 #定时任务 #自动化工作流 #开发工具 #AGI基础设施

---

---
