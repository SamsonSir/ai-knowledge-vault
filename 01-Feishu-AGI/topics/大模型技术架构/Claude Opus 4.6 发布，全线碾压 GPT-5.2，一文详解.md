# 大模型技术架构

## 16. [2026-02-05]

## 📕 文章 1


> 文档 ID: `TGEQwJQK0ilUiPkEeuUcEpGHnue`

**来源**: Claude Opus 4.6 发布，全线碾压 GPT-5.2，一文详解 | **时间**: 2026-02-06 | **原文链接**: `https://mp.weixin.qq.com/s/L3Tbd4KM...`

---

### 📋 核心分析

**战略价值**: Anthropic 发布 Opus 4.6，在知识工作、Agent 编码、多学科推理、长上下文四大维度全面超越 GPT-5.2，同步推出 1M 上下文、128K 输出、adaptive thinking、context compaction 等工业级 API 能力，并将产品线延伸至 Excel/PowerPoint/多 Agent 协作。

**核心逻辑**:

- **GDPval-AA 知识工作评测**：Opus 4.6 领先 GPT-5.2 约 144 Elo，领先自家 Opus 4.5 约 190 Elo，换算胜率约 70%，覆盖金融、法律等专业领域子项全面领先
- **Agent 搜索（BrowseComp）**：单 Agent 模式已领先同类，叠加多 Agent 框架后得分达 86.8%，测的是在网络上检索难以找到信息的实际能力
- **Agent 编码（Terminal-Bench 2.0）**：拿下最高分；SWE-bench Verified 平均跑 25 轮，调整 prompt 后最高达 81.42%
- **多学科推理（Humanity's Last Exam）**：跑分时启用 web search + code execution + context compaction（50K token 触发，最大 3M token），使用 max effort + adaptive thinking 组合
- **ARC AGI 2**：使用 max effort + 120K thinking budget 配置
- **长上下文突破（MRCR v2 八针 1M 测试）**：Opus 4.6 得分 76%，Sonnet 4.5 同测试仅 18.5%，差距达 4 倍；这是 Opus 级模型首次支持 1M token 上下文（beta），能在数十万 token 中追踪 Opus 4.5 会漏掉的细节
- **其他专项评测**：OpenRCA（复杂软件故障根因诊断，全匹配得 1 分否则 0 分）、MCP Atlas 长期连贯性（max effort 最高分，high effort 达 62.7%）、CyberGym 网络安全（默认 effort + temperature + top_p，配备 think tool 做多轮交叉思考）、多语言编码、生命科学均有跑分数据
- **内部使用观察**：模型自动将算力集中在任务最难部分，简单部分快速通过；但简单任务上存在「想太多」问题，Anthropic 建议此类场景将 effort 从默认 high 调为 medium
- **Early Access 合作伙伴反馈**：三个核心点——能自主工作无需手把手、能完成前代模型搞不定的任务、改变了团队协作方式
- **安全评估**：对齐偏差率（欺骗、谄媚、配合滥用）与 Opus 4.5 持平；over-refusal 率是近期 Claude 模型最低；首次引入可解释性（interpretability）技术分析模型底层行为；新增 6 个网络安全探针追踪潜在滥用；同时用该模型为开源软件找漏洞打补丁

---

### 🎯 关键洞察

**长上下文的核心突破**：以往 1M token 上下文的问题不是「支不支持」，而是 context rot——上下文越长，模型表现越差。Opus 4.6 在 MRCR v2 八针 1M 测试中以 76% vs 18.5% 的比分证明这个问题得到了实质性解决，而非仅仅是参数上的扩展。

**Adaptive Thinking 的工程意义**：之前 extended thinking 是二元开关，现在变成了连续控制——模型自己判断何时需要深度推理，何时快速通过。这对 API 调用成本控制有直接影响，开发者不再需要为所有请求支付深度推理的代价。

**Context Compaction 的 Agent 价值**：长对话和 Agent 任务最大的工程痛点是上下文窗口撞顶。Context compaction 自动将旧上下文压缩为摘要替换，触发阈值可配置，这让长时间运行的 Agent 任务在工程上变得可行。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| 模型 API 标识 | `claude-opus-4-6` | 调用 Opus 4.6 | 在 claude.ai / API / AWS / GCP / Azure 均可用 |
| Effort 控制 | `low` / `medium` / `high`（默认）/ `max` | 控制推理深度与成本 | 简单任务建议调为 `medium`，避免「想太多」增加延迟和成本 |
| Adaptive Thinking | 默认 `high` effort 下自动启用 | 模型自判断是否需要深度推理 | 无需手动开关，effort 档位决定触发频率 |
| Context Compaction | beta，触发阈值可配置，默认 50K token 触发，最大压缩至 3M token | 自动压缩旧上下文，防止窗口撞顶 | 适合长 Agent 任务；摘要替换会损失部分细节 |
| 1M 上下文 | beta，超过 200K token 部分单独计费 | 处理超长文档、多文件代码库 | 200K 以内价格不变；超出部分价格上浮 |
| 128K 输出 | 无需额外配置 | 大输出任务无需拆分多次请求 | 替代之前需要多轮请求的大输出场景 |
| US-only Inference | 可选，价格 1.1 倍 | 数据留在美国境内 | 有合规要求的场景使用 |
| Humanity's Last Exam 跑分配置 | web search + code execution + context compaction（50K 触发，最大 3M）+ max effort + adaptive thinking | 多学科推理最高分 | 这是评测配置，生产环境按需裁剪 |
| ARC AGI 2 跑分配置 | max effort + 120K thinking budget | AGI 推理评测最高分 | thinking budget 直接影响成本 |
| CyberGym 跑分配置 | 默认 effort + 默认 temperature + 默认 top_p + think tool（多轮交叉思考） | 网络安全能力评测 | 未开启 extended thinking |
| MCP Atlas 长期连贯性 | max effort 最高分；high effort 达 62.7% | 长期任务连贯性 | high effort 已领先，max effort 进一步提升 |

---

### 🛠️ 操作流程

**1. 准备阶段**

- 确认调用入口：claude.ai、Claude API、AWS Bedrock、GCP Vertex AI、Azure 均已上线
- 模型标识符：`claude-opus-4-6`
- 确认任务复杂度，预判所需 effort 档位（简单任务 → `medium`，复杂推理 → `high` 或 `max`）

**2. 核心执行**

- 普通任务：默认 `high` effort，adaptive thinking 自动介入
- 简单/高频任务：显式设置 `effort: medium`，降低延迟和成本
- 极限推理任务（如 ARC AGI 类）：`effort: max` + 设置 `thinking_budget: 120000`
- 长 Agent 任务：启用 context compaction（beta），配置触发阈值（默认 50K token），上限可设至 3M token
- 超长文档处理：使用 1M 上下文（beta），注意 200K token 以上部分计费变化
- 大输出任务：直接使用，128K 输出上限无需拆分请求

**3. 多 Agent 场景（Claude Code agent teams）**

- 将任务拆分为可独立执行的子任务（如大规模 code review）
- 同时启动多个 Agent 并行工作、自主协调
- 使用 `Shift+Up/Down` 或 `tmux` 随时接管任意子 Agent
- 当前为 research preview 阶段

**4. Excel + PowerPoint 组合工作流**

- 先用 Claude in Excel 处理非结构化数据、推断表结构、设置条件格式和数据验证
- 再用 Claude in PowerPoint（research preview，Max/Team/Enterprise 可用）读取版式/字体/母版，保持品牌一致性，从数据直接生成完整 deck

**5. 验证与优化**

- 长上下文任务：用 MRCR 类多针检索测试验证模型是否真正追踪到关键信息
- Agent 任务：观察是否出现「想太多」现象（延迟异常高），若有则降 effort 档位
- 安全敏感场景：参考 system card 了解对齐偏差率和网络安全探针细节：`https://www.anthropic.com/claude-opus-4-6-system-card`

---

### 💡 具体案例/数据

| 评测 | Opus 4.6 | 对比对象 | 差距 |
|---|---|---|---|
| GDPval-AA vs GPT-5.2 | 领先 144 Elo | GPT-5.2 | 胜率约 70% |
| GDPval-AA vs Opus 4.5 | 领先 190 Elo | Opus 4.5 | — |
| BrowseComp（多 Agent） | 86.8% | — | 单 Agent 已领先，多 Agent 进一步提升 |
| SWE-bench Verified | 81.42%（调整 prompt 后最高） | — | 平均跑 25 轮 |
| MRCR v2 八针 1M | 76% | Sonnet 4.5：18.5% | 差距 4 倍 |
| MCP Atlas（high effort） | 62.7% | — | max effort 更高 |
| Terminal-Bench 2.0 | 最高分 | 全部参测模型 | — |
| Humanity's Last Exam | 最高分 | 全部参测模型 | 配置：web search + code execution + context compaction + max effort + adaptive thinking |
| ARC AGI 2 | 最高分 | 全部参测模型 | 配置：max effort + 120K thinking budget |

---

### 📝 避坑指南

- ⚠️ **简单任务别用默认 effort**：Opus 4.6 默认 `high` effort，简单任务会「想太多」，显著增加延迟和成本，明确设置 `effort: medium`
- ⚠️ **1M 上下文是 beta**：生产环境谨慎依赖，200K token 以上部分计费上浮，评估实际需求再开启
- ⚠️ **Context compaction 会损失细节**：压缩旧上下文本质是摘要替换，对需要精确回溯早期对话内容的任务要谨慎，触发阈值需根据任务特性配置
- ⚠️ **Agent teams 是 research preview**：Claude Code 多 Agent 功能尚未 GA，不建议用于生产关键路径
- ⚠️ **Claude in PowerPoint 是 research preview**：仅 Max/Team/Enterprise 可用，功能尚不稳定
- ⚠️ **网络安全能力提升带来的双刃剑**：Anthropic 额外开发了 6 个新网络安全探针追踪潜在滥用，安全敏感场景需关注 system card 更新
- ⚠️ **US-only inference 有溢价**：需要数据留在美国境内的场景价格为标准价 1.1 倍，按需选择

---

### 🏷️ 行业标签

#Claude #Anthropic #LLM评测 #AgentAI #长上下文 #AdaptiveThinking #ContextCompaction #ClaudeCode #多Agent #GPT对比

---

---
