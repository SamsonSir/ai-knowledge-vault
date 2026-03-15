# Agent与技能系统

## 131. [2026-04-24]

## 📓 文章 6


> 文档 ID: `HXA6w8wNbihl7NkJbXAcV1Y7n7g`

**来源**: AI下半场，聊一聊 Agent 本质与变革 | 大白话技术科普系列@Jomy | **时间**: 2025-04-24 | **原文链接**: https://mp.weixin.qq.com/s/0X58GZqP...

---

### 📋 核心分析

**战略价值**: 用「Agent = LLM + Tools」这一最小公式，拆解 Agent 的技术本质、三种框架类型及未来生态走向，给出可直接对接白皮书和一线实践的认知底座。

**核心逻辑**:

- **LLM 天然无状态（stateless）**：每次请求处理完毕后模型内部恢复初始状态，「连续对话」是应用层把历史上下文打包塞进 Context 模拟出来的，记忆存在本地或云端，不在模型权重里。
- **Agent 的最小公式**：`Agent = LLM + Tools`。LLM 负责思考与调用决策，Tools 负责执行并返回结果。Anthropic/OpenAI/Google 三家白皮书定义各异，但都可以收敛到这个公式。
- **Human in the Loop → Human on the Loop 是质变**：旧模式「人-AI-人-AI」，人持续干预；新模式「人-AI-AI-AI」，人只设定初始目标，AI 自我循环完成后续所有步骤。这是 Agent 的核心本质之一。
- **Function Call 是自我循环的最小实现**：人提问 → AI 决定调用工具 → 工具执行返回结果 → AI 判断是否继续循环。每调用一次工具，AI 实际完成了两次回答，大部分客户端把这个过程折叠在同一界面里，造成「只有一次问答」的错觉。
- **三种 Agent 框架并非对立，而是组合使用**（详见下方表格）。
- **单 Agent（全自动）短期无法包打天下**，原因有二：① LLM 输出有随机性，多步骤任务误差累积放大；② 主流 LLM 训练/评估围绕单轮问答，缺乏「长链条现实任务」的高质量行动序列数据，连 OpenAI/Anthropic 也未必有足够数量。
- **Multi-Agent 是现阶段主流范式**：通过将任务拆解给多个垂直 Agent（各自有专属系统提示词+特定工具），再由编排层组合结果，换取可控性和可靠性。LangChain 调研显示，Agent 落地最大瓶颈是「性能质量（Performance Quality）」，根源在大模型本身。
- **Token 消耗将指数级暴增**：人机对话时代 Token 消耗受限于人类输入/阅读速度（约每秒 4 Token）；Agent 自我循环后取决于模型推理速度（每秒上百 Token+），且可 7×24 不间断，对并发能力和推理速度提出前所未有的挑战。
- **AI 交互模式从「即时问答」转向「异步任务委托」**：用户角色从「AI 创作者」变为「AI 消费者」，产品形态随之重构。
- **闭源与开源 Agent 生态将并行**：闭源路径——模型厂商直接提供 Agent 接口而非模型接口，通过特定工具训练+用户反馈形成数据飞轮（Alexander Doria & Databricks VP Naveen Rao 预测 2-3 年内发生）；开源路径——DeepSeek 等联合开发者社区，降低 Agent 开发门槛，覆盖海量长尾需求。

---

### 🎯 关键洞察

**为什么 LLM 无法替代 Agent（逻辑链）**:

> 原因：LLM 单次推理无法在同一次回答中既调用工具又获得工具返回结果
> → 动作：需要外部 Agent 框架代码接收请求、传递信息、维护循环状态
> → 结果：Agent 框架是 LLM 实现自我循环的必要基础设施，不是可选项

**为什么通往 AGI 必须经过 Agent**:

> 当前 LLM 训练以静态数据为主 → 缺乏「在真实世界中持续行动-反馈-调整」的经验数据 → Agent 在真实环境中做强化学习，才能获取第一手经验 → 这正是 Sutton 所说的「the Era of Experience（经验时代）」的核心逻辑

**垂直 Agent 生态爆发的结构性原因**:

> 复杂任务 → 需要多 Agent 协作 → 需要大量专注特定领域的垂直 Agent → 垂直 Agent 互联互通（ANP、A2A 协议）→ 开启下一波创业浪潮。百度云/阿里云/腾讯云/火山云密集接入 MCP 并押注 Agent 生态，本质是争夺垂直 Agent 开发平台的入口。

---

### 📦 三种 Agent 框架对比

| 框架类型 | 别名 | 代表产品 | 核心机制 | 透明度 | 适用场景 |
|---------|------|---------|---------|--------|---------|
| 手动 Agent 框架 | Workflow | Dify、Coze | 开发者预设每一步计划，LLM 在预设节点填充内容或做简单决策，Tools 执行步骤由人强制指定 | 白盒 | 确定性要求高、流程固定的任务 |
| 半自动 Agent 框架 | Multi-Agent System | Manus、扣子空间（规划模式） | 多个垂直 Agent（系统提示词+特定工具）各负责子任务，编排层组合执行过程和结果 | 灰盒 | 复杂任务拆解、需要可控性的场景 |
| 全自动 Agent 框架 | Single-Agent System / 通用 Agent | — | 只给模型设定最终目标，模型自主循环直到完成或遇到障碍，核心就是调用工具的几行代码 | 黑盒 | 模型能力足够强时的简单任务或实验场景 |

> 三种框架常组合使用：Multi-Agent 可嵌套 Workflow；Single-Agent 是 Workflow 和 Multi-Agent 的重要组成部分。

---

### 🛠️ 操作流程：理解 Function Call 自我循环的完整链路

1. **准备阶段**：为 LLM 配置可调用的 Tools 列表（函数签名+描述），构建 Agent 框架代码用于接收 LLM 的工具调用请求并执行。

2. **核心执行（一次完整循环）**:
   - 用户输入目标 → LLM 第一次推理：决定调用哪个工具、传入什么参数
   - Agent 框架接收调用请求 → 执行对应工具 → 获取返回结果
   - 将工具返回结果注入上下文 → LLM 第二次推理：基于结果判断任务是否完成，或继续下一轮循环
   - 重复上述过程直到 LLM 判断任务完成或触发终止条件

3. **验证与优化**:
   - 检查循环次数是否合理（过多循环 = 模型能力不足或任务拆解有问题）
   - 对于复杂任务，优先选择 Multi-Agent 框架而非 Single-Agent，以换取可控性
   - 在 Workflow 节点强制指定工具执行顺序，可显著提升确定性

---

### 💡 具体案例/数据

- **Simon Willison 的 280 字挑战**：在 X 上发起用 280 字给 Agent 下通用定义的挑战，Latent Space 主理人 Swyx 在 2025 AI Engineer Summit 上展示了评论区五花八门的答案，印证行业认知混乱现状。
- **LangChain Agent 落地调研**：影响 Agent 落地的最大瓶颈是「性能质量（Performance Quality）」，根源是大模型本身能力不足。
- **OpenAI AGI 路线图**：当前已发展到 Agent 时代阶段。
- **闭源 Agent 时间预测**：Alexander Doria（独立研究者）和 Naveen Rao（Databricks 副总裁）均判断，模型厂商从提供模型接口转向直接提供 Agent 接口，只需 2-3 年甚至更快。
- **GPT-5 传言**：可能以「LLM + 工具直接封装」的 Agent 接口形态出现，而非裸模型 API。
- **已无 API 接口的 Agent 产品**：OpenAI Deep Research、Anthropic Claude Code，均未提供 API 接口，印证顶尖厂商向闭源 Agent 生态转型的一致判断。

---

### 📝 避坑指南

- ⚠️ **「Model is Agent」是不严谨的表达**：准确说法是「Single-Agent 系统要替代 Workflow 和 Multi-Agent 系统」，且短期内不现实，因为 LLM 随机性导致多步骤误差累积，且缺乏长链条任务训练数据。
- ⚠️ **「通用 Agent 比垂直 Agent 更高级」是误解**：当前阶段垂直 Agent 的可控性和可靠性远优于通用 Agent，Multi-Agent 系统才是主流。
- ⚠️ **把所有自动执行任务的产品都叫 Agent 是泛化**：严格区分 Workflow（手动框架）、Multi-Agent（半自动）、Single-Agent（全自动）三种类型，它们的可控性、适用场景差异显著。
- ⚠️ **误以为 Function Call 只有一次 AI 问答**：每调用一次工具，LLM 实际完成两次推理，客户端界面折叠了这个过程。
- ⚠️ **Agent 训练数据的核心难点**：不能只看最终结果，必须评估模型获取信息、生成中间步骤、根据反馈调整计划、回溯重试的全过程行动序列数据，这类高质量数据极度稀缺。

---

### 📚 官方资料索引

| 文档 | 链接 |
|-----|------|
| OpenAI - A practical guide to building agents (2025.4) | https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf |
| Google - Agents (2024.12) | https://www.kaggle.com/whitepaper-agents |
| Anthropic - Building effective agents (2024.10) | https://www.anthropic.com/engineering/building-effective-agents |
| Lilian Weng - LLM Powered Autonomous Agents (2023.6) | https://lilianweng.github.io/posts/2023-06-23-agent |
| Shunyu Yao - The Second Half (2025.4) | https://ysymyth.github.io/The-Second-Half |
| Sutton - Welcome to the Era of Experience (2025.4) | https://storage.googleapis.com/deepmind-media/Era-of-Experience%20/The%20Era%20of%20Experience%20Paper.pdf |
| LangChain - How to think about agent frameworks (2025.4) | https://blog.langchain.dev/how-to-think-about-agent-frameworks |
| Alexander Doria - The Model is the Product (2025.3) | https://vintagedata.org/blog/posts/model-is-the-product |
| Alexander Doria - Actual LLM agents are coming (2025.3) | https://vintagedata.org/blog/posts/designing-llm-agents |
| Sutton - The Bitter Lesson (2019.3) | https://www.incompleteideas.net/IncIdeas/BitterLesson.html |
| TechCrunch - No one knows what the hell an AI agent is (2025.3) | https://techcrunch.com/2025/03/14/no-one-knows-what-the-hell-an-ai-agent-is |
| 李宏毅 - AI Agent (2025.3) | https://www.youtube.com/watch?v=M2Yg1kw Ppts |

---

### 🏷️ 行业标签
#Agent #LLM #MultiAgent #Workflow #FunctionCall #AgentFramework #VerticalAgent #OpenSource #ClosedSource #AGI #EraOfExperience #ScalingLaw

---

---
