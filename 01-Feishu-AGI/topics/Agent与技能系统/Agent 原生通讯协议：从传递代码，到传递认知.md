# Agent与技能系统

## 55. [2026-02-11]

## 📔 文章 5


> 文档 ID: `Gx64w6q3nivmkak3LmocNF9Bnbc`

**来源**: Agent 原生通讯协议：从传递代码，到传递认知 | **时间**: 2026-02-11 | **原文链接**: `https://mp.weixin.qq.com/s/6ppTHXXd...`

---

### 📋 核心分析

**战略价值**: Git/GitHub 正在被 Agent 自发用作通讯协议，而 Entire（GitHub 前 CEO Thomas Dohmke 创立，6000 万美元种子轮）要在此基础上构建 Agent 原生的开发生命周期——核心产品 Checkpoint 把 Agent 的推理过程绑定到 commit，让"为什么这么改"第一次变得可追溯。

**核心逻辑**:

- **Agent 已在自发使用 GitHub 作为通讯协议**：Issue = 任务指令，PR = 执行结果，Comment = 方案讨论。这套流程没人设计，自然发生。GitHub 天然满足 Agent 通讯的四个条件：纯文本可审计、命令式结构、标签/状态机器可解析、版本控制不丢失。
- **Git 的致命缺失是 "Why"**：Git 忠实记录 What/Who/When/Where，但不记录推理链。Agent 生成 500 行代码后，你只看到 diff，不知道它权衡了什么、放弃了什么。关闭终端，prompt 和讨论过程全部消失。
- **Checkpoint 的实现机制**：不修改 Git，在 Git 之上增加语义元数据层。每次 Agent commit 时，自动捕获并绑定到 commit SHA：原始 prompt、推理链（考虑了什么/放弃了什么）、工具调用记录（读了哪些文件/调了哪些 API）、约束条件、token 消耗、完整对话 transcript。元数据存储在独立分支 `entire/checkpoints/v1`，append-only 追加，不影响现有 Git 工作流。
- **Checkpoint 改变代码审查范式**：过去打开 PR 逐行读 diff，现在先看 Checkpoint——Agent 接到的意图是什么、考虑了哪些方案、为什么选当前实现。审查对象从"代码对不对"变成"思维过程合不合理"。
- **Checkpoint 解决多 Agent 共享记忆问题**：Agent A 在一个 session 做了技术选型，session 结束上下文消失。Agent B 接手时读取 Agent A 的 Checkpoint，直接继承决策和约束，不需要从头推理。
- **Checkpoint 解决"人肉记录"痛点**：过去 Vibe Coding 开发者必须手动维护 CLAUDE.md、cursor rules 等规则文件来保存技术选型和架构约束，且依赖"有意识地去做"。Checkpoint 自动化这一过程，每次 commit 自动存档，无需人工干预。
- **多 Agent 并行场景的实际改善**：用 Git worktree 管理多分支、每个 worktree 启动 Agent Team 并行工作时，过去需要逐行对比几千行 diff。有了 Checkpoint，直接看各方案的推理摘要和决策依据，5 分钟完成判断。
- **Checkpoint 尚未解决的问题一——上下文爆炸**：三个月项目可能累积 10M tokens 的 Checkpoint 数据，而当前最好模型上下文窗口仅 200k。存下来了，但 Agent 一次看不完。更关键的是，Checkpoint 反而可能更快塞爆 Agent 上下文——如何从 500 个 Checkpoint 里精准找到当前任务需要的 3 个，是未解决的检索问题。
- **Checkpoint 尚未解决的问题二——实时协调缺失**：Checkpoint 是"事后记录"。多 Agent 并行时，Team 1 做到一半决定用 Drizzle ORM，这个决定需要实时同步给 Team 2 和 Team 3，而不是等 Team 1 commit 后 Team 2 才读到并发现不兼容。这进入了 Agent 间实时通讯协议的领域，超出 Checkpoint 范畴。
- **范式转变的本质**：人的角色从"写代码的工人"变成"审查 Agent 思维过程的监督者"——不需要理解每行代码怎么写，但需要判断 Agent 推理是否合理、决策是否正确、有没有遗漏关键约束。

---

### 🎯 关键洞察

**为什么 Entire 要开源并强调 "open, scalable, independent"**：Thomas Dohmke 的目标不只是做一个产品，而是推一个协议标准。类比 HTTP 之于互联网——HTTP 是人访问网站的协议，Entire 想成为 Agent 协作的协议。开源是让协议被广泛采纳的必要条件，封闭协议无法成为基础设施。

**"2A"逻辑链**：过去软件服务人类消费者（2C）或企业（2B）。如果 Agent 是软件的新用户（2A），那 Agent 之间如何高效协作就是最关键的基础设施问题。Checkpoint 本质上是给 Agent 读的结构化推理数据，不是给人看的漂亮界面——这是 2A 产品设计思路的具体体现。

**"韩信点兵"的指挥体系逻辑**：驱动 1 个 Agent 和驱动 100 个 Agent 的难度不是线性增长。没有协调体系，100 个 Agent 就是混乱——各自为战、重复推理、互相冲突。Entire 的三层架构对应的就是这个指挥体系：统一信息存储（Checkpoint）+ 共享态势感知（Context Graph）+ 清晰协作流程（AI 原生开发生命周期）。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|----------|-------------|---------|-----------|
| Checkpoint 存储分支 | `entire/checkpoints/v1`，append-only | 不影响现有 Git 工作流，完全兼容 | 长期项目可能累积 10M+ tokens 数据 |
| Checkpoint 绑定方式 | 绑定到 commit SHA | 每个 commit 对应完整推理记录 | 必须通过 Entire 工具链触发，普通 git commit 不会自动捕获 |
| Checkpoint 捕获内容 | 原始 prompt + 推理链 + 工具调用 + 约束条件 + token 消耗 + 完整 transcript | Agent 思维过程从黑箱变白箱 | 当前只解决存储，检索问题待 Context Graph 解决 |
| Context Graph（语义推理层） | 根据当前任务语义检索相关历史上下文，分层压缩（完整记录/决策摘要/关键约束） | 解决上下文爆炸，精准检索 | 尚未发布 |
| AI 原生开发生命周期 | Agent 间实时协调与工作流 | 解决并行 Agent 实时同步问题 | 尚未发布 |

---

### 🛠️ 操作流程

1. **当前可用（Checkpoint 层）**
   - 接入 Entire 工具链，替代或包装现有 git commit 操作
   - Agent 每次生成代码并 commit 时，Checkpoint 自动捕获推理元数据，写入 `entire/checkpoints/v1` 分支
   - Review PR 时，先查对应 commit 的 Checkpoint，看意图→决策→约束，再看 diff

2. **多 Agent 并行场景**
   - 用 Git worktree 管理多分支，每个 worktree 启动独立 Agent Team
   - 各 Team commit 后，通过 Checkpoint 查看各方案推理摘要
   - 对比决策依据而非逐行 diff，快速做出方案选择

3. **历史决策追溯**
   - 有人问"为什么选 SQLite 而不是 PostgreSQL"时，查询对应时间段的 Checkpoint 历史
   - 找到讨论该技术选型的 session，直接引用当时推理回复——有理有据，不靠记忆

4. **待发布功能（Context Graph 层）**
   - 根据当前任务语义，从海量 Checkpoint 中精准检索相关历史上下文
   - 分层压缩：完整记录 / 决策摘要 / 关键约束，不同场景用不同粒度
   - 类比人类记忆的遗忘曲线和按需回忆机制

---

### 📦 Entire 三层架构路线图

| 层次 | 解决什么 | 状态 |
|------|---------|------|
| Checkpoint（存储层） | 信息不再丢失，推理过程可追溯 | ✅ 已发布 |
| Context Graph（语义推理层） | 从海量 Checkpoint 中精准检索，解决上下文爆炸 | 🔜 待发布 |
| AI 原生开发生命周期 | Agent 间实时协调与工作流，解决并行冲突 | 🔜 待发布 |

---

### 💡 具体案例/数据

- **融资规模**：GitHub 前 CEO Thomas Dohmke 创立 Entire，种子轮 6000 万美元
- **上下文窗口瓶颈**：三个月项目累积约 10M tokens Checkpoint 数据，当前最好模型上下文窗口 200k，存储与检索之间存在 50 倍差距
- **多 Agent 审查效率**：6 个 Agent Team 并行产出几千行代码，有 Checkpoint 后可在 5 分钟内通过推理摘要完成方案比较，无需逐行对比 diff
- **Thomas Dohmke 原话**："我们仍然依赖一个在云时代之前构建的软件开发生命周期，它天生是为人与人协作设计的。"

---

### 📝 避坑指南

- ⚠️ **Checkpoint 不是万能的**：它解决存储问题，但引入检索问题。不要期望把所有 Checkpoint 塞给 Agent——200k 上下文窗口装不下 10M tokens 的历史数据，需要等 Context Graph 层解决精准检索。
- ⚠️ **实时协调仍是空白**：Checkpoint 是事后记录，无法解决并行 Agent 的实时同步。Team 1 做到一半的决策无法实时通知 Team 2，仍需人工协调或等待 AI 原生开发生命周期层发布。
- ⚠️ **现有 CLAUDE.md / cursor rules 不能立即废弃**：Checkpoint 目前只捕获通过 Entire 工具链触发的 commit，存量项目和非 Entire 工作流的历史决策仍需手动维护规则文件过渡。
- ⚠️ **协议标准之争尚未结束**：Entire 开源并强调独立性，但 Agent 通讯协议领域竞争者众多，押注单一工具链有锁定风险，关注其开放标准的实际落地情况。

---

### 🏷️ 行业标签

#Agent协作 #GitWorkflow #开发者工具 #Entire #Checkpoint #多Agent #AI原生基础设施 #VibeCoding #上下文管理 #2A

---

**引用**:
- 互联网已死，Agent 永生（原文引用）
- Entire 官方介绍：`https://entire.io/blog/hello-entire-world`

---

---
