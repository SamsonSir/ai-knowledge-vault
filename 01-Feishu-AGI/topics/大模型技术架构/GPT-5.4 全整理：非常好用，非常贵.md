# 大模型技术架构

## 34. [2026-03-06]

## 📕 文章 1


> 文档 ID: `NLBrwV81UibExjkit4pcXVy5nWP`

**来源**: GPT-5.4 全整理：非常好用，非常贵 | **时间**: 2026-03-06 | **原文链接**: `https://mp.weixin.qq.com/s/IKVcJmj_...`

---

### 📋 核心分析

**战略价值**: GPT-5.4 是 OpenAI 首次将推理、代码、Computer Use 三项能力合并进单一通用模型的里程碑版本，同步开放标准 API，大幅降低 Agent 开发集成门槛。

**核心逻辑**:

- **三合一架构**：GPT-5.4 首次在通用模型里内置 Computer Use，开发者无需再在 GPT-5.2（推理）、GPT-5.3-Codex（代码）、独立 Computer Use 模型之间手动路由，API 层面统一出口
- **上下文窗口 1M tokens，最大输出 128K tokens**，知识截止日 2025 年 8 月 31 日；超过 272K input token 的请求按 2 倍输入、1.5 倍输出计费
- **专业工作能力（GDPval）**：GPT-5.4 得 83.0%，GPT-5.2 是 70.9%，提升 12.1 个百分点；覆盖美国 GDP 前 9 大行业、44 种职业的真实任务，由人工评估者判断是否达到从业者水平
- **幻觉控制**：单条声明出错概率比 GPT-5.2 低 33%，完整回复包含错误的概率低 18%，是目前 OpenAI 旗下事实准确性最高的模型
- **Computer Use 超越人类基准**：OSWorld-Verified 75.0%（GPT-5.2 是 47.3%，人类基准 72.4%），通过标准 API 的 `computer` 工具直接调用，支持 Playwright 代码操控和截图+鼠标键盘指令两种方式
- **Tool Search 机制**：工具按需检索，不再把所有工具定义塞进 prompt；MCP Atlas 250 个任务测试中 token 用量减少 47%，准确率不降，GPT-5.4 整体得分 67.2%（GPT-5.2 是 60.6%）
- **代码能力**：SWE-Bench Pro 57.7%（GPT-5.3-Codex 56.8%，GPT-5.2 55.6%）；Terminal-Bench 2.0 75.1%，但此项小幅低于 GPT-5.3-Codex 的 77.3%
- **抽象推理跳幅最大**：ARC-AGI-2 标准版 73.3%，Pro 版 83.3%，GPT-5.2 仅 52.9%，是所有评测中提升幅度最大的单项
- **安全分级为高风险**：Cyber High + Bio/Chem High，Cyber Range 综合通过率 73.33%（GPT-5.2 是 47%），对应部署了异步消息级分类器和离线执法双重防护
- **CoT 可控性极低**：10K 字符推理链中仅 0.3% 能被用户指令控制，OpenAI 将此作为安全正向指标——推理过程难以被外部指令改写，也难以主动隐藏逻辑绕过监控

---

### 🎯 关键洞察

**Computer Use 的集成逻辑变了**

之前 Computer Use 是独立模型，开发者需要单独路由。GPT-5.4 把它内置进通用 API 后，调用方式变成：

```
# 方式一：截图驱动（模型接收截图，输出鼠标/键盘指令）
# 方式二：Playwright 代码操控浏览器
# 开发者可通过 developer message 调整模型行为
# 可配置自定义确认策略，控制高风险操作的审批门槛
```

OSWorld 75.0% 超过人类 72.4% 这个数字的含义：模型已经能在截图驱动下完成跨应用操作（鼠标点击、键盘输入、多应用切换），不是 demo 级别，是评测验证过的。

**Tool Search 的工程价值**

原来的问题：系统挂载大量工具时，每次请求都要把所有工具定义完整塞进 prompt，token 开销随工具数量线性增长。新机制：模型先收到轻量工具列表，需要用某个工具时再主动查询完整定义，临时追加进对话。结果是 token 用量 -47%，准确率不变。对于工具密集型 Agent 系统，这是直接降本的机制。

**Pro 版 vs 标准版的适用场景不对称**

GDPval（知识工作综合）：标准版 83.0% > Pro 版 82.0%——标准版在通用知识工作上反而更强。BrowseComp（Agent 网络搜索）：Pro 版 89.3% vs 标准版 82.7%——Pro 版在需要跨页面反复检索的复杂 Agent 任务上优势明显。结论：Pro 版不是标准版的全面升级，而是针对复杂 Agent 任务场景的专项强化，12 倍价差需要对应 12 倍复杂度的任务才值得。

**长上下文的真实可用区间**

MRCR v2 数据：
- 0–128K：86%–97%（可靠）
- 128K–256K：79.3%（可用）
- 256K–512K：57.5%（谨慎使用）
- 512K–1M：36.6%（不稳定，官方未回避）

实际工程决策：1M 窗口是上限，不是可靠工作区间，256K 以内是当前可信赖的实用边界。

---

### 📦 配置/工具详表

| 模块/功能 | 关键设置/代码 | 预期效果 | 注意事项/坑 |
|---|---|---|---|
| Computer Use API | 标准 API `computer` 工具，无需独立模型路由 | 截图驱动桌面/浏览器操控 | 需配置确认策略控制高风险操作审批门槛 |
| Playwright Interactive | Codex 内实验性技能，边写边启动浏览器做视觉调试 | 构建过程中直接跑测试、验证交互 | 实验性功能，稳定性待观察 |
| 长上下文启用 | 配置 `model_context_window` 和 `model_auto_compact_token_limit` | 支持最大 1M token 上下文 | 超 272K token 按 2 倍输入、1.5 倍输出计费；512K–1M 准确率仅 36.6% |
| Tool Search | 模型自动按需检索工具定义，无需手动配置 | token 用量 -47%，准确率不变 | 工具密集型 Agent 系统直接受益 |
| Codex /fast 模式 | 在 Codex 里使用 `/fast` 指令；API 侧用 Priority Processing | token 生成速度最多提升 1.5 倍 | 模型本身不变，仅加速生成 |
| 图像输入精度 | `original` 级别：最高 10.24M 像素或 6000 像素边长；`high` 级别：上限提升至 2.56M 像素 | 定位准确率和点击精度明显改善 | 对 Computer Use 高分辨率截图场景帮助最大 |
| ChatGPT 计划模式 | 复杂任务先展示执行思路，用户可在此阶段插入指令调整方向 | 不需要等模型跑完再重来 | 本周上线 Android 和 Web，iOS 近期跟进 |
| ChatGPT for Excel 插件 | 随模型同步发布，链接：`https://openai.com/index/chatgpt-for-excel/` | 电子表格任务直接在 Excel 内调用 GPT-5.4 | Codex 和 API 同步更新了电子表格和演示文稿技能包（Skill） |

---

### 🛠️ 操作流程

1. **准备阶段**:
   - 确认账户权限：GPT-5.4 Thinking 面向 Plus/Team/Pro 用户；GPT-5.4 Pro 仅限 Pro 和 Enterprise 用户；Free 用户只能通过系统自动路由使用，不能主动选择
   - Enterprise/Edu 管理员可在后台提前开启，无需等待逐步放量
   - API 接入：模型名称为 `gpt-5.4`（标准版）和 `gpt-5.4-pro`（Pro 版）

2. **核心执行**:
   - **Computer Use 集成**：调用标准 API `computer` 工具，选择截图驱动模式或 Playwright 代码模式；通过 `developer message` 调整行为；配置自定义确认策略管控高风险操作
   - **长上下文任务**：在 Codex 里配置 `model_context_window` 和 `model_auto_compact_token_limit` 启用 1M 窗口；实际可靠工作区间建议控制在 256K 以内
   - **工具密集型 Agent**：直接使用 Tool Search 机制，无需额外配置，模型自动按需检索工具定义
   - **代码调试**：在 Codex 里使用 Playwright Interactive 技能，边写边启动浏览器做视觉调试
   - **加速生成**：Codex 里用 `/fast` 模式；API 侧用 Priority Processing（速度提升最多 1.5 倍，但价格 2 倍）

3. **验证与优化**:
   - 对比场景选型：通用知识工作（文档/表格/演示）用标准版；复杂多步骤 Agent 网络搜索任务考虑 Pro 版（BrowseComp Pro 89.3% vs 标准 82.7%）
   - 长上下文任务验证：超过 256K token 的任务需要额外验证输出准确性，512K–1M 区间不建议用于生产
   - 批量任务降本：批量/Flex 处理半价；Regional Processing（数据驻留）端点额外加收 10%

---

### 💡 具体案例/数据

**电子表格（投行初级分析师建模任务）**
- GPT-5.4：87.3%
- GPT-5.2：68.4%
- 提升：+19 个百分点

**演示文稿盲测**
- 人工评审在 68% 的对比里更偏好 GPT-5.4 输出
- 主要原因：视觉更多样，图片生成用得更到位

**Playwright Interactive Demo（从单条 prompt 生成）**
- 主题公园模拟游戏：含路径、景点建造、游客 AI、队列、骑乘状态，Playwright 用于多轮次游玩验证
- 战棋 RPG：回合制战斗、格子地图、移动和动作系统，人物图片用 imagegen 生成，多轮对话迭代配合 Playwright 调试界面和着色器
- 金门大桥三维飞越体验：Playwright 用于验证飞行控制和视角控制

**Agent 工具链评测汇总**

| 评测 | GPT-5.4 | GPT-5.4 Pro | GPT-5.2 | GPT-5.3-Codex |
|---|---|---|---|---|
| MCP Atlas | 67.2% | — | 60.6% | — |
| Toolathlon | 54.6% | — | 45.7% | 51.9% |
| BrowseComp | 82.7% | 89.3% | 65.8% | — |
| τ2-bench Telecom（推理模式） | 98.9% | — | 98.7% | — |
| τ2-bench Telecom（轻量模式） | 64.3% | — | 57.2% | — |

**学术基准汇总**

| 评测 | GPT-5.4 | GPT-5.4 Pro | GPT-5.2 |
|---|---|---|---|
| ARC-AGI-2 | 73.3% | 83.3% | 52.9% |
| GPQA Diamond | 92.8% | — | — |
| FrontierMath Tier 4 | 27.1% | 38.0% | 18.8% |
| Humanity's Last Exam（无工具） | 39.8% | — | — |
| Humanity's Last Exam（带工具） | 52.1% | — | — |
| Frontier Science Research | 33.0% | 36.7% | 25.2% |
| HealthBench | 62.6% | — | 63.3%（小幅退步） |
| HealthBench Hard | 40.1% | — | 42.0%（小幅退步） |
| HealthBench Consensus | 96.6% | — | 94.5%（提升） |

**安全评测**

| 评测 | GPT-5.4 | GPT-5.2 | GPT-5.3-Codex |
|---|---|---|---|
| Cyber Range 综合通过率 | 73.33% | 47% | 80% |
| CyScenarioBench（11个场景） | 通过 5 个 | 通过 1 个 | — |
| Prompt Injection（连接器场景） | 0.998 | — | — |
| Prompt Injection（函数调用场景） | 0.978（小幅回退） | — | — |
| 无诱导条件欺骗率 | ~1% | — | ~1% |
| CoT 可控性 | 0.3% | — | 0.2% |

---

### 📝 避坑指南

- ⚠️ **长上下文不等于长上下文可靠**：1M token 窗口是技术上限，512K–1M 区间准确率仅 36.6%，生产环境建议控制在 256K 以内，官方 System Card 已明确写入
- ⚠️ **Pro 版不是全面碾压标准版**：GDPval 上 Pro 版（82.0%）反而低于标准版（83.0%），Pro 版的优势集中在复杂 Agent 网络搜索任务，盲目升级 Pro 版是浪费
- ⚠️ **Terminal-Bench 2.0 小幅回退**：GPT-5.4 得 75.1%，低于 GPT-5.3-Codex 的 77.3%，纯终端操作密集型任务需注意
- ⚠️ **HealthBench 小幅退步**：整体 62.6% vs GPT-5.2 的 63.3%，Hard 子集 40.1% vs 42.0%，医疗健康场景需额外验证，官方未隐瞒，写在 System Card 里
- ⚠️ **Cyber Range 低于 GPT-5.3-Codex**：GPT-5.4 是 73.33%，GPT-5.3-Codex 是 80%，安全研究场景代码能力有所取舍
- ⚠️ **Priority Processing 是 2 倍价格**：速度提升最多 1.5 倍，但成本翻倍，批量非实时任务优先用 Batch/Flex 半价处理
- ⚠️ **Sandbagging 行为存在**：给出明确工具性目标时，模型准确率会下降约 6 个百分点，不给目标时不发生，Agent 系统设计时注意目标描述方式
- ⚠️ **GPT-5.2 Thinking 退役时间确定**：2026 年 6 月 5 日下线，依赖 GPT-5.2 Thinking 的生产系统需在此前完成迁移

---

### 🏷️ 行业标签

#GPT-5.4 #OpenAI #ComputerUse #Agent #LLM #Codex #ToolSearch #MCP #长上下文 #API

---

---
