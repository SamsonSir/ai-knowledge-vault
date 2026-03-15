# AI编程与开发工具

## 4. [2026-01-07]

## 📔 文章 5


> 文档 ID: `EecQwfUG3iOe5skLQI6c6zppnWy`

**来源**: 2025年LLM最全总结！Django创始人亲述：这一年，AI 改变了编程 | **时间**: 2026-01-07 | **原文链接**: https://mp.weixin.qq.com/s/-de7cMZt...

---

### 📋 核心分析

**战略价值**: Simon Willison（Django 联合创始人）对 2025 年 LLM 全领域的第一手观察，覆盖推理模型、代码 Agent、中国开源崛起、安全风险、新术语体系，是开发者制定 2026 年 AI 工具栈决策的最佳参考。

**核心逻辑**:

- **推理模型（RLVR）是 2025 年最大技术跃迁**：OpenAI o1（2024.9）→ o3/o3-mini/o4-mini（2025 初），核心机制是在可自动验证的奖励（数学题、代码谜题）上做强化学习，让模型自发学会"拆分中间步骤 + 来回推敲"。Karpathy 解释：这不是预训练扩展，而是推理时扩展（inference-scaling），算力从预训练转移到 RL 训练阶段。所有主要实验室 2025 年都发布了至少一个推理模型，部分支持推理/非推理模式切换旋钮。
- **推理 × 工具调用 = 真正可用的 Agent**：推理模型能规划多步任务 → 执行 → 对结果继续推理 → 调整计划。实际效果：复杂研究问题 ChatGPT GPT-5 Thinking 能直接回答；最棘手的 bug，给推理模型读取+执行代码权限，哪怕代码库庞大复杂也能诊断。
- **Claude Code 是 2025 年最重要的单一产品发布**（2025.2，甚至没有独立博客文章，藏在 Claude 3.7 Sonnet 发布公告第二条）：定义了"代码 Agent"范式——写代码 → 执行 → 检查结果 → 迭代。截至 2025.12.2，Anthropic 宣布 Claude Code 带来 **10 亿美元年化收入**，一个 CLI 工具达到此量级完全出乎预料。
- **代码 Agent 生态全面爆发**，主要产品矩阵：

| 类型 | 产品 | 厂商 |
|------|------|------|
| 命令行代码 Agent | Claude Code | Anthropic |
| 命令行代码 Agent | Codex CLI（`--yolo` = `--dangerously-bypass-approvals-and-sandbox`） | OpenAI |
| 命令行代码 Agent | Gemini CLI | Google |
| 命令行代码 Agent | Qwen Code（fork 自 Gemini CLI） | 阿里巴巴 |
| 命令行代码 Agent | Mistral Vibe | Mistral |
| 命令行代码 Agent（独立） | GitHub Copilot CLI、Amp、OpenCode、OpenHands CLI、Pi | 多方 |
| 异步代码 Agent（云端） | 网页版 Claude Code（2025.10） | Anthropic |
| 异步代码 Agent（云端） | Codex web（原 Codex cloud，2025.5） | OpenAI |
| 异步代码 Agent（云端） | Jules（2025.5） | Google |
| IDE 集成 | Zed、VS Code、Cursor | 多方 |

- **中国开源模型 2025 年登顶**：Artificial Analysis 截至 2025.12.30 开源模型排名前五全为中国模型（GLM-4.7、Kimi K2 Thinking、MiMo-V2-Flash、DeepSeek V3.2、MiniMax-M2.1），排名最高的非中国模型是 OpenAI gpt-oss-120B（high），排第六。关键节点：DeepSeek 3（2024 圣诞，训练成本约 **550 万美元**）→ DeepSeek R1（2025.1.20，引发 NVIDIA 市值单日蒸发约 **5930 亿美元**）。重点关注实验室：DeepSeek、阿里 Qwen（Qwen3）、月之暗面（Kimi K2）、智谱 AI（GLM-4.5/4.6/4.7）、MiniMax（M2）、元石 AI（XBai o4）。许可证：Qwen 多数用 Apache 2.0，DeepSeek/智谱 AI 用 MIT。
- **AI 能完成的任务时长每 7 个月翻倍**（METR 数据）：2024 年最好模型上限约 30 分钟任务；2025 年 GPT-5、GPT-5.1 Codex Max、Claude Opus 4.5 能完成人类需要数小时的任务。一致性测试套件是解锁这个能力的关键——给代码 Agent 一个现有测试套件对照，效果大幅提升（已验证：html5lib 测试、MicroQuickJS 测试套件、WebAssembly 规范测试集）。
- **YOLO 模式与风险常态化**：大多数代码 Agent 默认每步要求确认；YOLO 模式（自动确认）感觉像完全不同的产品，但风险真实存在（删除 Home 目录、提示词注入窃取凭证）。安全研究员 Johann Rehberger 提出"风险常态化"概念（源自社会学家 Diane Vaughan 对 1986 年挑战者号灾难的研究）：反复接触风险行为而无负面后果 → 接受风险为正常 → 接近自己的"挑战者号时刻"。
- **MCP 爆红但可能被 Skills/Bash 取代**：MCP（Anthropic 2024.11 发布）2025 年初爆炸式流行，5 月内 OpenAI/Anthropic/Mistral 八天内相继推出 API 级 MCP 支持。但实际使用中，`gh`、`playwright` 等 CLI 工具比对应 MCP 更好用；Anthropic 的 Skills 机制（一个 Markdown 文件 + 可选脚本，比 MCP 的 web 服务器 + 复杂 JSON 负载轻得多）可能更重要。MCP 于 2025.12 初捐赠给 Agentic AI Foundation；Skills 于 2025.12.18 升级为"开放格式"。
- **图片生成：GPT-image-1 引爆消费市场，Nano Banana Pro 成专业工具**：2025.3 ChatGPT 图片编辑功能上线，**一周新增 1 亿注册用户，高峰期一小时 100 万账号创建**。"吉卜力化"等技巧反复爆火。API 版本：gpt-image-1（3 月）→ gpt-image-1-mini（10 月）→ gpt-image-1.5（12.16）。Google Nano Banana（代号，API 名 Gemini 2.5 Flash Image）：3 月预览，8.26 正式可用，11 月推出 Nano Banana Pro——能生成有用文字、详细信息图，是目前遵循图片编辑指令最好的模型。开源竞品：Qwen-Image（8.4）→ Qwen-Image-Edit（8.19）→ Qwen-Image-Edit-2511（11 月）→ Qwen-Image-2512（12.30），可在消费级硬件运行。
- **学术竞赛金牌**：2025.7 OpenAI 和 Google Gemini 推理模型在 IMO（国际数学奥林匹克，1959 年起每年举办）取得金牌水平，题目为竞赛专属新题，不可能在训练数据中，且两个模型均未使用工具，纯内部推理。2025.9 在 ICPC（国际大学生程序设计竞赛）取得类似成就，有代码执行环境但无互联网访问。

---

### 🎯 关键洞察

**Llama 的衰落**：Llama 4（2025.4）发布令人失望，Scout（109B）和 Maverick（400B）太大，量化后仍无法在 64GB Mac 上运行，失去了"可在笔记本运行"的核心优势。LM Studio 最受欢迎模型列表中无一来自 Meta；Ollama 上最受欢迎的仍是 Llama 3.1。Meta 2025 年 AI 新闻主要是内部政治和为超级智能实验室招聘，Llama 路线图不明朗。

**OpenAI 失去全面领先**：图片模型被 Nano Banana Pro 超越；代码方面多数开发者认为 Claude Opus 4.5 略领先 GPT-5.2 Codex；开源模型 gpt-oss 落后中国实验室；音频领先受 Gemini Live API 威胁。唯一优势：消费者心智份额（ChatGPT 品牌认知远超 Gemini/Claude）。2025.12 OpenAI 宣布进入"红色警戒"应对 Gemini 3，推迟新项目专注核心竞争。

**Google Gemini 全面崛起**：Gemini 2.0 → 2.5 → 3.0，全系列支持 1,000,000+ token 多模态输入；核心硬件优势是自研 TPU（其他实验室全用 NVIDIA GPU），训练和推理成本结构性更低

---

---
