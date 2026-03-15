# AI编程与开发工具

## 1. [2026-01-05]

## 📘 文章 3


> 文档 ID: `S0pKwili5ijvunkr6Nqc3N7hnlb`

**来源**: Gemini API 负责人破防：团队干了一年，被 Claude Code 1 小时复现？Claude 亲授的 13 个技巧 | **时间**: 2026-01-05 | **原文链接**: `https://mp.weixin.qq.com/s/JXX6SoAU...`

---

### 📋 核心分析

**战略价值**: Claude Code 创始人 Boris Cherny 亲授 13 个实战技巧，配合 Gemini API 主管 Jaana Dogan 的真实案例，揭示 AI 编程的正确打开方式——不是替代人类探索，而是极速复现已验证的方案。

**核心逻辑**:

- **"一年 vs 一小时"的本质**：Jaana 团队花一年踩坑、验证最佳方案；把结论写进 Prompt 后，Claude Code 1 小时复现玩具原型。AI 压缩的是"执行时间"，不是"探索时间"——创新和试错仍是人的核心价值。
- **并行 5 个本地进程**：Boris 在终端同时跑 5 个 Claude 进程，标签页编号 1-5，用系统通知（iTerm2）监控进度，彻底告别串行等待。
- **本地 + Web 端无缝切换**：本地跑 5 个实例的同时，claude.ai/code 再开 5-10 个；用 `&` 符号或 `--teleport` 命令在终端和 Web 端之间切换；早晨和白天从 Claude iOS App 启动会话，晚些再回来查看结果。
- **坚持用 Opus 4.5 + Thinking 模式**：Sonnet 更快，但 Boris 选 Opus 4.5——原因是工具调用能力更强、干预更少，不需要反复调教，综合效率反而更高。
- **全队共建 CLAUDE.md**：整个团队共用一个 CLAUDE.md 文件，Claude 每次执行前都会读取；谁发现 Claude 犯错就往里记一笔，积累团队代码风格和避坑指南；Code Review 时直接 `@.claude`，让它把修改规则同步进 CLAUDE.md，通过 `/install-github-action` 安装 Claude Code GitHub Action 实现自动化。
- **Plan Mode 是灵魂**：大部分会话从 Plan 模式启动（`Shift+Tab` 按两次），先让 Claude 列出执行计划，对齐后再切自动模式——计划对了基本 One-shot 搞定。
- **斜杠命令消灭重复动作**：把高频操作编成 `/` 命令，存放在 `.claude/commands/` 目录；例如每天使用数十次的 `/commit-push-pr`，命令内嵌脚本让 Claude 自动查 git 状态，避免来回交互。
- **子代理按职能分工**：不让一个 AI 包揽所有任务；`code-simplifier` 专门简化代码，`verify-app` 专门负责测试——按流程职能分工，不是按领域专家分工。
- **PostToolUse 钩子自动格式化**：每次 Claude 写完代码，钩子自动触发格式化，保证代码进测试环境前的最后 10% 质量。
- **权限预设用 `/permissions`**：不用 `--dangerously-skip-permissions` 暴力跳过；而是用 `/permissions` 提前给常用安全的 bash 命令授权，配置提交到 `.claude/settings.json` 全队共享，不再手动点确认。
- **MCP 协议跨平台打工**：通过 MCP 协议让 Claude Code 发 Slack 消息、用 `bq` CLI 跑 BigQuery 查询、从 Sentry 拉错误日志；配置提交到 `.mcp.json` 全队共享。
- **长任务挂机三件套**：(a) 任务完成后让 Claude 通过后台代理自验结果；(b) 用 `agent Stop` 钩子做确定性验证；(c) 用 `ralph-wiggum` 插件自动循环直到完成。沙盒中配合 `--permission-mode=dontAsk` 或 `--dangerously-skip-permissions` 让 Claude 无干扰运行。插件地址：`https://github.com/anthropics/claude-plugins-official/tree/main/plugins/ralph-wiggum`
- **验证闭环是最终杀招**：给 Claude 一个稳定的反馈回路（跑测试、开浏览器测 UI），产出质量可提升 2-3 倍。Boris 的做法是用 Chrome 扩展测试每次改动，Claude 自动打开浏览器、测试界面、持续迭代直到功能正常且 UX 良好。

---

### 🎯 关键洞察

**"一年 vs 一小时"的正确解读**：

Jaana 后来澄清，这不是 AI 有多牛，而是：
1. 人类花了一年把"最佳方案"探索出来
2. 把结论写进 Prompt，AI 自然能快速复现一个质量不错的原型
3. Claude Code 给的是"玩具版"，不是生产级代码

核心结论：**AI 压缩的是"已知解的执行成本"，人类的核心价值在于"未知解的探索能力"**。

Jaana 的建议：如果你对 Code Agent 持怀疑态度，去你最熟悉的领域，从头构建一个足够复杂的东西，由你自己判断产出是否靠谱。

**Boris 的数据背书**：过去一个月为 Claude Code 贡献 497 次提交、新增约 4 万行代码，全程没打开过一次 IDE，全靠 Claude Code + Opus 4.5 完成。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| 并行本地进程 | 终端开 5 个标签页，编号 1-5，iTerm2 系统通知 | 并行执行多任务，不等待 | 参考：`https://code.claude.com/docs/en/terminal-config` |
| Web 端并行 | `claude.ai/code` 开 5-10 个实例，`--teleport` 切换 | 本地+云端同时跑 | 用 `&` 符号或手动在 Chrome 启动 |
| 模型选择 | Opus 4.5 + Thinking 模式 | 工具调用强、干预少 | Sonnet 快但需要更多调教 |
| CLAUDE.md | 全队共用，记录错误和代码风格 | AI 每次执行前自动读取 | Code Review 时 `@.claude` 同步规则 |
| GitHub Action | `/install-github-action` | PR 中自动触发 Claude | 需先安装 Claude Code GitHub Action |
| Plan Mode | `Shift+Tab` 按两次 | 先规划再执行，One-shot 成功率高 | 计划对齐后再切自动模式 |
| 斜杠命令 | `.claude/commands/` 目录下定义 | 消灭重复操作 | 命令内可嵌脚本，如自动查 git 状态 |
| 子代理 | `code-simplifier`、`verify-app` 等 | 专职分工，效率更高 | 按流程职能分，不是按领域专家分 |
| PostToolUse 钩子 | 写完代码自动触发格式化 | 保证代码质量最后 10% | 需在钩子配置中设定 |
| 权限预设 | `/permissions` + `.claude/settings.json` | 全队共享，不再手动点确认 | 避免用 `--dangerously-skip-permissions` |
| MCP 协议 | `.mcp.json` 提交到仓库 | Slack/BigQuery/Sentry 跨平台操作 | 配置全队共享 |
| 长任务挂机 | `ralph-wiggum` 插件 + `--permission-mode=dontAsk` | 自动循环直到完成 | 插件地址见上方链接 |
| 验证闭环 | Chrome 扩展 + 测试套件 + 浏览器/模拟器 | 产出质量提升 2-3 倍 | 验证方式因领域而异，需提前投入建设 |

---

### 🛠️ 操作流程

1. **准备阶段**:
   - 建立 `CLAUDE.md`，写入团队代码风格和已知坑点
   - 在 `.claude/commands/` 下定义高频斜杠命令（如 `/commit-push-pr`）
   - 用 `/permissions` 预授权常用 bash 命令，提交 `.claude/settings.json`
   - 配置 `.mcp.json`，接入 Slack/BigQuery/Sentry 等工具

2. **核心执行**:
   - 本地开 5 个终端标签（编号 1-5），配置 iTerm2 系统通知
   - 同时在 `claude.ai/code` 开 5-10 个 Web 实例并行运行
   - 每个会话从 Plan Mode 启动（`Shift+Tab` 两次），对齐计划后切自动模式
   - 长任务启用 `ralph-wiggum` 插件 + `--permission-mode=dontAsk`，挂机等结果
   - 复杂任务拆分子代理：`code-simplifier` 简化代码，`verify-app` 负责测试

3. **验证与优化**:
   - 配置 PostToolUse 钩子，写完代码自动格式化
   - 用 Chrome 扩展或测试套件建立验证闭环，让 Claude 自动迭代直到通过
   - Code Review 时 `@.claude`，把新发现的坑同步进 `CLAUDE.md`
   - 用 `agent Stop` 钩子做确定性的任务完成验证

---

### 💡 具体案例/数据

- Jaana Dogan（谷歌 Gemini API 主管）：用三句话描述分布式 Agent 编排器，Claude Code 花 1 小时复现玩具版原型；原版是团队踩坑数月的成果
- Boris Cherny（Claude Code 创始人）：过去一个月贡献 497 次提交、新增约 4 万行代码，全程零 IDE，全靠 Claude Code + Opus 4.5
- 验证闭环效果：建立稳定反馈回路后，产出质量提升 2-3 倍（Boris 实测数据）

---

### 📝 避坑指南

- ⚠️ 不要用 `--dangerously-skip-permissions` 作为日常权限方案，应用 `/permissions` 精细预授权，配置提交到 `.claude/settings.json`
- ⚠️ 不要让一个 AI 实例包揽所有任务，按流程职能拆分子代理（简化、测试、验证分开）
- ⚠️ 不要跳过 Plan Mode 直接执行，计划不对齐会导致多轮返工，One-shot 成功率大幅下降
- ⚠️ CLAUDE.md 不是一次性文档，需要全队持续维护，发现 Claude 犯错就立即记录
- ⚠️ Claude Code 产出的是"原型/玩具版"，不是生产级代码，上线前必须人工审查
- ⚠️ 验证闭环需要提前投入建设（Chrome 扩展、测试套件等），不能临时凑合

---

### 🏷️ 行业标签

#ClaudeCode #AI编程 #AgentWorkflow #提示工程 #开发效率 #MCP协议 #Boris Cherny #Jaana Dogan

---

---
