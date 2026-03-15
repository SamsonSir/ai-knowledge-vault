# AI编程与开发工具

## 19. [2026-02-04]

## 📓 文章 6


> 文档 ID: `ZxpQwHdhMiBSGKkpqKxcdcLhnre`

**来源**: Codex桌面端深度体验：功能、技巧、定价、和Claude Code的正面交锋 | **时间**: 2026-02-04 | **原文链接**: https://mp.weixin.qq.com/s/iBz48C4D...

---

### 📋 核心分析

**战略价值**: Codex 桌面端不是 AI 编程助手的升级版，而是一个「AI 工程团队指挥中心」——开发者角色从写代码者变成项目经理，通过并行 Agent、Skills、Automations、MCP 四层架构实现真正的工程自动化。

**核心逻辑**:

- **并行 Agent 架构打破串行瓶颈**：同时开多个线程，每个线程一个独立 AI agent，最长独立运行 30 分钟。重构数据库、写集成测试、调前端样式三件事同时推进，而非排队等待。Peter Steinberger 切换后生产力翻倍，Dominik Kundel 99.9% 时间在 Codex 桌面端。
- **Git Worktree 做 Agent 隔离，防止多 Agent 互踩**：每个 agent 在代码的独立副本里工作，改完通过 diff 面板逐行审查，满意合并，不满意直接丢弃，原始代码零污染。这是 Codex 最关键的工程设计，与 AI 能力无关。
- **Skills 系统 = 用 Markdown 文件给 AI 装技能包**：在 `~/.codex/skills/`（个人）或 `.codex/skills/`（项目团队共享）下创建文件夹，放一个 `SKILL.md`，用自然语言描述操作步骤，无需代码、无需 API 调用。内置技能：Figma 设计稿生成代码、一键部署到 Vercel/Netlify/Cloudflare/Render、读取 Linear 看板、GPT Image 生图、创建 PDF 和电子表格。整个系统开源。
- **Automations 实现定时自动化流水线**：OpenAI 内部已在用：每天早上自动整理 GitHub Issues 优先级、CI 构建失败自动分析原因并给出建议、每天生成发布简报、定期扫描代码库找潜在 bug。结果进审核队列，人工确认或驳回，AI 不自作主张。组合玩法：`Automation 定时触发 → 调用 Skill → 通过 MCP 连接 GitHub/Slack/Linear → 结果回审核队列`。
- **MCP 协议打通全工具链**：配置在 `~/.codex/config.toml`，CLI 和 IDE 扩展共享同一份。可接入 GitHub、Figma、Linear、Sentry、Playwright、Chrome DevTools、Docker。实战：Slack 里说 `@Codex 修 #123 bug`，它自动读 GitHub 代码、修复、创建 PR、把链接回复到 Slack。自动 PR 审查流水线：新 PR 触发 → GitHub MCP 读取变更 → Codex 分析 → 自动发评论 → 开发者回复 `codex fix it` → 直接提交修复。
- **AGENTS.md 是多 Agent 的统一规则手册**：放在项目里的 Markdown 文件，已成行业标准，由 Linux 基金会下的 Agentic AI Foundation 管理，OpenAI Codex、Google Jules、Cursor、Amp、Factory 共同参与制定。内容包含：项目结构、编码规范（如 TypeScript strict、禁止 any）、测试命令（如 `pnpm test`）、Git 规范（Conventional Commits）、禁区（不改 schema 文件、不删测试、加新依赖先问）。支持层级覆盖：全局默认 → 项目级 → 子目录级，越深层优先级越高。用 `/init` 命令自动生成。
- **推理强度五档，日常用 Medium 就够**：Minimal / Low / Medium / High / xHigh 五档。日常编码 Medium，又快又省。只有最复杂的架构设计才开 High 或 xHigh。Low 档被社区批评为"不足以用于实际代码生成"。
- **权限管理采用渐进信任模式**：从 Read Only 开始，信任后切到 Workspace Write，必要时再开 Full Access。需要 AI 访问额外目录用 `--add-dir`，不要直接关闭沙箱。
- **实际战绩**：OpenAI 内部 4 人团队用 Codex 在 28 天内完成 Sora Android 应用；单条 prompt 构建完整赛车游戏（8 张地图、多辆赛车、道具系统），消耗 700 万 token；社区报告 Codex 预审 PR 减少约 60% 人工审查时间；Superhuman 用它提高测试覆盖率，产品经理也能直接写代码。
- **最大槽点**：只支持 macOS，无 Windows、无 Linux，Windows 版"正在开发中"但无时间表。Codex 发布被多位评论者认为是对 Anthropic 的回应——Claude Code 6 个月做到 10 亿美元年化收入，OpenAI 曾出价 30 亿美元收购 Windsurf 被拒后自己做。

---

### 🎯 关键洞察

**开发者只有 16% 的时间在写代码**（Atlassian 报告），其余 84% 是会议、审查、调试、沟通。传统 AI 编程工具只优化了这 16%，且省下的时间几乎被额外的审查和调试需求抵消。

Codex 的反驳逻辑：多 Agent 并行 + Automations 恰恰在优化那 84%——自动化 issue 整理、PR 审查、CI 分析，这些都不是"写代码"。这是 Codex 和其他 AI 编程工具的本质差异。

OpenAI 给出的开发者新角色定义：**项目经理**。需求、架构、审美、判断由人负责，机械性实现交给 AI 团队。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| Git Worktree 隔离 | 新建线程时选择"Worktree 模式" | 每个 agent 在独立代码副本工作，互不干扰 | 合并前必须用 `/diff` 逐行审查 |
| 个人 Skills | `~/.codex/skills/<skill-name>/SKILL.md` | 纯自然语言描述，无需代码 | 个人专属，不随项目共享 |
| 团队 Skills | `.codex/skills/<skill-name>/SKILL.md` 提交到 Git | 团队共享技能包 | 整个系统开源 |
| MCP 配置 | `~/.codex/config.toml` | CLI 和 IDE 扩展共享同一份配置 | 设一次到处能用 |
| AGENTS.md 层级 | 全局 → 项目根目录 → 子目录 | 越深层优先级越高 | 用 `/init` 自动生成初始版本 |
| 推理强度 | Minimal / Low / Medium / High / xHigh | Medium 日常够用，High/xHigh 留给架构设计 | Low 档质量差，慎用于实际代码生成 |
| 权限模式 | Read Only → Workspace Write → Full Access | 渐进信任，降低风险 | 额外目录用 `--add-dir`，不要直接关沙箱 |
| 上下文压缩 | `/compact` 命令 | 压缩上下文保留核心信息，可持续工作数小时 | 对话过长时主动触发，防止走偏 |

---

### 🛠️ 操作流程

1. **准备阶段**:
   - 在项目根目录运行 `/init` 自动生成 `AGENTS.md`，手动补充：项目结构说明、编码规范（TypeScript strict、禁止 any 等）、测试命令（`pnpm test`）、Git 规范（Conventional Commits）、禁区（不改 schema、不删测试、加依赖先问）
   - 在 `~/.codex/config.toml` 配置 MCP 连接（GitHub、Slack、Linear、Sentry 等）
   - 按需创建 Skills：`~/.codex/skills/<name>/SKILL.md`（个人）或 `.codex/skills/<name>/SKILL.md`（团队）

2. **核心执行**:
   - 拆解任务，开多个线程并行推进，每个线程一个 agent，最长跑 30 分钟
   - 新线程选择 Worktree 模式，确保 agent 在独立代码副本工作
   - Prompt 写法：指定文件名 + 行号 + 错误信息 + 验证命令（如"修复 login.ts 第 42 行 TimeoutError，原因是 Redis 连接超时，改完跑 npm test"）
   - 不要让 AI 先汇报计划，直接让它干活
   - 批量读文件：一口气说"先读 auth.ts、db.ts、routes.ts，然后基于这三个文件修改"，三轮变一轮
   - 给约束："不要动 config/ 目录"、"用已有的 DatabaseClient 类"
   - 推理强度日常选 Medium

3. **验证与优化**:
   - 用 `/diff` 逐行审查 AI 改动，对问题行加评论让 AI 修改
   - 满意则合并，不满意直接丢弃
   - AI 彻底迷路时用 `/new` 从头来，不要硬撑
   - 对话过长时用 `/compact` 压缩上下文
   - 用 `/review` 让 AI 扫描代码找问题
   - 配置 Automations：定时触发 → 调用 Skill → MCP 连接工具链 → 结果进审核队列

---

### 💡 具体案例/数据

- OpenAI 内部 4 人团队，28 天完成 Sora Android 应用
- 单条 prompt 构建完整赛车游戏：8 张地图、多辆赛车、道具系统，消耗 700 万 token，上下文窗口 40 万 token
- Peter Steinberger 独自构建整个 OpenClaw 项目，切换 Codex 后生产力约翻倍
- Dominik Kundel：99.9% 时间在 Codex 桌面端
- Cisco 工程团队用于加速产品组合开发
- Superhuman 用于提高测试覆盖率，产品经理也能直接写代码
- 社区报告：Codex 预审 PR 减少约 60% 人工审查时间
- Atlassian 报告：开发者只有 16% 时间在写代码，其余 84% 是会议、审查、调试、沟通
- Claude Code 6 个月年化收入达 10 亿美元；OpenAI 曾出价 30 亿美元收购 Windsurf 被拒

---

### 📝 避坑指南

- ⚠️ 不要让 AI 先汇报计划——会消耗大量 token 输出计划书，然后执行到一半停下来，直接让它干活
- ⚠️ 不要用模糊 prompt——"帮我改进代码"是最差写法，必须指定文件名、行号、错误信息、验证命令
- ⚠️ 不要逐个读文件——批量一次性给出所有需要读的文件，省 token 省时间
- ⚠️ 不要不给约束——没有约束的 AI 会乱改任何地方，必须明确禁区
- ⚠️ 不要用 Low 推理强度做实际代码生成——社区反馈质量不足，日常用 Medium
- ⚠️ 不要直接关闭沙箱——需要访问额外目录用 `--add-dir`，权限从 Read Only 开始渐进开放
- ⚠️ 不要忽略 AGENTS.md——没有它，多 Agent 生成的代码风格五花八门，禁区乱改，测试不跑
- ⚠️ 平台限制：目前只支持 macOS，Windows/Linux 用户无法使用，Windows 版无明确时间表
- ⚠️ GPT-5.2 Codex 的"ChatGPT 风格语气"会出现在代码注释中，需要在 AGENTS.md 里明确规范注释风格

---

### 🏷️ 行业标签

#Codex #OpenAI #AI编程 #多Agent #GitWorktree #MCP #AGENTS.md #Skills #Automations #ClaudeCode #开发者工具 #工程自动化

---

---
