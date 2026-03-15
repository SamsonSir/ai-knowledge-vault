# AI编程与开发工具

## 21. [2026-02-06]

## 📓 文章 6


> 文档 ID: `Ih20wQD9bit7S4kUNNZc3BBAnAL`

**来源**: Claude Code 之父 Boris 的最佳实践：23 条技巧，10 倍生产力 | **时间**: 2026-02-02 | **原文链接**: `https://mp.weixin.qq.com/s/G56aWwnB...`

---

### 📋 核心分析

**战略价值**: Boris Cherny（Claude Code 创建者）通过并行化 + Plan Mode + CLAUDE.md 积累 + 验证循环四个支柱，将 AI 编码效率提升至 10 倍，核心不在于复杂配置，而在于工作流纪律。

**核心逻辑**:

- **并行是第一生产力杠杆**：Boris 同时运行 15-20 个 Claude 会话（本地 5 个 + Web 5-10 个 + 手机若干），约 10-20% 会话会被放弃，这是正常损耗，并行收益远超损耗。
- **Opus 慢但总时间更短**：Opus 4.5 with thinking 单次 2 分钟但只需 1 次迭代；Sonnet 单次 1 分钟但需 5 次纠正，总耗时 5 分钟。真正瓶颈是人类纠正时间，不是 AI 处理时间。
- **CLAUDE.md 是团队复利资产**：Boris 团队每周贡献多次，每次 Claude 犯错就添加规则，约 2500 tokens 为最佳长度。提交到 git，全团队共享，Claude 越用越懂项目。
- **Plan Mode 是"量好再切"**：Shift+Tab 两次进入，与 Claude 反复讨论直到计划满意，再切换自动接受模式一次性执行。跳过计划看似省时，实际修复错误花更多时间。
- **验证循环是质量倍增器**：给 Claude 验证能力，最终结果质量提升 2-3 倍。Boris 用 Chrome 扩展让 Claude 测试每一个提交到 claude.ai/code 的改动，打开浏览器、测试 UI、迭代直到 UX 良好。
- **Slash Command 消灭重复劳动**：`/commit-push-pr` 每天使用几十次，用内联 bash `$(...)` 预计算 git status 等上下文，减少模型来回调用次数，命令存储在 `.claude/commands/` 并提交 git。
- **PostToolUse Hook 自动格式化**：Claude 写代码后自动触发 `bun run format`，处理最后 10% 格式问题，避免 CI 因格式错误失败。
- **MCP 让 Claude 操作外部系统**：Boris 6 个月没写过一行 SQL，全靠 Claude 通过 BigQuery CLI 完成。Slack MCP 让 Claude 直接搜索和发布消息，工具按需加载不消耗上下文。
- **Git Worktrees 是团队公认最大生产力提升**：每个 worktree 独立目录，可同时运行不同 Claude 会话不冲突，配合 shell 别名（za/zb/zc）一键跳转。
- **让 Claude 自己写 CLAUDE.md 规则**：每次纠正后说"更新你的 CLAUDE.md 这样你下次就不会犯同样的错误"，Claude 擅长为自己编写规则，比人工编写更高效。

---

### 🎯 关键洞察

**双 Claude 审查策略**：Claude A 写计划 → Claude B 以"Staff Engineer"角色审查（新鲜上下文、更少偏见）→ 修改计划 → 执行。新鲜上下文的价值在于避免第一个 Claude 的路径依赖和确认偏误。

**Subagent vs Slash Command 本质区别**：Slash Command 在当前会话执行，共享上下文；Subagent 在独立会话执行，适合高容量操作（测试输出、日志分析、深度代码搜索）。触发方式极简：提示词末尾加 `"use subagents"` 即可。

**语音输入被严重低估**：说话速度是打字的 3 倍，macOS 按 fn 两次激活，适合详细描述复杂需求。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| iTerm2 系统通知 | iTerm2 System Notifications 配置 | Claude 需要输入时自动提醒 | 多标签并行时必备，否则会漏掉等待中的会话 |
| Web 会话后台化 | `claude "任务描述" &` | 长任务交后台运行 | 约 10-20% 会话会被放弃，正常现象 |
| Web 会话拉回本地 | `claude --teleport <session-id>` | 在本地终端继续 Web 会话 | 需要记录 session-id |
| CLAUDE.md | 提交到 git，约 2500 tokens | 团队知识积累，Claude 越用越懂项目 | 不要写太长，定期清理不再相关的规则 |
| GitHub Action | `/install-github-action` | PR 审查时 @.claude 自动更新 CLAUDE.md | 需要在 Claude Code 中运行安装命令 |
| Plan Mode | Shift+Tab 两次 | 先规划再执行，减少返工 | 出问题切回 Plan Mode 重新规划，不要硬推 |
| Slash Command | `.claude/commands/` 目录，提交 git | 消灭重复提示 | 用 `$(...)` 内联 bash 预计算上下文 |
| PostToolUse Hook | `.claude/hooks.json`，matcher: `Write\|Edit` | 自动格式化，避免 CI 格式错误 | 命令加 `\|\| true` 避免格式化失败阻断流程 |
| 权限白名单 | `.claude/settings.json`，`permissions.allow` 数组 | 精细化授权，避免频繁权限提示 | 严禁用 `--dangerously-skip-permissions`，沙箱除外 |
| Slack MCP | `.mcp.json`，url: `https://slack.mcp.anthropic.com/mcp` | Claude 直接操作 Slack | 提交到 `.mcp.json` 与团队共享 |
| Git Worktrees | `git worktree add ../project-x branch-x` | 并行会话不冲突 | 配合 shell 别名（za/zb/zc）使用 |
| Statusline | `/statusline` | 实时显示上下文窗口使用率和当前分支 | 多会话时必备，防止上下文溢出 |
| 学习模式 | `/config` → 输出风格: Explanatory 或 Learning | Claude 解释改动原因 | 适合学习陌生代码库 |

---

### 🛠️ 操作流程

**1. 准备阶段**

- 安装 Ghostty 或 iTerm2，配置系统通知（Claude 需要输入时提醒）
- 创建项目 `CLAUDE.md`，包含：项目命令（install/test/typecheck）、不可违反规则、常见错误积累
- 创建 `.claude/settings.json`，配置权限白名单（build/test/typecheck/format/git status/git diff）
- 运行 `/install-github-action` 安装 GitHub Action，支持 PR 中 @.claude

**2. 核心执行**

- 每个任务：Shift+Tab 两次进入 Plan Mode → 与 Claude 讨论计划 → 满意后切换自动接受模式执行
- 并行任务：创建 3-5 个 git worktrees，每个运行独立 Claude 会话，配置 za/zb/zc 别名
- 重复工作：写成 Slash Command 存入 `.claude/commands/`，用 `$(...)` 预计算上下文
- 重型任务：提示词末尾加 `"use subagents"` 保持主上下文干净
- 外部工具：配置 MCP（Slack/BigQuery/Sentry），让 Claude 直接操作

**3. 验证与优化**

- 为你的领域建立验证机制（Web 用 Chrome 扩展，后端用测试套件，CLI 用 bash 命令）
- 每次 Claude 犯错：说"更新你的 CLAUDE.md 这样你下次就不会犯同样的错误"
- 配置 PostToolUse Hook 自动格式化，消灭 CI 格式错误
- 定期清理 CLAUDE.md，删除不再相关规则，保持约 2500 tokens

---

### 💡 具体案例/数据

**Boris 的并行规模**：本地终端 5 个 + claude.ai/code 5-10 个 + 手机若干 = 总计 15-20 个并行会话

**模型选择数据对比**：

| 模型 | 单次耗时 | 迭代次数 | 总时间 |
|------|---------|---------|------|
| Sonnet（快） | 1 分钟 | 5 次 | 5 分钟 |
| Opus 4.5 with thinking（慢） | 2 分钟 | 1 次 | 2 分钟 |

**CLAUDE.md 最佳长度**：约 2500 tokens，Boris 团队每周贡献多次

**验证循环收益**：给 Claude 验证能力，最终结果质量提升 2-3 倍

**SQL 替代**：Boris 已 6 个月以上没写过一行 SQL，全靠 Claude 通过 bq CLI 完成

**语音输入效率**：说话速度是打字的 3 倍，macOS 按 fn 两次激活

**强力提示词案例**：
- 确保质量：`"审查这些改动，除非我通过你的测试否则不要创建 PR"`
- 要求重做：`"基于你现在知道的一切，推翻这个方案，实现优雅的解决方案"`
- 验证工作：`"证明给我看这能工作。比较 main 分支和这个分支的行为（测试/日志/输出差异）"`
- 修复 CI：`"去修复失败的 CI 测试。运行测试套件，找到根本原因，应用最小修复，保持测试通过。"`

---

### 📝 避坑指南

- ⚠️ 严禁在非沙箱环境使用 `--dangerously-skip-permissions`，只在隔离沙箱中使用 `--permission-mode=dontAsk`
- ⚠️ CLAUDE.md 不要无限堆砌，超过 2500 tokens 后效果递减，定期清理过时规则
- ⚠️ 不要微观管理 Claude 怎么修 bug，给原始信息（Slack 线程、CI 日志、docker logs）让它自己找方案
- ⚠️ PostToolUse Hook 的格式化命令必须加 `|| true`，否则格式化工具报错会阻断整个写文件流程
- ⚠️ 并行会话不要用同一个分支，必须配合 git worktrees，否则会话间文件冲突
- ⚠️ 跳过 Plan Mode 直接执行看似省时，出错后修复成本远高于规划成本，复杂任务必须先 Plan
- ⚠️ 不要过度指导 Claude（"看第 42 行，我觉得可能是…"），这会限制它找到更优解

---

### 🛠️ 快速入门检查清单（按顺序执行）

1. 学会 Plan Mode（Shift+Tab 两次）
2. 创建项目 `CLAUDE.md`
3. 设置一个常用 Slash Command（如 `/commit-push-pr`）
4. 配置 `/permissions` 白名单（`.claude/settings.json`）
5. 尝试并行运行 2 个 Claude 会话
6. 为你的领域建立验证机制
7. 探索 Git Worktrees 实现更多并行
8. 逐步添加 Skills 和 Subagents

---

### 🏷️ 行业标签

#ClaudeCode #AI编程 #开发者工作流 #并行化 #提示词工程 #MCP #GitWorktrees #生产力工具 #Anthropic

---

---
