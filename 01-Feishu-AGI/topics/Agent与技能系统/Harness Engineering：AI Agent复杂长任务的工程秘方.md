# Agent与技能系统

## 90. [2026-02-27]

## 📒 文章 7


> 文档 ID: `QCf5wxyDpiBpFSkruvTc4JBQnEg`

**来源**: Harness Engineering：AI Agent复杂长任务的工程秘方 | **时间**: 2026-02-21 | **原文链接**: https://mp.weixin.qq.com/s/yluRK-qE...

---

### 📋 核心分析

**战略价值**: Harness Engineering 是让 AI Agent 在生产环境中可靠完成长时程复杂任务的系统工程方法论——模型能力到达瓶颈后，系统设计才是决定 Agent 成败的核心变量。

**核心逻辑**:

- **Harness 的本质定义**：处理输入、编排工具调用、返回结果的系统层，让 LLM 能作为 Agent 工作。三个核心维度：Context Engineering（结构化上下文）、Tool Engineering（受控工具）、Workflow Engineering（验证循环）。
- **LLM 无状态 vs 任务有状态的根本矛盾**：LLM 的本质是 `f(context) → output`，每次推理独立。但复杂任务需要"记住我做了什么、为什么、下一步是什么"。Harness 是在无状态 LLM 和有状态任务之间搭桥，类比操作系统让无状态 CPU 运行有状态程序。
- **Durability（持久可靠性）独立于 Capability（单步能力）**：模型在 MMLU 得 90 分，不代表它能在第 50 步后不跑偏。"排行榜 1% 的差异无法检测模型在第 50 步之后是否偏离轨道"（Philipp Schmid）。两个典型失败模式：① All-or-nothing（一次性写完导致 context 耗尽）；② 过早胜利（看到进展就宣布完成）。
- **Context 是动态构建的，不可预测**：Agent 执行第 14 步时，context 是前 13 步任意组合的产物。第 1 步工具 A 返回 100 行数据，第 7 步只保留摘要，第 14 步可能只剩"工具 A 返回了客户列表"这一描述。"Everything's context engineering"（Harrison Chase, LangChain）。
- **"Lost in the middle"是 Transformer 的数学特性**：百万级 context window 没有解决根本问题。把 100 页文档全塞进 context，效果不如给 Agent 一个 100 行"地图"按需检索——因为每次检索的内容都在 attention 有效区域（前 20% 和后 20%），而非被埋在中间 60% 的 attention sink 里。
- **Harness 比换更大模型更有效**：LangChain 用同一模型 GPT-5.2-Codex，只改 harness，Terminal Bench 2.0 从 52.8% → 66.5%（26% 相对提升）。而模型从 GPT-5.2-Codex 升级到 GPT-5.3-Codex，SWE-Bench Pro 只提升 0.7%（56.4% → 56.8%）。
- **可验证性是 Harness 的核心价值**："改善系统的能力与验证其输出的难易程度成正比"（Jason Wei）。Anthropic 用 200+ 个 pass/fail 标准 + git commits；LangChain 用 middleware 强制验证；OpenAI 用 custom linters + structural tests。把"模糊的多步骤工作流"变成"可记录、可评分的结构化数据"。
- **训练数据偏差导致 Agent 不会自我验证**：LLM 训练数据主要是 GitHub commits（写代码），而非"写代码-测试-修复"完整循环。模型学会了"生成看起来正确的代码"，但没学会"验证代码是否真的正确"。这不是模型不够聪明，是系统设计问题。
- **Harness 是持久竞争护城河**：Harness 积累的是领域知识、工作流程模式、安全策略，不会因新模型发布而过时。即使模型完美，如何与人类工作流程、合规要求、安全边界集成，依然是独立的系统工程问题。
- **OpenAI 5 个月 100 万行代码的核心发现**：3 个工程师平均每天合并 3.5 个 PR，没有一行代码是工程师手写的。最大挑战不是"让 AI 写代码"，而是"让 AI 写的代码可维护"——"我们现在面临的最大挑战集中在设计环境、反馈循环和控制系统上"（OpenAI Codex Team）。

---

### 🎯 关键洞察

**为什么 Context Engineering 的核心是架构而非压缩？**

原因：Transformer 的 attention 机制对中间 tokens 存在数学级别的衰减。把 100 页文档塞进 context，模型对后 50 页的 attention 显著降低。

动作：给 Agent 一个 100 行的"地图"（如 AGENTS.md）+ 按需检索工具，而非把所有信息压缩后一次性注入。

结果：每次检索的内容都落在 attention 高效区域（首尾 20%），信息利用率远高于"百科全书式"注入。

**为什么"软约束"（prompt）不如"硬约束"（middleware）？**

原因：Agent 可能忽略 prompt 中的"记得测试"指令，因为训练数据偏差导致它倾向于"生成看起来正确的代码"就停止。

动作：用 PreCompletionChecklistMiddleware 在 Agent 退出前拦截，用代码逻辑强制检查测试是否运行、是否通过。

结果：LangChain 同模型下 Terminal Bench 2.0 提升 13.7 个百分点（52.8% → 66.5%）。

**为什么"分层抽象"比"线性压缩"更优？**

原因：压缩是有损的，细节丢失后结论不可靠。1000 个客户查询 × 500 tokens = 50 万 tokens，远超 context window，强行压缩会丢失关键细节。

动作：主 Agent 生成 1000 个并行子 Agent，每个处理一个客户生成摘要（50 tokens），主 Agent 只看 1000 个摘要（共 5 万 tokens）。

结果：系统总"工作记忆"可远超单个 context window，细节在子层无损保留，主层只处理摘要。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| OpenAI AGENTS.md | 100 行入口文件，指向编目的设计文档和架构地图 | Agent 按需检索，每次检索内容在高 attention 区域 | 必须保持 100 行以内，超长则失去"地图"效果，退化为百科全书 |
| OpenAI 自动偏差修复 | 后台任务定期扫描偏差，自动打开重构 PR | 人类品味被捕获一次，持续执行 | 约束条件（边界解析数据）而非具体实现，防止架构漂移 |
| Anthropic Initializer Agent | `init.sh` + 功能需求文件（200+ 个功能全标记"失败"）+ `claude-progress.txt` + 初始 git 提交 | 构建"记忆基础设施"，每个会话启动时可读取完整状态 | 功能需求文件必须是 pass/fail 二元标准，模糊标准无法验证 |
| Anthropic Coding Agent 会话流程 | 读取状态 → 做一件事（一次只处理一个功能）→ 端到端测试 → git commit + 更新 progress notes | 有状态任务分解为无状态操作，每个会话是纯函数 | 写错代码用 git 回滚，不允许跨功能操作 |
| LangChain PreCompletionChecklistMiddleware | Agent 准备退出时拦截，检查：① 是否运行测试 ② 测试是否通过，用代码逻辑强制执行 | Agent 无法跳过测试宣布完成 | 不能用 prompt 替代，prompt 可被 Agent 忽略 |
| LangChain LocalContextMiddleware | 启动时自动映射工作目录、查找可用工具、注入环境信息 | Agent 不需要主动"探索环境"，Harness 负责准备和交付 context | Agent 不会主动探索环境，必须由系统注入 |
| LangChain LoopDetectionMiddleware | 跟踪每个文件编辑次数，编辑 N 次后注入："你已经编辑这个文件 5 次了，考虑重新考虑方法" | 防止 Agent 陷入无效循环 | N 值需根据任务复杂度调整 |
| Hightouch make_plan / execute_step_in_plan / update_plan | 特殊工具调用，Agent 管理自己的思维过程，计划可根据新信息动态更新 | 规划与执行分离，支持动态调整 | 计划必须可更新，静态计划在复杂任务中会失效 |
| Hightouch 文件缓冲 | 工具返回大量数据时，Agent 调用 `write_file` 缓冲到磁盘，context 中只保留指针（文件名 + 描述） | context 只存"地图"，详细数据在磁盘 | 类似学生草稿纸，指针描述必须足够清晰让 Agent 知道何时检索 |
| Hightouch 扇出模式 | 对非结构化数据（如 1000 个客户评论），主 Agent 生成数百个并行调用到小模型（Haiku），每个处理一个评论，主 Agent 汇总 | 比 RAG 更便宜、更可靠 | 适用于非结构化数据批处理，结构化数据用动态子 Agent |

---

### 🛠️ 操作流程

**先诊断瓶颈，再选择方案：**

1. **准备阶段：诊断你的核心瓶颈**
   - 信息量超出 context window？→ 选渐进式披露（OpenAI 方案）
   - 任务跨多个会话、Agent 会"失忆"？→ 选外部化状态管理（Anthropic 方案）
   - Agent 写完代码不跑测试就宣布完成？→ 选强制验证循环（LangChain 方案）
   - 单个 Agent context 装不下复杂任务的中间步骤？→ 选动态子 Agent（Hightouch 方案）
   - 实际项目瓶颈通常是多个，需要组合多种方案

2. **核心执行：四种方案的最小实现**

   **方案 A（渐进式披露）**：
   - 创建 `AGENTS.md`（严格控制在 100 行以内），作为稳定入口点
   - 所有关键信息必须在代码库内可检索（偏好"无聊"的技术，更容易建模）
   - 约束条件而非具体实现（如"在边界解析数据"，不规定如何实现）
   - 配置后台任务定期扫描架构偏差，自动打开重构 PR

   **方案 B（外部化状态管理）**：
   - Initializer Agent 生成：`init.sh` + 功能需求文件（200+ 个功能，全部初始标记"失败"）+ `claude-progress.txt` + 初始 git 提交
   - Coding Agent 每个会话严格遵循：读取状态 → 处理一个功能 → 端到端测试 → git commit + 更新 progress notes
   - 每个会话是纯函数：`f(功能列表 + git history + progress notes) → 完成一个功能 + 更新记录`

   **方案 C（强制验证循环）**：
   - 实现 `PreCompletionChecklistMiddleware`：拦截 Agent 退出信号，代码逻辑检查测试运行状态
   - 实现 `LocalContextMiddleware`：启动时自动注入工作目录映射、可用工具列表、环境信息
   - 实现 `LoopDetectionMiddleware`：跟踪文件编辑次数，超过阈值 N 时注入重新思考提示

   **方案 D（动态子 Agent）**：
   - 主 Agent 配置三个特殊工具：`make_plan`、`execute_step_in_plan`、`update_plan`
   - 工具返回大数据时强制调用 `write_file` 缓冲，context 只保留文件名 + 描述指针
   - 主 Agent 识别复杂子任务时生成独立 LLM 线程，子 Agent 完成后只返回摘要
   - 非结构化数据批处理用扇出模式：并行调用小模型（如 Haiku），主 Agent 汇总

3. **验证与优化**：
   - 用 feature list 的 pass/fail 标准衡量每个功能是否真正完成
   - 监控 Agent 在第 50 步、第 100 步后的行为是否偏离目标（Durability 指标）
   - 用 Terminal Bench 2.0 等 benchmark 对比 harness 改动前后的分数变化
   - LangChain 的 deepagents-cli 自 2024 年 3 月以来被重新架构了五次，迭代是常态

---

### 💡 具体案例/数据

| 案例 | 数据 | 关键结论 |
|---|---|---|
| OpenAI Codex 团队 | 5 个月，100 万行代码，3 个工程师，平均每天合并 3.5 个 PR，0 行人工手写代码 | 最大挑战是"让 AI 写的代码可维护"，而非"让 AI 写代码" |
| LangChain deepagents-cli | GPT-5.2-Codex 固定不变，只改 harness，Terminal Bench 2.0：52.8% → 66.5%（+13.7 pp，26% 相对提升） | 模型固定时，harness 设计是效果的主要决定因素 |
| 模型升级对比 | GPT-5.2-Codex → GPT-5.3-Codex，SWE-Bench Pro：56.4% → 56.8%（+0.4 pp，0.7% 相对提升） | 模型升级边际收益远低于 harness 优化 |
| Anthropic Claude Code | 连续工作数天构建完整 Web 应用，功能需求文件 200+ 个 pass/fail 标准 | 外部化状态管理让跨会话长时程任务成为可能 |
| Hightouch 扇出模式 | 1000 个客户查询 × 500 tokens = 50 万 tokens（超出 context window）→ 1000 个并行子 Agent × 50 tokens 摘要 = 5 万 tokens（可管理） | 分层抽象比线性压缩节省 90% context，且无损 |
| Gartner 预测 | 超过 40% 的 Agentic AI 项目将在 2027 年底前被取消 | 生产可靠性问题是 Agent 项目失败的主因 |

---

### 📝 避坑指南

- ⚠️ **把 harness 当"胶水层"**：harness 不只是给 LLM 接工具的适配器，它包含 Context Engineering + Tool Engineering + Workflow Engineering 三个维度，缺任何一个都会导致长时程任务失败。
- ⚠️ **用 prompt 替代 middleware 做验证**：prompt 中写"记得测试"会被 Agent 忽略，因为训练数据偏差。必须用代码逻辑（middleware）强制拦截，Agent 无法绕过。
- ⚠️ **把所有信息压缩后塞进 context**：压缩是有损的，且中间 tokens 的 attention 会衰减。正确做法是构建"地图"（100 行 AGENTS.md）+ 按需检索，而非"百科全书式"注入。
- ⚠️ **期望 Agent 自己"记住"跨会话状态**：LLM 是无状态的，每个新会话都是"失忆"状态。必须用 git commits + progress notes + feature list 把状态外化为可读取的文件系统。
- ⚠️ **用 benchmark 单步准确率预测长时程可靠性**：MMLU 90 分的模型可能在第 50 步后完全跑偏。Durability 是独立于 Capability 的维度，必须单独测量。
- ⚠️ **认为更强的模型会让 harness 变简单**：OpenAI Codex 团队在 5 个月内构建了越来越复杂的 harness；LangChain deepagents 自 2024 年 3 月以来重新架构了五次。生产系统的要求远超 benchmark，模型越强，任务越复杂，harness 越精细。
- ⚠️ **单个 Agent 处理超出 context window 的复杂任务**：不要强行压缩，用动态子 Agent 隔离 context。主 Agent 只存"地图"，详细数据在子 Agent 的独立 context 中处理。
- ⚠️ **All-or-nothing 模式**：Agent 试图一次性完成所有功能，导致 context 耗尽，下一个 session 接手时发现代码写了一半、没有文档、无法继续。解决方案：强制"一次只处理一个功能"的约束。

---

### 🏷️ 行业标签

#HarnessEngineering #AIAgent #ContextEngineering #LLM #CodingAgent #OpenAI #Anthropic #LangChain #Hightouch #长时程任务 #生产可靠性 #WorkflowEngineering

---

**参考文献**:
- https://openai.com/index/harness-engineering/
- https://blog.langchain.com/improving-deep-agents-with-harness-engineering/
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- https://www.philschmid.de/agent-harness-2026
- https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
- https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027

---

---
