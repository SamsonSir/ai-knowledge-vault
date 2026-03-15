# Agent与技能系统

## 25. [2026-01-24]

## 📗 文章 2


> 文档 ID: `KBRiwneXsiEUfWkaUxccgCZ7nxF`

**来源**: Claude Code 升级：Tasks 取代 Todos | **时间**: 2026-01-24 | **原文链接**: https://mp.weixin.qq.com/s/CVupGttF...

### 📋 核心分析
**战略价值**: Claude Code 用文件系统级的 Tasks 替换内存级的 TodoWrite Tool，使多 subagent、跨 session 的复杂项目协作成为可能。

**核心逻辑**:
- **TodoWrite Tool 被废弃**：Opus 4.5 模型能力增强后，对小任务已能自主记忆状态，TodoWrite 作为辅助记忆工具失去存在意义——模型变强，工具做减法。
- **"unhobble"（解绑）是官方用词**：意味着之前 Claude 的能力被工具设计本身限制了，现在主动移除这些限制。
- **Opus 4.5 可自主运行更长时间**：相比前代模型，能更好地追踪自身状态，不再依赖外部 Todo 列表维持上下文。
- **Tasks 存储路径固定为 `~/.claude/tasks`**：文件系统级存储，而非内存/session 内存储，这是跨 session 协作的物理基础。
- **多 Claude 实例可同时读写同一份 Task List**：多个 subagent 或 session 并发操作不冲突，解决了之前 Todos 只能单 session 使用的根本缺陷。
- **Tasks 支持依赖关系（dependencies）**：任务间的依赖存在 metadata 里，可以表达 blocker 关系，适配真实项目的复杂任务图。
- **实时广播机制**：一个 session 更新 Task 后，所有操作同一 Task List 的 session 立即收到更新，实现多智能体实时同步。
- **环境变量 `CLAUDE_CODE_TASK_LIST_ID` 控制协作范围**：指定同一个 ID，多个 session 即可共享同一 Task List，无需额外配置。
- **`claude -p` 和 AgentSDK 均已支持 Tasks**：不只是交互式 CLI，程序化调用场景同样可用。
- **Tasks 文件系统可扩展**：存在本地文件系统意味着开发者可以在上面构建自定义工具，Tasks 是一个开放的数据层。
- **设计灵感来自社区项目 Beads**：作者是 Steve Yegge，官方 @Thariq 明确致谢，说明 Anthropic 在主动吸收社区实践。

### 🎯 关键洞察

**为什么是现在升级**：Anthropic 内部自己在用 Claude Code 做跨多个 subagent、多个 context window、多个 session 的长项目，亲身踩到了 Todos 的天花板——这不是用户反馈驱动，是 dogfooding 驱动的架构升级，可信度更高。

**依赖关系是核心差异**：Todos 本质是一个平铺列表，Tasks 是一个有向图（DAG）。真实工程项目中任务之间存在 blocker，平铺列表无法表达"任务 B 必须等任务 A 完成"这种约束，Tasks 的 metadata 层解决了这个问题。

**文件系统存储 = 持久化 + 可观测性**：`~/.claude/tasks` 路径下的数据人类可读、可编辑、可版本控制，这让 Tasks 不只是 Claude 的内部状态，而是一个可以被外部工具集成的数据接口。

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| Tasks 存储路径 | `~/.claude/tasks` | 跨 session 持久化任务数据 | 多 agent 并发写入需注意文件锁 |
| 多 session 共享 Task List | `CLAUDE_CODE_TASK_LIST_ID=groceries claude` | 多个 Claude 实例操作同一任务列表 | ID 需手动保持一致，拼写错误会导致隔离 |
| 程序化调用 | `claude -p` 及 AgentSDK | 非交互式场景同样支持 Tasks | 需确认 SDK 版本已包含 Tasks 支持 |
| 任务依赖关系 | 存储在 Task metadata 中 | 表达任务间 blocker/依赖 | 依赖关系需在创建 Task 时显式声明 |
| 实时广播 | 自动触发，无需额外配置 | 同一 Task List 的所有 session 实时同步 | 网络/文件系统延迟可能影响同步时效 |

### 🛠️ 操作流程

1. **准备阶段**: 确认使用的是支持 Tasks 的 Claude Code 版本（Opus 4.5 及以上），旧版 TodoWrite Tool 已废弃，无需迁移，直接使用新接口。

2. **核心执行**:
   - 单 session 场景：直接用自然语言让 Claude 创建 tasks，无需特殊命令。
   - 多 session / 多 subagent 协作场景：启动时设置环境变量：
     ```bash
     CLAUDE_CODE_TASK_LIST_ID=your_project_id claude
     ```
   - 所有参与协作的 session 使用相同的 `CLAUDE_CODE_TASK_LIST_ID` 值。
   - 启动 subagent 时尤其推荐显式传入 Task List ID，确保子任务写回主任务列表。

3. **验证

---

---
