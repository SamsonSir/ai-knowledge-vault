# AI编程与开发工具

## 38. [2026-02-25]

## 📔 文章 5


> 文档 ID: `N8eTwc19Mi7VqZkNPIDc64S0nbL`

**来源**: OpenClaw + Codex/ClaudeCode智能体集群：一人开发团队 | **时间**: 2026-03-13 | **原文链接**: `https://x.com/elvissun/status/2025920521871716562?s=46`

---

### 📋 核心分析

**战略价值**: 用 OpenClaw 作编排层，让一个人通过管理 AI Agent 集群实现"虚拟开发团队"效果——每天自动提交 50+ 次代码，无需打开编辑器。

**核心逻辑**:

- **上下文窗口是零和博弈**：单个 AI 无法同时装载完整代码库 + 完整业务背景。解法是分层：编排层（Zoe/OpenClaw）持有业务上下文，编码 Agent（Codex/Claude Code）只持有代码上下文，各司其职。
- **编排器 Zoe 的四项核心权限**：管理 API 访问权限（可直接充值解封客户）、只读生产 DB 访问权限（编码 Agent 永远没有此权限）、生成 Agent 并写提示、Telegram 通知推送。
- **每个 Agent 独立隔离运行**：每个任务对应一个独立 git worktree + 独立 tmux 会话，避免并行任务互相污染。
- **定时任务每 10 分钟轮询一次**，但不直接轮询 Agent（成本太高），而是读取 JSON 注册表 + 跑确定性脚本，token 消耗极低。
- **"完成"定义极其严格**：PR 创建 + 无合并冲突 + CI 全过（lint/type/unit/E2E/Playwright) + 三个 AI 审查员全过 + UI 变更必须附截图，缺一不可才触发 Telegram 通知。
- **三审查员分工明确**：Codex 审查员负责边缘情况和逻辑错误（误报率最低，最全面）；Gemini Code Assist 负责安全和可扩展性（免费）；Claude Code 审查员过于保守，大量"考虑添加…"建议，除非标记 critical 否则忽略。
- **Zoe 主动找工作，不等分配**：早上扫 Sentry 错误 → 自动生成修复 Agent；会议结束后扫会议记录 → 自动生成功能 Agent；晚上扫 git log → 自动更新 changelog 和文档。
- **失败重试时 Zoe 重写提示而非原样重跑**：结合业务背景分析失败原因，针对性修正（上下文超限 → 缩小文件范围；方向跑偏 → 注入客户原话；需要补充说明 → 附上客户邮件和公司背景）。
- **奖励信号驱动自我改进**：CI 通过 + 三审通过 + 人工合并 = 正向信号，失败触发循环，成功的提示模式被记录（如"Codex 需要提前提供类型定义"、"始终包含测试文件路径"）。
- **Agent 选型策略**：Codex 处理 90% 任务（后端/复杂 bug/多文件重构）；Claude Code 处理前端和 git 操作（权限问题少）；Gemini 先出 HTML/CSS 设计稿，再交 Claude Code 在组件系统中实现。

---

### 🎯 关键洞察

**为什么两层架构比单 AI 更有效**：

原因 → 上下文窗口有限，业务背景（客户数据、会议记录、历史决策）和代码库无法同时塞入同一个 AI。

动作 → 编排层（Zoe）持有 Obsidian 笔记库中的全部业务上下文，将其转化为针对每个编码 Agent 的精准提示；编码 Agent 只看代码。

结果 → Agent 专注执行，编排器负责战略，互不干扰，且编排器可以在失败时用业务背景重写提示，而不是盲目重试。

**Stripe 的 "Minions" 系统**（集中式编排层 + 并行编码 Agent）与此架构本质相同，作者是在 Mac Mini 上独立复现了企业级方案。

**RAM 是真实瓶颈**：5 个 Agent 并行 = 5 个 TypeScript 编译器 + 5 个测试运行器 + 5 套 node_modules，16GB Mac Mini 在 4-5 个 Agent 后开始内存交换。作者为此购入 128GB RAM 的 Mac Studio M4 Max，3 月底到货后会分享结果。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| Codex Agent 启动 | `codex --model gpt-5.3-codex -c "model_reasoning_effort=high" --dangerously-bypass-approvals-and-sandbox "Your prompt here"` | 高推理强度执行任务 | 需要 bypass 沙箱才能操作文件系统 |
| Claude Code 启动 | `claude --model claude-opus-4.5 --dangerously-skip-permissions -p "Your prompt here"` | 前端/git 操作 | 权限问题比 Codex 少 |
| 创建 worktree + tmux | `git worktree add ../feat-custom-templates -b feat/custom-templates origin/main` → `cd ../feat-custom-templates && pnpm install` → `tmux new-session -d -s "codex-templates" -c "/path/to/worktree" "$HOME/.codex-agent/run-agent.sh templates gpt-5.3-codex high"` | 每个 Agent 完全隔离 | 每个 worktree 需要独立 node_modules，RAM 消耗大 |
| 向运行中 Agent 注入指令 | `tmux send-keys -t codex-templates "Stop. Focus on the API layer first, not the UI." Enter` | 纠偏而不杀掉 Agent | 不要用 kill，用 send-keys 重定向 |
| 任务注册表（运行中） | `.clawdbot/active-tasks.json`，字段：`id/tmuxSession/agent/description/repo/worktree/branch/startedAt/status/notifyOnComplete` | 统一追踪所有 Agent 状态 | 见下方 JSON 示例 |
| 任务注册表（完成后） | 追加字段：`status:"done"/pr/completedAt/checks{prCreated/ciPassed/claudeReviewPassed/geminiReviewPassed}/note` | 完整审计链 | 见下方 JSON 示例 |
| 定时轮询脚本 | `.clawdbot/check-agents.sh`，每 10 分钟运行 | 监控所有 Agent，失败自动重启（最多 3 次） | 不直接轮询 Agent，读 JSON 注册表 + gh CLI 检查 CI |
| PR 创建 | `gh pr create --fill` | Agent 自动提交推送开 PR | 仅创建 PR 不触发通知，需全部 checks 通过 |
| UI 变更强制截图 | CI 规则：PR 描述中无截图则 CI 失败 | 审查时无需点预览链接 | 上周新增规则，大幅缩短审查时间 |
| Gemini Code Assist | 直接安装到 GitHub PR 审查流程 | 免费捕捉安全/可扩展性问题 | 安装成本极低 |

---

### 🛠️ 操作流程

**完整八步工作流（以"客户请求自定义模板功能"为真实案例）**

1. **客户通话 → 与 Zoe 范围界定**
   - 通话结束后直接和 Zoe 讨论需求，会议记录已自动同步到 Obsidian 笔记库，无需手动解释背景
   - Zoe 与你共同确定功能范围（本例：模板系统，支持保存和编辑现有配置）
   - Zoe 立即执行三个动作：充值信用额度解封客户（用 API 管理权限）、从生产 DB 提取客户现有配置（只读权限）、生成带完整上下文的 Codex Agent 提示

2. **生成 Agent（隔离 worktree + tmux）**
   ```bash
   # 创建隔离 worktree
   git worktree add ../feat-custom-templates -b feat/custom-templates origin/main
   cd ../feat-custom-templates && pnpm install
   
   # 在 tmux 中启动 Agent
   tmux new-session -d -s "codex-templates" \
     -c "/Users/elvis/Documents/GitHub/medialyst-worktrees/feat-custom-templates" \
     "$HOME/.codex-agent/run-agent.sh templates gpt-5.3-codex high"
   ```
   写入 `.clawdbot/active-tasks.json`：
   ```json
   {
     "id": "feat-custom-templates",
     "tmuxSession": "codex-templates",
     "agent": "codex",
     "description": "Custom email templates for agency customer",
     "repo": "medialyst",
     "worktree": "feat-custom-templates",
     "branch": "feat/custom-templates",
     "startedAt": 1740268800000,
     "status": "running",
     "notifyOnComplete": true
   }
   ```

3. **循环监测（每 10 分钟）**
   - 运行 `.clawdbot/check-agents.sh`
   - 检查 tmux 会话是否活跃
   - 检查追踪分支上的开放 PR
   - 用 `gh` CLI 检查 CI 状态
   - CI 失败或收到 critical 审查 → 自动重启 Agent（最多 3 次）
   - 需要人工介入才发警报

4. **Agent 创建 PR**
   - Agent 执行 `gh pr create --fill` 自动提交、推送、开 PR
   - 此时不触发 Telegram 通知，仅创建 PR 不算完成

5. **自动代码审查（三个 AI 审查员）**
   - Codex 审查员：边缘情况、逻辑错误、遗漏错误处理、竞态条件，误报率最低
   - Gemini Code Assist：安全问题、可扩展性问题，免费，直接评论 PR
   - Claude Code 审查员：过于保守，大量"考虑添加…"，除非标记 critical 否则忽略
   - 注册表更新为：
   ```json
   {
     "status": "done",
     "pr": 341,
     "completedAt": 1740275400000,
     "checks": {
       "prCreated": true,
       "ciPassed": true,
       "claudeReviewPassed": true,
       "geminiReviewPassed": true
     },
     "note": "All checks passed. Ready to merge."
   }
   ```

6. **自动化测试（CI 全套）**
   - Lint + TypeScript 检查
   - 单元测试
   - E2E 测试
   - 针对预览环境的 Playwright 测试（与生产环境相同）
   - UI 变更必须在 PR 描述中附截图，否则 CI 失败

7. **人工审核（5-10 分钟）**
   - 收到 Telegram："PR #341 已准备好进行审核"
   - 此时 CI 已过、三个 AI 审查员已批准、截图已展示 UI 变化、所有边缘情况已记录在审查意见中
   - 很多 PR 不看代码直接合并，截图提供足够信息

8. **合并 + 清理**
   - PR 合并
   - 每日定时任务清理孤立 worktree 和任务注册表 JSON

---

### 💡 具体案例/数据

| 指标 | 数据 |
|------|------|
| 单日最高提交次数 | 94 次（当天打了 3 个客户电话，一次没打开编辑器） |
| 日均提交次数 | ~50 次 |
| 30 分钟内完成 PR 数 | 7 个 |
| Codex 任务占比 | 90% |
| Agent 一次性完成率 | 几乎所有中小任务无需干预 |
| 硬件瓶颈触发点 | 16GB Mac Mini 在 4-5 个 Agent 并行后开始内存交换 |
| 升级硬件 | Mac Studio M4 Max 128GB RAM，3 月底到货 |
| 系统上线时间节点 | 2025 年 1 月后切换为 OpenClaw 编排，git 历史可见明显分界线 |

**Zoe 主动工作的一个真实下午**：
- 作者打完客户电话出去散步
- 回来看 Telegram："7 个 PR 已准备好进行审查。3 个功能，4 个漏洞修复。"

---

### 📝 避坑指南

- ⚠️ **不要用 kill 杀掉跑偏的 Agent**，用 `tmux send-keys` 注入新指令重定向，保留已完成的工作
- ⚠️ **编码 Agent 永远不给生产 DB 写权限**，只读权限由编排层（Zoe）持有，编码 Agent 通过提示中的数据快照获取上下文
- ⚠️ **"PR 创建"≠"任务完成"**，必须 CI + 三审 + 截图全过才算完成，否则 Telegram 不通知，避免人工审查不完整的代码
- ⚠️ **Claude Code 审查员的建议大多可忽略**，它过于保守，只关注它标记为 critical 的问题，其余"考虑添加…"类建议跳过
- ⚠️ **RAM 是真实瓶颈而非 API 费用**：5 个并行 Agent = 5 套完整 TypeScript 工具链同时运行，16GB 不够用
- ⚠️ **定时任务轮询不要直接调用 AI**，用确定性脚本读 JSON 注册表 + gh CLI，token 消耗接近零
- ⚠️ **快速上手方式**：将整篇文章复制进 OpenClaw，告诉它"为我的代码库实现这个 Agent 群设置"，它会自动读取架构、创建脚本、设置目录结构、配置定时任务，约 10 分钟完成

---

### 🏷️ 行业标签

#AI智能体编排 #OpenClaw #Codex #ClaudeCode #一人开发团队 #自动化CI #gitworktree #tmux #B2BSaaS #递归自我改进

---

---
